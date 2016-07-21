notice('MODULAR: gcs_cinder_config.pp')
include gcs
class { 'gcs::config': }
class { 'gcs::services': }
