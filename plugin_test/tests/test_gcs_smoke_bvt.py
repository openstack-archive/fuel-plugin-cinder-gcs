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

from proboscis.asserts import assert_equal
from proboscis import test

from fuelweb_test.helpers.decorators import log_snapshot_after_test
from fuelweb_test.tests.base_test_case import SetupEnvironment
from helpers.gcs_base import GcsTestBase


@test(groups=["test_gcs_all"])
class GcsTestClass(GcsTestBase):
    """GcsTestBase."""  # TODO(unknown) documentation

    @test(depends_on=[SetupEnvironment.prepare_slaves_3],
          groups=["gcs_deploy_smoke"])
    @log_snapshot_after_test
    def gcs_deploy_smoke(self):
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
        cluster_id = self.create_gcs_non_ha_cluster()

        self.install_plugin()
        self.set_attributes(cluster_id)

        self.fuel_web.deploy_cluster_wait(
            cluster_id,
            check_services=False
        )

        self.env.make_snapshot("gcs_deploy_smoke")

    @test(depends_on=[SetupEnvironment.prepare_slaves_5],
          groups=["gcs_deploy_bvt"])
    @log_snapshot_after_test
    def gcs_deploy_bvt(self):
        """Deploy HA cluster with GCS plugin installed and enabled.

        Scenario:
            1. Create cluster
            2. Add 3 node with controller role
            3. Add 1 node with compute role
            4. Add 1 node with cinder role
            5. Install GCS plugin
            6. Deploy the cluster
            7. Run network verification
            8. Run OSTF
        """
        self.env.revert_snapshot("ready_with_5_slaves")
        cluster_id = self.create_env_gcs_ha()

        self.install_plugin()
        self.set_attributes(cluster_id)

        self.fuel_web.deploy_cluster_wait(
            cluster_id,
            check_services=False
        )

        cluster = self.fuel_web.client.get_cluster(cluster_id)
        assert_equal(str(cluster['net_provider']), 'neutron')

        self.fuel_web.verify_network(cluster_id)

        self.fuel_web.security.verify_firewall(cluster_id)

        self.fuel_web.run_ostf(
            cluster_id=cluster_id,
            test_sets=['smoke', 'sanity', 'ha', 'tests_platform',
                       'cloudvalidation'])
        self.env.make_snapshot("gcs_deploy_bvt")
