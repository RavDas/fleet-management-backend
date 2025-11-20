# Data source for latest Ubuntu AMI (if not provided)
data "aws_ami" "ubuntu" {
  count       = var.ami != "" ? 0 : 1
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# EC2 Instances with flexible configuration
resource "aws_instance" "compute" {
  for_each = var.instances

  ami                     = var.ami != "" ? var.ami : data.aws_ami.ubuntu[0].id
  instance_type           = each.value.instance_type
  subnet_id               = length(var.subnet_ids) > 0 ? var.subnet_ids[each.value.subnet_index] : var.subnet_id
  vpc_security_group_ids  = var.security_group_ids
  monitoring              = var.enable_monitoring
  key_name                = var.key_name
  iam_instance_profile    = var.iam_instance_profile
  disable_api_termination = var.disable_api_termination
  user_data               = var.user_data
  
  # Public IP association
  associate_public_ip_address = var.associate_public_ip

  # IMDSv2 enforcement
  metadata_options {
    http_endpoint = "enabled"
    http_tokens   = "required"
  }

  # T3 credit specification
  credit_specification {
    cpu_credits = var.credit_specification
  }

  root_block_device {
    volume_type           = var.root_volume_type
    volume_size           = var.root_volume_size
    delete_on_termination = true
    encrypted             = true
  }

  tags = merge(
    var.tags,
    {
      Name = each.value.name
      Role = each.value.role
    }
  )
}
