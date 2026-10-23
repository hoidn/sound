# Bundled-device host protocol packet r1

Analyst-authored 2026-10-19; static only, not a released handoff. Canonical pages:
[research](../../../../wiki/research/device-host-protocol.md) and
[spec](../../../../wiki/specs/bundled-device-hosting.md). Local page snapshots are
frozen for separate review; manifest digests identify the reviewed revision.

- Target: Ableton Live 12 Suite 12.4.3, macOS arm64 main executable, SHA-256
  `3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad`.
- Seven device bundles: original H4 `bundles.json`, copied unchanged as
  `bundle-identities.json`, pins executable and arm64 slice digests.
- `live-records.jsonl`: 51 selected original export records copied as exact bytes
  from retained `/var/tmp/sound-analysis/corpus/decomp/chunks/`. No reconstructed
  pseudocode or reserialization. `record-locators.json` maps packet line to source
  chunk/line and hashes original record/code bytes. `corpus-run.json` copied
  unchanged; `n5-manifest.json` preserves earlier source provenance.
- `capture.py`: analyst retention utility; `python3 -I <packet>/capture.py` reads
  pinned local source files, checks record/code integrity/completeness and retains
  these selected records. It never calls the original program or native tools.
- `case-index.json`: analyst index of all 26 draft cases, 14 conditional static
  expectations and 12 explicitly ungraded unknowns. Numeric vectors and conditions
  are in `spec-r1.md`, not falsely represented as captured execution results.
- `research-r1.md`, `spec-r1.md`: exact canonical snapshots.
- `manifest.json`: payload sizes/digests, source pins, scope and validation.

No whole-application or extracted original-code run, candidate test, binary
modification, installation, host identity spoofing or publication occurred.
Amp/Cabinet emulation remains blocked and T1.6 pending. Shared indexes, coverage,
questions, log and historical correction backlinks are root-owned integration.

The bounded correction matters: ordinary reset and rate changes call no warm-up;
ResetAndDispatch requests four 1,024-frame warm-ups, then reset. Earlier extracted
1,024-frame test sequences remain those finite tests, not proof of Live's insertion
sequence. Reset sound/stop/resume/frame base remain ungraded.
