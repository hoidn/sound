---
id: LESSON-MIDI-INTEGER-PARSING
type: research
status: current
updated: 2026-10-17
access: analysis
target: Ableton Live 12 Suite 12.4.3 / shipped CPython 3.11 bytecode
---

# Why an invalid controller number is sometimes ignored

## The question

A controller profile contains integer assignments. If a value is missing,
outside its allowed range or not an integer, does the parser disable that
assignment—or fail while loading the profile? This sounds like one question,
but the retained code shows that the answer depends on which setting we mean.

This lesson follows one ordinary-number helper and then checks a contrasting
pad path. It teaches how to read a branch and an exception boundary. It does
not execute Live or establish what error message a user sees.

## Select evidence and find the code

The [MIDI source record](../../sources/midi-user-mapping-12.4.3.md) identifies the
copied module `_UserScript/__init__.pyc` and the xdis 6.3.0 static decode. The
module was decoded, not imported or run. The evidence is CPython 3.11 bytecode,
not arm64 machine instructions or reconstructed Python source.

Open the retained [disassembly](../../../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/disassembly/_UserScript/__init__.dis.txt)
and search for `Method Name:       parse_int`. A reproducible read-only route
from the repository root is:

```sh
rg -n -A 100 'Method Name:       parse_int' analysis/ableton-live-12.4.3/midi-user-mapping-v1/disassembly/_UserScript/__init__.dis.txt
```

This navigation was used while preparing the lesson. The earlier capture and
decoder provenance remain in the source record. The exact claim locator is
`parse_int`, source metadata lines 56–66, bytecode offsets 2–264, recorded as
PARSE-01 in the [parser findings](../../../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/parser-findings.json).
“Source metadata lines” means numbers carried by the bytecode; we do not have
the original `.py` file at the embedded build path.

That capture is not present on the Linux workstation. The
[S4 re-decode](../../midi-closure-r2.md#evidence-re-established) used CPython
3.11.13's own `dis` module instead of xdis. It reproduces every instruction
quoted below at the same offsets, in a slightly different layout. To follow
along there, open its [listing](../../../../analysis/ableton-live-12.4.3/r2/s4-midi-v1/listings/_UserScript/__init__.dis.txt)
and search for `## code parse_int`.

## Read the branch

Here are three short, verbatim selections from that disassembly. The numbers on
the left are source-line metadata and instruction offsets. Gaps mean this lesson
omits intervening instructions; the linked file contains the complete function.

```text
 57:           2 LOAD_CONST           (-1)
               4 STORE_FAST           (integer)
```

The function begins by storing `-1` in its result variable. That is a sentinel:
a special result meaning no accepted assignment at this parser boundary.

```text
             126 CONTAINS_OP          (in)
             128 POP_JUMP_FORWARD_IF_FALSE (to 134)

 62:         130 LOAD_FAST            (option_value)
             132 STORE_FAST           (integer)
         >>  134 JUMP_FORWARD         (to 262)
```

Read the preceding offsets 96–116 in the full file: they put `option_value` and
`range(integer_range)` into the membership check. Only a value inside that range
replaces the sentinel. The caller fixes the range: `create_instance` source
metadata lines 96–97, offsets 180–266, binds 128 for ordinary identifiers and 16
for channels. That means the accepted integer domains on those paths are
0–127 and 0–15 respectively. A helper with a parameter is not enough evidence;
the caller tells us what parameter it receives.

```text
 63:         138 LOAD_GLOBAL          (ValueError)
             150 CHECK_EXC_MATCH
             152 POP_JUMP_FORWARD_IF_FALSE (to 254)
```

This begins the handler for `ValueError`. The rest of the function logs that
error and returns the result variable, still `-1` when integer conversion failed.
An exception of another type is not silently covered by this handler. Missing
options branch to the return without attempting conversion (offsets 6–48).

## Do not generalize before checking the other path

The pad path calls integer conversion directly instead of using this helper.
PARSE-02 records `create_instance`, source metadata lines 195–220, offsets
1088–1756: a nonnumeric pad note can propagate `ValueError`; a pad channel is
read only after the note passes its validity check. There is no local catch in
that function. A malformed channel beside an invalid note therefore cannot be
assumed to take the same path as a malformed channel beside a valid note.

This is why “all bad controller numbers are ignored” would be the wrong contract.
It is also why “Live crashes on a bad pad number” would be unsupported: the
outer host's error recovery has not been traced. The canonical interpretation
and open boundary are in the [MIDI investigation](../../midi-user-mapping.md).

## What this establishes

| Kind | Conclusion |
| --- | --- |
| Observed in retained bytecode | The helper initializes `-1`, checks a range and catches `ValueError`; callers bind 128 and 16 |
| Static inference, conditional on this path | Ordinary missing, out-of-range and nonnumeric values return the sentinel at this boundary |
| Observed contrasting path | Pad parsing uses direct conversion and lacks that local handler |
| Unknown | User-visible host recovery, complete loader lifecycle and native MIDI effects |

Downstream code determines what the sentinel does. For ordinary channels,
PARSE-08 and BC-01 in the [mapping findings](../../../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/bytecode-mapping-findings.json)
trace a fallback to the generic default channel. Pads are assembled earlier and
follow different requirements. We do not need to repeat the whole contract here:
its current rules and exclusions live in the [draft spec](../../../specs/midi-user-mapping.md).

## Try the reasoning yourself

For the ordinary identifier helper with range 128, what would 127, 128 and a
nonnumeric string produce? The static-derived answers are 127, `-1` and `-1`.
Those are not results of an executed Live test. Now ask what a pad note containing
the same nonnumeric string does: it propagates a conversion error at the traced
boundary, and the user's eventual experience remains unknown.

On the ordinary-identifier path, conversion happens before the range check, and
Python's `int()` accepts more spellings than you might expect. The
[S4 classification](../../midi-closure-r2.md#clause-classification) derives that
`+20` and `0021` are accepted, `1_0` is read as 10, and `0x14` and
`20.0` disable the assignment. This assumes the embedded 3.11.6 interpreter is
unmodified, and none of it was executed in Live.

The next discriminating check would follow the outer loader's exception handling,
or run a bounded malformed-profile probe if that host outcome becomes necessary
for a contract. S4 found that `create_instance` has no exception table, so the
outcome depends on native host code. It prepared that probe as PRB-S4-03 in its
[probe batch](../../midi-closure-r2.md#phase-4-probe-batch). Repeating the same
helper disassembly would not answer it.

Return to the [learning index](../index.md) or follow the [program atlas](../../program-structure.md#one-code-path-we-have-traced-user-controller-configuration).
