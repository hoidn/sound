---
id: SPEC-APC-CONTROLLER-CAPABILITIES
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3 installed startup-byte identity; controller/runtime applicability U
---

# APC controller startup declaration capabilities

## Scope and strength

This bounded F-08 analyst draft records eight selected APC-family startup
identity/port/auto-load declaration roles from exact installed 12.4.3 bytes.
It is not a complete controller profile, runtime/startup contract, supported
hardware matrix or released implementation input. [Research](../research/apc-controller-capabilities.md)
records method and limits; [coverage design](../research/full-live-specification-design.md)
governs future closure. No source code or reconstructed controller algorithm is
adopted as a behavioral contract.

**S-literal** is local strength for a directly supported static declaration:
identity literal inputs, ordered port/property-symbol declarations and explicit
presence/omission of an auto-load declaration. It establishes package metadata
only. Imported key/property meanings and helper results remain opaque; this grade
is not an executed metadata return, decoded protocol, host match or compatibility
result. **U** marks unsupported startup/runtime outcomes. Every requirement has
runtime/target applicability U; all actual documentary and target expected/comparison
fields are null, target grades U and all 49 cases unexecuted. No profile is complete.

No original module, creator/class, capability helper, reconstructed function,
controller script, Live/native/Max/example/candidate runtime or hardware ran.
No profile import, assignment, port detection, pairing, firmware/driver action,
MIDI/LED/audio/clock probe, installation or network service operation occurred.
Only analyst static decoding inspected the selected bytes. No helper/framework or
other-family source sweep was performed. Literal symbol names below are metadata
labels with unresolved values, not Python statements, flag values or routing laws.

## Exact denominator and existing owners

The immutable [149-row controller inventory](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/controller-profiles.json)
contains eight named APC entries selected here;141 other rows remain untouched.
The separate `_APC` row is classified support/internal in that inventory and
excluded, with no source decode here. Directory presence does not prove that every
row is a controller, a chooser option or an accepted device. The
[denominator](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/denominator.json) preserves exact selected rows and
source identities. No sibling/old/new profile declaration is copied into another.

[MIDI user mapping](midi-user-mapping.md) retains finite InstantMappings tokens,
transforms/takeover/banks and unresolved host effects. [Remote control](remote-control-workflows.md)
retains generic Control Surface chooser/setup/lock/control UI and149-profile gaps.
[Routing](routing-monitoring-latency.md) keeps actual ports/channels and
Track/Sync/Remote settings. Imported symbolic names here do not redefine those
roles, guarantee any port or map a physical endpoint. [Racks](device-racks.md)
and [automation](automation-envelopes.md) retain target/control/value/history
contracts and unknowns. No controller declaration expands finite MIDI codecs,
parameter transforms, audio behavior, bank contents, feedback, scheduling or Undo.
The Amp/Cabinet execution blocker and clean implementation status remain unchanged.

## Future positive prerequisites

[Fixtures](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/fixtures.json) are definitions, not hardware, code,
responses, port inventory or executable source. Later startup comparisons need
separate authorization and independently known genuine supported device/firmware,
exact host/OS/framework/profile and actual initialized usable ports with a productive
positive mapped-control/feedback baseline. Literal identifiers or a visible profile
name do not supply that baseline. Declaration positions differ from OS endpoint
numbers, enumeration and default selections.

Before absent/wrong/busy-port, no-device, no-effect or source-loss variants, retain
actual positive device/profile/port admission first. Audible comparisons additionally
need nonempty valid owned source, enabled supported active target/path, nonzero
source/amount/gain/send, nonmuted wet/return/output and calibrated positive output,
with correct Monitor/arm/receiver/clip/record/transport gates. No such setup is
supplied. Missing hardware/runtime/port/control, muted or zero signal and a failed
positive baseline remain unknown, never a passing negative or exclusion result.

## Per-profile declaration overview

Vendor literal2536 occurs in all eight identity declarations. Product and model
inputs below remain source literal shapes; a one-item model list is not silently
collapsed to a string. Input/output and tag sequences are recorded individually
in the clauses; their counts are declarations, not discovered physical port counts.

| Profile | Product-ID literal list | Model literal shape | Port declarations | Auto-load declaration |
| --- | --- | --- | --- | --- |
| APC20 | 123 | string: Akai APC20 | 2 | not declared; default U |
| APC40 | 115 | string: Akai APC40 | 2 | not declared; default U |
| APC40_MkII | 41 | string list: APC40 mkII, Akai APC40 MkII | 2 | not declared; default U |
| APC64 | 83 | string list: APC64 | 3 | True present |
| APC_Key_25 | 39 | string: APC Key 25 | 2 | not declared; default U |
| APC_Key_25_mk2 | 78 | string list: APC Key 25 mk2 | 4 | True present |
| APC_mini | 40 | string: APC MINI | 2 | not declared; default U |
| APC_mini_mk2 | 79 | string list: APC mini mk2 | 4 | True present |

