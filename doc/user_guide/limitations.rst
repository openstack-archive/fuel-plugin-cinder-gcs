Limitations
-----------

Google Cloud Storage(GCS) Fuel plugin 1.0.0 has the following limitations:

* Cinder does not support multiple backup backends at the same time so switching
  backup backend for a cloud with some backups already created by another driver
  may not be possible without losing access to previously created backups.

* A single GCS bucket can be used per OpenStack environment.
