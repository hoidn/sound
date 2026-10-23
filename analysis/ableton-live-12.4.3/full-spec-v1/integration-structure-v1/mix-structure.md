# Playback, track output and Arrangement recording boundaries

This is the mix-owned part of integration packet 1b. It records retained ARM64 source structure and bounded call-index frontiers. It does not establish runtime scheduling, host-buffer delivery, native recording transactions or a complete playback chain. The broader recording scenario does not expand the restricted T1 implementation scope. No original, provider, harness, decoder or audio computation ran in this work; only the shared read-only index tracer ran.

The seeds are in `mix-seeds.json`; their original nomination and as-of canonical identities are in `mix-seed-explanation.json`. Those identities describe author-time context, not future mutable-wiki gates. Its NOT_STARTED/metadata-only statements remain historical: the later traversal and complete builder reading are recorded here and in the separate source/frontier files. Approved component packet 1a is carried at manifest SHA256 `392a738005f7d776dca96d7c78220cb94091081ef7086ec45b9397afccbe438b`; my class recovery authorship is disclosed. Its class inventory is not reapproved here and supplies no automatic receiver identity.

## Components and local ownership

| Boundary / owner | Exact source anchor | Retained evidence and limit |
| --- | --- | --- |
| Playback event scheduler | `0x101ab5cec` | Full projected list/countdown handling and due-event virtual `+0x10` dispatch; actual event receiver classes and audio-callback reachability remain unknown. |
| Solo control propagation / Mix graph | `0x102719f88` | Full local selection/bitset/state processing with calls to `10272cd14` and `10272d398`; solo semantic classification comes from T14. Warnings and computed-jump targets remain unresolved. |
| Track-output unit construction / Mix graph | `0x102731438` | Full 2,019-line projection registers named control/input/output nodes, twelve send groups and their wiring helper calls. This is graph construction, not an identified per-sample execution entry. |
| Main/meter per-sample processor wrapper | `0x101b1c114` | Named `OTrackOutProcessor::CalcStereo<1,0>` wrapper reads referenced float inputs, advances local matrix state and writes output fields. Runtime wrapper dispatch, reached object identity and downstream host buffer are unknown. |
| Send accumulation wrapper | `0x101b1afbc` | Named `CalcStereo<0,1>` wrapper reads referenced inputs and accumulates into referenced destinations. Concrete bus/return ownership and global summation order remain unknown. |
| Recording / Arrangement | Recording003/026/031; Arrangement020/021 | Manual/source contracts distinguish newly recorded input/media from recording Session launches/property changes into Arrangement. Existing command/string inventories nominate navigation only; no native writer or transition is identified in this source set. |

The retained builder projection initializes many `param_1` slots, then returns `param_1` (line2017). Its earlier `puVar25 = FUN_102348a34()` and vptr store (96–97) are a distinct projected expression: this work does not equate that allocation with `param_1` or infer a class from the stored address point. Helper signatures in exporter metadata sometimes omit arguments present in C; source/ABI correspondence remains a premise.

## Source-grounded structural edges

`mix-builder-source.json` retains the exact full row, source byte locator, code hash and all nine unreachable-block warnings. The following are observed helper-call arguments in that projection; treating them as unit-port connections carries T14's recovered helper interpretation, rather than newly proving every helper receiver's runtime class.

| Edge / carried state | Exact builder lines | Qualification |
| --- | --- | --- |
| Speaker and SoloPrehear controls → Switches → Split → MainOn / SendsOn / PrehearOn ramps | 1683–1698; nodes1284–1308 | Control graph wiring; no callback order or numeric ramp duration. |
| PanMode → PanModeRamp → Volumes.PanModeAmount; Pan and split-pan controls → Volumes | 1712–1724 | Named fields and helper arguments, not a pan algorithm or public UI-to-object binding. |
| Group 2×2 controls / GroupOn ramps and transaction plus Volume → Volumes | 1725–1750 | Explicit group/transaction route; actual synchronization and update atomicity unknown. |
| PrePostState → Split → twelve IsPost ramps → Volumes.SendIsPost[k], Send[k] controls → Volumes | 1751–1814; loop bounds1340/1477/1770/1814 | Twelve construction iterations in this source, not a global maximum or all Live track variants. |
| Volumes main/meter/send matrix ports → TrackOut | 1815–1891 | Named 2×2 wiring roles, not independently executed coefficients or summation precision. |
| Unit input fields `+0x168/+0x170` (InL/R) → TrackOut (`+0x428`) | 1482–1489,1898–1903 | This closes only the unit-local input-to-processor construction edge. Which instantiated device-chain outputs supply these unit inputs is not established. |
| TrackOut outputs → unit OutL/R, routing gates, prehear buffers, twelve send buffers, meters | 1907–2016 | Local construction arguments. Host/device/export buffers, instantiated return buses and recording file delivery remain unknown. |

