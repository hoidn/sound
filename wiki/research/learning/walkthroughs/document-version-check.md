---
id: LEARN-DOCUMENT-VERSION-CHECK
type: research
status: draft
updated: 2026-10-17
access: analysis
target: Ableton Live 12 Suite 12.4.3 arm64
---

# Following one attribute: how Live decides a set's version is acceptable

## The question

Every Live Set starts with a line like this, inside the gzip compression:

```xml
<Ableton MajorVersion="5" MinorVersion="12.0_12402" SchemaChangeCount="1" Creator="Ableton Live 12.4d1" Revision="42bc…">
```

What does Live 12.4.3 do with `MajorVersion`? Which values does it accept,
and what happens to the others? This lesson follows that one attribute through
the actual machine code, from the place where it is read to the place that
accepts or refuses it. Nothing here was executed. Each step is a reading of retained
disassembly, and the lesson ends where that evidence ends.

The canonical findings are on the [native research page](../../document-container-native.md);
the resulting contract is [SPEC-ALS-CONTAINER](../../../specs/als-container.md).

## Where the evidence is

The packet's query results are JSON *dossiers*: one file per function, holding
its pseudocode, its disassembly, and who calls it. All of them live under
`analysis/ableton-live-12.4.3/r2/n2-container-v1/results/`. Addresses are the
unslid addresses of the arm64 image `Live.arm64` (SHA-256 `3a99ceea…d1c383cfad`).
The function names Ghidra shows, such as `FUN_1015299e0`, are invented by
Ghidra, not recovered from Live.

How did the investigator find the right functions? It started from text.
The string `MajorVersion` sits at `0x105b916e7`. The
[reference report](../../../../analysis/ableton-live-12.4.3/r2/n2-container-v1/results/n2-0001/refs/0x105b916e7.json)
lists the code that uses it: exactly two functions. One writes documents
(`0x101485240`); the other reads them (`0x1015299e0`). We follow the reader.

## Step 1: the root element is checked by name