## Bounded declaration clauses and unknowns

All clauses are source-declaration constraints with runtime outcomes unresolved.
The source symbol sequence is intentionally exact; it supplies no encoded flag,
visibility, direction-to-endpoint, controller behavior or original function result.

### REQ-APCC-01-IDENTITY — APC20 identity declaration

**S-literal/target-U.** The retained APC20 startup declaration supplies vendor literal 2536, product-ID list 123, and model-name single string "Akai APC20". These are literal identity inputs, not a proof of matched hardware, accepted labels, registration or successful startup. Helper normalization and matching remain U.

Evidence: `SURF-SCRIPT-APC20`, startup declaration offsets 40; [analyst evidence ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/capability-ledger.json). Offset provenance and raw-source identity are in research, not an implementation recipe.

### REQ-APCC-01-PORT-01 — APC20 declaration position 1

**S-literal/target-U.** The APC20 declaration at source-list position 1 is an input declaration carrying ordered opaque property symbols NOTES_CC, SCRIPT, REMOTE. This position and symbol sequence are metadata facts; they do not establish OS/device port number, actual port count/name, flag value, UI visibility, MIDI routing, clock or message/LED behavior.

Evidence: `SURF-SCRIPT-APC20`, startup declaration offsets 118, 110, 74, 86, 98; [analyst evidence ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/capability-ledger.json). Offset provenance and raw-source identity are in research, not an implementation recipe.

### REQ-APCC-01-PORT-02 — APC20 declaration position 2

**S-literal/target-U.** The APC20 declaration at source-list position 2 is an output declaration carrying ordered opaque property symbols SCRIPT, REMOTE. This position and symbol sequence are metadata facts; they do not establish OS/device port number, actual port count/name, flag value, UI visibility, MIDI routing, clock or message/LED behavior.

Evidence: `SURF-SCRIPT-APC20`, startup declaration offsets 172, 164, 140, 152; [analyst evidence ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/capability-ledger.json). Offset provenance and raw-source identity are in research, not an implementation recipe.

### REQ-APCC-01-AUTOLOAD — APC20 auto-load declaration context

**S-literal/target-U.** APC20 does not declare the auto-load symbol/pair in the selected startup metadata expression. Absence is not False, a framework default, disabled loading, failure or a rule for other profiles.

Evidence: `SURF-SCRIPT-APC20`, startup declaration offsets 184, 186; [analyst evidence ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/capability-ledger.json). Offset provenance and raw-source identity are in research, not an implementation recipe.

### REQ-APCC-02-IDENTITY — APC40 identity declaration

**S-literal/target-U.** The retained APC40 startup declaration supplies vendor literal 2536, product-ID list 115, and model-name single string "Akai APC40". These are literal identity inputs, not a proof of matched hardware, accepted labels, registration or successful startup. Helper normalization and matching remain U.

Evidence: `SURF-SCRIPT-APC40`, startup declaration offsets 40; [analyst evidence ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/capability-ledger.json). Offset provenance and raw-source identity are in research, not an implementation recipe.

### REQ-APCC-02-PORT-01 — APC40 declaration position 1

**S-literal/target-U.** The APC40 declaration at source-list position 1 is an input declaration carrying ordered opaque property symbols NOTES_CC, SCRIPT, REMOTE. This position and symbol sequence are metadata facts; they do not establish OS/device port number, actual port count/name, flag value, UI visibility, MIDI routing, clock or message/LED behavior.

Evidence: `SURF-SCRIPT-APC40`, startup declaration offsets 118, 110, 74, 86, 98; [analyst evidence ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/capability-ledger.json). Offset provenance and raw-source identity are in research, not an implementation recipe.

### REQ-APCC-02-PORT-02 — APC40 declaration position 2

**S-literal/target-U.** The APC40 declaration at source-list position 2 is an output declaration carrying ordered opaque property symbols SCRIPT, REMOTE. This position and symbol sequence are metadata facts; they do not establish OS/device port number, actual port count/name, flag value, UI visibility, MIDI routing, clock or message/LED behavior.

Evidence: `SURF-SCRIPT-APC40`, startup declaration offsets 172, 164, 140, 152; [analyst evidence ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/capability-ledger.json). Offset provenance and raw-source identity are in research, not an implementation recipe.

