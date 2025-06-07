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