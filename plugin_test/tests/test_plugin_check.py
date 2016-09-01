"""Copyright 2016 Mirantis, Inc.

Licensed under the Apache License, Version 2.0 (the "License"); you may
not use this file except in compliance with the License. You may obtain
copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations
under the License.
"""

from proboscis.asserts import assert_true

from devops.helpers.helpers import wait

from fuelweb_test import logger
from fuelweb_test.helpers import os_actions
from fuelweb_test.settings import SERVTEST_PASSWORD
from fuelweb_test.settings import SERVTEST_TENANT
from fuelweb_test.settings import SERVTEST_USERNAME

from helpers.gcs_settings import options


class TestPluginCheck(object):
    """Test suite for contrail openstack check."""

    def __init__(self, obj):
        """Create Test client for run tests.

        :param obj: Test case object
        """
        self.obj = obj
        cluster_id = self.obj.fuel_web.get_last_created_cluster()
        ip = self.obj.fuel_web.get_public_vip(cluster_id)
        self.os_conn = os_actions.OpenStackActions(
            ip, SERVTEST_USERNAME, SERVTEST_PASSWORD, SERVTEST_TENANT)

    def plugin_check(self):
        """TestPluginCheck test suite.

        Scenario:
            1. Create volume
            2. Create backup
            3. Verify type of backup
            4. Restore volume from backup
            5. Delete backup
            6. Delete volumes

        Duration 5 min


        """
        os_cinder = self.os_conn.cinder
        os_volumes = os_cinder.volumes
        logger.info('#'*10 + ' Run check_create_backup_and_restore ' + '#'*10)
        logger.info('Create volume ...')
        volume = os_volumes.create(size=1)
        wait(lambda: os_volumes.get(volume.id).status == 'available',
             timeout=60, timeout_msg='Volume is not created')

        logger.info('Create backup ...')
        backup = os_cinder.backups.create(volume.id)
        wait(lambda: os_cinder.backups.get(backup.id).status == 'available',
             timeout=120, timeout_msg='Backup is not created')

        logger.info('Verify type of backup ...')
        assert_true(backup.container == options['backup_gcs_bucket/value'],
                    "Backup doesn't configure via plugin")

        logger.info('Restore volume from backup ...')
        restore = os_cinder.restores.restore(backup.id)
        wait(lambda: os_volumes.get(restore.volume_id).status == 'available',
             timeout=120, timeout_msg='Backup is not restored')

        logger.info('Delete backup ...')
        os_cinder.backups.delete(backup.id)
        wait(lambda: len(os_cinder.backups.list()) == 0,
             timeout=120, timeout_msg='Backup is not deleted')

        logger.info('Delete volumes ...')
        os_volumes.delete(restore.volume_id)
        os_volumes.delete(volume.id)
        wait(lambda: len(os_volumes.list()) == 0,
             timeout=120, timeout_msg='Volumes are not deleted')
