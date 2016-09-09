Automate with Mistral
---------------------

Many backup strategies require taking backups on regular basis
and it's good to have these repeatable actions automated.

Taking a drive backup is often considered as a single action but
usually requires taking a snapshot, taking a backup of the snapshot and
then deleting the snapshot. So taking a drive backup is actually a workflow.

Mistral is a workflow service for OpenStack cloud and the plugin provides a
sample Mistral workbook.

The workflow provided by the sample basicly does:

* Create a list of Cinder volumes to backup
* Create snapshots for the volumes
* Create backups for the snapshots
* Wait until backups are created
* Remove the snapshots
* Send a report(optional)

After the plugin is installed on Fuel master the sample can be found in
``/var/www/nailgun/plugins/fuel-plugin-cinder-gcs-1.0/examples/mistral_workbook.yaml``
on Fuel master node.

To use the sample it's required to have Mistral service installed and running.


Copying Mistral workbook to an Openstack controller
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Copy the sample from Fuel master to an OpenStack controller::

  root@fuel-master# scp /var/www/nailgun/plugins/fuel-plugin-cinder-gcs-1.0/examples/mistral_workbook.yaml root@<CONTROLLER_NAME_OR_IP>:~

Customizing the sample workbook
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Mistral has a possibility to send e-mails via an MTA(**TO BE ADDED TO ACRONYMS**)
which support SSL/TLS and authentication. It's not possible to use a MTA without
SSL/TLS and authentication support.

Proper MTA credentials should be set in the sample file before creating Mistral
workbook to sample.

#. Login to the controller and edit the sample file

::

  root@controller:~# vi mistral_workbook.yaml
  ...
        from_addr: '<USERNAME>@<DOMAIN>'
        smtp_server: '<MTA_HOSTNAME_OR_IP>'
        smtp_password: '<PASSWORD>'

*Note:* The step can be skipped if sending e-mails by the workflow if not
supposed.

Creating Mistral workbook from the sample
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Verify Mistral CLI works

::

  root@controller:~# openstack workbook list
  +------------------------+--------+---------------------+------------+
  | Name                   | Tags   | Created at          | Updated at |
  +------------------------+--------+---------------------+------------+
  +------------------------+--------+---------------------+------------+

  root@controller:~# openstack workflow list -c Name
  +---------------------+
  | Name                |
  +---------------------+
  | std.create_instance |
  | std.delete_instance |
  +---------------------+

*Note:* It may be required to source the approriate *openrc* file to get the
command working.

#. Create Mistral workbook from the sample

::

  root@controller:~# openstack workbook create mistral_workbook.yaml
  +------------+----------------------------+
  | Field      | Value                      |
  +------------+----------------------------+
  | Name       | sample_backup_workbook     |
  | Tags       | <none>                     |
  | Created at | 2016-09-08 13:59:10.306180 |
  | Updated at | None                       |
  +------------+----------------------------+

#. Verify the workbook and the workflow are added

::

  root@controller:~# openstack workbook list
  +------------------------+--------+---------------------+------------+
  | Name                   | Tags   | Created at          | Updated at |
  +------------------------+--------+---------------------+------------+
  | sample_backup_workbook | <none> | 2016-09-08 13:59:10 | None       |
  +------------------------+--------+---------------------+------------+

  root@controller:~# openstack workflow list -c Name
  +------------------------------------------------+
  | Name                                           |
  +------------------------------------------------+
  | std.create_instance                            |
  | std.delete_instance                            |
  | sample_backup_workbook.create_backups_workflow |   <---
  +------------------------------------------------+

Using workflow
^^^^^^^^^^^^^^

The workflow accepts the following parameters:

* *projects_id_list*

  * Optional
  * Default: null
  * Mutual exclusive with *volumes_id_list*
  * Comment: Mutual exclusive with *volumes_id_list*. If *projects_id_list* is
    provided all volumes of the projects are backued up. If *volumes_id_list* is
    provided only volumes from the list are backud up. If neither
    *projects_id_list* nor *volumes_id_list* is provided all volumes of all
    projects will be backed up.

* *volumes_id_list*

  * Optional
  * Default: null
  * Comment: Mutual exclusive with *volumes_id_list*. If *projects_id_list* is
    provided all volumes of the projects are backued up. If *volumes_id_list* is
    provided only volumes from the list are backud up. If neither
    *projects_id_list* nor *volumes_id_list* is provided all volumes of all
    projects will be backed up.

* *incremental*

  * Optional
  * Default: false
  * Comment: Full backups are created is not provided.

* *report_to_list*

  * Optional
  * Default: null
  * Comment: E-mails are not sent if not provided.

