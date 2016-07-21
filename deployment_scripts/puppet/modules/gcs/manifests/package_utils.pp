#    Copyright 2016 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

class gcs::package_utils (
  $action                  = 'install',
  $packages                = $gcs::packages,
  $pip_packages            = $gcs::pip_packages,
  $pip_flags               = '',
  $python_package_provider = $gcs::python_package_provider,
)  {

  define gcs::package_utils::exec_pip (
    $pip_action = $gcs::package_utils::action,
    $flags = $gcs::package_utils::flags,
  )  {
    exec { "pip_install_${name}":
      command  => "pip ${pip_action} ${flags} ${name}",
      provider => shell,
      path     => '/usr/local/bin:/usr/bin:/bin'
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
