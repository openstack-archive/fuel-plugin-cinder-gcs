class gcs::package_utils (
  $action                  = 'install',
  $packages                = $gcs::packages,
  $pip_packages            = $gcs::pip_packages,
  $pip_flags               = '',
  $python_package_provider = $gcs::python_package_provider,
)  {
  notice ( $packages)

  define gcs::package_utils::exec_pip (
    $pip_action = $gcs::package_utils::action,
    $flags = $gcs::package_utils::flags,
  )  {
    exec { "pip_install_${name}":
      command  => "pip ${pip_action} ${flags} ${name}",
      provider => shell,
    }
  }
  
  package { $python_package_provider:
    ensure => installed,
  }

  case $action {
    'install': {
      if ($packages) {
        package { $packages:
          ensure   => installed,
        }
      }
      if ($pip_packages) {
        gcs::package_utils::exec_pip { $pip_packages:
          flags => '-U',
          require => Package[$python_package_provider],
        }
      }
    }
    'uninstall': {
      if ($packages) {
        package { $packages:
          ensure   => purged,
        }
      }
      if ($pip_packages) {
        package { $pip_packages:
          ensure   => absent,
          provider => pip,
        }
      }
    }
  }
}
