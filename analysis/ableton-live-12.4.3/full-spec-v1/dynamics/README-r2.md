# Dynamics owner revision 2: bounded control/history adoption

Partial analyst successor, pending independent ROOT semantic review. The author
independently reviewed the source audit and now authors this owner successor;
that earlier review is not selfapproval of this revision. No original/runtime,
UI, audio, hardware, source example, native function or candidate was executed.

The [approved full selected-source audit](../dynamics-source-audit/README.md) and
[review](../reviews/dynamics-source-audit-review.json) support 20 bounded groups.
The read covered all 123 selected blocks, 38 literal resources, 62 contract texts,
129 actual actions/fixture fields, full as-of research/preconditions and original
review. It does not cover all 1,137 Audio Effects chapter blocks, image pixels,
linked destinations, adjacent owners or algorithms. Version12/date2026-10-19,
UTC unknown; exact12.4.3 applicability remains U.

All **62 requirement IDs and bodies are unchanged** in [requirements.json](requirements.json).
The normative section of the current spec must be byte-identical to R1.
[Current cases](cases-r2.json) preserve all 129 old objects exactly and add 24
concrete compound/reset control histories: Compressor028–032, Gate025–028,
Glue026–029, Limiter025–028 and Multiband030–036 with full DYN prefixes.
There are 153 cases: 47 old D12 documentary, five old Dpkg file-only and 101 U.
All 24 new documentary expected/comparison pairs and all 153 actual pairs are null/U/unexecuted.
The 47 old documentary/five file assertions remain historical fields, not measurements.

[The explicit current-version overlay](fixtures-r2.json) references every case
without editing old objects or oracles. UI-only control/menu/edit observations
need admitted actual entrypoints, no audio/hardware. Signal absence/order/noeffect
requires independent genuinely NONEMPTY productive matched main input, effect,
route, nonzero relevant control/wet and nonmuted output. Detector work needs
productive normal AND trigger; Listen needs independent normal-output AND audition
positives and replaces normal output. BOTH relevant bands/channels need independent
productive contributions before loss/order/shared comparisons. Flags, meters and
nominal sample amplitudes are not calibration. Original N01/N02 remain open;
no rate-specific S2 interpretation, detector dB or generator rounding is chosen.

[Adoption](adoption-r2.json) assigns actual operations to all 20 groups without
claiming group completion. Optional ducking/gating/de-essing/uncompression remain
advice, not every-input effects or guaranteed sound/recovery. No generic lifecycle
cases duplicate 77 old U. CompressorRatio1 is no compression, GlueRange0 retains
Makeup/SoftClip, Amount0 retains gains/crossover; none implies full identity.
Glue oversampled peaks MAY exceed0dB; no mandatory overshoot or universalbound.
Link endpoints retain BOTH L/R and M/S contexts; no intermediate coupling law.
Lookahead labels/2x source factor are not measured delays or architecture.

[Inputs](inputs-r2.json) freeze 41 immutable/as-of pins, including all 27 old packet
files plus their original seal, source audit/review, parser and four inspected
Browser definitions. The 27 includes the seal; it is 26 payloads plus seal.
Existing [R1 spec](spec-r1.md) and [research](research-r1.md) are exact prior wiki
providers, reused without redundant archive. [Current spec](spec-r2.md) and
[research](research-r2.md) freeze the R2 wiki. Snapshot relative links use the
original wiki base. [Consumer census](consumers-asof-r2.json) records 15 exact
prior hash values in five unchanged files with JSON pointers and historical providers.
No cross-owner live hash gate, old tool, adapter or historical replay is added.

Inspect [check-r2.py](check-r2.py) before:

```sh
python3 -B analysis/ableton-live-12.4.3/full-spec-v1/dynamics/check-r2.py --check
```

This read-only checker hashes retained inputs, uses the pinned inspected pure
analyst HTML parser, AST-extracts only four inspected Browser functions, checks
normative byte preservation, old object equality, source references, meaningful
positive-baseline/null guards, 18 unsafe variants, links and untracked-aware
authored whitespace. Own packet is hashed first; input metadata enumerates
additional immutable providers, which are hashed before source parsing and watched
through completion. No writer, old validator/author, preset decode or installed
source read exists. Unsupported arguments refuse before input reading.

[Delta](delta-r2.json) and [preseal check output](validation-r2.json) are frozen
once. Only exact declared seal/validation artifacts may be pending in an explicitly
unsealed preflight. Postseal checks require both and emit stdout without rewriting
reports. The [R2 seal](manifest-author-r2.json) freezes all old/additive payloads.
Integrity and a reviewable packet grant no completion, coverage or compatibility.
