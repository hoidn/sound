# v5 author candidate and execution preflight

Authoring/readiness only. No comparator, audio decoder, numerical/control
calculation, model/fit/FFT, original/native or candidate-device code has run at
this freeze. Root must separately select the exact sealed source after full
code inspection and independent preflight. This preparation does not grant
handoff approval or local publication.

The [candidate](../../device-corpus-v5/README.md) is pending independent handoff
and numerical integration. Its exact adopted R7 source is bound by
[source-binding.json](source-binding.json); reconstruction uses the immutable
R7 snapshot plus only the receipt's reviewed 456-byte metadata banner, not a
future live canonical gate. [providers.json](providers.json) pins the separate
owner/capture/method reviews and immutable inputs.

All 72 old evaluation objects and 81 F32 files are preserved. Only group027/
evaluation027-01 and one reference are added. [comparator-delta.json](comparator-delta.json)
and [comparator.patch](comparator.patch) retain the exact ten-line branch and
four-line guard additions: removing those two literal strings restores the full
old 8,830-byte comparator. Imports/dependencies, all old labels/errors/branches
and old Ramp/NoteOff reference guards remain unchanged. The new channel-major
labels explicitly map to the method's four independent axes.

Read [check_structure.py](check_structure.py) fully before this allowed check:

```sh
python3 -B analysis/ableton-live-12.4.3/handoff-staging/device-corpus-v5-analysis/preflight/check_structure.py --check
```

It uses only stdlib text/JSON/hash/AST checks, old-object/fixture preservation,
exact source/banner reconstruction, six unsafe structural fixtures, links,
sanitization, inventory and before/after identities. It never imports or executes
the comparator, decodes F32 or performs metrics. Unsupported arguments fail
before reading inputs. Its stdout can be retained before source freeze; frozen
reports are never rewritten by replay.

Read the full [validate_once.py](validate_once.py) and new public comparator
before any later authorization. The proposed one-shot command is:

```sh
python3 -B analysis/ableton-live-12.4.3/handoff-staging/device-corpus-v5-analysis/preflight/validate_once.py --approved-preflight-sha EXACT_MANIFEST_SHA256
```

The literal hash must equal this preparation's frozen manifest. The script
verifies provider/preparation/candidate identities, requires the exclusive
sibling `numeric-validation` output directory to be absent, disables/restores
bytecode writes and uses only the NEW public comparator. No old comparator,
model, collector or original code is imported or replayed. The source readiness
gate is not permission to run it.

If selected, one isolated export and one public CLI regression process will
measure all73 reference-self evaluations. The prospective count is4799:
4795old plus four new checks. Actual counts/errors, including tiny nonzero old
self-errors, are recorded rather than claimed now. Every old evaluation must
still pass, and the new self result must contain the four named zero-error
checks. The reference-self directory contains copies, not a candidate device.

The same new public functions would then consume the exact38 retained method
control files, with no audio synthesis or source estimator. All valid controls'
four results must match the retained errors/tolerances/pass flags exactly after
mapping report order. Invalid cases fail as whole public cases; the runner does
not invent partial-axis public reports. Synthetic arithmetic uses direct
measurement functions explicitly, while real and synthetic-as-real hash failures
exercise the public strict guard. All three separate hash guards also receive
wrong-reference controls. The isolated test temporarily redirects only the NEW
run function's `HERE` to a minimal test directory and restores it in `finally`;
the public CLI itself has no such option or trust bypass.

All38 full source records are retained in the results, including ignored-step,
four isolated 2% failures, positive-energy/invalid/boundary controls and passing
concentrated/prefix limitations. No new threshold, phase/gain fit, transition
exclusion or candidate grade follows. Old174modal omissions and two note72
mode16 omissions remain unchanged.

The selected run would retain attempt, public stdout/stderr/receipt, all control
results, summary/environment, before/after scoped identity maps and final
receipt/inventory. Temporary export/candidate copies are removed. Failures after
the exclusive output is created are retained without retry; failures during
the pre-output source/argument gate stop without that result directory. The
script's final identity comparison covers pinned source, old release payloads,
stage and preparation. It does not claim a whole-workspace or whole-session
watch. No install, native call, source change or publication is selected here.
