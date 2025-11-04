variable "environment" {
  description = "Environment name"
  type        = string
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
}

variable "instances" {
  description = "Map of instance configurations"
  type = map(object({
    name           = string
    instance_type  = string
    subnet_index   = number
    role           = string
  }))
}

variable "subnet_id" {
  description = "Subnet ID where instances will be launched (legacy, use subnet_ids)"
  type        = string
  default     = ""
}

variable "subnet_ids" {
  description = "List of subnet IDs for instances"
  type        = list(string)
  default     = []
}

variable "security_group_ids" {
  description = "Security group IDs to attach to instances"
  type        = list(string)
}

variable "ami" {
  description = "AMI ID for EC2 instances"
  type        = string
}

variable "root_volume_size" {
  description = "Root volume size in GB"
  type        = number
  default     = 20
}

variable "root_volume_type" {
  description = "Root volume type"
  type        = string
  default     = "gp3"
}

variable "enable_monitoring" {
  description = "Enable detailed CloudWatch monitoring"
  type        = bool
  default     = false
}

variable "key_name" {
  description = "EC2 Key Pair name for SSH access"
  type        = string
  default     = null
}

variable "iam_instance_profile" {
  description = "IAM Instance Profile name"
  type        = string
  default     = null
}

variable "disable_api_termination" {
  description = "Enable termination protection"
  type        = bool
  default     = false
}

variable "credit_specification" {
  description = "T3 credit specification (standard or unlimited)"
  type        = string
  default     = "standard"
}

variable "associate_public_ip" {
  description = "Associate public IP address"
  type        = bool
  default     = false
}

variable "user_data" {
  description = "User data script for cloud-init"
  type        = string
  default     = null
}

variable "tags" {
  description = "Common tags for all resources"
  type        = map(string)
  default     = {}
}
