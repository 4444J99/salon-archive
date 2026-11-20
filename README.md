# Salon Archive

[![ORGAN-VI: Koinonia](https://img.shields.io/badge/ORGAN--VI-Koinonia-4a148c?style=flat-square)](https://github.com/organvm-vi-koinonia)
[![Access: Private](https://img.shields.io/badge/Access-Private%20%2F%20Invitation--Only-333333?style=flat-square)]()
[![Status: Active](https://img.shields.io/badge/Status-Active-4caf50?style=flat-square)]()

> Transcripts, session metadata, topic taxonomy, and discovery infrastructure for salon-style intellectual gatherings within the organvm eight-organ system.

[Purpose](#purpose) | [Install & run](#install--run) | [Participation Model](#participation-model) | [Session Formats](#session-formats) | [Archive Structure](#archive-structure) | [Metadata Schema](#metadata-schema) | [Topic Taxonomy](#topic-taxonomy) | [Transcription Pipeline](#transcription-pipeline) | [Search & Discovery](#search--discovery) | [Community Guidelines](#community-guidelines) | [Access & Invitations](#access--invitations) | [Contributing](#contributing) | [Channels & Platforms](#channels--platforms) | [Code of Conduct](#code-of-conduct) | [Inspirations & Lineage](#inspirations--lineage) | [Author & Contact](#author--contact)

---

## Install & run

Requires Python 3.11+.

```bash
git clone https://github.com/4444J99/salon-archive.git
cd salon-archive
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

`pip install -e .` installs the `salon` and `salon-data-export` commands.
(`koinonia-db` is not on PyPI; it is installed from its repository, pinned
in `pyproject.toml` to the frozen head of the archived repo.)

```bash
salon --help
salon-data-export --help
```

Smoke test — regenerates the data artifacts from the seed sessions, no
database needed (needs the `koinonia-db` checkout as a sibling directory,
`../koinonia-db`, as CI does):

```bash
salon-data-export
# Written: data/sessions-index.json
# Written: data/sample-session.md
```

The `salon` subcommands that query the archive (`search`, `export`, `stats`)
need a database: set `DATABASE_URL` to a Postgres URL with the koinonia-db
schema. Releases: [v0.3.0](https://github.com/4444J99/salon-archive/releases/tag/v0.3.0)
is the first published release (wheel + sdist attached).

## Purpose

The salon archive is the institutional memory of ORGAN-VI. Every gathering, conversation, and collaborative encounter that takes place within the koinonia community produces ideas, connections, and insights that deserve to persist beyond the moment of their articulation. This repository provides the infrastructure to capture, organize, index, and make discoverable the full output of the salon program.

Without an archive, salons become ephemeral social events — enjoyable but structurally invisible. The conviction underlying this repository is that intellectual community produces *artifacts*, not just experiences. A well-indexed transcript is as much an output of the organvm system as a deployed application or a published essay. The salon archive transforms dialogue into a searchable, cross-referenced knowledge base that feeds back into the system: theorists in ORGAN-I discover connections they missed, artists in ORGAN-II find provocations for new work, and the public-process documentation in ORGAN-V draws on salon discussions for essay material.

This is not a simple recording dump. The archive is designed with the same care applied to any other production system in the eight-organ model. Every session receives structured metadata, every transcript is indexed against the topic taxonomy, and every cross-reference to work in other organs is explicitly linked. The goal is an archive that becomes more valuable over time — a compounding resource for the community and for the system as a whole.

## Participation Model

Salon participation operates on an invitation-only basis. This is a deliberate architectural choice, not gatekeeping for its own sake. The salons are designed for a specific kind of engagement: participants are expected to have read preparatory materials, to engage substantively with the session's provocation, and to contribute to the documented outcomes. Open attendance would dilute the depth of exchange that makes the format generative.

Invitations are extended by the salon facilitator in consultation with the ORGAN-VI community steward. The criteria for invitation are intellectual engagement and willingness to participate in structured dialogue, not credentials or institutional affiliation. A thoughtful autodidact is as welcome as an academic; a practicing artist is as welcome as a theorist. What matters is the capacity and willingness to contribute to the shared inquiry.

Participants in any given salon session are recorded in the session metadata (with consent). Repeat participation builds familiarity and depth — the salon program is designed for an evolving cohort, not a rotating cast of strangers. Over time, participants develop shared references, running threads, and the kind of productive shorthand that makes deep intellectual work possible in a group setting.

New participants are typically introduced through a specific session rather than joining the archive directly. The archive itself is accessible to all community members — you do not need to have attended a salon to read its transcript — but the live sessions maintain a curated participant list to preserve the conditions for substantive exchange.

## Session Formats

The salon program offers several distinct formats, each designed for a different mode of intellectual engagement. The format is selected by the facilitator based on the session's topic, the available participants, and the desired outcome.

### Lightning Talks

Short, focused presentations (10-15 minutes) followed by structured Q&A. Lightning talks are designed for sharing work-in-progress, introducing new concepts, or presenting preliminary findings. The constraint of brevity forces clarity — speakers must distill their contribution to its essential argument. Lightning talk sessions typically feature three to four speakers, with facilitated discussion weaving the presentations into a coherent conversation. These sessions are particularly effective for surfacing unexpected connections between different parts of the organvm system.

### Deep Dives

Extended single-topic explorations (60-90 minutes) in which a facilitator guides the group through a prepared investigation of a specific question, framework, or problem. Deep dives begin with a provocation — a reading, a demonstration, a question — and proceed through structured phases of exploration, critique, and synthesis. The facilitator's role is not to lecture but to maintain the thread of inquiry, ensuring the group goes deep rather than wide. Deep dives produce the most substantive archive entries, as the extended format allows ideas to develop through multiple iterations of challenge and refinement.

### Socratic Dialogues

Facilitated exchanges structured around a specific question, using the Socratic method of guided inquiry. The facilitator poses questions rather than providing answers, drawing out the assumptions, implications, and contradictions in participants' positions. Socratic dialogues are particularly valuable for examining foundational commitments — what do we mean by "recursive" in the context of ORGAN-I? What constitutes "community" in a distributed creative practice? These sessions often surface disagreements and tensions that are productive rather than divisive, revealing the genuine complexity of the system's conceptual landscape.

### Collaborative Ideation

Working sessions designed to produce specific outputs: a new project concept, a curriculum outline, an essay draft, a governance proposal. Collaborative ideation sessions are less about exploration and more about production. They begin with a clear brief, proceed through structured brainstorming and critique, and conclude with an artifact that can be developed further. The archive for these sessions includes not only the transcript but the output artifact itself, with attribution to all contributors.

## Archive Structure

The archive is organized around sessions as the primary unit. Each session receives its own directory containing all associated materials.

```
sessions/
  YYYY-MM-DD--session-slug/
    transcript.md          # Full session transcript (cleaned, attributed)
    metadata.yaml          # Structured session metadata
    notes.md               # Facilitator notes and post-session reflections
    materials/             # Pre-session readings, slides, reference materials
    outputs/               # Artifacts produced during the session
    media/                 # Audio recordings, images, screenshots (if applicable)
```

Sessions are indexed by date, topic, format, and participants. The archive's root contains aggregate indices that allow multiple navigation paths into the material:

```
index/
  by-date.md               # Chronological session listing
  by-topic.md              # Sessions organized by topic taxonomy
  by-format.md             # Sessions grouped by format type
  by-participant.md        # Sessions indexed by participant (with consent)
  cross-references.md      # Links between sessions and other organ repos
taxonomy/
  organ-mapping.yaml       # Topic-to-organ alignment
  themes.yaml              # Cross-cutting themes across sessions
```

The archive structure is designed to be both human-browsable and machine-parseable. A researcher can navigate the index files directly; a script can parse the YAML metadata to generate visualizations, statistics, or cross-reference reports.

## Metadata Schema

Every session carries structured metadata in YAML format. The schema captures the information necessary for indexing, cross-referencing, and retrospective analysis.

```yaml
session:
  id: "2026-03-15--recursive-ontology"
  date: 2026-03-15
  format: deep-dive
  facilitator: "@4444J99"
  duration_minutes: 90
  participants:
    - name: "Participant Name"
      handle: "@github-handle"
      consent_to_archive: true
  topic:
    title: "Recursive Ontology and Self-Referential Systems"
    taxonomy_tags:
      - recursion
      - ontology
      - self-reference
    organ_alignment:
      primary: ORGAN-I
      secondary: [ORGAN-II, ORGAN-IV]
  cross_references:
    - repo: "organvm-i-theoria/recursive-engine--generative-entity"
      context: "Discussion of RE:GE's ritual syntax as a model for recursive ontology"
    - repo: "organvm-ii-poiesis/metasystem-master"
      context: "Metasystem-master's orchestration layer as practical instantiation"
  materials:
    - type: reading
      title: "Hofstadter, Strange Loops chapter 12"
    - type: demonstration
      title: "Live walkthrough of recursive-engine ritual execution"
  outputs:
    - type: insight
      description: "Proposed extension of ritual syntax to handle nested self-reference"
    - type: action_item
      description: "Draft specification for recursive ritual nesting (assigned to @4444J99)"
  transcript_word_count: 4200
  notes: "Particularly generative session. The connection between ritual syntax and self-referential ontology had not been explicitly drawn before."
```

The schema is extensible — additional fields can be added for specific session formats — but these core fields are required for every archived session. The `organ_alignment` field is particularly important: it makes explicit how each salon session connects to the broader eight-organ system, enabling the kind of cross-organ discovery that makes the archive a system resource rather than a standalone document collection.

## Topic Taxonomy

The salon topic taxonomy is aligned with the eight-organ model, providing a shared vocabulary for categorizing and cross-referencing session content.

**ORGAN-I (Theory) Topics:** recursion, ontology, epistemology, self-reference, formal systems, symbolic logic, framework design, philosophical foundations, system theory, emergence, autopoiesis, strange loops, category theory applied.

**ORGAN-II (Art) Topics:** generative art, algorithmic composition, performance systems, interactive media, aesthetic philosophy, creative process, artistic intention, medium specificity, audience experience, exhibition design, sound art, visual systems, procedural generation.

**ORGAN-III (Commerce) Topics:** creative sustainability, product design, business models for art, SaaS architecture, public data infrastructure, open source economics, value capture, ethical commerce, pricing philosophy, B2B creative tools.

**ORGAN-IV (Orchestration) Topics:** governance models, dependency management, promotion criteria, system health, automation philosophy, workflow design, institutional structure, decision-making processes, quality gates.

**ORGAN-V (Public Process) Topics:** building in public, transparency, documentation as practice, essay craft, long-form writing, publication ethics, audience relationship, knowledge sharing.

**ORGAN-VI (Community) Topics:** facilitation, salon design, curriculum development, collaborative inquiry, community governance, inclusion, intellectual hospitality, gathering design, feedback culture.

**ORGAN-VII (Marketing) Topics:** distribution strategy, audience building, POSSE methodology, content repurposing, announcement craft, narrative framing, public communication.

**Cross-cutting themes** span multiple organs: sustainability, scale, ethics, recursion-in-practice, human-AI collaboration, institutional design, portfolio as practice, creative infrastructure.

## Transcription Pipeline

Session transcription follows a defined pipeline to ensure accuracy, attribution, and archival quality.

**Stage 1: Capture.** Sessions are recorded (audio or video, with participant consent). The raw recording is stored in the session's `media/` directory. For text-based sessions (asynchronous or chat-format), the raw log serves as the capture artifact.

**Stage 2: Draft Transcription.** AI-assisted transcription generates a first-pass transcript from the recording. Speaker attribution is assigned using voice identification or manual tagging. The draft transcript preserves the full session content, including digressions, tangents, and informal exchanges.

**Stage 3: Editorial Review.** The facilitator reviews the draft transcript for accuracy, corrects misattributions, and annotates key moments (insights, decisions, action items). Participants are invited to review their own contributions for accuracy. The editorial review preserves the conversational character of the session while ensuring factual correctness.

**Stage 4: Structuring.** The reviewed transcript is structured with section headings, cross-reference links, and taxonomy tags. Key quotes are highlighted. The `metadata.yaml` file is populated from the structured transcript.

**Stage 5: Archival.** The structured transcript and metadata are committed to the archive. Index files are updated. Cross-reference links to other organ repos are verified and added to the cross-references index.

The pipeline is designed to minimize the time between session and archival — ideally, a session is fully archived within one week of occurrence. The AI-assisted transcription stage reduces the bottleneck of manual transcription, while the editorial and structuring stages ensure quality.

## Search & Discovery

The archive supports multiple discovery paths to serve different use cases.

**Chronological browsing** — the `by-date.md` index provides a timeline view of all sessions, useful for understanding the salon program's evolution and for finding sessions from a specific period.

**Topic-based search** — the `by-topic.md` index and `taxonomy/themes.yaml` allow navigation by subject matter. A researcher interested in recursion can find all sessions that engaged with recursive systems, regardless of format or date.

**Cross-organ discovery** — the `cross-references.md` index maps salon sessions to specific repositories in other organs. A contributor to ORGAN-I's recursive-engine can find all salon discussions that referenced their work. This bidirectional linking makes the archive a navigation tool for the entire system, not just ORGAN-VI.

**Participant-based access** — the `by-participant.md` index (populated with consent) allows participants to find all sessions they attended, creating a personal record of engagement with the community.

**Full-text search** — transcript files are plain Markdown, enabling standard text search across the full archive. Combined with the structured metadata, this allows queries such as "all deep-dive sessions in which ontology was discussed and ORGAN-II repos were referenced."

## Community Guidelines

The salon community operates according to principles that prioritize generative exchange over performative debate.

**Intellectual generosity.** Assume good faith. Engage with the strongest version of a position, not the weakest. Offer your knowledge freely and receive others' contributions with curiosity rather than defensiveness.

**Structured spontaneity.** Salons are facilitated, not free-form. Respect the facilitator's role in maintaining focus and managing time. Within the structure, be willing to follow unexpected threads — the most valuable insights often emerge from productive tangents.

**Attribution and credit.** Ideas shared in salons belong to the community, but attribution matters. When an insight from a salon session influences work in another organ, credit the session and the contributor. The archive exists partly to make this attribution possible.

**Consent and privacy.** Participation in a salon implies consent to archival of the session transcript, but participants can request redaction of specific contributions. The archive respects boundaries: some discussions may be marked as off-the-record at the facilitator's discretion.

**Preparation.** Salon participants are expected to engage with pre-session materials. The depth of the exchange depends on participants arriving with shared context. If you cannot prepare for a session, communicate this to the facilitator in advance.

## Access & Invitations

Access to the salon archive is governed by ORGAN-VI community membership. All community members can read archived transcripts. Participation in live sessions requires a specific invitation for each session or series.

Invitations are extended based on relevance to the session topic, track record of substantive participation, and the facilitator's judgment about group composition. The goal is to assemble groups that are intellectually diverse but operationally compatible — people who will challenge each other's assumptions while maintaining the conditions for collaborative inquiry.

To request access to the archive or express interest in salon participation, contact the ORGAN-VI community steward through the channels listed below. There is no formal application process; a brief expression of interest and relevant background is sufficient to begin the conversation.

Community membership is not permanent by default. Members who are inactive for an extended period may be moved to an alumni list with continued read access to the archive. This is not punitive — it reflects the reality that active community requires ongoing participation, and the invitation list should reflect who is currently engaged.

## Contributing

Contributions to the salon archive take several forms.

**Transcript improvement.** Reviewing and correcting archived transcripts, adding cross-references, improving structuring. This is the most accessible form of contribution and is valuable regardless of whether you attended the original session.

**Taxonomy development.** Proposing new taxonomy categories, refining existing ones, mapping sessions to the evolving topic structure. The taxonomy is a living document that grows with the archive.

**Index maintenance.** Keeping the various index files accurate and up to date, especially the cross-references index which depends on awareness of work across all eight organs.

**Session facilitation.** Experienced community members may propose and facilitate salon sessions. This requires familiarity with the session formats, the archival pipeline, and the community guidelines. Aspiring facilitators should attend several sessions before proposing their own.

**Tool development.** Building scripts, search tools, or visualization systems that make the archive more accessible and useful. Technical contributions should follow the conventions established in ORGAN-IV for system tooling.

## Channels & Platforms

The salon program uses multiple channels for different functions.

**Session scheduling and logistics** are coordinated through the ORGAN-VI community platform (currently Discord, with invitations managed by the community steward).

**Pre-session materials** are distributed via the session directory in this repository, with notifications sent through the community platform.

**Live sessions** take place on video call (platform determined per session) or, when possible, in person.

**Post-session discussion** continues on the community platform, with substantive threads archived in the session's `notes.md` or as addenda to the transcript.

**Archive access** is through this GitHub repository directly. Community members with repository access can browse, search, and contribute to the archive using standard Git workflows.

## Code of Conduct

All salon participants and archive contributors are bound by the [organvm Code of Conduct](https://github.com/organvm-vi-koinonia/.github/blob/main/CODE_OF_CONDUCT.md), which establishes baseline expectations for respectful, inclusive engagement across the eight-organ system.

In addition to the system-wide code of conduct, the salon community observes specific norms. Disagreement is expected and welcomed — intellectual community without disagreement is intellectual performance. But disagreement is directed at ideas, not people. Personal attacks, dismissive rhetoric, and bad-faith argumentation are incompatible with the salon format and will result in removal from the session and, if persistent, from the community.

Conflict resolution follows the ORGAN-VI community governance process: direct conversation first, mediation by the community steward second, and formal review by the ORGAN-IV governance framework as a last resort. The goal is always restoration of the conditions for productive exchange, not punishment.

## Inspirations & Lineage

The salon archive draws on several historical and contemporary models for structured intellectual community.

**Gertrude Stein's Paris salons** (1903-1946) demonstrated that curated gatherings of artists, writers, and thinkers could produce cultural movements — not through formal instruction but through the friction of diverse perspectives in a hospitable setting. The salon archive's emphasis on cross-disciplinary encounter and documented outcomes reflects this tradition.

**The Macy Conferences** (1941-1960) brought together researchers from cybernetics, anthropology, psychology, and mathematics in a series of invitation-only meetings that produced foundational work in systems theory, information theory, and cognitive science. The conferences' interdisciplinary structure and their insistence on documenting proceedings for future reference directly inform the salon program's approach to archival.

**The Long Now Foundation's seminars** (2003-present) model sustained intellectual programming over decades, with each session archived and made available as a resource for future inquiry. The Long Now's commitment to long-term thinking — the idea that cultural infrastructure should be designed for decades, not quarters — resonates with the organvm system's approach to institutional design.

**Santa Fe Institute workshops** combine structured inquiry with collaborative problem-solving, assembling small groups of researchers to tackle specific questions at the boundaries of their disciplines. The salon program's collaborative ideation format draws directly on this model.

These inspirations share a common conviction: that intellectual community, properly structured and documented, produces more than any individual working alone. The salon archive is the infrastructure that makes this conviction operational within the organvm system.

## Author & Contact

**Maintained by:** [@4444J99](https://github.com/4444J99)
**Organization:** [organvm-vi-koinonia](https://github.com/organvm-vi-koinonia)
**Part of:** The [organvm eight-organ system](https://github.com/meta-organvm) — a creative-institutional framework spanning theory, art, commerce, orchestration, public process, community, and marketing.

For questions about the salon archive, community membership, or session participation, reach out through the organvm community channels or open a discussion in this repository.

---

*ORGAN-VI is the gathering space where the organvm system's ideas are tested, challenged, and extended through shared inquiry. The salon archive ensures that what happens in these gatherings persists, compounds, and feeds back into the system as a whole.*

<!-- SYSTEM-NAV-START -->

---

<sub>[Portfolio](https://4444j99.github.io/portfolio/) · [System Directory](https://4444j99.github.io/portfolio/directory/) · [ORGAN VI · Koinonia](https://organvm-vi-koinonia.github.io/) · Part of the <a href="https://4444j99.github.io/portfolio/directory/">ORGANVM eight-organ system</a></sub>

<!-- SYSTEM-NAV-END -->
