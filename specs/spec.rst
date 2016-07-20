================================
Google Cloud Storage Fuel Plugin
================================

The GCS plugin allows Fuel to deploy OpenStack with support of
OpenStack Cinder backup driver for Google Cloud Storage.

Problem description
===================
Since Mitaka release, OpenStack supports Cinder backup driver for
Google Cloud Storage.

The user who decided to store backups of their OpenStack VMs in
Google Cloud Storage have to configure Cinder and OpenStack Cinder backup driver
for Google Cloud Storage on a number of OpenStack nodes manually.

Fuel is a widely used automation tool for deploying OpenStack clouds but
currently does not support the backup driver installation and configuration.

As backups often need to be automated sample YAML files with descriptions of
Mistral workflows is required too.

Proposed changes
================

Implement Fuel plugin to automate Cinder and Cinder backup driver for
Google Cloud Storage installation and configuration.
Provide sample Mistral workflows.

OpenStack backups are stored as objects in object storages like Swift or Ceph.
Also other objects are stored in object storage. This plugin impacts only
backups. Other objects will be stored in the object storage selected during
the environment creation.

Before deployment user has to download and install GCS plugin into Fuel Master.
Driver inclusion and configuration will be done by Puppet manifests included
in plugin.

The cinder plugin for Google backup is included in Cinder package for Mitaka.

After installation of plugin RPM package, additional file must be placed
manually on master node. This file contains GCS service account credentials in
JSON format, and will be copied automatically to cinder nodes.

The plugin will deploy changes in the following way

* Copy credentials file to all cinder nodes
* Install python packages for Google Cloud Storage client on cinder nodes
* Modify cinder.conf:

  * Enable google backup driver in backup_driver variable
  * Set up configuration options for driver such as bucket name, project ID,
    path to credentials file

* Restart cinder services to use updated parameters

Volume Backup Workflow
----------------------

The steps that occur when a user requests that a Cinder volume be backed up.

#. User request to backup a Cinder volume by invoking REST API (client may use
   python-cinderclient CLI utility).
#. cinder-api process validates request, user credentials; once validated,
   posts message to backup manager over AMQP.
#. cinder-backup reads message from queue, creates a database record for
   the backup and fetches information from the database for the volume
   to be backed up.
#. cinder-backup invokes the backup_volume method of the Cinder volume driver
   corresponding to volume to be backed up, passing the backup record and
   the connection for the backup service to be used.
#. The appropriate Cinder volume driver attaches to the source Cinder volume.
#. The volume driver invokes the backup method for the configured
   backup service, handing off the volume attachment.
#. The backup service transfers the Cinder volume's data and metadata to
   the GCS using GCS driver.
#. The backup service updates the database with the completed record for
   this backup and posts response information to cinder-api process via
   AMQP queue.
#. cinder-api process reads response message from queue and passes results in
   RESTful response to the client.

Web UI
------

Fuel Web UI is extended with plugin-specific settings.

The settings are:

* A checkbox to enable Google Cloud Storage Fuel Plugin.

* GCS Project ID

  * name: backup_gcs_project_id
  * label: GCS Project ID
  * description: Denotes the project ID where the backup bucket will be created
  * type: text
  * value: ‘’
  * regexp: is like GCS Project ID

* GCS Bucket

  * name: backup_gcs_bucket
  * label: GCS Bucket
  * description: GCS bucket name to use for backup. Please refer to
    the official bucket naming guidelines
    https://cloud.google.com/storage/docs/naming
  * type: text
  * value: ‘’
  * regexp: match https://cloud.google.com/storage/docs/naming

* GCS Bucket Location

  * name: backup_gcs_bucket_location
  * label: GCS Bucket Location
  * description: Location of GCS bucket
    Details at https://cloud.google.com/storage/docs/bucket-locations
    Defaults to ‘us’ if empty
  * type: text
  * value: ‘us’
  * regexp: alphanumeric with dashes

