---
id: ADR-0004
type: decision
status: adopted
updated: 2026-10-18
access: neutral
---

# ADR 0004: First completion target T1

## Decision and authority

Adopted by user direction on 2026-10-18 ("proceed"), accepting the coordinator's
recommendation. A reimplementation of all of Live is not a realistic target, so the project
completes a bounded target, T1, first. This answers
[Q-001](../questions.md#q-001-compatibility-targets) for T1 only.

## T1 scope

The candidate runs on Linux x86_64 ([ADR 0003](adr-0003-no-reference-execution.md)).

- **Live Set files.** Open and save Live Sets whose content lies in T1. That content is
  tracks (MIDI, audio, return, main), mixer values, session clip slots and scenes, MIDI
  clips with notes, audio clips with sample references and warp markers, automation
  envelopes on mixer and device parameters, transport values, and device chains of the
  seven bundled devices. The candidate's handling of content outside T1 is its own design
  choice and carries no compatibility claim.
- **Playback, verified as an offline render.** From a Live Set and a script of transport
  and launch actions, render the output audio deterministically. This covers:
  - transport play, stop, loop and tempo;
  - session clip launch with quantization (Trigger launch mode);
  - MIDI clip notes driving instruments;
  - audio clip playback with warping off;
  - mixer volume, pan, sends and returns, crossfader, mute and solo;
  - automation applied during playback;
  - the seven bundled devices: Amp, Cabinet and Corpus as effects; Analog, Tension,
    Collision and Electric as instruments.
- **Control.** MIDI controller mapping as released in midi-config.
- **Already specified and kept.** Browser tag sidecars, plug-in folder discovery and the
  container and version check.

Out of T1:
- Arrangement View, recording, editing commands and undo;
- warp modes that stretch audio, and launch modes other than Trigger;
- follow-action timing;
- native Live devices outside the seven bundles, racks and plug-in hosting beyond discovery;
- Push, Link, Max for Live, and UI beyond what the above needs;
- real-time latency and jitter.

## Acceptance dimensions for T1

| Dimension | Criterion |
| --- | --- |
| Files | The T1 fields mean the same after open and after open-then-save. Exact text only where a spec requires it, such as number text |
| Values | Exact, or within the tolerance stated by the requirement |
| Device audio | For a given input and parameter set, the candidate's device output matches a reference render made by extracted execution of the original x86_64 device code, within the metric each device spec states |
| Timing | Launch and note positions are sample-exact at the stated sample rate, as each spec's arithmetic gives them |
| Whole-mix audio | Composed from verified parts as the playback specs state. No render of Live itself exists to compare against, so whole-mix results are spec conformance, not measured compatibility |

## Consequences

- Specification work targets the gaps that T1 needs (see
  [roadmap revision 3](../research/native-decompilation-roadmap.md#revision-3--t1-completion-plan-2026-10-18)).
  Families outside T1 stay at their current drafts.
- Device behavior is specified from extracted execution of the device bundles' own x86_64
  slices, plus documented behavior. Handoffs carry behavioral descriptions and reference
  renders, never recovered code.
- Implementation still needs a separately restricted workspace (ADR 0001, AGENTS.md).
