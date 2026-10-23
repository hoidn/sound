# Corpus note-off before impulse: preparation only

This packet prepares three fresh extracted x86 Corpus captures. No collector,
original function or diagnostic has executed. Independent preflight and Root's
explicit selection of the exact sealed command remain pending. The final
`depth-corpus-midi-gate-before-impulse/` directory must remain absent until that
selection. The author and reviewer must not invoke the collector.

A is a deliberately fresh `gate1-held` matched control. B is `gate1-off`; C is
`gate0-off`. Relative to the corrected R2 preparation, A's script is exact and
B/C change only the off event from host frame8193 to3073: status80, key60,
velocity64. All three have note-on1537/status90/key60/velocity100. A/B use
MidiGate index13=1; C uses0. All38 ordered values, MidiPitch1/LFOoff,44100Hz,
16384frames/block512, stereo unit impulse4096/input flag1, stopped0/0/120,
time0, MXCSR1f80, create/rate/process/destroy and import substitutions remain
exact. There is no reset, warmup, bend, sustain, extra event/process or retry.

The hypothesis is limited: an off after a one-sample impulse can fail to
discriminate hypothetical input gating because the later input is already zero.
An earlier off is a proposed discriminating protocol; it predicts neither silence
nor a change and does not recover a gate or note-off law. Existing original
captures remain immutable historical evidence. The retained arm64 setter trace
stops at its message-handler frontier; this preparation adds no source proof.

Driver coordinates are on1537→block1536/local1 and off3073→block3072/local1.
No extra decrement is applied. Actual Corpus admission/latency, Live frame base,
UI routing, x86/arm64 equivalence and downstream state remain unknown. Exact
retained driver spans are referenced through the pinned parent source-context
file; full loader/binding/shim semantic review is carried from the immutable
review records, not freshly repeated here.

Both output windows4096..8191 (`early_response`) and8192..16383 are **after the
B/C off command**. Prefix0..4095 remains descriptive. `productive_response`
compares early energy/peak to that prefix floor only; it is not note-off delivery,
release-tail evidence, an acceptance criterion or a continuation condition.
Silent, unchanged, exact-length finite output remains structurally valid and
proceeds. No optional diagnostic is included or run; no fit, FFT, threshold or
grade is selected.

The collector is a literal four-operation successor of the corrected R2 source;
`delta.json` retains every replacement and occurrence count. Apart from off-frame
and descriptive-label changes, launch/PID/valid-capture accounting, parameter
bit echoes, clean logs/status, exact131072-byte/full-finite format, timeout/core,
environment, exclusive outputs and structural stop guards reconstruct exactly.
One child requests73 direct exports; at most three attempts request219, excluding
loader/import/nested calls. Failed Popen records an attempt without a returned
usable PID; a PID alone never proves original export execution. Failures and
partial artifacts remain unknown beyond their exact evidence and are never
removed, reused or retried.

`check.py --check` reads data and parses the collector as AST. It compiles only
its inspected parameter/validity/accounting expressions against synthetic data;
it never imports the collector, executes its functions/main or launches a child.
Finite-zero, bad event/script/provider/format, actual log/parameter-predicate and
four launch-accounting controls are checked. The parent R1/R2 seals, approved R2
preflight, current gate-capture seal/review and source bytes are pinned; old
manifest payloads are verified without invoking old tools. Mutable wiki context
is copied only as-of by a future selected collector, never a future hash gate.

The proposed invocation is `python3 -B capture-once.py --capture-selected-once`
with this preparation's exact reviewed `manifest-preflight.json` SHA, using the
absolute path in `proposal.json`. That hash fixes bytes; Root's selection and
later actual capture review are separate. No normative ID, criterion, release,
application/candidate grade or completion credit is introduced here.
