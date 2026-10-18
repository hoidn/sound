---
id: ADR-0002
type: decision
status: adopted
updated: 2026-10-18
access: neutral
---

# ADR 0002: Static-first analysis and targeted runtime checks

## Decision and authority

Adopted by user direction on 2026-10-09: "demote runtime interaction as much as
is possible / reasonable". This is research-process policy, not evidence of
original behavior or a claim about typical LLM reimplementation practice.

Use versioned documentation, shipped resources, schemas, scripts, saved examples,
and focused decompilation as the default inputs to behavioral specifications.
Do not require a reference execution before beginning each feature or drafting
its specification. Prefer bounded analysis over whole-binary decompilation.

> Narrowed 2026-10-18 by [ADR 0003](adr-0003-no-reference-execution.md): no whole-application reference
> execution is available; extracted execution of original x86_64 functions
> replaces it where possible.

## Runtime escalation rule

Use original-program execution only when a material question remains after
reasonable static investigation, when a small experiment is clearly cheaper
than further tracing, or when a declared compatibility claim needs measured
evidence. Record the question, existing evidence, reason for execution, minimal
inputs, expected discriminating observation, and stopping condition first.

Reuse retained captures. Prefer deterministic file/API/MIDI/audio harnesses
where available and validated. Use UI interaction for behavior that requires
it; broad GUI exploration and a general GUI automation framework are not default
prerequisites. Tool or API availability must be established before relying on it.
This rule does not authorize new tooling installation or broad runtime analysis.

## Specification and verification boundary

Static evidence can support a reviewed behavioral contract without a prior
runtime capture when its relevant paths, assumptions, inputs and outputs are
sufficiently established. Record derived expected outputs as static derivations,
never as observed execution. Unresolved details remain unknown, or are explicitly
excluded from the release; do not invent expected behavior to unblock a handoff.

Handoff review still removes recovered code and internal implementation structure.
Runtime-dependent questions may include effective scheduling, latency, jitter,
host/device interaction and audio output where numerical fidelity is required.
These need targeted measurements before claiming empirical compatibility.
Static confidence, spec release and passing candidate tests do not constitute an
original-versus-candidate comparison. Existing verification criteria still apply.

## Consequences

Research and spec drafting can progress without operating the original UI.
Runtime work becomes an explicit exception and a later validation activity.
Some contracts can be released while reference compatibility remains unverified;
their remaining validation obligations must stay visible. No evidence or released
payload is rewritten by this decision.