### REQ-APCC-02-AUTOLOAD — APC40 auto-load declaration context

**S-literal/target-U.** APC40 does not declare the auto-load symbol/pair in the selected startup metadata expression. Absence is not False, a framework default, disabled loading, failure or a rule for other profiles.

Evidence: `SURF-SCRIPT-APC40`, startup declaration offsets 184, 186; [analyst evidence ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/capability-ledger.json). Offset provenance and raw-source identity are in research, not an implementation recipe.

### REQ-APCC-03-IDENTITY — APC40_MkII identity declaration

**S-literal/target-U.** The retained APC40_MkII startup declaration supplies vendor literal 2536, product-ID list 41, and model-name ordered string list "APC40 mkII", "Akai APC40 MkII". These are literal identity inputs, not a proof of matched hardware, accepted labels, registration or successful startup. Helper normalization and matching remain U.

Evidence: `SURF-SCRIPT-APC40_MKII`, startup declaration offsets 44; [analyst evidence ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/capability-ledger.json). Offset provenance and raw-source identity are in research, not an implementation recipe.

### REQ-APCC-03-PORT-01 — APC40_MkII declaration position 1

**S-literal/target-U.** The APC40_MkII declaration at source-list position 1 is an input declaration carrying ordered opaque property symbols NOTES_CC, SCRIPT, REMOTE. This position and symbol sequence are metadata facts; they do not establish OS/device port number, actual port count/name, flag value, UI visibility, MIDI routing, clock or message/LED behavior.

Evidence: `SURF-SCRIPT-APC40_MKII`, startup declaration offsets 122, 114, 78, 90, 102; [analyst evidence ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/capability-ledger.json). Offset provenance and raw-source identity are in research, not an implementation recipe.

### REQ-APCC-03-PORT-02 — APC40_MkII declaration position 2

**S-literal/target-U.** The APC40_MkII declaration at source-list position 2 is an output declaration carrying ordered opaque property symbols SYNC, SCRIPT, REMOTE. This position and symbol sequence are metadata facts; they do not establish OS/device port number, actual port count/name, flag value, UI visibility, MIDI routing, clock or message/LED behavior.

Evidence: `SURF-SCRIPT-APC40_MKII`, startup declaration offsets 188, 180, 144, 156, 168; [analyst evidence ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/capability-ledger.json). Offset provenance and raw-source identity are in research, not an implementation recipe.

### REQ-APCC-03-AUTOLOAD — APC40_MkII auto-load declaration context

**S-literal/target-U.** APC40_MkII does not declare the auto-load symbol/pair in the selected startup metadata expression. Absence is not False, a framework default, disabled loading, failure or a rule for other profiles.

Evidence: `SURF-SCRIPT-APC40_MKII`, startup declaration offsets 200, 202; [analyst evidence ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/capability-ledger.json). Offset provenance and raw-source identity are in research, not an implementation recipe.

### REQ-APCC-04-IDENTITY — APC64 identity declaration

**S-literal/target-U.** The retained APC64 startup declaration supplies vendor literal 2536, product-ID list 83, and model-name ordered string list "APC64". These are literal identity inputs, not a proof of matched hardware, accepted labels, registration or successful startup. Helper normalization and matching remain U.

Evidence: `SURF-SCRIPT-APC64`, startup declaration offsets 42; [analyst evidence ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/capability-ledger.json). Offset provenance and raw-source identity are in research, not an implementation recipe.

### REQ-APCC-04-PORT-01 — APC64 declaration position 1

**S-literal/target-U.** The APC64 declaration at source-list position 1 is an input declaration carrying ordered opaque property symbols NOTES_CC, SCRIPT, HIDDEN. This position and symbol sequence are metadata facts; they do not establish OS/device port number, actual port count/name, flag value, UI visibility, MIDI routing, clock or message/LED behavior.

Evidence: `SURF-SCRIPT-APC64`, startup declaration offsets 120, 112, 76, 88, 100; [analyst evidence ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/capability-ledger.json). Offset provenance and raw-source identity are in research, not an implementation recipe.

### REQ-APCC-04-PORT-02 — APC64 declaration position 2

**S-literal/target-U.** The APC64 declaration at source-list position 2 is an output declaration carrying ordered opaque property symbols NOTES_CC, SCRIPT, HIDDEN. This position and symbol sequence are metadata facts; they do not establish OS/device port number, actual port count/name, flag value, UI visibility, MIDI routing, clock or message/LED behavior.

