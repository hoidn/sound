# Keyboard source audit R2: association-role correction

R2 addresses required finding KNA-REVIEW-001 from the exact preserved `review-r1.json` (SHA256 `cdca5739615d9ccc8828ce9f9c8b680f9aec6248a320f986dc06f05ba210d829`). Independent focused re-review is pending. This is not normative owner adoption or a command/compatibility/completion result.

All20 R1 payloads and original manifest remain byte-identical in place, listed in r1-preservation.json. The formal R1 review is copied verbatim; its external source is also pinned. No full duplicate archive is needed. Original sources,292 shortcut discovery rows,641 claims,questions including Q052 source conflicts,23 proposals,old checks/reports and as-of snapshots are unchanged.

The successor `binding-reconciliation-r2.json` changes only three association fields in each of rows287–291 (five rows,15 field deltas in delta-r2.json). Rows287–289 no longer attach B350 as a toggle prerequisite; B350 remains adjacent explanatory context there. Rows290–291 retain B350's supported enabled Computer MIDI octave/velocity-use context. B351 remains general single-letter-plus-Shift related context for allfive, not a proved row-specific prerequisite or forced modifier. Empty prerequisite lists do not assert unconditional toggle dispatch, a Shift exception or a behavior law.

Allother287 discovery records are identical. Every discovery closure/dispatch flag remains false and actual oracle null/U. No source, raw-row hash, binding syntax, ID, count, proposal predicate or outcome was changed. No keyboard, reader, OS, original function, application, native, media, hardware, network, capture, install or candidate operation occurred.

Run only the current read-only checker:

```sh
python3 -B analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation-source-audit/validate-r2.py
```

It verifies all R1 bytes and the review, replays the inspected historical validator in memory with only its obsolete exact-tree assertion relaxed to allow successor additions, and independently seals/checks the full current tree. Original code/data stay unchanged; no frozen output is rewritten. It checks the exact15-field delta, qualified source pointers, ten invalid-association mutations and retained positive octave/velocity context. Original source/pin/span/oracle fixtures still replay. The original validate.py is historical and must not be run as-is against this enlarged directory.
