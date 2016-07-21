class gcs::services {
  $services = $gcs::services
  service { $services: ensure => running }
  Cinder_config <||> ~> Service[$services]
}
