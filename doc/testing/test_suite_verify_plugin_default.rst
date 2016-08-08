=========
BVT tests
=========


UI test
-------


ID
##

gcs_ui_defaults

Description
###########

Test case designed to verify if plugin is being deployed with correct default
values set.

Complexity
##########

core

Steps
#####

    1. Create cluster
    2. Add 1 nodes with controller role
    3. Add 1 node with compute role
    4. Add 1 node with cinder role
    5. Upload plugin to the master node
    6. Install plugin
    7. Verify default values

Expected results
################

All steps must be completed successfully, without any errors.
