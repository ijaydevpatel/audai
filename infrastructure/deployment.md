# Deployment Guide

## Prerequisites
- AWS account with permissions for S3, ECS, RDS, and IAM.
- Terraform >= 1.5 installed locally.
- Docker registry (ECR or GHCR) for container images.

## Steps
1. **Bootstrap Infrastructure**
   - Copy `terraform/` and populate variables for VPC, subnets, S3 bucket, Redis/ElastiCache, and RDS PostgreSQL.
   - Run `terraform init && terraform apply`.
2. **Build & Push Images**
   - Frontend: `cd frontend && npm install && npm run build && docker build -t <registry>/audai-frontend .`
   - Backend: `cd backend && poetry export -f requirements.txt --output requirements.lock && docker build -t <registry>/audai-backend .`
   - Push both images to the registry.
3. **Configure Secrets**
   - Store JWT secret, GPT-OSS keys, Hugging Face token, and database credentials in AWS Secrets Manager.
4. **Deploy Services**
   - ECS Service 1: FastAPI API on Fargate with ALB.
   - ECS Service 2: Celery worker (with queue autoscaling based on pending tasks).
   - Schedule Whisper/GPT-OSS cache warmers via AWS Lambda if desired.
5. **Frontend Hosting**
   - Deploy Next.js static export to S3 + CloudFront or to Vercel with env vars pointing to the API.
6. **Monitoring**
   - Enable CloudWatch dashboards for queue depth, worker success rate, and LUFS distribution metrics.
   - Configure alerts on failed jobs and S3 storage thresholds.

## Local Development
- Use `docker-compose` with MinIO, Postgres, and Redis for local parity.
- Configure `NEXT_PUBLIC_API_BASE=http://localhost:8000` when running the frontend dev server.