Evidence: `SURF-SCRIPT-APC64`, startup declaration offsets 186, 178, 142, 154, 166; [analyst evidence ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/capability-ledger.json). Offset provenance and raw-source identity are in research, not an implementation recipe.

### REQ-APCC-04-PORT-03 — APC64 declaration position 3

**S-literal/target-U.** The APC64 declaration at source-list position 3 is an output declaration carrying ordered opaque property symbols SYNC. This position and symbol sequence are metadata facts; they do not establish OS/device port number, actual port count/name, flag value, UI visibility, MIDI routing, clock or message/LED behavior.

Evidence: `SURF-SCRIPT-APC64`, startup declaration offsets 228, 220, 208; [analyst evidence ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/capability-ledger.json). Offset provenance and raw-source identity are in research, not an implementation recipe.

### REQ-APCC-04-AUTOLOAD — APC64 auto-load declaration context

**S-literal/target-U.** APC64 has a literal True associated with the imported auto-load declaration symbol. This is a static declaration, not proof that the profile actually loads automatically or initializes successfully.

Evidence: `SURF-SCRIPT-APC64`, startup declaration offsets 254, 256; [analyst evidence ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/capability-ledger.json). Offset provenance and raw-source identity are in research, not an implementation recipe.

### REQ-APCC-05-IDENTITY — APC_Key_25 identity declaration

**S-literal/target-U.** The retained APC_Key_25 startup declaration supplies vendor literal 2536, product-ID list 39, and model-name single string "APC Key 25". These are literal identity inputs, not a proof of matched hardware, accepted labels, registration or successful startup. Helper normalization and matching remain U.

Evidence: `SURF-SCRIPT-APC_KEY_25`, startup declaration offsets 40; [analyst evidence ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/capability-ledger.json). Offset provenance and raw-source identity are in research, not an implementation recipe.

### REQ-APCC-05-PORT-01 — APC_Key_25 declaration position 1

**S-literal/target-U.** The APC_Key_25 declaration at source-list position 1 is an input declaration carrying ordered opaque property symbols NOTES_CC, SCRIPT, REMOTE. This position and symbol sequence are metadata facts; they do not establish OS/device port number, actual port count/name, flag value, UI visibility, MIDI routing, clock or message/LED behavior.

Evidence: `SURF-SCRIPT-APC_KEY_25`, startup declaration offsets 118, 110, 74, 86, 98; [analyst evidence ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/capability-ledger.json). Offset provenance and raw-source identity are in research, not an implementation recipe.

### REQ-APCC-05-PORT-02 — APC_Key_25 declaration position 2

**S-literal/target-U.** The APC_Key_25 declaration at source-list position 2 is an output declaration carrying ordered opaque property symbols SCRIPT, REMOTE. This position and symbol sequence are metadata facts; they do not establish OS/device port number, actual port count/name, flag value, UI visibility, MIDI routing, clock or message/LED behavior.

Evidence: `SURF-SCRIPT-APC_KEY_25`, startup declaration offsets 172, 164, 140, 152; [analyst evidence ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/capability-ledger.json). Offset provenance and raw-source identity are in research, not an implementation recipe.

### REQ-APCC-05-AUTOLOAD — APC_Key_25 auto-load declaration context

**S-literal/target-U.** APC_Key_25 does not declare the auto-load symbol/pair in the selected startup metadata expression. Absence is not False, a framework default, disabled loading, failure or a rule for other profiles.

Evidence: `SURF-SCRIPT-APC_KEY_25`, startup declaration offsets 184, 186; [analyst evidence ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/capability-ledger.json). Offset provenance and raw-source identity are in research, not an implementation recipe.

### REQ-APCC-06-IDENTITY — APC_Key_25_mk2 identity declaration

**S-literal/target-U.** The retained APC_Key_25_mk2 startup declaration supplies vendor literal 2536, product-ID list 78, and model-name ordered string list "APC Key 25 mk2". These are literal identity inputs, not a proof of matched hardware, accepted labels, registration or successful startup. Helper normalization and matching remain U.

Evidence: `SURF-SCRIPT-APC_KEY_25_MK2`, startup declaration offsets 42; [analyst evidence ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/capability-ledger.json). Offset provenance and raw-source identity are in research, not an implementation recipe.

### REQ-APCC-06-PORT-01 — APC_Key_25_mk2 declaration position 1

**S-literal/target-U.** The APC_Key_25_mk2 declaration at source-list position 1 is an input declaration carrying ordered opaque property symbols NOTES_CC. This position and symbol sequence are metadata facts; they do not establish OS/device port number, actual port count/name, flag value, UI visibility, MIDI routing, clock or message/LED behavior.

