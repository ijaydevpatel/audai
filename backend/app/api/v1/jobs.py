from __future__ import annotations

import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ...models.job import ProcessingJob
from ...schemas.job import JobCreate, JobRead, JobStatus
from ..deps import get_current_user, get_session
from ...workers.tasks import process_audio

router = APIRouter()


@router.post("", response_model=JobStatus)
def create_job(
    payload: JobCreate,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
) -> JobStatus:
    job_id = uuid.uuid4().hex
    job = ProcessingJob(
        id=job_id,
        owner_id=current_user.id,
        title=payload.title,
        source_object_key=payload.sourceObjectKey,
        preserve_harmonium=payload.preserveHarmonium,
        stage="uploaded",
        progress=0.1,
        message="Queued",
    )
    session.add(job)
    session.commit()

    process_audio.delay(job_id)

    return JobStatus(
        id=job.id,
        stage=job.stage,
        progress=job.progress,
        message=job.message,
        updatedAt=datetime.utcnow(),
    )


@router.get("", response_model=list[JobRead])
def list_jobs(session: Session = Depends(get_session), current_user=Depends(get_current_user)) -> list[JobRead]:
    jobs = session.exec(select(ProcessingJob).where(ProcessingJob.owner_id == current_user.id)).all()
    return [
        JobRead(
            id=job.id,
            title=job.title,
            stage=job.stage,
            progress=job.progress,
            message=job.message,
            detectedLanguages=job.detected_languages,
            lufs=job.lufs,
            preserveHarmonium=job.preserve_harmonium,
            downloadUrl=f"/api/v1/files/{job.id}/download" if job.processed_object_key else None,
            createdAt=job.created_at,
            updatedAt=job.updated_at,
        )
        for job in jobs
    ]


@router.get("/{job_id}", response_model=JobStatus)
def get_job(job_id: str, session: Session = Depends(get_session), current_user=Depends(get_current_user)) -> JobStatus:
    job = session.get(ProcessingJob, job_id)
    if job is None or job.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Job not found")

    return JobStatus(
        id=job.id,
        stage=job.stage,
        progress=job.progress,
        message=job.message,
        updatedAt=job.updated_at,
    )
