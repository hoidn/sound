
## Finite sensitivity evidence qualification — proposed revision 4

The [222-child batch](../../analysis/ableton-live-12.4.3/full-spec-v1/batch-tension-uncalibrated-sensitivity-v1/manifest.json)
passed its [sole actual/source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/tension-uncalibrated-sensitivity-v1-review.json)
for bounded finite observations. It retains a fresh unperturbed control and the
five stated perturbations for each of 37 settings without a prior per-setting
sensitivity study. All captures use 44,100 Hz, 44,100 frames and 512-frame host blocks.
Every input is the exact prior 129-word script, with only the historical MXCSR
command insertion in rounding variants. All 37 fresh controls match the prior
raw-output hashes; both channels of all 222 captures are finite and identical.
The complete 444 channel comparisons retain the prior per-setting held windows,
partial centers, floors and normalization. These are finite x86 extracted
observations under the recorded substituted libraries, not ARM or Apple bounds,
physical calibration, actual Live A1/A2 behavior or a general signal law.

The [37-row mapping](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-tension-r4-sensitivity-v1/adoption-map.json)
joins each existing case and primary requirement to all inputs and complete
metric records. The table below compares the maximum deviation from the fresh
same-setting control over all five perturbations and both channels with the
existing proposed quarter-tolerance margins: held 7.5 × 10⁻⁴, release
2.5 × 10⁻³, frequency 5 × 10⁻⁷, log radius 1.5 × 10⁻⁴ and complex amplitude
1.25 × 10⁻⁴. This arithmetic introduces no tolerance or acceptance criterion.
A recorded numerical margin is not an accepted stable class or release
eligibility. A margin not met leaves eligibility unresolved; it does not
classify a setting as physically chaotic or admit a statistical substitute.

