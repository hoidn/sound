---
id: NAV-DECISIONS
type: index
status: active
updated: 2026-10-22
access: neutral
---

# Documentation governance decisions

| Decision | State | Purpose |
| --- | --- | --- |
| [ADR 0001](adr-0001-documentation.md) | Adopted | Persistent wiki, role routing, specs, implementation docs, and handoff boundaries |
| [ADR 0002](adr-0002-static-first-analysis.md) | Adopted; narrowed by ADR 0003 | Static-first specification work and targeted runtime escalation |
| [ADR 0003](adr-0003-no-reference-execution.md) | Adopted; reopened by ADR 0006 | No whole-application reference execution; extracted execution of original x86_64 functions permitted (label X); work finishes on the Linux x86_64 workstation. The whole-application restriction is reopened by ADR 0006; the X rules stand |
| [ADR 0006](adr-0006-reference-observation-reopened.md) | Adopted; D-07 local Windows VM selected/readiness open | Whole-application observation of Live 12.4.3 reinstated as evidence route O once a reference host is recorded; Phase 4 run sheet reinstated; completion rule and clean-room boundary unchanged |
| [ADR 0004](adr-0004-target-scope-t1.md) | Adopted | First completion target T1: Live Set files, offline-rendered playback of session clips, mixer, automation and the seven bundled devices, MIDI control; acceptance dimensions (answers Q-001 for T1) |

| [ADR 0005](adr-0005-full-live-specification-coverage.md) | Adopted | Entire Live behavioral specification target; supersedes the outside-T1 specification freeze while preserving T1 and analyst/implementation boundaries; [confirmed closure rule](adr-0005-full-live-specification-coverage.md#completion-rule-confirmation--2026-10-20) keeps unsupported required behavior open |

Technical implementation decisions belong with the candidate's implementation
documentation. Analyst findings remain evidence, not architectural mandates.
