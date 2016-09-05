===================
Integration testing
===================


Deploy GCS plugin with Ceph-osd standalone nodes
------------------------------------------------


ID
##

gcs_ceph


Description
###########

Check deploy an environment with Ceph-OSD standalone nodes


Complexity
##########

Core


Steps
#####

    1. Create an environment with 3 Ceph-OSD nodes at least
    2. Enable and configure GCS plugin
    3. Deploy cluster with plugin
    4. Run OSTF tests
    5. Verify GCS plugin


Expected results
################

All steps must be completed successfully, without any errors.


Deploy with GCS plugin and cinder-multirole
-------------------------------------------


ID
##

gcs_cinder_multirole


Description
###########

Check deploy an environment with cinder-multirole


Complexity
##########

Core


Steps
#####

    1. Create an environment with controller+cinder and compute+cinder nodes
    2. Enable and configure GCS plugin
    3. Deploy cluster with plugin
    4. Run OSTF tests
    5. Verify GCS plugin


Expected results
################

All steps must be completed successfully, without any errors.


