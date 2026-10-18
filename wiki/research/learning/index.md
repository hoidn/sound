---
id: NAV-RE-LEARNING
type: index
status: active
updated: 2026-10-12
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

The native lesson uses actual main-image code; the bytecode companion remains a
separate kind of evidence. To inspect current code immediately, use the [artifact catalog](../artifacts/index.md),
including its warnings and coverage labels.

## Continue exploring

- [Learning design and task plan](design-and-plan.md): deliverables, review checks and current status.
- [MIDI investigation](../midi-user-mapping.md): canonical conclusions behind the first lesson.
- [Native phase roadmap](../native-decompilation-roadmap.md): export, behavioral and teaching milestones.
- [Research index](../index.md): all analyst topics and source records.

The distinction to keep throughout: readable code is an artifact, an explanation
is an interpretation, and a compatibility claim needs evidence for its stated
cases. One does not automatically establish the next.
