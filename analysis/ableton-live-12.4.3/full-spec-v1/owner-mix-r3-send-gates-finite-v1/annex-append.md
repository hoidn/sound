
## Finite supplied-input send observations (revision3)

This annex records one finite extracted-x86 class under REQ-MIX-GRAPH-005.
The16 requirement bodies and the34 existing acceptance rows above remain unchanged.
The preceding34-case count describes that existing acceptance table. This annex
adds25 ungraded observation IDs, MG-042–066, plus seven historical references;
the revised owner therefore names59 case/observation IDs without adding an accepted
criterion. The published28-case scope, all proposed precision/assumption/state/error
conditions and every general U remain unchanged.

**Evidence and limits.** The [fixed batch](../../analysis/ableton-live-12.4.3/full-spec-v1/batch-mix-send-gates-v1/manifest.json)
contains25 once-only new calls and seven exact inherited historical joins.
Its [sole independent actual review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/mix-send-gates-v1-review.json)
approves only those finite observations and inherited joins.
The [complete finite catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-mix-r3-send-gates-finite-v1/finite-catalog.json)
preserves every13-word input and distinguishes fresh receipts from inherited projections.
X in this annex labels the extracted source of a finite observation; it supplies
no new application compatibility grade or candidate acceptance criterion.

The two contexts G0 and G1 are recorded argument vectors, not identified current
track/group receivers. Group tracks remain excluded by Scope. G1 does not add a
public grouped-send contract. No input here varies MainOn, so these observations
cannot establish MainOn independence or the pan/volume/crossfade/floor consequences
for arbitrary values. Actual receiver, graph delivery, public controls, lifecycle,
ARM/Apple precision and calibration joins remain outside this finite class.

**Exact supplied input.** Each fresh child uses the unchanged MXB-01 call shape:
`call 0x101b40d30 buf:8 hex:<52 bytes below> buf:16 dump b2 16`.
There is one direct entry call, fresh owned buffers and no setter, constructor,
rate/audio process, MIDI/clock phase, patch or FP perturbation. The52-byte vector
is thirteen little-endian uint32 words, interpreted by the recorded call model.
The Boolean argument order in both tables is words0,1,2,8: recorded SendsOn,
sendActive, prePost and GroupOn. Each0 is `00000000`; each1 is `3f800000`.
The names identify supplied arguments and do not establish a public binding.

| Word | Recorded role | G0 raw uint32 | G1 raw uint32 |
| --- | --- | --- | --- |
| 0 | SendsOn | Boolean tuple | Boolean tuple |
| 1 | sendActive | Boolean tuple | Boolean tuple |
| 2 | prePost | Boolean tuple | Boolean tuple |
| 3 | send gain | `3f000000` | `3f000000` |
| 4 | M[0] | `3f666666` | `3f666666` |
| 5 | M[1] | `3dcccccd` | `3dcccccd` |
| 6 | M[2] | `3e4ccccd` | `3e4ccccd` |
| 7 | M[3] | `3f19999a` | `3f19999a` |
| 8 | GroupOn | Boolean tuple | Boolean tuple |
| 9 | G[0] | `3f800000` | `3f000000` |
| 10 | G[1] | `00000000` | `3d4ccccd` |
| 11 | G[2] | `00000000` | `3d8f5c29` |
| 12 | G[3] | `3f800000` | `3e800000` |

**Twenty-five new finite observations.** These are every new tuple in the
complete G0/G1 × {0,1}⁴ catalog, not a selected subset. Each fresh b2 output is
the exact16-byte sequence `00000000000000000000000000000000`: four raw
binary32 positive-zero words. This is the observed native result for that exact
input, not a portable required output. All pre-execution predictions remain NULL
in the immutable batch. Every portable expected value, candidate comparator and
candidate grade below remains NULL; the existing C-case10⁻⁶ precision is not
silently assigned to these observation rows. Neither volatile pointer values nor
unpromised/high return-register lanes become candidate criteria.

