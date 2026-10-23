# Component layer and indirect-call resolution — packet 1a

Analyst evidence for Ableton Live 12 Suite 12.4.3, main arm64 executable
SHA256 `3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad`.
This packet precedes the integration map under the
[amended plan revision 4](../../../../wiki/research/full-live-specification-plan.md#amendment--indirect-call-resolution-precedes-the-map-2026-10-20).
It does not grade externally observable behavior, establish runtime order or
recover the complete architecture. Payloads are frozen; independent review is pending as of this manifest.

## Inputs and units

[Input pins](packet-inputs.json) verify the five retained `c1-live-v1` indexes
against their original manifest. Mutable policy pages are pinned as of selection;
later edits do not invalidate retained source evidence.

- Symbol occurrences, distinct labels and distinct function entries are different
  units. A namespace or class spelling is a lexical navigation aid. It does not
  establish a subsystem, receiver identity or an execution boundary.
- An exported indirect site can be a call or a computed jump. Nonempty target
  references and targets that name a known function are separate measures.
- A table's executable slot prefix, its RTTI/class identity, a constructor store,
  and a site's receiver/slot chain need separate evidence. An available table
  never resolves every call with a matching slot offset.
- Grounded static class-slot targets remain conditional on the stated object and
  ordinary-call premises. Runtime reachability and behavioral outcomes stay unknown.

## Evidence parts

The packet combines independently authored [symbol membership](symbol-readme.md),
[class/table recovery](class-README.md), and the indirect-site census/resolution. Source row numbers are
one-based; byte offsets and addresses are exact source locators, with each
producer stating whether its record hash includes the newline. The original
indexes remain unchanged; derived edges are an overlay.

The first integration search uses forward and backward frontiers with hub pruning
and explicit per-level bounds. It cannot treat an unresolved indirect site as a
dead end. The search bounds and pruning rule belong to that map's evidence;
this prerequisite inventory performs no scenario traversal.

## Frozen inventory scope — independent review pending

| Unit | Retained or derived count | Evidence |
| --- | ---: | --- |
| Qualified primary/symbol field occurrences | 91,903 | [Symbol definitions and reconciliation](symbol-readme.md) |
| Distinct qualified labels / function entries containing them | 38,154 / 45,948 | [Symbol summary](symbol-summary.json) |
| Conservatively parsed lexical owners | 22,548 | [Owner dictionary](symbol-owners.jsonl); namespace versus class remains undetermined |
| Typeinfo-layout records / distinct literal encodings | 28,017 / 25,101 | [Class summary](class-summary.json) |
| Structurally matched address points / executable-prefix slots | 25,485 / 458,796 | [Class tables](class-tables.jsonl); prefixes capped at 128, not full table extents |
| Unique indirect sites: call-kind / computed jump | 244,762 / 23,253 | [Baseline census](indirect-baseline.json) |
| Sites with exported target references | 25,071 of 268,015 | Same baseline; includes jump targets and non-function destinations |
| Sites with an exported known-function target | 21,685 of 268,015 | Same baseline; not virtual-call coverage |
| Added conditional class-slot records | 24 | [Resolution overlay](indirect-resolution.jsonl), all previously empty exported target lists |
| Exported-or-conditional site inventory | 25,095 of 268,015 | [Scoped report](indirect-report.json); not an unconditional resolved-call count |

The added cohort starts with the retained transport sender and then the first
23 eligible constructor callers in numeric address order. Selection found 754
direct constructor callers, of which 435 met the declared bounded call-site
predicate. It is not a representative sample of semantic components. Each new
record joins stack receiver construction, address point `0x106756188`, slot
`+0x10`, and the native call PC to target `0x101ab7898`. Stable receiver/vptr,
ordinary-call and no-interference premises remain explicit; opaque intervening
calls are listed. The original indirect index is not changed. No other recovered
class or lexical store is assigned to a site without that evidence chain.

The static decode batch uses the existing decoder on owned byte extracts, with
zero original function calls. Per-process commands, input identities, raw
instructions and results are retained in the `indirect-native-*` payloads.
The per-function and total budgets are stated in the selection/report; neither
selected prefix length nor `LC_FUNCTION_STARTS` establishes full function extent.

## Checks and review

Producer self-checks exercise the distinction between duplicates, lexical
ambiguity, table candidates and grounded targets. The packet manifest pins all completed payloads; the wiki atlas is separately
pinned as of freeze because it remains a mutable synthesis. One independent structure
review is required before packet 1b is selected. Mechanical checks cover changed
payloads and affected documentation; no full released-handoff replay is needed
for this analyst inventory.