Evidence: `SURF-SCRIPT-APC_KEY_25_MK2`, startup declaration offsets 96, 88, 76; [analyst evidence ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/capability-ledger.json). Offset provenance and raw-source identity are in research, not an implementation recipe.

### REQ-APCC-06-PORT-02 — APC_Key_25_mk2 declaration position 2

**S-literal/target-U.** The APC_Key_25_mk2 declaration at source-list position 2 is an input declaration carrying ordered opaque property symbols NOTES_CC, SCRIPT. This position and symbol sequence are metadata facts; they do not establish OS/device port number, actual port count/name, flag value, UI visibility, MIDI routing, clock or message/LED behavior.

Evidence: `SURF-SCRIPT-APC_KEY_25_MK2`, startup declaration offsets 150, 142, 118, 130; [analyst evidence ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/capability-ledger.json). Offset provenance and raw-source identity are in research, not an implementation recipe.

### REQ-APCC-06-PORT-03 — APC_Key_25_mk2 declaration position 3

**S-literal/target-U.** The APC_Key_25_mk2 declaration at source-list position 3 is an output declaration carrying ordered opaque property symbols NOTES_CC. This position and symbol sequence are metadata facts; they do not establish OS/device port number, actual port count/name, flag value, UI visibility, MIDI routing, clock or message/LED behavior.

Evidence: `SURF-SCRIPT-APC_KEY_25_MK2`, startup declaration offsets 192, 184, 172; [analyst evidence ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/capability-ledger.json). Offset provenance and raw-source identity are in research, not an implementation recipe.

### REQ-APCC-06-PORT-04 — APC_Key_25_mk2 declaration position 4

**S-literal/target-U.** The APC_Key_25_mk2 declaration at source-list position 4 is an output declaration carrying ordered opaque property symbols NOTES_CC, SCRIPT, SYNC, HIDDEN. This position and symbol sequence are metadata facts; they do not establish OS/device port number, actual port count/name, flag value, UI visibility, MIDI routing, clock or message/LED behavior.

Evidence: `SURF-SCRIPT-APC_KEY_25_MK2`, startup declaration offsets 270, 262, 214, 226, 238, 250; [analyst evidence ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/capability-ledger.json). Offset provenance and raw-source identity are in research, not an implementation recipe.

### REQ-APCC-06-AUTOLOAD — APC_Key_25_mk2 auto-load declaration context

**S-literal/target-U.** APC_Key_25_mk2 has a literal True associated with the imported auto-load declaration symbol. This is a static declaration, not proof that the profile actually loads automatically or initializes successfully.

Evidence: `SURF-SCRIPT-APC_KEY_25_MK2`, startup declaration offsets 296, 298; [analyst evidence ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/capability-ledger.json). Offset provenance and raw-source identity are in research, not an implementation recipe.

### REQ-APCC-07-IDENTITY — APC_mini identity declaration

**S-literal/target-U.** The retained APC_mini startup declaration supplies vendor literal 2536, product-ID list 40, and model-name single string "APC MINI". These are literal identity inputs, not a proof of matched hardware, accepted labels, registration or successful startup. Helper normalization and matching remain U.

Evidence: `SURF-SCRIPT-APC_MINI`, startup declaration offsets 40; [analyst evidence ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/capability-ledger.json). Offset provenance and raw-source identity are in research, not an implementation recipe.

### REQ-APCC-07-PORT-01 — APC_mini declaration position 1

**S-literal/target-U.** The APC_mini declaration at source-list position 1 is an input declaration carrying ordered opaque property symbols NOTES_CC, SCRIPT, REMOTE. This position and symbol sequence are metadata facts; they do not establish OS/device port number, actual port count/name, flag value, UI visibility, MIDI routing, clock or message/LED behavior.

Evidence: `SURF-SCRIPT-APC_MINI`, startup declaration offsets 118, 110, 74, 86, 98; [analyst evidence ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/capability-ledger.json). Offset provenance and raw-source identity are in research, not an implementation recipe.

### REQ-APCC-07-PORT-02 — APC_mini declaration position 2

**S-literal/target-U.** The APC_mini declaration at source-list position 2 is an output declaration carrying ordered opaque property symbols SCRIPT, REMOTE. This position and symbol sequence are metadata facts; they do not establish OS/device port number, actual port count/name, flag value, UI visibility, MIDI routing, clock or message/LED behavior.

Evidence: `SURF-SCRIPT-APC_MINI`, startup declaration offsets 172, 164, 140, 152; [analyst evidence ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/capability-ledger.json). Offset provenance and raw-source identity are in research, not an implementation recipe.

