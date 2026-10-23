# Utility Mute model and routing context

Research-only D03 companion. This packet retains the bounded static model, bool-unit, graph-object and enrollment records selected by Root and Delay. It does not establish a public Mute gesture → identified runtime model → processor descriptor → processing endpoint join. All application outcomes remain unknown; zero requirements, cases, runtime passes or coverage credit are added. Independent review is pending.

## Retained evidence

`records.json` contains 29 unique complete decompiler records: Root's 23 selected bodies and Delay's eight enrollment bodies share two records. Their union contains 92,649 bytes of decompiler code text, not native instruction bytes. Each record retains its original JSONL path, one-based line, raw-line SHA (excluding its line terminator), code SHA, export state, warnings and partial flag. Five complete initial navigation alias rows retain equivalent exact source-line provenance; their presence does not imply that adjacent functions belong to a class or dispatch path.

The five literal pointer words total 40 bytes. `word_reads` retains the image SHA, file size, header, segment mapping, exact virtual address, slot, file offset, raw bytes and target. These are ordinary file reads from the retained arm64 image; no executable mapping or loader is used. The `OutText` storage word pointing to `0x106d91730` is not proof of a name/object identity, an initialized guard, or an actual runtime output. No additional strings-index record receives full-read credit; the earlier LegacyMode record output was truncated.

The generic factory `0x10319c4dc`, comparison helper and managed-wrapper helper are reused through three exact JSON pointers into the frozen A1 `records.json`; their bodies are not copied here. Factory bool selection requires earlier comparisons to fail and the bool comparison to succeed. Equality of the retained bool metadata addresses alone does not establish those preceding failures or an actual factory invocation. A1 remains unknown. No old checker, author script, import or historical replay is used.

`routing.json` has twelve scoped research observations, source snippets with exact code offsets, related selected-function and word-read indices, object-domain offsets and explicit unknown joins. This is not a normative behavior catalog. `D+0x350` is the model/device wrapper, and its supplied pointer at `D+0x358` is distinct from processor `P` in the earlier conditional mute-kernel trace. The supplied model virtual `+0x328` return controls the local RampOut/Out selection; it is not evidence of a current public Mute float. Constructor/View creation is not a UI gesture.

Processor registration independently retains the literal Mute and callback word resolving to `0x10216533c`. Observer enrollment and member eligibility/typed descriptors remain separate from that descriptor. Callback exclusions do not prove a particular Mute pointer was traversed or admitted. The bool bind export's jumptable/indirect-call warnings remain intact. Graph-object link helpers and private literal offsets do not establish processing, delivery, audio, clock, ABI, timing, lifecycle, Legacy or unmute behavior.

## Read and contribution scope

Root freshly read all 23 selected routing bodies and supplied their interpretation. Delay freshly read all eight enrollment bodies, including the full 34,155-byte enumeration body. Delay's exact notes and stated limitations are retained in `records.json/enrollment_contributor_notes`. The packager freshly read all 23 Root bodies, the five additional short Delay bodies, and selected context windows of the large enumeration body; its full semantic read is attributed to Delay rather than claimed independently here. The packager read the three reused provider bodies and all five complete alias rows, and verified every retained source line/code hash and five word bytes. Neither source selection contributor is the independent reviewer of these conclusions.

Original corpus export UTC is not established here (`null`); analyst packaging UTC is separate. Temporary extraction paths and their as-of digests are recorded in `inputs.json` for attribution, not required as future temporary-file dependencies. Original immutable JSONL parents, image and prior research providers are pinned. No mutable canonical identity is required. No application or original function was executed, imported, compiled or reconstructed for execution. No new export, decompiler/provider, installation, hardware or source capture occurred.

## Read-only check

After reading the checker, run from any directory:

```sh
python3 -B analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-mute-model-routing/check.py --check
```

The checker reads only pinned data, checks all selected JSONL lines and code hashes, the three provider pointers, exact image/header/segment/word mapping, snippets and finite offset/route/unknown-grade invariants. Eleven unsafe variants cover wrong pointer/slot, wrong object domain/offset, source association, premature factory selection and public grade/output promotion. It snapshots all packet and input hashes before checks and verifies them afterward. Unsupported arguments, including `--write` and `--seal`, refuse before packet reads. No checker writes reports or changes any frozen file. Its passing result is integrity evidence, not semantic approval or application proof.
