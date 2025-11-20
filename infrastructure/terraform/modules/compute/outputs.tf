output "instance_ids" {
  description = "IDs of the EC2 instances"
  value       = { for k, v in aws_instance.compute : k => v.id }
}

output "instance_public_ips" {
  description = "Public IP addresses of the EC2 instances"
  value       = { for k, v in aws_instance.compute : k => v.public_ip }
}

output "instance_private_ips" {
  description = "Private IP addresses of the EC2 instances"
  value       = { for k, v in aws_instance.compute : k => v.private_ip }
}

output "instance_dns_names" {
  description = "DNS names of the EC2 instances"
  value       = { for k, v in aws_instance.compute : k => v.public_dns }
}
