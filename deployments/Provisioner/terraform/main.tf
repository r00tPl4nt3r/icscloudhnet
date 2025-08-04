# main.tf
provider "azurerm" {
  features {}

  subscription_id = var.subscription_id
}

# generate a small random suffix for globally-unique storage account names
resource "random_string" "suffix" {
  length  = 6
  upper   = false
  numeric = true
  special = false
}

resource "azurerm_resource_group" "resource_group" {
  name     = "trapnet_Provisioner"
  location = "West Europe"
}

resource "azurerm_storage_account" "sa" {
  name                     = "trapnetprovisioner${random_string.suffix.result}"
  resource_group_name      = azurerm_resource_group.resource_group.name
  location                 = azurerm_resource_group.resource_group.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  min_tls_version          = "TLS1_2"
  access_tier              = "Cool"      
}

resource "azurerm_storage_container" "certs" {
  name                  = "certs"
  storage_account_name  = azurerm_storage_account.sa.name
  container_access_type = "private"
}

resource "azurerm_virtual_network" "vnet" {
  name                = "trapnet_Provisioner-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.resource_group.location
  resource_group_name = azurerm_resource_group.resource_group.name
}

resource "azurerm_subnet" "subnet" {
  name                 = "trapnet_Provisioner-subnet"
  resource_group_name  = azurerm_resource_group.resource_group.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.100.0/24"]
}

resource "azurerm_public_ip" "public_ip" {
  name                = "trapnet_Provisioner-public-ip"
  location            = azurerm_resource_group.resource_group.location
  resource_group_name = azurerm_resource_group.resource_group.name
  allocation_method   = "Dynamic"
  sku                 = "Basic"

  domain_name_label = var.domain_name_label
}


resource "azurerm_network_security_group" "nsg" {
  name                = "trapnet_Provisioner-nsg"
  location            = azurerm_resource_group.resource_group.location
  resource_group_name = azurerm_resource_group.resource_group.name

  security_rule {
    name                       = "allow_custom_ssh"
    priority                   = 1001
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22122"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  security_rule {
    name                       = "allow_https"
    priority                   = 1002
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "443"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}


resource "azurerm_network_interface" "nic" {
  name                = "trapnet_Provisioner-nic"
  location            = azurerm_resource_group.resource_group.location
  resource_group_name = azurerm_resource_group.resource_group.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.subnet.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.public_ip.id
  }
}

resource "azurerm_network_interface_security_group_association" "nsg_association" {
  network_interface_id      = azurerm_network_interface.nic.id
  network_security_group_id = azurerm_network_security_group.nsg.id
}


resource "azurerm_linux_virtual_machine" "vm" {
  name                = "ProvisionerVM"
  location            = azurerm_resource_group.resource_group.location
  resource_group_name = azurerm_resource_group.resource_group.name
  size                = "Standard_DS1_v2"
  admin_username      = "azureuser"
  network_interface_ids = [
    azurerm_network_interface.nic.id,
  ]

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
    name                 = "Provisioner-os-disk"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts-gen2"
    version   = "latest"
  }

  admin_ssh_key {
    username   = "azureuser"
    public_key = var.ssh_public_key
  }

  disable_password_authentication = true

   custom_data = base64encode(<<EOF
#cloud-config
package_update: true
package_upgrade: true
packages:
  - git
runcmd:
  # SSH configuration
  - sed -i 's/#Port 22/Port 22122/' /etc/ssh/sshd_config
  - systemctl restart sshd

  # Install Docker
  - apt-get update
  - apt-get install -y ca-certificates curl gnupg lsb-release
  - install -m 0755 -d /etc/apt/keyrings
  - curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
  - chmod a+r /etc/apt/keyrings/docker.gpg
  - echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
  - apt-get update
  - apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
  - systemctl enable docker
  - systemctl start docker
  - usermod -aG docker azureuser

  # Install Docker Compose

  - mkdir -p /home/azureuser/repos
  - chown azureuser:azureuser /home/azureuser/repos
  - su - azureuser -c 'git clone https://github.com/r00tPl4nt3r/trapnet.git /home/azureuser/repos/trapnet'

  # Run docker builds and compose as azureuser
  - su - azureuser -c 'cd /home/azureuser/repos/trapnet/deployments/Provisioner/docker/
  - docker build -t trapnet-ca ./ca/
  - docker build -t trapnet-api ./flask/
  - docker build -t trapnet-provisioner ./provisioner/
  - docker build -t trapnet-wg ./wg/
  - docker compose up -d'

  # Upload certificates to Azure Blob Storage
  - apt-get update && apt-get install -y curl
  - STORAGE_ACCOUNT="${azurerm_storage_account.sa.name}"
  - CONTAINER="${azurerm_storage_container.certs.name}"
  - SAS_TOKEN="${data.azurerm_storage_account_sas.upload.sas}"
  - |
    for f in client.crt client.key ca.crt; do
      ls -la "/home/azureuser/repos/trapnet/deployments/Provisioner/docker/client/certs/$f"
      curl -X PUT -T "/home/azureuser/repos/trapnet/deployments/Provisioner/docker/client/certs/$f" \
            -H "x-ms-blob-type: BlockBlob" \
            "https://${azurerm_storage_account.sa.name}.blob.core.windows.net/${azurerm_storage_container.certs.name}/$f${data.azurerm_storage_account_sas.upload.sas}"
    done
EOF
  )
}


