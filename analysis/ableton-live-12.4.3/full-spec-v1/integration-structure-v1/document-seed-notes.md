# Document-side seeds for the single T1 integration packet

Analyst: modulation_finish. Packet1a's approved manifest is SHA256 `392a738005f7d776dca96d7c78220cb94091081ef7086ec45b9397afccbe438b`. Its atlas and README retain pre-review freeze wording; the separate independent review is the approval evidence. My earlier symbol-layer authorship is a dependency, not independent approval of it. All addresses below refer to main Live arm64, image SHA256 `3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad`.

This contribution concerns document load, Live Set object data, save/reopen and export/delivery. It does not enlarge implementation T1, grade a case, or treat a static call chain as runtime sequence. Reopening is initially a scenario connection back to the load entry, not a proven save→reopen native edge. Actual graph traversal waits for Root's shared helper and reviewed per-level frontiers.

## Seed roles and exact provenance

The seed JSON has only `entries` and `sinks` arrays of addresses. A sink is a backward-search landmark; it need not be a terminal function. Command initialization and backend landmarks remain distinguished from an invoked user command.

| Address | Search role | Evidence and confidence |
| --- | --- | --- |
| `0x101854f54` | User-document load entry | Retained T11 `traces/a1a2/trace.txt`, lines under “A1: open path”; `vtable-owners.txt` records app address point `0x10659ad00`, slot `+0x730`, exact stored function. Canonical Live Set structure carries the remaining menu/OS-event route inference. No current UI invocation proved. |
| `0x1002e6e00` | ALiveApp document-type load branch | Same trace: app `+0x840`; `.abl`/`.ablbundle` type-mask `0x3000` imports, other files go to `0x1018536d4`. Conditional on actual app receiver/type, not a generic “every document” law. |
| `0x1018536d4` | File stream→general document reader | Fresh complete retained N2 body `results/n2-0003/functions/0x1018536d4.c`: stream vcall setup, log “Loading document ”, actual direct call `FUN_10148389c(&local_38,local_40,local_60,&local_48)`, Creator handling, then `FUN_10153f480(param_1,&local_50)`. Full receiver/state and omitted ABI arguments remain unproved. |
| `0x101485c50` | Generic compound-format save dispatcher | Fresh complete N2 body `results/n2-0005/functions/0x101485c50.c`: format0→`101484980`, formats1–3→`101484e7c`, format4→`101485240`. Its known direct callers are preference savers; **not yet the Live Set save command**. |
| `0x101741430` | Command-code/name initialization landmark | Fresh full16,174-byte C, exact original chunk00918 line96/byte161795, retained in `document-source-rows.jsonl`. Contains `FUN_101742fa0(0x73617665,"Save")`, `...0x73616173,"SaveAs"`, `...0x7361636f,"SaveCopy"`, `...0x7365636f,"SaveSelfContained"`, `...0x72746f64,"RenderToDisk"`, and `...0x65736d63,"ExportMIDIClip"`. **Only literal identifier/name registration is observed**; no handler binding or export invocation is shown by those calls. |
| `0x101486fe4` | Parsed root→object load landmark | T11 open-path trace and N1 canonical reader: create root, invoke root `+0xc8`/`+0x140`, conditional post-load `+0xd0`, then walk `101487198`. Ownership of generic loading is supported; actual dynamic class/ABI needs separate dispatch evidence. |
| `0x102695f78` | Song-level post-load validation landmark | T11 trace identifies `LSong::AfterRead_Virtual` as ASong root post-load. Track counts, pointees and repairs belong to canonical Live Set structure; no new rereview of all those laws in seed selection. |
| `0x101487198` | Member/object validation walk landmark | T11 trace: member recursion and object `+0x100` tail dispatch, with retained x86 disassembly support qualified in that trace. This is not an audio-engine handoff. |
| `0x101485240` | Compound→XML envelope writer | Fresh complete retained N2 body `results/n2-0002/functions/0x101485240.c`: stream compression setup, class virtual calls, declaration/root/version attributes, body `(*param_1+0x138)` and flush. Canonical “Writing on save” distinguishes concrete body from unknown Live Set save callsite/level/format. |
| `0x1014339e4` | Compression/output flush landmark | Direct call near end of the complete writer body; N2 canonical identifies flush/deflate-vs-direct-stream path. No bytes-on-disk, atomicity, close, file replacement or durable-save claim. |
| `0x104f8502c` | Named movie-export backend run landmark | Fresh full1,797-byte C, chunk03703 line62/byte89286, retained in `document-source-rows.jsonl`; alias row370362/byte110123247 names `TAVFoundationMovieExporter::run`. Flag `param_1+0x5c` bit0 gates logging “Starting video export...”, ObjC stub calls and two stack-block callback values `104f85174`/`104f851f0`. **Video backend nomination only**: does not join `RenderToDisk`, audio rendering, mixer buffers, files or public UI settings. |

Original source-file bytes, hashes, metadata and selected raw-row/code identities are in `document-providers.json` and `document-source-rows.jsonl`. Later graph rows must add their own index line/byte/call-PC evidence; this table is not substituted for graph evidence.

## State crossing the candidate boundaries

1. **External file→container/parser:** path/stream handle, leading bytes, parsed root/class and Creator/version information. N2 separates gzip, XML and other dispatch; byte-format recognition is not proof of sample/codec or engine readiness.
2. **Parsed tree→Live Set object graph:** context flag `+0x2c`, schema/class/member descriptors, factories, root/member hooks and validation walk. Track/device/clip/sample-reference/pointee data belong to Live Set structure. A valid serialized graph does not establish engine ownership, audio callback registration or ready-to-play state.
3. **Modified graph→serialized output:** document-class version flag, save format, compression argument, writer context and body virtual dispatch. The public Save/SaveAs command→song writer connection is open; do not join it by a matching save label or a generic writer's preference callers.
4. **Saved document→reopen:** scenario intent routes a later file back to load. Same-path resolution, successful replacement, generated bytes, dirty state and runtime save/open ordering are not established by generic reader/writer existence.
5. **Render/export command→rendering/delivery:** command token `0x72746f64` is grounded; execution dispatch, export-range state, track selection, mixer/device buffers, offline-vs-realtime coordination, encoder and file lifecycle remain unjoined. The retained manual supplies documentary option descriptions with exact12.4.3 applicability unknown. Movie backend existence does not fill the audio side.

## Immediate unknown frontiers

- Actual command handler/receiver for Save/SaveAs/SaveCopy and RenderToDisk, rather than the name initializer.
- Generic reader object publication (`10153f480`)→active application/song/engine state, including any callback registration and synchronization; source/class matches do not establish live ownership.
- Loaded tracks/clips/device-chain data→runtime playback/mix/device graph, a boundary shared with the other contributors.
- Song save caller→format/compression choice→actual file writer and replacement/durability/error/cancellation effects.
- Mixer/render buffers→audio export backend/codec/file writer, and the relationship of movie export to that pipeline.

No unknown indirect site will be treated as a dead end. Bodies and static fields can support conditional local edges; absent target references and hub pruning cannot prove absence of a route. Root's common trace bounds, frontier reviews and shared cross-component synthesis will govern any expansion.
