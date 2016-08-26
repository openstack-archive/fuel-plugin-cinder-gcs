=====================================
Google Cloud Storage(GCS) Fuel plugin
=====================================

Google Cloud Storage(GCS) Fuel plugin allows Fuel to deploy Mirantis OpenStack with
a possibility to store VM backups in Google Cloud Storage using Cinder Google Cloud Storage backup
driver.

Problem description
===================
Since Mitaka OpenStack release, Cinder supports Google Cloud Storage
backup driver.

The user who decided to store backups of their OpenStack VMs in
GCS have to configure Cinder for using GCS backup driver manually.

Fuel is a widely used automation tool for deploying OpenStack clouds but
currently does not support Cinder GCS backup driver configuration
out of the box.

Proposed changes
================

Develop Fuel plugin to automate Cinder configuration
for using GCS backup driver.

VMs backups are stored as objects in object storages like Swift or Ceph.
Also other objects are stored in object storage. Fuel GCS plugin impacts only
backups. Other objects will be stored in the object storage selected during
the environment creation.

Before deployment user has to download and install the Fuel GCS plugin into Fuel Master.
Driver inclusion and configuration will be done by Puppet manifests included
in the plugin.

The Cinder backup driver for GCS is included in Cinder package since Mitaka
OpenStack release. Fuel GCS plugin should support environments with either LVM
or Ceph used as a block storage.

Before deploying an environment the Fuel GCS plugin has to be configured in Fuel UI or
Fuel API.

The Fuel GCS plugin will deploy changes in the following way

* Create a credentials file on all cinder nodes with resctrive permissions, readable only by Cinder
* Install python packages for Google Cloud Storage client on cinder nodes
* Modify cinder.conf:

  * Overwrite backup_driver parameter value to enable GCS backup driver
  * Set up configuration options for driver such as bucket name, project ID,
    path to credentials file, etc.

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
  * default value: ''
  * valid values: not empty

* GCS Bucket

  * name: backup_gcs_bucket
  * label: GCS Bucket
  * description: GCS bucket name to use for backup. Please refer to
    the official bucket naming guidelines
    https://cloud.google.com/storage/docs/naming
  * type: text
  * default value: ''
  * valid values: not empty

* GCS Bucket Location

  * name: backup_gcs_bucket_location
  * label: GCS Bucket Location
  * description: Location of GCS bucket.
    Check available locations at
    https://cloud.google.com/storage/docs/bucket-locations
  * type: text
  * default value: 'us'
  * valid values: alfanumeric with dashes and underscores

* GCS Storage Class

  * name: backup_gcs_storage_class
  * label: GCS Storage Class
  * description: Storage class of GCS bucket
  * type: dropdown list
  * default value: 'NEARLINE'
  * list values: STANDARD, NEARLINE , DURABLE_REDUCED_AVAILABILITY

* GCS Account type

  * name: gcs_account_type
  * label: GCS Account type
  * description: type parameter value from the GCS credentials file.
  * type: text
  * default value: 'service_account'
  * valid values: alphanumeric and symbols -_

* GCS Private Key ID

  * name: gcs_private_key_id
  * label: GCS Private Key ID
  * description: private_key_id parameter value from the GCS credentials file.
  * type: text
  * default value: ''
  * valid values: alphanumeric

* GCS Privare Key

  * name: gcs_private_key
  * label: GCS Privare Key
  * description: private_key parameter value from the GCS credentials file.
  * type: text
  * default value: ''
  * valid values: alphanumeric and symbols +-/\ and space

* GCS Client E-mail

  * name: gcs_client_email
  * label: GCS Client E-mail
  * description: client_email parameter value from the GCS credentials file.
  * type: text
  * default value: ''
  * valid values: alphanumeric and symbols -.@

* GCS Client ID

  * name: gcs_client_id
  * label: GCS Client ID
  * description: client_id parameter value from the GCS credentials file.
  * type: text
  * default value: ''
  * valid values: digits

* GCS Auth URI

  * name: gcs_auth_uri
  * label: GCS Auth URI
  * description: auth_uri parameter value from the GCS credentials file.
  * type: text
  * default value: 'https://accounts.google.com/o/oauth2/auth'
  * valid values: https://[a-zA-Z][a-zA-Z0-9-_.!~*'() ;/?:@&=+$,%]*

* GCS Token URI

  * name: gcs_token_uri
  * label: GCS Token URI
  * description: token_uri parameter value from the GCS credentials file.
  * type: text
  * default value: 'https://accounts.google.com/o/oauth2/token'
  * valid values: https://[a-zA-Z][a-zA-Z0-9-_.!~*'() ;/?:@&=+$,%]*

* GCS  Auth Provider X509 Cert URL

  * name: gcs_auth_provider_x509_cert_url
  * label: GCS Auth Provider X509 Cert URL
  * description: auth_provider_x509_cert_url parameter value from
    the GCS credentials file.
  * type: text
  * default value: 'https://www.googleapis.com/oauth2/v1/certs'
  * valid values: https://[a-zA-Z][a-zA-Z0-9-_.!~*'() ;/?:@&=+$,%]*

