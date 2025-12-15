# Security Group
resource "aws_security_group" "main" {
  name_prefix = "${var.project_name}-${var.environment}-sg"
  description = "Security group for ${var.project_name} ${var.environment}"
  vpc_id      = var.vpc_id

  tags = merge(
    var.tags,
    {
      Name = "${var.project_name}-${var.environment}-sg"
    }
  )
}

# Ingress Rule - SSH (Port 22)
resource "aws_vpc_security_group_ingress_rule" "ssh" {
  count             = var.enable_ssh ? 1 : 0
  security_group_id = aws_security_group.main.id

  description = "Allow SSH access"
  from_port   = 22
  to_port     = 22
  ip_protocol = "tcp"
  cidr_ipv4   = var.ssh_cidr_blocks[0]

  tags = merge(
    var.tags,
    {
      Name = "ssh-ingress"
    }
  )
}

# Ingress Rule - HTTPS (Port 443)
resource "aws_vpc_security_group_ingress_rule" "https" {
  count             = var.enable_https ? 1 : 0
  security_group_id = aws_security_group.main.id

  description = "Allow HTTPS access"
  from_port   = 443
  to_port     = 443
  ip_protocol = "tcp"
  cidr_ipv4   = var.https_cidr_blocks[0]

  tags = merge(
    var.tags,
    {
      Name = "https-ingress"
    }
  )
}

# Ingress Rule - HTTP (Port 80)
resource "aws_vpc_security_group_ingress_rule" "http" {
  count             = var.enable_http ? 1 : 0
  security_group_id = aws_security_group.main.id

  description = "Allow HTTP access"
  from_port   = 80
  to_port     = 80
  ip_protocol = "tcp"
  cidr_ipv4   = var.http_cidr_blocks[0]

  tags = merge(
    var.tags,
    {
      Name = "http-ingress"
    }
  )
}

# Ingress Rule - Kubernetes API Server (Port 6443)
resource "aws_vpc_security_group_ingress_rule" "k8s_api" {
  count             = var.enable_k8s_api ? 1 : 0
  security_group_id = aws_security_group.main.id

  description = "Allow Kubernetes API Server access"
  from_port   = 6443
  to_port     = 6443
  ip_protocol = "tcp"
  cidr_ipv4   = var.k8s_api_cidr_blocks[0]

  tags = merge(
    var.tags,
    {
      Name = "k8s-api-ingress"
    }
  )
}

# Ingress Rule - Kubernetes NodePort Services (Port 6000-10250)
resource "aws_vpc_security_group_ingress_rule" "k8s_nodeport" {
  count             = var.enable_k8s_nodeport ? 1 : 0
  security_group_id = aws_security_group.main.id

  description = "Allow Kubernetes NodePort and kubelet API access"
  from_port   = 6000
  to_port     = 10250
  ip_protocol = "tcp"
  cidr_ipv4   = var.k8s_nodeport_cidr_blocks[0]

  tags = merge(
    var.tags,
    {
      Name = "k8s-nodeport-ingress"
    }
  )
}

# Ingress Rule - VXLAN for CNI (Port 8472 UDP)
resource "aws_vpc_security_group_ingress_rule" "vxlan" {
  count             = var.enable_vxlan ? 1 : 0
  security_group_id = aws_security_group.main.id

  description = "Allow VXLAN overlay network for CNI (Flannel/Calico)"
  from_port   = 8472
  to_port     = 8472
  ip_protocol = "udp"
  cidr_ipv4   = var.vxlan_cidr_blocks[0]

  tags = merge(
    var.tags,
    {
      Name = "vxlan-ingress"
    }
  )
}

# Ingress Rule - Allow all traffic from VPC (for K8s cluster communication)
resource "aws_vpc_security_group_ingress_rule" "internal" {
  security_group_id = aws_security_group.main.id

  description = "Allow all internal VPC traffic for K8s cluster"
  from_port   = 0
  to_port     = 0
  ip_protocol = "-1"
  cidr_ipv4   = var.vpc_cidr

  tags = merge(
    var.tags,
    {
      Name = "internal-vpc-ingress"
    }
  )
}

# Egress Rule - Allow all outbound traffic
resource "aws_vpc_security_group_egress_rule" "allow_all" {
  security_group_id = aws_security_group.main.id

  description = "Allow all outbound traffic"
  from_port   = 0
  to_port     = 0
  ip_protocol = "-1"
  cidr_ipv4   = "0.0.0.0/0"

  tags = merge(
    var.tags,
    {
      Name = "allow-all-egress"
    }
  )
}
