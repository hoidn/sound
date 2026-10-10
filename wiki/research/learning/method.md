---
id: GUIDE-RE-METHOD
type: research
status: current
updated: 2026-10-09
access: analysis
---

# Reading a program we did not write

The distributed application contains machine instructions and resources that a
computer can use. It does not contain the original source project in a form we
can simply reopen. Reverse engineering builds an explanation from those retained
artifacts. Our [artifact catalog](../artifacts/index.md) makes the evidence
readable; this guide explains how to approach it.

## Begin with a question and an identified file

A useful question has a boundary: “How does this parser handle an out-of-range
controller number?” is small enough to answer or leave explicitly unresolved.
“How does Live work?” is the long-term investigation, not a single code-reading
task. The [bytecode lesson](walkthroughs/midi-integer-parsing.md) demonstrates the
smaller kind of question.

Before inspecting code, check the source record. Our [package source](../sources/ableton-live-12.4.3.md)
pins the build and hashes; the [MIDI source](../sources/midi-user-mapping-12.4.3.md)
pins copied modules and decoder provenance. A hash identifies exact bytes. It
does not prove that a tool interpreted them correctly. Native addresses also need
the architecture and image: an arm64 address does not identify a function in the
Intel slice or a later release.

## Choose the representation that answers the question

| Representation | What it gives you | What it does not give you |
| --- | --- | --- |
| Package tree | Files and components shipped together | Runtime process or signal routing |
| Symbol table | Retained names associated with addresses | Complete original names or verified function behavior |
| Disassembly | Decoded machine instructions, or decoded virtual-machine opcodes for bytecode | Original high-level source syntax |
| Decompiled pseudocode | A tool's reconstruction into C-like control flow and expressions | Original C++, reliable types everywhere, or buildable source |
| Call/reference table | Statically identified uses of functions, strings or data | Proof a branch executes or a complete account of indirect calls |
| Resource/schema | Stored structure or shipped sample content | Every runtime default, accepted value or format migration rule |

For example, the package ships a default set whose creator label predates the
installed executable. Its stored tempo is evidence about that fixture, not a
measurement of launching the current application. The [package research](../ableton-package-structure.md#resources-that-can-ground-specifications)
records this distinction and the exact source.

## Why opening the file does not immediately produce source

The [REA full-inventory route](../native-export-design.md) has separate stages.
Opening the arm64 file establishes that the provider accepts the target. The
first deep query starts Ghidra's analysis of code and data; an accepted file is
therefore not yet a completed function inventory. A later pseudocode request
uses the analyzed program to reconstruct a selected function. Exporting that
text makes it readable, but does not establish that its interpretation is correct.

We record these distinctions explicitly: **opened**, **inventoried**, **exported**,
**interpreted**, and **behaviorally compared** describe different accomplishments.
Export counts measure which discovered functions produced text. They do not
measure how much of Live we understand or how closely a replacement behaves.
The [execution ledger](../native-phase-execution.md) records actual progress,
including warnings and unfinished steps.

The current REA provider also keeps its native analysis in a temporary session.
Keeping that session alive avoids repeating initialization between queries.
A saved query snapshot preserves supported results, not the full native analysis
database; a new uncached query after restarting can require analysis again.
That is why we measure startup cost separately from per-function export speed,
and why the corpus stores durable text and provenance outside that session.
These are properties of our inspected tool route, not properties of Ableton's
original source organization.

We also have a bounded selected-function route. After the default analysis hit
its disk floor, a custom Ghidra script imported the same binary with automatic
analysis disabled, disassembled selected address windows and exported accepted
bodies. The [first main-code lesson](walkthroughs/first-native-loop-factory.md)
links its actual command, profile and output. This produces useful code sooner,
with less recovered context: uncertain types, incomplete indirect targets and
rejected bodies remain visible. It supplies no whole-image function inventory,
and its counts must stay separate from the REA full-inventory route. A failed
selected export can still preserve useful assembly, as the
[transport wrapper lesson](walkthroughs/transport-wrapper-boundary.md) shows.

## Read code as a chain of conditional claims

Locate the function, then identify its inputs, branches, calls and exits. Read
the smallest section that affects the question, and follow a dependency when it
could change the conclusion. A meaningful-looking name is a search seed: check
the instructions or pseudocode before assigning responsibility to it.

When reading pseudocode, treat `param_1`, `local_...`, casts and guessed structures
as the decompiler's representation unless supporting metadata says more.
Warnings deserve inspection because they may affect recovered flow or types.
Keep unedited output and put explanatory names in separate annotations. The
existing [Push2 entry](../../../analysis/ableton-live-12.4.3/push2-entry-pseudocode.c)
is a real example with warnings; it belongs to the display helper, not main Live.

A call through a named address is easier to follow than a call through a pointer.
For a pointer call, the target may depend on an object, table or runtime state we
have not recovered. Stop at that boundary if the answer depends on it. Do not
turn a guessed target into a confirmed graph edge.

Likewise, a bytecode function's exception handler only establishes what that
function catches. The application may handle a propagated exception elsewhere.
In the [parser lesson](walkthroughs/midi-integer-parsing.md), this prevents us
from turning “raises here” into “Live displays an error dialog.”

## Record the conclusion at the strength the evidence supports

The [schema](../../schema.md#claim-and-evidence-conventions) defines the labels.
Use **observed** for the branch, value or file directly present in a retained
source; **inferred** for the conditional interpretation; **unknown** when a
necessary dependency or measurement is missing. A project design is **proposed**
or **decided**, rather than an observation about Live.

Static reasoning can support a bounded contract without executing Live. Runtime
claims such as latency, actual rendering or scheduling need their own evidence.
Under the [static-first policy](../../decisions/adr-0002-static-first-analysis.md),
a runtime probe is added for a material question or a cheaper discriminating
experiment, not as a universal prerequisite. Record the inputs and conditions
for either route. Review does not turn unexecuted cases into compatibility passes.

## A small glossary

| Term | Meaning here |
| --- | --- |
| Architecture slice | The part of a universal executable containing code for one processor family, such as arm64 |
| Function entry | The address an analyzer identifies as the start of a callable function; discovery can be incomplete |
| Static virtual address | Address in the analyzed image's load model; not a file byte offset or necessarily the address in a running process |
| ASLR | Runtime address randomization; a running image can be relocated from its static layout |
| Basic block | A run of instructions with no branch into its middle and a control-flow exit at the end |
| Control-flow graph | Possible branch paths between blocks, not a record of which path a run took |
| Direct / indirect call | A call with a statically named destination / one selected through a value such as a pointer |
| Cross-reference | An identified use of an address, string or other item; inspect its kind before treating it as a call |
| Bytecode offset | Instruction position inside a named virtual-machine code object; not a native arm64 address |
| Sentinel | A special value used to represent a condition, such as the parser's `-1` for an unassigned value |
| Corpus | The collected exports, with an inventory and explicit success/failure coverage |
| Handoff | A reviewed behavioral package that excludes recovered code and internal structure; see the [release workflow](../../workflows.md#release-a-handoff) |

Return to the [learning index](index.md) to follow a real investigation.
