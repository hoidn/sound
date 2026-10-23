# Bundled-device host protocol packet r2

Analyst-authored 2026-10-19; static only, not a released handoff. Canonical pages:
[research](../../../../wiki/research/device-host-protocol.md) and
[spec](../../../../wiki/specs/bundled-device-hosting.md). Revision 2 snapshots are
frozen for focused independent re-review; manifest digests identify this revision.
The original r1 manifest and all 10 original payloads remain byte-identical under
`revisions/r1/`; root-level r1 page snapshots are also retained unchanged.

- Target: Ableton Live 12 Suite 12.4.3, macOS arm64 main executable, SHA-256
  `3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad`.
- Seven device bundles: original H4 `bundles.json`, copied unchanged as
  `bundle-identities.json`, pins executable and arm64 slice digests.
- `live-records.jsonl`: **51 unchanged original export records**, copied as exact
  bytes from retained `/var/tmp/sound-analysis/corpus/decomp/chunks/`. The original
  trailing newlines and all newline-inclusive record SHA256 pins are preserved.
  `record-locators.json` maps packet line to source chunk/line and record/code
  hashes. `corpus-run.json` and `n5-manifest.json` preserve source provenance.
- `capture.py`: existing analyst retention utility, unchanged from r1. No recapture
  or original/native-tool execution was required for the classification correction.
- `case-index.json`: current analyst inventory of **26 case entries: three
  conditional S composition checks and 23 U application cases**. Eleven U entries
  additionally link to non-normative static component models in canonical research;
  those models are excluded from compatibility coverage. Synthetic wet samples
  and arithmetic tolerances are project vectors, not captured Amp/Cabinet audio.
- Requirements: **12 total, one conditional S mixing law and 11 U application
  requirements**. The supported internal preparation/queue/partition/context/rate
  transformations impose no candidate boundary, instrumentation or architecture.
- `research-r2.md`, `spec-r2.md`: exact current canonical snapshots.
- `review-response-r2.json`: disposition of BDH-REVIEW-001/002 from the independent
  r1 review. Acceptance remains for the separate reviewer.
- `manifest.json`: current payload sizes/digests, source pins and classification;
  prior seal is `revisions/r1/manifest.json`.

No whole-application or extracted original-code run, candidate test, binary
modification, installation, host identity spoofing or publication occurred.
No application compatibility case passed. Amp/Cabinet emulation remains blocked
and T1.6 pending. Shared indexes, coverage, questions, log and historical correction
backlinks are root-owned integration.

Static reset distinction remains supported: ordinary reset and rate changes call
no host warm-up helper; ResetAndDispatch requests four 1,024-frame warm-ups, then
reset. Earlier extracted 1,024-frame sequences remain those finite tests, not
proof of Live insertion behavior. Reset sound, stop/resume, frame base, rate-change
note continuity and processing-error outcomes remain ungraded.
