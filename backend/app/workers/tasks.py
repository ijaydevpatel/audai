from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any

from celery import shared_task
from sqlmodel import Session

from ..api.deps import engine
from ..models.job import ProcessingJob
from ..services.pipeline import run_pipeline
from ..services.storage import storage_client


@shared_task(bind=True)
def process_audio(self: Any, job_id: str) -> None:
    with Session(engine) as session:
        job = session.get(ProcessingJob, job_id)
        if job is None:
            self.update_state(state="FAILURE", meta={"message": "Job missing"})
            return

        temp_dir = Path(f"/tmp/audai/{job_id}")
        temp_dir.mkdir(parents=True, exist_ok=True)
        source_path = temp_dir / "source.wav"
        # download from S3 (omitted for brevity)

        async def _run() -> None:
            result = await run_pipeline(source_path, temp_dir, job.preserve_harmonium)
            job.processed_object_key = f"processed/{job.id}.wav"
            job.stage = "delivered"
            job.progress = 1.0
            job.message = "Completed"
            job.detected_languages = result.detected_languages
            job.lufs = result.lufs

        asyncio.run(_run())
        session.add(job)
        session.commit()
