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

from proboscis.asserts import assert_equal
from proboscis import test

from fuelweb_test.helpers.decorators import log_snapshot_after_test
from fuelweb_test.tests.base_test_case import SetupEnvironment
from helpers.gcs_base import GcsTestBase


@test(groups=["test_gcs_all"])
class GcsTestClass(GcsTestBase):
    """GcsTestBase"""  # TODO documentation

    @test(depends_on=[SetupEnvironment.prepare_slaves_3],
          groups=["deploy_gcs_non_ha"])
    @log_snapshot_after_test
    def deploy_gcs_non_ha(self):
        """

        """
        self.env.revert_snapshot("ready_with_3_slaves")
        self.install_plugin()
        cluster_id = self.create_gcs_non_ha_cluster()

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
            test_sets=['smoke', 'sanity', 'tests_platform', 'cloudvalidation'])
        self.env.make_snapshot("deploy_gcs_non_ha")

    @test(depends_on=[SetupEnvironment.prepare_slaves_5],
          groups=["deploy_gcs_ha"])
    @log_snapshot_after_test
    def deploy_gcs_ha(self):
        """

        """
        self.env.revert_snapshot("ready_with_5_slaves")
        # self.install_plugin()
        cluster_id = self.create_env_gcs_ha()

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
        self.env.make_snapshot("deploy_gcs_ha")
