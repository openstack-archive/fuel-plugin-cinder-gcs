class gcs::google_api {

  package {'python-pip' :
    ensure    => installed
  } ->

  exec { 'upgrade-pip':
    command   => 'pip install --upgrade pip',
    provider  => 'shell'
  } ->

  package { 'google-api-python-client':
    ensure    => installed,
    provider  => pip,
  }
}
