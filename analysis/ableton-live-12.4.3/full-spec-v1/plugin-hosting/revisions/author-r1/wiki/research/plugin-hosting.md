---
id: RESEARCH-PLUGIN-HOSTING
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3
---

# Third-party plug-in hosting evidence

## Question and source

F-05 needs an observable hosting contract beyond scanner discovery. The
[canonical draft](../specs/plugin-hosting.md) owns the new workflow clauses;
existing [discovery](../specs/plugin-discovery.md) retains source enumeration,
scanner messages, database and scanner crash/restart scope. No scanner process
boundary is generalized to hosted device execution.

Official Version12 [Using Plug-Ins](https://www.ableton.com/en/live-manual/12/using-plug-ins/)
was captured with exact bytes, URL/final URL/time/size/digest in
[source.json](../../analysis/ableton-live-12.4.3/full-spec-v1/plugin-hosting/source.json).
HTML SHA-256 `df44bdab506fa5422fbe4da0fceaff6e8250e3117d9f5b53802889c83e3e7a1a`.
[Heading records](../../analysis/ableton-live-12.4.3/full-spec-v1/plugin-hosting/headings.json)
pin source lines and anchors. This is current major-version documentation, not
an immutable12.4.3 reference. All app expectations remain exact-build U.

## Findings and boundary

The useful new contract is parameter-list/editor/configuration state, warning
conditions and program/sidechain workflows. The64/65 boundary is documentary and
requires default-free, independently counted fixture inputs; hidden/read-only
counting rules remain U. Published versus unpublished parameters and editorless
plug-ins need separate capability fixtures. A parameter-deletion warning does not
establish what cancellation or confirmation preserves.

The sidechain Mute wording does not identify every affected routing branch;
the draft has a null-oracle interaction probe rather than asserting track mute.
VST program/bank prose is not blanket VST3 binary-format support. AU preset
extension spelling in this capture is ambiguous, so exact extensions and bytes
remain U. Vendor identity, opaque state, API callbacks, event/block scheduling,
latency, DSP and failures have no established oracle in this capture.

## Packet and validation

21 requirements and 40 finite declarative cases span positive,
negative, boundary, persistence, interaction, timing, malformed, error, cancel,
undo and teardown. Fixtures describe independently required capabilities; none
was provisioned, executed or graded. The packet manifest pins source and derived
artifacts. Separate semantic review is required before any release decision.
No original code, application, vendor binary, UI or candidate was executed.
