# Corpus x86 CalcA entry-window preparation

This is preparation only. No instruction window has been extracted and no decoder,
original function, observer, model, or numerical analysis has run in this packet.
Root must review the complete code and the independent export-metadata review
before separately selecting any actual attempt. The metadata review was pending
at author preparation. Before seal, the exact metadata review was approved
and pinned in inputs.json. This is not an execution approval.

The fixed physical range is `[0x29c0,0x2ab0)` in the pinned x86_64 slice. Fresh
fat/header/load-command metadata maps it uniquely to bundle offset27072, with
slice offset16384. It is an entry context selected by Root, not a function extent
inferred from neighboring linker starts. No branch target or callee is selected.

The future command uses the pinned existing Rizin with no initialization, raw
input, no execute permission, file-sized block, x86/64 little endian, mapped at
0x29c0, and exactly `pdj 16`. Sixteen instructions of at most15bytes fit the
selected240bytes. Successful validation requires exactly16 valid normalized rows,
each with integer size1..15, cumulative offsets and row-byte length equal to its
declared size. Their concatenated bytes must match exactly the consumed prefix
of the240-byte input. Remaining selected bytes are explicitly uninterpreted.
Neither a decoded prefix nor an unused suffix establishes whole-body coverage.

`collect-once.py` is retained as data until a separate selection. It creates an
exclusive destination, retains before-map and attempt receipt before the single
Popen, distinguishes an attempted spawn from a returned PID, limits the child to
30seconds/core0 and retains stdout/stderr/status/after-map on ordinary failures,
including validation and timeout. It never retries. Pre-try destination setup and
catastrophic receipt I/O failures require the coordinator's outer receipts;
blanket failure retention is not claimed. The future extraction and decoder
analyze bytes as data and do not execute original instructions.

`delta.json` reverses the literal collector changes to the previously inspected
fixed ARM64 preparation. Only the destination/image/range, fat/slice mapping,
x86 command and variable-length prefix validation change. All26 parent
preparation files are pinned unchanged; there is no duplicate archive or old-tool
replay. Source metadata, the state-readout design, readiness review, original006
fixture and tool identity are pinned as immutable/as-of inputs.

Inspect `check.py`, then use `python3 -B check.py --check`. It performs stdlib
identity/header/LC and AST checks plus synthetic prefixes. It compiles only the
fully inspected pure new `validate_prefix` definition; it never imports or runs
the collector's main. Valid short/full/variable prefixes and malformed row sizes,
row-byte boundaries, counts, gaps, invalid types/opcodes and prefix mismatches
are covered. It reads no selected instruction window and refuses other options.

This packet supplies no internal state, processor/slot identity, arm64-to-x86
correspondence, native pole, audible-component measurement or compatibility
grade. Existing captures and all unknown modal observations remain unchanged.
