---
id: PLAN-DEVICE-CORPUS-HANDOFF
type: research
status: current
updated: 2026-10-22
access: analysis
target: Ableton Live 12 Suite 12.4.3 / macOS arm64; retained x86_64 extracted renders
---

# Corpus audio pilot handoff

This page records the author staging and separate review of device-corpus-v1
from historical [SPEC-DEVICE-CORPUS](device-corpus.md) revision3. Revision4
adds the separately reviewed finite host-input Ramp case; revision5
adds two exact held-note histories. Their successor staging is recorded below
and does not change immutable earlier packages. The current disposition is
[released locally](#local-publication) after independent review; the author staging checks below retain their original scope. The payload contains original-code render
outputs, generated input signals, named comparison-domain vectors and an exact
measurement procedure. It contains no recovered application code. Stored-value
mapping, file loading and Live chain integration are excluded; A1 is not accepted.
The fixed render protocol is a project comparison input, not a claim about every
Live call sequence. The arm64 slice and whole application are not executed.

Current finite release: [device-corpus-v5](../../handoff/device-corpus-v5/README.md);
[release5 publication](#release5-local-publication) records the current disposition.
Sections through the first Local publication record the immutable v1 history;
[release2 publication](#release2-local-publication) records its finite successor.

## Staging plan

1. Verify retained manifests, render/input hashes and exact vectors. Correct draft
   precision errors against retained bytes. Record the source inventory privately.
2. Build self-contained cases and numerical metrics; retain only resolved modal
   measurements. Keep omitted estimates and every scope limitation explicit.
3. Copy generated signals/reference outputs without modifications; write a small
   measurement-only comparator and sanitized contract. No DSP synthesis code.
4. Verify hashes, links, source exclusion, self-comparison, corruption rejection,
   every-case silence/gain mutations, and an isolated export. Record outcomes here.
5. Leave review and publication pending a separate reviewer. No shared index,
   question, coverage or log edits in this worker.

## Finite scope and narrowing

The candidate has 24 groups, CORPUS-AUDIO-001 to 024, corresponding to draft
DCO-001 to 024; 68 evaluations; 61 distinct reference renders and nine generated
signals. Seven evaluations reuse a base reference for the supported block/rate/reset
variants. All retained outputs are 16,384 stereo binary32 frames. The public
parameter vectors contain all 38 named **comparison-domain** values, exactly
rounded to binary32, not recovered table indices. No assumption about project
loading or stored position values is accepted (A1 stays open).

Only finite reference-output portions of REQ-001 and REQ-004 to 012 are proposed.
REQ-002, 003 and 013 remain unreleased. No general resonator/controller formulas,
Live chain integration or arbitrary parameter automation is carried. Modal cases
grade 1,427 mode/channel/evaluation occurrences and omit 174 occurrences that
were unresolved or whose retained reference estimate falls outside the 1e-4
eligibility band. The exact omission records are in traceability.json. The
waveform check still grades each modal case's first 256 post-impulse frames.
A missing required mode fails; omitted modes and complete long-term spectral
identity are not passes. The pitch-only LFO metric does not constrain its gain.

The draft metric was proposed, never accepted. The payload fixes every numeric
window, filter, frequency bound (including its factor four), decay/amplitude
normalization, FFT band edge and failure outcome. It makes these **project
criteria pending review**, not a measured arm64 tolerance bound. Startup keeps
an explicit 1e-18 floor criterion and exact onset at frame 100. Whole Live and
arm64 execution remain not-run. The fixed transport/input protocol is a test
convention, not an assertion that Live always uses it.

## Draft corrections found during staging

Revision 2 corrects two precision issues against retained bytes:

- REQ-002's 1000 Hz FilterMidFreq input is binary32 0.5089499354362488. The
  prior printed 0.50894606 did not match the captured default vector.
- Startup frames 0–99 contain the approximately 1e-22 numerical floor, not
  bitwise silence. At frame 100 a 0.5 input produces approximately 0.00487155.

The public payload does not import the unfinished general parent equations.
Its protocol distinguishes the complete initial rate-history sequence from
warm-up/reset actions after the parameter vector.

## Evidence and exact identity

Retained source run:
[t12-device-dsp-v1 manifest](../../analysis/ableton-live-12.4.3/r2/t12-device-dsp-v1/manifest.json).
All 287 files listed there were re-hashed before copying. The source manifest
SHA-256 is `1bb3c9c677eca0544c955ff81b32f0dd992c3de04c585eabbe58f0bb253ff4ae`.

The analyst companion contains:

- [source-inventory.json](../../analysis/ableton-live-12.4.3/handoff-staging/device-corpus-v1-analysis/source-inventory.json): 199 source paths, exact hashes and sizes,
  including every used input, original output, script/log, the capture summaries,
  parent draft, N5 numerical table and independently authored measurement sources;
- [traceability.json](../../analysis/ableton-live-12.4.3/handoff-staging/device-corpus-v1-analysis/traceability.json): per-evaluation draft ID, source render/script/input,
  variant record, exact reference hash and ungraded mode records;
- `build.py`: copies the verified captures and emits the cases/traceability inventory;
  Markdown is hand-authored, and the manifest seals its exact current bytes;
- `compare_payload.py`: independently authored numerical measurement only; no
  recovered DSP or device synthesis code;
- `validate.py`, `check_sources.py`, `check_export.py`: candidate-only integrity,
  comparison behavior, generated-input reproduction and isolated-export checks;
- `environment.json`: Python 3.13.9, NumPy 2.3.1, SciPy 1.16.0, Linux little endian.

## Mechanical checks and failed attempt

The first isolated export uncovered a JSON serialization error: a NumPy Boolean
in a measurement row was not accepted by Python's strict JSON encoder. It was
corrected to an ordinary Boolean/float without changing the numerical metric.
The final checks rerun after this correction, and no failed run is counted as a pass.

`check_sources.py` independently reproduces all nine generated signals byte for
byte and checks all 68 vectors against the captured parameter scripts and all
68 output hashes. No original device or application was executed during staging.

Final validation, 2026-10-19:

- All 82 listed payload files match hashes/sizes; the inventory is exact, with no
  symlink, bytecode cache or unlisted file. All local payload Markdown links resolve;
  the deny scan finds no recovered identifiers, addresses or analyst paths.
- All 68 self-comparisons pass, covering 4,601 measurements. Per-channel silence
  and wrong-gain (wrong-frequency for the pitch-only LFO) mutations are rejected:
  272 checks. Seven missing/size/non-finite file checks are rejected.
- An isolated export at `/tmp/corpus-handoff-export-7chb9jgy/device-corpus-v1` runs the complete CLI
  with no analyst siblings: exit 0, all 68 evaluations pass. Export hashes/sizes
  and inventory match, with no generated payload bytes.
- Manifest SHA-256: `5de57ad6b345505422012480620a3a4856b8743da2dfdf3a5b52bb5c875ce2e5`.
  Payload size excluding manifest: 10,395,830 bytes. Candidate compatibility and
  whole-application execution remain not-run. The comparator is measurement-only.
- `git diff --check` passes. Evidence and payload hashes were checked; binaries
  were not rerun or reinstalled. The parent handles the shared index/coverage/log.

Reports: [author validation](../../analysis/ableton-live-12.4.3/handoff-staging/device-corpus-v1-analysis/author-validation.json),
[source validation](../../analysis/ableton-live-12.4.3/handoff-staging/device-corpus-v1-analysis/source-validation.json),
[export validation](../../analysis/ableton-live-12.4.3/handoff-staging/device-corpus-v1-analysis/export-validation.json).

## Original separate-review gate (author staging record)

At staging, a reviewer was required to check each source/fixture pin, named-domain convention, fixed
history protocol, mode eligibility, proposed tolerances and their limited
coverage, measurement independence, payload sanitization and isolated export.
The stage author did not review or publish the candidate. At that checkpoint
the payload was unreviewed and shared routing was untouched; subsequent review
and publication are recorded below. No clean implementation workspace exists.

## Review outcome — 2026-10-19

**Approved with listed clarifications** by a separate Codex handoff-review
context that did not author this candidate and will not implement it. The
[review record](../../analysis/ableton-live-12.4.3/handoff-staging/device-corpus-v1/REVIEW.md)
approves the finite partial clauses of REQ-DEVICE-CORPUS-001 and 004 to 012:
24 groups, 68 evaluations and unchanged fixtures, vectors, histories and numerical
thresholds. Requirements 002, 003 and 013 stay unreleased. A1, Live integration
and arm64 compatibility remain unaccepted.

The finite metric is accepted as an executable project criterion. This does not
approve the parent draft's general equations, arbitrary inputs, complete modal
coverage, LFO gain, or an arm64 error bound. All 174 omitted occurrences remain
ungraded. The seven variant expectations use retained equivalence measurements
against the base outputs; they are not newly executed reference renders.

RCO-01 clarifies case 023: `defaults_48_via_44` sets both rates **before** all
parameters. The distinct `defaults_48_rate_after_params` scenario stays excluded
and is not silently substituted. RCO-02 distinguishes startup gain from output
for a 0.5 input and accepts the 1e-18 floor criterion as a project convention.
These corrections are carried into [parent revision 3](device-corpus.md).
The release pins revision 3 with the listed clarifications. The exact
[staging draft snapshot](../../analysis/ableton-live-12.4.3/handoff-staging/device-corpus-v1-analysis/parent-draft-at-staging.md)
retains the author input's original bytes; its source-inventory entry adds a
retained-copy locator without changing the source digest.

Independent retained checks:

- [reviewer_check.py](../../analysis/ableton-live-12.4.3/handoff-staging/device-corpus-v1-analysis/reviewer_check.py)
  and [reviewer-validation.json](../../analysis/ableton-live-12.4.3/handoff-staging/device-corpus-v1-analysis/reviewer-validation.json):
  all 68 vectors, orders, rates, source signals, output bytes and history actions
  agree with retained evidence; all 287 source-manifest files and both Corpus
  bundle/image identities match. The 199 source inventory entries, including
  the retained staging draft, were also checked.
- All 1,427 mode occurrences were independently refitted with a different
  linear-fit parameterization. Largest difference from the retained frequency
  estimates: 5.9e-11 Hz; log radius: 5.9e-15. Eligibility, cutoffs and all 174
  omitted occurrences agree exactly with the finite case list.
- Synthetic probes check both sides of waveform, sine gain/phase, band-power,
  LFO frequency, modal frequency/log-radius limits and startup timing. A
  separate modal fit checks the tool's complex amplitude.
- The author's existing validation suite was rerun: 4,601 self-measurements
  pass, 272 per-channel wrong-output mutations and seven malformed-file
  checks are rejected. Every input signal reproduces byte-for-byte from its
  generation rule.
- The independent export executes the complete payload CLI without analyst
  siblings: exit 0 and all 68 evaluations pass. All payload hashes, sizes,
  links, inventory and independent/author sanitization checks pass.

No new original-code or application execution took place. The only executable
payload is the newly authored numerical comparator; there is no DSP synthesis.
The reviewed package is still in staging. The coordinator must publish its exact
bytes, update shared catalog/index/coverage/session/log state, and run the full
release lint. A restricted implementation workspace remains unprovisioned.

Final manifest SHA-256: `9fa257fa0e76d666d17da3fc363bf0cfd2facd0db3542db05d22a4260b771af2`. The package contains 83 payload files
and the manifest (84 total).
[Final metadata seal](../../analysis/ableton-live-12.4.3/handoff-staging/device-corpus-v1-analysis/reviewer-final-seal.json)
records the last revision-pointer and status-wording edits. Measurement code,
cases, vectors, signals and reference outputs are byte-identical to the package
that passed the complete numerical and mutation checks; all final inventory
hashes/sizes, links and sanitization were verified again. No published payload
was edited.

## Local publication

Released locally on 2026-10-19 as [device-corpus-v1](../../handoff/device-corpus-v1/README.md),
a byte-identical reviewed package. Final manifest:
`9fa257fa0e76d666d17da3fc363bf0cfd2facd0db3542db05d22a4260b771af2`.
The coordinator reran the final exported comparison procedure: 68 evaluations
and all 4,601 measurements passed against the included reference outputs.
This is self-comparison, not candidate or Live compatibility.


## Release2 staging — finite Ramp addition

[Canonical R4 owner review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-owner-r4-review.json)
approves one new host-input case DCO-029 after separate [finite criterion review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-lfo-ramp-criterion-review.json).
The proposed [v2 staging payload](../../analysis/ableton-live-12.4.3/handoff-staging/device-corpus-v2/README.md)
appends CORPUS-AUDIO-020-02 within existing group020, preserving all68old
evaluation objects,77physical fixtures and old measurement branches. It has
24groups/69evaluations,69physical reference files/62distinct byte streams and
nine generated signals. Its dedicated per-channel math.fsum waveform metric
requires positive reference/candidate energy, full-file finite samples and an
exact nominal reference SHA. No other criterion transfers to the new case.

[Author numerical validation](../../analysis/ableton-live-12.4.3/handoff-staging/device-corpus-v2-analysis/author-validation.json)
passes18checks plus19pure-comparator tests and69isolated self-comparisons/4603
measurements. No original or candidate DSP executed. The first packaging
link check tested manifest.json before creating it; that [failed author attempt](../../analysis/ableton-live-12.4.3/handoff-staging/device-corpus-v2-analysis/author-final-draft-check-attempt-01.json)
is preserved. Ordering was corrected; [final draft checks](../../analysis/ableton-live-12.4.3/handoff-staging/device-corpus-v2-analysis/author-final-draft-check.json)
pass all links, hashes, source exclusions,38parameter bits/order and signal
identity. The [in-review manifest snapshot](../../analysis/ableton-live-12.4.3/handoff-staging/device-corpus-v2-analysis/manifest-at-review.json)
is immutable historical evidence; staged final metadata will follow reviewer
disposition. Separate handoff review/publication remain pending at this checkpoint.
A1,174modal omissions and full-device/Live/arm64 compatibility remain open.


## Release2 local publication

[Corpus v2](../../handoff/device-corpus-v2/README.md) is released locally after
[separate handoff review](../../handoff/device-corpus-v2/REVIEW.md) and a focused
[final inventory seal](../../analysis/ableton-live-12.4.3/handoff-staging/device-corpus-v2-analysis/reviewer-final-seal.json).
The staged final metadata changed only three README phrases, cases/status and
manifest review/status/inventory; all numerical code,69evaluation objects and
reference/input bytes stayed exact. The preceding in-review record is historical.
The reviewer corrected two report-only assertions (a historical pending-word
match and the added review links); no stage change or numerical rerun resulted.

Final manifest17,447B SHA-256
`7207cba976e25616e93efdb0e6685533570ed71b805d1920711c44c890047fab`,
84payloads/85tree; all12local links and hashes pass. The [publication receipt](../../analysis/ableton-live-12.4.3/handoff-staging/device-corpus-v2-analysis/local-publication.json)
records exact copy equality. v2 supersedes v1 only by this finite extension; v1
remains immutable. Nothing was pushed or published externally, and no candidate
or original application ran. Whole-profile and whole-product gates remain open.


## Release3 staging — two finite held-note histories

[Finite modal method review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-midi-modal-method-review.json)
approved note60scored-region reuse and note72first15points/channel as explicit
finite engineering applicability. Separate [owner R5 review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-owner-r5-review.json)
approved DCO030/031 only, and [exact canonical adoption](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-owner-r5-adoption.json)
preserves13IDs/all29earlier rows:31cases,27finite/fourU. Both new mode16
observations stay ungraded, separately from174historical omissions. General
MIDI timing/routing, native-pole eligibility and uncertainty remain unknown.

The proposed [v3payload](../../analysis/ableton-live-12.4.3/handoff-staging/device-corpus-v3/README.md)
adds group025 with two complete38-value vectors/events and two exact raw
references:25groups/71evaluations,87tree files. All69earlier evaluation objects,
78physical input/reference files and7795Bcomparator remain exact. New public
selfchecks pass98+92measurements; wrongnote60fails64/92note72checks. Earlier
4603measurements are carried from v2 approval, not freshly rerun. Independent
handoff review and final publication remain separate pending gates; current
release is still v2. No original/candidate execution or compatibility grade.


## Release3 local publication

[Corpus v3](../../handoff/device-corpus-v3/README.md) was published locally on
2026-10-20 after [independent finite-content review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-v3-handoff-review.json)
and [focused final-seal approval](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-v3-handoff-final-seal-review.json).
The six-path final delta changes only review/status/provenance wording and
inventory. The original 87-file review candidate remains archived; all 71
evaluation objects, 80 input/reference files and comparator bytes stay exact.

Final manifest: 18,590 bytes, SHA-256
`7b8b13d1b29345a8b29d9709fb8b1a45b35fed88f37a3b50976b469d63649900`. The [publication receipt](../../analysis/ableton-live-12.4.3/handoff-staging/device-corpus-v3-analysis/local-publication.json)
records exact copy equality, 86 payload files/87 total, and unchanged older
releases. v3 supersedes v2 by these two finite comparisons only. New 190 self
measurements and 64/92 wrong-note failures are retained; 4,603 earlier
measurements carry v2 approval rather than a fresh combined batch. No original
or candidate ran during publication, and no whole-profile result follows.


## Release4 preparation — one finite On/Off history

[Owner R6 review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-owner-r6-review.json)
and [exact adoption](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-owner-r6-adoption.json)
approve only DCO032: canonical13IDs/32cases,28finite/fourU, all31oldrows and
clauses001–012 literal. Capture/method approval are separate. The proposed v4
adds only group026/026-01 with its exact38-value B history and separate hash-
guarded1%post4096 waveform metric. Prefix finite-only and late-tail-zero blind
spot stay explicit; no general gate/decay/flag/silence law. All25oldgroups/
71evaluation objects and80physicalF32 remain exact. Comparator preparation
actually passes4793old+2newself measurements; these are tool checks, not device
compatibility. Private staging still awaits independent handoff review; current
released v3 and catalog totals remain unchanged. No original or candidate ran
during owner adoption/staging.


## Release4 local publication

[Corpus v4](../../handoff/device-corpus-v4/README.md) is released locally after
[independent content review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-v4-handoff-review.json),
[complete isolated CLI integration](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-v4-handoff-review-cli-addendum.json)
and [focused final seal](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-v4-handoff-final-seal-review.json).
Final manifest20279B/SHA5375571b14812cfc901e0970ab0c627b2e6a6a1a51e0ab3e4c6c29f9a959a1ad,
87payloads/88files;26groups/72evaluations. All71oldobjects/81F32/comparator and
normative content stayed exact across five status/review metadata changes.
The [publication receipt](../../analysis/ableton-live-12.4.3/handoff-staging/device-corpus-v4-analysis/local-publication.json)
records exactcopy/oldermanifest preservation. First audit-only beforeprojection
shallowcopy error is retained and corrected by R2; no stage/numerical defect.
Actual fullpublicCLI4795self measurements pass; no original/candidateDSP or
whole-profile result. v4 supersedes v3 only by this one finite extension.


## Release5 author staging selected — 2026-10-20

Canonical [R7](device-corpus.md) has separate [owner approval/adoption](../research/corpus-dsp-static.md#corpus-r7-owner-adoption--2026-10-20).
The [private delta design](../../analysis/ableton-live-12.4.3/full-spec-v1/corpus-v5-proposal/README.md)
adds only DCO033/one exact same-instance pickup history to partial001/012.
Prospective v5 counts are27groups/73evaluations/82physicalF32, preserving all
26oldgroups/72objects/81F32 and old comparison branches/guards. A fixed four-axis
branch and separate literal step-reference hash guard are the only proposed
measurement-code additions. The one additive parameter_updates field records
8192processedframes/index15=.75/8192remaining on the same instance/input.

Author staging/code/preflight is selected; no new numerical/comparator execution
has been authorized at this checkpoint. Read-before-run inspection, bounded
regression/control execution, independent handoff/content/publicCLI/final-seal
review and local publication remain separate. Prospective4799measurements is
not a result. V4 remains current and every published package is immutable. No
new original capture, candidate grade or full-profile completion follows.


### First v5 candidate metadata finding — 2026-10-20

The initial stage/preflight froze without numerical execution. Independent
source review identified stale manifest pointers: supersedesv3, R6/B-only
readiness/change-list and an unqualified earlier approval/numerical pass. These
must be corrected and historicalv4 results explicitly qualified before any new
approval. The first candidate/preparation is preserved; correctedR2 will carry
identical comparison code/cases/F32 with accurate R7/027/pending metadata.
Root read the full9969Bcomparison and11686Bnumeric runner as data; no math defect
identified. The runner's pre-try write and CLI-timeout partial-output limits
must be explicit, with Root outer selection/exit receipts; no blanket complete
failure capture is claimed. Numerical selection remains pending corrected review.


The [frozen source preflight](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-v5-code-preflight-review.json)
requires CORPUS-V5-PREFLIGHT-001 at six exact manifest pointers; comparator/math
needs no change. All72oldobjects/81F32 and exact ten-line branch/four-line guard
inverse were checked;294scoped paths unchanged. LIMIT-001 is a nonblocking
failure-accounting limit with Root outer receipts and truthful scope. No actual
numerical result, export execution or release approval is granted. CorrectedR2
is being authored separately; frozenR1 remains unchanged.


## Actual release5 integration check — 2026-10-20

[CorrectedR2preflight](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-v5-r2-code-preflight-review.json)
passed. Root selected the sealed runner once11:29:46–11:30:12UTC; [actual record](../../analysis/ableton-live-12.4.3/handoff-staging/device-corpus-v5-r2-analysis/numeric-validation/manifest.json)
passes73reference-self evaluations/4799measurements,38controls and3strictguards.
All72old result objects equal retainedv4stdout exactly;311tinyselferrors retained.
Control output is24whole-valid/96publicmeasurements and14whole-invalid cases,
not152newpublicaxes. Inner294/Root2382paths unchanged, no neworiginal/candidateDSP.
Independent actual-result/content review and a separate finalmetadata seal remain
pending. All27groups/73evaluationobjects and82F32/comparator/normative criteria
must remain literal in finalization; qualify embedded pending provenance as
fixture-author history. Currentv4 remains the published clean implementation input.


The [actual-result and finite-content review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-v5-content-and-results-review.json)
is approved with no required findings. A separate final tree is now authorized
for the five metadata/status paths only. All27group/73evaluation objects,
including new027 pending provenance, must remain exact and be qualified as
author-freeze history. Focused final seal remains required; no numerical rerun
is needed for this exact metadata-only scope. No publication is claimed yet.


## Release5 local publication

Root locally published [device-corpus-v5](../../handoff/device-corpus-v5/README.md)
on2026-10-20 at11:52:02UTC after separate [finite-content/actual-results approval](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-v5-content-and-results-review.json)
and [exact final seal](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-v5-handoff-final-seal-review.json).
The89-file tree/88payloads is byte-exact the approved candidate, manifest21460B/
SHA60734632edbc8bae80f0a080e0af70cdc1217e61e8a5433f6ade67845f17f479.
[Publication receipt](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-v5-root-publication/receipt.json)
records2079oldhandoff files unchanged,34release manifests/2133payload hashes,
19current/15superseded. All earlier Corpus releases remain immutable.

Only027-01/DCO033 is added:27groups/73evaluations, all72oldobjects and81oldF32
exact,82F32total. Actual73reference-self evaluations/4799measurements passed;
38controls/threeguards matched. Finalization changed five status/metadata paths
only, all27group objects exact; embedded pending/proposed provenance retains
author-freeze history. No numerical rerun was needed for final metadata.
Five current device packages total261finite evaluations. No original/candidate
DSP ran during publication; no full-profile, arm64 or application grade follows.

## Unreleased R8 deterministic observation annex — 2026-10-21

[Canonical R8](device-corpus.md) now includes the [reviewed three-observation annex](../research/corpus-dsp-static.md#corpus-owner-r8-deterministic-annex-adoption--2026-10-21), with waveform expectations/comparators NULL and U acceptance criteria. All 33 old rows/criteria are preserved; 36 rows now comprise 29 existing criterion cases, three native-observation-only cases and four existing U. Current v5 remains 27 groups / 73 evaluations. No new release or candidate comparison is selected.

## Unreleased R9 finite host observation annex — 2026-10-21

The [canonical draft](device-corpus.md) applies the [sole-reviewed R9 annex](../research/corpus-dsp-static.md#corpus-owner-r9-native-integer-annex-adoption--2026-10-21). New observation navigation does not supply portable candidate criteria or close public/ARM/history unknowns. Existing immutable release, criteria and scope remain exact; no new release or candidate comparison selected.

## Unreleased R10 complete finite-host annex — 2026-10-21

[Canonical R10](device-corpus.md) applies the [sole-reviewed201-observation annex](../research/corpus-dsp-static.md#corpus-owner-r10-complete-finite-host-annex-adoption--2026-10-21), with277aliases/264vectors/63 inherited references. Fresh checker PASS and prior failed-checker/default/source qualifications stay separate; old criteria/U and immutable v5 scope remain exact. No new portable candidate criterion, general/public/ARM law, release or candidate comparison selected.

## Unreleased R11 finite observation annex — 2026-10-21

The [canonicaldraft](device-corpus.md) applies the [sole-reviewed R11 annex](../research/corpus-dsp-static.md#corpus-owner-r11-held-on-midi-annex-adoption--2026-10-21). Fixed native observations add no portable candidate criterion, general public/ARM/calibration law or release. All prior criteria/U/history and immutable release scopes remain exact; candidate comparison remains unselected.

## Unreleased R12 two-event observation annex — 2026-10-21

The [canonicalR12](device-corpus.md) applies the [sole-reviewed396historyannex](../research/corpus-dsp-static.md#corpus-owner-r12-two-event-midi-annex-adoption--2026-10-21), no portablecandidatecriterion/generalMIDI/publicARM/calibration law or release. All prior criteria/U/history and immutable v5scope remain exact; candidate comparison remains unselected.

## Unreleased R13 residual MIDI annex — 2026-10-21

The [canonical R13](device-corpus.md) applies the [sole-reviewed157history annex](../research/corpus-dsp-static.md#corpus-owner-r13-residual-midi-annex-adoption--2026-10-21). It adds no portable candidate criterion, general public/ARM/calibration law or release. All prior criteria/U/history and immutable v5 scope remain exact; no candidate comparison is selected.

## Unreleased R14 finite observation annex — 2026-10-21

The [canonical draft](device-corpus.md) applies the [sole-reviewed R14 annex](../research/corpus-dsp-static.md#corpus-owner-r14-matching-key-annex-adoption--2026-10-21). New fixed native observations carry NULL portable criteria/grades and no application proof. Earlier criteria, unknowns, objects, history and immutable release scope remain preserved. No new release or candidate comparison is selected.

## Unreleased R15 Decay observation annex — 2026-10-21

The [canonical draft](device-corpus.md) applies the [sole-reviewed R15 annex](../research/corpus-dsp-static.md#corpus-owner-r15-decay-annex-adoption--2026-10-21),127finite supplied-host observations/full128input representatives. REQ003’s formula supplies input context, not a new quantizer/within-cell law. All new portable criteria/grades remain NULL/applicationFalse; prior clauses/objects/criteria/U/history and immutable v5 remain exact. No new release or candidate comparison is selected.

## Unreleased R16 seven-resonator observation annex — 2026-10-21

The [canonical draft](device-corpus.md) applies the [sole-reviewed R16 annex](../research/corpus-dsp-static.md#corpus-owner-r16-seven-resonator-annex-adoption--2026-10-21),890finite observations/full896aliases891histories/one qualified INPUT reference6aliases. Only bounded007/009append/annex/revision change; ENTIRE003formula remains INPUTcontext, not a new native quantizer/within-cell law. Eleven other whole bodies/all prior rows/objects/criteria/U/history/releases exact; new portablecriteria/gradesNULL/appFalse. No new release or candidate comparison is selected.

## Unreleased R17 observation annex — 2026-10-21

The [canonical draft](device-corpus.md) applies the [sole-reviewed annex](../research/corpus-dsp-static.md#corpus-owner-r17-native-host-position-annex-adoption--2026-10-21), adding 189 draft navigation IDs with NULL new portable criteria and grades. All prior whole requirements, cases, objects, criteria, unknowns, history and immutable release scope remain exact. The linked adoption owns the input, custody and method limitations. No new release or candidate comparison is selected.

## Unreleased R18 boundary observation annex — 2026-10-21

[CurrentdraftR18](device-corpus.md) adds3586finite nativeobservations after sole new-owner review, preserving all oldclauses/criteria/history and immutablev5scope27groups73evaluations. NewportablecriteriaGradeNULL/appFalse; nativequantizer/within-cell/generalpublicARM law unknown. No newrelease selected.

## Unreleased R19 finite observation adoption — 2026-10-22

The [R19 draft](device-corpus.md) and [canonical adoption](../research/corpus-dsp-static.md#corpus-owner-r19-declared-protocol-annex-adoption--2026-10-22) add 13 finite observation IDs. Earlier whole requirements, objects, criteria, unknowns, history and immutable releases remain exact. New portable expectations/comparators/grades are NULL; no release, candidate conformance or whole-product closure follows.
