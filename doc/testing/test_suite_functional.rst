==================
Functional testing
==================


Check that Controller node can be deleted and added again
---------------------------------------------------------


ID
##

gcs_delete_add_controller


Description
###########

Verify that a controller node can be deleted and added after deploying


Complexity
##########

advanced


Steps
#####

    1. Create an environment with 3 controller nodes at least
    2. Enable and configure GCS plugin
    3. Deploy cluster with plugin
    4. Run OSTF tests
    5. Verify GCS plugin
    6. Delete a Controller node and deploy changes
    7. Run OSTF tests
    8. Verify GCS plugin
    9. Add a node with "Controller" role and deploy changes
    10. Run OSTF tests
    11. Verify GCS plugin



Expected results
################

All steps must be completed successfully, without any errors.


Check that Compute node can be deleted and added again
------------------------------------------------------


ID
##

gcs_delete_add_compute


Description
###########

Verify that a compute node can be deleted and added after deploying


Complexity
##########

advanced


Steps
#####

    1. Create an environment with 2 compute nodes at least
    2. Enable and configure GCS plugin
    3. Deploy cluster with plugin
    4. Run OSTF tests
    5. Verify GCS plugin
    6. Delete a compute node and deploy changes
    7. Run OSTF tests
    8. Verify GCS plugin
    9. Add a node with "compute" role and deploy changes
    10. Run OSTF tests
    11. Verify GCS plugin



Expected results
################

All steps must be completed successfully, without any errors.


Check that Cinder node can be deleted and added again
-----------------------------------------------------


ID
##

gcs_delete_add_cinder


Description
###########

Verify that a cinder node can be deleted and added after deploying


Complexity
##########

advanced


Steps
#####

    1. Create an environment with 2 cinder nodes at least
    2. Enable and configure GCS plugin
    3. Deploy cluster with plugin
    4. Run OSTF tests
    5. Verify GCS plugin
    6. Delete a cinder node and deploy changes
    7. Run OSTF tests
    8. Verify GCS plugin
    9. Add a node with cinder role and deploy changes
    10. Run OSTF tests
    11. Verify GCS plugin



Expected results
################

All steps must be completed successfully, without any errors.


Check that the only cinder node can be deleted and added again
--------------------------------------------------------------


ID
##

gcs_delete_add_single_cinder


Description
###########

Verify that the only cinder node can be deleted and added after deploying


Complexity
##########

advanced


Steps
#####

    1. Create an environment with 1 cinder node
    2. Enable and configure GCS plugin
    3. Deploy cluster with plugin
    4. Run OSTF tests
    5. Verify GCS plugin
    6. Delete the cinder node and deploy changes
    7. Run OSTF tests
    8. Add a node with cinder role and deploy changes
    9. Run OSTF tests
    10. Verify GCS plugin



Expected results
################

All steps must be completed successfully, without any errors.


Check that a Ceph-OSD node can be added again
---------------------------------------------


ID
##

gcs_add_ceph


Description
###########

Verify that a Ceph-OSD node can be added after deploying


Complexity
##########

advanced


Steps
#####

    1. Create an environment with Ceph-OSd as a storage backend
    2. Enable and configure GCS plugin
    3. Deploy cluster with plugin
    4. Run OSTF tests
    5. Verify GCS plugin
    6. Add a node with Ceph-OSD role and deploy changes
    7. Run OSTF tests
    8. Verify GCS plugin



Expected results
################

All steps must be completed successfully, without any errors.

