---
id: SRC-MIDI-USER-MAPPING-1243
type: source
status: current
updated: 2026-10-09
access: analysis
target: Ableton Live 12 Suite 12.4.3
---

# MIDI user mapping sources, Live 12.4.3

This capture narrows the [installed package](ableton-live-12.4.3.md) to the
user-defined controller configuration and its parser/mapping paths. Target:
`12.4.3 (2026-07-07_e3d8be4d07)`. Captured 2026-10-09 America/Los_Angeles.
The original package was not changed or launched.

## Retention and provenance

The [primary manifest](../../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/source-manifest.json)
records original absolute paths, retained paths, sizes and SHA-256 for two shipped
documents and twelve bytecode files. Three more files (mode declarations and
bundled configuration parser) are in the [supplemental manifest](../../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/supplemental-source-manifest.json).
The [toggle manifest](../../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/toggle-source-manifest.json)
and [matrix manifest](../../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/button-matrix-source-manifest.json)
identify two further dependency captures. Total: nineteen source files,
including seventeen CPython bytecode modules. The files are retained under
`analysis/ableton-live-12.4.3/midi-user-mapping-v1/source/`; local ignored storage
is not an off-machine backup or an approved implementation input.

| Document | SHA-256 | Relevant locations |
| --- | --- | --- |
| `_Tools/UserConfiguration.txt` | `52ec71be0a51fd89a0d1cebebc9a3f7c2a2cb62f6a55d25e7a4be3b3228322a4` | Lines 5–55 rules/modes; 59–99 pads; 103–171 devices; 175–292 mixer; 296–340 transport |
| `_Tools/InstantMappings-HowTo.txt` | `6d710bba5610cba5c17213fc46472fb87843857fcba8d28f6f838d69aa1554ef` | Lines 8–22 naming, placement and scope |

## Decoding method

[xdis](https://github.com/rocky/python-xdis) 6.3.0 decoded the captured bytecode
as CPython 3.11 (magic 3495 / `a70d0d0a`). This is cross-version static
disassembly, not execution or import of the target modules. The tool ran in a
local isolated Python 3.12.11 environment with click 8.5.0 and six 1.17.0.
The [disassembly manifest](../../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/disassembly-manifest.json)
retains command, package versions and hashes for the initial twelve outputs;
supplemental manifests pin the other five outputs. The retained
[decoder script](../../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/disassemble.py)
uses classic disassembly with code offsets and no source execution. It writes
outputs: use a new capture directory if repeating it, preserving this evidence.
Representation text can contain process-specific code-object addresses; do not
expect a later textual disassembly to have the same hash.

The tool installation used the already available Python 3.12.11 interpreter to
create `midi-user-mapping-v1/tooling`, then ran its Python with
`-m pip install --disable-pip-version-check 'xdis==6.3.0'`. It did not change the
system Python. Upstream README consulted 2026-10-09; installed versions and
retained artifacts, rather than that mutable README, identify this analysis.

The final [artifact inventory](../../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/artifact-checksums.json)
pins the retained capture, findings, case plan and review payloads; it excludes
the local tooling environment and the inventory itself.

## What the evidence establishes

Shipped documentation directly establishes the described interface and template
values. Decoded branches support conditional derivations of parsing, assignment
selection and button handling. They do not establish that a host dispatches each
path, native MIDI transformation arithmetic, actual GUI errors, audio effects,
latency or compatibility. Native property effects remain outside these Python
traces. No original-versus-candidate comparison was performed.

Canonical conclusions: [mapping research](../midi-user-mapping.md).
Candidate contract: [MIDI mapping draft](../../specs/midi-user-mapping.md).
