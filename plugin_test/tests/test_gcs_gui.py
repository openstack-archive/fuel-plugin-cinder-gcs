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

"""Module with ui defaults verification test."""

from proboscis import test

from fuelweb_test.helpers.decorators import log_snapshot_after_test
from fuelweb_test.tests.base_test_case import SetupEnvironment
from helpers.gcs_base import GcsTestBase
from helpers import gcs_settings
from fuelweb_test.settings import DEPLOYMENT_MODE
from fuelweb_test import logger


@test(groups=["test_gcs_all"])
class TestGCSPlugin(GcsTestBase):
    """TestGCSPlugin."""  # TODO(unknown) documentation

    @test(depends_on=[SetupEnvironment.prepare_slaves_3],
          groups=["gcs_gui_defaults"])
    @log_snapshot_after_test
    def gcs_gui_defaults(self):
        """Create non HA cluster with GCS plugin installed.

        Scenario:
            1. Create cluster
            2. Install GCS plugin
            3. Create cluster
            4. Verify default values
        """
        self.env.revert_snapshot("ready_with_3_slaves")

        logger.info('Creating GCS non HA cluster...')
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
        self.verify_defaults(cluster_id)
        self.env.make_snapshot("gcs_gui_defaults")
