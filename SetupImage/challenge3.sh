
#Variables
#$location - retrieve a list of locations
#$storageaccount - generate a random account name
#Need to:
#1. Login
#2. Select subscription
#3. Select location
#4. Generate randomized storage account name

azure login 
azure config mode arm
azure group create -l $location onprem-RG
azure network vnet create -g onprem-RG -l $location --name onprem-VNET --address-prefixes 192.168.0.0/24 
azure network vnet subnet create -g onprem-RG -e onprem-VNET -n hosts -a 192.168.0.0/25
azure network vnet create -g onprem-RG -l $location --name azure-VNET --address-prefixes 192.168.1.0/24 
azure network vnet subnet create -g onprem-RG -e azure-VNET -n hosts -a 192.168.1.0/25
azure network public-ip create -g onprem-RG -l $location -n onpremhost-PIP
azure network public-ip create -g onprem-RG -l $location -n onpremee-PIP
azure network public-ip create -g onprem-RG -l $location -n azurehost-PIP
azure network nic create -g onprem-RG -l $location -n onpremhost-NIC -k hosts -m onprem-VNET -p onpremhost-PIP
azure network nic create -g onprem-RG -l $location -n onpremee-NIC -k hosts -m onprem-VNET -p onpremee-PIP
azure network nic create -g onprem-RG -l $location -n azurehost-NIC -k hosts -m azure-VNET -p azurehost-PIP
azure storage account create -g onprem-RG -l $location --sku-name LRS --kind Storage $storageaccount
azure vm docker create -g onprem-RG -l $location -y Linux -Q Canonical:ubuntuserver:16.04-LTS:latest -u student -M ~/.ssh/id_rsa.pub -z STANDARD_A1_V2 -o $storageaccount -f onpremhost-NIC -n onpremhost-VM
azure vm create -g onprem-RG -l $location -y Linux -Q Canonical:ubuntuserver:16.04-LTS:latest -u student -M ~/.ssh/id_rsa.pub -z STANDARD_A1_V2 -o $storageaccount -f onpremee-NIC -n onpremee-VM
azure vm docker create -g onprem-RG -l $location -y Linux -Q Canonical:ubuntuserver:16.04-LTS:latest -u student -M ~/.ssh/id_rsa.pub -z STANDARD_A1_V2 -o $storageaccount -f azurehost-NIC -n azurehost-VM
