---
id: RESEARCH-ABLETON-DECOMP-PREP
type: research
status: current
updated: 2026-10-09
access: analysis
target: Ableton Live 12 Suite 12.4.3
---

# Decompilation and specification preparation

The [package inventory](ableton-package-structure.md) is complete within its
static scope. The next phase should answer bounded feature questions using the
following retained inputs. This page is a research plan, not a behavioral spec.

For direct reading, use the [artifact catalog](artifacts/index.md): pseudocode,
assembly, call/string tables, symbol search and decoded Python modules.

The [next-phase roadmap](native-decompilation-roadmap.md) proposes main Live
pseudocode as the next concrete deliverable, alongside readable explanations of
the method and emerging structure. The feature priorities below guide semantic
investigation; they do not require delaying code export until all specs exist.

## Ready native inputs

Both arm64 copies are byte-identical slices of their original universal images;
see the [derivation manifest](../../analysis/ableton-live-12.4.3/derived/manifest.json).
REA [rejected explicit Ghidra selection](../../analysis/ableton-live-12.4.3/evidence/universal-ghidra-rejection.json)
on the universal app, then successfully
accepted the thin copies. [Live open evidence](../../analysis/ableton-live-12.4.3/evidence/live-thin-open.json)
proves target/provider validation only. The [authorized execution](native-phase-execution.md)
retains a full-analysis attempt stopped at the disk floor, followed by a
separate bounded selected-entry route that exported main Live pseudocode.
The [artifact catalog](artifacts/index.md) links the readable files; the
execution ledger now also records the successful full-analysis retry, its frozen
procedure inventory and default-profile export checkpoints. The selected route remains a
separate analysis profile.

The Push2 pipeline check completed Ghidra auto-analysis: 13,611 procedures and
14,769 defined strings. These are provider inventory counts, not original-source
function counts. `analyze_function` on entry `0x100006b10` produced 1,590 assembly
lines, 265 basic blocks, 77 callee records and 47 referenced strings. The
[dossier](../../analysis/ableton-live-12.4.3/evidence/push2-entry-dossier.json)
retains pseudocode, three inclusive function-body ranges and provider limitations.
Decompiler warnings include removed unreachable blocks and unsettled type
propagation. This proves the pipeline returns results; it does not prove source
recovery accuracy or establish the helper's complete behavior.

To resume the retained Push2 observations:

```json
{
  "path": "/Users/ollie/sound/analysis/ableton-live-12.4.3/derived/Push2DisplayProcess.arm64",
  "provider_id": "ghidra",
  "snapshot_path": "/Users/ollie/sound/analysis/ableton-live-12.4.3/evidence/push2-analysis-snapshot.json"
}
```

Pass this to `open_binary`. The snapshot preserves eligible query results, not
a full Ghidra project; new uncached deep queries may need fresh auto-analysis.
For Live, open `derived/Live.arm64` with `provider_id: ghidra`, then query specific
symbols/functions. Reuse the [symbol TSV](../../analysis/ableton-live-12.4.3/live-arm64-symbols.tsv)
before broad search. Candidate arm64 static virtual addresses include:

| Question seed | Symbol | Address |
| --- | --- | --- |
| Transport object setup | `TPtr<ACompound> SNewCompound<ATransport>()` | `0x10275dc64` |
| Audio clip object setup | `TPtr<ACompound> SNewCompound<AAudioClip>()` | `0x1027aff04` |
| Song object setup | `TPtr<ACompound> SNewCompound<ASongAgent>()` | `0x10269c558` |
| Device object setup | `TPtr<ACompound> SNewCompound<ADeviceUnit>()` | `0x1024a6e78` |

These MACH export names identify candidate factories, not scheduler entry points
or validated ownership relationships. Resolve each in Ghidra, inspect its actual
callers/data references, and trace only the remaining question. Runtime addresses
must account for ASLR. Never reuse addresses across architectures/builds.

## Proposed first specification work

