---
id: RESEARCH-APC-CONTROLLER-CAPABILITIES
type: research
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3 installed startup-byte identity; controller/runtime applicability U
---

# APC startup capability source and static decoding

## Scope and evidence boundary

This bounded F-08 task supports the [canonical declaration draft](../specs/apc-controller-capabilities.md).
It selects only eight named APC entries from the immutable149-row
[controller inventory](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/controller-profiles.json).
The separate `_APC` support/internal entry is excluded; no framework/helper or
other-family source was decoded. Eight complete installed `__init__.pyc` files were
retained with hashes matching baseline. The other141 rows and every original file
remain unchanged. No directory name becomes proof of a controller or runtime
capability. This is partial source evidence, not a released implementation input.

Static source identity is exact installed 12.4.3 package data. Runtime applicability,
framework/import/helper return, startup/hardware match and all protocol/lifecycle
outcomes remain U. Local S-literal means directly supported literal/symbolic
metadata only, distinct from dynamic behavior. No original module/function/class,
creator, script, Live/native/Max/example/hardware/candidate ran. No import, exec,
eval or invocation of original or reconstructed original code occurred. Analyst
tools run solely on byte/code-object data; no controller or helper is simulated.

## Method selection and immutable acquisition

The existing [static mapping decoder pattern](../../analysis/ableton-live-12.4.3/r2/s4-midi-v1/decode.py)
and [mapping source record](sources/midi-user-mapping-12.4.3.md) distinguish decoding
from execution. Default Python3.13 was identified before decoding; it was not used
to marshal/disassemble incompatible source bytes. Already installed CPython3.11.13
has exact magic `a70d0d0a`; no tooling was installed. Its resolved interpreter,
version and method are recorded in [capture environment](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/capture-environment.json).

[Sources](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/sources.json) records original installed paths, retained
copy names, byte sizes/SHA256, capture UTC and header identities.
[Initial capture pins](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/initial-capture-pins.json) protect all 11
original raw/capture/catalog payloads. [Header fields](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/header-fields.json)
preserve exact16-byte headers: all eight flags are 0 (timestamp/source-size form).
Header timestamp/source-size fields are raw data, not independently verified source
`.py` metadata, `.pyc` sizes or capture times. No original `.py` file was acquired.
The original build filename inside code data is separate from the installed path.

### APC20

`SURF-SCRIPT-APC20`; original `/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/MIDI Remote Scripts/APC20/__init__.pyc`; [retained bytes](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/sources/APC20--__init__.pyc); 1223bytes; SHA256 `fa3c57811319b141a48af7629777fc3eb5c2a69bc3fb70f1f99976b38d726231`; captured `2026-10-19T22:48:50.271906+00:00`. Magic `a70d0d0a`, header `a70d0d0a0000000038ef3a6a97020000`. Module code filename `output/Live/mac_universal_64_static/Release/python-bundle/MIDI Remote Scripts/APC20/__init__.py` is retained provenance, not a source lookup or executed path.

### APC40

`SURF-SCRIPT-APC40`; original `/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/MIDI Remote Scripts/APC40/__init__.pyc`; [retained bytes](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/sources/APC40--__init__.pyc); 1218bytes; SHA256 `f593cfbb78ea3c1dcd4cf812c96bd94e1924973288fe02c1ece65789398ec855`; captured `2026-10-19T22:48:50.272716+00:00`. Magic `a70d0d0a`, header `a70d0d0a0000000038ef3a6a68020000`. Module code filename `output/Live/mac_universal_64_static/Release/python-bundle/MIDI Remote Scripts/APC40/__init__.py` is retained provenance, not a source lookup or executed path.

### APC40_MkII

`SURF-SCRIPT-APC40_MKII`; original `/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/MIDI Remote Scripts/APC40_MkII/__init__.pyc`; [retained bytes](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/sources/APC40_MkII--__init__.pyc); 1301bytes; SHA256 `c8293849376de4b38ccab3c5277b1f4006ce1273c4c7c4b51ecbb16d4e88e418`; captured `2026-10-19T22:48:50.273236+00:00`. Magic `a70d0d0a`, header `a70d0d0a0000000038ef3a6ab5020000`. Module code filename `output/Live/mac_universal_64_static/Release/python-bundle/MIDI Remote Scripts/APC40_MkII/__init__.py` is retained provenance, not a source lookup or executed path.

### APC64

