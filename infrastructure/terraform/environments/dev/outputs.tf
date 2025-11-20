# These match the references you used in main.tf

output "vpc_id" {
  description = "ID of the VPC created by the networking module."
  value       = module.networking.vpc_id
}

output "public_subnet_ids" {
  description = "IDs of public subnets created by the networking module."
  value       = module.networking.public_subnet_ids
}

output "instance_ids" {
  description = "IDs of EC2 instances created by the compute module."
  value       = module.compute.instance_ids
}