The first MIDI mapping task now has a [reviewed analyst draft](../specs/midi-user-mapping.md)
and [retained static traces](midi-user-mapping.md). It has not been released as a
handoff or executed against the reference. The table retains the original
priority order; the MIDI row is ongoing bounded coverage, not untouched work.

Follow [ADR 0002](../decisions/adr-0002-static-first-analysis.md). The cases below
are contract/acceptance coverage to derive from static evidence first, not a
mandatory list of original-program executions before drafting or release. Use
targeted probes for unresolved material behavior; measured compatibility remains
a separate verification obligation.

| Priority / feature | Evidence to start from | Observable cases to specify |
| --- | --- | --- |
| 1: FEAT-ECOSYSTEM, MIDI user mapping | `_Tools/UserConfiguration.txt` lines 5–46 and `InstantMappings-HowTo.txt` lines 13–22; hashes in resource evidence | Channel/CC/note bounds, `-1` fallback, momentary press/release, every mapping mode, malformed/missing/duplicate values, setup naming and restart behavior |
| 2: FEAT-PERSISTENCE / FEAT-TRANSPORT | Schema `LiveSet`, `Transport`, `AudioClip`, `MidiClip`; default ALS and sampled ALC | Minimal create/save/reopen, tempo/loop units, enum meanings, missing media, malformed and unknown fields, old-version migration, cancellation and recovery |
| 3: FEAT-SESSION / FEAT-MIDI | `FollowAction`, `MidiNoteEvent`, `QuantizeAlgorithm`; Push2 `Quantization.qml` | Launch boundaries, stop/relaunch, note end state, recording and undo, zero/full quantize amount, swing bounds, tempo changes; measure event timing |
| 4: FEAT-DEVICES / FEAT-AUDIO | `Utility/Mono.adv` stored control values | State load/save, mono/stereo routing, channel impulse and anti-phase inputs, gain behavior, bypass and automation; define audio tolerances before comparison |
| 5: FEAT-ECOSYSTEM / FEAT-UI | Push2 QML and native helper dossier | Model-to-display mappings, selection, percent formatting, disconnect/reconnect, teardown; hardware availability remains unestablished |
| 6: FEAT-PERSISTENCE | Sample ASCL text and SQLite resource-map schema | Valid/invalid tuning, boundary pitches, metadata preservation, resource collisions and missing references |

This order prioritizes an external documented interface and small persistence
cases. Whole-app planning remains in the [feature map](../specs/feature-map.md);
the proposed integrated musical workflow in the [investigation plan](ableton-plan.md)
remains a later milestone. Support expected outputs with a precise shipped
contract, sufficiently traced static derivation, or controlled observation;
label the evidence type and its limits. Do not silently turn a proposed test
case into an established expected output.

For each bounded spec, assign requirement IDs and state inputs, preconditions,
outputs, state transitions, errors, timing, persistence and undo. Preserve raw
reference fixtures and build hashes. Separate observed facts, inference and
unknowns in its analysis appendix. Review observable requirements through the
[handoff workflow](../workflows.md#release-a-handoff) before implementation.
Original code, pseudocode, internal identifiers and these analyst notes remain
outside a released behavioral handoff.

## Unresolved preparation boundaries

- Core Live's 149.7 MB arm64 slice is undergoing default auto-analysis;
  provider throughput and full-binary decompilation coverage remain unknown.
- Seventeen MIDI-related Python modules have been decoded in the
  [follow-up investigation](midi-user-mapping.md); remaining module behavior and
  proprietary ALP/AGR formats remain unresolved.
- Dylib resolution was a static model with partial coverage, not observed loading.
- No UI/audio/MIDI execution, controlled scenarios or compatibility checks ran.
- User configuration, external packs/plugins and user libraries are outside this pass.

Track these in [open questions](../questions.md) and
[verification coverage](../verification/coverage.md). Earlier preparation sessions
were closed; the current owned session is tracked in the execution ledger.
