Troubleshooting
---------------

This section contains a guidance on how to verify Cinder is configured for using
Google Cloud Storage backup driver and where to look for logs.

**Finding logs**

Backup-related Cinder logs can be found on nodes with ``cinder`` role in
``/var/log/cinder/cinder-backup.log``.

**Verifying Cinder configuration files**

Cinder configuration files are located at /etc/cinder/cinder.conf on ``cinder``
nodes.

The following cinder.conf parameters are related to the plugin:

* xxxx
* yyyyy

There is a separate file with GCS credentials.
It's located at ``/var/lib/cinder/credentials.json``.
The file content should be the same as credentials file
downloaded from Google Cloud Storage UI.
