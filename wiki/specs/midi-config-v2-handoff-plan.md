---
id: PLAN-MIDI-CONFIG-V2-HANDOFF
type: research
status: current
updated: 2026-10-17
access: analysis
target: Ableton Live 12 Suite 12.4.3 / macOS
---

# Second MIDI configuration handoff: candidate and review plan

## Decision and boundary

Stage a second finite candidate, midi-config-v2, from
[revision 2 of the MIDI specification](midi-user-mapping.md), with the same
structure and gates as the [first handoff plan](midi-config-handoff-plan.md).
The scope is the configuration-interpretation layer that the
[S4 closure assessment](../research/midi-closure-r2.md#clause-classification)
classifies as statically supportable. When published, the candidate supersedes
[midi-config-v1](../../handoff/midi-config-v1/README.md) as a strict superset;
v1 stays immutable and valid for its narrower scope.

This page is an analyst-side proposal. The candidate is **staged, not reviewed
and not released**. It is not an implementation input. No reference or
candidate execution has run and no compatibility is claimed.

## Scope

Every included clause is labeled S or D in the specification and was re-checked
against its listing before staging. The representation adds `section`,
`map_mode`, `button_kind`, `message_type: note` and `device_parameter_banks` to
the v1 assignment set.

| Requirement | Included in v2 | Excluded remainder |
| --- | --- | --- |
| REQ-MIDI-USER-001 | None | Discovery, naming, refresh (PRB-S4-01/02) |
| REQ-MIDI-USER-002 | Number enablement for all 103 CC keys and integer pad notes; integer text forms | Noninteger pad notes; interpolation (PRB-S4-03) |
| REQ-MIDI-USER-003 | Effective global channel; 27 per-control channel keys; global-only controls; pad channel rules | Noninteger pad channel after a valid note (PRB-S4-03) |
| REQ-MIDI-USER-004 | None | All value handling (S-cond; PRB-S4-06/07) |
| REQ-MIDI-USER-005 | Ten exact tokens, absent default, key scope, 14-bit label above CC 95 | Unknown tokens (PRB-S4-04); transforms (PRB-S4-05) |
| REQ-MIDI-USER-006 | Pad identity and documented grid position | Playback via host pad translation (PRB-S4-08) |
| REQ-MIDI-USER-007 | Encoder compaction to positions; span 1 or 2 | Parameter identity and bank contents (PRB-S4-09) |
| REQ-MIDI-USER-008 | Direct-bank selector compaction; named device button targets; momentary, global channel | Bank selection, navigation, lock, activator, status message (S-cond; PRB-S4-10) |
| REQ-MIDI-USER-009 | Strip and mixer-bank targets; `Send2Knob`*N* only with `Send1Knob`*N* valid | Lone `Send2Knob`*N* (new refinement, unreviewed); track ordering (PRB-S4-11); arm-select (S-cond) |
| REQ-MIDI-USER-010 | v1 targets plus `VolumeMapMode`/`CrossfaderMapMode` scope | Scaling, takeover (S-cond), smoothing (PRB-S4-05) |
| REQ-MIDI-USER-011 | Button kind from `MixerButtonsToggle`, Boolean spellings, absent = toggle | Value response, mute feedback and its default, eligibility (S-cond; PRB-S4-12/13); invalid Boolean (PRB-S4-03) |
| REQ-MIDI-USER-012 | 14 keys and targets; momentary; global channel; `FwdButton` not a key | Effects and timing (S-cond; PRB-S4-06/07) |
| REQ-MIDI-USER-013 | Option case, exact sections, `:`/`=`, full-line comments, trimming, empty values, `[DEFAULT]` into present sections, unknown and misplaced keys ignored | Duplicates, pre-section text, continuation lines, `%`, non-ASCII (PRB-S4-03/16) |

Explicit exclusions, stated in the candidate spec and manifest: every S-cond
clause; failed-parse outcomes; unknown map-mode tokens; MIDI address
collisions; non-ASCII or CR input; numeric transforms; feedback; lifecycle,
timing and teardown. The lone-`Send2Knob` case is also excluded because its
static derivation is new and unreviewed.

## Deliverables

The candidate is under `analysis/ableton-live-12.4.3/handoff-staging/`:

- [midi-config-v2/README.md](../../analysis/ableton-live-12.4.3/handoff-staging/midi-config-v2/README.md),
  `AGENTS.md`, `spec.md`, `cases.json` (109 cases), `fixtures/` (109 files) and
  a draft `manifest.json`. The manifest inventories 113 payload files; 114 with
  itself. Draft manifest SHA-256:
  `e1e74176c0030c0990d3bba59cb94b6e2dcd5be4d29bee26e1dc46b20cdd4994`. Review
  edits will change it.
- Analyst side, never shipped: `midi-config-v2-analysis/` with the builder
  [build_v2.py](../../analysis/ableton-live-12.4.3/handoff-staging/midi-config-v2-analysis/build_v2.py),
  the [cross-check model](../../analysis/ableton-live-12.4.3/handoff-staging/midi-config-v2-analysis/crosscheck_model.py),
  [traceability](../../analysis/ableton-live-12.4.3/handoff-staging/midi-config-v2-analysis/traceability.json)
  and the [author validation](../../analysis/ableton-live-12.4.3/handoff-staging/midi-config-v2-analysis/author-validation.json).

## Evidence traceability

This mapping stays on the analyst side; the payload contains no locator,
derivation field or analyst link.

| v2 cases | Source | Support |
| --- | --- | --- |
| MIDI-CONFIG-001–054 | midi-config-v1 cases of the same ID; fixture bytes identical | v1 release review; the added `section`, `map_mode: Absolute` and null span follow from E1/E2 and the explicit `Absolute` mode keys in each fixture |
| MIDI-CONFIG-055–109 | S4-MIDI-001–055 in order (S4-MIDI-*n* is MIDI-CONFIG-*n*+54) | S4 rule IDs per case in `traceability.json`, defined in the S4 draft `rules`; spec appendix E1–E9 gives the listings |
| MIDI-CONFIG-084 | S4-MIDI-030, corrected | The draft expected Send B for a lone `Send2Knob1`. Send knobs are compacted per strip and connected by position (E2 L272–302; E3 L299–319, L79–82), so the fixture now enables both knobs of strip 1 |

Purpose texts of S4-MIDI-011, 032 and 038 were reworded to remove template and
internal phrasing; their inputs and expectations are unchanged. Clause support:

| Clause | Evidence |
| --- | --- |
| Number enablement, integer text | E1 L56–66, L96, L197–200; E2 L24–25; E7; E8 (inferred 3.11.6) |
| Channels | E1 L125, L148–155, L182–184, L201–209, L227–242, L285–291; E2 L83–95, L136–155, L239–249, L274–283, L313–316, L368–378, L399–405 |
| Map-mode labels | E1 L17, L50–53, L170–171, L245–252; E2 L132–140, L188–212, L289–293; E6 |
| Pads | E1 L182–220; D3 |
| Encoder and bank-button compaction, span | E2 L339–388; E3 L33–43; E4 L15–18 |
| Targets and button kinds | E1 L159–178, L223–317; E2 L37–55, L129–137, L158–166, L218–224, L312–336, L398–420; D4–D7 |
| Lexical rules | E1 L146–283 (`has_section`); E7 L608–616, L890–904 |

## Mechanical checks performed

`build_v2.py seal`, run with CPython 3.11.13 `-I`, wrote the author validation:

- 109 cases; each fixture is ASCII with LF endings and a final newline, parses
  without error in the host 3.11.13 parser, which matches the shipped module for
  non-raising input, and has distinct MIDI addresses.
- The cross-check model, an independent re-reading of the listings as rules,
  agrees with all 109 expectations. Before the correction it disagreed only
  with S4-MIDI-030. It is not an oracle; it shares the static evidence.
- Hashes and sizes of all 113 listed files match. The inventory equals the
  directory. In a copy outside the checkout, all nine Markdown links and all 109
  case inputs resolve inside the package.
- Sanitization deny-list (analyst paths, internal module and function names,
  locators, bytecode terms, derivation fields, absolute paths): the only hit is
  the word "decompilation" in the forbidden-inputs list of `AGENTS.md`, the same
  wording as v1. No case carries derivation or digest fields.

Not checked: reference or candidate execution; an independent proof of any
expectation; the bytecode digest match to the revision 1 pins, which stays
unknown until roadmap gate G0.2. Bundle version and Live slice match.

## Review gates still required

1. **Scope review**, in a separate context: check every included clause against
   E1–E9. Give the new derivations particular attention: send position, pad
   channel rules, `[DEFAULT]` inheritance into present sections only, integer
   text grammar, the 14-bit label and both compactions. Confirm the
   MIDI-CONFIG-084 correction.
2. **Quality and sanitization review**: behavioral completeness, exclusions
   stated in both spec and manifest, no internal structure or analyst link, and
   no claim beyond static derivation.
3. **Evidence identity**: decide whether the S4 re-decode (same bundle version,
   matching Live slice and documents) suffices while the bytecode digest match
   is unknown, or whether G0.2 must close first.
4. **Fixture and sharing review** of the 55 new fixtures. They are authored
   text with three invented comment lines.
5. **Finalize**: add `REVIEW.md`; set the manifest review fields,
   `release_status` and `release_date`; re-run `seal`; verify hashes and links
   in an isolated export; record the manifest hash in the handoff catalog.
6. **Publish** only after approval: copy unchanged to `handoff/midi-config-v2/`;
   add a catalog row superseding midi-config-v1; update spec status, coverage,
   indexes and the log. Never edit midi-config-v1.
7. An isolated implementation workspace remains unprovisioned.

## Current disposition

Staged on 2026-10-17 and awaiting separate review. midi-config-v1 remains the
only released MIDI contract.
