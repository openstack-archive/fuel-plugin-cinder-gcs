=======================================
Integration with Mistral plugin testing
=======================================


Verify GCS plugin working correctly in integration with Mistral plugin
----------------------------------------------------------------------


ID
##

gcs_mistral_integration


Description
###########

Check deploy env with Mistral and GCS Fuel plugins installed


Complexity
##########

manual


Steps
#####

    1. Create cluster
    2. Install Mistral Fuel plugin
    3. Install GCS Fuel plugin
    4. Configure GCS Fuel plugin
    5. Add 3 Controller-mistral nodes
    6. Add 1 compute and cinder +LVM node
    7. Deploy cluster
    8. Run OSTF
    9. Create a volume
    10. Using workbook from examples in gcs plugin on master node, backup
        volume


Expected results
################

All steps must be completed successfully, without any errors.