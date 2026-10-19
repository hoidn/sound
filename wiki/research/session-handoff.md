---
id: RESEARCH-SESSION-HANDOFF
type: research
status: active
updated: 2026-10-19
access: analysis
---

# Session handoff (2026-10-19)

A continuation note for the next analyst or maintainer session. It points to the
canonical pages and does not replace them. Replace this page when a later
session ends; do not keep competing copies.

## Read first

1. [Project status](../project.md), then the [gate table](native-phase-execution.md)
   (rows X1, X2, T1.1 to T1.7).
2. [Roadmap revision 3](native-decompilation-roadmap.md#revision-3--t1-completion-plan-2026-10-18),
   [ADR 0003](../decisions/adr-0003-no-reference-execution.md) and
   [ADR 0004](../decisions/adr-0004-target-scope-t1.md).
3. [Open questions](../questions.md) Q-001 to Q-026 and the [catalog](../../handoff/index.md).

## Repository state

- `main` is at f17c8d0 and is 29 commits ahead of `origin/main`. The origin
  (github.com/hoidn/sound) is **public**: push only when the user asks.
- `analysis/ableton-live-12.4.3/r2/n1-transport-state-v1/.entry-map.pickle`
  (11 MB) is deliberately untracked. Leave it uncommitted.
- `analysis/ableton-live-12.4.3/r2/t12-collision-v1/` is untracked. A Collision
  device-spec agent was still writing it when this note was made. If
  `wiki/specs/device-collision.md` and `wiki/research/device-collision-dsp.md`
  exist and the evidence manifest matches its files, commit all three. Add the spec
  and research index rows, a Q-025 progress line and a log entry, as for Electric,
  Tension and Analog. If they don't exist, the run did not finish.
- Persistent analysis state lives in `/var/tmp/sound-analysis`, outside the repo.
  The extracted-execution harness (`tools/xexec/`) builds to
  `/var/tmp/sound-analysis/xexec/xexec`. Harness limit: 256 calls per process.

## Standing constraints

- Static-first evidence. No whole-application reference run is possible, because
  Mac observation is impossible and the project finishes on this Linux x86_64 host.
  Gaps close by extracted execution (label X) or stay unknown (ADR 0003).
- Clean room: analyst contexts never implement. Released payloads are immutable;
  correct them by superseding releases.
- Get approval before installing tooling. An arm64 emulator needs its own approval.
- The user asked to save tokens: **do not dispatch new agent work without asking.**

## Decisions waiting on the user

| Decision | Options | Where |
| --- | --- | --- |
| Amp and Cabinet device audio | Approve CoreFoundation and Objective-C emulation plus a fake host identity; exclude them from T1; or specify them statically only | [Q-025](../questions.md#q-025-device-host-protocol-and-device-audio-acceptance) |
| T1.6 implementation workspace | A bwrap sandbox holding only the released handoffs and neutral governance (proposed) | Gate row T1.6 |

## Gate status (2026-10-19)

| Gate | State |
| --- | --- |
| X1, X2 | Passed |
| T1.1 structure, T1.3 playback core, T1.4 mix graph | Drafts done |
| T1.2 device audio | Feasibility passed. Drafts exist for Corpus, Electric, Tension and Analog; Collision is in progress; Amp and Cabinet wait on Q-025 |
| T1.5 releases | First round done: 23 releases, 13 current. playback-core-v1 is staged (`analysis/ableton-live-12.4.3/handoff-staging/`) but not reviewed. Device specs are unreleased |
| T1.6, T1.7 | Not started |

## Work queue (not dispatched)

In suggested order. Each item needs the user's go-ahead under the token constraint.

1. Commit the Collision outputs (see above).
2. Review the staged playback-core-v1, then publish it if it passes.
3. Run one spec-correction pass over the items below. The wiki spec revisions have
   not changed since these were recorded. For a family that has since been released,
   check the release review record first, because a release author may already have
   applied a correction in the staged copy.
4. Release the device specs (Corpus, Electric, Tension, Analog, then Collision).
5. Fix the t11 structure checker, which gives false results on the older 11.0_405
   fixture schema (`analysis/ableton-live-12.4.3/r2/t11-structure-v1/schema_check.py`).

## Pending spec corrections

These items came from reviews and authors in the 2026-10-18 round. They were kept
in session scratch and are copied here so they survive.

- **mixer-values r5:** Remove "bit-exact" from REQ-005, 011 and 015. The round trip
  is not exact between curve points: about half of random gains come back 1 to 3
  binary32 steps off. Make the same fix in MIX-GRAPH REQ-003 and Q-019. Also:
  - The snap rule feeds forward.
  - The REQ-013 w-mapping label is inconsistent.
  - MV-047 and MV-048 need absolute bounds; MV-048 confuses 1 ulp with a 6e-17
    cross-feed.
- **mix-graph r2:**
  - MG-008 internal checks, and the speaker type 4 contradiction.
  - REQ-003 and MG-029 keep an out-of-range volume assumption, but mixer REQ-015
    marks it U.
  - REQ-014: 32-bit overflow at r ≥ 2^31 (ramp 200).
  - The A4 and A7 labels are too broad; add A6 and A7 to Q-023.
  - REQ-013: the automation offset is untraced and needs a value step.
  - REQ-012: the one-event rule conflicts with the T11-MIN envelopes.
  - Review findings F1 to F3 and F6 are confirmed.
- **live-set-structure r2:**
  - Device-free T11-MIN: LSS-020 → 66; LSS-014 → 67, 68 and 69.
  - REQ-001: arrays, and the missing-Value rule needs a class schema.
  - REQ-009: codes 2 to 7.
  - REQ-018: track row, and its citations of unreleased parts.
  - LSS-004 send-holder order, LSS-005 stray SendPreBool, LSS-008 slot/scene count,
    LSS-029 tempo, LSS-035 relocation; basis A6 for LSS-001.
  - The source of the added send value, and the SendsPre count ambiguity.
  - The track rule is "audio, MIDI or group". Also state it in the plan and the
    catalog.
  - REQ-014 open condition.
- **automation-envelopes r5:**
  - A3 is stale. Is REQ-009 enablement settled?
  - REQ-005 and 007 omit the removal step on open: it removes clip envelopes with
    exactly one event, and Speaker, Pan and CrossFadeState envelopes with fewer
    than two.
  - The AEN-033 base fixture does not open.
  - "v1 not contradicted" is false.
  - The playback comparator ignores ramps.
  - SF-3 status.
- **transport-state r5:**
  - The spec page presents v2 without the fixture defect.
  - The case wording calls fixtures edits of shipped set B0.
  - The handoff section should name v3.
  - New REQ-012 evidence: on open, an envelope value replaces the tempo Manual value.
- **midi-note-storage r4:**
  - MNS-072 to 075 requirement IDs: 073 to 075 lack REQ-002, and 073 lacks REQ-004.
  - REQ-006 "on grid unchanged" conflicts with "−0 stored as +0", and the REQ-006
    and 007 wording is unchanged.
  - REQ-002: −0 reads as negative zero.
- **midi-user-mapping r6:**
  - 3.8τ → 96 to 408τ.
  - Two precision corrections from review RV4.
- **clip-launch r5:**
  - REQ-016's Global bullet is S, but PLAYBACK-CORE A4 differs.
  - REQ-011: out-of-range follow times are X, which contradicts A2 in r3.
  - The fixtures section uses edited shipped sets.
- **warp-markers r5:**
  - WMK-019 was never run, though r4 labels it X.
  - WMK-039 rounding.
  - The shadow formula has no observable case.
  - A1 is settled by structure A1.
  - REQ-002: duplicate marker Ids are refused.
  - REQ-009 is untestable outside playback.
- **playback-core r2:**
  - PBC-004 binary32 wording.
  - PBC-024 at 48 kHz.
  - PBC-023: launch on the note beat.
  - Linear tolerance near cancellation.
  - REQ-006: the jump rule is one sample.
  - REQ-021: the end sample with Fade off.
  - Q-024: StartRelative audio.
- **bundled-device-parameters r3:**
  - Electric REQ-005 settles the REQ-014 Polyphony labels.
  - The N5 `conversions.tsv` Volume default is 0.7047892213.
  - The t12 Electric probe peak is 0.296.
- **device-dsp-extracted (research):** corrections from Analog:
  - The activity flag spans 2 blocks.
  - C4 = 261.537 exactly.
  - The unseeded random LFO is X.
- **Leads to check:**
  - Does the note-storage integer converter, which accepts a leading '-', also back
    REQ-TRANSPORT-STATE-006?
  - The mixer research page's Phase 4 probes and Unknowns sections are stale under
    ADR 0003.
