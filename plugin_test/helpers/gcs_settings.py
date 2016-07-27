tempest_cmds = {
    'install_git': 'apt-get -y install git',
    'clone_rally': 'git clone https://github.com/obutenko/mos-rally-verify.git',
    'fixate_tempest_ver': "sed -i -re 's/(--version) [0-9a-fA-F]+/--version "
                          "{tempest_commit}/' "
                          "mos-rally-verify/install_tempest.sh",
    'fix_docker_rally': "sed -i -re 's/(latest)/{rally_commit}/'"
                        " /root/mos-rally-verify/prepare_env.sh",
    'fix_ti': "sed -i -re 's/(exec -ti)/exec/'"
              " /root/mos-rally-verify/prepare_env.sh",
    'prepare_env': 'cd mos-rally-verify && ./prepare_env.sh',
    'copy_report_to_master': 'scp {node_name}:/home/{report_name}.html .',
    'test_list_path_on_lab': '/home/vyerys/test_list',
    'docker_exec_command': 'docker exec {} {}',
    'start_rally': 'rally verify start --tests-file {path_to_file}',
    'verify_rally_results': 'rally verify results --html --output-file'
                            ' {report_name}.html'
}

plugin_install_steps = {
    'install_deps': 'yum install -y createrepo rpm rpm-build dpkg-devel'
                    ' dpkg-dev git python-pip && pip install --upgrade pip',
    'install_fpb': 'git clone https://github.com/stackforge/fuel-plugins.git '
                   '&& cd fuel-plugins && sudo python setup.py install',
    'clone_plugin_repo': 'git clone https://github.com/openstack/fuel-plugin-cinder-gcs.git && '
                         'cd fuel-plugin-cinder-gcs && '
                         'git pull https://git.openstack.org/openstack/fuel-plugin-cinder-gcs refs/changes/84/345484/12',
    'is_hotpluggable_fix': "sed -i -re 's/(is_hotpluggable: false)+/"
                           "is_hotpluggable: true/' "
                           "/root/fuel-plugin-cinder-gcs/metadata.yaml",
    'build_plugin': 'fpb --build fuel-plugin-cinder-gcs',
    'fuel_install': 'fuel plugins --install fuel-plugin-cinder-gcs/{rpm_name}'
}

path_to_tests_in_container = '/home/rally/test_list'
tempest_commit = "63cb9a3718f394c9da8e0cc04b170ca2a8196ec2"
rally_commit = 'latest'
rpm_name = 'fuel-plugin-cinder-gcs-1.0-1.0.0-1.noarch.rpm'
plugin_name = 'fuel-plugin-cinder-gcs'
