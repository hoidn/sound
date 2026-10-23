# Captured Version 12 manual heading census — R9

This finite source-discovery companion preserves the original **880 TOC rows,
708 original leaves and 43 chapters** unchanged. Actual retained chapter headings
are a separate discovery dimension. No paragraph semantics, behavioral contract,
completed topic/leaf, exact12.4.3 applicability or whole-product coverage is claimed.
The [existing coverage design](../../../../../wiki/research/full-live-specification-design.md)
and [plan](../../../../../wiki/research/full-live-specification-plan.md) retain closure.

The frozen `rg --files … -g '*.html'` input list has134 physical HTML paths and109
distinct content hashes. The census selects69 paths representing44 distinct byte
captures at43 exact official Version12 chapter URLs. It explicitly excludes53
Max API pages, two Version11 pages and ten Help article-body/response files. All
original43 chapter URLs have selected retained bytes; **zero unavailable chapters
in this snapshot does not mean zero missing product behavior**. Later files are
not silently added to this frozen set.

| Discovery dimension | Count |
| --- | ---: |
| Actual numbered heading occurrences across44 content variants | 1,088 |
| Distinct literal chapter-URL plus heading-ID URLs | 1,066 |
| Original TOC URLs matched literally | 880 |
| Additional actual heading URLs absent from original TOC | 186 |
| Actual heading tags across content variants | 44 h1 /365 h2 /493 h3 /186 h4 |
| Actual numbered-outline leaf occurrences /distinct leaf URLs | 854 /833 |
| Original TOC leaf URLs with actual numbered-outline children | 61 |
| Matched-URL number/title differences or conflicting observations | 0 |

All186 additional headings are actual h4 elements across18 chapters, including
the14 Browser headings independently recorded in the separate
[R8 discovery companion](../r8-browser-heading-dispositions/README.md). They are
not added to or merged with the original TOC here. The61 original leaf flags stay
exact discovery-time fields even when this captured outline has children.
“Leaf” in the new dimension describes only the retained heading outline.

There are25 byte-identical extra physical bindings. They are deduplicated only
by exact bytes/hash, while every physical path remains visible. The two different
Concepts hashes at the same URL remain distinct captures; neither is chosen as
latest authority or interpreted as a semantic/version change. Their22 matching
headings explain why exact-TOC match occurrences are902 rather than880.

## Evidence and exact boundaries

- [HTML inputs](html-inputs.json) freezes all134 paths/bytes/hashes, including
  exclusions, duplicates and archives. [Classifications](html-classifications.json)
  gives every path's explicit selection/exclusion basis.
- [Metadata inputs](metadata-inputs.json), [source records](source-records.json)
  and [manifest bindings](manifest-bindings.json) retain148 existing catalog files,
  355 exact URL/hash records and200 explicit manifest-file bindings. All134 paths
  have source-catalog content-hash associations;93 have a directly resolvable
  named-file manifest binding. The other41 remain physically pinned, with only
  the recorded byte-identity catalog association rather than invented capture history.
  Help article-body hashes remain distinguished from captured full responses.
- [Captures](captures.json) retains all44 selected source variants, physical
  bindings, exact source catalog pointers, document title, version/time assertions
  and actual headings. The pages provide explicit English alternate self URLs,
  not canonical links; a matching retained source-catalog URL plus the same HTML
  hash corroborates each selection. No URL is guessed from a filename or heading.
- [Heading ledger](heading-ledger.json) keeps actual h1..h6 tags with numeric
  `data-number`, exact ID/number, decoded text/title (including NBSP), attribute
  values, source HTML line/column and source-order outline ancestors. Only a
  literally displayed number prefix is removed for the separate title field.
  No title, number, parent, alias or normalized URL is used for joining.
- [TOC comparison](original-TOC-comparison.json) embeds every original row in
  original order. [Availability](chapter-availability.json) uses exact original
  chapter URLs. [Differences](differences.json) keeps extras, absent rows, duplicate
  IDs/numbers, variants and conflicting observations, including empty sets.
  [Summary](summary.json) owns the separate counts and zero-completion claims.

The parser reads only heading text within exactly one complete `chapter_content`
div, plus self-link/document-title metadata. Navigation, paragraphs, scripts,
figures, source examples and source modules are not executed or semantically read.
It records actual encountered heading-level ancestors, not DOM containment or
imagined intermediate headings. Twenty h4 records skip an actual h3 level
(including printed `.0.` number components); they retain explicit gap flags.
No replacement h3 or parent URL is fabricated. Duplicate and malformed cases stay
visible in the parser checks/difference model rather than being overwritten.

Eight selected captures have no safely resolved explicit UTC: editing MIDI,
editing MPE, audio effects, MIDI effects, MIDI Tools, grooves, tuning and Welcome.
Their original date-only/null fields remain exact assertions; no midnight, file
mtime, other copy's timestamp or HTTP time is substituted. Other capture UTC and
version assertions are individually retained with source pointers, without
selecting an authority. Current Version12 pages do not establish exact12.4.3 parity.

## Read-only reproduction

Inspect [derive.py](derive.py), then run from repository root:

```sh
python3 -B analysis/ableton-live-12.4.3/full-spec-v1/inventory-revisions/r9-captured-manual-headings/derive.py --check
```

`--check` reconstructs all deterministic outputs from the frozen finite inputs,
checks283 unique external source/catalog/baseline [pins](input-pins.json), original
TOC identity and all record/JSON pointer relationships, then verifies the
[manifest](manifest.json), local README links and untracked-aware whitespace.
Before/after hashes of the companion and external inputs must remain identical.
Selfchecks cover chapter boundaries, scripts/outside headings, numeric attributes,
h1..h6 depth/gaps, duplicate IDs/numbers, missing IDs/multiple/unclosed boundaries,
literal NBSP preservation and byte duplicates versus same-URL hash variants.
Without `--check`, author output is refused once sealed, and existing generated
outputs are not overwritten. Revisions require an explicit preserved successor.
No recapture, network, native/API/helper/script/runtime, hardware, installation,
implementation or candidate operation occurred. Root owns shared integration and
independent review; this source census does not modify R8 or any original capture.
