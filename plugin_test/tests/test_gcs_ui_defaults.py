# Copyright 2016 Mirantis, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Module with ui defaults verification test."""

from proboscis import test

from fuelweb_test.helpers.decorators import log_snapshot_after_test
from fuelweb_test.tests.base_test_case import SetupEnvironment
from helpers.gcs_base import GcsTestBase


@test(groups=["test_gcs_all"])
class TestGCSPlugin(GcsTestBase):
    """TestGCSPlugin."""  # TODO(unknown) documentation

    @test(depends_on=[SetupEnvironment.prepare_slaves_3],
          groups=["gcs_ui_defaults"])
    @log_snapshot_after_test
    def gcs_ui_defaults(self):
        """Create non HA cluster with GCS plugin installed.

        Scenario:
            1. Create cluster
            2. Add 1 node with controller role
            3. Add 1 node with compute role
            4. Add 1 node with cinder role
            5. Install GCS plugin
            6. Verify default values
        """
        self.env.revert_snapshot("ready_with_3_slaves")
        cluster_id = self.create_gcs_non_ha_cluster()

        self.install_plugin()
        self.verify_defaults(cluster_id)
