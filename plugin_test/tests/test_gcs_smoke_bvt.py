#    Copyright 2016 Mirantis, Inc.

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

"""Module with set of basic test cases."""

from proboscis import test

from fuelweb_test.helpers.decorators import log_snapshot_after_test
from fuelweb_test.tests.base_test_case import SetupEnvironment
from helpers.gcs_base import GcsTestBase
from helpers import gcs_settings
from fuelweb_test.settings import DEPLOYMENT_MODE
from fuelweb_test import logger
from tests.test_plugin_check import TestPluginCheck


@test(groups=["test_gcs_all"])
class GcsTestClass(GcsTestBase):
    """GcsTestBase."""  # TODO(unknown) documentation

    @test(depends_on=[SetupEnvironment.prepare_slaves_3],
          groups=["gcs_smoke"])
    @log_snapshot_after_test
    def gcs_smoke(self):
        """Deploy non HA cluster with GCS plugin installed and enabled.

        Scenario:
            1. Create cluster
            2. Add 1 node with controller role
            3. Add 1 node with compute role
            4. Add 1 node with cinder role
            5. Install GCS plugin
            6. Deploy the cluster
        """
        self.env.revert_snapshot("ready_with_3_slaves")

        logger.info('Creating GCS HA cluster...')
        segment_type = 'vlan'
        cluster_id = self.fuel_web.create_cluster(
            name=self.__class__.__name__,
            mode=DEPLOYMENT_MODE,
            settings={
                "net_provider": 'neutron',
                "net_segment_type": segment_type,
                'tenant': gcs_settings.default_tenant,
                'user': gcs_settings.default_user,
                'password': gcs_settings.default_user_pass,
                'assign_to_all_nodes': True
            }
        )

        self.fuel_web.update_nodes(
            cluster_id,
            {
                'slave-01': ['controller'],
                'slave-02': ['compute'],
                'slave-03': ['cinder']
            }
        )

        self.install_plugin()
        self.fuel_web.update_plugin_settings(cluster_id,
                                             gcs_settings.plugin_name,
                                             gcs_settings.plugin_version,
                                             gcs_settings.options)

        self.fuel_web.deploy_cluster_wait(
            cluster_id,
            check_services=False
        )

        self.env.make_snapshot("gcs_smoke")

    @test(depends_on=[SetupEnvironment.prepare_slaves_5],
          groups=["gcs_bvt"])
    @log_snapshot_after_test
    def gcs_bvt(self):
        """Deploy HA cluster with GCS plugin installed and enabled.

        Scenario:
            1. Install GCS plugin
            2. Create an environment
            3. Add 3 nodes with controller role
            4. Add a node with compute role
            5. Add a node with cinder role
            6. Configure GCS plugin
            7. Deploy the cluster
            8. Run OSTF
            9. Verify GCS plugin
        """
        self.env.revert_snapshot("ready_with_5_slaves")

        self.show_step(1)
        self.install_plugin()

        self.show_step(2)
        cluster_id = self.fuel_web.create_cluster(
            name=self.__class__.__name__,
            mode=DEPLOYMENT_MODE)

        self.show_step(3)
        self.show_step(4)
        self.show_step(5)
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

        self.show_step(6)
        self.fuel_web.update_plugin_settings(cluster_id,
                                             gcs_settings.plugin_name,
                                             gcs_settings.plugin_version,
                                             gcs_settings.options)

        self.show_step(7)
        self.fuel_web.deploy_cluster_wait(
            cluster_id,
            check_services=False
        )

        self.show_step(8)
        self.fuel_web.run_ostf(
            cluster_id=cluster_id,
            test_sets=['smoke', 'sanity', 'ha'])

        self.show_step(9)
        TestPluginCheck(self).plugin_check()
