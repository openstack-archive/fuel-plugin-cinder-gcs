.. _configure:

Configure an environment with GCS Fuel plugin
---------------------------------------------

To create and configure environment with GCS Fuel plugin,
follow the steps below:

#. `Create a new OpenStack environment <http://docs.openstack.org/developer/fuel-docs/userdocs/fuel-user-guide.html>`_
   in Fuel web UI.

#. Use Cinder with LVM backend or CEPH for block storage in
   Storage Backends tab. Additional details on storage planning can be found in
   `Mirantis OpenStack Planning guide <https://docs.mirantis.com/openstack/fuel/fuel-8.0/mos-planning-guide.html#plan-the-storage>`_.

    .. image:: images/storage.png

#. Enable the Google Cloud Storage Fuel plugin in `Additional services`  tab:

    .. image:: images/plugin.png

#. Add nodes and assign them roles:

   * in case if LVM backend for Cinder is enabled

     * At least 1 Controller
     * Desired number of Compute hosts
     * At least 1 Cinder node, the Cinder role can also be added to Compute or
       Controller node

   * in case if CEPH backend is enabled for volumes

     * At least 1 Controller
     * Desired number of Compute hosts
     * At least 3 CEPH OSD hosts, this role can be co-located with other roles

#. Navigate to the `Settings` tab to configure the Fuel GCS plugin parameters.
   All of the plugin settings fields must be filled with correct values,
   most of them do not have default values as they are environment-specific.

Google Cloud Storage(GCS) Fuel plugin settings are logically divided into
two parts:

* Mandatory settings

    .. image:: images/settings.png

  * The project ID
  * The bucket name to store backup data
  * The storage class for the bucket, can be selected from drop-down list
  * Bucket location, a list of locations can be found in
    `Google Cloud storage documentation <https://cloud.google.com/storage/docs/bucket-locations>`_

  * Credentials related settings such as `GCS Account type`, `Private Key ID`,
    `Private Key`, `Client E-mail`, `Client ID`, `Auth URI`, `Token URI`,
    `Auth Provider X509 Cert URL`, `Client X509 Cert URL` should be copied from
    corresponding fields of credentials JSON file. This file is downloaded from
    `Google Cloud Console <https://console.cloud.google.com/apis/credentials>`_
    on new service account creation at API management page.

* Advanced settings

    .. image:: images/advanced_settings.png

This section is visible only when `Show advanced settings` checkbox is enabled.
Changing values here may be required to override the  default settings for
Google Cloud Cinder backup driver.
The fields have reasonable default values, which correspond to driver defaults.
Please see `OpenStack documentation <http://docs.openstack.org/mitaka/config-reference/block-storage/backup/gcs-backup-driver.html>`_
for a list of GCS backup driver configuration options.

#. Press `Save Settings` button.

#. Make additional
   `configuration adjustments <http://docs.openstack.org/developer/fuel-docs/userdocs/fuel-user-guide/configure-environment.html>`__.

#. Proceed to the
   `environment deployment <http://docs.openstack.org/developer/fuel-docs/userdocs/fuel-user-guide/deploy-environment.html>`__.
