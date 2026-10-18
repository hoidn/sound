---
id: ADR-0003
type: decision
status: adopted
updated: 2026-10-18
access: neutral
---

# ADR 0003: No reference execution; the project finishes on the Linux workstation

## Decision and authority

Adopted by user direction on 2026-10-18: "mac observation not possible; we are
finishing the proj on this x86 machine". No macOS host is available. Neither
Mach-O slice of the reference build can run on the Linux x86_64 workstation, and
no compatibility layer is authorized. All remaining analysis, specification,
handoff, implementation and validation work happens on this workstation.

This decision narrows [ADR 0002](adr-0002-static-first-analysis.md). Static
evidence becomes the only source of reference behavior. That evidence is the
decompiled arm64 and x86_64 corpora, shipped resources, schemas, scripts and
saved documents, and published documentation.

## Extracted execution of original code

Amended by user direction on 2026-10-18: "integration test style observation is
still possible if you can compile portions of the original program on this
machine". The whole application cannot run here, but some of its own machine code can.

- **What is permitted.** The x86_64 slice can be loaded into a harness process on this
  host, and self-contained functions can be called with recorded inputs. macOS
  x86_64 and Linux x86_64 share the System V AMD64 calling convention. Execution of
  the shipped bytes counts as reference evidence of a new kind, labelled X
  (extracted execution).
- **What it shows.** It shows what the original code computes for the given
  inputs. It does not show how the application reaches that code, what state
  it holds there, or what the user sees. The harness supplies the setup, and
  every stub or replaced import is recorded with the result.
- **Slice.** Results bind to the x86_64 slice. The release target is the arm64
  slice, so arm64 equivalence is an inference. It must be checked by comparing the
  two slices' code statically, and noted wherever floating-point evaluation could
  differ (for example, fused multiply-add on arm64).
- **Recompiled decompiler output** is a static derivation, not X evidence,
  unless it is checked against X runs of the same function.
- **Tooling.** Only tools already installed are used (gcc, gdb, objdump). Adding an
  emulator for the arm64 slice needs separate user approval.

## Consequences

- **Runtime escalation.** ADR 0002's escalation rule has no whole-application
  path. A question that would have needed observation is answered by
  extracted execution where the behavior lives in a self-contained function.
  Otherwise it is answered statically or stays unknown. Unknown behavior is excluded from releases, never guessed.
- **Phase 4 probes.** The [probe batch](../research/phase4-probe-batch.md) will
  not run as planned. It is kept as the record of what observation would have
  settled. Each probe's question becomes an extracted-execution target, a
  static investigation target or a permanent unknown.
- **Specs.** A clause or case that waits on a probe stays unknown or ungraded
  and cites this decision. A static derivation stays labelled static. Neither
  is ever relabelled as observed.
- **Releases.** Released payloads are not rewritten. Their "comparison not-run"
  obligations are now permanent: no original-versus-candidate comparison will
  happen. Extracted-execution results may support a later release revision.
- **Verification.** Candidate checks compare against released expectations, which are
  static-derived or, where available, from extracted execution. Reports must say so and must not claim compatibility with
  Live. Where coverage would show a reference comparison, it records it as
  unavailable.
- **Implementation.** The candidate is built and tested on this Linux x86_64
  workstation. Clean-room separation still applies (ADR 0001, AGENTS.md).
  Implementation needs a separately restricted workspace with only released
  handoffs and neutral governance. This decision does not provision one.
