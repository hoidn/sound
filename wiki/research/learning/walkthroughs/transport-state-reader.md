---
id: LEARN-TRANSPORT-STATE-READER
type: research
status: draft
updated: 2026-10-17
access: analysis
target: Ableton Live 12 Suite 12.4.3 arm64
---

# Following `LoopOn Value="true"` into Live

**Where does the text `true` in a Live Set end up, and what happens if it says
`TRUE` instead?** The [first native lesson](first-native-loop-factory.md) found
a constructor that clears two bytes at offset `0x60`. It could not say whether
those bytes had anything to do with the saved `LoopOn` field. This lesson follows
the field from the document text to that offset, using real instructions. It also
marks where the evidence stops.

The [native transport-state page](../../transport-state-native.md) owns the
findings. The draft contract is [SPEC-TRANSPORT-STATE](../../../specs/transport-state.md).

## The field and the question

Every shipped set stores the arrangement loop switch as
`/Ableton/LiveSet/Transport/LoopOn/@Value`. The schema declares `LoopOn` as a class
whose only field, `Value`, has base type `Bool`
([static half](../../transport-state-static.md#selected-classes-in-120_12402)).
We want to know three things: which text values the reader accepts, where the
result is stored, and what happens when the element is missing.

## Step 1: find the text conversion by its error message

A good way into a parser is a message it would print on bad input. The corpus
strings index lists `Unexpected value for bool node: $1`. Its only referencing
function is `0x10152bfb8`, which converts attribute text into a typed value. It
dispatches on a base-type number, and `0x10` selects the Boolean branch. Here is
that branch, verbatim from the retained dossier
([n1-0006](../../../../analysis/ableton-live-12.4.3/r2/n1-transport-state-v1/results/n1-0006/functions/0x10152bfb8.json)).
`x20` points to the text and `[x20, #0x8]` holds its length:

```text
0x10152c1c8 ldr w8,[x20, #0x8]
0x10152c1cc cmp w8,#0x1
0x10152c1d0 b.eq 0x10152c930
0x10152c1d4 cmp w8,#0x5
0x10152c1d8 b.eq 0x10152c908
0x10152c1dc cmp w8,#0x4
0x10152c1e0 b.ne 0x10152c95c
0x10152c1e4 ldr x8,[x20]
0x10152c1e8 ldr w8,[x8]
0x10152c1ec mov w9,#0x7274
0x10152c1f0 movk w9,#0x6575, LSL #16
0x10152c1f4 cmp w8,w9
0x10152c1f8 b.ne 0x10152c95c
0x10152c1fc b 0x10152c940
```

The constant `0x65757274` is the four bytes `t r u e` read as one little-endian
word. Text of length 4 equal to `true` jumps to `0x10152c940`, which sets `w1=1`
and calls the Boolean setter. The length-5 branch at `0x10152c908` compares
`fals` + `e` and goes to `0x10152c970` (`w1=0`). The length-1 branch at
`0x10152c930` accepts the character `1`. Anything else reaches `0x10152c95c`:

```text
0x10152c95c adrp x1,0x105ab3000
0x10152c960 add x1,x1,#0x2f8
0x10152c964 mov x0,x20
0x10152c968 bl 0x10152bf4c
0x10152c96c cbz w0,0x10152cc74
0x10152c970 mov x0,x19
0x10152c974 mov w1,#0x0
```

The string at `0x105ab32f8` is `0`
([vtable-reads](../../../../analysis/ableton-live-12.4.3/r2/n1-transport-state-v1/vtable-reads.txt)
records the bytes). So `0` means false. Every other text goes to `0x10152cc74`,
which allocates and throws the "Unexpected value for bool node" exception. `TRUE`
fails because the comparison is an exact byte match. No case folding or whitespace
trimming happens on this path.

## Step 2: where the converted value goes

The converted value lands in a temporary document-node tree, not yet in the
transport object. Later, each object reads its node through a virtual method. For
`ALoopOn`, the vtable slot `+0x140` holds `0x101487310`
([vtable-reads](../../../../analysis/ableton-live-12.4.3/r2/n1-transport-state-v1/vtable-reads.txt),
the `ALoopOn` block). That loader loops over the members **present in the node**.
For a Boolean member it does this
([n1-0008](../../../../analysis/ableton-live-12.4.3/r2/n1-transport-state-v1/results/n1-0008/functions/0x101487310.json)):

```text
0x101487450 bl 0x1054d4970
0x101487454 ldr w9,[x22, #0x30]
0x101487458 mov x8,x20
0x10148745c tbnz w9,#0x1f,0x101487464
0x101487460 ldr x8,[x20, x9#0x0]
0x101487464 ldrsw x9,[x22, #0x38]
0x101487468 strb w0,[x8, x9]
```

`0x1054d4970` is the import stub for `AAbstractNode::GetValue<bool>`, which returns
the parsed Boolean in `w0`. `x22` is the member descriptor. `strb` stores that one
byte at the object plus the descriptor's offset (`[x22, #0x38]`). No setter is
called, so nothing else can intervene in this store.

Which offset? The descriptor is created when the class registers its members. The
corpus pseudocode of `0x101564330` registers `ARemoteableBool`'s value:

```c
FUN_10147e954(&DAT_106e0ea80,0xffffffff,0xffffffff,0x60,L"mValue",6,&DAT_1062a3ca0,0,auStack_30,
              0x4fffffffc);
```

It is called with offset `0x60` and the name `mValue`. The registration helper
drops the `m`, which leaves `Value`, the attribute name in the file. The class
registry `0x1027744a4` declares `ALoopOn` with `ARemoteableBool` as its parent. So
`<LoopOn Value="true" />` ends up as the byte at `ALoopOn + 0x60`. That is the same
offset the first lesson saw being cleared, and the same byte the one-line getter
`0x1015645a0` returns.

## Step 3: what if the element is missing

The loader visits only members that exist in the node. If `<LoopOn …/>` is absent,
or has no `Value`, nothing is stored and the byte keeps its constructor value. The
transport constructor `0x102760d88` sets it explicitly
([n1-0008](../../../../analysis/ableton-live-12.4.3/r2/n1-transport-state-v1/results/n1-0008/functions/0x102760d88.json)):

```text
0x102762eac ldr x0,[x19, #0x228]
0x102762eb0 stp x22,xzr,[x29, #-0xb0]
0x102762eb4 sub x2,x29,#0xb0
0x102762eb8 mov w1,#0x0
0x102762ebc bl 0x101564728
```

Offset `0x228` holds the `LoopOn` object (its member was registered at `0x220`, and
the object pointer sits 8 bytes later). `0x101564728` stores `w1` at `+0x60`.
Missing `LoopOn` therefore reads as loop off. This is a static derivation, and it
holds only if load always starts from a freshly constructed transport.

## Where the evidence stops

- We traced the parser, the node and the loader, but not the top-level function
  that opens a set and catches the exception. "The set does not open" is the
  natural reading of an uncaught read error, but the dialog and recovery are
  untraced (PRB-N1-01).
- The trace shows where the byte is stored, not what the audio engine or the loop
  brace does with it.
- The loader's store bypasses setters. A Double field with an out-of-range value
  is therefore stored as written, and whether a later step clamps it is unknown
  (PRB-N1-03).

**Reader exercise.** The float branch of `0x10152bfb8` calls `strtod` and only
checks that the end pointer moved. Predict what `<LoopStart Value="4.5abc" />`
loads, then check your answer against REQ-TRANSPORT-STATE-004.
