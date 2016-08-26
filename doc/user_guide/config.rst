Configure an environment with Google Cloud Storage(GCS) Fuel plugin
-------------------------------------------------------------------

Configuring and deploying an environment with Google Cloud Storage(GCS) Fuel
plugin involves creating an environment in Fuel and modifying the environment
settings.

Google Cloud Storage(GCS) Fuel plugin settings are divided into two parts:
* Mandatory settings

  * Are always visible
  * Empty settings must be filled
  * Filled settings must be verified
  * Most of the parameters can be taken from the GCS credentials file

* Additional settings

  * Are only visible when 'Show advanced settings' is enabled
  * Have reasonable defaults
  * Usually there is no need to change them

**To configure an OpenStack environment with
Google Cloud Storage(GCS) Fuel plugin:**

#. Using the Fuel web UI, follow steps 1 to 5 of the `Create a new OpenStack
   environment
<http://docs.openstack.org/developer/fuel-docs/userdocs/fuel-user-guide/create-environment/start-create-env.html>`
   instruction.

#. In `Other` menu, select `Fuel Cinder GCS plugin` to enable the plugin.

#. Set `GCS Project ID`. Denotes the project ID where the backup bucket will be
   created. It's the value of `project_id` parameter in the GCS credentials
   file.

#. Set `GCS Bucket`. This is a name of existent GCS bucket to use for backup.

#. Set `GCS Bucket Location`. This is a name of the GCS bucket location.

#. Set `GCS Storage Class`. This is storage class of the GCS bucket.

#. Set `GCS Account type`.  This is `type` parameter value from
   the GCS credentials file.

#. Set `GCS Private Key ID`. This is `private_key_id` parameter value from
   the GCS credentials file.

#. Set `GCS Private Key`. This is `private_key` parameter value from
   the GCS credentials file.

#. Set `GCS Client E-mail`. This is `client_email` parameter value from
   the GCS credentials file.

#. Set `GCS Client ID`. This is `client_id parameter` value from
   the GCS credentials file.

#. Set `GCS Auth URI`. This is `auth_uri` parameter value from
   the GCS credentials file.

#. Set `GCS Token URI`. This is `token_uri` parameter value from
   the GCS credentials file.

#. Set `GCS  Auth Provider X509 Cert URL`. This is `auth_provider_x509_cert_url`
   parameter value from the GCS credentials file.

#. Set `GCS Client X509 Cert URL`. This is `client_x509_cert_url`
   parameter value from the GCS credentials file.

#. In case you need to change advanced options enable `Show advanced settings`.
   All advanced settings parameters have reasonable defaults so you can change
   only those you need to. The default values are provided in the parameters
   descriptions. 

#. Change `GCS Object Size`. The size in bytes of GCS backup objects in bytes.
   Must be a multiple of GCS Block Size.

#. Change `GCS Block Size`. The change tracking size for incremental backup in
   bytes.

#. Change `HTTP User-Agent`. HTTP User-Agent string for the GCS API.

#. Change `GCS Reader Chunk Size`. Chunk size for GCS object downloads in bytes.
    Pass in a value of -1 to cause the file to be uploaded as a single chunk.

#. Change `GCS Writer Chunk Size`. Chunk size for GCS object uploads in bytes
    Pass in a value of -1 to cause the file to be uploaded as a single chunk.

#. Change `GCS Retries Number`. Number of times to retry transfers.

#. Change `GCS Retry Error Codes`. A comma separated list of GCS error codes
   for which to initiate a retry.

#. Change `Enable GCS progress Timer`. Enable the timer to send the periodic
   progress notifications to Ceilometer when backing up the volume to
   the GCS backend storage.

#. Press `Save Settings` button.

#. Make additional `configuration adjustments
<http://docs.openstack.org/developer/fuel-docs/userdocs/fuel-user-guide/configure-environment.html>`_.
                                                                                 
#. Proceed to the `environment deployment
<http://docs.openstack.org/developer/fuel-docs/userdocs/fuel-user-guide/deploy-environment.html>`_.

