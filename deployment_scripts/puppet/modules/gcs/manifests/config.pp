class gcs::config (
  $backup_driver                       = $gcs::backup_driver,
  $backup_gcs_bucket                   = $gcs::settings['backup_gcs_bucket'],
  $backup_gcs_project_id               = $gcs::settings['backup_gcs_project_id'],
  $backup_gcs_bucket_location          = $gcs::settings['backup_gcs_bucket_location'],
  $backup_gcs_enable_progress_timer    = $gcs::settings['backup_gcs_enable_progress_timer'],
  $backup_gcs_storage_class            = $gcs::settings['backup_gcs_storage_class'],
  $backup_gcs_user_agent               = $gcs::user_agent,
  $backup_gcs_credential_file          = $gcs::credential_file,
) {

  cinder_config {
    'DEFAULT/backup_driver':                    value   => $backup_driver;
    'DEFAULT/backup_gcs_bucket':                value   => $backup_gcs_bucket;
    'DEFAULT/backup_gcs_project_id':            value   => $backup_gcs_project_id;
    'DEFAULT/backup_gcs_credentials_file':      value   => $backup_gcs_credentials_file;
    'DEFAULT/backup_gcs_bucket_location':       value   => $backup_gcs_bucket_location;
    'DEFAULT/backup_gcs_enable_progress_timer': value   => $backup_gcs_enable_progress_timer;
    'DEFAULT/backup_gcs_storage_class':         value   => $backup_gcs_storage_class;
    'DEFAULT/backup_gcs_user_agent':            value   => $backup_gcs_user_agent;
    'DEFAULT/backup_gcs_credential_file':       value   => $backup_gcs_credential_file;
  }
   
    file { $backup_gcs_credential_file:
      owner => 'cinder',
      group => 'cinder',
      mode  => 600,
    }
}
