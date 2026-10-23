# Whole 32-family route ledger census — correction proposal

Status: PROPOSAL, pending one independent review. No shared authority, owner, case, grade, release or selection changed. Fresh work is retained-document custody, schema-specific extraction, joins, counts and sorting; prior family/source semantic audits remain inherited.

The selected 32 frozen family cuts contain **691 X / 1,076 S / 3,857 no-established-route**, totaling **5,624 heterogeneous inventory units**. This combines bounded predicates/contexts and whole-clause bundles. It is not an atomic denominator, fraction, behavior grade or whole-product completion claim. Required unsupported behavior stays U and coverage stays OPEN.

Selection is the canonical program-structure atlas's distinct current family links, with active Warp v2 and Analog v2's explicit correction overlay applied to frozen v1. The Analog cut's 241 units / 199 X / 30 S / 12 none remain predecessor-r1 contexts, not a newly derived current Analog R2 denominator. The current-owner-qualified 32-family denominator is not established by this census. Excluding that historical Analog cut yields 492 X / 1,046 S / 3,845 none across 5,383 units in the other31 cuts; that subtotal does not fill the current Analog gap. MIDI storage's 88-unit map likewise stays pinned to R4, not a new R5/R6 denominator.

## Exact required-unit counts

| Family cut | Required units | X | S | None | Required array | Unit |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| mix | 110 | 17 | 70 | 23 | `/outcomes` | bounded predicate/context |
| playback | 243 | 43 | 69 | 131 | `/outcomes` | bounded predicate/context |
| transport | 108 | 30 | 44 | 34 | `/outcomes` | bounded predicate/context |
| clip-launch | 229 | 21 | 98 | 110 | `/rows` | bounded predicate/context |
| midi-note | 88 | 12 | 52 | 24 | `/outcomes` | bounded predicate/context |
| structure-als | 196 | 1 | 129 | 66 | `/outcomes` | bounded predicate/context |
| warp | 80 | 5 | 50 | 25 | `/outcomes` | bounded predicate/context |
| mixer | 104 | 14 | 52 | 38 | `/outcomes` | bounded predicate/context |
| automation | 129 | 22 | 69 | 38 | `/rows` | bounded predicate/context |
| corpus | 146 | 49 | 83 | 14 | `/outcomes` | bounded predicate/context |
| electric | 181 | 149 | 11 | 21 | `/rows` | bounded predicate/context |
| tension | 93 | 71 | 12 | 10 | `/outcomes` | bounded predicate/context |
| analog | 241 | 199 | 30 | 12 | `/rows` | bounded predicate/context |
| collision | 84 | 38 | 10 | 36 | `/rows` | bounded predicate/context |
| midi-user | 94 | 19 | 31 | 44 | `/rows` | bounded predicate/context |
| bundled-parameters | 135 | 1 | 120 | 14 | `/rows` | bounded predicate/context |
| browser-index | 83 | 0 | 35 | 48 | `/rows` | bounded predicate/context |
| plugin-discovery | 84 | 0 | 53 | 31 | `/rows` | bounded predicate/context |
| utility | 48 | 0 | 2 | 46 | `/rows` | bounded predicate/context |
| arrangement | 345 | 0 | 6 | 339 | `/rows` | bounded predicate/context |
| native-midi-effects | 309 | 0 | 0 | 309 | `/rows` | bounded predicate/context |
| filter-eq | 65 | 0 | 4 | 61 | `/clauses` | whole-clause bundle |
| dynamics | 271 | 0 | 20 | 251 | `/predicates` | bounded predicate/context |
| recording-comping | 282 | 0 | 8 | 274 | `/rows` | bounded predicate/context |
| audio-video-export | 91 | 0 | 0 | 91 | `/predicates` | bounded predicate/context |
| sample-instruments | 350 | 0 | 0 | 350 | `/predicates` | bounded predicate/context |
| distortion | 67 | 0 | 9 | 58 | `/bundles` | whole-clause bundle |
| device-racks | 38 | 0 | 1 | 37 | `/bundles` | whole-clause bundle |
| delay-reverb | 562 | 0 | 0 | 562 | `/required_outcomes` | bounded predicate/context |
| modulation-pitch-loop | 106 | 0 | 0 | 106 | `/required_outcomes` | whole-clause bundle |
| synthesis-instruments | 585 | 0 | 0 | 585 | `/outcomes` | bounded predicate/context |
| legacy-native | 77 | 0 | 8 | 69 | `/required_outcomes` | whole-clause bundle |

Every family's manifest, exact ledger, route-field name and required-array pointer are in census.json. Every required unit's ID, requirement association, source-array pointer and exact raw/normalized route are in required-units.jsonl. Per-family required_rows_source pins resolve those pointers; Analog's optional overlay_pointer resolves against its v2 ledger while its row pointers resolve against v1. Each row also names qualifier-field pointers; this census does not discard those premises or convert a local route to public behavior.

## Required correction findings

