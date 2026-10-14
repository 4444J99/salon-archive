"""CLI entry point for salon-archive.

Usage:
    python -m src ingest --audio /path/to/audio.wav --session-id S001
    python -m src search --topic "recursion"
    python -m src export --session-id 1 --format json
    python -m src stats
"""

from __future__ import annotations

import sys

import click

from .config import Settings
from .export import export_session_json, export_session_markdown, session_to_dict
from .transcription import TranscriptionPipeline


@click.group()
def cli() -> None:
    """Salon transcription, search, and export toolkit."""


@cli.command()
@click.option("--audio", required=True, help="Path to audio file")
@click.option("--session-id", required=True, help="Unique session identifier")
@click.option("--language", default="en", help="Language code (default: en)")
def ingest(audio: str, session_id: str, language: str) -> None:
    """Ingest an audio recording and produce a transcription."""
    pipeline = TranscriptionPipeline(language=language)
    result = pipeline.process_audio(session_id, audio)
    click.echo(f"Ingested session {session_id}: {len(result.segments)} segment(s)")
    click.echo(f"Status: {result.status.value}")
    click.echo(f"Duration: {result.total_duration}")
    if result.speaker_list:
        click.echo(f"Speakers: {', '.join(result.speaker_list)}")


@cli.command()
@click.option("--topic", default=None, help="Search by topic keyword (text search)")
@click.option("--exact-tag", default=None, help="Search by exact organ_tags array match")
@click.option("--limit", type=int, default=20, help="Max results")
def search(topic: str | None, exact_tag: str | None, limit: int) -> None:
    """Search the session archive by topic or tag."""
    try:
        db_url = Settings.require_db()
    except RuntimeError as exc:
        click.echo(f"Error: {exc}", err=True)
        raise SystemExit(1)

    from .repository import SalonRepository

    repo = SalonRepository(db_url)
    if exact_tag:
        results = repo.search_by_topic(exact_tag)
    elif topic:
        results = repo.search_by_text(topic)
    else:
        results = repo.list_sessions(limit=limit)

    if not results:
        click.echo("No matching sessions found.")
        return

    for row in results:
        click.echo(f"  [{row.id}] {row.title} ({row.date})")
    click.echo(f"\n{len(results)} session(s) found.")


@cli.command("export")
@click.option("--session-id", required=True, type=int, help="Session ID to export")
@click.option(
    "--format",
    "fmt",
    type=click.Choice(["json", "markdown"]),
    default="json",
    help="Output format",
)
def export_cmd(session_id: int, fmt: str) -> None:
    """Export a session record in the requested format."""
    try:
        db_url = Settings.require_db()
    except RuntimeError as exc:
        click.echo(f"Error: {exc}", err=True)
        raise SystemExit(1)

    from .repository import SalonRepository

    repo = SalonRepository(db_url)
    row = repo.get_session(session_id)
    if row is None:
        click.echo(f"Session {session_id} not found.", err=True)
        raise SystemExit(1)

    segments = repo.get_segments(session_id)
    data = session_to_dict(row, participants=[], segments=segments)

    if fmt == "json":
        click.echo(export_session_json(data))
    else:
        click.echo(export_session_markdown(data))


@cli.command()
def stats() -> None:
    """Show archive statistics."""
    try:
        db_url = Settings.require_db()
    except RuntimeError as exc:
        click.echo(f"Error: {exc}", err=True)
        raise SystemExit(1)

    from .repository import SalonRepository

    repo = SalonRepository(db_url)
    sessions = repo.count_sessions()
    nodes = repo.count_taxonomy_nodes()
    click.echo(f"Sessions:       {sessions}")
    click.echo(f"Taxonomy nodes: {nodes}")


# Legacy entry point for `python -m src`
def main(argv: list[str] | None = None) -> int:
    """Dispatch to Click CLI, returning an exit code."""
    try:
        cli(standalone_mode=False, args=argv)
        return 0
    except SystemExit as exc:
        return exc.code if isinstance(exc.code, int) else 1
    except Exception as exc:  # noqa: BLE001 - intentional top-level CLI guard: report and exit 1
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
