## Prerequisites
- Terraform >= 1.5
- AWS credentials configured (aws configure or profile)

## Setup
git clone (my repo code)
```bash
cd iam-fuzzer
```
```bash
cp terraform.tfvars.example terraform.tfvars
```

## Run
```bash
terraform init -upgrade
```
```bash
terraform apply -auto-approve
```

## Cleanup
```bash
terraform destroy -auto-approve
```
**Note: _This project creates intentionally vulnerable IAM roles. Only run this in a test or sandbox AWS account_**