---
id: LESSON-NATIVE-INCOMING-REGISTERS
type: research
status: current
updated: 2026-10-12
access: analysis
target: Ableton Live 12 Suite 12.4.3 arm64
---

# Why an apparently uninitialized variable can appear in decompiled code

The [retained pseudocode](../../../../analysis/ableton-live-12.4.3/native-live-arm64-v1/functions/0x100002000/ev_10bfc42a7e873004f14b7ebf76339ebad410aca4947c6aac11aec86a28d75f02-0/pseudocode.c)
for `FUN_100002000` declares `int in_w5;` and immediately tests it. In ordinary
C, reading such an uninitialized automatic integer would be undefined behavior.
Here the text is a decompiler reconstruction, and the name records a value in
a CPU register at entry. It is not proof that Ableton's source declared this local.

Ghidra's [official troubleshooting guide](https://ghidra.re/ghidra_docs/GhidraClass/Advanced/improvingDisassemblyAndDecompilation.pdf)
discusses `in_`/`unaff_` variables on displayed slide 93, PDF page 100: they can
indicate a register read before a write that the decompiler has not represented
as a parameter. Slides 96–97 describe checking signatures and calling conventions.
Retrieved 2026-10-12; the online guide is unversioned and its original bytes were
not archived by this query.

## Check the instructions instead of initializing the pseudocode

**Observed:** a bounded, read-only LLVM disassembly of this exact arm64 target
produces seven instructions, from `0x100002000` through `0x100002018`. The
[capture](../../../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/input-register-reading-v1/assembly.txt)
and [executed command](../../../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/input-register-reading-v1/command.json)
pin target SHA `3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad`.
The first instruction is:

```asm
cbz w5, 0x100002010
```

This branches when the incoming 32-bit `w5` value is zero. There is no earlier
assignment within the inspected entry. `w5` is the 32-bit view of the register
also addressed as `x5`; see [AAPCS64, section 6.1.1](https://github.com/ARM-software/abi-aa/blob/main/aapcs64/aapcs64.rst#611general-purpose-registers)
(retrieved 2026-10-12; moving upstream document, not archived).

The remaining instructions show more than the exported C-like text:

| Incoming value | Register preparation after the test | Direct branch |
| --- | --- | --- |
| Nonzero | `adrp` + `add` load `x5 = 0x100002594` | `b 0x1000cedd0` |
| Zero | `adrp` + `add` load `x5 = 0x1000028d4` | `b 0x1000cf028` |

These are direct jumps, not `bl` call instructions followed by a local `ret`.
**Inferred:** this entry acts as a small dispatcher with tail transfers, and
the decompiler's inferred prototypes hide the outgoing `x5` preparation. The
two-branch selection is grounded in the instructions; the apparent no-argument
calls and `void` signature are not established source-level interfaces.

## What remains unknown

The caller may supply the tested register through an ordinary argument or another
calling convention. AAPCS64 uses `x0`–`x7` for general-purpose argument values,
but this alone does not establish the original argument count, order or types.
The caller, both target interfaces and meanings of the two prepared addresses
were not examined. No Live execution or DAW feature behavior was observed.

Do not repair the capture by inserting `in_w5 = 0`: that would force one branch
and change the behavior represented by the instructions. Preserve the original
text and put interpretations here. The [revision metadata](../../../../analysis/ableton-live-12.4.3/native-live-arm64-v1/functions/0x100002000/ev_10bfc42a7e873004f14b7ebf76339ebad410aca4947c6aac11aec86a28d75f02-0/metadata.json)
reports no warnings; absence of warnings does not certify a recovered signature
or complete register/argument semantics.
