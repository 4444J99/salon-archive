"""Transcription module for processing salon audio recordings.

Provides a pipeline for converting audio recordings into structured
text transcripts with speaker diarization and segment metadata.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import timedelta
from enum import Enum
from typing import Any


class TranscriptionStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Segment:
    """A time-aligned segment of transcribed speech."""
    speaker: str
    text: str
    start_time: timedelta
    end_time: timedelta
    confidence: float = 0.0

    @property
    def duration(self) -> timedelta:
        return self.end_time - self.start_time

    def to_dict(self) -> dict[str, Any]:
        return {
            "speaker": self.speaker,
            "text": self.text,
            "start_seconds": self.start_time.total_seconds(),
            "end_seconds": self.end_time.total_seconds(),
            "confidence": self.confidence,
        }


@dataclass
class TranscriptionResult:
    """Complete transcription output for a salon session."""
    session_id: str
    segments: list[Segment] = field(default_factory=list)
    status: TranscriptionStatus = TranscriptionStatus.PENDING
    language: str = "en"

    @property
    def full_text(self) -> str:
        return " ".join(seg.text for seg in self.segments)

    @property
    def speaker_list(self) -> list[str]:
        return list(dict.fromkeys(seg.speaker for seg in self.segments))

    @property
    def total_duration(self) -> timedelta:
        if not self.segments:
            return timedelta(0)
        return max(seg.end_time for seg in self.segments)


# ── Backends ──────────────────────────────────────────────────────────


class TranscriptionBackend(ABC):
    """Abstract base for transcription backends."""

    @abstractmethod
    def transcribe(self, audio_path: str) -> list[Segment]:
        """Convert an audio file to a list of time-aligned segments."""
        ...


class MockBackend(TranscriptionBackend):
    """Returns deterministic mock segments for testing and development."""

    def transcribe(self, audio_path: str) -> list[Segment]:
        speakers = ["Speaker 1", "Speaker 2"]
        segments: list[Segment] = []
        offset = 0
        for i in range(6):
            speaker = speakers[i % len(speakers)]
            duration = 15 + (i * 5)  # varying segment lengths
            segments.append(Segment(
                speaker=speaker,
                text=f"Segment {i+1} from {speaker} discussing {audio_path}",
                start_time=timedelta(seconds=offset),
                end_time=timedelta(seconds=offset + duration),
                confidence=0.90 + (i % 3) * 0.03,
            ))
            offset += duration
        return segments


class WhisperBackend(TranscriptionBackend):
    """Placeholder for OpenAI Whisper API integration."""

    def transcribe(self, audio_path: str) -> list[Segment]:
        raise NotImplementedError("Whisper integration not yet configured")


# ── Pipeline ──────────────────────────────────────────────────────────


class TranscriptionPipeline:
    """Pipeline for processing audio into structured transcripts."""

    def __init__(
        self,
        language: str = "en",
        backend: TranscriptionBackend | None = None,
    ) -> None:
        self.language = language
        self.backend = backend or MockBackend()
        self._results: dict[str, TranscriptionResult] = {}

    def process_audio(self, session_id: str, audio_path: str) -> TranscriptionResult:
        """Process an audio file and generate a transcription.

        Args:
            session_id: Unique identifier for the salon session.
            audio_path: Path to the audio file.

        Returns:
            TranscriptionResult with segments from the configured backend.
        """
        result = TranscriptionResult(
            session_id=session_id,
            status=TranscriptionStatus.PROCESSING,
            language=self.language,
        )
        try:
            result.segments = self.backend.transcribe(audio_path)
        except Exception:
            self._results[session_id] = TranscriptionResult(
                session_id=session_id,
                status=TranscriptionStatus.FAILED,
                language=self.language,
            )
            raise
        result.status = TranscriptionStatus.COMPLETED
        self._results[session_id] = result
        return result

    def get_result(self, session_id: str) -> TranscriptionResult | None:
        return self._results.get(session_id)

    def extract_segments(self, result: TranscriptionResult, speaker: str | None = None) -> list[Segment]:
        """Extract segments, optionally filtered by speaker."""
        if speaker:
            return [s for s in result.segments if s.speaker == speaker]
        return list(result.segments)
