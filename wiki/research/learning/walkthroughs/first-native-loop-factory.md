---
id: LEARN-FIRST-NATIVE-LOOP-FACTORY
type: research
status: current
updated: 2026-10-09
access: analysis
target: Ableton Live 12 Suite 12.4.3 arm64
---

# Reading the first main Live function

**Can a function named for `LoopOn` tell us the default loop setting?** We now
have real decompiled code from Live's main executable. It shows a small setup
function, but it does not answer that behavior question. This lesson explains
what we can read, how the machine instructions help, and which next inspection
would be informative.

Start with the [method guide](../method.md) if “symbol,” “assembly,” or
“pseudocode” is unfamiliar. The [transport study](../../native-transport-study.md)
owns the question and detailed findings. This walkthrough explains those
findings; it is not a new behavior contract.

## Why this function

The retained schema declares a `LoopOn` field whose `Value` class is `Bool`, and
the bundled default set stores `false`. Neither establishes Live's rule for an
absent field or the value created by a new runtime object. The symbol index
contains `TPtr<ACompound> SNewCompound<ALoopOn>()` at `0x10276e5d4`. That name
makes it a useful construction-related search seed, rather than evidence of a
parser or default. The [study's evidence table](../../native-transport-study.md#evidence-already-available)
pins the schema, fixture and symbol locations.

## Open the actual artifacts

The selected-function export contains:

- [Pseudocode](../../../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v1/functions/0x10276e5d4/pseudocode.c): 391 bytes of reconstructed C-like text.
- [Assembly](../../../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v1/functions/0x10276e5d4/assembly.txt): 26 ARM64 instructions, covering a 104-byte recovered body.
- [Metadata](../../../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v1/functions/0x10276e5d4/metadata.json): address, profile, body limits and uncertainties.
- [Run configuration](../../../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v1/run.json) and [sealed hashes](../../../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v1/manifest.json): input and method provenance.

The target is the retained arm64 Live image with SHA-256
`3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad`.
The profile is `ghidra-selected-entry-noanalysis-v1`, using Ghidra 12.1.4.
The [actual command](../../../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v1/command.json)
imports the binary with automatic analysis disabled, then runs a custom script
that disassembles a bounded region, creates the selected function and requests
decompilation. Its allowed window is 4,096 bytes; the recovered body is 104
bytes. These are different quantities.

This was a bounded fallback after the default analysis run crossed its disk
floor. The retained [stop record](../../../../analysis/ableton-live-12.4.3/native-live-arm64-v1/transport-pilot-v2/RESOURCE_STOP.json)
records that resource stop. This targeted export is a separate profile, not a
completed whole-image inventory or an interchangeable default-analysis result.
Its [run status](../../../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v1/run-status.json)
records successful export, exit code 0, about 21.36 seconds and no surviving
owned processes. Analysis did not launch Live.

## Read a small piece of pseudocode

Lines 8–12 of the actual export are:

```c
  lVar1 = func_0x0001012d9734(0x78);
  puVar2 = (undefined8 *)func_0x0001015644d4();
  *puVar2 = &UNK_106803d50;
  puVar2[0xb] = &UNK_106803fc0;
  func_0x000101486414();
```

`func_...` means the call target has an address but no useful recovered name in
this view. `undefined8` is an eight-byte value with an unresolved meaningful
type. `UNK_...` labels an address the decompiler has not explained. These names
are aids for reading the output, not original source identifiers.

The first call receives `0x78`, or 120 in decimal. The next call supplies the
pointer through which two address values are written. The expression
`puVar2[0xb]` selects element 11 in the displayed eight-byte pointer type, which
corresponds to byte offset `0x58`, or 88. This arithmetic says where the write
occurs; it does not tell us what that field means.

The function name and shape suggest object setup. It is tempting to call the
first routine an allocator, the second a constructor, and the two address
values virtual-method tables. Those remain hypotheses until the callees and
referenced data support them. None of those hypotheses would by itself prove
the loop-enable default.

## Check the machine instructions

The assembly provides a useful cross-check without requiring you to understand
every instruction. ARM64 registers such as `x0` and `x20` hold values; `w0` is
the lower 32-bit view of `x0`. Here `bl` calls a target and `str` stores a value.

| Addresses in the assembly | Direct observation | What remains uncertain |
| --- | --- | --- |
| `0x10276e5e8`–`0x10276e5f0` | Put `0x78` in `w0`, call `0x1012d9734`, preserve returned `x0` in `x20` | What the callee does with 120 |
| `0x10276e5f4`–`0x10276e608` | Call `0x1015644d4`; store `0x106803d50` and `0x106803fc0` through its result at offsets 0 and `0x58` | Whether these are table pointers and what the pointed-to state represents |
| `0x10276e614`–`0x10276e61c` | Load, increment and store the 32-bit word at `x20 + 8` | Whether this is a reference count or another counter |
| `0x10276e620`–`0x10276e628` | Pass `x20` to `0x101482718`, then store `x20` through the saved incoming `x8` value | The complete calling convention and original source-level return type |

There is a subtle warning in the readable output: the second call is printed
with empty parentheses, yet the instructions leave the first call's result in
`x0` before that call. Empty parentheses in this incomplete decompilation do
not prove that the original function accepted no argument. We must inspect the
callee before interpreting its parameter use.

Similarly, metadata's recovered signature says `undefined ...(void)`, while
the rendered pseudocode declares a `long *param_1`. The assembly shows incoming
`x8` being saved and later used as a write destination. It does not supply the
original C++ declaration. This disagreement is a reason to treat the recovered
types as provisional. An empty `warnings` array does not remove the explicit
no-analysis limitations.

## What we learned and what to inspect next

We observed four direct calls and a short sequence of setup-like writes in one
main-Live function. Their addresses are in the
[retained findings](../../../../analysis/ableton-live-12.4.3/native-live-arm64-v1/behavior-preparation/loop-factory-findings-v1.json),
which also pins this excerpt and the checked artifacts. An exact address lookup
found no entries for those four targets or the two stored addresses in the
existing symbol TSV. That is a limitation of this index, not proof that the
targets lack meaning or cannot be analyzed.

The next discriminating check was the body reached at `0x1015644d4`, followed
by the post-write call at `0x101486414`. The coordinator ran those bounded
queries; the [persistence packet](../../native-transport-study.md#persistence-packet-after-the-callee-follow-up)
records their actual results. Readers can inspect the retained files without
starting another analyzer.

## A follow-up found a zero write but not a default rule

The [first callee's assembly](../../../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v3/functions/0x1015644d4/assembly.txt)
contains this instruction:

```text
0x1015644fc: strh wzr,[x0, #0x60]
```

This writes a 16-bit zero at an address 96 bytes beyond the pointer in `x0`.
The same function installs a pointer whose displayed symbol names
`ARemoteableBool` and `SDefaultController`. Boolean-related setup is now a better
supported hypothesis. It is still not a demonstrated `LoopOn=false` rule:
we have not established which field those two cleared bytes represent, whether
later code changes them, or how the file reader connects to them.

The [other callee](../../../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v3/functions/0x101486414/pseudocode.c)
traverses entries obtained through an indirect call and writes entry pointers
to computed destinations. It adds a setup/registration lead but does not expose
a proved field reader or writer. The next discriminating work is that missing
field connection. The fact that the shipped fixture also contains `false`
cannot substitute for it.

**Reader exercise:** does the number `0x78` establish a default tempo of 120?
No. It is an argument to an unresolved callee inside a function named for
`ALoopOn`. Numerical equality is not a semantic connection. The same caution
prevents us from reading a loop default into unrelated setup instructions.

The [program atlas](../../program-structure.md#first-main-native-call-edges)
now includes these static call edges. It still does not claim a native parser,
transport scheduler, runtime thread map or recovered application architecture.
