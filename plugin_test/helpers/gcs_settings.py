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

"""Module with GCS plugin settings."""

import os

plugin_name = 'fuel-plugin-cinder-gcs'
plugin_version = '1.0.0'

default_tenant = 'gcs'
default_user = 'gcs'
default_user_pass = 'gcs123GCS'

options = {
    'backup_gcs_bucket_location/value': os.environ['GCS_LOCATION'],
    'backup_gcs_bucket/value': os.environ['GCS_BUCKET_NAME'],
    'backup_gcs_project_id/value': os.environ['GCS_PROJECT_ID'],
    'gcs_private_key/value': os.environ['GCS_PRIVATE_KEY'],
    'gcs_private_key_id/value': os.environ['GCS_KEY_ID'],
    'gcs_client_x509_cert_url/value': os.environ['GCS_CERT_URL'],
    'gcs_client_email/value': os.environ['GCS_CLIENT_EMAIL'],
    'gcs_client_id/value': os.environ['GCS_CLIENT_ID']
}

default_values = {
    'backup_gcs_advanced_settings': False,
    'backup_gcs_enable_progress_timer': True,
    'backup_gcs_retry_error_codes': '429',
    'backup_gcs_writer_chunk_size': '2097152',
    'backup_gcs_bucket_location': 'US',
    'backup_gcs_bucket': '',
    'backup_gcs_project_id': '',
    'backup_gcs_block_size': '32768',
    'backup_gcs_object_size': '52428800',
    'backup_gcs_storage_class': 'NEARLINE',
    'backup_gcs_user_agent': 'gcscinder',
    'backup_gcs_reader_chunk_size': '2097152',
    'backup_gcs_num_retries': '3',
    'metadata': True,
    'gcs_private_key': '',
    'gcs_private_key_id': '',
    'gcs_token_uri': 'https://accounts.google.com/o/oauth2/token',
    'gcs_client_x509_cert_url': '',
    'gcs_auth_provider_x509_cert_url': 'https://www.googleapis.com/'
                                       'oauth2/v1/certs',
    'gcs_client_email': '',
    'gcs_auth_uri': 'https://accounts.google.com/o/oauth2/auth',
    'gcs_client_id': '',
    'gcs_account_type': 'service_account'
}
