# Corpus A1 constructor instructions: failed first decode

This frozen packet preserves one inconclusive static-decoder attempt for exactly `0x1026e8e50..0x1026e8f6f` (288 bytes). The extractor verified the pinned Live.arm64 full hash/header and unique file-backed `__TEXT` mapping, then invoked the existing pinned Rizin with `-NN -n -x`, ARM64 little-endian, explicit virtual mapping and `pdj 72`. No original instructions, ESIL or emulator executed; no helpers, table words or other bodies were read. The synthetic RET control was not repeated.

Rizin exited zero but produced only 64 valid four-byte entries, followed by eight invalid entries and a length warning. The extractor correctly exited one at its complete-offset/size assertion. The failure beginning at byte 256 is consistent with a decoder buffer limit; this remains a diagnosis, not malformed-code evidence. No complete 72-instruction semantic read or normal-return identity conclusion is claimed. No retry ran. Root must separately select any corrected command.

The original raw data, full output/stderr, invocation and script are unchanged. `extractor-status.json` retains the completed extractor result. `failure-first-attempt.json` records the exact failed rows and limits. Its current 20-provider identities and the prior factory's full 16-file seal were checked; the interrupted extractor did not reach its final before/after-map save, so no durable initial map is claimed. Do not replay `extract-and-decode.py`: it is historical one-shot code and refuses this existing destination.

All application expectations, comparisons and grades remain null. A1 is unknown. No requirements, cases, compatibility credit or original-execution count changed.
