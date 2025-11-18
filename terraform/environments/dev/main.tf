terraform {
  required_version = ">= 1.13, < 2.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # backend "s3" {
  #   bucket         = "your-terraform-state-bucket"
  #   key            = "fleet-management/dev/terraform.tfstate"
  #   region         = "us-east-1"
  #   encrypt        = true
  #   dynamodb_table = "terraform-locks"
  # }
}

provider "aws" {
  region  = var.aws_region
  # profile = var.aws_profile  # optional; add var if you use a named profile

  # Single source of truth for common tags
  default_tags {
    tags = {
      Environment = var.environment
      Project     = var.project_name
      ManagedBy   = "Terraform"
    }
  }
}

locals {
  # Keep locals for extra tags ONLY (no duplicates of default_tags)
  extra_tags = {
    # e.g., "CostCenter" = "FM-1234"
  }
}

module "networking" {
  source = "../../modules/networking"

  environment  = var.environment
  project_name = var.project_name

  vpc_cidr     = var.vpc_cidr
  # Let the module create one subnet per AZ using subnet CIDR blocks list
  subnet_cidrs = var.subnet_cidrs   # e.g., ["10.0.1.0/24", "10.0.2.0/24"]
  azs          = var.azs

  tags = local.extra_tags
}

module "security" {
  source = "../../modules/security"

  environment  = var.environment
  project_name = var.project_name
  vpc_id       = module.networking.vpc_id
  vpc_cidr     = var.vpc_cidr

  enable_ssh        = var.enable_ssh
  enable_https      = var.enable_https
  enable_http       = var.enable_http
  ssh_cidr_blocks   = var.ssh_cidr_blocks
  https_cidr_blocks = var.https_cidr_blocks
  http_cidr_blocks  = var.http_cidr_blocks

  # Kubernetes-specific rules
  enable_k8s_api           = var.enable_k8s_api
  enable_k8s_nodeport      = var.enable_k8s_nodeport
  enable_vxlan             = var.enable_vxlan
  k8s_api_cidr_blocks      = var.k8s_api_cidr_blocks
  k8s_nodeport_cidr_blocks = var.k8s_nodeport_cidr_blocks
  vxlan_cidr_blocks        = var.vxlan_cidr_blocks

  tags = local.extra_tags
}

module "compute" {
  source = "../../modules/compute"

  environment  = var.environment
  project_name = var.project_name

  # Define instances with custom names and types
  instances = {
    control-plane = {
      name          = "${var.project_name}-control-plane"
      instance_type = "t3.medium"
      subnet_index  = 0
      role          = "control-plane"
    }
    worker-1 = {
      name          = "${var.project_name}-worker-1"
      instance_type = "t3.large"
      subnet_index  = 0
      role          = "worker"
    }
    worker-2 = {
      name          = "${var.project_name}-worker-2"
      instance_type = "t3.large"
      subnet_index  = 1
      role          = "worker"
    }
  }

  ami                = var.ami
  key_name           = var.key_name
  enable_monitoring  = var.enable_monitoring
  iam_instance_profile = var.iam_instance_profile

  # Pass list of subnets for multi-AZ placement
  subnet_ids         = module.networking.public_subnet_ids
  security_group_ids = [module.security.security_group_id]

  # Volumes
  root_volume_size = var.root_volume_size
  root_volume_type = var.root_volume_type

  # Security and instance settings
  disable_api_termination = var.disable_api_termination
  credit_specification    = var.credit_specification
  associate_public_ip     = var.associate_public_ip
  user_data               = var.user_data

  tags = local.extra_tags
}

