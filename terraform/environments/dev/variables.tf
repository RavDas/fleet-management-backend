############################
# Global / provider inputs #
############################
variable "aws_region" {
  type        = string
  description = "AWS region (e.g., us-east-1)."
}

variable "environment" {
  type        = string
  description = "Environment name (e.g., dev, staging, prod)."
}

variable "project_name" {
  type        = string
  description = "Project/application name used for naming and tagging."
}

############################
# AZ & networking inputs   #
############################
variable "azs" {
  type        = list(string)
  default     = []
  description = "Explicit list of AZs to use (optional). If empty, first 2 available AZs will be used."
}

variable "vpc_cidr" {
  type        = string
  description = "CIDR block for the VPC."
  validation {
    condition     = can(cidrnetmask(var.vpc_cidr))
    error_message = "vpc_cidr must be a valid CIDR (e.g., 10.0.0.0/16)."
  }
}

variable "subnet_cidrs" {
  type        = list(string)
  description = "CIDR blocks for subnets (one per AZ in the same order)."
  validation {
    condition     = length(var.subnet_cidrs) > 0 && alltrue([for c in var.subnet_cidrs : can(cidrnetmask(c))])
    error_message = "subnet_cidrs must be a non-empty list of valid CIDRs."
  }
}

############################
# Security inputs          #
############################
variable "enable_ssh" {
  type        = bool
  default     = true
  description = "Whether to open TCP/22 on the instance security group."
}

variable "enable_http" {
  type        = bool
  default     = false
  description = "Whether to open TCP/80 on the instance security group."
}

variable "enable_https" {
  type        = bool
  default     = false
  description = "Whether to open TCP/443 on the instance security group."
}

variable "ssh_cidr_blocks" {
  type        = list(string)
  default     = []
  description = "CIDRs allowed for SSH (required if enable_ssh=true)."
  validation {
    condition     = length(var.ssh_cidr_blocks) == 0 || alltrue([for c in var.ssh_cidr_blocks : can(cidrnetmask(c))])
    error_message = "ssh_cidr_blocks must be valid CIDRs."
  }
}

variable "http_cidr_blocks" {
  type        = list(string)
  default     = []
  description = "CIDRs allowed for HTTP."
  validation {
    condition     = length(var.http_cidr_blocks) == 0 || alltrue([for c in var.http_cidr_blocks : can(cidrnetmask(c))])
    error_message = "http_cidr_blocks must be valid CIDRs."
  }
}

variable "https_cidr_blocks" {
  type        = list(string)
  default     = []
  description = "CIDRs allowed for HTTPS."
  validation {
    condition     = length(var.https_cidr_blocks) == 0 || alltrue([for c in var.https_cidr_blocks : can(cidrnetmask(c))])
    error_message = "https_cidr_blocks must be valid CIDRs."
  }
}

variable "enable_k8s_api" {
  type        = bool
  default     = true
  description = "Whether to open TCP/6443 for Kubernetes API Server."
}

variable "enable_k8s_nodeport" {
  type        = bool
  default     = true
  description = "Whether to open TCP/6000-10250 for Kubernetes NodePort services."
}

variable "enable_vxlan" {
  type        = bool
  default     = true
  description = "Whether to open UDP/8472 for VXLAN overlay network (CNI)."
}

variable "k8s_api_cidr_blocks" {
  type        = list(string)
  default     = []
  description = "CIDRs allowed for Kubernetes API Server access."
  validation {
    condition     = length(var.k8s_api_cidr_blocks) == 0 || alltrue([for c in var.k8s_api_cidr_blocks : can(cidrnetmask(c))])
    error_message = "k8s_api_cidr_blocks must be valid CIDRs."
  }
}

variable "k8s_nodeport_cidr_blocks" {
  type        = list(string)
  default     = []
  description = "CIDRs allowed for Kubernetes NodePort services."
  validation {
    condition     = length(var.k8s_nodeport_cidr_blocks) == 0 || alltrue([for c in var.k8s_nodeport_cidr_blocks : can(cidrnetmask(c))])
    error_message = "k8s_nodeport_cidr_blocks must be valid CIDRs."
  }
}

variable "vxlan_cidr_blocks" {
  type        = list(string)
  default     = []
  description = "CIDRs allowed for VXLAN overlay network."
  validation {
    condition     = length(var.vxlan_cidr_blocks) == 0 || alltrue([for c in var.vxlan_cidr_blocks : can(cidrnetmask(c))])
    error_message = "vxlan_cidr_blocks must be valid CIDRs."
  }
}

############################
# Compute inputs           #
############################
variable "instance_count" {
  type        = number
  description = "Number of EC2 instances to launch."
  validation {
    condition     = var.instance_count >= 1 && floor(var.instance_count) == var.instance_count
    error_message = "instance_count must be a positive integer."
  }
}

variable "instance_type" {
  type        = string
  description = "EC2 instance type (e.g., t3.large)."
}

variable "ami" {
  type        = string
  description = "AMI ID for the instances (e.g., Ubuntu 24.04)."
}

variable "key_name" {
  type        = string
  description = "Existing EC2 Key Pair name for SSH."
}

variable "enable_monitoring" {
  type        = bool
  default     = false
  description = "Enable EC2 detailed monitoring."
}

variable "iam_instance_profile" {
  type        = string
  default     = null
  description = "IAM Instance Profile name (optional; e.g., to enable SSM)."
}

variable "root_volume_size" {
  type        = number
  description = "Root EBS volume size in GiB."
  validation {
    condition     = var.root_volume_size >= 8
    error_message = "root_volume_size must be >= 8 GiB."
  }
}

variable "root_volume_type" {
  type        = string
  default     = "gp3"
  description = "Root EBS volume type (gp3, gp2, io1, io2, st1, sc1, standard)."
}

variable "disable_api_termination" {
  type        = bool
  default     = false
  description = "Protect instances from being terminated via API/console."
}

variable "credit_specification" {
  type        = string
  default     = "standard"
  description = "For T-family instances: standard or unlimited."
  validation {
    condition     = contains(["standard", "unlimited"], var.credit_specification)
    error_message = "credit_specification must be 'standard' or 'unlimited'."
  }
}

variable "associate_public_ip" {
  type        = bool
  default     = false
  description = "Associate a public IP (only effective if subnet mapping allows public IPs)."
}

variable "user_data" {
  type        = string
  default     = null
  description = "Optional cloud-init/user-data script."
}
