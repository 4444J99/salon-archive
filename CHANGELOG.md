# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- CI: ruff and pyright made green (#13)

## [0.5.0] - 2026-02-24

### Added
- `data_export` module — generates `data/sessions-index.json` and `data/sample-session.md` from seed data
- `salon-data-export` CLI entry point
- 5 new tests in `tests/test_data_export.py`
- Produce edge fulfilled: `data` (json+markdown)

## [0.4.0] - 2026-02-17

### Added
- **AQUA COMMUNIS sprint** — no code changes; test suite stable at 76 tests (72 pass, 4 skipped)

## [0.3.0] - 2026-02-17

### Added
- Full-text search repository method `search_fulltext()` using PostgreSQL tsvector + `plainto_tsquery`
- Transcript search method `search_transcripts()` with `ts_headline` highlighted results

### Deprecated
- `search_by_text()` ILIKE method — use `search_fulltext()` for better performance

## [0.2.0] - 2026-02-17

### Added

- Database-backed repository (SalonRepository) using koinonia-db models
- Click CLI with `search`, `export`, `stats`, and `ingest` commands
- Text search via ILIKE (`search_by_text`) alongside exact tag search
- `--exact-tag` flag for array-element matching (original behavior)

### Changed

- URL conversion (postgresql→psycopg) moved from repository to config.py
- Default search uses text matching instead of exact tag match

### Deprecated

- In-memory `SessionArchive` and `Taxonomy` classes (retained as offline fallback)

## [0.1.1] - 2026-02-11

### Added

- Platinum Sprint: standardized badge row, CHANGELOG
- Initial CHANGELOG following Keep a Changelog format

## [0.1.0] - 2026-02-11

### Added

- Initial public release as part of the organvm eight-organ system
- Core project structure and documentation

[Unreleased]: https://github.com/4444J99/salon-archive/compare/v0.5.0...HEAD
[0.5.0]: https://github.com/4444J99/salon-archive/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/4444J99/salon-archive/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/4444J99/salon-archive/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/4444J99/salon-archive/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/4444J99/salon-archive/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/4444J99/salon-archive/releases/tag/v0.1.0