`SURF-SCRIPT-APC64`; original `/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/MIDI Remote Scripts/APC64/__init__.pyc`; [retained bytes](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/sources/APC64--__init__.pyc); 6835bytes; SHA256 `6db32886e19d764575de5183010fc60e4d64bf1b28171ee4d279e55a4307f8bd`; captured `2026-10-19T22:48:50.274310+00:00`. Magic `a70d0d0a`, header `a70d0d0a0000000038ef3a6af9100000`. Module code filename `output/Live/mac_universal_64_static/Release/python-bundle/MIDI Remote Scripts/APC64/__init__.py` is retained provenance, not a source lookup or executed path.

### APC_Key_25

`SURF-SCRIPT-APC_KEY_25`; original `/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/MIDI Remote Scripts/APC_Key_25/__init__.pyc`; [retained bytes](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/sources/APC_Key_25--__init__.pyc); 1228bytes; SHA256 `a3ae76501197d9de76787584725b8f99266fca886016d773604ca4984ea6b52b`; captured `2026-10-19T22:48:50.275053+00:00`. Magic `a70d0d0a`, header `a70d0d0a0000000038ef3a6a77020000`. Module code filename `output/Live/mac_universal_64_static/Release/python-bundle/MIDI Remote Scripts/APC_Key_25/__init__.py` is retained provenance, not a source lookup or executed path.

### APC_Key_25_mk2

`SURF-SCRIPT-APC_KEY_25_MK2`; original `/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/MIDI Remote Scripts/APC_Key_25_mk2/__init__.pyc`; [retained bytes](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/sources/APC_Key_25_mk2--__init__.pyc); 2424bytes; SHA256 `a9281c1b8b4c8273f06906724b12d0b7057978cba27555290ab68052945b00ea`; captured `2026-10-19T22:48:50.275682+00:00`. Magic `a70d0d0a`, header `a70d0d0a0000000038ef3a6a67050000`. Module code filename `output/Live/mac_universal_64_static/Release/python-bundle/MIDI Remote Scripts/APC_Key_25_mk2/__init__.py` is retained provenance, not a source lookup or executed path.

### APC_mini

`SURF-SCRIPT-APC_MINI`; original `/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/MIDI Remote Scripts/APC_mini/__init__.pyc`; [retained bytes](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/sources/APC_mini--__init__.pyc); 1222bytes; SHA256 `d87102f0ecbbe6d9e7ceacd26894a55db0adbb3c767f427e64ad9ab4182805a3`; captured `2026-10-19T22:48:50.276166+00:00`. Magic `a70d0d0a`, header `a70d0d0a0000000038ef3a6a6f020000`. Module code filename `output/Live/mac_universal_64_static/Release/python-bundle/MIDI Remote Scripts/APC_mini/__init__.py` is retained provenance, not a source lookup or executed path.

### APC_mini_mk2

`SURF-SCRIPT-APC_MINI_MK2`; original `/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/MIDI Remote Scripts/APC_mini_mk2/__init__.pyc`; [retained bytes](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/sources/APC_mini_mk2--__init__.pyc); 4265bytes; SHA256 `887db501fdefa7c55eeaf5f049940b1d608a0ae6c69b2a204c94491fe08ba40d`; captured `2026-10-19T22:48:50.276927+00:00`. Magic `a70d0d0a`, header `a70d0d0a0000000038ef3a6ab5080000`. Module code filename `output/Live/mac_universal_64_static/Release/python-bundle/MIDI Remote Scripts/APC_mini_mk2/__init__.py` is retained provenance, not a source lookup or executed path.

## Bounded static recognizer and locators

[decode.py](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/decode.py) requires CPython3.11 and matching magic,
16-byte valid flags/header, one module code object, fully consumed marshal payload,
one direct zero-formal-argument get_capabilities code object, no closure/cell or
exception table and a small allowed instruction set. It parses original data with
stdlib marshal and dis; original code objects are never called, imported, exec'd,
eval'd or installed. Unsupported control flow/opcodes/calls stop recognition rather
than guessing branches or helper behavior. All eight decoded successfully;
[failures](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/decode-failures.json) is empty, not a claimed hardware pass.

The recognizer records literal/list/map declaration structure and symbolic imports.
Every CALL becomes an **opaque data node**; no helper result is computed. Global
keys/properties stay imported symbols with the declaring import/store offsets.
Only identity keyword input literals and their literal-list shape are projected;
symbol values/call results are refused. This is a restricted static data recognizer,
not a Python evaluator, reconstructed creator, framework shim or candidate controller.

