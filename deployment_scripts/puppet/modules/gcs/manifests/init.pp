class gcs {
  $services                 = 'cinder-backup'
  $plugin_hash              = hiera_hash('fuel-plugin-cinder-gcs')
  $backup_driver            = 'cinder.backup.drivers.google'
  $user_agent               = 'gcscinder'
  $credential_file          = '/var/lib/cinder/credentials.json'
  $pip_packages             = ['google-api-python-client']
  $python_package_provider  = ['python-pip']

  if $plugin_hash['backup_gcs_advanced_settings'] {
    $settings = $plugin_hash
  }
  else {
    $settings = {
      backup_gcs_bucket                 => $plugin_hash['backup_gcs_bucket'],
      backup_gcs_project_id             => $plugin_hash['backup_gcs_project_id'],
      backup_gcs_bucket_location        => $plugin_hash['backup_gcs_bucket_location'],
      backup_gcs_storage_class          => $plugin_hash['backup_gcs_storage_class'],
      gcs_private_key_id                => $plugin_hash['gcs_private_key_id'],
      gcs_private_key                   => $plugin_hash['gcs_private_key'],
      gcs_client_email                  => $plugin_hash['gcs_client_email'],
      gcs_client_id                     => $plugin_hash['gcs_client_id'],
      gcs_auth_uri                      => $plugin_hash['gcs_auth_uri'],
      gcs_token_uri                     => $plugin_hash['gcs_token_uri'],
      gcs_auth_provider_x509_cert_url   => $plugin_hash['gcs_auth_provider_x509_cert_url'],
      gcs_client_x509_cert_url          => $plugin_hash['gcs_client_x509_cert_url'],
      gcs_account_type                  => $plugin_hash['gcs_account_type']
    }
  }
}
