output "vm_hostname" {
  value = azurerm_public_ip.public_ip.fqdn
}

output "test_output" {
  value = "hello from terraform"
}

