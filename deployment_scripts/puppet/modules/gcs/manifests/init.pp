class gcs {
  $services        = 'cinder-backup'
  $settings        = hiera_hash('fuel-plugin-cinder-gcs')
  $backup_driver   = 'cinder.backup.drivers.google'
  $user_agent      = 'gcscinder'
  $credential_file = '/var/lib/cinder/credentials.json'
  $pip_packages    = ['google-api-python-client']
  $packages        = ['python-pip']
}

