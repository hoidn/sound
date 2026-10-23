# Automation M: two-point Mach-O/linker metadata

Author packet only. Root sealing and an independent whole metadata review are
pending. This author does not independently approve the packet.

The concrete Root selection is copied exactly in `selection-root.json`:
3287B SHA`eab887f6e30884451b7ec63ca50948ca5a492246a4599a56b38d511e4a6e41ae`.
It selected only strict header/LC_FUNCTION_STARTS metadata for M at
x86`0x1011f2080` and ARM`0x1012132d8`, following five separately retained local
boundary discrepancies. This packet does not recompare results or repair an
oracle. Posthoc arithmetic regrouping and those discrepancies establish no
native operation order or cause here.

The new270line source was read fully before24 synthetic/document-only controls
passed. One exclusive batch then opened each exact selected image once and
hashed each copied byte snapshot once. Both whole-image identities and sameFD
before/after metadata matched. No images are retained, reopened or decoded.
No old collector/main was imported or run. The existing strict parser was
adapted only as inert source. Do not rerun `--acquire-once` or the pre-acquisition
`--check`: the exclusive `acquisition-attempt.json` marker forbids reuse.

Both selected points are exact linker-declared starts in file-backed
`__TEXT.__text`. Current/previous/next rawULEB locator metadata is retained:

| Architecture | Previous declared start | Selected/current | Next declared start | Distance to next (metadata only) |
| --- | --- | --- | --- | --- |
| x86_64 | `0x1011f2060` | `0x1011f2080` | `0x1011f22d0` | 592B |
| arm64 | `0x1012132c4` | `0x1012132d8` | `0x1012134c0` | 488B |

These are not proven function bodies, code extents or permission to read code.
The412317/413794 complete declared-start counts are metadata counts, not a
complete/discovered-function inventory or behavioral denominator. Every delta
is mechanically checked, including canonical unsignedLEB, overflow, zero
sentinel/trailing padding, executable section mapping and architecture
alignment. x86 starts are not forced to ARM's4-byte alignment.

The only binary payloads are retained header/load-command metadata
(6864B x86,6976B ARM) and bounded LC tables(559744B x86,560280B ARM).
Their combined1133864B is metadata, not native instruction windows. The
per-image limits remain64KiB header/commands,256commands,32segments,
256sections,4MiB LCtable and1000000start entries. No adjacent native target,
caller, callee, alias, C source, global, provider or runtime object was followed.

After reading the entire source, the repeatable retained-data check is:

```sh
/usr/bin/python3 -I -B analysis/ableton-live-12.4.3/full-spec-v1/depth-automation-M-native-metadata-v1/metadata-once.py --check-retained
```

It reads this packet and3immutable document pins, reparses both saved complete
LC tables, verifies every selected locator/header/receipt join and opens no
original image. Its observed result is `retained-check.json`; the earlier
synthetic result is `author-check.json`. Source and payload identities are
locked in `inventory-author.json` for Root's final manifest/review routing.

No decoder, original/model/harness execution, build/install or numerical
formula evaluation occurred. No native cause, operation order, ABI, callable
body, ready-X status, requirement/case/grade/site/release or coverage closure
is established. Unsupported behavior staysU, coverage staysOPEN. No shared
wiki or prior immutable packet was changed and no successor is selected.
