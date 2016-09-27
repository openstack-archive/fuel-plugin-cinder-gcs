===================
GUI verify defaults
===================


UI test
-------


ID
##

gcs_gui_defaults

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
    2. Upload plugin to the master node
    3. Install plugin
    4. Create cluster
    5. Verify default values

Expected results
################

All steps must be completed successfully, without any errors.
