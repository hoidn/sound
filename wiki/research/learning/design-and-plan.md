---
id: PLAN-RE-LEARNING
type: research
status: current
updated: 2026-10-09
access: analysis
revision: 1
---

# Design and execution plan for learning materials

## Outcome and audience

A technically curious reader should be able to open actual recovered code,
understand why we inspected it, follow one supported conclusion, and identify
what the evidence does not establish. The materials also explain the evolving
structure of Live. They teach the investigation, not how to build a replacement
from recovered internals. This is the learning work package of the
[native roadmap](../native-decompilation-roadmap.md#pedagogy-and-the-evolving-program-map).

The reader needs basic familiarity with files, functions and conditional logic.
No Ghidra, ARM64 or Python bytecode knowledge is assumed. Define those terms at
first use and keep a small glossary in the method guide. The goal is a navigable
explanation, not a second corpus of tool transcripts.

## Information design

| Page | Owns | Does not own |
| --- | --- | --- |
| [Learning index](index.md) | Reading order and current lessons | Findings copied from subsystem pages |
| [Method guide](method.md) | Terminology, reading techniques and evidence discipline | Claims about unexamined Live internals |
| [Program atlas](../program-structure.md) | Plain-language relationships with evidence and uncertainty | Behavioral requirements or candidate architecture |
| Walkthroughs linked from the index | One real question, navigation, reasoning and limitation | Synthetic code presented as recovered source |
| Existing research/spec pages | Canonical detailed findings and proposed contracts | Tutorial navigation |

Every consequential diagram edge carries a label or a nearby evidence row.
Containment means “is packaged inside”; a dependency means “names a required
image”; a static call means “code contains a call”; none implies a runtime
thread, process message or audio signal route. Inferred responsibilities are
explicit prose hypotheses, not unlabeled boxes in an architecture diagram.

Walkthroughs retain this sequence: question → source selection → actual
navigation → a small real excerpt → reasoning → observed/inferred/unknown →
next discriminating check. Commands only read retained evidence unless clearly
marked otherwise. Source-line metadata is distinguished from lines of recovered
source; static addresses are tied to image identity and architecture.

## Task sequence and acceptance

| Task | Concrete work | Completion check | State |
| --- | --- | --- | --- |
| L1 | Create index, method glossary and initial atlas from retained package/MIDI evidence | Links resolve; atlas separates package containment from traced code relationships | Written; independent reader review passed |
| L2 | Add a bytecode companion illustrating a supported rule and an unresolved boundary | Reader can locate `parse_int`, explain the sentinel/range check, and avoid generalizing it to pads | Written; independent reader review passed |
| L3 | Explain the first actual main-Live export | Link real pseudocode, provider warnings, input identity and exact function; no invented success | Written from selected no-analysis export; independent reader review pending |
| L4 | Update atlas and add persistence/transport walkthroughs with the native packets | At least two native lessons, including a limitation; relationships match cited evidence | Two native lessons and atlas updates written; packets remain partial; independent reader review pending |
| L5 | Independent reader review and corrections | Reviewer reproduces navigation, states one supported conclusion and one limitation, and distinguishes containment from code structure | Planned |

L1 and L2 execute immediately from existing retained evidence. L3 follows the
coordinator's main-image export; it is not replaced by the helper or bytecode
lesson. L4 follows actual behavior packets. L5 occurs before phase closure,
with review findings retained alongside phase evidence and linked here. Root
coordination owns research-index, coverage and log updates; this work package
owns these learning pages and the atlas.

## Verification and maintenance

Check frontmatter, relative links, heading anchors, inbound index links and
whitespace after each group of edits. Independently inspect the cited snippet
against the retained artifact. Reader review assesses whether the explanation
can be followed; it does not increase the underlying claim's confidence or
establish runtime compatibility.

Update the atlas and related lesson whenever a new finding changes their
interpretation. Preserve the prior evidence and record the correction in the
[project log](../../log.md). A page may be readable while its behavioral question
remains unknown. All pages and recovered-code links remain analyst-only.

The [initial reader review](../../../analysis/ableton-live-12.4.3/native-live-arm64-v1/learning-reader-review.json)
pins the five reviewed page hashes, checks 52 links/anchors and three bytecode
excerpts, and records the reader’s supported conclusion and remaining boundary.
It covers L1/L2 only; native lessons and phase-closing reader review remain open.

Native materials now include the
[factory lesson](walkthroughs/first-native-loop-factory.md) and
[wrapper-boundary lesson](walkthroughs/transport-wrapper-boundary.md). The
[transport study](../native-transport-study.md) records their canonical partial
packets and the completed four-callee follow-up. Readable native exports and
clear lessons do not imply that a native behavioral contract is releasable.

A [method follow-up review](../../../analysis/ableton-live-12.4.3/native-live-arm64-v1/learning-method-review-v2.json)
checks the explanation of opening, analysis, export and interpretation. The atlas
now also links the reviewed schema recapture as a declared document relationship;
it does not promote that relationship to a native object graph.