Four small helpers are retained in `mix-wiring-helper-sources.json` (3,475 C bytes). `102321f5c` searches a receiver's input entries (`+0x40`, count`+0x52`) by stored name token before calling `102312ed0`; `102321e6c` additionally gets `**(source+0x48)`; `102322044` searches output entries (`+0x48`, count`+0x56`). A failed search forwards zero, so successful lookup/valid objects are required premises. No string-equality or lifetime mechanism is invented beyond the shown token comparison and normalization calls.

`mix-connection-core-source.json` retains the full 10,885-C-byte `102312604` projection. `102312ed0(a,b,c,d)` calls it as `(b,a,c,d,1)`. The core obtains endpoint representations through virtual `+0x50/+0x58` or collection fallbacks, then (when fifth argument is nonzero) invokes each endpoint's current virtual `+0x40` with the opposite representation and combined selector/flag bytes. Thus the local wiring path reaches endpoint registration calls; the target method identities and the final storage/processing consequences are unknown. The zero-fifth-argument branch instead uses `+0x48`; it is not selected by this wrapper. No arbitrary class-table slot is attached to those calls.

## Call-index exploration and omissions

The first depth1 attempt stopped with `KeyError: implementation_targets` before writing graph output. `mix-trace-depth1-failure.json` preserves it. Root corrected only the shared consumer to the approved singular `target` schema; component packet1a stayed unchanged. The successful helper SHA256 is `d1fa658bc2e74449034348b34c79eead0e8487f04f118282dd44d8e6a4dc7c24`; hubs are `b465a06baa50b083a41493a5abc947c798a8ff7703814906d4291fad4970aae9`.

Each wave was reviewed before the next depth. Results and separate review notes remain in `mix-trace-depth{1,2,3}.json` and `mix-frontier-depth{1,2,3}-review.json`.

| Wave | Retained forward rows | New forward nodes | Hub-pruned rows | Edge/node-budget omissions | Backward rows / intersections |
| --- | ---: | ---: | ---: | --- | --- |
| 1 | 97 | 20 | 501 | 0 / 0 | 0 / 0 |
| 2 | 18 | 10 | 42 | 0 / 0 | 0 / 0 |
| 3 | 9 | 9 | 56 | 0 / 0 | 0 / 0 |

The top1,000 incoming-row hub policy prunes real wiring helpers such as `102321f5c`, `102321e6c`, `102322044`; those references remain retained and were partly read manually above. The traversal is not a semantic slice, and common helpers are not components merely because they survive pruning. Fifteen unresolved indirect rows are recorded for functions considered through the third expansion; the final nine frontier functions are not expanded, so this is not their full indirect census. Zero backward rows into function-pointer wrappers cannot prove that they are unreachable. No conditional OSendThreadMessage overlay row applies to these seeds; its 24 receiver proofs cannot transfer to TrackOut.

## Explicit remaining integration gaps

1. **Control/audio entry:** exact host audio callback → playback scheduler / processor dispatch. Retained donor Engine `CalcAudio` and Mainx86 correspondence are navigation context; no ARM callback address or cross-image offset is guessed.
2. **Device chain:** instantiated clip/instrument output → actual chain → selected unit InL/R. The unit-local port wiring above is narrower than that whole chain.
3. **Execution:** constructed TrackOut node → reached processor-wrapper receiver and main/send destination ownership. The next evidence must bind the concrete receiver and dispatch slot/site, not merely match a class name.
4. **Main delivery:** track outputs / return accumulation → main bus → export or device callback, with actual scheduling and summation ownership. T14 explicitly leaves this broader path open.
5. **Recording:** eligible recording state and launched/input events → native Arrangement materialization and, separately, new audio/MIDI media writer. Registry vocabulary and demo container positions do not prove transitions, timestamps, saved output or undo transaction boundaries.

Recording031's Session-performance path captures launched clips/property changes and eligible automation/scene tempo/meter, while newly recorded input/media belongs to separate003/026 contexts. This distinction is a source contract boundary, not proof of two native code paths. A string hit such as CaptureMidi or PunchIn is not a writer sink.

Fresh full C scope is ten functions / 103,736 bytes: builder74,662; scheduler5,723; solo4,391; wrappers2,508+2,092; four small wiring helpers3,475; connection core10,885. Other T14/research/manual facts are explicitly carried or selected documentary context, not freshly reapproved whole chapters. No runtime routes, new behavioral clauses/cases, completeness credit, candidate outcomes or grades are claimed. Shared packet seal, atlas, cross-owner reconciliation and independent review remain Root-owned.
