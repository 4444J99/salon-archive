"""Repository pattern for salon archive database operations.

Wraps sync SQLAlchemy queries for CLI simplicity. Uses the shared
koinonia-db ORM models from ORGAN-VI.
"""

from __future__ import annotations

from koinonia_db.models.salon import (
    Participant,
    SalonSessionRow,
    TaxonomyNodeRow,
)
from koinonia_db.models.salon import (
    Segment as SegmentRow,
)
from sqlalchemy import any_, create_engine, literal, select
from sqlalchemy.orm import Session


class SalonRepository:
    """Synchronous repository for salon session CRUD against Neon/Postgres."""

    def __init__(self, database_url: str) -> None:
        self._engine = create_engine(database_url)

    # ── Sessions ──────────────────────────────────────────────────────

    def add_session(
        self,
        title: str,
        date: str | object,
        format: str,
        facilitator: str | None,
        notes: str,
        organ_tags: list[str],
        participants: list[dict],
        segments: list[dict],
    ) -> int:
        """Insert a salon session with participants and segments. Returns the new session id."""
        with Session(self._engine) as s:
            row = SalonSessionRow(
                title=title,
                date=date,
                format=format,
                facilitator=facilitator,
                notes=notes,
                organ_tags=organ_tags,
            )
            s.add(row)
            s.flush()
            for p in participants:
                s.add(
                    Participant(
                        session_id=row.id,
                        name=p["name"],
                        role=p.get("role", "participant"),
                        consent_given=p.get("consent_given", False),
                    )
                )
            for seg in segments:
                s.add(
                    SegmentRow(
                        session_id=row.id,
                        speaker=seg["speaker"],
                        text=seg["text"],
                        start_seconds=seg["start_seconds"],
                        end_seconds=seg["end_seconds"],
                        confidence=seg.get("confidence", 0.0),
                    )
                )
            s.commit()
            return row.id

    def get_session(self, session_id: int) -> SalonSessionRow | None:
        """Fetch a single session by primary key."""
        with Session(self._engine) as s:
            return s.get(SalonSessionRow, session_id)

    def search_by_topic(self, topic: str) -> list[SalonSessionRow]:
        """Find sessions whose organ_tags array contains the given topic (exact match)."""
        with Session(self._engine) as s:
            stmt = select(SalonSessionRow).where(
                literal(topic) == any_(SalonSessionRow.organ_tags)
            )
            return list(s.scalars(stmt))

    def search_by_text(self, query: str) -> list[SalonSessionRow]:
        """Find sessions matching query via ILIKE on title, notes, and organ_tags text."""
        with Session(self._engine) as s:
            q = f"%{query}%"
            from sqlalchemy import String, cast
            stmt = select(SalonSessionRow).where(
                SalonSessionRow.title.ilike(q)
                | SalonSessionRow.notes.ilike(q)
                | cast(SalonSessionRow.organ_tags, String).ilike(q)
            )
            return list(s.scalars(stmt))

    def list_sessions(self, limit: int = 20) -> list[SalonSessionRow]:
        """Return the most recent sessions, ordered by date descending."""
        with Session(self._engine) as s:
            stmt = (
                select(SalonSessionRow)
                .order_by(SalonSessionRow.date.desc())
                .limit(limit)
            )
            return list(s.scalars(stmt))

    def get_segments(self, session_id: int) -> list[SegmentRow]:
        """Return transcript segments for a session, ordered by start time."""
        with Session(self._engine) as s:
            stmt = (
                select(SegmentRow)
                .where(SegmentRow.session_id == session_id)
                .order_by(SegmentRow.start_seconds)
            )
            return list(s.scalars(stmt))

    # ── Taxonomy ──────────────────────────────────────────────────────

    def add_taxonomy_node(
        self,
        slug: str,
        label: str,
        parent_id: int | None = None,
        description: str = "",
        organ_id: int | None = None,
    ) -> int:
        """Insert a taxonomy node. Returns the new node id."""
        with Session(self._engine) as s:
            node = TaxonomyNodeRow(
                slug=slug,
                label=label,
                parent_id=parent_id,
                description=description,
                organ_id=organ_id,
            )
            s.add(node)
            s.commit()
            return node.id

    def get_taxonomy_roots(self) -> list[TaxonomyNodeRow]:
        """Return all root-level taxonomy nodes (parent_id IS NULL)."""
        with Session(self._engine) as s:
            stmt = select(TaxonomyNodeRow).where(
                TaxonomyNodeRow.parent_id.is_(None)
            )
            return list(s.scalars(stmt))

    def search_taxonomy(self, query: str) -> list[TaxonomyNodeRow]:
        """Search taxonomy by label or description (case-insensitive ILIKE)."""
        with Session(self._engine) as s:
            q = f"%{query}%"
            stmt = select(TaxonomyNodeRow).where(
                TaxonomyNodeRow.label.ilike(q) | TaxonomyNodeRow.description.ilike(q)
            )
            return list(s.scalars(stmt))

    # ── Counts ────────────────────────────────────────────────────────

    def count_sessions(self) -> int:
        """Return the total number of salon sessions."""
        with Session(self._engine) as s:
            return s.query(SalonSessionRow).count()

    def count_taxonomy_nodes(self) -> int:
        """Return the total number of taxonomy nodes."""
        with Session(self._engine) as s:
            return s.query(TaxonomyNodeRow).count()
