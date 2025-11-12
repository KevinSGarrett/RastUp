# ECR + GitHub OIDC (One-time Bootstrap)

## Prereqs
- AWS CLI configured with admin (temporary) or infra role
- Terraform >= 1.5 installed locally
- Values:
  - `AWS_ACCOUNT_ID` = **<your account id>**
  - `AWS_REGION`     = **<your region, e.g., us-east-1>**
  - `APP_NAME`       = **rastup** (example)
  - `ECR_REPO_NAME`  = **rastup-dev**
  - `GITHUB_ORG`     = **KevinSGarrett**
  - `GITHUB_REPO`    = **RastUp**

## Apply (local)
```powershell
cd C:\RastUp\RastUp\infra
terraform init
terraform apply -auto-approve `
  -var "aws_account_id=AWS_ACCOUNT_ID" `
  -var "aws_region=AWS_REGION" `
  -var "app_name=APP_NAME" `
  -var "ecr_repo_name=ECR_REPO_NAME" `
  -var "github_org=GITHUB_ORG" `
  -var "github_repo=GITHUB_REPO"
