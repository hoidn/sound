# Pickup-step finite waveform method proposal

**Proposal only. No metric run, new evaluator, owner/case or handoff adoption.**

Propose a new direct waveform criterion for the exact same-instance left pickup
step under REQ-DEVICE-CORPUS-012. Score two fixed regions separately: productive
baseline[4096,8192) and response[8192,16384), left/right individually. Four
relative RMS errors must each be <=0.01 with binary64 arithmetic and math.fsum.
Full files must be finite, exact131072B, with positive energy in every scored
reference/candidate channel/window. Prefix0..4095 is finite-only. A real-case
evaluator must guard the exact step reference SHA1336d901…977e73.

[The proposal](proposal.json) fixes the mathematical/rounding definition, trust
boundary, planned controls and limits. This NEW1% budget is explicit engineering
policy for one dynamic history. Ramp/B calibration does not transfer; neither
reference uncertainty nor an all-architecture correctness envelope is claimed.
The separate window/channel checks prevent a correct pre-step segment or good
other channel from hiding a missed intervention. No actual error was computed here.

The independently reviewed capture supplies a genuine productive baseline and
left contrast. The matched ignore-step control should reject post-L; its other
three comparisons should be exact matches from retained sample identity. It is
one negative contrast, not four independent failures. Right-only2% waveform
corruptions, exact boundary, invalid/zero/hash guards and concentrated/timing/tail
sensitivity controls are planned. Any observed limitations must remain visible.

Every poststep sample is scored, including the first eight equal frames. No
phase/gain/offset/time fitting, transition exclusion,4000-frame ramp,8-frame
latency or general right-invariance law is inferred. Aggregate errors can hide
local/tail defects. This method would add only the exact finite dynamic I/O
expectation; stored position mapping A1, Live/arm64, other histories and oldmodal
omissions remain open. Existing R6/v4 and old cases stay unchanged.

[Providers](providers.json) pin exact retained capture/review/source/catalog
identities. Their hashes and the25capture payload hashes were verified as data;
no samples were decoded and no comparator, fit, FFT, model, collector or native
function ran. Independent method review and explicit selection precede any new
measurement implementation/execution, then owner/handoff adoption separately.