| Setting | Existing case | Primary REQ | Held rel RMS | Release rel RMS | Frequency rel | Log radius rel | Complex amplitude rel | Proposed numerical margin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `body_mix_1` | DTN-023 | 011 | 3.16792297039e-05 | 0.0001886992214 | 9.54400225517e-10 | 2.53576877691e-05 | 1.64068318376e-06 | meets proposed numerical margin for captured class |
| `body_size_0` | DTN-023 | 011 | 1.72042995077e-05 | 0.000228142705639 | 5.51389156556e-09 | 2.5704146881e-05 | 2.02267110993e-06 | meets proposed numerical margin for captured class |
| `body_size_4` | DTN-023 | 011 | 7.24388038135e-06 | 0.000225213772094 | 1.8249159961e-09 | 2.53676958839e-05 | 1.34735185402e-06 | meets proposed numerical margin for captured class |
| `body_type_0` | DTN-022 | 011 | 8.93329856094e-06 | 0.000226543316603 | 9.06080210861e-10 | 2.53752367343e-05 | 1.42505549537e-06 | meets proposed numerical margin for captured class |
| `body_type_3` | DTN-022 | 011 | 8.23195038731e-06 | 0.000219864889304 | 1.7211694292e-09 | 2.5412033491e-05 | 1.39427389939e-06 | meets proposed numerical margin for captured class |
| `damper_pos_0` | DTN-017 | 008 | 1.46964671213e-06 | 0.000231178145997 | 6.40431607746e-09 | 2.34694075418e-06 | 1.123242032e-06 | meets proposed numerical margin for captured class |
| `filt_base` | DTN-024 | 012 | 0.000571366834323 | 0.00115036719389 | 3.4996817766e-07 | 3.91661282597e-05 | 2.06117816507e-05 | meets proposed numerical margin for captured class |
| `filt_t0` | DTN-024 | 012 | 8.29853774531e-05 | 0.000323280009547 | 3.55767362348e-07 | 9.99452832855e-05 | 1.41398163451e-05 | meets proposed numerical margin for captured class |
| `filt_t1` | DTN-024 | 012 | 8.91113437483e-05 | 0.000328003471282 | 3.54537418201e-07 | 9.28639427088e-05 | 1.62922619783e-05 | meets proposed numerical margin for captured class |
| `filt_t1_c0.25` | DTN-025 | 012 | 7.14892811914e-05 | 0.000299549658195 | 3.62518961627e-07 | 0.000321521467201 | 3.6858145941e-05 | margin not met; eligibility unresolved |
| `filt_t1_c0.75` | DTN-025 | 012 | 0.00018065505458 | 0.00045965320057 | 3.50087274392e-07 | 4.05387024629e-05 | 1.86970367181e-05 | meets proposed numerical margin for captured class |
| `filt_t1_q0.5` | DTN-025 | 012 | 0.000289802262399 | 0.000651986105032 | 3.50148550377e-07 | 4.13510972502e-05 | 5.50159633815e-05 | meets proposed numerical margin for captured class |
| `filt_t2` | DTN-024 | 012 | 0.000539021289181 | 0.00110850106493 | 3.5060551673e-07 | 4.62470269791e-05 | 2.41516656765e-05 | meets proposed numerical margin for captured class |
| `filt_t3` | DTN-024 | 012 | 0.000525680330308 | 0.00109135845221 | 3.50517228798e-07 | 4.70154317416e-05 | 2.83467316006e-05 | meets proposed numerical margin for captured class |
| `filt_t4` | DTN-024 | 012 | 0.000645930055719 | 0.00125222275856 | 3.57425346986e-07 | 0.000451569127593 | 1.41966159901e-05 | margin not met; eligibility unresolved |
| `filt_t5` | DTN-024 | 012 | 0.000713985397331 | 0.00135134589842 | 3.69968419234e-07 | 0.000544374811749 | 2.69183029284e-05 | margin not met; eligibility unresolved |
| `filt_t6` | DTN-024 | 012 | 0.00356088511348 | 0.00708128675605 | 3.53510992257e-07 | 4.72811886004e-05 | 0.000100355587732 | margin not met; eligibility unresolved |
| `filt_t7` | DTN-024 | 012 | 0.00327490093718 | 0.00651507574043 | 5.05372568571e-07 | 0.000461960087759 | 0.000125137644663 | margin not met; eligibility unresolved |
| `filt_t9` | DTN-024 | 012 | 0.000250853946956 | 0.000503448685803 | 3.82944453148e-07 | 0.000807291275269 | 0.000135659396905 | margin not met; eligibility unresolved |
| `ham_damp1` | DTN-012 | 006 | 7.54040373117e-06 | 0.000223777850329 | 3.06932790295e-09 | 2.51378163241e-05 | 1.55148758203e-06 | meets proposed numerical margin for captured class |
| `ham_stiff1` | DTN-012 | 006 | 7.37418100412e-06 | 0.000224264890228 | 1.62382729485e-09 | 2.51905608197e-05 | 1.58952657288e-06 | meets proposed numerical margin for captured class |
| `note_48` | DTN-004 | 004/005 | 9.6287975316e-05 | 0.00019352035191 | 2.36902208073e-07 | 1.40070917725e-05 | 1.06283556597e-05 | meets proposed numerical margin for captured class |
| `note_72` | DTN-004 | 004/005 | 0.000219464454886 | 0.000742142485477 | 3.53220086735e-07 | 2.50315842816e-05 | 4.52993588718e-05 | meets proposed numerical margin for captured class |
| `pickup_pos_0` | DTN-020 | 010 | 6.23312350891e-06 | 0.000224787599721 | 6.95429824837e-10 | 2.52798462228e-05 | 1.40276483933e-06 | meets proposed numerical margin for captured class |
| `plk_damp0` | DTN-011 | 006 | 7.24241665542e-06 | 0.000227931294558 | 6.62182086941e-10 | 2.53411341757e-05 | 1.24844214787e-06 | meets proposed numerical margin for captured class |
| `plk_stiff0` | DTN-011 | 006 | 7.26002790368e-06 | 0.000226927345411 | 2.08763217824e-09 | 2.53855631056e-05 | 1.23752830692e-06 | meets proposed numerical margin for captured class |
| `plk_x0` | DTN-011 | 006 | 6.88324148584e-06 | 0.000222895551692 | 9.67229074611e-10 | 2.53053649322e-05 | 2.195148421e-06 | meets proposed numerical margin for captured class |
| `pos_0` | DTN-013 | 006 | 6.48275479571e-06 | 0.000227632570189 | 1.09623221611e-09 | 2.54065648557e-05 | 1.24407474796e-06 | meets proposed numerical margin for captured class |
| `str_damp_0` | DTN-014 | 005 | 7.39931908442e-07 | 0.000228002043784 | 2.81631651333e-09 | 2.43397921595e-07 | 8.19548003039e-07 | meets proposed numerical margin for captured class |
| `str_damp_1` | DTN-014 | 005 | 7.77993518902e-06 | 0.000230473077241 | 2.93968183129e-10 | 3.06521430029e-05 | 1.21928074388e-06 | meets proposed numerical margin for captured class |
| `str_decay_0.25` | DTN-014 | 005 | 1.09599433464e-06 | 1.69598405099e-05 | 1.7123433782e-09 | 1.04988106786e-06 | 1.7319368105e-06 | meets proposed numerical margin for captured class |
| `str_inharm_0` | DTN-016 | 005 | 6.73369847066e-06 | 0.000222429244787 | 3.6834342243e-09 | 2.52064044046e-05 | 1.618814244e-06 | meets proposed numerical margin for captured class |
| `str_ratio_0` | DTN-015 | 005 | 7.14608192821e-06 | 0.00246223796686 | 1.40746925226e-09 | 2.53889066326e-05 | 1.22726577282e-06 | meets proposed numerical margin for captured class |
| `term_force_0` | DTN-019 | 009 | 6.63890674682e-06 | 0.000198623074314 | 3.41087151856e-08 | 7.50021799045e-06 | 3.1846670612e-06 | meets proposed numerical margin for captured class |
| `vel_1` | DTN-005 | 007 | 7.12366386544e-06 | 0.000226196311616 | 1.2066577737e-09 | 2.54084477624e-05 | 1.25156599421e-06 | meets proposed numerical margin for captured class |
| `velmod_1` | DTN-006 | 007 | 7.12366386544e-06 | 0.000226196311616 | 1.2066577737e-09 | 2.54084477624e-05 | 1.25156599421e-06 | meets proposed numerical margin for captured class |
| `velmod_64` | DTN-006 | 007 | 7.34308507271e-06 | 0.000221754445022 | 1.20305854168e-09 | 2.53661640042e-05 | 1.50648348014e-06 | meets proposed numerical margin for captured class |

