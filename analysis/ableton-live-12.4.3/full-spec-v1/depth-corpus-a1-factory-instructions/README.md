# Corpus A1 factory: exact instruction data

This source-only query decodes exactly the 100-byte factory at `0x1024f415c` through `0x1024f41bf`. The pinned Live.arm64 image, header and unique file-backed `__TEXT` mapping were verified before extraction. Rizin 0.9.1 decoded a synthetic RET control and then the 25 factory instructions once, using `-NN -n -x`, little-endian ARM64, an explicit virtual mapping and only `pdj`. No original instruction, ESIL, emulator, analysis pass, source function or provider executed.

The allocator result is passed directly to the constructor and saved for the outpointer store. The actual indirect-result carrier is entry X8, saved in X19. The vptr stores use constructor-returned X0. Equating that result with the allocation still relies on the retained constructor's normal-return source/ABI premise. See `findings.json` for exact addresses and limits. This narrows a construction edge; it does not identify a processing slot or current-cell consumer, prove A1, or add compatibility credit.

`extraction.json` records the image/tool/parent identities, complete selected raw words, mapping and invocations. The two raw tool outputs and stderr files are retained unchanged. Generated ESIL fields are output data only. `extract-and-decode.py` is historical one-shot extraction code and refuses an existing destination; do not replay it. The current `check.py --check` only reads this packet and verifies its finite byte/offset/branch/flow and integrity assertions. It never invokes Rizin or reads original image bytes.

No other code, data word or callee was selected. The previous C2 metadata STOP remains unchanged. New runtime expectations, comparisons and grades remain null; no requirements or cases were adopted.