[Declarations](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/declarations.json) retains stable module/import and
get_capabilities instruction offsets, literal constant indices, list-build offsets,
call sites, key-symbol order and final map/return locations. [Listings](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/listings.txt)
is restricted analyst disassembly with process addresses removed, not source code
or behavioral pseudocode. It includes module top-level instructions for import
provenance only; creator/class and other nested code bodies were not decoded or
analyzed. Only the eight get_capabilities streams and required module import-name
bindings support adopted metadata. Merely listing a top-level call does not execute
it or establish its result; module/class dependencies and side effects remain U.

[Capability ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/capability-ledger.json) preserves eight identity
input declarations and21 ordered input/output port declarations plus three explicit
True auto-load associations/five omitted declarations. The29 helper-call nodes
remain opaque. APC64 has one declared input and two outputs; Key25mk2/Minimk2 each
have two inputs/two outputs, in different property/order contexts. These are source
expression counts/positions, never actual physical port counts or OS indices.
Five old-style declarations cite `_Framework.Capabilities`; three cite
`ableton.v3.control_surface.capabilities`. No imported framework file was read or
called, and no equivalent flag/helper meaning across them is assumed.

Decoder selfchecks reject seven bad header/payload variants including non-code
marshal data, an unsupported branch and an unknown helper call. Two tiny analyst-
authored compile-only rejection fixtures are never executed; no compiled original
function is invoked. These checks validate analysis boundaries only, not controller
behavior. All target/runtime oracles remain null/U/unexecuted.

## Interpretation, questions and ownership

[MIDI user mapping](../specs/midi-user-mapping.md), [remote-control workflows](../specs/remote-control-workflows.md),
[routing](../specs/routing-monitoring-latency.md), [racks](../specs/device-racks.md)
and [automation](../specs/automation-envelopes.md) retain finite configuration,
transforms/banks, generic chooser/setup/lock, actual ports/Track-Sync-Remote and
parameter/history laws. Startup declarations supply none of their native codecs,
control maps, protocol, event timing, LED bytes, MIDI feedback or audio algorithms.
Package identity does not establish accepted devices or broaden all 149 profiles.

### Q-APCC-001

Matching Python3.11/header/data decoding establishes only literal code evidence; it does not execute or validate module imports, creator/classes or get_capabilities in Live.

### Q-APCC-002

Key/property globals and controller/port helper results remain opaque. No framework module was read, imported or called; missing auto-load declaration never implies False/default.

### Q-APCC-003

Single-string versus list model-name inputs, numeric vendor/product IDs and label spelling do not establish real device matching, normalization, alias, firmware/OS/edition support.

### Q-APCC-004

Twenty-one declaration positions and input/output/property-symbol roles do not determine actual port count, number, names, visibility, routing or Sync/Remote functionality. APC64 and mk2 declarations differ and must not be flattened.

### Q-APCC-005

Creators, class/type configuration, imports and framework side effects/branches/exceptions remain outside the literal scope and unexecuted.

### Q-APCC-006

Actual MIDI/LED/protocol/timing/output, failed/missing ports, detection/activation, persistence/cancel/reconnect/teardown require separately authorized genuine positive hardware/host evidence; no simulation or borrowed mapping law.

## Future cases and frozen validation

There are43 requirements (37 S-literal metadata contexts/6 U) and49 future cases,
with zero actual documentary or target expected/comparison values. All target
grades U, executed false, complete profiles zero. Positive context requires an
independently known initialized genuine controller/profile/firmware/host and usable
ports; audible tests add active nonzero inputs/amount/gain, nonmuted output and
calibrated positive baseline. Missing hardware, port, feature, silent output or
failed baseline remains inconclusive. No such fixture is supplied; no fake controller,
helper return or runtime is invented to satisfy it.

The [read-only validator](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/validate.py) uses the same existing matching
interpreter: `/home/ollie/.local/bin/python3.11 -I -B analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/validate.py`.
It checks original baseline/source/owner pins, raw headers/code objects, literal/
symbol/offset provenance, decoder rejection selfchecks,43 exact Browser IDs, cases/
nulls, links, two canonical snapshots and untracked-aware whitespace. It prints to
stdout and never rewrites source or frozen reports. [Manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/apc-controller-capabilities/manifest-author-r1.json)
seals this partial revision for independent review. Shared catalogs/coverage/log
are root-owned, with implementation and Amp/Cabinet blocker unchanged.
