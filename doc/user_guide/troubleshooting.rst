Troubleshooting
---------------

This section contains a guidance on how to verify Cinder is configured for using
Google Cloud Storage backup driver and where to look for logs.

Finding logs
^^^^^^^^^^^^

LVM as backend for Cinder volumes
"""""""""""""""""""""""""""""""""

Backup-related Cinder logs can be found in ``/var/log/cinder/cinder-backup.log``
on nodes with *cinder* role.

Ceph as backend for Cinder volumes
""""""""""""""""""""""""""""""""""

Backup-related Cinder logs can be found in ``/var/log/cinder/cinder-backup.log`` 
on nodes with *controller* role.

Finding configuration files
^^^^^^^^^^^^^^^^^^^^^^^^^^^

LVM as backend for Cinder volumes
"""""""""""""""""""""""""""""""""

Backup-related Cinder parameters are stored in /etc/cinder/cinder.conf on
*cinder* nodes.

Ceph as backend for Cinder volumes
""""""""""""""""""""""""""""""""""

Backup-related Cinder parameters are stored in /etc/cinder/cinder.conf on
*controller* nodes.

Verifying GCS Cinder backup driver is enabled
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If GCS Cinder backup driver is enabled *[DEFAULT]* section of *cinder.conf*
should contain

``backup_driver = cinder.backup.drivers.google``

and

``backup_gcs_credential_file = /var/lib/cinder/credentials.json``

``/var/lib/cinder/credentials.json`` should contain the same information as
the credentials file downloaded from Google Cloud Storage UI.

