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
from fuelweb_test.tests import base_test_case
from helpers import gcs_base
from helpers import gcs_settings
from tests import test_plugin_check


@test(groups=["gcs_integration_tests"])
class GcsTestClass(gcs_base.GcsTestBase):
    """GcsTestBase."""  # TODO(unknown) documentation

    @test(depends_on=[base_test_case.SetupEnvironment.prepare_slaves_5],
          groups=["gcs_ceph"])
    @log_snapshot_after_test
    def gcs_ceph(self):
        """Deploy with GCS plugin and CEPH standalone roles.

        Scenario:
            1. Install GCS plugin
            2. Create an environment with tunneling segmentation
            3. Add a node with controller role
            4. Add a node with compute role
            5. Add 3 nodes with Ceph-OSD roles
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
            settings={
                "net_provider": 'neutron',
                "net_segment_type": 'tun',
                'images_ceph': True,
                'volumes_ceph': True,
                'ephemeral_ceph': True,
                'objects_ceph': True,
                'volumes_lvm': False
            }
        )

        self.show_step(3)
        self.show_step(4)
        self.show_step(5)
        self.fuel_web.update_nodes(
            cluster_id,
            {
                'slave-01': ['controller'],
                'slave-02': ['compute'],
                'slave-03': ['ceph-osd'],
                'slave-04': ['ceph-osd'],
                'slave-05': ['ceph-osd'],
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
            test_sets=['smoke', 'sanity'])

        self.show_step(9)
        test_plugin_check.TestPluginCheck(self).plugin_check()

    @test(depends_on=[base_test_case.SetupEnvironment.prepare_slaves_5],
          groups=["gcs_cinder_multirole"])
    @log_snapshot_after_test
    def gcs_cinder_multirole(self):
        """Deploy with GCS plugin and cinder multirole.

        Scenario:
            1. Install GCS plugin
            2. Create an environment with tunneling segmentation
            3. Add 3 nodes with controller+cinder roles
            4. Add 2 nodes with compute+cinder roles
            5. Configure GCS plugin
            6. Deploy the cluster
            7. Run OSTF
            8. Verify GCS plugin
        """
        self.env.revert_snapshot("ready_with_5_slaves")

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
        self.show_step(4)
        self.fuel_web.update_nodes(
            cluster_id,
            {
                'slave-01': ['controller', 'cinder'],
                'slave-02': ['controller', 'cinder'],
                'slave-03': ['controller', 'cinder'],
                'slave-04': ['compute', 'cinder'],
                'slave-05': ['compute', 'cinder'],
            }
        )

        self.show_step(5)
        self.fuel_web.update_plugin_settings(cluster_id,
                                             gcs_settings.plugin_name,
                                             gcs_settings.plugin_version,
                                             gcs_settings.options)

        self.show_step(6)
        self.fuel_web.deploy_cluster_wait(
            cluster_id,
            check_services=False
        )

        self.show_step(7)
        self.fuel_web.run_ostf(
            cluster_id=cluster_id,
            test_sets=['smoke', 'sanity', 'ha'])

        self.show_step(8)
        test_plugin_check.TestPluginCheck(self).plugin_check()

    @test(depends_on=[base_test_case.SetupEnvironment.prepare_slaves_5],
          groups=["gcs_cinder_ceph_multirole"])
    @log_snapshot_after_test
    def gcs_cinder_ceph_multirole(self):
        """Deploy with GCS plugin and cinder+Ceph-OSD multiroles.

        Scenario:
            1. Install GCS plugin
            2. Create an environment
            3. Add following nodes:
                * 1 controller + ceph + cinder
                * 1 controller + ceph
                * 1 controller + cinder
                * 1 compute + ceph + cinder
                * 1 compute
            4. Configure GCS plugin
            5. Deploy the cluster
            6. Run OSTF
            7. Verify GCS plugin
        """
        self.env.revert_snapshot("ready_with_5_slaves")

        self.show_step(1)
        self.install_plugin()

        self.show_step(2)
        cluster_id = self.fuel_web.create_cluster(
            name=self.__class__.__name__,
            settings={'images_ceph': True}
        )

        self.show_step(3)
        self.fuel_web.update_nodes(
            cluster_id,
            {
                'slave-01': ['controller', 'cinder', 'ceph-osd'],
                'slave-02': ['controller', 'cinder'],
                'slave-03': ['controller', 'ceph-osd'],
                'slave-04': ['compute', 'cinder', 'ceph-osd'],
                'slave-05': ['compute', 'cinder'],
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
        test_plugin_check.TestPluginCheck(self).plugin_check()

    @test(depends_on=[base_test_case.SetupEnvironment.prepare_slaves_5],
          groups=["gcs_ceilometer"])
    @log_snapshot_after_test
    def gcs_ceilometer(self):
        """Deploy an environment with GCS plugin and ceilometer.

        Scenario:
            1. Install GCS plugin
            2. Create an environment
            3. Add following nodes:
                * 1 controller + mongo-db
                * 1 mongo-db
                * 1 cinder + mongo-db
                * 2 compute
            4. Configure GCS plugin
            5. Deploy the cluster
            6. Run OSTF
            7. Verify GCS plugin
        """
        self.env.revert_snapshot("ready_with_5_slaves")

        self.show_step(1)
        self.install_plugin()

        self.show_step(2)
        cluster_id = self.fuel_web.create_cluster(
            name=self.__class__.__name__,
            settings={'ceilometer': True}
        )

        self.show_step(3)
        self.fuel_web.update_nodes(
            cluster_id,
            {
                'slave-01': ['controller', 'mongo'],
                'slave-02': ['mongo'],
                'slave-03': ['cinder', 'mongo'],
                'slave-04': ['compute'],
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
            test_sets=['smoke', 'sanity', 'tests_platform'])

        self.show_step(7)
        test_plugin_check.TestPluginCheck(self).plugin_check()
