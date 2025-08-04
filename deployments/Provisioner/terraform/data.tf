// data.tf

data "azurerm_storage_account_sas" "upload" {
  # use primary connection string from your storage account
  connection_string = azurerm_storage_account.sa.primary_connection_string

  https_only = true
  start      = "2025-01-01"
  expiry     = "2030-01-01"

  services {
    blob = true
    queue = false
    table = false
    file  = false
  }

  resource_types {
    service   = false
    container = false
    object = true
  }

  permissions {
    tag   = false
    filter = false
    create = true
    write  = true
    read   = false
    delete = false
    list   = false
    add    = false
    update = false
    process = false
  }
}