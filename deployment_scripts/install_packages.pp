notice('MODULAR: gcs_install_packages.pp')
include gcs
class { 'gcs::google_api': }