* GCS Storage Class

  * name: backup_gcs_storage_class
  * label: GCS Storage Class
  * description: Storage class of GCS bucket
    Defaults to ‘NEARLINE’ if empty
  * type: text
  * value: ‘NEARLINE’
  * regexp: a valid storage class

* Show advanced settings

  * name: backup_gcs_advanced_settings
  * label: Show advanced settings
  * description: When selected all GCS Cinder driver settings are shown
  * type: checkbox

* GCS Object Size

  * name: backup_gcs_object_size
  * label: GCS Object Size
  * description: The size in bytes of GCS backup objects in bytes
    Must be a multiple of GCS Block Size
    Defaults to 52428800 bytes if empty
  * type: text
  * value: 52428800
  * regexp: is a number within allowed range OR is empty
  * visibility: only when backup_gcs_advanced_settings is selected

* GCS Block Size

  * name: backup_gcs_block_size
  * label: GCS Block Size
  * description: The change tracking size for incremental backup in bytes
    Defaults to 327678 bytes if empty
  * type: text
  * value: 327678
  * regexp: is a number within allowed range OR is empty
  * visibility: only when backup_gcs_advanced_settings is selected

* HTTP User-Agent

  * name: backup_gcs_user_agent
  * label: HTTP User-Agent
  * description: HTTP User-Agent string for the GCS API
  * type: text
  * value: not defined
  * regexp: a valid string for HTTP User-Agent OR empty
  * visibility: only when backup_gcs_advanced_settings is selected

* GCS Reader Chunk Size

  * name: backup_gcs_reader_chunk_size
  * label: GCS Reader Chunk Size
  * description: Chunk size for GCS object downloads in bytes
    Defaults to 2097152 bytes if empty
  * type: text
  * value: 2097152
  * regexp: a number within allowed range OR empty
  * visibility: only when backup_gcs_advanced_settings is selected

* GCS Writer Chunk Size

  * name: backup_gcs_writer_chunk_size
  * label: GCS Writer Chunk Size
  * description: Chunk size for GCS object uploads in bytes
    Pass in a value of * -1 to cause the file to be uploaded as a single chunk
    Defaults to 2097152 bytes if empty
  * type: text
  * value: 2097152
  * regexp: a number within allowed range OR empty OR -1
  * visibility: only when backup_gcs_advanced_settings is selected


* GCS Retries Number

  * name: backup_gcs_num_retries
  * label: GCS Retries Number
  * description: Number of times to retry transfers
    Defaults to 3 if empty
  * type: text
  * value: 3
  * regexp: valid number OR empty
  * visibility: only when backup_gcs_advanced_settings is selected

* GCS Retry Error Codes

  * name: backup_gcs_retry_error_codes
  * label: GCS Retry Error Codes
  * description: List of GCS error codes for which to initiate a retry
    Defaults to [‘429’] if empty
  * type: text
  * value: [‘429’]
  * regexp: valid list of numbers
  * visibility: only when backup_gcs_advanced_settings is selected

* GCS progress Timer

  * name: backup_gcs_enable_progress_timer
  * label: GCS progress Timer
  * description: Enable or Disable the timer to send the periodic progress
    notifications to Ceilometer when backing up the volume to
    the GCS backend storage.
  * type: checkbox
  * value: true
  * visibility: only when backup_gcs_advanced_settings is selected

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
Cinder does not support multiple backup backends at the same time so switching
backup backend for a cloud with backup enabled may not be possible without
losing current backups.

Alternatives
============
The plugin can also be implemented as a part of Fuel core but it was decided
to create a plugin as any new additional functionality makes a project and
testing more difficult which is an additional risk for the Fuel release.

Upgrade impact
==============
Compatibility of new Fuel components and the Plugin should be checked before
upgrading Fuel Master.

Security impact
===============
Google Cloud Storage credentials are stored on Fuel Master and
Cinder/Compute nodes and need to be protected from unauthorized use.

