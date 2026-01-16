variable "environment" {
  description = "Deployment environment name"
  type        = string
  default     = "test"
}

variable "external_account_id" {
  description = "External AWS account ID trusted by the role (Stranger Danger scenario)"
  type        = string
}

variable "vendor_account_id" {
  description = "Vendor AWS account ID for cross-account trust"
  type        = string
}

variable "external_id" {
  description = "External ID used to prevent confused deputy attacks"
  type        = string
  sensitive   = true
}

variable "common_tags" {
  description = "Common tags applied to all IAM roles"
  type        = map(string)
}
