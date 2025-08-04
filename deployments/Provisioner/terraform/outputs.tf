output "deployment_output" {
  value = "Provisioner"
}


output "vm_hostname" {
  value = azurerm_public_ip.public_ip.fqdn
}


output "public_ip" {
  value = azurerm_public_ip.public_ip.ip_address
}

output "storage_account_name" {
  value = azurerm_storage_account.sa.name
}
output "container_id" {
  value = azurerm_storage_container.certs.id
}

output "primary_blob_endpoint" {
  value = azurerm_storage_account.sa.primary_blob_endpoint
}