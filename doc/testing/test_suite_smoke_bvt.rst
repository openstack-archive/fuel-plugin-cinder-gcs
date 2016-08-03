=========
BVT tests
=========


Smoke test
----------


ID
##

gcs_deploy_smoke

Description
###########

BVT test for Google Cloud Storage fuel plugin. Deploy cluster with controller,
compute and cinder nodes and install plugin.

Complexity
##########

core

Steps
#####

    1. Upload plugin to the master node
    2. Install plugin
    3. Create cluster
    4. Add 1 nodes with controller role
    5. Add 1 node with compute role
    6. Add 1 node with cinder role
    7. Deploy the cluster

Expected results
################

All steps must be completed successfully, without any errors.



BVT test
--------


ID
##


gcs_deploy_bvt

Description
###########

BVT test for Google Cloud Storage fuel plugin. Deploy cluster in HA mode with
3 controllers, compute and cinder nodes and install plugin.

Complexity
##########

core

Steps
#####

    1. Upload plugin to the master node
    2. Install plugin
    3. Create cluster
    4. Add 3 nodes with controller role
    5. Add 1 node with compute role
    6. Add 1 node with cinder role
    7. Deploy the cluster
    8. Run network verification
    9. Check plugin installation
    10. Run OSTF

Expected results
################

All steps must be completed successfully, without any errors.
