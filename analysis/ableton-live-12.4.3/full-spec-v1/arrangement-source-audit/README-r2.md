# Arrangement audit R2: historical launch-action association

This preserved successor responds only to required **ASA-REVIEW-001** in the exact [R1 review](review-r1.json). It corrects the three CON-B032 assessment strings in [claim plan R2](claim-plan-r2.json) and [claims R2](claims-r2.json), ASA-C270–272. The [six field deltas](delta-r2.json) are the entire data change. [Response](response-r2.json) and [preservation ledger](preservation-r1.json) retain the precise selected source/case relation and original review.

Pinned historical Session SV-001 actually selects A by name and presses Enter, navigates to B with arrows, and separately clicks B's launch triangle. That action does not establish a deliberately nonsequential launch history. The retained Concepts source still permits launch at any time and in any order; the source text, source predicate, Session contract and all IDs/pointers remain unchanged. Later Session R3 SV-041 is not substituted or credited in this as-of audit. Existing selected launch-setting actions retain their scope.

All 31 R1 payloads, the [R1 manifest](manifest.json), source bytes, snapshots, proposals, counts, dispositions, original requirements/cases and original tools remain exact in place. No full archive was duplicated. R1's audit remains partial, with all target outcomes U/null/unexecuted and zero normative adoption or coverage/completion. Its [README](README.md) gives the full reading scope. This correction awaits separate focused review; it does not reopen full source or product approval.

Inspect [focused derivation](derive-r2.py) and [read-only checker](validate-r2.py) before running from the repository root:

```sh
python3 -B analysis/ableton-live-12.4.3/full-spec-v1/arrangement-source-audit/derive-r2.py --check
python3 -B analysis/ableton-live-12.4.3/full-spec-v1/arrangement-source-audit/validate-r2.py
```

Both commands read and print. The focused checker verifies all R1 hashes and existing50 input pins, reconstructs the corrected strings, checks exact six-field deltas, rejects old-overclaim/future-case/source/unrelated mutations and replays unchanged `derive.py --check`. The original exact-tree `validate.py` predates successor additions and remains historical; it is not invoked or rewritten. No old reports are rewritten. `derive-r2.py --write` refuses after the R2 seal exists. The R2 seal includes every preserved R1 file and all additions. No canonical, consumer, source or shared file changed; no application, vendor, native, hardware, network or candidate ran.