| Case ID | Requirement context | Recorded G | Boolean tuple (0,1,2,8) | Native b2 observation | Portable expected | Comparator / grade |
| --- | --- | --- | --- | --- | --- | --- |
| MG-042 | 005 | G0 | 0000 | Four `00000000` words; finite X observation only | NULL | NULL / NULL |
| MG-043 | 005 | G0 | 0001 | Four `00000000` words; finite X observation only | NULL | NULL / NULL |
| MG-044 | 005 | G0 | 0010 | Four `00000000` words; finite X observation only | NULL | NULL / NULL |
| MG-045 | 005 | G0 | 0011 | Four `00000000` words; finite X observation only | NULL | NULL / NULL |
| MG-046 | 005 | G0 | 0100 | Four `00000000` words; finite X observation only | NULL | NULL / NULL |
| MG-047 | 005 | G0 | 0101 | Four `00000000` words; finite X observation only | NULL | NULL / NULL |
| MG-048 | 005 | G0 | 0110 | Four `00000000` words; finite X observation only | NULL | NULL / NULL |
| MG-049 | 005 | G0 | 1000 | Four `00000000` words; finite X observation only | NULL | NULL / NULL |
| MG-050 | 005 | G0 | 1001 | Four `00000000` words; finite X observation only | NULL | NULL / NULL |
| MG-051 | 005 | G0 | 1010 | Four `00000000` words; finite X observation only | NULL | NULL / NULL |
| MG-052 | 005 | G0 | 1100 | Four `00000000` words; finite X observation only | NULL | NULL / NULL |
| MG-053 | 005 | G1 | 0000 | Four `00000000` words; finite X observation only | NULL | NULL / NULL |
| MG-054 | 005 | G1 | 0001 | Four `00000000` words; finite X observation only | NULL | NULL / NULL |
| MG-055 | 005 | G1 | 0010 | Four `00000000` words; finite X observation only | NULL | NULL / NULL |
| MG-056 | 005 | G1 | 0011 | Four `00000000` words; finite X observation only | NULL | NULL / NULL |
| MG-057 | 005 | G1 | 0100 | Four `00000000` words; finite X observation only | NULL | NULL / NULL |
| MG-058 | 005 | G1 | 0101 | Four `00000000` words; finite X observation only | NULL | NULL / NULL |
| MG-059 | 005 | G1 | 0110 | Four `00000000` words; finite X observation only | NULL | NULL / NULL |
| MG-060 | 005 | G1 | 0111 | Four `00000000` words; finite X observation only | NULL | NULL / NULL |
| MG-061 | 005 | G1 | 1000 | Four `00000000` words; finite X observation only | NULL | NULL / NULL |
| MG-062 | 005 | G1 | 1001 | Four `00000000` words; finite X observation only | NULL | NULL / NULL |
| MG-063 | 005 | G1 | 1010 | Four `00000000` words; finite X observation only | NULL | NULL / NULL |
| MG-064 | 005 | G1 | 1011 | Four `00000000` words; finite X observation only | NULL | NULL / NULL |
| MG-065 | 005 | G1 | 1100 | Four `00000000` words; finite X observation only | NULL | NULL / NULL |
| MG-066 | 005 | G1 | 1110 | Four `00000000` words; finite X observation only | NULL | NULL / NULL |

**Seven historical references, with no new IDs or calls.** The following exact
tuples already had approved outputs. They were not replayed or given fresh receipts.
The three zero records and four enabled pre/post records complete the32-tuple
logical catalog. The enabled records are inherited productive calculation baselines,
not fresh controls, host audio or evidence that every new gated-off tuple is productive.

| Historical reference | Recorded G | Boolean tuple (0,1,2,8) | Native b2 bytes, little endian |
| --- | --- | --- | --- |
| retained-006 | G0 | 0111 | `00000000000000000000000000000000` |
| retained-008 | G0 | 1011 | `00000000000000000000000000000000` |
| retained-002 | G0 | 1101 | `0000003f00000000000000000000003f` |
| retained-010 | G0 | 1110 | `00000000000000000000000000000000` |
| retained-001 | G0 | 1111 | `6666e63ecdcc4c3dcdcccc3d9a99993e` |
| retained-004 | G1 | 1101 | `0000003f00000000000000000000003f` |
| retained-003 | G1 | 1111 | `e7fb693e295c0f3d7368913d0bd7a33d` |

These historical references name copied approved input/output projections, not
old case regradings. In particular, G1 records and the GroupOn-off record are not
silently substituted for the ungrouped MG-001/MG-002/MG-004 acceptance setups.
The complete catalog has28 observed zero tuples, three inherited and25 fresh,
and four inherited nonzero enabled pre/post tuples. It supports no universal
group-gating equation, statistical/calibration model, new public failure law or
expanded release. Unsupported required behavior remains U; coverage remains open.
