notice('MODULAR: gcs_cinder_config.pp')
include gcs
class { 'gcs::config': }
class { 'gcs::package_utils': }
class { 'gcs::services': }
