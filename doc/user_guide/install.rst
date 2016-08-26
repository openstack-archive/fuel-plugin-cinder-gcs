Install Google Cloud Storage(GCS) Fuel plugin
---------------------------------------------

Before you proceed with Install Google Cloud Storage(GCS) Fuel plugin
installation, verify that:

#. You have completed steps from Prerequisites section.

#. All the nodes of your future environment are ``DISCOVERED`` on the
   Fuel Master node.

**To install the Google Cloud Storage(GCS) Fuel plugin plugin:**

#. Download Google Cloud Storage(GCS) Fuel plugin from the
   `Fuel Plugin Catalog
<https://www.mirantis.com/products/openstack-drivers-and-plugins/fuel-plugins/>`.

#. Copy the plugin ``.rpm`` package to the Fuel Master node:

   .. code-block:: console

     $ scp fuel-plugin-cinder-gcs-1.0-1.0.0-1.noarch.rpm <Fuel Master node
ip>:/tmp

#. Log in to the Fuel Master node CLI as root.

#. Install the plugin:

   .. code-block:: console

     # fuel plugins --install /tmp/fuel-plugin-cinder-gcs-1.0-1.0.0-1.noarch.rpm

#. Verify that the plugin was installed successfully:

   .. code-block:: console

     # fuel plugins

     id | name                   | version | package_version | releases
     ---+------------------------+---------+-----------------+--------------------
     2  | fuel-plugin-cinder-gcs | 1.0.0   | 4.0.0           | ubuntu (mitaka-9.0)

#. Proceed to Configure section.
