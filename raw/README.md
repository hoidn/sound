# Source storage

Raw sources are immutable inputs. Capture new bytes under a new name; never
edit an existing capture to correct or modernize its contents. Source pages in
the wiki hold interpretation and corrections.

| Location | Contents | Versioning |
| --- | --- | --- |
| `public/` | Small, redistributable source captures and user-supplied excerpts | May be tracked; record provenance |
| `inbox/` | New sources awaiting classification | Ignored; ingest into a durable location before relying on them |
| `restricted/` | Binary-derived material, decompilation, private research | Ignored; analyst access only |
| `artifacts/` | Optional local copies of binaries or packages | Ignored; prefer an external artifact store |
| `captures/` | Original-side audio, UI, API, and process captures | Ignored; use a backed-up external store for durable evidence |
| `../analysis/` | Existing original-side generated evidence, scripts, and derived binaries | Ignored; registered in the research source catalog |

Create directories when they first have content. An ignored local file is not
a durable archive or a security boundary. Every source page must record the
locator, version/date, SHA-256 where bytes are available, access class, and
retention location. Evidence needed for a conclusion must remain retrievable.
If it is lost, mark affected claims unsupported or stale.

Keep original applications outside this repository. Record artifact identity
without copying proprietary executables or bundled media into tracked files.
Capture public URLs at a commit/version when practical. If a copy cannot be
retained, record that it is URL-only and may change.

New sources enter through [the ingest workflow](../wiki/workflows.md#ingest-a-source).
Only reviewed, explicitly listed material enters an implementation handoff.

Initial capture: [selected LLM Wiki excerpts](public/2026-10-09-llm-wiki-excerpts.md).
Existing analysis intake: [Ableton analysis outputs](../wiki/research/sources/ableton-analysis-intake.md).
