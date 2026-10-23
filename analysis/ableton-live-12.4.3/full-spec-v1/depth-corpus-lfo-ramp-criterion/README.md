# Proposed finite Corpus Ramp audio criterion

**Proposed engineering choice: at most1% relative waveform RMS error in EACH channel.** Criterion review remains pending as of author preparation; the pinned nominal and sensitivity captures have separate bounded-observation approvals. This is not a current adopted requirement, a recovered original tolerance, an inaudibility claim or an architecture portability bound. No new original function or candidate is executed here.

The nominal finite x86 reference is the newly captured Ramp Up stereo output. The only musical change from the independently reviewed Sine initialization is host index18=3. All38host values, rate44100Hz,16384frames, impulse4096, blocks512, inputflag1, transport0/0/120 and MXCSR1f80 are explicit in the pinned provider. This is a host-input contract; stored mapping, A1 and Live delivery remain unknown.

## Choice and observable meaning

[Criterion](criterion.json) freezes the proposed method and named engineering budget before any candidate result. Decode exactly16384interleaved stereo little-endian binary32 frames. All samples must be finite. For BOTH channels independently, use every frame4096through16383inclusive and compute `sqrt(sum((trial-reference)^2)/sum(reference^2))`, with positive reference/candidate energy. The proposed limit is inclusive `<=0.01`. It permits at most0.0001error energy/reference energy per channel. No phase/gain/offset fitting, alignment, transient deletion or alternate windows occurs.

The1%budget is explicitly chosen for this one finite T1 acceptance set. It admits the nominal vector and the two recorded coherent math-import substitution vectors, whose maximum observed error is about0.0070808, with margin inside the chosen budget. It rejects the pinned Sine contrast (about1.41–1.44), and the measured finite controls below. No automatic `observed maximum × factor` rule, confidence interval, worst-case envelope, Apple-libm or arm64 guarantee is inferred. The source-existing perturbation knob advances selected-family results toward ±infinity, including exact results; it is not a test of IEEE inexactness or all mixed per-call errors.

Global Q001 remains open. ADR0004 and the existing reviewed finite-device precedent allow a new bounded engineering proposal; neither the published Sine0.2Hz window criterion, its0.1Hz source-model agreement nor another device's RMS limit is imported as this rule. Ordinary independent successor and release review are still required before adoption. Earlier requirements/174omissions remain in scope and unchanged.

## Scope limits and controls

The metric compares finite AUDIO, not reconstructed LFO samples. Its aggregate error budget can admit concentrated, onset or low-energy-tail defects; it does not set a per-sample or transition bound. Frames0..4095receive full-file finite validation but no error grade in this local metric. Startup and other obligations retain their separate owners. Full duration below one free period does not exclude a right-channel wrap with the180degree offset. No absence/full-cycle/Sync/Spin/random or Live/arm64/candidate result is inferred.

[Controls](controls.json) retains actual nominal/±1substitution/Sine distances plus explicit data transformations: half gain, polarity,2%gain, channel swap, one-frame delay and planar repacking. The latter three are demonstrated contrasts for THIS record, not universal detectors. A finite prefix-only change intentionally passes, exposing the local scope. The standalone comparator also checks algebraic gain/polarity consequences, each-channel failure, an exactly constructed1%boundary and adjacent binary32 values, malformed/nonfinite data and zero-energy failures. These finite checks are not general semantic completeness proof.

## Read-only evaluator

Inspect [compare_ramp.py](compare_ramp.py), then run its mathematical self-check:

```sh
python3 -B analysis/ableton-live-12.4.3/full-spec-v1/depth-corpus-lfo-ramp-criterion/compare_ramp.py --self-test
```

To evaluate the one proposed case, pass its pinned nominal reference and a trial file as the two positional arguments. Exit0means both channel metrics pass,1means metric failure,2means invalid inputs/unsupported invocation. The CLI requires the nominal reference SHA; the reusable pure byte-measure function is used only for mathematical controls. It writes nothing and never invokes native code or old tools. Binary64 subtraction/products, `math.fsum`, square root and the inclusive comparison define rounding; no hidden acceptance epsilon applies. Exact-boundary tests use a synthetic100→101sample pair, not a claimed known device output.

[Inputs](inputs.json) pin immutable capture/review/release providers. ADR0004is embedded as-of rather than checked against an evolving governance page later. Independent sensitivity review approves only bounded observations; no proposed criterion or case is silently made normative by captured bytes or successful controls. Only this new proposal/evaluator is authored; no old checker/model/fit/main, original/native call, new capture, implementation or owner/release edit occurs.

[Manifest](manifest.json) seals this proposal as authored; approval or adoption belongs to a separate review or successor.
