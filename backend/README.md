# Audai Backend

FastAPI + Celery backend powering the harmonium-aware enhancement pipeline.

## Getting Started
1. Install dependencies: `poetry install`
2. Create `.env` with credentials:
   ```env
   AUDAI_S3_BUCKET=your-bucket
   AUDAI_S3_REGION=ap-south-1
   AUDAI_DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/audai
   AUDAI_REDIS_URL=redis://localhost:6379/0
   GPT_OSS_ENDPOINT=https://gpt-oss.example.com/v1/segment
   GPT_OSS_API_KEY=sk-...
   HF_TOKEN=hf_...
   AUDAI_JWT_SECRET=super-secret
   ```
3. Initialize the database: `poetry run python -m backend.app.api.deps`
4. Start services:
   - API: `poetry run uvicorn backend.app.main:app --reload`
   - Worker: `poetry run celery -A backend.app.workers.celery_app.celery_app worker -l info`

## Pipeline Overview
- `workers.tasks.process_audio` orchestrates the async processing lifecycle.
- `services.pipeline.HarmoniumAwarePipeline` runs Whisper segmentation, GPT-OSS-120B classification, Hugging Face denoisers, and LUFS normalization.
- `services.storage` provides S3-backed signed URL uploads and artifact publishing.

## API Surface
- `POST /api/v1/auth/signup` – create account, returns JWT tokens.
- `POST /api/v1/auth/login` – login via password grant.
- `POST /api/v1/files/sign-upload` – issue signed S3 upload URLs.
- `POST /api/v1/jobs` – enqueue processing job.
- `GET /api/v1/jobs` – list user history.
- `GET /api/v1/jobs/{id}` – poll processing status.
