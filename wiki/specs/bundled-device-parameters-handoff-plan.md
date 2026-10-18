---
id: PLAN-BUNDLED-DEVICE-PARAMETERS-HANDOFF
type: research
status: current
updated: 2026-10-18
access: analysis
target: Ableton Live 12 Suite 12.4.3 / macOS
---

# Bundled device parameters handoff: candidate and review plan

## Review outcome

Released 2026-10-18 as [bundled-device-parameters-v1](../../handoff/bundled-device-parameters-v1/README.md),
approved with two narrowings by a separate review agent
([review record](../../handoff/bundled-device-parameters-v1/REVIEW.md)); manifest SHA-256
`02927f0ec9ca68a7810f863a264c3d6de3607730d06c2b867a1e0369618b4f8e`. All 82 cases are
kept. RVB-01: the build shows Cabinet `MicrophoneTypeSwitch` as Dynamic for true and
Condenser for false, which is the reverse of the candidate. Its labels are excluded from REQ-014 and
from cases 004 and 070 to 074. RVB-02: 30 graded value entries for the nine Corpus
and Collision position parameters were removed. Their table rows stay, marked
"position". For the draft spec: fix the switch label order in REQ-014 (the N5
research page's Cabinet default "Dynamic" has the same error); the Amp and Cabinet
`DryWet` range is traced, 0..1. The author's three findings are confirmed, and none
reaches a case: the stored-field claims in REQ-011, the Corpus side-chain list and
the inexact labels.

## Decision and boundary

Stage a finite candidate, bundled-device-parameters-v1, from
[SPEC-BUNDLED-DEVICE-PARAMETERS revision 1](bundled-device-parameters.md). It
follows the pattern and gates of the [als-container plan](als-container-handoff-plan.md),
the [transport-state plan](transport-state-handoff-plan.md) and the
[release workflow](../workflows.md#release-a-handoff). Under
[ADR 0002](../decisions/adr-0002-static-first-analysis.md#specification-and-verification-boundary)
every expectation is documented (shipped bytes) or static-derived; nothing was
executed.

The scope is the load side of one document kind: the decoded XML of a device
preset (`.adv`) holding one of the seven devices. The candidate releases the
parameter tables of all seven devices (paths, kinds, domains, whole-number
parameters, plain fields, document order), the parameter element shape, the
value text read on open, duplicate and unknown elements, and the labels of
eight parameters. It leaves out every clause that depends on an open question:
the device create path on load and new-instance defaults
([Q-006](../questions.md#q-006-native-analysis-and-resource-decoding)), the
position contradiction (P4-N5-01, P4-N6-01), out-of-range handling (P4-H4-02)
and save output (P4-H4-01).

This page is the analyst-side plan and traceability record, not an
implementation input. The candidate is **unreviewed and unpublished**. No
reference or candidate execution has run, and no compatibility is claimed.

## Scope

Outcomes are `opens` or `refused`; `state` judges the values read on open and
`labels` the displayed label text. Refusal classes and presentation are never
graded.

| Requirement | Included | Excluded remainder |
| --- | --- | --- |
| 001 | Seven element names; in `.adv` the device element is the root's only child | Placement in `.adg`, `.als`, `.alc` (no exact path; containers outside scope); save placement (U) |
| 002 | Member set and document order per device and group (D); duplicate parameter, group or `Manual` refused (S); repeated attribute refused | Save order and omissions (P4-H4-01); runtime-only members (internal names, not stated); duplicate plain fields and other parameter children |
| 003 | Float, Enum, Bool shapes; `LockEnvelope`; fixture form (`LomId` 0, range = domain, thresholds 64/127) | `KeyMidi` (moved with 013) |
| 004 | Float, Enum and Bool `Manual` text rules as narrowed in transport-state-v1 (REQ-004/005, 006, 003) | `0x`, `inf`, `nan`, `Invalid`, `#`, non-space leading whitespace; Enum both-sides decoration, `+` with trailing spaces, `-`, long text ending in a space |
| 005 | None | All of it: whether and where 12.4.3 writes each parameter is P4-H4-01; the task scope excludes save output |
| 006 | Domains of the tables (D); in-domain values are the values read | Narrower stored ranges, out-of-range values (P4-H4-02) |
| 007 | Whole-number marks; documents hold whole numbers | Fractional values (S(A1) and U parts) |
| 008 | None | All of it: the "default when absent" values rest on A1, the untraced create path (Q-006) |
| 009 | None | All of it (P4-H4-03, P4-N5-03); the shipped Defaults presets are not used |
| 010 | None | All of it (P4-H4-02, PRB-N1-06) |
| 011 | Unknown child of device, group or parameter skipped with content (S); documented plain field values (D) | "Not written on save"; meaning of plain fields; unknown attributes |
| 012 | `Id` present; `.adv` stores 0 (D) | Assignment rule on save (P4-H4-01); nonzero Ids |
| 013 | None | All of it (meaning U; racks and sets outside scope) |
| 014 | Amp `AmpType`; Cabinet `CabinetType`, `MicrophonePosition`, `MicrophoneTypeSwitch`; Electric `PickupModel`; Corpus `ResonanceType`, `ResonatorQuality`, `MidiMode` (S, A3 stated) | Electric `Polyphony` (finding F4); Corpus `LfoType`, `LfoSync`, `LfoStereoMode` (F5); Analog, Tension, Collision (P4-H4-04) |
| 015 | None as a requirement; the six position parameters keep their table rows (path, Float, 0..1) | Which part of the position range the stored value covers (P4-N5-01, P4-N6-01) |

Released partial requirements: 001, 002, 003, 004, 006, 007, 011, 012, 014.
Unreleased: 005, 008, 009, 010, 013, 015.

### Case disposition

| Draft case | Candidate | Change |
| --- | --- | --- |
| BDP-001 | 001–021 | Replaced: an authored complete preset per device with values inside every domain, at every lower bound and at every upper bound, instead of the shipped F1–F7 |
| BDP-002, 003, 031, 032 | Not released | Save output |
| BDP-004, 005, 007 | 022, 028 and the other positive Float cases | Narrowed to the value read on open; moved from Amp `Bass` to Electric `KeyboardStretch` |
| BDP-006 | 032 | Moved to Electric `KeyboardStretch` |
| BDP-008, 009 | 051, 049 | 009 narrowed to the value read |
| BDP-010, 011 | 043, 044 | Moved to Cabinet `CabinetType` |
| BDP-012 | 055 | Moved to Cabinet `CabinetType` |
| BDP-013 | 002, 003, 005, 006 and the other bound cases | Narrowed to the value read |
| BDP-014–017, 028 | Not released | REQ-010, REQ-007 fractional |
| BDP-018–027 | Not released | REQ-008 (A1) |
| BDP-029, 030 | 060, 061 | Narrowed to the values read; 030 moved to Electric |
| BDP-033, 034, 037 | Not released | U |
| BDP-035, 036 | 067, 081 | Authored fixtures instead of F5 and F7 |

The other cases are new and each exercises a D or S clause of the draft that
had no case: the Float, Enum and Bool text forms of REQ-004, duplicate `Manual`,
group parameter and group (056–058), the repeated attribute (059), unknown
elements in a group and before the first member (062, 063), and
the remaining label values (064–082 except the two above). The mid-value
complete cases of the four labelled devices also carry labels.

## Findings while staging

Proposed corrections for a spec revision 2; this page does not edit the spec.

- **F1.** REQ-011 S lists Collision `PitchBendRangeRelativePosition` and
  `Lfo1`/`Lfo2` `SyncRateRelative` among the constructor-set plain fields "with
  the same values" as shipped content. They are set by the constructors
  (N6 `out/nonparam_fields.tsv`) but are not stored members of `12.0_12402`
  (H4 `out/schema_devices.json`); Collision stores only
  `Resonator1/2/TransposeRelativePosition` and `CurrentTab`.
- **F2.** REQ-011 D, Corpus side-chain routing, omits
  `SideChain/RoutedInput/Routable/LowerDisplayString` (`""`) and
  `Routable/MpePitchBendUsesTuning` (`true`) (H4 `out/fields.json`).
- **F3.** The draft tables group instances as `{1,2}` rows and leave out the
  plain fields, so they do not show the document order that REQ-002 states.
  The candidate lists every member in document order, checked against all 268
  shipped `.adv` that hold these devices. Classes, domains and integer steps
  of all 502 parameters agree with the draft tables (0 differences).
- **F4.** REQ-014 "Electric `Polyphony`: 2 to 32 voices" is not an exact label
  list: the constructor (`FUN_1030e9578`) passes labels `2` … `32` and a separate
  `Voices` string, and the displayed text is not established. Excluded.
- **F5.** For Corpus `LfoType`, `LfoSync` and `LfoStereoMode` the constructor
  `FUN_1030e3830` holds a second name list after the labels (`ModulationSine` …,
  `ModulationHertz`/`ModulationBeat`, `Phi`/`Spin`), which suggests icons or
  short names in the user interface. A3 is weaker for them. Excluded.
- **F6.** The [device tables](../research/device-tables-native.md#load-handling)
  page says every device class uses the generic member loader, but N6
  `out/loader_slots.txt` reads "typeinfo name not found once" for `AAmp`. The
  claim holds: `SNewCompound<AAmp>` (`0x1030b42e8`) calls `FUN_1030b4934`,
  which stores vtable `0x1068bff78`; its `+0x140` is `0x101487310` and `+0xd0`
  is `0x1023a3b14`, as for the other devices (read 2026-10-18 with N6
  `extract_nested.Image` on `Live.arm64`). The research page should cite this.
- **F7.** REQ-002 "holds the shared device envelope" (21 schema fields): all
  268 shipped `.adv` omit `RemoteSelectionKeyMidi`, so documents carry 20 of
  them. Not material here; the candidate leaves the shared members out.
- **F8.** REQ-006 D's narrower stored ranges do not occur in `.adv`: all 28,116
  parameter instances in the 268 presets store exactly the domain.

## Deliverables

- Payload: [bundled-device-parameters-v1/README.md](../../analysis/ableton-live-12.4.3/handoff-staging/bundled-device-parameters-v1/README.md),
  `AGENTS.md`, `spec.md` (contract, generated parameter tables, comparison
  convention), `cases.json` (82 cases), `fixtures/` (82 files, 1.2 MB, 1.7 to
  68 KB each) and a draft `manifest.json` (`release_status:
  candidate-unreviewed`, review pending). The manifest lists 86 payload files;
  with itself the package has 87. Draft manifest SHA-256:
  `a5783931f7ef2c34a8388597eda745d94bfff3c5935356c62c0d8e3df366c8a9`. Review
  edits will change it.
- Analyst side, never shipped: `bundled-device-parameters-v1-analysis/` with
  [build_bdp.py](../../analysis/ableton-live-12.4.3/handoff-staging/bundled-device-parameters-v1-analysis/build_bdp.py)
  (`build`, `seal`, `verify`), `cases.py` (case table, exclusions, manifest
  metadata), `crosscheck_model.py` (independent reader of the payload),
  `trace.py` (shipped re-check, draft cross-check, traceability),
  [traceability.json](../../analysis/ableton-live-12.4.3/handoff-staging/bundled-device-parameters-v1-analysis/traceability.json)
  and [author-validation.json](../../analysis/ableton-live-12.4.3/handoff-staging/bundled-device-parameters-v1-analysis/author-validation.json).

## Evidence traceability

Evidence is H4 [h4-devices-v1](../../analysis/ableton-live-12.4.3/r2/h4-devices-v1/manifest.json),
N5 [n5-device-mapping-v1](../../analysis/ableton-live-12.4.3/r2/n5-device-mapping-v1/manifest.json),
N6 [n6-device-tables-v1](../../analysis/ableton-live-12.4.3/r2/n6-device-tables-v1/manifest.json)
and the N1 [transport-state native](../research/transport-state-native.md)
reading rules, with `Live.arm64` `3a99ceea…d1c383cfad`. The seal step re-hashes
eight evidence inputs, including `Live.arm64`, against their run manifests (all
match). Per-case
sources, evidence keys and inferred links are in `traceability.json`; the
payload contains none of them.

| Clause | Kept evidence | Inferred links |
| --- | --- | --- |
| 001 names, placement | H4 `out/occurrences.jsonl`, `out/scan.json`; seal re-check of 268 `.adv` | none |
| 002 members, order | H4 `out/schema_devices.json` `current`, `out/params.json`; re-check of order in 268 `.adv` | none |
| 002 duplicates | N1 add slot `0x101472624` (n1-0007), corrupt-document key `0x10148229c` | I1 |
| 003, 012 shape, Ids | H4 `out/param_table.tsv`, `params.json` `AutomationTarget.IdIsZero.adv`; re-check: `LomId`, Ids and `LockEnvelope` 0, thresholds 64/127 | none |
| 004 text | N1 n1-0006 `0x10152bfb8` (float: strtod then `(float)`; bool branch), `0x1002fd908` and the converter `0x1002fda78` confirmed in the transport-state-v1 review; Enum `Manual` is the time-signature `Manual` class (`ATimeableEnum`) | I1 (refusals) |
| 006 domains, value read | H4 `param_table.tsv` range column, `checks.txt`; N5 and N6 constructor ranges equal 370 of 372 Float domains and the 11 Enum domains of Amp, Cabinet, Electric and Corpus; the other 59 Enum domains (Analog, Tension, Collision) are D only (N6's Enum internal range is copied from the stored range). N6 `out/loader_slots.txt` and F6: generic loader, Enum index stored directly, no range check | I2, I3 |
| 007 whole numbers | N5 `out/conversions.tsv` (`legacyint`, `quantizing`), N6 `out/conversions.tsv` (`legacyint(…)`, `quantizing(…)`); exactly 28 | none |
| 011 unknown, plain | N1 `0x1015299e0` skip and `0x101453aac` record (not thrown); transport-state-v1 review (TS-016); H4 `out/fields.json`; re-check of plain values | I6 |
| 014 labels | N5 `out/conversions.tsv` labels; string order re-read 2026-10-18 in `FUN_1030b4934`, `FUN_1030c9c90`, `FUN_1030e9578`, `FUN_1030e277c` (corpus `chunk-02345`, `02350`, `02352`, `02351`) | I4 |

| Link | Inference not established by kept evidence | Affects |
| --- | --- | --- |
| I1 | A read error anywhere in a device preset stops the preset from opening. The preset open command and its catch are untraced; the reader is the Live Set reader, whose catch the als-container-v1 review confirmed (RVA-01) | Every refused case |
| I2 | The root-position device element is created through its class by name and read by the generic member reader. With every member present, the untraced create path (Q-006, A1) cannot change a value read | Every opening case |
| I3 | No device-level post-load step changes a value read. The device post-load `0x1023a3b14` calls `0x10248857c` and resets `+0x1cc` from INT_MIN to 0; it was traced one level only | Every opening case |
| I4 | The REQ-014 label lists are the texts the user interface shows (A3) | Label cases |
| I5 | The absence of the members shared by all devices does not change a judged outcome. The comparison obligation inserts them for the reference | Every case |
| I6 | No class involved registers a member named `Foo` | 060–063 |

## Fixture construction and sanitization

`build_bdp.py build` writes every fixture from the payload tables: the XML
declaration, the root with exactly `MajorVersion="5"`,
`MinorVersion="12.0_12402"` and `SchemaChangeCount="1"`, and the device element
with every member in document order and the fixture form, two-space
indentation, ASCII, LF. Values are computed (quarter point, Enum
`ceil(max/2)`, alternating Bools; or every bound); plain fields hold the modal
shipped texts. They equal every plain value in the 268 shipped `.adv`; the
three outliers H4 lists (two Tension, one Collision) occur in other document
kinds. No shipped file is read by `build`; the Defaults presets
and F1–F7 are not used. The seal-time re-check reads the shipped `.adv`
read-only and copies nothing.

The payload names device element and parameter names, domains and eight label
lists as behavioral facts. It contains no addresses, internal class or
function names, schema class names (`Timeable…`), engine or bundle terms,
probe or question IDs, shipped file paths or analyst links. Shared device
members are described, not named.

## Mechanical checks performed

`build_bdp.py seal` (CPython 3.13.9 `-I`) wrote the author validation:

- The cross-check model reads only the payload's `spec.md` (device table,
  parameter tables, label lists) and the fixtures. It agrees with all 82
  expectations. Five mutated expectations were each detected, and 21 excluded
  inputs (excluded text forms, out-of-range and fractional values, missing
  `Manual` or `Value`, `KeyMidi`, Id 7, a narrower range, an unknown name other
  than `Foo`, another plain value) each had no expectation in the model. The
  model shares the static evidence and is not an oracle.
- Shipped re-check: 268 `.adv`, 28,116 parameter instances; 0 failures in
  placement, member order, element shape, fixture form, plain values, Bool
  text, domain and whole-number values.
- Draft cross-check: 0 differences in class, domain and integer steps for 502
  parameters.
- Fixtures are distinct, ASCII with LF endings, no tabs and a final newline.
  Hashes and sizes of the 86 listed files match; the inventory equals the
  directory; all case inputs exist; no symlinks.
- The deny list (analyst paths, addresses, internal and schema class names,
  tool and derivation terms, probe, question, assumption and draft case IDs,
  shipped paths and preset names, corpus counts) has no hit except
  "decompil" in the forbidden-inputs list of `AGENTS.md`, worded as in the
  released packages. A copy with planted terms was flagged.
- In the export copy
  `/tmp/claude-1000/-home-ollie-Documents-sound/5c433942-c5e3-420d-833a-756602393383/scratchpad/bdp/export/`,
  `verify` matched all 86 hashes and resolved all 10 Markdown links inside the
  package, and the copy was byte-identical to staging. An independent hash
  recheck matched as well.

Not checked: any reference or candidate execution, and any proof of I1 to I6.

## Review gates still required

1. **Scope review** in a separate context. Check every included clause and the
   82 expectations against the locators. Rule on I1 to I6, on releasing the
   parameter tables while excluding defaults (I2's argument that complete
   fixtures make the create path irrelevant), on F4 and F5, and on keeping the
   position parameters' rows with REQ-015 unreleased.
2. **Quality and sanitization review**: behavioral completeness, exclusions
   identical in `spec.md` and the manifest, no internal structure or analyst
   link, no claim beyond documented or static-derived. Confirm that the
   comparison obligation (inserting shared members, a stored-number channel)
   is usable without analyst material.
3. **Evidence identity**: the H4, N5, N6 and `Live.arm64` hashes matched on
   2026-10-18; re-check before release.
4. **Fixture and sharing review** of the 82 authored presets, including the
   documented plain texts (`MidiIn/None`, `No Output`) and the package size.
5. **Finalize**: add `REVIEW.md`; set the manifest review fields,
   `release_status` and `release_date`; re-run `seal`; verify an isolated
   export; record the manifest hash in the handoff catalog.
6. **Publish** only after approval: copy unchanged to
   `handoff/bundled-device-parameters-v1/`, then update the catalog, spec
   status, coverage, indexes and log, and carry F1 to F8 into revision 2.
7. An isolated implementation workspace remains unprovisioned.

## Current disposition

Staged on 2026-10-18 as an unreviewed candidate: 82 cases, partial
REQ-BUNDLED-DEVICE-PARAMETERS-001 to 004, 006, 007, 011, 012 and 014, with 005,
008, 009, 010, 013 and 015 unreleased. It is not published, and no handoff
exists for SPEC-BUNDLED-DEVICE-PARAMETERS. This page has no catalog link yet;
the spec index was left unchanged as the staging brief requires.
