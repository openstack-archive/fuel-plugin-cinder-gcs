==============
System testing
==============


Check data consistency of backed up volume
------------------------------------------


ID
##

gcs_data_consistency_verification


Description
###########

Verify that data writen into volume stays consistent after backup restoration.


Complexity
##########

manual


Steps
#####

    1. Create an environment with 1 controller, compute, cinder node
    2. Enable and configure GCS plugin
    3. Deploy cluster
    4. Boot VM and attach volume to it
    5. Write a test file onto volume and get it md5sum value
    6. Backup volume
    7. Destroy VM and volume
    8. Boot VM and restore volume from a GCS
    9. Attack restored volume to a VM
    10. Verify file consistency by comparing md5sum value with value obtained in step 5


Expected results
################

All steps must be completed successfully, without any errors. Both md5sum
values obtained from step 5 and 10 must be the same.
