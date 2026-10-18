---
id: NAV-RE-LEARNING
type: index
status: active
updated: 2026-10-17
access: analysis
---

# Learn how this investigation works

We are examining one pinned Ableton Live 12.4.3 distribution and turning selected
findings into behavioral contracts. These pages explain the reasoning in ordinary
language, with links to the actual files. They are analyst materials, not clean
implementation inputs.

Start with the [method guide](method.md), then the [program atlas](../program-structure.md).
The guide explains what symbols, disassembly and decompiled code can tell us.
The atlas distinguishes what is inside the application package from what we have
learned about relationships in its code.

## Worked investigations

| Lesson | What you will learn | Evidence boundary |
| --- | --- | --- |
| [Why an invalid controller number is sometimes ignored](walkthroughs/midi-integer-parsing.md) | Follow a real branch and exception handler in decoded Python bytecode; check the caller before generalizing | Static parser result; no Live execution or native audio/MIDI inference |
| [Reading the first main Live function](walkthroughs/first-native-loop-factory.md) | Compare actual pseudocode with ARM64 instructions; distinguish a setup hypothesis from a loop-default claim | One selected function under an explicit no-analysis profile; native callees and persistence behavior unresolved |
| [Why a decompiled variable looks uninitialized](walkthroughs/incoming-registers.md) | Recognize an incoming register, check branch instructions and notice hidden outgoing arguments | Seven instructions from one arm64 entry; callers, prototypes and feature meaning unresolved |
| [Why code archives and analysis databases differ](walkthroughs/artifact-storage-and-recovery.md) | Disk allocation, exact archives, evidence/commit boundaries, cancellation and fixture limits | Mirror and reader delivered; actual target import/save passes, reopening capacity-blocked |
| [Learning from a transport export failure](walkthroughs/transport-wrapper-boundary.md) | Read a retained branch when a selected body fails acceptance; separate batch completion from successful decompilation | Two wrapper branch targets, with handler semantics and playback effects unresolved |
| [Resolving an indirect call](walkthroughs/transport-dispatch.md) | Resolve a `blr` through constructor-stored vtables and RTTI; name functions from a donor build; find a message consumer through its registration | Static; donor names are inferred matches; runtime timing unresolved |
| [Following LoopOn Value="true" into Live](walkthroughs/transport-state-reader.md) | Find a parser by its error message, read an exact-match branch, follow a value to an object offset through a member registry | Parser, loader and constructor traced statically; top-level load, error dialog and engine use unresolved |
| [Following one attribute: how Live decides a set's version is acceptable](walkthroughs/document-version-check.md) | Trace MajorVersion from the root reader through the integer parser and version check to the post-parse decision; check a notes summary against disassembly | Static reading of retained disassembly; the catch step, dialog text and File > Open's reading path are unresolved |

The native lesson uses actual main-image code; the bytecode companion remains a
separate kind of evidence. To inspect current code immediately, use the [artifact catalog](../artifacts/index.md),
including its warnings and coverage labels.

On the Linux workstation, most evidence links in these lessons point into the
macOS `analysis/` tree, which has not been copied here (gate G0.2 in the
[execution ledger](../native-phase-execution.md#gate-ledger)). The linked
findings pages still say what was observed. The bytecode lesson also links a
re-decode that is present on this host.

## Revision 2 so far

Native lessons now exist for the transport fields, the version check and the
transport dispatch (rows above). Each revision 2 packet gets its lesson once its
native half has traced code. For the outside-in route itself, the [method guide](method.md#start-from-what-live-stores-or-shows)
explains the outside-in route using the static halves of the
[container packet](../document-container-static.md) and the
[transport-state packet](../transport-state-static.md). The
[MIDI closure assessment](../midi-closure-r2.md) re-established the bytecode
evidence behind the first lesson and classified every draft MIDI clause. Its
supportable clauses shipped as [midi-config-v2](../../../handoff/midi-config-v2/README.md),
which supersedes v1. To read whole decompiled programs, use the
[revision 2 corpus browsers](../../../analysis/ableton-live-12.4.3/browse/r2/r2-index.html):
Push2 and 15 helper executables so far, with main Live to follow.

## Interactive demos

| Demo | What you can do | Evidence boundary |
| --- | --- | --- |
| [Corpus resonator](demos/corpus-resonator.md) | Excite a resonator with clicks, noise, a drum loop, a file or a microphone; change type, decay, strike and pickup positions; load the 26 shipped presets; see the modes and the spectrum | Controls, ranges and presets observed in shipped files; the sound is a labelled textbook stand-in, not Corpus's algorithm |
| [Corpus traced engine](../../../analysis/ableton-live-12.4.3/demos/corpus-traced/index.html) | The same controls and presets driving a port of Corpus's own signal chain, traced from the decompiled bundle; compare it with the stand-in | Derived from recovered code; not compared with Corpus's real output; how Live converts four controls is assumed ([DSP page](../corpus-dsp-static.md)) |

## Continue exploring

- [Learning design and task plan](design-and-plan.md): deliverables, review checks and current status.
- [MIDI investigation](../midi-user-mapping.md): canonical conclusions behind the first lesson.
- [Native phase roadmap](../native-decompilation-roadmap.md): export, behavioral and teaching milestones.
- [Research index](../index.md): all analyst topics and source records.

The distinction to keep throughout: readable code is an artifact, an explanation
is an interpretation, and a compatibility claim needs evidence for its stated
cases. One does not automatically establish the next.
