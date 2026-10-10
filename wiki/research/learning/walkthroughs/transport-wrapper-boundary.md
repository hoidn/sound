---
id: LEARN-TRANSPORT-WRAPPER-BOUNDARY
type: research
status: current
updated: 2026-10-09
access: analysis
target: Ableton Live 12 Suite 12.4.3 arm64
---

# Learning from a transport export failure

**Why did a three-instruction function fail to produce pseudocode?** The selected
function export rejected a branch that left its recovered body. That failure
still preserved useful assembly: two concrete next addresses for investigating
Start and Stop. Reading the failure precisely keeps the investigation moving
without pretending that a wrapper explains playback.

This follows the [first native lesson](first-native-loop-factory.md). The
[transport study](../../native-transport-study.md#transport-wrapper-findings)
owns the findings and proposed Start→Stop cases.

## The question and actual route

We want to know which state changes follow Start and Stop requests. The retained
symbol index names callback wrappers referring to `ATransport::OnStart` at
`0x102770a58` and `ATransport::OnStop` at `0x102770a64`. The names suggest useful
entry points but do not establish a GUI action's path or the handler bodies.

The second selected export used the same pinned arm64 Live binary and
`ghidra-selected-entry-noanalysis-v1` profile as the first lesson. Its
[configuration](../../../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v2/run.json)
and [manifest](../../../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v2/manifest.json)
retain the exact inputs, method and output hashes. We read the result metadata
before treating any file as successful pseudocode.

The [Start metadata](../../../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v2/functions/0x102770a58/metadata.json)
reports `state: failed` with `Non-call transfer outside recovered body:
10276a7b0`. Its recovered body is only 12 bytes. The
[Stop metadata](../../../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v2/functions/0x102770a64/metadata.json)
records the corresponding failure for target `102767b70`. These are per-item
failures even though the batch process itself exited successfully. Neither is
a successfully decompiled function.

## What the retained instructions say

The complete [Start assembly](../../../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v2/functions/0x102770a58/assembly.txt) is:

```text
0x102770a58: mov w1,#0x1
0x102770a5c: mov w2,#0x1
0x102770a60: b 0x10276a7b0
```

Two registers receive the number one, then `b` transfers control to another
address. Unlike the `bl` calls in the first lesson, this is a direct branch
without recording a new return address. A forwarding or tail-transfer wrapper
is a plausible interpretation. Its target lies outside the small body retained
here, so the exporter refuses to present a complete C-like function for it.

The entire [Stop assembly](../../../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v2/functions/0x102770a64/assembly.txt) is shorter:

```text
0x102770a64: b 0x102767b70
```

There is no visible write to a “playing” flag in either excerpt. Nor do the
numbers in `w1` and `w2` tell us what those parameters mean. They could select
behavior within the target, but only inspecting its use of those registers can
support that interpretation. Calling both values “true” and naming the flags
from intuition would introduce unsupported semantics.

## Failure is evidence about a boundary

The guard's conclusion is narrow: this selected export did not recover a
self-contained body suitable for its pseudocode acceptance rule. It does not
prove that the program is malformed, that these functions never run, or that
the target addresses cannot be inspected.

The [retained wrapper findings](../../../../analysis/ableton-live-12.4.3/native-live-arm64-v1/behavior-preparation/transport-wrapper-findings-v1.json)
pin both complete excerpts and metadata. They support two static branch edges
and a precise follow-up: inspect `0x10276a7b0` and `0x102767b70` under the
coordinator's bounded native query procedure. That follow-up has now run.
The failures remain in coverage; later target exports are new evidence, not
retroactive success for these items.

## Following the branch uncovered another boundary

The [Start destination](../../../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v3/functions/0x10276a7b0/pseudocode.c)
exported successfully. The [Stop destination](../../../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v3/functions/0x102767b70/metadata.json)
still failed acceptance, this time because two transfers obtain their target
from a register: `br x2` at `0x102767c60` and `br x1` at `0x102767c98`.
The [retained assembly](../../../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v3/functions/0x102767b70/assembly.txt)
shows those register values loaded from pointer tables. A direct branch supplies
the next address in the instruction; a computed branch requires the missing
table/receiver information to resolve the target.

Both destination bodies contain a conditional call to the same address,
`0x101a4abd8`. Start's path prepares `w2=1, w3=0`; Stop's prepares `w2=0, w3=1`.
Both supply `w1=0x100500`. This is a useful shared code boundary, with exact
locators and guard conditions in the
[updated transport packet](../../native-transport-study.md#transport-packet-after-the-destination-follow-up).
It does not identify a “play” flag: that requires seeing how the common callee
uses the arguments and affects observable state. Other branches and calls
remain part of both operations.

Even a readable target body may contain an unresolved indirect call or a
request to another subsystem. Continue until the selected input can be joined
to an externally describable state change, or document that remaining boundary.
Real-time timing and audio behavior require their own observations.

**Reader exercise:** does the batch's exit code 0 establish that these wrappers
were decompiled successfully? No. Process completion and item acceptance are
different results. The item metadata records failure, while the assembly gives
us useful next targets. That distinction belongs in both the browser and the
[program atlas](../../program-structure.md#transport-wrapper-branches).


## When another profile produces code

Later, completed whole-image analysis produced
[default-profile Stop pseudocode](../../../../analysis/ableton-live-12.4.3/native-live-arm64-v1/functions/0x102767b70/ev_2bdece1772423ee0a8c327b787f71017b84e69af7d109ed21100070237fba02d-3/pseudocode.c).
Open it and search for `WARNING`. It reports unrecovered jumps at the same two
addresses and represents each indirect jump as a call. The selected profile
rejected those unresolved transfers; the default export retained pseudocode
with warnings. Both outcomes remain valid descriptions of their own methods.
Readable output is not evidence that the missing targets have been recovered.

The [shared-helper follow-up](../../native-transport-study.md#default-profile-comparison-and-shared-helper)
then traced the common call into a small record-building path. Instructions
show one eight-byte append and three one-byte appends, followed by an indirect
operation whose purpose is still unknown. This replaces one broad question
with a narrower one: who consumes that record, and how does consumption affect
externally visible state? Calling its bytes “play” and “stop” before answering
that question would still be a guess.
