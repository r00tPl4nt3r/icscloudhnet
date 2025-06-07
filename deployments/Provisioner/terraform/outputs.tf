output "deployment_output" {
  value = "Provisioner"
}


output "vm_hostname" {
  value = azurerm_public_ip.public_ip.fqdn
}


output "public_ip" {
  value = azurerm_public_ip.public_ip.ip_address
}