### REQ-APCC-07-AUTOLOAD — APC_mini auto-load declaration context

**S-literal/target-U.** APC_mini does not declare the auto-load symbol/pair in the selected startup metadata expression. Absence is not False, a framework default, disabled loading, failure or a rule for other profiles.

Evidence: `SURF-SCRIPT-APC_MINI`, startup declaration offsets 184, 186; [analyst evidence ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/capability-ledger.json). Offset provenance and raw-source identity are in research, not an implementation recipe.

### REQ-APCC-08-IDENTITY — APC_mini_mk2 identity declaration

**S-literal/target-U.** The retained APC_mini_mk2 startup declaration supplies vendor literal 2536, product-ID list 79, and model-name ordered string list "APC mini mk2". These are literal identity inputs, not a proof of matched hardware, accepted labels, registration or successful startup. Helper normalization and matching remain U.

Evidence: `SURF-SCRIPT-APC_MINI_MK2`, startup declaration offsets 42; [analyst evidence ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/capability-ledger.json). Offset provenance and raw-source identity are in research, not an implementation recipe.

### REQ-APCC-08-PORT-01 — APC_mini_mk2 declaration position 1

**S-literal/target-U.** The APC_mini_mk2 declaration at source-list position 1 is an input declaration carrying ordered opaque property symbols NOTES_CC, SCRIPT. This position and symbol sequence are metadata facts; they do not establish OS/device port number, actual port count/name, flag value, UI visibility, MIDI routing, clock or message/LED behavior.

Evidence: `SURF-SCRIPT-APC_MINI_MK2`, startup declaration offsets 108, 100, 76, 88; [analyst evidence ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/capability-ledger.json). Offset provenance and raw-source identity are in research, not an implementation recipe.

### REQ-APCC-08-PORT-02 — APC_mini_mk2 declaration position 2

**S-literal/target-U.** The APC_mini_mk2 declaration at source-list position 2 is an input declaration carrying ordered opaque property symbols NOTES_CC. This position and symbol sequence are metadata facts; they do not establish OS/device port number, actual port count/name, flag value, UI visibility, MIDI routing, clock or message/LED behavior.

Evidence: `SURF-SCRIPT-APC_MINI_MK2`, startup declaration offsets 150, 142, 130; [analyst evidence ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/capability-ledger.json). Offset provenance and raw-source identity are in research, not an implementation recipe.

### REQ-APCC-08-PORT-03 — APC_mini_mk2 declaration position 3

**S-literal/target-U.** The APC_mini_mk2 declaration at source-list position 3 is an output declaration carrying ordered opaque property symbols NOTES_CC, SCRIPT, SYNC, HIDDEN. This position and symbol sequence are metadata facts; they do not establish OS/device port number, actual port count/name, flag value, UI visibility, MIDI routing, clock or message/LED behavior.

Evidence: `SURF-SCRIPT-APC_MINI_MK2`, startup declaration offsets 228, 220, 172, 184, 196, 208; [analyst evidence ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/capability-ledger.json). Offset provenance and raw-source identity are in research, not an implementation recipe.

### REQ-APCC-08-PORT-04 — APC_mini_mk2 declaration position 4

**S-literal/target-U.** The APC_mini_mk2 declaration at source-list position 4 is an output declaration carrying ordered opaque property symbols NOTES_CC. This position and symbol sequence are metadata facts; they do not establish OS/device port number, actual port count/name, flag value, UI visibility, MIDI routing, clock or message/LED behavior.

Evidence: `SURF-SCRIPT-APC_MINI_MK2`, startup declaration offsets 270, 262, 250; [analyst evidence ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/capability-ledger.json). Offset provenance and raw-source identity are in research, not an implementation recipe.

### REQ-APCC-08-AUTOLOAD — APC_mini_mk2 auto-load declaration context

**S-literal/target-U.** APC_mini_mk2 has a literal True associated with the imported auto-load declaration symbol. This is a static declaration, not proof that the profile actually loads automatically or initializes successfully.

Evidence: `SURF-SCRIPT-APC_MINI_MK2`, startup declaration offsets 296, 298; [analyst evidence ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/capability-ledger.json). Offset provenance and raw-source identity are in research, not an implementation recipe.

### REQ-APCC-U-HELPERS — Opaque declaration helpers and keys

**U/target-U.** Imported property/key values, declaration-helper results, normalization/defaults, duplicate-key/runtime return types and exceptions are unknown. Framework imports/calls were not resolved or executed.

### REQ-APCC-U-MATCH — Actual device matching and applicability

