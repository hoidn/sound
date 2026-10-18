---
id: RESEARCH-MIDI-CLOSURE-R2
type: research
status: draft
updated: 2026-10-17
access: analysis
target: Ableton Live 12 Suite 12.4.3
---

# MIDI user-mapping closure assessment (packet S4)

Bounded question from [roadmap revision 2](native-decompilation-roadmap.md#revision-2-proposal--2026-10-17):
which clauses of the 13-requirement [MIDI draft](../specs/midi-user-mapping.md),
beyond the four partial clauses released in [midi-config-v1](../../handoff/midi-config-v1/README.md),
are supportable from static evidence now? Method: re-establish the pinned
evidence on the Linux host, re-decode the bytecode, classify every clause, draft
cases for the supportable remainder and record runtime probes under
[ADR 0002](../decisions/adr-0002-static-first-analysis.md). Nothing was
imported or executed from the bundle and Live was not run.

**Answer.** The whole configuration-interpretation layer is statically
supportable: which configured key yields which MIDI address, channel, user
target, map-mode label and button kind, for every control and pad, and the INI
lexical rules that decide it. Handler semantics such as toggles, bank
navigation and mute behavior can be derived in Python, but they end in native
Live properties. Discovery, host error recovery, numeric transforms, pad
playback, feedback bytes, timing and lifecycle still need native tracing or a
probe on the macOS host.

## Evidence re-established

All artifacts are in the [S4 evidence directory](../../analysis/ableton-live-12.4.3/r2/s4-midi-v1/manifest.json),
whose manifest pins every file.

| Item | Result |
| --- | --- |
| `_Tools/UserConfiguration.txt`, `_Tools/InstantMappings-HowTo.txt` | **Match**: recomputed SHA-256 equal to the [source record](sources/midi-user-mapping-12.4.3.md) |
| 17 pinned bytecode modules + `_Framework/ControlSurface` (new) | Located. Current digests in [hashes.json](../../analysis/ableton-live-12.4.3/r2/s4-midi-v1/hashes.json). Recorded digests are **unknown**: they live only in the absent `midi-user-mapping-v1` manifests, so no match or mismatch is claimed |
| `Contents/MacOS/Live`, derived `Live.arm64` | Match the [installed-package record](sources/ableton-live-12.4.3.md) (`52289af6…`, `3a99ceea…`); `CFBundleVersion` = `12.4.3 (2026-07-07_e3d8be4d07)` |
| Decoder | `.pyc` magic `a70d0d0a` (3495, CPython 3.11). Re-decoded with CPython 3.11.13 `dis` from a uv install under `/var/tmp/sound-analysis/scratch/d-midi/` ([decode.py](../../analysis/ableton-live-12.4.3/r2/s4-midi-v1/decode.py)); `marshal.loads` only |
| Locator reproduction | Every offset/line cited in the draft appendix (parse_int 2–264, create_instance 180–266/1088–1432/2098–2286, parse_map_mode 46–164, `_init_device_component` 348–1322, `set_parameter_controls` 4–64, `_bank_value` 134–308, TransportComponent L63–81, ToggleComponent 2–244, MapMode L20–48) reappears in the new listings, for example [_UserScript/__init__](../../analysis/ableton-live-12.4.3/r2/s4-midi-v1/listings/_UserScript/__init__.dis.txt) |
| Embedded interpreter | Inferred **CPython 3.11.6**: the string `3.11.6` sits beside the `%.80s (%.80s) %.80s` version format in `Live.arm64` at file offset 95776493 ([native-anchors.json](../../analysis/ableton-live-12.4.3/r2/s4-midi-v1/native-anchors.json)) |
| Shipped `configparser` | Observed: with docstrings stripped, bytecode-identical to CPython 3.11.13 stdlib except `RawConfigParser._read`. There, 3.11.13 alone also joins multiline values in a `finally` block when parsing raises. Both versions raise the same exception, so the host stdlib is a valid lexical checker for non-raising input ([configparser-equivalence.json](../../analysis/ableton-live-12.4.3/r2/s4-midi-v1/configparser-equivalence.json)) |

Native string anchors, Observed in `Live.arm64` (adjacency only; these are
not call edges): `UserConfiguration.txt` beside `MidiRemoteScripts: Scanning for
scripts in folder ` (96219912), `UserScripts: ` and `HIDE_SCRIPT` (96220482),
`create_instance` beside `Script could not be loaded. The Package has no
'create_instance' function.` (96257008), and `OMidiPadTranslator.*` (96256736).

## Clause classification

Labels: **S** means supportable now as configuration interpretation, from
shipped documents, shipped bytecode and CPython 3.11 rules. **S-cond** means
the Python handler logic is derived, but the observable effect passes through
a named native property. **N** means blocked on native code. **R** means
blocked on runtime observation; the PRB IDs refer to the [probe batch](#phase-4-probe-batch).
Unless another module is named, line references point to the
`_UserScript/__init__` or `_Generic/GenericScript` listings.

| Req | S (supportable now) | S-cond | N / R |
| --- | --- | --- | --- |
| 001 | none observable (the `get_name_for_script` class-name rule, L30–47, is internal) | none | N: native script enumeration (anchors above). R: PRB-S4-01, 02 |
| 002 | CC 0–127 enable/disable for all 103 ordinary CC keys (parse_int L56–66; bound 128 at L96; call sites L148–317). Pad note 0–127 accepted; integer out of range omitted (L195–200). `int()` forms: `+20` and `0021` accepted, `1_0` read as 10, `0x14` and `20.0` disabled | none | Noninteger pad note and interpolation errors leave `create_instance`, which has no exception table. The host outcome is N (TMidiRemoteScript) and R: PRB-S4-03 |
| 003 | GlobalChannel valid else 0 (GenericScript L83–95). Per-control channel keys exist only for Encoder1–16, VolumeSlider1–8 and master/cue/crossfader. Every button, send knob and transport key uses the effective global channel. Pad channel rules L201–209, including: missing GlobalChannel key or absent `[Globals]` omits channel-less pads | none | Noninteger pad channel after a valid note: PRB-S4-03 |
| 004 | none | Positive = press, zero = release. Toggles invert on positive and ignore zero; Play/Stop set the state (ToggleComponent L93–100; TransportComponent L63–81) | N: Song property setters. R: PRB-S4-06, 07 |
| 005 | Ten exact, case-sensitive tokens (elements_base L27–47; dictcomp L17). An absent key gives Absolute (L51–53). Key scopes: Encoder, Volume (track/master/cue), Sends, Crossfader. `Absolute14Bit` becomes `Absolute` above CC95 (EncoderElement L27, L53–56) | none | An unknown token reaches native MidiMap as the string `'Absolute'` (L52): PRB-S4-04. Numeric transforms, 14-bit pairing and relative arithmetic: PRB-S4-05 |
| 006 | Pad *n* gives cell (col (n−1)%4, row (n−1)//4) with its note and channel (L210–213); geometry from D3 | none | N: `c_instance.set_pad_translation` (ControlSurface L372–373). R: PRB-S4-08 |
| 007 | Valid encoders are compacted in slot order (L366–388). A count above 8 gives a two-bank span (`_UserScript/DeviceComponent` L16) | none | Bank contents: a static lead (Python bank tables in `_Generic/Devices`, imported by `_Framework/DeviceComponent`) was **not traced**; name resolution is N. PRB-S4-09 is deferred |
| 008 | Direct-bank buttons compacted (L339–363) and named targets. All device buttons momentary on the global channel (L312–316) | Next-only wraps; Next+Prev steps. A bank is selected only if its index < bank count. OnOff inverts the activator value (DeviceComponent L380–388). Re-pressing the current bank shows "*device* Bank: *name*" (L407–408, new) | Bank count and lock (c_instance) are N. R: PRB-S4-10 |
| 009 | Target association for strips 1–8: volume, send A/B, mute, solo, select, arm, mixer bank next/prev (L272–317; GenericScript L218–302) | Arming a track that becomes armed also selects it when `select_instrument()` succeeds (SelectChanStripComponent L16–27, new) | Strip-to-track ordering, returns and groups: PRB-S4-11 |
| 010 | Released targets, plus mode scope: VolumeMapMode covers master and cue (make_mixer_encoder default L140); CrossfaderMapMode (L205–212). Crossfader takeover is disabled (L216; effect N) | none | Scaling and smoothing: PRB-S4-05 |
| 011 | Button kind: `MixerButtonsToggle` False gives momentary, True or absent gives toggle, including mixer bank buttons (L255–258; GenericScript L129–137, L218–224). Boolean spellings from configparser `BOOLEAN_STATES` | Momentary acts on nonzero values; toggle acts on every value (ChannelStripComponent `_mute_value` L367–370, `_select_value` L357–361). Mute does nothing on master. An absent `InvertMuteButtonFeedback` is True (L128–129); feedback can be lit only for regular and return tracks (L464–475) | Feedback bytes: PRB-S4-13. Exclusivity: PRB-S4-12. Invalid Boolean: PRB-S4-03 |
| 012 | 14 keys map to targets (GenericScript L37–55; L175–178). `FwdButton` is not a key. All transport buttons are momentary on the global channel (`NORELEASE` is never set, L409) | Play/stop/toggle logic as in REQ-004 | Effects and timing: PRB-S4-06, 07 |
| 013 | Option names are case-insensitive for every key. Section names are case-sensitive. Unknown keys are never queried. `=` and `:` delimit; full-line `#`/`;` are comments; inline comments stay in the value; empty values are disabled; values are trimmed; `[DEFAULT]` values are inherited (configparser L574–616). Duplicates, pre-section text and invalid Booleans raise out of `create_instance` | none | Host outcome of a raise: PRB-S4-03. File encoding: PRB-S4-16 |
| Timing, lifecycle, teardown | none | none | PRB-S4-14, 15 |

New observations relative to the draft, all static derivations and none
observed at runtime: the per-control channel limit, the pad behavior with a
missing GlobalChannel, mixer bank buttons following `MixerButtonsToggle`,
always-momentary transport buttons, the absent-feedback default, crossfader
takeover, arm-selects-track, the current-bank status message and the lexical
rules above.

## Draft cases for a v2 candidate

[draft-cases-v2.json](../../analysis/ableton-live-12.4.3/r2/s4-midi-v1/draft-cases-v2.json)
holds 55 cases (S4-MIDI-001–055) with independently authored ASCII fixtures,
built by [build_cases.py](../../analysis/ableton-live-12.4.3/r2/s4-midi-v1/build_cases.py).
They extend the v1 assignment set with `section`, `map_mode` (continuous
controls), `button_kind` (buttons), note-type pad assignments and a
`device_parameter_banks` field. Coverage: encoders, compaction and the ten
mode tokens (001–010), device buttons (011–014), mixer strips, sends, button
kinds and Boolean spellings (015–028), volume/crossfader mode scope (029–030),
transport (031–033), pads (034–041), lexical rules (042–054) and a noninteger
GlobalChannel (055). Expectations are hand-authored static
derivations, each with rule IDs mapped to locators. The script checks only
structure, ranges, address uniqueness and that host-stdlib configparser parses
every fixture with the expected integer text (0 problems). It is not an
oracle. Every case is unexecuted for both reference and candidate. Excluded:
raising inputs, unknown tokens, collisions, non-ASCII and every behavioral
transition.

Correction 2026-10-17: draft case S4-MIDI-030 expected a lone `Send2Knob1` to
target Send B. The spec revision 2 check found that send knobs are compacted per
strip and connected by position, so a lone Send2 knob reaches Send A. The v2
candidate excludes the lone-Send2 input and uses MIDI-CONFIG-084, which enables
both knobs of strip 1; see [spec revision 2](../specs/midi-user-mapping.md).

## Phase 4 probe batch

[probe-batch.json](../../analysis/ableton-live-12.4.3/r2/s4-midi-v1/probe-batch.json)
holds 16 records. Each lists the question, existing evidence, why static
evidence is insufficient, minimal input, discriminating observation and
stopping condition. All need the macOS host; the virtual MIDI port is
unverified.

| ID | Clause | Question |
| --- | --- | --- |
| PRB-S4-01/02 | 001 | Listing, displayed name, restart, name rules |
| PRB-S4-03 | 002c/d, 003e, 011b, 013d | Host outcome when `create_instance` raises |
| PRB-S4-04/05 | 005c/d, 010d | Unknown mode token; Absolute scaling |
| PRB-S4-06/07 | 004, 012 | Toggle/play/stop effects; seek, nudge and tap timing |
| PRB-S4-08 | 006 | Pad translation plays the documented visible pad |
| PRB-S4-09 | 007 | Device parameter addressing (deferred until `_Generic/Devices` is traced) |
| PRB-S4-10/11/12 | 008, 009, 011 | Bank navigation, lock, activator; strip ordering; toggle-on-zero, exclusivity, arm-select |
| PRB-S4-13 | 011e | Mute feedback bytes |
| PRB-S4-14/15/16 | Lifecycle, teardown, 013h | Reload, held controls at disconnect, file encoding |

## Limitations and next steps

The bytecode digest comparison with the v1 pins is unknown until the macOS
`analysis/` tree is restored (gate G0.2). Identity is otherwise established: the
midi-config-v2 review found that the pinned executable's code signature lists
`CodeResources` hashes matching all 18 decoded modules and both documents (RV2-06). Static paths are conditional on host initialization and
MIDI delivery. CPython `int()` behavior assumes the embedded 3.11.6 interpreter
is unmodified. S-cond clauses need a state-transition representation before any
release. The cheapest static follow-ups are `_Generic/Devices` (REQ-007) and
`_Framework/MixerComponent` track ordering (REQ-009), before PRB-S4-09/11.
Open questions remain in [Q-008–Q-010](../questions.md#q-008-midi-profile-parsing-and-host-errors).