1. **CENSUS-001 — literal totals disagree with the selected ledgers.** Plan revision4 second amendment, item4 (as-of lines562–577; see authority-snapshots.json) states “190 X, 732 S and 2,528” none across27 cuts. The selected32 total above differs by +501 X / +344 S / +1,329 none. Even the27 cuts obtained by removing the five cuts the prose calls column-less (Analog, Arrangement, Automation, bundled parameters, Electric) give **320 X / 840 S / 3,433 none**, not the stated numbers. The amendment does not supply a reproducible row-selection rule for its claimed totals; this census does not invent an exact origin for the mistake.
2. **CENSUS-002 — the claimed column-less cuts have explicit row route fields.** Analog's frozen base ledger `/rows` has199 `X-route` rows; v2 preserves routes by contract. Electric `/rows` has149 `X-route`; Automation `/rows` has22 `X-route`; bundled `/rows` has1 `X-route` (BP119, `/rows/118/route`); Arrangement `/rows` has6 `S-route` (AROUT-260…265, `/rows/259/route`…`/rows/264/route`). All five have route fields, not absent columns. Playback also has43 `X-route` in `/outcomes` and clip launch21 in `/rows`: their counts are machine-readable, not merely prose. All affected field pointers and every contributing row are retained.
3. **CENSUS-003 — the literal priority list omits higher X counts.** Item3 (as-of lines548–561) begins Corpus49 and playback43. A count sort instead starts Analog199 (historical-owner warning), Electric149, Tension71, Corpus49, playback43, Collision38, transport30, Automation22, clip-launch21, MIDI-user19, mix17, mixer14, MIDI-note12, Warp5, then bundled1 and structure/ALS1 tied. Tension's71 are in `/outcomes` (TNR-001 `/outcomes/0/route` through final X TNR-091 `/outcomes/90/route`). Equal counts use alphabetical family IDs only for stable presentation, not a semantic eligibility rule. All16 zero-X families follow, parked. No batch is automatically selected: current owner, legal input/state, route premises, calibrated/or accepted expectation and scope must still be checked. In particular the historical Analog count does not authorize a new current-R2 batch.

## Schema and exception controls

- Route spellings admitted only for required units: `X`/`X-route`; `S`/`S-route`/`S-retained-file-only`; `none`/`no-established-route`. Exactly647 required S rows use `S`,419 use `S-route`,10 use `S-retained-file-only`. Recording/Comping uses `route_class`; the others use `route` on a declared required row or its unique context witness. Unknown/missing spellings fail; no implicit none/default classification.
- Dynamics has271 required predicates, each joined to exactly one `required-observable-context`:20 file-only S and251 none. Its142 documentary annotations (`no-established-exact-target-route`) are not extra required outcomes;413 total context records must not be summed as413 required predicates.
- Export has91 required predicates, each with one required context;46 documentary annotations are excluded. Sample instruments has350 required predicates, each with one context with `source_annotation_not_extra_outcome:false`;221 documentary annotations with that flag true are excluded. Its five S fixture metadata records are auxiliary and not opened as sample bytes.
- Filter/EQ uses65 whole-clause bundles, not its140 case-navigation rows or46 additional U action contexts. Distortion67 and Racks38 use complete bundles; their duplicate route contexts and D12 annotations are not extra outcomes. Modulation106 and Legacy77 likewise remain whole-clause bundles.
- Delay/Reverb's7 file-S auxiliaries and Modulation's10 file-S auxiliaries are outside required counts; sample's5 fixture-S metadata records are outside too. These are not an exhaustive count of every auxiliary across32 cuts. All other declared auxiliary, exclusion, cross-reference and unresolved-enumeration records retain their exact JSON values/pointers in census.json and are not automatically added to required counts. None/unknown never means absence, contradiction, failure, pass or closure.
- Analog's ten context/history patches cannot edit ID, requirement, predicate or route; exact base/v2 pins and R2 route-delta are retained. Thirty-seven investigative X routes on owner-U contexts remain U by inherited map qualification. Tension's callable DamperVelocity route still has an unjoined exact receipt, as the canonical atlas qualifies; source/native/public joins are not promoted.

## Separate indirect-site inventory

The as-of canonical atlas lines66–83 records **25,071 exported-reference baseline +24 conditional class records =25,095 of268,015 sites**. These are inherited site units, not freshly recounted, route units, behavior grades or a fraction. This census adds zero sites or resolutions. Ordinary-call/receiver stability premises remain in force.

## Evidence and limits

source-pins.json records68 immutable retained-document inputs (32 manifests+32 ledgers, Analog base manifest/ledger, Analog current-owner route-delta and sample fixture metadata), plus three mutable authority identities as-of capture. authority-snapshots.json retains exact captured atlas/plan/design texts for reproducibility; these evidence snapshots are not competing canonical pages. Later mutable-document changes are reported non-gating; immutable inputs must remain exact. We verified each selected ledger against its own frozen manifest, Analog base against its manifest, and sample fixture metadata against its manifest. We did not verify or traverse every other payload of those predecessor maps.

No C body, raw metadata index, original binary/image, provider, fixture sample bytes, native instruction, decoder, source query, harness, original call, model or comparator was opened/executed. No predecessor helper was imported/run. No new source semantics, public route, grade, owner/case/release, automatic next selection or coverage closure follows. The one frozen census manifest is the review unit; there is no separate preparation/preflight/actual/receipt chain.
