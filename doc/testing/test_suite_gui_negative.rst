====================
GUI negative testing
====================


Check the plugin reaction on non-consistent data in plugin configuration fields
-------------------------------------------------------------------------------


ID
##

gcs_non_consistent_configuration


Description
###########

Verify that during plugin configuration, non-consistent input into plugin
configuration fields are handled properly.


Complexity
##########

manual


Steps
#####

    1. Deploy fuel master node
    2. Enable GCS plugin
    3. Verify that multiple lines in plugin fields are handled correctly
    4. Verify if special characters in url fields are handled properly
    5. Verify 'Client E-mail' field with incorrect patterns for e-mail


Expected results
################

All incorrect inputs must be handled properly, and warning should be displayed.


Check the plugin reaction on invalid configuration, typos verification
----------------------------------------------------------------------


ID
##

gcs_invalid_configuration


Description
###########

Verify that during plugin configuration with invalid data, proper errors are
displayed after a attempt of deployment.


Complexity
##########

manual


Steps
#####

    1. Create an environment with 1 controller, compute, cinder node
    2. Enable GCS plugin
    3. Configure plugin with invalid bucket location
    4. Verify that during deployment of changes proper error/warning is shown
    5. Configure plugin with invalid storage class
    6. Verify that during deployment of changes proper error/warning is shown
    7. Configure plugin with invalid private key
    8. Verify that during deployment of changes proper error/warning is shown


Expected results
################

Steps 4, 6, 8 will fail with proper error message.
