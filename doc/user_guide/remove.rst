Uninstall Google Cloud Storage(GCS) Fuel plugin
-----------------------------------------------

To uninstall GCS Fuel plugin, follow the steps below:

#. Log in to the Fuel Master node CLI.

#. Delete all the environments with GCS Fuel plugin enabled:

   .. code-block:: console

    # fuel --env <ENV_ID> env delete

#. Uninstall the plugin:

   .. code-block:: console

     # fuel plugins --remove fuel-plugin-cinder-gcs==1.0.0

#. Verify whether GCS Fuel plugin was uninstalled successfully:

   .. code-block:: console

     # fuel plugins

   GCS Fuel plugin should not appear in the output list.

.. raw:: latex

   \pagebreak
