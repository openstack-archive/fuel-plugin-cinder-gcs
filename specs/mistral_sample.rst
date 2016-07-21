==============================
Sample Mistral backup workflow
==============================

The workflow can be imported to Mistral to perform backups in an automated way.

Problem description
===================

Any backup strategy requires taking backups on regular basis
and it's good to have these repeatable actions automated.

Taking a drive backup is often considered as a single action but
usually requires taking a snapshot, taking a backup of the snapshot and
then deleting the snapshot. So taking a drive backup is actually a workflow.

Mistral is a workflow service for OpenStack cloud.

Creating a workflow for Mistral requires some practice and
working workflow example should make it easier to start using Mistral
for the backup process automation.

Proposed changes
================

Provide an example of Mistral workflow for creating backups.

The sample is written in Mistral DSL v2.

The workflow accepts the following input parameters:

  - project_id_list - list of project identifiers.
    Backup of all volumes of projects from project_id_list
    will be taken if not provided.
    Mutually exclusive with volume_id_list.
    Optional.
  - volume_id_list - list of volume identifiers.
    Backup of volumes from volume_id_list will be taken.
    Mutually exclusive with project_id_list.
    Optional.
  - is_incremental - create an incremental backup or full.
    Default is false.
    Optional.
  - report_to - list of e-mail addresses to send reports to
    Reports are not e-mailed if not provided.
    Optional.

If neither project_id_list nor volume_id_list are provided then
backup of all volumes of all projects will be taken.
If both project_id_list and volume_id_list are provided
the workflow does not take backups.

create_backups workflow tasks:

  - analyze_input

    - chooses the task to execute next accordingly to input
    - if neither project_id_list nor volume_id_list are provided
      then run get_all_projects_volumes_list
    - if project_id_list is provided but volume_id_list is not
      then run get_volumes_list
    - if volume_id_list is provided but project_id_list is not
      then run create_snapshots task
    - if project_id_list are volume_id_list are provided
      then report error

  - get_all_projects_volumes_list

    - provides list of volumes to backup
    - runs create_snapshots task

  - get_volumes_list

    - provides list of volumes to backup accordingly to project_id_list
    - runs create_snapshots task

  - create_snapshots

    - creates snapshots of selected volumes
    - runs create_backups task

  - create_backups

    - creates backups using the snapshots
    - runs wait_for_backups_completion task

  - wait_for_backups_completion

    - verifies if the backups are in avalilable state
    - runs delete_snapshots task

  - delete_snapshots

    - deletes snapshots
    - runs send_report task

  - send_report

    - sends report if report_to is provided


Web UI
------

None

Nailgun
-------

None

Data model
----------

None

REST API
--------

None

Orchestration
-------------

None

Fuel Client
-----------

None

Fuel Library
------------

None

Limitations
-----------

None

Alternatives
============

A set of separate OpenStack API calls can be invoked by a self written script.

Upgrade impact
==============

None

Security impact
===============

None

Notifications impact
====================

None

End user impact
===============

None

Performance impact
==================

None

Deployment impact
=================

None

Developer impact
================
None

Infrastructure impact
=====================

None

Documentation impact
====================

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:

- Taras Kostyuk <tkostyuk@mirantis.com> - developer

Other contributors:

- Oleksandr Martsyniuk <omartsyniuk@mirantis.com> - feature lead, developer
- Kostiantyn Kalynovskyi <kkalynovskyi@mirantis.com> - developer

Project manager:

- Andrian Noga <anoga@mirantis.com>

Quality assurance:

- Vitaliy Yerys <vyerys@mirantis.com> - qa

Work Items
----------

* Prepare development environment
* Create Mistral workflow
* Test the workflow

Dependencies
============

* Mistral >= 2.0

Testing
=======

TODO

Acceptance criterias
--------------------

* The workflow can be imported to Mistral
* Backups can be created by Mistral
* A report e-mail is received

References
==========

* Mistral’s documentation http://docs.openstack.org/developer/mistral/
* YAQL’s documentation https://yaql.readthedocs.io/en/latest/
