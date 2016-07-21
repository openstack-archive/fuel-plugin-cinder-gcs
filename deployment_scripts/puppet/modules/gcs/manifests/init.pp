class gcs {
  $services      = 'cinder-backup'
  $settings      = hiera_hash('gcs')
  $backup_driver = 'cinder.backup.drivers.google'
  $user_agent    = 'gcscinder'
}
