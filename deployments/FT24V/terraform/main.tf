# main.tf
provider "azurerm" {
  features {}

  subscription_id = var.subscription_id
}

resource "azurerm_resource_group" "trapnet_FT24V" {
  name     = "trapnet_FT24V"
  location = "West Europe"
}

resource "azurerm_virtual_network" "vnet" {
  name                = "trapnet_FT24V-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.trapnet_FT24V.location
  resource_group_name = azurerm_resource_group.trapnet_FT24V.name
}

resource "azurerm_subnet" "subnet" {
  name                 = "trapnet_FT24V-subnet"
  resource_group_name  = azurerm_resource_group.trapnet_FT24V.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.1.0/24"]
}

resource "azurerm_public_ip" "public_ip" {
  name                = "trapnet_FT24V-public-ip"
  location            = azurerm_resource_group.trapnet_FT24V.location
  resource_group_name = azurerm_resource_group.trapnet_FT24V.name
  allocation_method   = "Dynamic"
  sku                 = "Basic"

  domain_name_label = var.domain_name_label
}


resource "azurerm_network_security_group" "nsg" {
  name                = "FT24V-nsg"
  location            = azurerm_resource_group.trapnet_FT24V.location
  resource_group_name = azurerm_resource_group.trapnet_FT24V.name

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
    name                       = "allow_wireguard"
    priority                   = 1002
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Udp"
    source_port_range          = "*"
    destination_port_range     = var.wireguard_server_port
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}


resource "azurerm_network_interface" "nic" {
  name                = "trapnet_FT24V-nic"
  location            = azurerm_resource_group.trapnet_FT24V.location
  resource_group_name = azurerm_resource_group.trapnet_FT24V.name

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
  name                = "FT24V"
  location            = azurerm_resource_group.trapnet_FT24V.location
  resource_group_name = azurerm_resource_group.trapnet_FT24V.name
  size                = "Standard_DS1_v2"
  admin_username      = "azureuser"
  network_interface_ids = [
    azurerm_network_interface.nic.id,
  ]

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
    name                 = "F24V-os-disk"
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
  - wireguard
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
  - mkdir -p /home/azureuser/repos
  - chown azureuser:azureuser /home/azureuser/repos
  - su - azureuser -c 'git clone https://github.com/r00tPl4nt3r/trapnet.git /home/azureuser/repos/trapnet'
  - cd /home/azureuser/repos/trapnet/deployments/FT24V/docker/
  - sudo docker build -t ft/ft-ui-opcua ./ft-ui/ 
  - sudo docker build -t plc/opcua ./opcua-plc/
  - docker compose up -d
  - echo ${var.wireguard_server_private_key} | sudo tee /etc/wireguard/private.key > /dev/null
  - chmod 600 /etc/wireguard/private.key
  - echo ${var.wireguard_server_public_key} | sudo tee /etc/wireguard/public.key > /dev/null
  - echo "[Interface]" | sudo tee /etc/wireguard/wg0.conf > /dev/null
  - echo "Address = ${var.wireguard_server_private_ip}" | sudo tee -a /etc/wireguard/wg0.conf > /dev/null
  - echo "ListenPort = ${var.wireguard_server_port}" | sudo tee -a /etc/wireguard/wg0.conf > /dev/null
  - echo "PostUp = wg set %i private-key /etc/wireguard/private.key" | sudo tee -a /etc/wireguard/wg0.conf > /dev/null

  - echo "[Peer]" | sudo tee -a /etc/wireguard/wg0.conf > /dev/null
  - echo "PublicKey = ${var.wireguard_client_public_key}" | sudo tee -a /etc/wireguard/wg0.conf > /dev/null
  - echo "AllowedIPs = ${var.wireguard_approved_networks}" | sudo tee -a /etc/wireguard/wg0.conf > /dev/null

  - sudo systemctl enable wg-quick@wg0
  - sudo systemctl start wg-quick@wg0
  - echo "WireGuard server setup complete"
  
EOF
  )
}