Open the [reader's dossier](../../../../analysis/ableton-live-12.4.3/r2/n2-container-v1/results/n2-0002/functions/0x1015299e0.json)
and find the `disassembly` entries from `0x101529c5c`. The parser calls this
function for every opening tag. On the first tag, the root, it does this:

```text
0x101529c5c ldr w8,[x21, #0x8]
0x101529c60 cmp w8,#0x7
0x101529c64 b.ne 0x101529ec0
```

`x21` points to the element's name and its length. The first branch rejects
any name that is not 7 bytes long. The next instructions compare two 4-byte
words, `Able` and `eton` (the two words overlap at the `e`), and branch to the
same place on a mismatch. That place throws
`Expected 'Ableton' root node, got '$1' instead`. So `ableton` in lower case
fails: the comparison is on exact bytes.

## Step 2: MajorVersion is read as an integer

Immediately after the name check:

```text
0x101529c98 adrp x2,0x105b91000
0x101529c9c add x2,x2,#0x6e7
0x101529ca0 bl 0x10152a900
0x101529ca4 str w0,[x19, #0xbc]
```

The first two lines build the address `0x105b916e7`, which is the string
`MajorVersion`. On arm64 a 64-bit address is often built in two steps like
this. The call goes to a helper that searches the tag's attributes for that
name, and the result is stored at offset `0xbc` of the parser object, `x19`.
Remember that offset; we meet it again in step 4.

The [helper's dossier](../../../../analysis/ableton-live-12.4.3/r2/n2-container-v1/results/n2-0003/functions/0x10152a900.json)
shows two outcomes. If no attribute has that exact name, it returns 0
(`mov w0,#0x0` at `0x10152aa54`). If one does, it hands the text to a number
parser and tests one bit of the answer:

```text
0x10152a9b4 bl 0x1002fd908
0x10152a9b8 tbnz x0,#0x20,0x10152aa58
```

`tbnz` means "test bit and branch if not zero". Bit 32 is the parser's success
flag, so a successful parse skips ahead and returns the number. Otherwise the
code falls through to `Illegal value for int attribute: $1`.

Notice what this means: a *missing* MajorVersion becomes the number 0, but a
MajorVersion of `five` is an error at this point.

## Step 3: a detour into the number parser

The [number parser](../../../../analysis/ableton-live-12.4.3/r2/n2-container-v1/results/n2-0005/functions/0x1002fd908.json)
is worth reading slowly. It is a good example of why a summary in a notes file
needs checking. The investigator's notes say it "trims spaces at both ends".
The disassembly shows it computes three things:

- where the first non-space is;
- one past the last non-space;
- whether a `+` comes first.

It then calls a converter with a start pointer and a *count*. But the count it
passes is `min(length − start, end)`, and `end` is a position, not a length.
When the value starts with a space or a `+`, the count is too large by that
much. The trailing space then stays inside the text handed to the converter.
` 5` and `5 ` reduce to `5`, but ` +5 ` reduces to `5 `.

We cannot see the converter itself (`0x1002fda78` is not in the retained
evidence). A standard decimal converter would stop at the space. The check
after it would then report failure, because the end pointer did not reach the
end. So `MajorVersion=" +5 "` is probably refused, which is the opposite of what
the packet's test case expected. The spec now marks that case unknown rather
than guessing.

## Step 4: the check happens one tag later

You might expect the version to be checked right after it is read. It is not.
The same reader function handles the *next* tag, the root's first child
(`LiveSet` in a set). It looks up that tag's class and, at `0x101529e88`, calls
the version check `0x101529024`. It does this only when the class is unknown or
marked as versioned. Open its
[dossier](../../../../analysis/ableton-live-12.4.3/r2/n2-container-v1/results/n2-0002/functions/0x101529024.json):

```text
0x101529038 ldr w8,[x0, #0xbc]
0x10152903c cbz w8,0x101529090
  …
0x101529060 and w9,w8,#0xfffffffe
0x101529064 cmp w9,#0x4
```

There is offset `0xbc` again: this is the MajorVersion from step 2. `cbz`
branches when the value is zero, to the code that throws
`MajorVersion attribute missing from 'Ableton' root node`. So a missing
attribute and a literal `0` produce the same message.

The `and` with `0xfffffffe` clears the lowest bit. 4 and 5 both become 4, and
every other number becomes something else. That is a compact way of writing
"MajorVersion is 4 or 5". If the comparison fails (`b.ne 0x101529120`, just
after), the code continues here:

```text
0x101529124 cmp w8,#0x6
0x101529128 b.lt 0x101529134
0x10152912c mov w8,#0x1
0x101529130 strb w8,[x20, #0x29]
```

For 6 or more it sets a flag at offset `0x29`, and then, either way, it throws
`Unsupported MajorVersion (<n>)`. The flag is the only difference between
"version 3" and "version 6", so where is it used?

## Step 5: the decision after the parse

The flag is read after the whole parse has finished, in
`0x1015289c8` ([dossier](../../../../analysis/ableton-live-12.4.3/r2/n2-container-v1/results/n2-0003/functions/0x1015289c8.json)).
These are its first decisions:

```text
0x101528a04 ldrb w8,[x19, #0x29]
0x101528a08 tbnz w8,#0x0,0x101528aec
  …
0x101528aec mov x0,x19
0x101528af0 bl 0x101528c84
```

If the flag is set, it calls `0x101528c84`, which raises one of Live's two
"document is from a newer version" errors. Without the flag, the same function
later finds the error recorded during parsing and raises "document corrupt
while reading" instead. The error names come from the static initializers that
register them ([`0x10148e4cc`](../../../../analysis/ableton-live-12.4.3/r2/n2-container-v1/results/n2-0002/functions/0x10148e4cc.c)
and [`0x101535400`](../../../../analysis/ableton-live-12.4.3/r2/n2-container-v1/results/n2-0002/functions/0x101535400.c)).

So the traced path gives these static derivations:

| MajorVersion | Outcome |
| --- | --- |
| `4`, `5`, `+5`, ` 5` | Passes this check |
| missing, `0` | Corrupt: "MajorVersion attribute missing" |
| `five`, empty | Corrupt: illegal integer value |
| `3`, `1`, `-2` | Corrupt: "Unsupported MajorVersion" (negative numbers assume the converter accepts a minus sign) |
| `6`, `7`, … | Newer-version error |
| ` +5 ` | Probably corrupt (illegal integer); depends on the unseen converter |

## Where the evidence stops

Three links in this chain are not in the retained code, and the lesson should
not pretend otherwise.

1. **How a thrown error becomes a recorded one.** Step 4 *throws*, but step 5
   runs after the parse and reads flags. Something between them must catch the
   error, stop the XML parser and record the message. The design implies it:
   why set a flag just before throwing, unless someone reads it later? But the
   catching code was not retrieved. Treat "refused as corrupt" as well
   supported, and the exact error class as inferred.
2. **What the user sees.** The error names are keys into `Languages.alp`, which
   we cannot read. Whether a dialog shows the detail text, and whether the
   previously open set stays open, are probes PRB-N2-03 and PRB-N2-04 in the
   [probe batch](../../../../analysis/ableton-live-12.4.3/r2/n2-container-v1/probe-batch.json).
3. **Which reading path File > Open uses.** There are two entry points into this
   parser. They agree about MajorVersion, but not about some MinorVersion values
   (see the research page). That is probe PRB-N2-05.

## Try the reasoning yourself

- `MajorVersion="4"` with a current `MinorVersion` passes this check. Does the
  set then load? The check says nothing about that. It is probe PRB-N2-06.
- A document has no `MajorVersion` and no `MinorVersion`. Which message comes
  first? (Step 4: the zero test runs before anything looks at MinorVersion.)
- A document has `MajorVersion="6"` and is also truncated halfway. Is it
  reported as newer or as corrupt? (Step 5 tests the newer flag first; the
  research page lists the full order.)

Return to the [learning index](../index.md), or see how the same packet reads
`MinorVersion` against the shipped `Schema` directory on the
[research page](../../document-container-native.md#runtime-use-of-schematxt).
