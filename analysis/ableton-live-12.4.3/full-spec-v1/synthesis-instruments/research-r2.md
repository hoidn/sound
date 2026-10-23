---
id: RES-SYNTHESIS-INSTRUMENTS
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 2
target: Ableton Live 12 Suite 12.4.3
---

# Five synthesis and drum instrument profiles

## Authority and bounded investigation

This is the F-06 analyst owner for Drift, Drum Sampler, Meld, Operator and
Wavetable. The [canonical draft](../specs/synthesis-instruments.md) owns behavior;
this page owns evidence interpretation and limitations. Read the
[inventory](full-live-coverage-inventory.md) and
[coverage design](full-live-specification-design.md) for the denominator and
closure rule. None of the five profiles is complete or released.

The existing manual/schema capture from [sample instruments](sample-instruments.md)
was reused, with exact hashes checked; no new fetch or original execution was
needed. The previous author had already retained five inventory-selected shipped
presets, decompressed XML and schema/preset observations. This continuation
preserves those captures and adds finite documentary requirements/cases,
paragraph locators, canonical snapshots and author validation.

## Sources and observations

The [source ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/sources.json) contains seven pins: the external
Version 12 instrument HTML captured 2026-10-19T20:27:58.247940+00:00, the external
installed `12.0_12402` schema, and five copied Core Library defaults. The manual
SHA-256 is `3975fec856ada335526b35504ab3ca058dbf8f2885169944e0a819d45990fd6a`;
the schema is `b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299`.
Manual patch parity remains U. The preset roots/fields are directly observed,
not reader/writer execution or a map of constructor defaults. Preset headers say
Live 12.4d1, not 12.4.3. Their package presence remains valid exact-build evidence
of supplied resources while their loading, semantics and DSP remain unproven.

| Device | Observed preset root | Manual section | Schema line | Retained paragraphs/headings |
| --- | --- | --- | --- | --- |
| Drift | `/Ableton/Drift` | §31.3 | 1737 | 95 [blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/manual-drift-blocks.json) |
| Drum Sampler | `/Ableton/DrumCell` | §31.4 | 1909 | 54 [blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/manual-drum-sampler-blocks.json) |
| Meld | `/Ableton/InstrumentMeld` | §31.8 | 3374 | 96 [blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/manual-meld-blocks.json) |
| Operator | `/Ableton/Operator` | §31.9 | 5640 | 211 [blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/manual-operator-blocks.json) |
| Wavetable | `/Ableton/InstrumentVector` | §31.13 | 3532 | 111 [blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/manual-wavetable-blocks.json) |

[Schema fields](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/schema-fields.json) and
[preset observations](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/preset-observations.json) preserve the exact
association. No field spelling establishes an enum, default, clamp, automation
eligibility, signal path or sound. Figures were not inspected separately.

## Source ambiguities and interpretation limits

**Operator restart — unresolved context.** The manual overview §31.9.4
`operator:B039–B041` describes Loop retrigger and restart from current level to
peak to avoid clicks. The complete parameter list §31.9.10.7
`operator:B197–B199` distinguishes general Loop/Beat/Sync, current-to-peak in the
Beat/Sync Repeat entry, and sustain-to-initial movement in Loop Time. These may
refer to distinct modes or phases. No contradiction is declared without matching
mode and preconditions; no prose is silently discarded. SYN-U-OP-LOOP / case
SYN-OP-012 retains distinct Loop/Beat/Sync setups with nonzero Initial/Sustain,
Attack and Loop Time, running/stopped clocks and unknown expected outputs.

**Meld count — unresolved version/context.** §31.8.2 `meld:B009` says twenty-four
types and six scale-aware types. §31.8.3 `meld:B012–B033` names twenty-five macro
types when all four Swarms and Chord are counted. The draft retains the named
macro controls and Chord's documentary scale behavior, but assigns no exact menu
count. The six-type scale-aware list at §31.8.8 `B060` does not include Chord;
this can be a different scale context, so Chord is not silently inserted into it.
SYN-U-ME-TYPES keeps the uncertainty visible. A version-matched UI enumeration or
bounded package mapping is needed to establish available type identities.

**Meld sign wording — target unspecified.** §31.8.6 `meld:B047` describes signed
matrix changes and faster/slower modulators without fixing the target/unit.
SYN-U-ME-TIME / SYN-ME-024 keeps this as a signal obligation and does not turn it
into a universal modulation law. Wavetable's explicitly documented additive and
multiplicative rules are not transferred to Meld or other instruments.

## Finite author packet

[Requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/requirements.json), [cases](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/cases.json)
and [stimulus recipes](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/stimulus-recipes.json) separate documentary
expectations from all-null exact-target results. Every requirement has source
blocks and a finite action, or is an explicit U lifecycle obligation with ten
concrete per-device cases. No omitted negative/malformed/cancel/teardown behavior
is labelled inapplicable. Effect/no-effect tests require active sections, routes,
nonzero depth/gain, valid notes/media and an audible paired positive baseline.
Media setups require future retained owned WAV/AIFF/AMS bytes; they are not
provided reference outputs. The extractor only parses pinned HTML; author tools
write analyst docs/catalogs and assert structural relationships.

| Device | D12 / U requirements | Cases |
| --- | --- | --- |
| Drift | 17 / 1 | 27 |
| Drum Sampler | 18 / 1 | 28 |
| Meld | 24 / 1 | 34 |
| Operator | 23 / 1 | 33 |
| Wavetable | 22 / 1 | 32 |

Total **109 requirements / 154 cases**, no S/X expectations, no executions and no candidate grades.

Required unknowns include exact 12.4.3 parity, audio curves/kernels/phase,
frequency and bend/tuning codecs, rate/block behavior, RNG/statistics, voice
stealing/stacking budgets, media/import failure semantics, automation/history,
state persistence/migration, cancellation, teardown, accessibility and CPU
performance. These prevent complete-draft or whole-profile closure. Existing
finite device handoffs and T1 are unaffected; Amp/Cabinet emulation remains
outside this packet and no restricted implementation workspace is claimed.

## Freeze and review

[Author manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/manifest-author-r2.json) freezes packet bytes,
external source pins and exact canonical page snapshots. Run
`python3 analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/validate-r2.py`
for the focused identity/catalog/link/frontmatter/whitespace checks. The retained
[author validation](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/validation-author-r2.json) reports actual scope;
a pass establishes structural consistency only. Root owns the shared index,
coverage, questions, plan and append-only log integration. Separate analyst
review is required before any reviewed-contract claim or sanitized handoff.

## Revision 2 discoverability correction

The existing 5 U lifecycle requirements now use requirement headings so the
existing requirements browser discovers all 109 IDs. Their IDs, U classification,
body text, 109 requirement records and 154 case records are unchanged. The
[original r1 seal and payloads](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/archive-r1/manifest-author-r1.json)
remain byte-for-byte preserved. The [narrow response](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/response-author-r2.json)
and [revision tool](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/revise-r2.py)
record this presentation-only change. Earlier independent semantic review retains
its prior partial scope; no runtime, whole-profile or compatibility claim expands.
