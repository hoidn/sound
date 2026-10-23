# Utility kind-7 base return: focused R2 preparation

AS OF AUTHOR FREEZE: pending full Root preflight and separate actual selection. R1 and every historical preparation/actual packet remain unchanged in place. This successor resolves only `UTBASE-PREFLIGHT-001`; it does not claim the older independently verified actual decodes failed.

Exactly `[0x102312d04, 0x102312d24)` remains selected, with one `pdj 8` static-data decoder attempt into a new exclusive destination. The only collector differences are its destination literal and row predicate, recorded exactly in [response-r2.json](response-r2.json). Everything else reconstructs byte-exact R1. The plan retains R1 header/mapping metadata as-of; a future selected run freshly checks image/tool identity and header/mapping.

The predicate now rejects normalized invalid/ill types and absent, None, non-string, empty, invalid, ill or none opcodes after case/whitespace normalization. [Guard fixtures](guard-fixtures.json) reproduce the R1 counterexample and check valid controls plus targeted exclusions using only extracted AST expressions on synthetic data. No collector import/main, image-window read or decoder ran during authoring.

After full Root source inspection, only a separate selection may invoke `python3 -B extract-decode-once.py --extract-decode-selected-once <exact-manifest-sha256>`. Do not run the collector as a readiness check. Existing destination/manifest/bytecode/pin/mapping/row-byte/timeout/one-attempt/failure receipt guards remain exact. Filesystem failure or uncatchable termination can prevent complete final receipts; that limit is unchanged.

The question remains the native X0 carrier and receiver/store association for P versus Q. No R/P/Q/U equality, runtime identity, public Mute behavior, case or grade is adopted. All 38 Utility outcomes remain U/unexecuted.
