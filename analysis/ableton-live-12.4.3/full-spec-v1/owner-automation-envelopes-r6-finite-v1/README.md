# Automation owner revision 6: finite expectations

Analyst-only draft fixtures for SPEC-AUTOMATION-ENVELOPES revision 6. This is
direct adoption of already independently approved actual observations under
design revision 12 and the plan's second amendment. No original, harness,
model, collector, source acquisition, compiler or candidate was run in this
adoption. No batch observation is re-reviewed here. One manifest pins the owner,
payloads and already approved source data; no new preflight or receipt chain.

`monotone-cases.jsonl` enumerates AEN-M-0001 through AEN-M-2138, tied to REQ-009.
Each line contains four exact binary64 input words (positive zero, c1, c2,
positive one), the required Boolean, and exact source aliases. Expected Boolean
means the selected low bit `RAX & 1`, including full RAX `0xffffff01` as true;
other return bits are not Boolean requirements. All 2,138 ordered sweep rows
are retained, with 663 true and 1,475 false expectations. The ten M calls of
the earlier whole-34 batch are exact-input aliases, not ten additional cases.

`adoption-map.json` lists the 1,874 agreements, five corrected expectations and
259 newly expected cases from the previously NULL local oracle (80 true and
179 false). It separately lists all 92 historical tolerance acceptances for
which exact cubic mathematics says false. The five corrections do not belong
to that group. The frozen pre-call expectations remain unchanged, including
all NULL values. New owner expectations come from actual X observations, not a
post-hoc oracle, model fit or invented division policy.

The closed sweep universe was 42×42 Cartesian anchors plus 64 complete 3×3
neighbor families: 2,340 contributions, deduplicated to 2,138 exact pairs. It
is finite, not all possible inputs. Exact words preserve signed zero, infinity
and the one selected positive quiet NaN payload. The host strtod checks and
temporary float conversion are not proof of child XMM inputs, per-process FP
mode or exception flags. Native arithmetic cause and operation order are unknown.

`arithmetic-cases.json` adds AEN-B-01 through 15 and AEN-S-01 through 09 under
REQ-010's local arithmetic scope. Bezier inputs are one explicit 64-byte buffer
of eight binary64 coordinates and s=i/16, i=1..15. Expected outputs are the
approved binary64 X/Y words; binary32 Y is a derived presentation. Segment
inputs are an independent zero-filled 40-byte state plus explicitly sized
binary32/binary64 scalar words in retained argument order; expected output is
the exact approved 40-byte state. Internal state representation is an
analysis-side local fixture, not a required independent product memory layout.
The two declared Bezier endpoints are auxiliary data, with no native call or X
credit. No volatile register, pointer identity or import declaration is graded.

`owner-before.json` pins the exact prior owner bytes and retains revision 5's
REQ-009 text. It is historical data, not a current universal decision algorithm.
The owner preserves all 33 prior document/evaluator rows (27 gradable, two
withdrawn, four U), plus historical dated qualifications and release references.
The 2,162 new case IDs grade only supplied standalone arithmetic. No new loaded
event, object construction, public normalization/open/save, provider, E(t),
timebase, ramped sample, audio or application behavior is established. All 50
factory/registry/converter rows remain withheld. Evidence is original x86 only;
ADR 0003's ARM inference caveat remains, and boundary Boolean equivalence is
unknown. A curve-value tolerance cannot prove Boolean equivalence.

The approved observation reviews are reused, not rerun. Whole-34 review:
`reviews/automation-eligible-leaves-actual-v1-review.json` (22,892 bytes,
SHA-256 8cd9f6b78ad486dc21ffbbd3d94b19e978b0a151a67032023aba301808e5e873).
Whole-2,138 review:
`reviews/automation-monotone-boundaries-actual-v1-review.json` (106,194 bytes,
SHA-256 523323a4880a3f4957fd7e8e6bc76123b34a2f6e17be855f70e66fce03a4b954).
The Root raw-output durability qualification also remains applicable: retained
and hashed raw files were closed but not explicitly fsynced; no power-loss
durability claim is added.

No release was rewritten. Released automation-envelopes-v2 REQ-009 only
requires keeping controls satisfying K, with both controls in [0,1], ordered
or D≤−10⁻⁶. Every corrected pair has a control outside [0,1]; none contradicts
that bounded contract or its finite cases. Only the draft universal M
extrapolation is superseded. A later release requires its ordinary review and
neutral behavioral fixtures. Owner review need only assess added wording and
fixture mapping beyond the already approved observations.
