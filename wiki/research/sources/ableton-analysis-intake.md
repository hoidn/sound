---
id: SRC-ABLETON-ANALYSIS-INTAKE
type: source
status: superseded
updated: 2026-10-09
access: analysis
---

# Existing Ableton analysis outputs

Current identity, retained evidence, and limitations are cataloged in
[the installed Ableton source](ableton-live-12.4.3.md). This page preserves the
initial intake scope and checksums; use that source page for current synthesis.

Local original-side analysis files appeared while the documentation system was
being established. This page registers their location and current review scope.
It does not certify the results or imply that this task ran the underlying tools.

## Provenance and retention

- Location: `analysis/ableton-live-12.4.3/` in this workspace.
- Producer/session: not independently established during intake.
- Intake date: 2026-10-09.
- Access: analyst-only; the entire generated analysis tree is Git-ignored.
- Retention: local files only; backup/long-term retention is unresolved.
- Source manifests sampled during intake: see the checksum table below.

## Inventory and inspection scope

| Material | Locator within the analysis directory | Intake scope |
| --- | --- | --- |
| Derived executable manifest | `derived/manifest.json` | Read; records original/derived paths, hashes, ARM64 extraction commands, and evidence linkage |
| Native/package summary | `native-summary.json` | Read for target identity and summary structure; conclusions not independently audited |
| REA and host environment | `evidence/rea-session-environment.json`, `evidence/host-environment.json` | Presence observed; not reviewed |
| Static/package evidence | `evidence/static-evidence.json`, `evidence/package-evidence.json` | Presence observed; not reviewed |
| Decompilation and helper evidence | `evidence/decompilation-evidence.json`, `evidence/push2-entry-dossier.json`, `evidence/push2-analysis-snapshot.json` | Presence observed; not reviewed |
| Tool limitations | `evidence/tool-limitations.json` | Presence observed; must be read before adopting tool-result claims |
| Other derived analysis | `native-targets.json`, `dylib-resolution.json`, `resource-analysis.json`, `resource-findings.txt`, `live-arm64-symbols.tsv` | Presence observed; not reviewed |

The manifest records an ARM64 `Live.arm64` derived from the installed Live
executable and a separate Push 2 helper slice. The native summary records the
reference version as `12.4.3 (2026-07-07_e3d8be4d07)`. These are observations of
the manifest/summary contents, not independent validation of the binary bytes.

## Next ingestion

Validate artifact identities against the retained evidence, read limitations,
pin the producing tool versions, and reconcile the results into canonical
research pages. Preserve observations, inferences, and unknowns separately.
Do not ingest decompiled content into an implementation handoff.

Affected records: [investigation plan](../ableton-plan.md),
[Q-002](../../questions.md#q-002-durable-reference-identity),
[source catalog](../index.md).

## Intake checksum record

The following values identify the two files sampled during documentation intake.
If later analysis changes them, retain the old evidence or mark this intake stale
and record a new revision. A digest records identity, not correctness.

| File | SHA-256 |
| --- | --- |
| `derived/manifest.json` | `b3839d18d65ec91dd1c04d1ee9048a38a74e7a9f30cd9b9481efdaebb19a95e3` |
| `native-summary.json` | `5bbd30b17acf78eced2ba6c0b01da4b888c0b173ea9133b040d66b54d60bc4a2` |
