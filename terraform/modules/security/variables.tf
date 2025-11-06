variable "environment" {
  description = "Environment name"
  type        = string
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID where security group will be created"
  type        = string
}

variable "vpc_cidr" {
  description = "VPC CIDR block for internal traffic rules"
  type        = string
}

variable "enable_ssh" {
  description = "Enable SSH access on port 22"
  type        = bool
  default     = true
}

variable "enable_https" {
  description = "Enable HTTPS access on port 443"
  type        = bool
  default     = true
}

variable "enable_http" {
  description = "Enable HTTP access on port 80"
  type        = bool
  default     = false
}

variable "ssh_cidr_blocks" {
  description = "CIDR blocks allowed for SSH access"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "https_cidr_blocks" {
  description = "CIDR blocks allowed for HTTPS access"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "http_cidr_blocks" {
  description = "CIDR blocks allowed for HTTP access"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "tags" {
  description = "Common tags for all resources"
  type        = map(string)
  default     = {}
}
