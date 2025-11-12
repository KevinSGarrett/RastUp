locals {
  repo_arn = "arn:aws:ecr:${var.aws_region}:${var.aws_account_id}:repository/${var.ecr_repo_name}"
  repo_url = "${var.aws_account_id}.dkr.ecr.${var.aws_region}.amazonaws.com/${var.ecr_repo_name}"
}

resource "aws_ecr_repository" "repo" {
  name                 = var.ecr_repo_name
  image_tag_mutability = "MUTABLE"
  image_scanning_configuration { scan_on_push = true }
  encryption_configuration     { encryption_type = "AES256" }
  lifecycle { prevent_destroy = false }
}

resource "aws_iam_openid_connect_provider" "github" {
  url = "https://token.actions.githubusercontent.com"
  client_id_list   = ["sts.amazonaws.com"]
  thumbprint_list  = ["6938fd4d98bab03faadb97b34396831e3780aea1"]
}

data "aws_iam_policy_document" "gh_trust" {
  statement {
    sid     = "GitHubOIDCTrust"
    actions = ["sts:AssumeRoleWithWebIdentity"]
    principals {
      type        = "Federated"
      identifiers = [aws_iam_openid_connect_provider.github.arn]
    }
    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }
    condition {
      test     = "StringLike"
      variable = "token.actions.githubusercontent.com:sub"
      values   = [
        "repo:${var.github_org}/${var.github_repo}:ref:refs/heads/*",
        "repo:${var.github_org}/${var.github_repo}:ref:refs/tags/*",
        "repo:${var.github_org}/${var.github_repo}:pull_request"
      ]
    }
  }
}

resource "aws_iam_role" "gh_ecr_push" {
  name               = "${var.app_name}-gh-oidc-ecr"
  assume_role_policy = data.aws_iam_policy_document.gh_trust.json
}

data "aws_iam_policy_document" "ecr_push" {
  statement {
    sid     = "ECRCommon"
    actions = [
      "ecr:GetAuthorizationToken",
      "ecr:BatchCheckLayerAvailability",
      "ecr:CompleteLayerUpload",
      "ecr:GetDownloadUrlForLayer",
      "ecr:InitiateLayerUpload",
      "ecr:PutImage",
      "ecr:UploadLayerPart",
      "ecr:BatchGetImage",
      "ecr:DescribeRepositories",
      "ecr:ListImages"
    ]
    resources = ["*"]
  }
  statement {
    sid       = "ECRRepoScoped"
    actions   = [
      "ecr:BatchDeleteImage",
      "ecr:BatchGetImage",
      "ecr:DescribeImages",
      "ecr:PutImage",
      "ecr:GetRepositoryPolicy",
      "ecr:SetRepositoryPolicy",
      "ecr:DescribeRepositories"
    ]
    resources = [aws_ecr_repository.repo.arn]
  }
}

resource "aws_iam_policy" "ecr_push" {
  name   = "${var.app_name}-ecr-push"
  policy = data.aws_iam_policy_document.ecr_push.json
}

resource "aws_iam_role_policy_attachment" "attach" {
  role       = aws_iam_role.gh_ecr_push.name
  policy_arn = aws_iam_policy.ecr_push.arn
}
