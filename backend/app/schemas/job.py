from datetime import datetime
from pydantic import BaseModel


class JobCreate(BaseModel):
    title: str
    sourceObjectKey: str
    preserveHarmonium: bool = True


class JobRead(BaseModel):
    id: str
    title: str
    stage: str
    progress: float
    message: str
    detectedLanguages: list[str]
    lufs: float | None
    preserveHarmonium: bool
    downloadUrl: str | None
    createdAt: datetime
    updatedAt: datetime


class JobStatus(BaseModel):
    id: str
    stage: str
    progress: float
    message: str
    updatedAt: datetime
