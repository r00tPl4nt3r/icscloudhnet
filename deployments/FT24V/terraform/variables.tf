variable "subscription_id" {
  description = "Azure subscription ID"
  type        = string
}

variable "ssh_public_key" {
    description = "ssh public key for authentication"
    type        = string
}

variable "domain_name_label" {
    description = "hostname for the public IP address"
    type        = string
}

variable "wireguard_server_private_key" {
    description = "WireGuard server private key"
    type        = string
}

variable "wireguard_server_public_key" {
    description = "WireGuard server public key"
    type        = string
}

variable "wireguard_server_private_ip" {
    description = "WireGuard server private IP address"
    type        = string
}

variable "wireguard_client_public_key" {
    description = "WireGuard client public key"
    type        = string    
     
}

variable "wireguard_server_port" {
    description = "WireGuard server port"
    type        = number
}

variable "wireguard_approved_networks" {
    description = "List of approved networks for WireGuard"
    type        = string
}