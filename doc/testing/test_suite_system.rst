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

    1. Boot VM and attach volume to it
    2. Write a test file onto volume and get it md5sum value
    3. Backup volume
    4. Destroy VM and volume
    5. Boot VM and restore volume from a GCS
    6. Attach restored volume to a VM
    7. Verify file consistency by comparing md5sum value with value obtained in step 5


Expected results
################

All steps must be completed successfully, without any errors. Both md5sum
values obtained from step 2 and 7 must be the same.
