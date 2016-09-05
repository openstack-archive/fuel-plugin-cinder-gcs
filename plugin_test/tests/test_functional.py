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
from tests.test_plugin_check import TestPluginCheck


@test(groups=["gcs_functional_tests"])
class GcsTestClass(GcsTestBase):
    """GcsTestBase."""  # TODO(unknown) documentation

    @test(depends_on=[SetupEnvironment.prepare_slaves_5],
          groups=["gcs_delete_add_controller"])
    @log_snapshot_after_test
    def gcs_delete_add_controller(self):
        """Delete a controller node and add again.

        Scenario:
            1. Install GCS plugin
            2. Create an environment
            3. Add following nodes:
                * 1 controller
                * 2 controller+ceph-osd
                * 1 compute+ceph-osd
                * 1 compute
            4. Configure GCS plugin
            5. Deploy the cluster
            6. Run OSTF
            7. Verify GCS plugin
            8. Delete node with controller role
            9. Deploy changes
            10. Run OSTF
            11. Verify GCS plugin
            12. Add a node with controller role
            13. Deploy changes
            14. Run OSTF
            15. Verify GCS plugin
        """
        self.env.revert_snapshot("ready_with_5_slaves")

        self.show_step(1)
        self.install_plugin()

        self.show_step(2)
        cluster_id = self.fuel_web.create_cluster(
            name=self.__class__.__name__,
            settings={
                'images_ceph': True,
                'volumes_ceph': True,
                'ephemeral_ceph': True,
                'objects_ceph': True,
                'volumes_lvm': False
            }
        )

        self.show_step(3)
        self.fuel_web.update_nodes(
            cluster_id,
            {
                'slave-01': ['controller'],
                'slave-02': ['controller', 'ceph-osd'],
                'slave-03': ['ceph-osd', 'controller'],
                'slave-04': ['ceph-osd', 'compute'],
                'slave-05': ['compute'],
            }
        )

        self.show_step(4)
        self.fuel_web.update_plugin_settings(cluster_id,
                                             gcs_settings.plugin_name,
                                             gcs_settings.plugin_version,
                                             gcs_settings.options)

        self.show_step(5)
        self.fuel_web.deploy_cluster_wait(
            cluster_id,
            check_services=False
        )

        self.show_step(6)
        self.fuel_web.run_ostf(
            cluster_id=cluster_id,
            test_sets=['smoke', 'sanity', 'ha'])

        self.show_step(7)
        TestPluginCheck(self).plugin_check()

        self.show_step(8)
        self.fuel_web.update_nodes(
            cluster_id, {'slave-01': ['controller']},
            pending_addition=False, pending_deletion=True)

        self.show_step(9)
        self.fuel_web.deploy_cluster_wait(
            cluster_id,
            check_services=False
        )

        self.show_step(10)
        self.fuel_web.run_ostf(
            cluster_id=cluster_id,
            should_fail=1,
            failed_test_name=['Check that required services are running'],
            test_sets=['smoke', 'sanity', 'ha'])

        self.show_step(11)
        TestPluginCheck(self).plugin_check()

        self.show_step(12)
        self.fuel_web.update_nodes(
            cluster_id, {'slave-01': ['controller']})

        self.show_step(13)
        self.fuel_web.deploy_cluster_wait(
            cluster_id,
            check_services=False
        )

        self.show_step(14)
        self.fuel_web.run_ostf(
            cluster_id=cluster_id,
            should_fail=1,
            failed_test_name=['Check that required services are running'],
            test_sets=['smoke', 'sanity', 'ha'])

        self.show_step(15)
        TestPluginCheck(self).plugin_check()

    @test(depends_on=[SetupEnvironment.prepare_slaves_3],
          groups=["gcs_delete_add_compute"])
    @log_snapshot_after_test
    def gcs_delete_add_compute(self):
        """Delete a compute node and add again.

        Scenario:
            1. Install GCS plugin
            2. Create an environment
            3. Add following nodes:
                * 1 controller
                * 1 compute+cinder
                * 1 compute
            4. Configure GCS plugin
            5. Deploy the cluster
            6. Run OSTF
            7. Verify GCS plugin
            8. Delete a node with compute role
            9. Deploy changes
            10. Run OSTF
            11. Verify GCS plugin
            12. Add a node with compute role
            13. Deploy changes
            14. Run OSTF
            15. Verify GCS plugin
        """
        self.env.revert_snapshot("ready_with_3_slaves")

        self.show_step(1)
        self.install_plugin()

        self.show_step(2)
        cluster_id = self.fuel_web.create_cluster(
            name=self.__class__.__name__,
            settings={
                "net_provider": 'neutron',
                "net_segment_type": 'tun',
            }
        )

        self.show_step(3)
        self.fuel_web.update_nodes(
            cluster_id,
            {
                'slave-01': ['controller'],
                'slave-02': ['compute', 'cinder'],
                'slave-03': ['compute'],
            }
        )

        self.show_step(4)
        self.fuel_web.update_plugin_settings(cluster_id,
                                             gcs_settings.plugin_name,
                                             gcs_settings.plugin_version,
                                             gcs_settings.options)

        self.show_step(5)
        self.fuel_web.deploy_cluster_wait(
            cluster_id,
            check_services=False
        )

        self.show_step(6)
        self.fuel_web.run_ostf(
            cluster_id=cluster_id,
            test_sets=['smoke', 'sanity'])

        self.show_step(7)
        TestPluginCheck(self).plugin_check()

        self.show_step(8)
        self.fuel_web.update_nodes(
            cluster_id, {'slave-03': ['compute']},
            pending_addition=False, pending_deletion=True)

        self.show_step(9)
        self.fuel_web.deploy_cluster_wait(
            cluster_id,
            check_services=False
        )

        self.show_step(10)
        self.fuel_web.run_ostf(
            cluster_id=cluster_id,
            should_fail=1,
            failed_test_name=['Check that required services are running'],
            test_sets=['smoke', 'sanity'])

        self.show_step(11)
        TestPluginCheck(self).plugin_check()

        self.show_step(12)
        self.fuel_web.update_nodes(
            cluster_id, {'slave-03': ['compute']})

        self.show_step(13)
        self.fuel_web.deploy_cluster_wait(
            cluster_id,
            check_services=False
        )

        self.show_step(14)
        self.fuel_web.run_ostf(
            cluster_id=cluster_id,
            should_fail=1,
            failed_test_name=['Check that required services are running'],
            test_sets=['smoke', 'sanity'])

        self.show_step(15)
        TestPluginCheck(self).plugin_check()

    @test(depends_on=[SetupEnvironment.prepare_slaves_3],
          groups=["gcs_delete_add_cinder"])
    @log_snapshot_after_test
    def gcs_delete_add_cinder(self):
        """Delete a cinder node and add again.

        Scenario:
            1. Install GCS plugin
            2. Create an environment
            3. Add following nodes:
                * 1 controller+cinder
                * 1 compute+cinder
                * 1 cinder
            4. Configure GCS plugin
            5. Deploy the cluster
            6. Run OSTF
            7. Verify GCS plugin
            8. Delete a node with cinder role
            9. Deploy changes
            10. Run OSTF
            11. Verify GCS plugin
            12. Add a node with cinder role
            13. Deploy changes
            14. Run OSTF
            15. Verify GCS plugin
        """
        self.env.revert_snapshot("ready_with_3_slaves")

        self.show_step(1)
        self.install_plugin()

        self.show_step(2)
        cluster_id = self.fuel_web.create_cluster(
            name=self.__class__.__name__,
        )

        self.show_step(3)
        self.fuel_web.update_nodes(
            cluster_id,
            {
                'slave-01': ['controller', 'cinder'],
                'slave-02': ['compute', 'cinder'],
                'slave-03': ['cinder'],
            }
        )

        self.show_step(4)
        self.fuel_web.update_plugin_settings(cluster_id,
                                             gcs_settings.plugin_name,
                                             gcs_settings.plugin_version,
                                             gcs_settings.options)

        self.show_step(5)
        self.fuel_web.deploy_cluster_wait(
            cluster_id,
            check_services=False
        )

        self.show_step(6)
        self.fuel_web.run_ostf(
            cluster_id=cluster_id,
            test_sets=['smoke', 'sanity'])

        self.show_step(7)
        TestPluginCheck(self).plugin_check()

        self.show_step(8)
        self.fuel_web.update_nodes(
            cluster_id, {'slave-03': ['cinder']},
            pending_addition=False, pending_deletion=True)

        self.show_step(9)
        self.fuel_web.deploy_cluster_wait(
            cluster_id,
            check_services=False
        )

        self.show_step(10)
        self.fuel_web.run_ostf(
            cluster_id=cluster_id,
            should_fail=1,
            failed_test_name=['Check that required services are running'],
            test_sets=['smoke', 'sanity'])

        self.show_step(11)
        TestPluginCheck(self).plugin_check()

        self.show_step(12)
        self.fuel_web.update_nodes(
            cluster_id, {'slave-03': ['cinder']})

        self.show_step(13)
        self.fuel_web.deploy_cluster_wait(
            cluster_id,
            check_services=False
        )

        self.show_step(14)
        self.fuel_web.run_ostf(
            cluster_id=cluster_id,
            should_fail=1,
            failed_test_name=['Check that required services are running'],
            test_sets=['smoke', 'sanity'])

        self.show_step(15)
        TestPluginCheck(self).plugin_check()

    @test(depends_on=[SetupEnvironment.prepare_slaves_3],
          groups=["gcs_delete_add_single_cinder"])
    @log_snapshot_after_test
    def gcs_delete_add_single_cinder(self):
        """Delete the only cinder node and add again.

        Scenario:
            1. Install GCS plugin
            2. Create an environment
            3. Add following nodes:
                * 1 controller
                * 1 compute
                * 1 cinder
            4. Configure GCS plugin
            5. Deploy the cluster
            6. Run OSTF
            7. Verify GCS plugin
            8. Delete a node with cinder role
            9. Deploy changes
            10. Run OSTF
            11. Add a node with cinder role
            12. Deploy changes
            13. Run OSTF
            14. Verify GCS plugin
        """
        self.env.revert_snapshot("ready_with_3_slaves")

        self.show_step(1)
        self.install_plugin()

        self.show_step(2)
        cluster_id = self.fuel_web.create_cluster(
            name=self.__class__.__name__,
            settings={
                "net_provider": 'neutron',
                "net_segment_type": 'tun',
            }
        )

        self.show_step(3)
        self.fuel_web.update_nodes(
            cluster_id,
            {
                'slave-01': ['controller'],
                'slave-02': ['compute'],
                'slave-03': ['cinder'],
            }
        )

        self.show_step(4)
        self.fuel_web.update_plugin_settings(cluster_id,
                                             gcs_settings.plugin_name,
                                             gcs_settings.plugin_version,
                                             gcs_settings.options)

        self.show_step(5)
        self.fuel_web.deploy_cluster_wait(
            cluster_id,
            check_services=False
        )

        self.show_step(6)
        self.fuel_web.run_ostf(
            cluster_id=cluster_id,
            test_sets=['smoke', 'sanity'])

        self.show_step(7)
        TestPluginCheck(self).plugin_check()

        self.show_step(8)
        self.fuel_web.update_nodes(
            cluster_id, {'slave-03': ['cinder']},
            pending_addition=False, pending_deletion=True)

        self.show_step(9)
        self.fuel_web.deploy_cluster_wait(
            cluster_id,
            check_services=False
        )

        self.show_step(10)
        self.fuel_web.run_ostf(
            cluster_id=cluster_id,
            should_fail=1,
            failed_test_name=['Check that required services are running'],
            test_sets=['smoke', 'sanity'])

        self.show_step(11)
        self.fuel_web.update_nodes(
            cluster_id, {'slave-03': ['cinder']})

        self.show_step(12)
        self.fuel_web.deploy_cluster_wait(
            cluster_id,
            check_services=False
        )

        self.show_step(13)
        self.fuel_web.run_ostf(
            cluster_id=cluster_id,
            should_fail=1,
            failed_test_name=['Check that required services are running'],
            test_sets=['smoke', 'sanity'])

        self.show_step(14)
        TestPluginCheck(self).plugin_check()

    @test(depends_on=[SetupEnvironment.prepare_slaves_5],
          groups=["gcs_add_ceph"])
    @log_snapshot_after_test
    def gcs_add_ceph(self):
        """Adding a ceph-osd node.

        Scenario:
            1. Install GCS plugin
            2. Create an environment
            3. Add following nodes:
                * 3 controller+ceph-osd
                * 1 compute+ceph-osd
            4. Configure GCS plugin
            5. Deploy the cluster
            6. Run OSTF
            7. Verify GCS plugin
            8. Add a node with compute+ceph-osd roles
            9. Deploy changes
            10. Run OSTF
            11. Verify GCS plugin
        """
        self.env.revert_snapshot("ready_with_5_slaves")

        self.show_step(1)
        self.install_plugin()

        self.show_step(2)
        cluster_id = self.fuel_web.create_cluster(
            name=self.__class__.__name__,
            settings={
                'images_ceph': True,
                'volumes_ceph': True,
                'ephemeral_ceph': True,
                'objects_ceph': True,
                'volumes_lvm': False,
                "net_provider": 'neutron',
                "net_segment_type": 'tun',
            }
        )

        self.show_step(3)
        self.fuel_web.update_nodes(
            cluster_id,
            {
                'slave-01': ['controller', 'ceph-osd'],
                'slave-02': ['controller', 'ceph-osd'],
                'slave-03': ['controller', 'ceph-osd'],
                'slave-04': ['ceph-osd', 'compute'],
            }
        )

        self.show_step(4)
        self.fuel_web.update_plugin_settings(cluster_id,
                                             gcs_settings.plugin_name,
                                             gcs_settings.plugin_version,
                                             gcs_settings.options)

        self.show_step(5)
        self.fuel_web.deploy_cluster_wait(
            cluster_id,
            check_services=False
        )

        self.show_step(6)
        self.fuel_web.run_ostf(
            cluster_id=cluster_id,
            test_sets=['smoke', 'sanity', 'ha'])

        self.show_step(7)
        TestPluginCheck(self).plugin_check()

        self.show_step(8)
        self.fuel_web.update_nodes(
            cluster_id, {'slave-05': ['ceph-osd', 'compute']})

        self.show_step(9)
        self.fuel_web.deploy_cluster_wait(
            cluster_id,
            check_services=False
        )

        self.show_step(10)
        self.fuel_web.run_ostf(
            cluster_id=cluster_id,
            test_sets=['smoke', 'sanity', 'ha'])

        self.show_step(11)
        TestPluginCheck(self).plugin_check()
