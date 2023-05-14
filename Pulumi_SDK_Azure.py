import * as azure from "@pulumi/azure";

const resourceGroup = new azure.core.ResourceGroup("my-resource-group", {
    location: "eastus",
});

const virtualNetwork = new azure.network.VirtualNetwork("my-virtual-network", {
    resourceGroupName: resourceGroup.name,
    addressSpaces: ["10.0.0.0/16"],
});

const subnet = new azure.network.Subnet("my-subnet", {
    resourceGroupName: resourceGroup.name,
    virtualNetworkName: virtualNetwork.name,
    addressPrefix: "10.0.1.0/24",
});

const networkInterface = new azure.network.NetworkInterface("my-network-interface", {
    resourceGroupName: resourceGroup.name,
    ipConfigurations: [{
        name: "my-ip-configuration",
        subnetId: subnet.id,
    }],
});

const virtualMachine = new azure.compute.VirtualMachine("my-virtual-machine", {
    resourceGroupName: resourceGroup.name,
    networkInterfaceIds: [networkInterface.id],
    vmSize: "Standard_B1ls",
    storageImageReference: {
        publisher: "Canonical",
        offer: "UbuntuServer",
        sku: "16.04-LTS",
        version: "latest",
    },
    storageOsDisk: {
        name: "my-os-disk",
        createOption: "FromImage",
    },
});