**U/target-U.** Physical identity, USB/MIDI/OS enumeration, supported firmware/platform/edition, model alias matching, user-selected/automatic profile assignment and exact target startup behavior remain unknown beyond package-byte identity.

### REQ-APCC-U-PORTS — Port ordering flag and direction effects

**U/target-U.** Declared list position/input-output role and opaque flags do not establish detected physical ports, host order/names, visibility, Track/Sync/Remote policy, exclusive acquisition or working events.

### REQ-APCC-U-CREATOR — Module creator and initialization lifecycle

**U/target-U.** Module top-level import/class creation, creator entry point, framework/type/branch/exception handling, actual object creation, loading, pairing and activation remain unknown and unexecuted. Only capability literals/import declarations were decoded.

### REQ-APCC-U-PROTOCOL — MIDI controls feedback and output

**U/target-U.** MIDI/LED/SysEx/pads/banks/notes/CC, synchronization/clock, timing, latency, numeric transforms, audio and arbitrary device controls have no supported protocol/output oracle here. Existing finite mapping/remote/routing owners retain their laws.

### REQ-APCC-U-STATE — Failures cancellation persistence and teardown

**U/target-U.** Wrong/absent ports, permissions/busy devices, disconnect/reconnect, stale configuration, loading errors, retry/cancel, restart/save/profile migration, concurrent controllers and close/quit cleanup remain unknown.

## Finite future cases

[Cases](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/cases.json) contain37 declaration-context proposals and12
unknown probes mapped to43 requirements (37 S-literal/6 U). All49 have null actual
documentary/target oracles. They do not execute capability code or provide a fake
host/controller. An individual proposed observation closes no compound profile,
helper, creator, protocol, output, failure or lifecycle branch.

| Case | Requirement | Kind | Proposed focus |
| --- | --- | --- | --- |
| APCC-001 | REQ-APCC-01-IDENTITY | identity | APC20 identity declaration |
| APCC-002 | REQ-APCC-01-PORT-01 | port | APC20 declaration position 1 |
| APCC-003 | REQ-APCC-01-PORT-02 | port | APC20 declaration position 2 |
| APCC-004 | REQ-APCC-01-AUTOLOAD | startup | APC20 auto-load declaration context |
| APCC-005 | REQ-APCC-02-IDENTITY | identity | APC40 identity declaration |
| APCC-006 | REQ-APCC-02-PORT-01 | port | APC40 declaration position 1 |
| APCC-007 | REQ-APCC-02-PORT-02 | port | APC40 declaration position 2 |
| APCC-008 | REQ-APCC-02-AUTOLOAD | startup | APC40 auto-load declaration context |
| APCC-009 | REQ-APCC-03-IDENTITY | identity | APC40_MkII identity declaration |
| APCC-010 | REQ-APCC-03-PORT-01 | port | APC40_MkII declaration position 1 |
| APCC-011 | REQ-APCC-03-PORT-02 | port | APC40_MkII declaration position 2 |
| APCC-012 | REQ-APCC-03-AUTOLOAD | startup | APC40_MkII auto-load declaration context |
| APCC-013 | REQ-APCC-04-IDENTITY | identity | APC64 identity declaration |
| APCC-014 | REQ-APCC-04-PORT-01 | port | APC64 declaration position 1 |
| APCC-015 | REQ-APCC-04-PORT-02 | port | APC64 declaration position 2 |
| APCC-016 | REQ-APCC-04-PORT-03 | port | APC64 declaration position 3 |
| APCC-017 | REQ-APCC-04-AUTOLOAD | startup | APC64 auto-load declaration context |
| APCC-018 | REQ-APCC-05-IDENTITY | identity | APC_Key_25 identity declaration |
| APCC-019 | REQ-APCC-05-PORT-01 | port | APC_Key_25 declaration position 1 |
| APCC-020 | REQ-APCC-05-PORT-02 | port | APC_Key_25 declaration position 2 |
| APCC-021 | REQ-APCC-05-AUTOLOAD | startup | APC_Key_25 auto-load declaration context |
| APCC-022 | REQ-APCC-06-IDENTITY | identity | APC_Key_25_mk2 identity declaration |
| APCC-023 | REQ-APCC-06-PORT-01 | port | APC_Key_25_mk2 declaration position 1 |
| APCC-024 | REQ-APCC-06-PORT-02 | port | APC_Key_25_mk2 declaration position 2 |
| APCC-025 | REQ-APCC-06-PORT-03 | port | APC_Key_25_mk2 declaration position 3 |
| APCC-026 | REQ-APCC-06-PORT-04 | port | APC_Key_25_mk2 declaration position 4 |
| APCC-027 | REQ-APCC-06-AUTOLOAD | startup | APC_Key_25_mk2 auto-load declaration context |
| APCC-028 | REQ-APCC-07-IDENTITY | identity | APC_mini identity declaration |
| APCC-029 | REQ-APCC-07-PORT-01 | port | APC_mini declaration position 1 |
| APCC-030 | REQ-APCC-07-PORT-02 | port | APC_mini declaration position 2 |
| APCC-031 | REQ-APCC-07-AUTOLOAD | startup | APC_mini auto-load declaration context |
| APCC-032 | REQ-APCC-08-IDENTITY | identity | APC_mini_mk2 identity declaration |
| APCC-033 | REQ-APCC-08-PORT-01 | port | APC_mini_mk2 declaration position 1 |
| APCC-034 | REQ-APCC-08-PORT-02 | port | APC_mini_mk2 declaration position 2 |
| APCC-035 | REQ-APCC-08-PORT-03 | port | APC_mini_mk2 declaration position 3 |
| APCC-036 | REQ-APCC-08-PORT-04 | port | APC_mini_mk2 declaration position 4 |
| APCC-037 | REQ-APCC-08-AUTOLOAD | startup | APC_mini_mk2 auto-load declaration context |
| APCC-038 | REQ-APCC-U-HELPERS | source-context | Opaque declaration helpers and keys |
| APCC-039 | REQ-APCC-U-MATCH | identity | Actual device matching and applicability |
| APCC-040 | REQ-APCC-U-PORTS | port | Port ordering flag and direction effects |
| APCC-041 | REQ-APCC-U-CREATOR | startup | Module creator and initialization lifecycle |
| APCC-042 | REQ-APCC-U-PROTOCOL | protocol | MIDI controls feedback and output |
| APCC-043 | REQ-APCC-U-STATE | teardown | Failures cancellation persistence and teardown |
| APCC-044 | REQ-APCC-U-HELPERS | source-context | Literal shape and symbol boundary |
| APCC-045 | REQ-APCC-U-MATCH | negative | Unavailable or mismatched device |
| APCC-046 | REQ-APCC-U-PORTS | source-loss | Missing busy or reordered port |
| APCC-047 | REQ-APCC-U-CREATOR | cancellation | Startup cancellation and source loss |
| APCC-048 | REQ-APCC-U-PROTOCOL | signal | Nonzero control and feedback baseline |
| APCC-049 | REQ-APCC-U-STATE | persistence | Reconnect restart and pending teardown |

