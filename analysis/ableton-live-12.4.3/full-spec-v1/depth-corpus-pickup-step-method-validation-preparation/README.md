# Pickup-step method: validation preparation

**Authoring only. The evaluator, its functions and controls have NOT run.**

[validate-once.py](validate-once.py) implements the independently reviewed method
proposal plus its preserved addendum: preL/preR over[4096,8192), postL/postR
over[8192,16384). Each relative waveform RMS uses exact binary32 widening,
binary64 subtraction/products/division/sqrt and math.fsum; all four errors must
be finite and <=0.01, with no epsilon, alignment or fitting. Full131072-byte
files must be finite; every scored reference/candidate region has positive
energy. Prefix[0,4096) remains finite-only.

Every real-reference comparison calls a mandatory literal SHA gate for the
actual step1336d901…977e73. A separately named pure arithmetic entry serves
explicit synthetic fixtures and is never a runtime trust bypass. The runner has
no generic metric, window, budget or reference override. It imports only stdlib;
no old comparator, private model, FFT/fit, collector or native function is used.

The fixed control suite retains all four axis records per comparison, including
structured invalid results. It includes self and the actual ignored-step
control; four separate positive1.02binary32 corruptions, each failing only its
own axis; zero/size/nonfinite/reference-hash failures; sparse synthetic boundary
fixtures at/below/above1%; scalar inclusive/outside tests; and fixed concentrated,
1/512-sample splice, last512zeroing and finite-prefix sensitivity controls.
Synthetic references and all generated control bytes/results are retained.
Neither the number of future controls nor their results is claimed as a pass
before execution. Wrong control rejects via postL; the other three axes match.
Timing/splice/tail controls report outcomes without forcing a pass/fail result.
No4000-frame movement,8-frame latency, right-invariance, A1 or general law follows.

[inputs.json](inputs.json) pins the original proposal trio, addendum, independent
design review, actual capture/review, publishedv4, immutableR6 and earlier
arithmetic source. The latter is inspected DATA only, never imported. The future
runner verifies all preparation/source/capture/v4 hashes and takes a durable
scoped before/after map. It creates one exclusive sibling output directory,
retaining copied preparation, attempt metadata, every generated candidate and
four-axis result, all requirements, and final watch maps. Unexpected exceptions
retain failure details and partial files; no deletion or automatic retry exists.
A failed required check yields failure rather than threshold/window adjustment.

Root must fully inspect the complete source before separately selecting this
single DATA-ONLY calculation. The exact invocation template is:

```sh
python3 -B /home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1/depth-corpus-pickup-step-method-validation-preparation/validate-once.py --validate-selected-once FROZEN_MANIFEST_SHA256
```

The SHA argument is the exact manifest-preparation.json digest provided with the
freeze notification. No self-test/replay/measurement mode is available. The
future output is depth-corpus-pickup-step-method-validation/; it is absent at
this preparation freeze. Wrong argv/hash or changed providers stops before any
measurement. Existing output refuses reuse. Passing controls would qualify only
this finite method; owner/case/comparator/handoff adoption remain separate.

Author checks performed only Python AST syntax/static invariants, JSON/source
identity, literal source guards and link/whitespace inspection. No evaluator
module import/function/main, synthetic audio generation, metric calculation,
old tool, original/native call or candidateDSP execution occurred. Current
capture/owner/release/proposal bytes are preserved. Independent source review
and Root execution selection are pending.