Notifications impact
====================
None

End user impact
===============
End user will have more distributed and hybrid cloud, backup storage function
will be delegated to the reliable external storage service provider.

Performance impact
==================
Backup operation performance depends on Google Cloud Storage plan and
the Internet connection speed.

Deployment impact
=================
The plugin can be installed and enabled either during Fuel Master installation
or after an environment is deployed.

Developer impact
================
None

Infrastructure impact
=====================
::

  Diagram showing Cinder components and GCS driver Fig.1 :
  ...............................................
  . ________            __________              .
  .|        |          |          |             .     O
  .| SQL DB |          |Cinder API|<----REST-API---> /|\
  .|________|          |__________|             .    / \
  .                      A                      .
  .                      |                      .
  .                      |                      .
  .                 _____V__                    .
  .                |        |                   .
  .      AMQP----->|RabbitMQ|<-----AMQP---      .
  .      |         |________|            |      .
  .      |                               |      .
  .      |               ________________V_____ .
  .      |              |                      |.
  . _____V_______       |    Cinder Backup     |.
  .|             |      |                      |.
  .|Cinder Volume|      |    ________________  |.
  .|_____________|      |   |  Google Cinder | |.
  .      A              |   |  Backup Driver | |.
  .      |              |___|________________|_|.
  .......|.........................A.............
         |                         |
         |                         | JSON-RPC
    _____V______                   |
   |            |            ______V_____________
   |Storage node|           |                    |
   |____________|           |Google Cloud Storage|
                            |____________________|

  Fig.1 Cinder components and GCS driver

Documentation impact
====================
* Deployment Guide
* User Guide
* Test Plan
* Test Report

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
- Valentyn Khalin <vkhalin@mirantis.com> - qa

Docs Lead:

- ?



Work Items
----------

* Prepare development environment
* Create Fuel plugin bundle which allows setting plugin parameters
  and pass them to Openstack nodes via Hiera
* Implement Puppet manifests to configure Cinder and
  Google Cloud Storage backup driver
* Test Google Cloud Storage Fuel plugin
* Prepare Documentation

Dependencies
============

* At least Fuel 9.0
* At least OpenStack Mitaka
* Internet connection on Cinder and Compute nodes
* file with GCS credentials uploaded to Fuel master node

Testing
=======

* Block storage operations verified using Tempest framework
  with specific test cases:

  - Create,delete, attach, detach volume
  - Create, delete, list snapshots and create volume from snapshot 
  - Create volume from image, from snapshot, from volume (clone)
  - Create image from volume

* System tests including deployment with different options enabled and plugin
  installation included, both LVM and Ceph options have to be verified as
  a Cinder backend for all this cases:

  - Install plugin and deploy environment
  - Install plugin and deploy environment with controller/cinder role
    assigned to a node
  - Install plugin and deploy environment with compute/cinder role assigned to
    a node
  - Remove, add controller node in cluster with plugin
  - Remove, add compute node in cluster with plugin
  - Remove, add cinder node in cluster with plugin
  - Remove, add controller/cinder node in cluster with plugin
  - Remove, add compute/cinder node in cluster with plugin
 
* Functional tests to verify plugin functionality are working correctly:

  - Backup Volume and reattach it to the VM
  - Write/Read data to/from volume

Acceptance criterias
--------------------

* A VM disk backup can be:

  - stored to Google Cloud Storage
  - restored from Google Cloud Storage object
  - removed from Google Cloud Storage
  - scheduled using Mistral

* All blocker, critical and major issues are fixed
* Documentation delivered
* Block, system and functional tests passed successfully
* Test results delivered

References
==========

OpenStack users: Backup your Cinder volumes to Google Cloud Storage
https://cloudplatform.googleblog.com/2016/04/OpenStack-users-backup-your-Cinder-volumes-to-Google-Cloud-Storage.html

