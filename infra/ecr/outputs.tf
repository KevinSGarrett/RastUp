output "ecr_repository_url"   { value = aws_ecr_repository.repo.repository_url }
output "github_oidc_role_arn" { value = aws_iam_role.gh_ecr_push.arn }
