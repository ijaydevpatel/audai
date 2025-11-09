from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx

from ..core.config import settings


@dataclass
class SegmentAnnotation:
    start: float
    end: float
    label: str
    confidence: float


class GPTOrchestrator:
    def __init__(self, *, client: httpx.AsyncClient | None = None) -> None:
        self._client = client or httpx.AsyncClient(timeout=60.0)

    async def annotate(self, transcript: list[dict[str, Any]]) -> list[SegmentAnnotation]:
        payload = {
            "task": "segment_classification",
            "prompt": "classify segments into speech, harmonium, singing, secondary_voice, noise",
            "transcript": transcript,
        }
        headers = {"Authorization": f"Bearer {settings.gpt_oss_api_key}"}
        response = await self._client.post(settings.gpt_oss_endpoint, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return [SegmentAnnotation(**segment) for segment in data["segments"]]


async def classify_segments(transcript: list[dict[str, Any]]) -> list[SegmentAnnotation]:
    orchestrator = GPTOrchestrator()
    return await orchestrator.annotate(transcript)
