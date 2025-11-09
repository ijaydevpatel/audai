from __future__ import annotations

import asyncio
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import librosa
import numpy as np
import soundfile as sf

from ..core.config import settings
from .orchestrator import SegmentAnnotation, classify_segments


@dataclass
class EnhancementResult:
    output_path: Path
    detected_languages: list[str]
    lufs: float


class HarmoniumAwarePipeline:
    def __init__(self, *, workdir: Path) -> None:
        self.workdir = workdir
        self.workdir.mkdir(parents=True, exist_ok=True)

    async def process(self, source_path: Path, preserve_harmonium: bool = True) -> EnhancementResult:
        waveform, sr = librosa.load(source_path, sr=None, mono=False)
        transcript = await self._run_whisper(source_path)
        annotations = await classify_segments(transcript)

        cleaned = await self._apply_segment_processing(waveform, sr, annotations, preserve_harmonium)
        cleaned = self._apply_lufs_normalization(cleaned, sr)
        output_path = self.workdir / "enhanced.wav"
        sf.write(output_path, cleaned.T, sr)

        languages = sorted({chunk.get("language", "unknown") for chunk in transcript})
        lufs_value = self._measure_lufs(cleaned, sr)
        return EnhancementResult(output_path=output_path, detected_languages=languages, lufs=lufs_value)

    async def _run_whisper(self, source_path: Path) -> list[dict[str, Any]]:
        await asyncio.sleep(0)  # placeholder for actual async call
        return [
            {"start": 0.0, "end": 5.0, "text": "Intro music", "language": "gu"},
            {"start": 5.0, "end": 60.0, "text": "Discourse", "language": "hi"},
        ]

    async def _apply_segment_processing(
        self,
        waveform: np.ndarray,
        sr: int,
        annotations: list[SegmentAnnotation],
        preserve_harmonium: bool,
    ) -> np.ndarray:
        cleaned = np.copy(waveform)
        for segment in annotations:
            start_idx = int(segment.start * sr)
            end_idx = int(segment.end * sr)
            segment_audio = cleaned[..., start_idx:end_idx]

            if segment.label in {"noise", "secondary_voice"}:
                cleaned[..., start_idx:end_idx] = self._attenuate_noise(segment_audio)
            elif segment.label in {"speech", "discourse"}:
                cleaned[..., start_idx:end_idx] = self._enhance_voice(segment_audio)
            elif segment.label in {"harmonium", "singing"} and preserve_harmonium:
                cleaned[..., start_idx:end_idx] = self._enhance_harmonium(segment_audio)

        return cleaned

    def _attenuate_noise(self, segment_audio: np.ndarray) -> np.ndarray:
        return segment_audio * 0.1

    def _enhance_voice(self, segment_audio: np.ndarray) -> np.ndarray:
        return segment_audio * 1.2

    def _enhance_harmonium(self, segment_audio: np.ndarray) -> np.ndarray:
        return segment_audio * 1.1

    def _apply_lufs_normalization(self, waveform: np.ndarray, sr: int) -> np.ndarray:
        rms = np.sqrt(np.mean(waveform**2))
        target_rms = 0.1
        if rms == 0:
            return waveform
        gain = target_rms / rms
        return waveform * gain

    def _measure_lufs(self, waveform: np.ndarray, sr: int) -> float:
        rms = np.sqrt(np.mean(waveform**2))
        return -0.691 + 10 * np.log10(rms + 1e-9)


async def run_pipeline(source_path: Path, output_dir: Path, preserve_harmonium: bool) -> EnhancementResult:
    pipeline = HarmoniumAwarePipeline(workdir=output_dir)
    return await pipeline.process(source_path, preserve_harmonium=preserve_harmonium)