The 31 rows meeting the proposed margins and six unresolved rows are all
retained. The unresolved rows are `filt_t1_c0.25`, `filt_t4`, `filt_t5`,
`filt_t6`, `filt_t7` and `filt_t9`. Even the full proposed stable tolerances
are exceeded by held deviation for `filt_t6` and `filt_t7`, and log-radius
deviation for `filt_t9`; no threshold is raised and no result is rounded into
eligibility. The linked JSON retains full values and every maximum's variant,
channel and exact record pointer; displayed numbers are descriptive.

This supplies the missing per-setting five-way evidence for the captured
inputs, subject to the sole actual review's custody and method limits. It
does not supply untested pairwise spreads, general parameter/rate behavior,
new calibration decisions, public receiver or output joins. The old baseline
format reconstruction does not fabricate missing historical execution receipts.
MXCSR variants begin after parameter setting and apply to processing and
teardown; the libm variants act from loading and initialization. They are not
identical whole-program perturbation scopes. The libm wrapper selects results
with `r != rint(r)` (or its float form); this does not prove that every
mathematically inexact result or every library operation is covered.

All 15 requirement bodies and 42 existing case rows and IDs remain unchanged.
REQ-008's ungated DamperVelocity remains U; `damper_pos_0` is not that missing
parameter comparison. `pickup_pos_0` remains DTN-020 and supplies no new
DTN-021 position-0.5/37-frame evidence. Old NULLs, check-custody qualifications,
all other U and broad proposed criteria remain. The 27 released finite
evaluations and four chaotic exclusions are unchanged. All 37 settings in
this annex remain outside the published handoff; no release, new case ID,
statistical substitute or implementation input is admitted here.
