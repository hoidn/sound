# Complete MIDI-user relative-byte class, existing UNIT state

Root selected this author packet and is the sole independent actual/source peer
after final seal. No approval or application grade is claimed by this author.

The bounded inventory is all eight relative mode codes `{1,2,3,4,6,7,8,9}` times
all legal seven-bit data bytes `0..127`: 1,024 logical rows. Exact 18 matching X1
observations are inherited by citation, not executed. All other 1,006 rows are
selected for eight sequential original-code children, one per mode, each preceded
by the already recorded unit initializer. Total selected original calls: 1,014.
The eight child target counts are 127/126/126/125/126/124/126/126, respectively;
maximum total calls per child is 128 and maximum supplied buffers is 127.

## Fixed method and inputs

Existing direct X1 `run_pilot.py:219–225` and X2 `run_x2.py:507–523` protocols
are retained in `protocol-source.json`. No old Python module is imported or run.
The unchanged existing loader and Live x86 image are freshly hashed for custody
only. The original unit initializer at `0x101bc1360` runs once per child. Each
target call at `0x101bb27b0` receives these exact supplied inputs:

- current `0.5f`: lower XMM0 bits `3f000000`, token `f:0x1.0000000000000p-1`;
- range `{0.0f,1.0f}`: XMM1 carrier `3f80000000000000`, token
  `d:0x1.0000000000000p-7`; this is a packed pair, not a scalar range argument;
- RDI points to a separate 16-byte owned buffer, little endian
  `{float32(byte), uint32(0x7f7fffff), int32(mode), float32(1)}`;
- ESI quantized=0; EDX reversed=0.

The low binary32 lane of returned XMM0 is the sole semantic return projection.
Full saved 64-bit RAX/RDX/XMM0/XMM1 carriers and all `out bN` bytes/addresses are
retained as raw observations. This is not a fresh entry-register trace or formal
ABI proof; the protocol is inherited from reviewed calls. The supplied data
buffers must remain byte-identical. The host libc parser tokens, conversion to
temporary float even for the `d:` argument, endianness and actual packed bytes
are checked before calls. Per-child floating environment/flags are not traced.

## Oracle and historical controls

The current r6 REQ005 integer relative table is frozen literally in the owned
recorder. At this fixed state the result is `.5 + delta/256`; every result is an
exact dyadic binary32 number in `[.25,.75]`. No clipping fit, new tolerance or
portable floating-point law is introduced. `inputs.json` freezes all input bits,
expected output bits and current-clause oracle classification before any call.
Any discrepancy is retained, not repaired; later children stop.

The 18 controls are exact `(mode,byte)` pairs already reported to Root:
`1:{1}; 2:{65,70}; 3:{1,8}; 4:{0,1,7}; 6:{1,64};
7:{0,64,65,127}; 8:{1,65}; 9:{1,64}`. `inherited-controls.json` supplies exact
old X1 result pointers, original raw row/byte offsets and hashes. The selected
original raw JSONL records are copied byte-for-byte once into
`historical-controls.jsonl`. Original records lack PID/UTC; neither is invented.
The immutable v4 review and approved family review carry earlier semantics and
finite-observation approval by citation; this packet does not re-review them.

## Execution and integrity

`manifest-before.json` freezes all input/source/code/context payload hashes before
the first original call. `run_batch.py --run-once` refuses an existing attempts
directory and launches exactly the eight declared plans. No build, patch,
debugger, accessor/setter simulation, receiver, new object graph, helper discovery
or provider tooling is used. `harness-source.c` and
`harness-driver-source.py` are inert exact tooling copies for peer inspection.

Each child has DEVNULL stdin, recorded minimal C-locale environment, core limit0,
CPU/wall bound20s and a new process group. Timeout/interrupted waits kill the
selected group and reap the direct child. SIGTERM is handled by the outer
recorder; uncatchable outer death/escaped descendants and power-loss durability
are not proved. Raw stdout/stderr regular files are closed and hashed, not
explicitly fsynced; JSON bookkeeping is fsynced. No retry/fallback is available.
Raw outputs/partial failures, argv, PID, UTC, exit, elapsed time, memory output,
import declarations/use and phase/custody flags survive ordinary failures.

Expected import use per complete child is inherited from the selected direct X1
controls: `__Znwm=2`, `___cxa_atexit=3`, `_pthread_key_create=1`. Full binding
declarations are printed by the existing loader. Import use is reported after
its queued call loop: the outer recorder can stop later unlaunched children
after detecting an anomaly, not retroactively stop already queued calls in the
failing child. Image/tool/source/code identities are checked before and after
each child. Full-file hashes are custody only, not additional binary analysis.

`run_batch.py --check-inputs` performs only data/parser checks and 14 meaningful
input controls. `check_data.py --write-analysis`/`--check` imports only the new
owned inert recorder, reads only this packet, reproduces all 1,024 provenance
joins/1,006 fresh bit comparisons, and checks recorded/import/call/overlap/raw
negative controls. It never hashes/reopens runtime images or calls original code.

## Required contribution and limits

The complete legal-byte class extends finite evidence for REQ-MIDI-USER-005 /
MU-OUT-026 at the existing UNIT state. 1,024 inputs are not 1,024 new required
outcomes, all 19 X contexts, a continuum proof or a grade. There is no actual
MIDI ingress, parameter/current-value/registry binding, receiver accumulation,
pairing, takeover, notification, deferred delivery, lifecycle, ARM/Apple or
application behavior inference. All other axes and unsupported required behavior
remain U; family/product closure stays OPEN. No shared owner/release/wiki edits
or automatic successor are selected.
