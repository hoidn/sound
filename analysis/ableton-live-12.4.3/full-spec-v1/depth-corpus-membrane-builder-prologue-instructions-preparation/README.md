# Membrane builder prologue: fixed 148-byte static decode preparation

Preparation only, pending Root's full preflight and separate actual selection.
No new instruction-window extraction, collector/decoder invocation or original
instruction execution has occurred. The exact future destination is separate
and must remain absent.

[proposal.json](proposal.json) selects only [0x243e8,0x2447c), 148 bytes/37 ARM64
slots, through the indexed computed BR at24478. The reviewed C base expression
and the prior [12-byte static result](../reviews/corpus-membrane-builder-call-static-actual-review.json)
leave X20's origin and incoming W1 unresolved. The future window asks whether
base/count definitions and preservation up to that branch are visible. It does
not follow branch targets, callees or table words; case4's24888 target stays
outside this window. Nothing substitutes a presumed table count70.

[inputs.json](inputs.json) pins the original reviewed sources, image and installed
decoder plus the exact prior R2 preparation, actual12B manifest and independent
actual review. [delta.json](delta.json) retains all22 parent-preparation/actual
file identities and seven reversible collector operations. Only fixed scope,
range/row/rawfile/status labels, destination and mapping change; all other
collector logic remains byte-exact R2. Its invalid/ill/None row guards and
one-attempt/failure accounting remain unchanged. No old module/main is run.

[header-map.json](header-map.json) preserves the verified full image identity,
MachO header/load-command bytes and segments. Unique file-backed TEXT mapping
gives fileoffset148456. Preparation hashes the image as data and rereads only
header/load commands for mapping; it does not extract the selected window.

Read the full [collect-once.py](collect-once.py) before any separate selection.
It would create one exclusive destination, retain before/attempt/returned-PID/
status/after receipts, extract exactly148 bytes, and run the pinned installed
rizin only once with raw/noinit/noexecute flags, `-f` and `pdj 37`. All37 rows
must have correct offsets/size4, valid type/opcode and exact byte roundtrip.
Timeout30seconds/core0, no retry or automatic expansion. Timeout stdout/stderr
is retained after killing that same child. Pre-directory refusal and catastrophic
receipt I/O still require coordinator outer receipts, without blanket guarantees.

Read [check.py](check.py) before its read-only command:

```sh
python3 -B analysis/ableton-live-12.4.3/full-spec-v1/depth-corpus-membrane-builder-prologue-instructions-preparation/check.py --check
```

The check validates exact inputs/parents/header/map, reversible fixed collector
operations, eight scope/flag guard mutations and ten invalid-row sets using only
selected synthetic AST predicates. A valid synthetic37-row control remains
accepted. No collector function/module, decoder, old tool, instruction or model
is executed. Decoder success alone would establish no actual W1 value, runtime
path/object state, source-to-x86 correspondence, physical006 mode, pole or new
criterion. All174+2 omitted observations remain ungraded. No owner/case/shared/
release modification or broader source analysis is proposed.
