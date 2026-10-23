# Recording/capture/comping analyst packet

Target: Ableton Live 12 Suite **12.4.3**; created 2026-10-19. Analysis only.
No original code was executed; no handoff payload or candidate implementation
is included. Canonical synthesis: `wiki/research/recording-comping.md`.
Behavioral draft: `wiki/specs/recording-comping.md`.

## Source capture

`sources.json` records the four official Live 12 chapter URLs, final URLs,
actual UTC capture timestamps, declared manual version, bytes and SHA-256.
The corresponding `manual-12-*-2026-10-19.html` files retain response bodies
without modification. Captured with Python 3 urllib.request.urlopen on
2026-10-19. Public pages declare **Version 12**, without a patch/build identifier
or publication date observed: documentary expectations have **exact-build U**.
Figures were not inspected. No visual/layout fidelity is inferred from HTML.

Recording chapter SHA-256:
`fd7325fb99d9887c46501fdd935c8b60e7eb81f121fed45f3a7bbc0109c84798`.
Comping chapter SHA-256:
`e750973536d4331342ad392e637a7661b2a75dcd533c3e72c6cabe4a8ceab28b`.
All four source hashes are in `sources.json`; all packet-file hashes except
the manifest itself are in `manifest.json`. Captures are immutable; a recapture
must use a new dated/revision file.

## Retained local evidence

- `schema-fields.json`: selected declarations from
  `/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/Schema/12.0_12402.txt`,
  SHA-256 `b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299`.
- `shipped-documents.json`: each of 376 original `.als`/`.alc` paths and byte
  hashes under App-Resources; selected recording metadata and exact per-lane
  paths. AppleDouble companion files excluded. The pinned bundle includes
  documents authored under earlier versions. No full-document source copy is
  implied; source bytes remain in the original local bundle.
- `native-string-excerpts.json`: seven referenced string records from
  `/var/tmp/sound-analysis/corpus/indexes/strings.jsonl`; source hash, original
  line number/line hash and exact record retained. Native **inventory only**;
  it proves neither action dispatch nor recording execution. Corpus identity
  relates to the existing C1/C2 arm64 target slice SHA-256
  `3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad`.
- `summary.json`: 376 documents, nine containing 140 lanes, 4,130 TakeId values,
  seven selected native records. Lane event clips: 140 MidiClip, no AudioClip;
  every retained lane Audition value is false. These content observations do
  not establish original interactive behavior.

## Reproduction and checks

From repository root, with existing local bundle/corpus inputs:

```sh
python3 analysis/ableton-live-12.4.3/full-spec-v1/recording/inspect_sources.py
```

This uses only the Python standard library; it reads XML/gzip/schema and the
retained native string inventory, and writes derived packet JSON. It never
starts Live, a decompiler or an extracted-code harness. Assertions check that
the selected schema classes, shipped documents and native string identities
exist. A second inventory run reproduced the retained summary. Public HTML
is not redownloaded by the inventory script.

Requirement/case audit: 32 stable requirement IDs, 81 distinct case IDs; 65 D12
documentary comparators, four D12403 artifact-only audits and 12 U cases. All
77 application-behavior cases are ungraded for 12.4.3. These scenarios are partial
clause coverage. The unreleased review correction narrows scene tempo/meter
capture to values included in launched-scene names and links Arrangement's
canonical playback-ownership laws. **X: none; S behavioral
comparators: none.** Local pages and packet links were checked; hashes verified
against `sources.json` and `manifest.json`. This is evidence integrity and
documentation checking, not original-versus-candidate validation.
