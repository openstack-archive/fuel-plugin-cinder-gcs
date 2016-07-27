#    Copyright 2013 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


import os
import re
import time
import random

from fuelweb_test import settings
from fuelweb_test.settings import DEPLOYMENT_MODE
from fuelweb_test.tests.base_test_case import TestBasic
from fuelweb_test import logger
from helpers import gcs_settings
from devops.helpers.helpers import wait


class GcsTestBase(TestBasic):
    """GcsTestBase"""  # TODO documentation

    def create_gcs_non_ha_cluster(self):
        logger.info('Creating GCS non HA cluster...')
        segment_type = 'vlan'
        cluster_id = self.fuel_web.create_cluster(
            name=self.__class__.__name__,
            mode=DEPLOYMENT_MODE,
            settings={
                "ceilometer": False,
                "net_provider": 'neutron',
                "net_segment_type": segment_type,
                'tenant': 'gcs',
                'user': 'gcs',
                'password': 'gcs123GCS',
                'assign_to_all_nodes': True
            }
        )

        # self._set_attributes(cluster_id, 'gamma')

        self.fuel_web.update_nodes(
            cluster_id,
            {
                'slave-01': ['controller'],
                'slave-02': ['compute'],
                'slave-03': ['cinder']
            }
        )

        return cluster_id

    def create_gcs_ha_cluster(self):
        logger.info('Creating GCS HA cluster...')
        segment_type = 'vlan'
        cluster_id = self.fuel_web.create_cluster(
            name=self.__class__.__name__,
            mode=DEPLOYMENT_MODE,
            settings={
                "ceilometer": False,
                "net_provider": 'neutron',
                "net_segment_type": segment_type,
                'tenant': 'gcs',
                'user': 'gcs',
                'password': 'gcs123GCS',
                'assign_to_all_nodes': True
            }
        )

        # self._set_attributes(cluster_id, 'gamma')

        self.fuel_web.update_nodes(
            cluster_id,
            {
                'slave-01': ['controller'],
                'slave-02': ['controller'],
                'slave-03': ['controller'],
                'slave-04': ['compute'],
                'slave-05': ['cinder']
            }
        )

        return cluster_id

    @staticmethod
    def get_test_list():
        logger.info('Getting list of tests...')
        f = open(gcs_settings.tempest_cmds['test_list_path_on_lab'], 'r')
        test_list = f.read()
        f.close()
        return test_list

    @staticmethod
    def set_test_list(remote, data, file_name='test_list'):
        logger.info('Setting list of tests...')
        for i in data.strip('\n').split('\n'):
            remote.execute(
                's=\"{data}\"; echo $s >> /home/{file_name}'.format(data=i+'\n',
                                                                    file_name=file_name))

    def get_remote(self, node):
        logger.info('Getting a remote to {0}'.format(node))
        if node == 'master':
            environment = self.env
            remote = environment.d_env.get_admin_remote()
        else:
            remote = self.fuel_web.get_ssh_for_node(node)
        return remote

    @staticmethod
    def exec_with_verification(remote, cmd, ex_code_expected=0):
        logger.info('Executing command:\n {0}'.format(cmd))
        ex_code = remote.execute(cmd)
        assert ex_code['exit_code'] == ex_code_expected

    @staticmethod
    def generate_report_name():
        logger.info('Generating report...')
        scenario_name = os.environ['MY_GROUP']
        current_time = time.strftime('%H_%M_%S-%d_%m_%y_%Z')
        report_name = 'tempest_report_for_{}_{}'.format(scenario_name,
                                                        current_time)
        return report_name

    @staticmethod
    def get_container_id(remote):
        logger.info('Getting container ID...')
        docker_data = remote.execute('docker ps -a')
        return docker_data['stdout'][1].split(' ')[0]

    @staticmethod
    def upload_creds(remote):
        logger.info('Uploading credentials file to fuel master node.')
        pwd = os.getcwd()
        file_name = os.environ['GCS_CREDS_FILE']
        source = os.path.join(pwd, file_name)
        remote.execute('mkdir gcs')
        remote.upload(source, '/root/gcs/')

    def install_plugin(self):
        master_remote = self.get_remote('master')
        logger.info('Installing plugin on master...')
        self.upload_creds(master_remote)
        self.exec_with_verification(
            remote=master_remote,
            cmd=gcs_settings.plugin_install_steps['install_deps'])
        self.exec_with_verification(
            remote=master_remote,
            cmd=gcs_settings.plugin_install_steps['install_fpb'])
        self.exec_with_verification(
            remote=master_remote,
            cmd=gcs_settings.plugin_install_steps['clone_plugin_repo'])
        self.exec_with_verification(
            remote=master_remote,
            cmd=gcs_settings.plugin_install_steps['build_plugin'])
        if os.environ['IS_HOTPLUGGABLE']:
            self.exec_with_verification(
                remote=master_remote,
                cmd=gcs_settings.plugin_install_steps['is_hotpluggable_fix'])
        self.exec_with_verification(
            remote=master_remote,
            cmd=gcs_settings.plugin_install_steps['fuel_install'].format(
                rpm_name=gcs_settings.rpm_name))

    def run_tempest(self, cluster_id):
        logger.info('Starting Tempest execution...')
        role = ['controller']
        log_folder = os.environ['REPORTS_FOLD']
        report_name = self.generate_report_name()
        nodes = self._get_pcs_master_node_by_role(cluster_id=cluster_id,
                                                  role=role)
        controller_remote = self.get_remote(nodes[0].name)
        master_remote = self.get_remote('master')

        self.exec_with_verification(
            remote=controller_remote,
            cmd=gcs_settings.tempest_cmds['install_git'])

        self.exec_with_verification(
            remote=controller_remote,
            cmd=gcs_settings.tempest_cmds['clone_rally'])
        test_list = self.get_test_list()
        self.set_test_list(controller_remote, test_list)

        self.exec_with_verification(
            remote=controller_remote,
            cmd=gcs_settings.tempest_cmds['fixate_tempest_ver'].format(
                tempest_commit=gcs_settings.tempest_commit))

        self.exec_with_verification(
            remote=controller_remote,
            cmd=gcs_settings.tempest_cmds['fix_docker_rally'].format(
                rally_commit=gcs_settings.rally_commit))

        self.exec_with_verification(
            remote=controller_remote,
            cmd=gcs_settings.tempest_cmds['fix_ti'])

        self.exec_with_verification(
            remote=controller_remote,
            cmd=gcs_settings.tempest_cmds['prepare_env'])
        docker_id = self.get_container_id(controller_remote)

        results = controller_remote.execute(
            gcs_settings.tempest_cmds['docker_exec_command'].format(
                docker_id, gcs_settings.tempest_cmds['start_rally'].format(
                    path_to_file=gcs_settings.path_to_tests_in_container)))

        logger.info('Tempest results:\n{}'.format(results))

        controller_remote.execute(
            gcs_settings.tempest_cmds['docker_exec_command'].format(
                docker_id,
                gcs_settings.tempest_cmds['verify_rally_results'].format(
                    report_name=report_name)))

        node_name = \
            self.fuel_web.get_nailgun_node_by_name(nodes[0].name)['hostname']

        master_remote.execute(
            gcs_settings.tempest_cmds['copy_report_to_master'].format(
                node_name=node_name, report_name=report_name))

        master_remote.download(
            '/root/{report_name}.html'.format(report_name=report_name),
            '{log_fold}{report_name}.html'.format(log_fold=log_folder,
                                                  report_name=report_name))

    def _get_master_node(self, active_node):
        node_name = None
        remote = self.fuel_web.get_ssh_for_node(active_node)
        pcs_status = remote.execute('pcs status')['stdout']
        for status in pcs_status:
            if re.search(u'Masters', status):
                node_name = status.split(':')[1].strip(' \,[\,]\,\n')
            elif re.search(u'Current DC', status):
                node_name = status.split(': ')[1].split(' ')[0]
        node_info = self.fuel_web.get_nailgun_node_by_fqdn(node_name)
        node = self.fuel_web.get_devops_node_by_nailgun_node(node_info)
        return node

    @staticmethod
    def _get_active_node(node, node_list):
        active_list = node_list[:]
        for nodes in active_list:
            if nodes == node:
                active_list.remove(nodes)
        active_node = random.choice(active_list)
        return active_node

    def _get_pcs_master_node_by_role(self, cluster_id, role):
        nodes = self.fuel_web.get_nailgun_cluster_nodes_by_roles(cluster_id,
                                                                 role)
        dev_nodes_all = self.fuel_web.get_devops_nodes_by_nailgun_nodes(nodes)
        node = random.choice(dev_nodes_all)
        if not re.search(u'mongo', role[0]):
            node = self._get_master_node(node.name)
        return [node, dev_nodes_all]

    def _verify_services_on_node(self, active_node, devops_node,
                                 cluster_id, num_fail, status):
        logger.info('Verifying pacemaker status:')
        if re.search(u'online', status):
            self.fuel_web.assert_pacemaker(
                active_node.name,
                set(devops_node[1]) - {devops_node[0]},
                [devops_node[0]])
            logger.info("Wait until Nailgun marked suspended node "
                        "as offline")
            wait(lambda: not
                 self.fuel_web.get_nailgun_node_by_devops_node(
                     devops_node[0])[status],
                 timeout=60 * 5)

        elif re.search(u'offline', status):
            time.sleep(45)
            self._verify_pacemaker(active_node.name, devops_node[1])
            logger.info("Wait until Nailgun marked suspended node "
                        "as online")
            wait(lambda: self.fuel_web.get_nailgun_node_by_devops_node(
                devops_node[0])['online'], timeout=60 * 5)

        logger.info("Wait the pacemaker react to changes in online nodes")
        time.sleep(60)
        logger.info("Wait for HA services ready")
        self.fuel_web.assert_ha_services_ready(cluster_id,
                                               should_fail=num_fail)
        logger.info("Wait until OpenStack services are UP")
        self.fuel_web.assert_os_services_ready(cluster_id,
                                               timeout=900,
                                               should_fail=num_fail)

    def _verify_mysql_galera(self, devops_node, status):
        logger.info("Wait until MySQL Galera is UP on online dbng nodes,"
                    " then run OSTF.")
        if status == u'Down':
            self.fuel_web.wait_mysql_galera_is_up(
                [n.name for n in set(devops_node[1]) - {devops_node[0]}],
                timeout=600)
        elif status == u'Up':
            self.fuel_web.wait_mysql_galera_is_up(
                [n.name for n in set(devops_node[1])], timeout=600)

    def _verify_pacemaker(self, ctrl_node, online_nodes):
        logger.info('Assert pacemaker status at devops node %s', ctrl_node)
        fqdn_names = lambda node: sorted([self.fuel_web.fqdn(n) for n in node])

        online = fqdn_names(online_nodes)
        try:
            wait(lambda: self.fuel_web.get_pcm_nodes(ctrl_node)['Online'] ==
                 online, timeout=60)
        except Exception:
            nodes = self.fuel_web.get_pcm_nodes(ctrl_node)
            assert(nodes['Online'] == online,
                   'Online nodes: {0} ; should be online: {1}'
                   .format(nodes['Online'], online))

    def _execute_ostf(self, cluster_id, test_sets, num_failed):
        logger.info("Running OSTF.")
        self.fuel_web.run_ostf(
            cluster_id=cluster_id,
            test_sets=test_sets,
            should_fail=num_failed)

    def cicd_ha_destroy_node_by_role(self, cluster_id, node_role_list):

        disabled_nodes = []
        logger.info('Starting disabling nodes.')
        for role in node_role_list:
            logger.info('Disabling node with role: {}'.format(role))
            devops_node = self._get_pcs_master_node_by_role(cluster_id, role)
            devops_node[0].destroy(False)
            if re.search(u'mongo', role[0]):
                time.sleep(600)
            else:
                if re.search(u'dbng', role[0]):
                    self._verify_mysql_galera(devops_node, status=u'Down')
                active_node = self._get_active_node(devops_node[0],
                                                    devops_node[1])
                self._verify_services_on_node(active_node, devops_node,
                                              cluster_id, num_fail=1,
                                              status='online')
            disabled_nodes.append({'role': role[0],
                                   'disabled_node': devops_node[0],
                                   'node_same_role': devops_node[1]})
        self._execute_ostf(cluster_id, test_sets=['ha', 'smoke', 'sanity'],
                           num_failed=1)
        return disabled_nodes

    def resume_node(self, nodes_to_re_enable, cluster_id):
        logger.info('Resuming suspended nodes.')
        for _dict in nodes_to_re_enable:
            devops_node = [_dict['disabled_node'], _dict['node_same_role']]
            logger.info('Enabling node: {} with role: {}'.format(
                devops_node[0], _dict['role']))
            devops_node[0].start()
            if re.search(u'mongo', _dict['role']):
                time.sleep(600)
            else:
                if re.search(u'dbng', _dict['role']):
                    self._verify_mysql_galera(devops_node, status=u'Up')
                active_node = self._get_active_node(devops_node[0],
                                                    devops_node[1])
                self._verify_services_on_node(active_node, devops_node,
                                              cluster_id, num_fail=1,
                                              status='offline')

        logger.info('Verifying nodes were resumed successfully.')
        self._execute_ostf(cluster_id, test_sets=['ha', 'smoke', 'sanity',
                                                  'tests_platform',
                                                  'cloudvalidation'],
                           num_failed=0)

    def update_packages(self):
        try:
            environment = self.env
            remote = environment.d_env.get_admin_remote()

            # Add temporary repo with new packages to YUM configuration
            conf_file = '/etc/yum.repos.d/temporary.repo'
            cmd = ("echo -e '[temporary]\nname=temporary\nbaseurl={0}"
                   "\ngpgcheck=0\npriority={1}' > {2}").format(
                settings.LCP_UPGRADE_REPO,
                settings.LCP_UPGRADE_REPO_PRIORITY,
                conf_file)
            environment.execute_remote_cmd(remote, cmd, exit_code=0)
            update_command = 'yum clean expire-cache; yum update -y -d3'
            result = remote.execute(update_command)
            logger.debug('Result of "yum update" command on master node: '
                         '{0}'.format(result))
            assert re.search('Complete!\n', result['stdout'][-1]),\
                'No packages were updated.'
            assert int(result['exit_code']) == 0, 'Packages update failed,' \
                                                  ' inspect logs for details'
        except Exception:
            logger.error("Could not update packages")
            raise

    def update_docker_containers(self):
        logger.info('Update and restart fuel docker containers.')
        environment = self.env

        environment.docker_actions.execute_in_containers(
            cmd='yum -y install yum-plugin-priorities')

        # Update docker containers and restart them
        environment.docker_actions.execute_in_containers(
            cmd='yum clean expire-cache; yum update -y')
        environment.docker_actions.restart_containers()

    def upgrade_ubuntu_repos(self, cluster_id):
        attributes = self.fuel_web.client.get_cluster_attributes(cluster_id)
        if settings.UPDATE_REWRITE_UBUNTU_REPOS:
            repos_attr = attributes['editable']['repo_setup']['repos']
            repos_attr['value'] = self.fuel_web.rewrite_ubuntu_repos(
                mirrors=settings.UPDATE_REWRITE_UBUNTU_REPOS)
            self.fuel_web.report_ubuntu_repos(repos_attr['value'])
