# Synchronization full-source semantic audit — proposed

This audit reads the entire retained synchronization chapter body and reconciles its individual source predicates and contexts with the existing partial [spec](../../../../wiki/specs/synchronization-workflows.md), [research](../../../../wiki/research/synchronization-workflows.md), [R1 packet](../synchronization/manifest-author-r1.json) and [independent R1 review](../reviews/synchronization-workflows-review.json). It does not add a feature page, revise any current requirement/case, revoke partial review, or establish application, source-topic or leaf completion. No source or frozen input was changed.

All 54 original blocks remain in order: 12 headings and 42 paragraph/list blocks. Hand-selected exact normalized-text spans yield 130 units covering every nonwhitespace source character. The ledger preserves source hash, literal text, paragraph ID, anchor, HTML line, JSON pointer and character interval. This is paragraph/clause reconciliation, not citation counting. A filled row proves neither its semantic mapping judgment nor target compatibility.

| Unit disposition | Count | Meaning |
| --- | ---: | --- |
| Represented partial source clause and case | 30 | A named control/state role has an existing clause and a sufficiently directed future action. Still partial, target U and unexecuted. |
| Documented but outcome U | 59 | Source role and relevant future action exist; signal/timing/protocol/detection outcomes remain prose-only and unmeasured. |
| Missing clause, case or context | 9 | Nine source spans yield eight concrete proposals. No new normative IDs allocated. |
| Research-only protocol/private/marketing context | 15 | Includes analogies, examples, optimization, broad product/reliability and qualitative performance language; no private algorithm was read or prescribed. |
| Editorial | 15 | Headings, transitions and internal narrative reference. |
| Image/link uninspected | 2 | Prose FAQ referrals; the destinations were not opened. |

The old 54-block extraction omits figure captions and markup. This audit additionally retains all 14 textual captions, all 14 image elements and all 14 hyperlink elements in the chapter body. Caption text and literal URLs/attributes were read; image pixels were not inspected, and no external linked destination was fetched. Same-chapter reference text was already read. No unassigned substantive body text remains in the independent markup pass. Navigation/footer/site content outside `chapter_content` is outside the manual-chapter scope.

[source-unit-ledger.json](source-unit-ledger.json) contains sufficiency judgments and exact existing requirement/case contract/action pointers only where used as support. Existing citations need not name the same overview block; that distinction is explicit. [source-block-ledger.json](source-block-ledger.json) preserves all original blocks. [supplemental-markup.json](supplemental-markup.json) retains captions, image and link provenance. [catalog-reconciliation.json](catalog-reconciliation.json) accounts for all 26 existing requirements and 36 cases, including the two generic U requirements and ten broad future probes with no direct mapped source predicate. Twenty-four documentary requirements and 26 case actions have some partial source mapping; this is no completeness count. Existing nine nonnull documentary proposals retain their original named-control-only comparator scope; every actual target output/comparison is null/U and all cases remain unexecuted. The audit supplies no new expected output.

[gap-proposals.json](gap-proposals.json) proposes only these bounded successor changes:

- SA-G01: remaining-peer continuity when a third participant joins/leaves; existing two-peer leave/rejoin cannot test it.
- SA-G02: distinguish source-described initial Link-toggle visibility from explicitly edited Show/Hide state.
- SA-G03: explicitly exercise adjacent-menu Link/Audio switches.
- SA-G04: inspect that menu's connected Audio-enabled peer list with an independently known capability contrast.
- SA-G05: observe initial tempo with explicitly known first participant before ordinary tempo edits.
- SA-G06: retain the textual Follow placement context without pixel/figure assumptions.
- SA-G07: explicitly preserve/test MIDI Clock receiver following host tempo changes, without a tick codec or timing law.
- SA-G08: obtain independently admitted MTC receiver-only/not-host capability evidence; receiving alone cannot establish exclusion.

Each proposal has null actual and documentary outputs/comparators and target U. Future evidence requires independently known usable peers, real capability/build identities, active nonzero paths where audible, owned configurations and a separate positive baseline. Missing source/hardware/feature never passes a negative case. Broad malformed, cancel, undo, persistence, loss, rate, arbitration and teardown probes remain incomplete U obligations. No execution is authorized by a proposal.

[context-questions.json](context-questions.json) preserves exact12.4.3/Link Audio capability uncertainty, peer/Push direction distinctions, Tempo Follower optimization versus rejection, Clock versus MTC and Link Start Stop Sync boundaries. The retained chapter does not give MIDI Start/Stop wire policy, preroll, calibrated lag/default offset/delay/rate values, enumerated SMPTE rates, clock/detector algorithms or measured tolerances. No such law follows from labels, LEDs, buffered text, count, “real time,” “reliable” or “perfect sync.”

[owner-impact.json](owner-impact.json) pins bounded existing recording/routing/launch/hardware-latency/settings/loaded-transport owner context and inventories exact frozen R4 navigation references. The R4 and all audited R1 payloads remain byte-identical. It is not a whole-repository reverse dependency claim; evolving shared registers and the separate R9 census remain root-owned. A reviewed successor must get a new identity/citation revision; do not silently redirect old frozen pointers.

Run `python3 -B analysis/ableton-live-12.4.3/full-spec-v1/synchronization-source-audit/validate.py` from the repository root. It checks source/manifest/review/payload pins, original extraction and block order, literal spans/no text drops, IDs/pointers/current null flags, proposed nulls, owner/downstream pointers, canonical snapshots, local links and untracked-aware whitespace. `derive.py --check` independently reproduces this audit read-only. `derive.py --write` refuses after sealing. Neither checker imports or executes original application/helper functions or accesses a network. Validation cannot prove semantic sufficiency; independent review is pending.

Only this audit directory was written. No canonical, existing packet, shared index, plan, coverage, question register or log was edited; root handles integration. No new capture, runtime, network connection, hardware, original functions, application, candidate or tooling installation was used.
