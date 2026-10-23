---
id: SPEC-BROWSER-WORKFLOWS
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; documented Live 12 workflows, exact-build applicability unknown
---

# Browser search, navigation and preview workflows

## Scope and evidence boundary

FEAT-UI and FEAT-PERSISTENCE, under the [full-product design](../research/full-live-specification-design.md).
This partial draft owns selected browser interactions, not the interchange format
or native index. [Browser index](browser-index.md) remains canonical for content
kinds and sidecars; [plug-in discovery](plugin-discovery.md) owns discovery.

D12 means documented in the captured current official Live 12 chapter, **not**
observed in the pinned build. U means unresolved. No runtime result or complete
browser coverage is claimed. The following documented-domain requirements are
usable acceptance proposals; their exact 12.4.3 applicability remains U for every
row. No requirement from this page is released.

## Requirements

The case fixture defines valid, readable test assets and completed indexing.
Reset unrelated search/filter state before each case unless it supplies that
state. Use only the listed collection members and folder assets. Preview cases
require a nonzero preview/cue gain and a working monitored output path.
Search and list comparisons use sets unless a requirement explicitly orders them.
No claim about timing, Unicode, tokenization or tie order follows from the tests.
Evidence locators E1–E7 refer to the appendix.

| Requirement ID | Input/precondition | Required observable result | Strength/source |
| --- | --- | --- | --- |
| REQ-BROWSER-WORKFLOWS-001 | Multiple search words | Results match every word. | D12/E1 |
| REQ-BROWSER-WORKFLOWS-002 | Clear search with its x control | Text clears; selected filters remain. | D12/E1 |
| REQ-BROWSER-WORKFLOWS-003 | Clear through the results bar | Text and selected tags clear. | D12/E1 |
| REQ-BROWSER-WORKFLOWS-004 | Global find shortcut | All becomes selected; search receives focus. | D12/E1 |
| REQ-BROWSER-WORKFLOWS-005 | Navigate backward/forward | Previous searches and navigation states are accessible. | D12/E2 |
| REQ-BROWSER-WORKFLOWS-006 | Select collection | Members bearing its color are displayed. | D12/E3 |
| REQ-BROWSER-WORKFLOWS-007 | Add user folder | Index contents without relocating the folder. | D12/E4 |
| REQ-BROWSER-WORKFLOWS-008 | Configured folder unavailable | Retain a dimmed sidebar entry. | D12/E4 |
| REQ-BROWSER-WORKFLOWS-009 | Enable preview; select eligible asset | Play a preview. | D12/E5 |
| REQ-BROWSER-WORKFLOWS-010 | Enter sample on selected Session track | MIDI: load Simpler; audio: populate a slot. | D12/E6 |

## Timing, state and ownership

Search state, chosen location, selected tags, collection assignments and focus
are distinct observable state. The two clear operations have separate contracts.
None defines disk serialization. Use the sidecar owner's released subset where
applicable; do not infer that every browser operation creates one undo entry.

For preview, exact onset scheduling, output samples, gain, transport alignment,
output routing and cancellation are not specified by this partial requirement.
Loading destination slot choice, insertion point, replacement confirmation and
unsupported-file behavior also remain U. Device synthesis remains owned by its
device contract, not by the browser's load action.

## Acceptance cases

Fixture [browser-workflow-fixtures.json](../../analysis/ableton-live-12.4.3/full-spec-v1/browser/browser-workflow-fixtures.json)
is an authored declarative setup; it was not executed against Live. D cases are
graded in the documented domain only. They do not establish build parity.

| Case ID | Requirement | Kind | Setup/action | Expected comparator |
| --- | --- | --- | --- | --- |
| BWF-001 | 001 | Positive/negative | Query `copper bell` in F1. | Exact set F1.expected. |
| BWF-002 | 002 | State boundary | F2, search x. | F2.text empty; F2.tags unchanged. |
| BWF-003 | 003 | State boundary | F2, results Clear. | Both F2 fields empty. |
| BWF-004 | 004 | Keyboard/focus | Invoke platform global-find shortcut. | REQ-004 state. |
| BWF-005 | 005 | Navigation | Visit F1.location/query, F3.location/text; back; forward. | Respective search/location restored; history-depth limit U. |
| BWF-006 | 006 | Membership | Select F4's collection. | Exact set F4.expected. |
| BWF-007 | 007 | Positive/persistence | Add F5 folder; finish indexing. | Contents available; folder path unchanged. |
| BWF-008 | 008 | Missing resource | Register F5, close, disconnect its volume, reopen. | REQ-008; error wording/retry U. |
| BWF-009 | 009 | Positive | Select eligible F6 with preview enabled and audible cue path. | Audible output exists; samples/timing ungraded. |
| BWF-010 | 010 | Destination type | Enter F6 on MIDI, then audio track. | REQ-010; precise slot/insertion position U. |
| BWF-011 | 001–010 | Malformed | Corrupt asset or unreadable folder. | U; no refusal/repair/pass invented. |
| BWF-012 | 007, 009, 010 | Cancellation/teardown | Cancel scan/load; remove selected folder; stop preview; close. | U; no atomicity, undo, cleanup or timing outcome invented. |

Cases compare only their stated observable fields. A zero-result query and a
failed index/load are not interchangeable. Every case retains build applicability
U; no candidate or reference comparison is recorded as passing.

## Open questions

[Q-027](../questions.md#q-027-whole-product-specification-evidence-and-version-coverage)
owns current-manual versus exact-build applicability. Browser-specific gaps also
include substring/case/Unicode rules, tag boolean algebra, sorting stability,
search-state persistence, history bounds, automatic tags/similarity, custom label
and group editing, preview timing/routing/scrubbing, pack/cloud/Push/Splice behavior,
load compatibility, cancellation, permissions, errors and undo/recovery. These
surfaces remain inventoried but unclosed; this page does not cover them by analogy.

## Analyst evidence appendix

Canonical source synthesis: [browser workflow evidence](../research/browser-workflows.md).
The retained official chapter is
[manual-browser-2026-10-19.html](../../analysis/ableton-live-12.4.3/full-spec-v1/browser/manual-browser-2026-10-19.html),
with URL/date/whole-byte digest in
[capture.json](../../analysis/ableton-live-12.4.3/full-spec-v1/browser/capture.json).
The exact HTML heading IDs below survive chapter renumbering. Only the chapter's
text was inspected; illustrations are not evidence of inspected visual behavior.

| Locator | HTML heading ID | Requirements |
| --- | --- | --- |
| E1 | `search-bar` | 001–004 |
| E2 | `browser-history` | 005 |
| E3 | `collections` | 006 |
| E4 | `user-folders` | 007–008 |
| E5 | `previewing-files` | 009 |
| E6 | `adding-content-from-the-browser-to-a-live-set` | 010 |
| E7 | `content-pane`, `filters-and-tags`, `places` | Remaining inventory gaps only |

No original code was executed. Existing index-derived results do not corroborate
these UI transitions end to end. Newer manual services have not been assigned to
the pinned product without evidence.

## Revision and handoff

| Revision | Date | Change |
| --- | --- | --- |
| 1 | 2026-10-19 | First partial documented-domain draft: ten requirements, ten partly bounded D12 acceptance cases and two ungraded error/lifecycle cases; exact-build applicability U throughout. Separate review was pending at initial authoring. |

Independent [review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/governance-browser-review.json)
approved this partial documented-domain contract after three fixture corrections:
explicit navigation location, narrowed folder-path comparator and controlled
reset/registration/preview conditions. This review-status note changes no
requirement or case. Exact-build applicability and wider browser coverage remain
unknown; there is no release or compatibility result.
