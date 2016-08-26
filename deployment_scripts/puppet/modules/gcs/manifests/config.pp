#    Copyright 2016 Mirantis, Inc.
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

class gcs::config {

  cinder_config {
    'DEFAULT/backup_driver':                    value   => $gcs::backup_driver;
    'DEFAULT/backup_gcs_bucket':                value   => $gcs::settings['backup_gcs_bucket'];
    'DEFAULT/backup_gcs_project_id':            value   => $gcs::settings['backup_gcs_project_id'];
    'DEFAULT/backup_gcs_credential_file':       value   => $gcs::credential_file;
    'DEFAULT/backup_gcs_bucket_location':       value   => $gcs::settings['backup_gcs_bucket_location'];
    'DEFAULT/backup_gcs_enable_progress_timer': value   => $gcs::settings['backup_gcs_enable_progress_timer'];
    'DEFAULT/backup_gcs_storage_class':         value   => $gcs::settings['backup_gcs_storage_class'];
    'DEFAULT/backup_gcs_user_agent':            value   => $gcs::settings['backup_gcs_user_agent'];
    'DEFAULT/backup_gcs_credential_file':       value   => $gcs::settings['backup_gcs_credential_file'];
    'DEFAULT/backup_gcs_block_size':            value   => $gcs::settings['backup_gcs_block_size'];
    'DEFAULT/backup_gcs_object_size':           value   => $gcs::settings['backup_gcs_object_size'];
    'DEFAULT/backup_gcs_writer_chunk_size':     value   => $gcs::settings['backup_gcs_writer_chunk_size'];
    'DEFAULT/backup_gcs_reader_chunk_size':     value   => $gcs::settings['backup_gcs_reader_chunk_size'];
    'DEFAULT/backup_gcs_retry_error_codes':     value   => $gcs::settings['backup_gcs_retry_error_codes'];
    'DEFAULT/backup_gcs_num_retries':           value   => $gcs::settings['backup_gcs_num_retries'];
  }
  file { $gcs::credential_file:
      owner => 'cinder',
      group => 'cinder',
      content => template('gcs/credentials.json.erb'),
      mode  => '0600',
  }

}