* GCS Client X509 Cert URL

  * name: gcs_client_x509_cert_url
  * label: GCS Client X509 Cert URL
  * description: client_x509_cert_url parameter value from
    the GCS credentials file.
  * type: text
  * default value: ''
  * valid values: https://[a-zA-Z][a-zA-Z0-9-_.!~*'() ;/?:@&=+$,%]*

* Show advanced settings

  * name: backup_gcs_advanced_settings
  * label: Show advanced settings
  * description: Show advanced settings. The driver defaults are used
    if not selected
  * type: checkbox

* GCS Object Size

  * name: backup_gcs_object_size
  * label: GCS Object Size
  * description: The size in bytes of GCS backup objects in bytes.
    Must be a multiple of GCS Block Size. Default is 52428800
  * type: text
  * default value: 52428800
  * valid values: positive integer
  * visibility: only when backup_gcs_advanced_settings is selected

* GCS Block Size

  * name: backup_gcs_block_size
  * label: GCS Block Size
  * description: The change tracking size for incremental backup in bytes.
    Deault is 32768
  * type: text
  * default value: 32768
  * valid values: positive integer
  * visibility: only when backup_gcs_advanced_settings is selected

* HTTP User-Agent

  * name: backup_gcs_user_agent
  * label: HTTP User-Agent
  * description: HTTP User-Agent string for the GCS API.
  * type: text
  * default value: gcscinder
  * valid values: a valid string accordigly to HTTP 1.1 RFC
    http://www.faqs.org/rfcs/rfc2068.html
  * visibility: only when backup_gcs_advanced_settings is selected

* GCS Reader Chunk Size

  * name: backup_gcs_reader_chunk_size
  * label: GCS Reader Chunk Size
  * description: Chunk size for GCS object downloads in bytes.
    Pass in a value of -1 to cause the file to be uploaded
    as a single chunk. Default is 2097152
  * type: text
  * default value: 2097152
  * valid values: positive integer OR -1
  * visibility: only when backup_gcs_advanced_settings is selected

* GCS Writer Chunk Size

  * name: backup_gcs_writer_chunk_size
  * label: GCS Writer Chunk Size
  * description: Chunk size for GCS object uploads in bytes
    Pass in a value of -1 to cause the file to be uploaded
    as a single chunk. Default is 2097152.
  * type: text
  * default value: 2097152
  * valid values: a number in a range from 1 to 5242880 OR -1
  * visibility: only when backup_gcs_advanced_settings is selected


* GCS Retries Number

  * name: backup_gcs_num_retries
  * label: GCS Retries Number
  * description: Number of times to retry transfers.
    Default is 3
  * type: text
  * default value: 3
  * valid values: positive integer
  * visibility: only when backup_gcs_advanced_settings is selected

* GCS Retry Error Codes

  * name: backup_gcs_retry_error_codes
  * label: GCS Retry Error Codes
  * description: A comma sepaated list of GCS error codes for which
    to initiate a retry. Default is 429
  * type: text
  * default value: 429
  * valid values: valid list of HTTP v1.1 error codes (4xx and 5xx)
  * visibility: only when backup_gcs_advanced_settings is selected

* Enable GCS progress Timer

  * name: backup_gcs_enable_progress_timer
  * label: GCS progress Timer
  * description: Enable the timer to send the periodic progress notifications
    to Ceilometer when backing up the volume to the GCS backend storage.
  * type: checkbox
  * default value: true
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
backup backend for a cloud with some backups already created by another driver
may not be possible without losing access to previously created backups.

A single GCS bucket can be used per OpenStack environment.

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
Backup operation performance depends on Google Cloud Storage storage class and
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


Work Items
----------

* Prepare development environment
* Create Fuel plugin bundle which allows setting plugin parameters
  and pass them to OpenStack nodes via Hiera
* Implement Puppet manifests to configure Cinder and
  Google Cloud Storage backup driver
* Test Google Cloud Storage Fuel plugin
* Prepare Documentation

Dependencies
============

* Fuel 9.0
* Ubuntu 14.04
* OpenStack Mitaka
* Internet connection available for Cinder nodes
* File with credentials for GCS service acccount

Testing
=======

* Acceptance testing (this cases will be executed along with CI tests during
  acceptance testing stage):

  * Verification of active OS cloud with GCS fuel plugin installed using tempest
    test framework

  * Performance testing to verify OpenStack cloud with GCS fuel plugin
    installed under heavy load. This testing will be performed using Rally
    benchmark.

  * Failover testing:

    - Destroy controller node in HA mode cluster with plugin
    - Destroy compute node in HA/non-HA mode cluster with plugin
    - Destroy cinder node in HA/non-HA mode cluster with plugin
    - Destroy controller/cinder node in cluster with plugin
    - Destroy compute/cinder node in cluster with plugin

* CI test cases:

  * System tests including deployment with different options enabled and plugin
    installation included, both LVM and Ceph options have to be verified as a
    Cinder backend for all this cases:

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

  * UI test cases:

    - Verify all default values are correct
    - Manual verification of plugin UI dashboard

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

