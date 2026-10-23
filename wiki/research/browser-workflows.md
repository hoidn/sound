---
id: RESEARCH-BROWSER-WORKFLOWS
type: research
status: current
updated: 2026-10-19
access: analysis
target: Ableton Live 12 Suite 12.4.3; current Live 12 documentation with patch applicability unknown
---

# Browser workflow evidence

## Question and canonical owners

Which browser interactions can be stated from retained official documentation,
without inferring UI behavior from index storage? [Browser index](browser-index-static.md)
and [SPEC-BROWSER-INDEX](../specs/browser-index.md) own native content/sidecar
facts. The new [workflow draft](../specs/browser-workflows.md) owns the selected
interaction contract. Full browser behavior remains incomplete.

## Retained source

Captured the official
[Working with the Browser chapter](https://www.ableton.com/en/live-manual/12/working-with-the-browser/)
on 2026-10-19, using Python's standard-library HTTP client. Retained bytes,
final URL, UTC time, length and SHA-256 are in the
[browser packet](../../analysis/ableton-live-12.4.3/full-spec-v1/browser/capture.json).
The [source manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/browser/source-manifest.json)
pins the HTML, normalized text, metadata and authored fixture definition.
Normalized text is a derived navigation aid; HTML bytes are the source.

The page identifies Version 12, without a pinned 12.4.3 patch revision. It therefore
supports documented-domain proposals, not a claim of exact-build behavior.
No original application or extracted original code was run for this packet.
Images were not inspected; their existence is not a visual result.

## Conclusions and limits

Ten selected interactions have explicit D12 requirements and acceptance setups
in the owning draft. Their exact-build applicability remains U; malformed,
cancellation and teardown outcomes remain ungraded. The authored set/membership
fixtures exercise distinctions in supported contracts, without claiming an
executable UI driver or actual observation.

Current manual services and automatic analysis features require separate
applicability evidence. Retained source identity establishes what was read,
not whether the pinned product implements it. [Q-027](../questions.md#q-027-whole-product-specification-evidence-and-version-coverage)
owns this cross-cutting gap. Next: independent review of source locators, claimed
search/list behavior, fixture consistency and the missing error/lifecycle cases;
then bounded native corroboration where it can settle exact-build applicability.
