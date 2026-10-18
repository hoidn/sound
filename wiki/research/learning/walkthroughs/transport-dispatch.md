---
id: LEARN-TRANSPORT-DISPATCH
type: research
status: draft
updated: 2026-10-17
access: analysis
target: Ableton Live 12 Suite 12.4.3 arm64
---

# Resolving an indirect call: where Start and Stop requests go

**Why did Start and Stop stop at a `blr x8`?** Both bodies call one small helper,
`0x101a4abd8`, and that helper calls a function whose address it loads from
memory. A call through a register has no fixed target in the instruction, so the
earlier lesson's method of following `bl` instructions stops there. This lesson
shows how the target was found without running Live. It also shows how a
separately shipped, symbol-rich build named the pieces, and why the answer
changed the question.

It follows [Learning from a transport export failure](transport-wrapper-boundary.md).
The [transport transitions page](../../transport-transitions-native.md) owns the
findings. Evidence:
[n3-transitions-v1](../../../../analysis/ableton-live-12.4.3/r2/n3-transitions-v1/manifest.json).

## Step 1: read what the register holds

These are the last instructions of the helper before the call (dossier n3-0001):

```text
0x101a4ac4c  ldr x8,[sp]          ; first word of a stack object
0x101a4ac50  ldr x8,[x8, #0x10]   ; third pointer of the table it points to
0x101a4ac54  mov x0,sp            ; the object itself is the first argument
0x101a4ac58  blr x8
```

This is how a C++ virtual call compiles: the object's first word points to a
table of function pointers (a *vtable*), and the call uses one entry. To resolve
it we need the value stored in the object's first word.

## Step 2: find who wrote the first word

The object lives at `sp`. Earlier in the helper, `mov x0,sp` is followed by
`bl 0x101ab7348`, so that function receives the object's address. Its pseudocode
in the corpus begins:

```c
*param_1 = &PTR_FUN_106756188;   /* first word := 0x106756188 */
```

A constructor that stores a constant address into the first word is setting the
vtable pointer. The constant is the vtable's *address point*, where slot 0 is.

**Why the index did not help.** The corpus `vtables` index lists only tables that
carry a symbol name, and Live keeps 80 of those. This one is unnamed, so tracing
the constructor was necessary.

## Step 3: read the table from the file

Live's arm64 slice stores rebased pointers as plain addresses, so a short
script can read words directly
([binary-reads.json](../../../../analysis/ableton-live-12.4.3/r2/n3-transitions-v1/binary-reads.json)):

| Address | Word | Meaning |
| --- | --- | --- |
| `0x106756180` (address point − 8) | `0x1067562d8` | Typeinfo record |
| typeinfo + 8 | → `18OSendThreadMessage` | Itanium-ABI class name: length 18, `OSendThreadMessage` |
| `0x106756188` + 0 | `0x101ab786c` | Destructor (the helper calls it last) |
| `0x106756188` + 8 | `0x101ab787c` | Deleting destructor |
| `0x106756188` + `0x10` | **`0x101ab7898`** | The target of `blr x8` |

The class name is part of the binary's own run-time type information, so it is
an observation, not a guess. `0x101ab7898` passes the message and two thread
identifiers to a queue function.

## Step 4: name the message with a donor build

Live does not export the engine's method names, but the shipped x86_64
`Ableton Live Engine` bundle does ([why](../../x86-only-bundles.md#consequence-for-analysis-a-named-copy-of-lives-engine-code)).
The helper's first constructor argument is the address `0x106f55ea8`. An
initialiser stores `{-1, "OSetPlayingCommand"}` there. The donor contains the
same string, used by a named function (donor pseudocode, simplified):

```c
/* OEngine::SendRequestForSetPlaying(AThreadManager::TId, bool, bool, bool) */
OSendThreadMessage::OSendThreadMessage(&msg, &DAT_017fb8a8 /* OSetPlayingCommand */, tid, 0x10100, 0);
msg << this; msg << b1; msg << b2; msg << b3;
(*msg.vtable[2])(&msg);            /* OSendThreadMessage::Finish */
```

The shape matches Live's helper call for call: one 8-byte append, three 1-byte
appends, slot `0x10`, then the destructor. In the donor, slot `0x10` of
`OSendThreadMessage` is named `Finish`. Matching the shape and the string makes
the name a **high-confidence inference**, not a symbol. The other matches and
their evidence are in the
[symbol-match table](../../../../analysis/ableton-live-12.4.3/r2/n3-transitions-v1/symbol-matches.tsv).

## Step 5: find the consumer through registration, not through calls

A queued message is not consumed by a call from the sender, so the call graph
alone will not show the receiver. The donor registers each message name with a
handler and member names, and Live does the same at `0x101a50bd4`:

```text
"OSetPlayingCommand" -> handler 0x101a524b8; members Engine, Playing, ByUser, AllowCountIn
```

That handler reads the four values and calls `0x101a4ac8c`, which sets the engine's
playing flag. When the flag changes, the engine sends another message,
`RootUnit.NotifyPlaying`, back toward the main thread. A further message,
`TransportEngineStateChanged`, finally updates the interface's Play state.

## What changed in the question

Before this step, the open question was "what state does Start write?" The
answer is that the Start and Stop bodies write no playing state themselves.
They post requests. The engine owns the state, and the interface mirrors it when
the engine reports. So the observable transition has two halves: the request
and the report. Their timing is a runtime property, which is why the transition
page ends with a targeted runtime question as well as a static table.

## Checks to keep

- Confirm each branch you rely on in disassembly. Here the dossiers confirmed
  that Stop's `ByUser` flag is passed through in `x2`, which the pseudocode had
  dropped from the call.
- Treat a donor name as evidence for a match, and state its confidence.
- A string scan through the shared dossier server took minutes per query on
  Live. The completed corpus `strings.jsonl` answers the same question offline.
- Nothing here was executed. Every result is a static derivation.
