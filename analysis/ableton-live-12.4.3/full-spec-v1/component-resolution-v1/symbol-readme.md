# Packet 1a: retained symbol layer

Author: modulation_finish. This is an analyst lexical inventory for plan revision 4's amended component layer, not the scenario integration map, a semantic subsystem assignment, or a route/coverage grade. Root coordinates the combined packet, its review and atlas adoption. Delay owns separately grounded RTTI/table recovery; Synthesis owns the indirect-site census/resolution. No function body, instruction, binary, call traversal, native/provider execution or demangler was used here.

## Reproduction and inputs

Run `python3 -B symbol-build.py --check` from this directory for a read-only reconstruction, or `--write` only where its four output names do not exist. Both paths first run 16 assert-based parser checks. Each invocation reads aliases, vtables and strings exactly once, hashing the complete byte stream while parsing it; line counts, sizes and hashes must match `r2/c1-live-v1/indexes-manifest.json`. Each source's identity is checked before/after its read, and all four input stats plus manifest bytes are checked through the entire derivation. Early unsealed exploratory derivations were refined before these outputs were offered for integration; “one pass” describes each derivation, not a claim that source files were only ever read once during authoring.

All data belongs to the pinned `Live.arm64` build, image SHA256 `3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad`. `symbol-summary.json#/sources` records complete index paths, byte counts and hashes. Source locators use one-based JSONL lines, zero-based bytes, and byte lengths including LF. `label_field` is the JSON pointer relative to the alias record (`name` or `symbols/i/name`). Slot indices are zero-based. No retained source bytes were changed.

## Files and membership interpretation

- `symbol-summary.json`: exact distinct-label/function counts, overlapping lexical categories, root inventory, requested root measures, T1 token candidates, and limitations.
- `symbol-memberships.jsonl`: the 45,948 alias entries with a literal `::` label, followed by all 80 vtable-export label records. Alias candidate pairs are `[label_field, scope_id]`; `source` is `[line, byte, length_including_LF]`. Each `scope_id` resolves in `symbol-owners.jsonl`. Equal primary/symbol labels within one row are deduplicated, keeping primary-name provenance. This is not an inherited class hierarchy.
- `symbol-owners.jsonl`: the interned lexical scope dictionary with distinct entry/name counts. The owner is the prefix before the last top-level `::` outside templates/parentheses/brackets. Root is before the first such separator. Namespace versus class, local lambda scope, imported ObjC label and semantic component are not decided by that text. Library paths, malformed/operator angle syntax and nested-template-only qualification remain explicit categories instead of guessed owners. T1 token matches are discovery tags, including matches inside template names, not family assignments.
- `symbol-string-candidates.jsonl`: 12,620 whole simple length-prefixed-name or explicit `_ZTV`/`_ZTS` syntax candidates. Its tuple schema is in the summary. Each candidate retains the original string address, complete row/byte locator, value digest and reference count. Templates/complex encodings and ordinary strings remain the 440,132-row pinned string-source complement. Even complete simple syntax may be a method name or incidental fragment; no class identity or function membership follows. Grounded RTTI identities belong to the separate class layer.

The remaining 374,522 alias entries are explicitly unclassified here: 370,696 generated-primary and 3,826 unqualified-primary entries. Their exact identity and names are the complement of the membership entry set within pinned `aliases.jsonl`; duplicating that source as another authority would not improve the inventory. All 420,470 alias entries are accounted for by this disjoint partition. These include 2,053 external rows and 20,059 thunk rows, so alias entries must not be called native function bodies or confused with the call index's smaller function population.

## Counts and the amendment's baseline

There are 91,903 **field occurrences** containing `::`: 45,948 primary-name fields plus 45,955 symbol-name fields. Every primary name is already present in that row's symbol array. After deduplication there are 38,154 distinct literal-qualified names across 45,948 distinct entries. The 39,700 raw `ableton::` prefix occurrences similarly represent 19,841 distinct names across 19,850 entries. Raw prefix counts do not imply well-parsed owners.

| Exact prefix | Distinct names | Distinct entries | Conservative parsed-root names / entries |
| --- | ---: | ---: | ---: |
| `ableton::` | 19,841 | 19,850 | 17,942 / 17,951 |
| `flip::` | 2,564 | 2,564 | 2,564 / 2,564 |
| `boost::` | 2,301 | 2,301 | 2,298 / 2,298 |
| `std::` | 987 | 1,027 | 673 / 695 |

The parsed-root subset deliberately withholds ambiguous template/operator syntax. Root/prefix/owner statistics overlap and must not be summed as semantic components. There are 22,548 distinct parsed lexical owners. The exporter supplies 2,191 slot-like records across 80 vtable rows, containing 894 distinct target values; exporter stop rules and mixed adjacent data mean neither a table's extent nor method callability is established by this count.

## How this can constrain receivers

An exact alias method owner and an independently grounded class/table identity can restrict a candidate dispatch set. That requires a separate proof of the actual receiver/address point, physical slot association, ABI/adjustments, control path and invocation. A shared namespace, template argument, substring, string reference, or function appearing in multiple exporter tables supplies none of those predicates. This layer adds **zero newly resolved indirect sites**, closes no observable outcome, and grants no runtime, implementation or whole-product compatibility conclusion. Unnamed and ambiguous entries remain available for later independent evidence, not declared absent or unreachable.
