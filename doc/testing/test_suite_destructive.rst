===================
Destructive testing
===================


Verify master controller fail in HA cluster  will not crash the system
----------------------------------------------------------------------


ID
##

gcs_controller_failover


Description
###########

Verify that after non-graceful shutoff of controller node, cluster stays
operational and after turning it back online, cluster is operational.


Complexity
##########

manual


Steps
#####

    1. Create an environment with 3 controller nodes at least
    2. Install and configure GCS plugin
    3. Deploy cluster
    4. Verify Cluster using OSTF
    5. Verify GCS plugin
    6. Power off main controller (non-gracefully)
    7. Run OSTF
    8. Verify GCS plugin
    9. Power on controller which was powered off in step 6.
    10. Run OSTF
    11. Verify GCS plugin


Expected results
################

All steps except step 7 must be completed successfully, without any errors.
Step 7 one OSTF HA test will fail, because one of controllers is offline - this
is expected.


Verify compute node fail in Non-HA cluster will not crush the system
--------------------------------------------------------------------


ID
##

gcs_compute_failover


Description
###########

Verify that after non-graceful shutoff of compute node cluster stays
operational and after turning it back online, cluster is operational.


Complexity
##########

manual


Steps
#####

    1. Create an environment with 1 controller, cinder and 2 compute nodes
    2. Install and configure GCS plugin
    3. Deploy cluster
    4. Run OSTF
    5. Verify GCS plugin
    6. Power off one of the computes (non-gracefully)
    7. Run OSTF
    8. Verify GCS plugin
    9. Power on compute which was powered off in step 6
    10. Run OSTF
    11. Verify GCS plugin


Expected results
################

All steps except step 7 must be completed successfully, without any errors.
Step 7 one OSTF test will fail, because one of nodes is offline - this is
expected.


Verification of Cinder node non-graceful shutoff in HA cluster
--------------------------------------------------------------


ID
##

gcs_cinder_failover


Description
###########

Verify that after non-graceful shutoff of cinder node cluster stays
operational and after turning it back online, cluster is operational.


Complexity
##########

manual


Steps
#####

    1. Create an environment with 1 controller, compute and 2 cinder nodes
    2. Install and configure GCS plugin
    3. Deploy cluster
    4. Run OSTF
    5. Verify GCS plugin
    6. Power off one of the cinder nodes (non-gracefully)
    7. Run OSTF
    8. Verify GCS plugin
    9. Power on cinder node which was powered off in step 6
    10. Run OSTF
    11. Verify GCS plugin


Expected results
################

All steps except step 7 must be completed successfully, without any errors.
Step 7 one OSTF test will fail, because one of nodes is offline - this is
expected.
