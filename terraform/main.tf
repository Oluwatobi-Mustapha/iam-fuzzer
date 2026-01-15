provider "aws" {
  region = "us-east-1"
}
data "aws_caller_identity" "current" {}

output "account_id" {
  value = data.aws_caller_identity.current.account_id
}

resource "aws_iam_role" "risk_stranger" {
  name = "target-prod-risk-stranger"

  # Terraform's "jsonencode" function converts a
  # Terraform expression format to valid JSON syntax.
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
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


# The Confused Deputy Role (Scenario B)
# RISK: Trusts a Vendor (simulated by your own account) but MISSING the ExternalID check
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
        # Note: The "Condition" block is MISSING!
        # This is what makes it vulnerable.
      }
    ]
  })

  tags = {
    Name = "Confused Deputy Role"
    Env  = "Test"
  }
}

# The safe vendor
resource "aws_iam_role" "safe_vendor" {
  name = "target-prod-safe-vendor"

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
        Condition = {
          StringEquals = {
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
