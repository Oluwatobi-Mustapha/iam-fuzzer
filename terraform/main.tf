
provider "aws" {
  region = "us-east-1"
}
# Fetch current AWS account ID
data "aws_caller_identity" "current" {}

# Expose account ID for debugging and reference
output "account_id" {
  value = data.aws_caller_identity.current.account_id
}

# RISK SCENARIO A:
# Trusts an external AWS account root user directly
resource "aws_iam_role" "risk_stranger" {
  name = "target-prod-risk-stranger"
  # Allows account 220065406396 to assume this role.
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      { 
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          "AWS" = "arn:aws:iam::220065406396:root"
        }
      },
    ]
  })

  tags = {
    Name = "Strange Account"
    Env = "Test"
  }
}

# RISK SCENARIO B (Confused Deputy):
# Vendor role WITHOUT ExternalId condition
resource "aws_iam_role" "risk_no_external_id" {
  name = "target-prod-risk-deputy"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          # I use my own account ID so Terraform doesn't crash.
          # In a real attack, this would be the Vendor's ID.
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        }
        # You will notice the "Condition" block is MISSING! and that makes it vuln.
      }
    ]
  })

  tags = {
    Name = "Confused Deputy Role"
    Env  = "Test"
  }
}

# SAFE SCENARIO:
# Vendor role protected with ExternalId
resource "aws_iam_role" "safe_vendor" {
  name = "target-prod-safe-vendor"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        }
        Condition = {
          StringEquals = {
            # Prevents confused deputy attacks
            "sts:ExternalId" = "MySecretPass123"
          }
        }
      }
    ]
  })

  tags = {
    Name = "Safe-Vendor"
    Env  = "Test"
  }
}
