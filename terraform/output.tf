output "risk_stranger_role_arn" {
  description = "ARN of the role with wildcard/external trust (Stranger Danger)"
  value       = aws_iam_role.risk_stranger.arn
}

output "risk_no_external_id_role_arn" {
  description = "ARN of the Confused Deputy vulnerable role"
  value       = aws_iam_role.risk_no_external_id.arn
}

output "safe_vendor_role_arn" {
  description = "ARN of the properly protected vendor role"
  value       = aws_iam_role.safe_vendor.arn
}

output "current_account_id" {
  description = "AWS account ID used for deployment"
  value       = data.aws_caller_identity.current.account_id
}
