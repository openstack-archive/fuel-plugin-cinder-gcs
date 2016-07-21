class gcs::google_api {

  package {'python-pip' :
    ensure    => installed
  }

  exec { 'upgrade-pip':
    command   => 'pip install --upgrade pip',
    provider  => 'shell'
  }

  package { 'google-api-python-client':
    ensure    => installed,
    provider  => pip,
  }

  Package['python-pip'] -> Exec['upgrade-pip'] -> Package['google-api-python-client']
}
