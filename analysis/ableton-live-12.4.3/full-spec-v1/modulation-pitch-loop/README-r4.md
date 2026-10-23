# Modulation owner R4: pointer-only correction

AS-OF AUTHOR FREEZE: independent owner review pending. Shared indexes carry current disposition. Root review must assess the 22 R3 histories as well as this effective correction; the author does not approve either owner revision.

The sealed [R3 packet](manifest-author-r3.json) has a self-detected navigation defect: its overlay and adoption ledger used `/cases/i`, although [the case catalog](cases-r3.json) is a top-level list. Its passing checker compared the same invented prefix instead of dereferencing the list. That sealed check was inadequate for pointer identity. All 118 R3 files remain exact, and no R3 check is rerun against current canonicals.

Only 230 metadata fields change: the [208 overlay pointers](actual-overlay-r4.json) and [22 adoption pointers](adoption-r4.json) now use `/i`. [The correction record](pointer-correction-r4.json) records the failure/refusal chronology; [the exact page delta](delta-r4.json) only updates metadata routes and adds the qualification. All 208 case objects, 186 original objects, 106 requirements/bodies, source references, actions, prerequisites and documentary/actual oracles remain unchanged. Current cases still live in `cases-r3.json`; it is not duplicated. All new documentary/actual outcomes stay null/U/unexecuted; no completion or runtime claim is added.

Run the [current read-only checker](check-r4.py):

```sh
python3 -B check-r4.py --check
```

It verifies every preserved R3 payload plus seal and 130 immutable original inputs, the exact 230-field-only difference, current [spec](spec-r4.md)/[research](research-r4.md) delta, all 106 browser IDs and all nulls. Crucially it **actually dereferences** every overlay/adoption pointer against the top-level list and checks the referenced case ID. Eight independent reference mutations reject a jointly restored `/cases/i` prefix, wrong valid index, missing/duplicate references and out-of-range values. Twenty substantive unsafe case/source/null variants also remain rejected by the retained pure guard function.

Only the fully inspected, hash-pinned R3 analyst `guards` definition is selectively compiled, with its two literal pointer-format checks corrected. R3 imports, assignments and main are not compiled or run. The current checker independently validates the actual JSON references rather than trusting those formats. There is no old main/tool replay, parser, source recapture, archive/preset decode, original/vendor/native/UI/audio/MIDI/hardware/network/install or candidate action. Unsupported arguments refuse before input reads; independent before/after watch, whitespace and seal refusal accompany freeze.

[The current seal](manifest-author-r4.json) includes all 118 preserved R3 files and eight additions: 126 payloads plus seal. Old consumers/providers remain as-of, unchanged; no automatic replay/adapter is added. R3's source-action scope and pending subsets remain exactly bounded as documented in [the historical author readme](README-r3.md). This metadata correction is not a behavioral or compatibility approval.