## Local questions

- **Q-APCC-001:** Matching Python3.11/header/data decoding establishes only literal code evidence; it does not execute or validate module imports, creator/classes or get_capabilities in Live.
- **Q-APCC-002:** Key/property globals and controller/port helper results remain opaque. No framework module was read, imported or called; missing auto-load declaration never implies False/default.
- **Q-APCC-003:** Single-string versus list model-name inputs, numeric vendor/product IDs and label spelling do not establish real device matching, normalization, alias, firmware/OS/edition support.
- **Q-APCC-004:** Twenty-one declaration positions and input/output/property-symbol roles do not determine actual port count, number, names, visibility, routing or Sync/Remote functionality. APC64 and mk2 declarations differ and must not be flattened.
- **Q-APCC-005:** Creators, class/type configuration, imports and framework side effects/branches/exceptions remain outside the literal scope and unexecuted.
- **Q-APCC-006:** Actual MIDI/LED/protocol/timing/output, failed/missing ports, detection/activation, persistence/cancel/reconnect/teardown require separately authorized genuine positive hardware/host evidence; no simulation or borrowed mapping law.

## Analyst freeze and limits

[Source records](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/sources.json) and [input/owner pins](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/input-owner-pins.json)
retain exact installed file identities matched to the unchanged149-row baseline.
The eight raw byte copies are immutable; the local static tool reads them as data,
never imports or calls original functions. Method, provenance, header checks and
restricted disassembly belong to [research](../research/apc-controller-capabilities.md).
No original source or pseudocode is reproduced as required behavior.

[Counts](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/counts.json), [manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/manifest-author-r1.json),
canonical snapshots and [read-only validator](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/validate.py)
seal this partial analyst revision. Use the documented existing CPython3.11 command;
validation rejects mismatched bytecode/interpreter versions and prints stdout only.
It never rewrites frozen reports. Independent semantic review, helper evidence and
separately authorized actual positive device/host evidence remain required.
Root owns shared indexes, coverage, questions and log; this packet edits none.
