---
id: SRC-APPLE-MACHO-FORMAT
type: source
status: partial
updated: 2026-10-21
access: analysis
---

# Apple Mach-O metadata and classic dyld sources

Apple's public XNU repository at commit
`f6217f891ac0bb64f3d375211650a4c1ff8ca1ea` is the retained format source. Ordinary
HTTPS captured both files with200responses at13:51:28–29UTC. The [source packet](../../../analysis/ableton-live-12.4.3/full-spec-v1/depth-apple-macho-format-source/manifest.json)
preserves source bytes, commit-resolution response and receipt identities.

| File | Exact source | Retained identity | Selected locations |
| --- | --- | --- | --- |
| loader.h | [Apple commit source](https://github.com/apple-oss-distributions/xnu/blob/f6217f891ac0bb64f3d375211650a4c1ff8ca1ea/EXTERNAL_HEADERS/mach-o/loader.h) |71322B/SHA8780a1e622375833b563f488bc820422c2fb5b8727bb8df8ceaa73ab6f0f88e3 |449–499(section64/stub rules),917–991(dynamic-symbol fields),1037–1041(indirect special bits) |
| nlist.h | [Apple commit source](https://github.com/apple-oss-distributions/xnu/blob/f6217f891ac0bb64f3d375211650a4c1ff8ca1ea/EXTERNAL_HEADERS/mach-o/nlist.h) |13793B/SHA9e1a328c1a9632fae48d4d95b09d377f5007374ddb8addad97e0841052304c96 |92–132(symbol layout/type bits),210–242(library ordinals) |

The declarations explain how a stub's position and section metadata locate an
indirect-table entry and then a symbol-table record. The symbol's string index
locates its name. Special indirect entries require separate handling. The high
byte of the symbol description identifies a library ordinal for ordinary
undefined references in an image declaring the corresponding namespace mode.
These are format rules, not evidence that a current process binds a selected
stub, calls the named function, receives valid arguments or obtains its result.

The selected reading above is limited; neither complete header nor the large
commit-response diff is claimed semantically read. Full bytes are retained for
identity/versioning. No header was compiled or installed. A browser attempt at
an unverified cctools tag returned cache misses; no content or version claim was
adopted from that attempt. The subsequent Apple XNU source is pinned explicitly.

The initial use was analyst-only Corpus call-target metadata navigation. The current
headers do not establish which headers built Live12.4.3 or a library's runtime
implementation. Exact bundle/slice/header/section/indirect/nlist/string mappings
must be checked independently for each selected image and address. No device
behavior, allocation contract, ABI or compatibility outcome follows alone.


## Selected DeviceKit declaration reading — 2026-10-20

Root additionally read pinned `nlist.h` lines 88–165 and 235–295 for the
[selected consumer records](../program-structure.md#selected-devicekit-symbol-acquisition--2026-10-20).
The selected type masks and defined-symbol weak bit distinguish a section-defined
weak declaration from an undefined import. Section ordinals refer to each file's
own load-command order. This extends format navigation to the main consumer;
no current loader resolution, executable body, ABI or public behavior follows.
No source bytes or frozen manifests were changed.


## Classic dyld declaration reading — 2026-10-21

The [Electric owned-site study](../device-electric-dsp.md#electric-encoded-site-association-adoption--2026-10-21) additionally reads retained loader.h lines1295–1374 and1405–1457: compressed stream tuples, weak/lazy context, classic pointer types and opcodes. The selected excerpts are retained in its frozen packet. They extend the earlier limited declaration reading; they do not supply Apple's arithmetic, validity checks, default state or runtime loader implementation. Those questions belong to the separately selected primary dyld source study. No header was compiled, installed or changed.


## Primary classic dyld implementation — 2026-10-21

The [primary-source packet](../../../analysis/ableton-live-12.4.3/full-spec-v1/depth-apple-dyld-classic-authority-v1/manifest.json),4,162-byte manifest/SHA-256 `c4453388308094229bc23d541ece98142eae28c58074f0deeebfdf447372ef2e`, passed [Root's sole independent review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/apple-dyld-classic-authority-v1-review.json),2,999 bytes/SHA-256 `bdd01ef1a4a5f7a0998569156c79da7b17d47e1ef710b1eec2bdcc958328c844`. Twenty payloads/685,216 bytes and21 files are read-only. Nine HTTP200 receipts retain the official Apple repository's annotated unsigned dyld-852.2 tag resolution to commit `3f24a36068a96722cf3acbd5087983ce658e9d70` and seven source files/576,387 bytes. The tag/commit chain and exact commit-specific URLs were independently checked; this is published source custody, without signature or running-loader authentication.

The [lossless projection](../../../analysis/ableton-live-12.4.3/full-spec-v1/depth-apple-dyld-classic-authority-v1/selected-functions.txt) and [range map](../../../analysis/ableton-live-12.4.3/full-spec-v1/depth-apple-dyld-classic-authority-v1/selected-source-map.json) identify17 complete-function/type-context ranges,1,283 lines/59,396 source bytes. All selected ranges and eleven claims were read; full-file semantic reading is not claimed. The source-only checker and five projection/custody negative controls pass. No Apple source was compiled or executed, and no original image or old stream suffix was interpreted by this source study.

Observed source statements in [MachOAnalyzer::forEachBind and validBindInfo/invalidBindState](https://github.com/apple-oss-distributions/dyld/blob/3f24a36068a96722cf3acbd5087983ce658e9d70/dyld3/MachOAnalyzer.cpp#L1793-L2198) keep ordinary/weak segment offsets in uint64_t and use addition for ADD_ADDR_ULEB and DO_BIND_ADD_ADDR_ULEB. Modulo2^64 behavior is a language-level inference from those unsigned types/operators. The emission callback separately checks segment/state/symbol/ordinal/type/permissions; the handler precedes the latter operation's address advance. The legacy [eachBind implementation](https://github.com/apple-oss-distributions/dyld/blob/3f24a36068a96722cf3acbd5087983ce658e9d70/src/ImageLoaderMachOCompressed.cpp#L1236-L1450) uses uintptr_t actual addresses with different validity checks. Neither path proves blanket acceptance of wrapped values. Prerequisite format checks were not traced completely; a safe data method must explicitly require vmsize≥8 before full-width subtraction and retain strict geometry and operand bounds.

Ordinary analyzer type starts0; weak starts POINTER/WEAK_LOOKUP and rejects ordinal-setting opcodes, recording strong-definition symbols separately. Whole lazy scanning starts POINTER/addend0 and persists state through DONE. Analyzer, legacy whole-lazy and individual fast-entry parsers accept different opcode subsets; they cannot be merged into a universal reset or acceptance rule. [The conditional weak updater](https://github.com/apple-oss-distributions/dyld/blob/3f24a36068a96722cf3acbd5087983ce658e9d70/src/ImageLoaderMachOCompressed.cpp#L1793-L1886) can invoke bindLocation, whose pointer update depends on caller-supplied coalesced value, addend and image state. An encoded site is not proof of a runtime replacement or winning provider.

These findings support a separately selected guarded data-method revision for the researched ordinary/weak state advances. They do not revise the frozen strict Electric result. Exact Live host/dyld version, build switches, loading prerequisites, slide, actual mappings/providers/coalescing, current class/ABI/public targets and whole-product behavior remain unknown. No behavioral case, grade, release or main-image site is added. The [current checkpoint](../full-live-specification-plan.md#current-execution-checkpoint) owns the separately selected method revision and its bounds.