* *snapshot_name*

  * Optional
  * Default: 'by_create_backups_workflow'
  * Comment: It becomes a name for Cinder snaphots. Useful for detecting not
    deleted Cinder snapshots.

Executing workflow without parameters (test only)
"""""""""""""""""""""""""""""""""""""""""""""""""

*Note:* Executing the workflow without parameters will cause taking full backups
of all volumes of all projects(tenants) what cat take a lot of time and
resources.

::

  root@controller:~# openstack workflow execution create sample_backup_workbook.create_backups_workflow
  +-------------------+------------------------------------------------+
  | Field             | Value                                          |
  +-------------------+------------------------------------------------+
  | ID                | 93fc32a1-d285-4934-9b14-9a58b395e5d1           | <---ID
  | Workflow ID       | c5816326-ae05-43cc-8732-943ace7b5947           |
  | Workflow name     | sample_backup_workbook.create_backups_workflow |
  | Description       |                                                |
  | Task Execution ID | <none>                                         |
  | State             | RUNNING                                        |
  | State info        | None                                           |
  | Created at        | 2016-09-09 13:06:27                            |
  | Updated at        | 2016-09-09 13:06:26.626167                     |
  +-------------------+------------------------------------------------+

Executing workflow with parameters
""""""""""""""""""""""""""""""""""

The next example shows providing *volumes_id_list* and *incremental* parameters
while creating an execution.

::

  root@controller:~# openstack workflow execution create sample_backup_workbook.create_backups_workflow '{"volumes_id_list": ["0774de3c-092a-4eb3-a25f-04c0790f51c6"], "incremental": true }'
  +-------------------+------------------------------------------------+
  | Field             | Value                                          |
  +-------------------+------------------------------------------------+
  | ID                | ec017763-11c6-421f-b7e9-7774bc2a7fa3           |
  | Workflow ID       | c5816326-ae05-43cc-8732-943ace7b5947           |
  | Workflow name     | sample_backup_workbook.create_backups_workflow |
  | Description       |                                                |
  | Task Execution ID | <none>                                         |
  | State             | RUNNING                                        |
  | State info        | None                                           |
  | Created at        | 2016-09-09 13:18:14                            |
  | Updated at        | 2016-09-09 13:18:14.044925                     |
  +-------------------+------------------------------------------------+

Checking execution and execution tasks status
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To check an execution status the execution ID is required. The ID can be found
in ``openstack workflow execution create`` command output.::

  root@node-1:~# openstack workflow execution show 9822a1c0-bd79-4bb2-9c91-c0accf96e60e
  +-------------------+------------------------------------------------+
  | Field             | Value                                          |
  +-------------------+------------------------------------------------+
  | ID                | 9822a1c0-bd79-4bb2-9c91-c0accf96e60e           |
  | Workflow ID       | c5816326-ae05-43cc-8732-943ace7b5947           |
  | Workflow name     | sample_backup_workbook.create_backups_workflow |
  | Description       |                                                |
  | Task Execution ID | <none>                                         |
  | State             | SUCCESS                                        |
  | State info        | None                                           |
  | Created at        | 2016-09-09 12:54:03                            |
  | Updated at        | 2016-09-09 12:55:23                            |
  +-------------------+------------------------------------------------+

To list the execution tasks run providing the execution ID::

  root@node-1:~# openstack task execution list 9822a1c0-bd79-4bb2-9c91-c0accf96e60e
  +-----..-+------..-+---------------..-+--------------..-+---------+------..-+
  | ID  .. | Name .. | Workflow name .. | Execution ID .. | State   | State.. |
  +-----..-+------..-+---------------..-+--------------..-+---------+------..-+
  | c4c3.. | analy.. | sample_backup_.. | 9822a1c0-bd79.. | SUCCESS | None .. |
  | c1e0.. | analy.. | sample_backup_.. | 9822a1c0-bd79.. | SUCCESS | None .. |
  | 81de.. | get_a.. | sample_backup_.. | 9822a1c0-bd79.. | SUCCESS | None .. |
  | cd74.. | creat.. | sample_backup_.. | 9822a1c0-bd79.. | SUCCESS | None .. |
  | df6f.. | creat.. | sample_backup_.. | 9822a1c0-bd79.. | SUCCESS | None .. |
  | 8513.. | wait_.. | sample_backup_.. | 9822a1c0-bd79.. | SUCCESS | None .. |
  | fc62.. | delet.. | sample_backup_.. | 9822a1c0-bd79.. | SUCCESS | None .. |
  +-----..-+------..-+---------------..-+--------------..-+---------+------..-+

