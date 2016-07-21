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
    $backup_gcs_retry_error_codes = inline_template("<%= '[\\''''+@plugin_hash['backup_gcs_retry_error_codes'].strip.gsub(/\s*,\s*/,'\\''',\s\\'''')+'\\''']' %>")
  }
  else {
    $settings = {
      backup_gcs_bucket          => $plugin_hash['backup_gcs_bucket'],
      backup_gcs_project_id      => $plugin_hash['backup_gcs_project_id'],
      backup_gcs_bucket_location => $plugin_hash['backup_gcs_bucket_location'],
      backup_gcs_storage_class   => $plugin_hash['backup_gcs_storage_class'],
    }
  }
}
