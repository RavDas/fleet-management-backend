# Getting Started with Fleet Management Terraform

## Quick Reference

### 1. Prerequisites Check

```bash
# Verify Terraform installation
terraform version

# Verify AWS CLI installation
aws --version

# Configure AWS credentials
aws configure
```

### 2. First-Time Setup

```bash
# Navigate to environment
cd environments/dev

# Copy variables file
cp terraform.tfvars.example terraform.tfvars

# Initialize Terraform
terraform init
```

### 3. Common Workflows

#### Planning Changes

```bash
terraform plan
```

#### Applying Infrastructure

```bash
terraform apply
```

#### Viewing Current State

```bash
terraform show
terraform output
```

#### Destroying Infrastructure

```bash
terraform destroy
```

## Using the Deployment Script

Make scripts executable:

```bash
chmod +x deploy.sh cleanup.sh
```

### Deploy to Development

```bash
./deploy.sh -e dev -a init
./deploy.sh -e dev -a plan
./deploy.sh -e dev -a apply
```

### View Outputs

```bash
./deploy.sh -e dev -a output
```

### Destroy Infrastructure

```bash
./deploy.sh -e dev -a destroy
```

## File Organization

### Modules

Each module handles a specific infrastructure component:

**networking/**
- Creates VPC and networking infrastructure
- Reusable across environments

**security/**
- Manages security groups
- Configurable ingress/egress rules

**compute/**
- Launches EC2 instances
- Handles sizing and configuration

### Environments

Each environment is isolated with:

**dev/** - Development environment
- Lower cost instances
- Minimal monitoring
- Quick iteration

**staging/** - Staging environment
- Production-like setup
- Monitoring enabled
- Pre-deployment validation

**prod/** - Production environment
- Maximum resources
- Enhanced monitoring
- Critical workloads

## Variable Configuration

### Understanding Variables

1. **Default Variables** (`variables.tf`)
   - Type definitions
   - Default values
   - Descriptions

2. **Override Values** (`terraform.tfvars`)
   - Environment-specific values
   - Sensitive data (not committed)
   - Custom configurations

### Customizing Deployment

Edit `terraform.tfvars` for your environment:

```hcl
# Change instance count
instance_count = 5

# Change instance type
instance_type = "t3.small"

# Restrict SSH access (security best practice)
ssh_cidr_blocks = ["YOUR_IP/32"]

# Enable HTTP
enable_http = true
```

## State Management

### Local State

Default: State stored in `terraform.tfstate` (in environment directory)

### Remote State Setup

For team environments or production:

#### Step 1: Create S3 Bucket

```bash
aws s3api create-bucket \
  --bucket fleet-management-tfstate \
  --region us-east-1

aws s3api put-bucket-versioning \
  --bucket fleet-management-tfstate \
  --versioning-configuration Status=Enabled
```

#### Step 2: Create DynamoDB Table

```bash
aws dynamodb create-table \
  --table-name terraform-locks \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
```

#### Step 3: Configure Backend

Uncomment in `environments/[env]/main.tf`:

```hcl
terraform {
  backend "s3" {
    bucket         = "fleet-management-tfstate"
    key            = "fleet-management/dev/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

Then reinitialize:

```bash
terraform init
```

## Troubleshooting

### Error: "Unauthorized"

```bash
# Check AWS credentials
aws sts get-caller-identity

# Reconfigure AWS
aws configure
```

### Error: "No available instances"

Instance type not available in region. Options:
- Change region in `terraform.tfvars`
- Change instance type
- Check AWS service status

### Error: "VPC quota exceeded"

Account limits reached. Options:
- Destroy unused infrastructure
- Request AWS quota increase
- Use different region

### State Lock Issues

```bash
# Force unlock (use carefully)
terraform force-unlock LOCK_ID
```

## Best Practices

### Before Deploying

1. ✅ Review `terraform plan` output
2. ✅ Verify AWS region
3. ✅ Check variable values
4. ✅ Validate security group rules

### During Deployment

1. ✅ Monitor `terraform apply` output
2. ✅ Check for errors
3. ✅ Verify AWS console for resources

### After Deployment

1. ✅ Test instance connectivity
2. ✅ Verify security group rules
3. ✅ Check CloudWatch metrics
4. ✅ Document any manual changes

### Source Control

```bash
# Do NOT commit these files
terraform.tfstate
terraform.tfstate.backup
.terraform/
terraform.tfvars

# Do commit these files
*.tf (all Terraform files)
terraform.tfvars.example
README.md
ARCHITECTURE.md
```

## Common Tasks

### Scale Up Instances

```hcl
# Edit terraform.tfvars
instance_count = 5  # Increase from 3

# Apply changes
terraform apply
```

### Change Instance Type

```hcl
# Edit terraform.tfvars
instance_type = "t3.small"  # Upgrade from t3.micro

# Apply changes
terraform apply
```

### Enable Monitoring

```hcl
# Edit terraform.tfvars
enable_monitoring = true

# Apply changes
terraform apply
```

### Restrict SSH Access

```hcl
# Edit terraform.tfvars - Change from anywhere to specific IP
ssh_cidr_blocks = ["203.0.113.0/32"]

# Apply changes
terraform apply
```

## Getting Help

### Resources

- [Terraform Docs](https://www.terraform.io/docs)
- [AWS Terraform Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [AWS Documentation](https://docs.aws.amazon.com/)

### Debugging

Enable debug output:

```bash
export TF_LOG=DEBUG
terraform apply
```

Check logs:

```bash
terraform show
```

Inspect state:

```bash
terraform state list
terraform state show 'aws_instance.compute[0]'
```

## Next Steps

1. Review `ARCHITECTURE.md` for infrastructure design
2. Customize variables in `terraform.tfvars`
3. Test in development environment first
4. Plan production deployment carefully
5. Set up remote state for team environments
6. Implement monitoring and alerting
7. Plan for disaster recovery

## FAQ

**Q: How many environments should I use?**
A: Recommended: dev, staging, prod. Add more as needed.

**Q: Can I use the same Terraform files for multiple regions?**
A: Yes, change `aws_region` in `terraform.tfvars`

**Q: How do I backup infrastructure?**
A: Enable remote state in S3, use EBS snapshots, maintain AMIs.

**Q: What if I make manual changes in AWS?**
A: Use `terraform refresh` to sync state, then use `terraform apply` to restore desired state.

**Q: How do I migrate from local to remote state?**
A: Configure backend in `main.tf`, then run `terraform init` and choose to migrate state.
