# Fetch current AWS account ID
data "aws_caller_identity" "current" {}

# Output for debugging/reference
output "account_id" {
  value = data.aws_caller_identity.current.account_id
}


# RISK SCENARIO A
# Stranger Danger
resource "aws_iam_role" "risk_stranger" {
  name = "target-${var.environment}-risk-stranger"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${var.external_account_id}:root"
        }
      }
    ]
  })

  tags = merge(
    var.common_tags,
    { Name = "Stranger Account Role" }
  )
}

# RISK SCENARIO B
# Confused Deputy (NO ExternalId)
resource "aws_iam_role" "risk_no_external_id" {
  name = "target-${var.environment}-risk-deputy"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${var.vendor_account_id}:root"
        }
        # Condition intentionally missing
      }
    ]
  })

  tags = merge(
    var.common_tags,
    { Name = "Confused Deputy Role" }
  )
}

# SAFE SCENARIO
# ExternalId protected
resource "aws_iam_role" "safe_vendor" {
  name = "target-${var.environment}-safe-vendor"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${var.vendor_account_id}:root"
        }
        Condition = {
          StringEquals = {
            "sts:ExternalId" = var.external_id
          }
        }
      }
    ]
  })

  tags = merge(
    var.common_tags,
    { Name = "Safe Vendor Role" }
  )
}
