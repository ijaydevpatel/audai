from datetime import datetime
from sqlmodel import Field, SQLModel


class ProcessingJob(SQLModel, table=True):
    id: str = Field(primary_key=True)
    owner_id: int = Field(foreign_key="user.id")
    title: str
    source_object_key: str
    processed_object_key: str | None = None
    stage: str = Field(default="uploaded")
    progress: float = Field(default=0.0)
    message: str = Field(default="Queued")
    detected_languages: list[str] = Field(default_factory=list, sa_column_kwargs={"type_": "JSONB"})
    lufs: float | None = None
    preserve_harmonium: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
