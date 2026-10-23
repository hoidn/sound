# R8: fourteen Browser headings absent from the original TOC

This is a finite source/navigation diagnosis for Q047, with no new behavioral
specification, source capture, citation join, completion or target parity claim.
The [R6 crosswalk](../r6-citation-crosswalk/README.md) and its 46 unmatched Browser
references remain exact. All 880 original TOC rows, 708 leaves and 43 chapters
remain unchanged. No application, account, service or controller was exercised.

[Heading dispositions](heading-dispositions.json) gives fourteen separately
identified retained-source headings. Each identity includes its exact URL and
full source hash; it is not a new original-TOC row. [Reference pointers](r6-reference-pointers.json)
retains all 46 original records, their R6 JSON pointers, original clause/block
pointers, case links and null/unknown flags. [Inputs](inputs.json) pins the old
R6 packet/review, current Browser packet/review/canonicals, both retained raw
HTML identities, original TOC rows/denominator/manifest and original parser.
The original inventory capture script was read as data and never imported or run.

## Retained-source result

All fourteen exact anchors are unique numbered `h4` headings within the retained
Browser chapter. None is a link target or an ID node in the retained original
TOC page; the Browser page likewise has no navigation link to them. Both raw
pages independently yield the same sequence of 880 numbered TOC link
numbers/titles/URLs. The original parser's number expression accepts four-part
numbers and has no explicit heading-depth filter. Thus these headings are absent
from the captured navigation link set; the evidence does not identify a parser
selection omission or establish a capture-version difference as its cause.
Publisher intent and the precise publication cause remain unknown.

| Retained heading number | Exact anchor |
| --- | --- |
| 4.7.3.1 | logging-into-splice |
| 4.7.3.2 | searching-for-splice-samples |
| 4.7.3.3 | working-with-splice-samples |
| 4.7.3.4 | splice-library |
| 4.7.3.5 | splice-settings |
| 4.7.6.1 | abl-assets |
| 4.7.6.2 | chord-banks |
| 4.7.6.3 | clips-folder |
| 4.7.6.4 | defaults-folder |
| 4.7.6.5 | grooves-folder |
| 4.7.6.6 | presets-folder |
| 4.7.6.7 | samples-folder |
| 4.7.6.8 | templates-folder |
| 4.7.6.9 | managing-files-in-the-user-library |

Each ledger row retains the complete raw heading HTML/start tag, attributes,
line/column, text, source capture identity and ordered heading outline. Fourteen
separate `source-heading-outline-child-of` relations point to source-proven
Splice/User Library ancestors. The heading levels and numeric prefixes agree.
These are outline relations between sibling HTML elements, not DOM parentage,
direct TOC matches, leaf semantic support or inherited citation joins. Both
original parent rows remain original TOC leaves. All 46 citations remain
`exact-URL-absent-from-TOC` with a null matched ID, unknown semantic coverage and
U target applicability. Current Version12 documentation does not establish
exact 12.4.3 applicability or any service outcome.

## Read-only reproduction

Inspect [derive.py](derive.py), then run:

```sh
python -B analysis/ableton-live-12.4.3/full-spec-v1/inventory-revisions/r8-browser-heading-dispositions/derive.py --check
```

The bounded stdlib parser verifies input hashes, exact original 880-row
reconstruction, the second page's identical navigation projection, all fourteen
raw tags/numbers/outlines, all 46 original references, parser fixtures, snapshots
of derived ledgers, manifest integrity, local links and whitespace. It writes
nothing. Initial author creation without `--check` refuses after a seal exists.
Independent navigation review remains pending. This packet neither replaces the
original denominator nor starts a general heading census or new work queue.
