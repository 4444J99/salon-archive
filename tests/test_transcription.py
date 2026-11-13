"""Tests for the transcription module."""
from datetime import timedelta

import pytest

from src.transcription import (
    MockBackend,
    Segment,
    TranscriptionBackend,
    TranscriptionPipeline,
    TranscriptionStatus,
    WhisperBackend,
)


def test_pipeline_processes_audio():
    pipeline = TranscriptionPipeline()
    result = pipeline.process_audio("S001", "/audio/session1.wav")
    assert result.status == TranscriptionStatus.COMPLETED
    assert len(result.segments) > 0

def test_pipeline_stores_result():
    pipeline = TranscriptionPipeline()
    pipeline.process_audio("S001", "/audio/session1.wav")
    assert pipeline.get_result("S001") is not None
    assert pipeline.get_result("MISSING") is None

def test_segment_duration():
    seg = Segment(speaker="A", text="Hello", start_time=timedelta(seconds=10), end_time=timedelta(seconds=25))
    assert seg.duration == timedelta(seconds=15)

def test_result_full_text():
    pipeline = TranscriptionPipeline()
    result = pipeline.process_audio("S001", "/audio/test.wav")
    assert len(result.full_text) > 0

def test_extract_segments_by_speaker():
    pipeline = TranscriptionPipeline()
    result = pipeline.process_audio("S001", "/audio/test.wav")
    segs = pipeline.extract_segments(result, "Speaker 1")
    assert len(segs) >= 1


def test_multi_segment_generation():
    pipeline = TranscriptionPipeline()
    result = pipeline.process_audio("S001", "/audio/session.wav")
    assert len(result.segments) >= 2


def test_multiple_speakers():
    pipeline = TranscriptionPipeline()
    result = pipeline.process_audio("S001", "/audio/session.wav")
    speakers = result.speaker_list
    assert len(speakers) >= 2


def test_total_duration():
    pipeline = TranscriptionPipeline()
    result = pipeline.process_audio("S001", "/audio/session.wav")
    assert result.total_duration.total_seconds() > 0


# --- Backend tests ---


class TestMockBackend:
    def test_is_transcription_backend(self):
        assert isinstance(MockBackend(), TranscriptionBackend)

    def test_returns_segments(self):
        backend = MockBackend()
        segments = backend.transcribe("/audio/test.wav")
        assert len(segments) == 6

    def test_segments_have_speakers(self):
        backend = MockBackend()
        segments = backend.transcribe("/audio/test.wav")
        speakers = {s.speaker for s in segments}
        assert "Speaker 1" in speakers
        assert "Speaker 2" in speakers

    def test_segments_are_ordered(self):
        backend = MockBackend()
        segments = backend.transcribe("/audio/test.wav")
        for i in range(1, len(segments)):
            assert segments[i].start_time >= segments[i - 1].start_time

    def test_segment_text_contains_path(self):
        backend = MockBackend()
        segments = backend.transcribe("/audio/my_recording.wav")
        assert any("my_recording" in s.text for s in segments)


class TestWhisperBackend:
    def test_is_transcription_backend(self):
        assert isinstance(WhisperBackend(), TranscriptionBackend)

    def test_raises_not_implemented(self):
        backend = WhisperBackend()
        with pytest.raises(NotImplementedError, match="Whisper integration"):
            backend.transcribe("/audio/test.wav")


class TestPipelineWithBackend:
    def test_default_backend_is_mock(self):
        pipeline = TranscriptionPipeline()
        assert isinstance(pipeline.backend, MockBackend)

    def test_accepts_custom_backend(self):
        backend = MockBackend()
        pipeline = TranscriptionPipeline(backend=backend)
        assert pipeline.backend is backend

    def test_pipeline_uses_injected_backend(self):
        """Verify the pipeline delegates to the backend's transcribe method."""

        class CountingBackend(TranscriptionBackend):
            def __init__(self):
                self.call_count = 0

            def transcribe(self, audio_path: str) -> list[Segment]:
                self.call_count += 1
                return [
                    Segment(
                        speaker="Test",
                        text="counted",
                        start_time=timedelta(0),
                        end_time=timedelta(seconds=1),
                    )
                ]

        backend = CountingBackend()
        pipeline = TranscriptionPipeline(backend=backend)
        result = pipeline.process_audio("S001", "/audio/test.wav")
        assert backend.call_count == 1
        assert len(result.segments) == 1
        assert result.segments[0].text == "counted"

    def test_pipeline_records_failed_status_on_backend_error_and_propagates(self):
        class FailingBackend(TranscriptionBackend):
            def transcribe(self, audio_path: str) -> list[Segment]:
                raise RuntimeError("Synthetic backend failure")

        pipeline = TranscriptionPipeline(language="fr", backend=FailingBackend())

        with pytest.raises(RuntimeError, match="Synthetic backend failure") as exc_info:
            pipeline.process_audio("S-fail", "/audio/fail.wav")

        assert str(exc_info.value) == "Synthetic backend failure"

        result = pipeline.get_result("S-fail")
        assert result is not None
        assert result.session_id == "S-fail"
        assert result.status == TranscriptionStatus.FAILED
        assert result.language == "fr"
        assert result.segments == []
        assert result.full_text == ""

    def test_pipeline_replaces_failed_result_on_subsequent_success(self):
        class FlakyBackend(TranscriptionBackend):
            def __init__(self):
                self.should_fail = True

            def transcribe(self, audio_path: str) -> list[Segment]:
                if self.should_fail:
                    raise ValueError("First attempt fails")
                return [
                    Segment(
                        speaker="Speaker 1",
                        text="recovered",
                        start_time=timedelta(seconds=0),
                        end_time=timedelta(seconds=5),
                    )
                ]

        backend = FlakyBackend()
        pipeline = TranscriptionPipeline(language="en", backend=backend)

        with pytest.raises(ValueError, match="First attempt fails"):
            pipeline.process_audio("S-flaky", "/audio/flaky.wav")

        failed_result = pipeline.get_result("S-flaky")
        assert failed_result is not None
        assert failed_result.status == TranscriptionStatus.FAILED
        assert failed_result.segments == []

        backend.should_fail = False
        success_result = pipeline.process_audio("S-flaky", "/audio/flaky.wav")

        assert success_result.status == TranscriptionStatus.COMPLETED
        assert len(success_result.segments) == 1
        assert success_result.segments[0].text == "recovered"
        stored_result = pipeline.get_result("S-flaky")
        assert stored_result is success_result
        assert stored_result.status == TranscriptionStatus.COMPLETED
