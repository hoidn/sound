# Wavetable exact eight-type x86 metadata

Author-locked metadata result; Root manifest and independent review pending.
This packet is not independently approved by its author.

Root explicitly selected one bounded metadata acquisition in
`selection-root.json`, whose original5856B SHA is
`69a810c15eabcbfff67bb813cd9e63d199cf29cdc58191d1cd768334bcb7b1a0`.
The collector was read completely before23 synthetic/document-only negative
controls passed, then opened the pinned x86 image exactly once. Its whole-image
163716848B SHA and same-descriptor metadata agree with the selection. The
exclusive `acquisition-attempt.json` marker forbids reuse. Do not rerun the
collector or its pre-acquisition `--check` now.

The complete eight-name union is retained. Seven exact NUL-bounded names were
found in file-backed `__TEXT`; each has one aligned DATA name-pointer join,
one candidate typeinfo head and one offset-zero candidate table header. The
first selected Phasor/Direction0/Interpolation1 literal has no match in that
bounded exact search. This is a locator gap, not absence of an implementation,
an invitation to fuzzy-search another spelling, or a cross-architecture law.
Zero here means only the selected **preceding-NUL and trailing-NUL** predicate.
The collector did not enumerate exact trailing-NUL occurrences whose preceding
byte is nonNUL. Their presence/count is unknown, not zero. Root suggested
linker suffix sharing as a possible explanation; this remains a hypothesis,
not an observed suffix match or authorization for another acquisition/search.

The result is `REFUSED-U`: the whole-eight join gate refused **every** six-slot
prefix. Zero slots and zero target instruction bytes were materialized; the
seven matches are not substituted for the selected eight. `metadata.json`
contains all bounded candidate joins and21exact selected raw metadata spans,
plus complete parsed header/segment/section records. `header-loadcommands.bin`
contains6864metadata bytes. Selected metadata retention totals45254B, below
the1MiB cap. No full image/DATA dump is retained.

Allseven raw typeinfo vptr words are `0x10`, explicitly unresolved. Exact
name/header joins do not prove loaded RTTI, provider binding, legal receiver,
complete table/class/function or behavior. The optional LC_FUNCTION_STARTS
payload was not parsed after the whole-set refusal; only its load-command
location/extent is recorded. No next-start interval/body claim is made.

Two aligned qword passes scan only file-backed `__DATA`/`__DATA_CONST`, first
for selected stringVAs and then derived candidate typeinfoVAs. Counts are
complete. Exceeded caps discard all partial candidate materialization and
report the whole count; no firstN prefix is retained. There is no base graph,
encountered callee/global/provider or instruction follow. The strict existing
Mach-O/function-start parser was consulted as inert text, never imported/run.

After reading the entire new retained checker, the only repeatable check is:

```sh
/usr/bin/python3 -I -B analysis/ableton-live-12.4.3/full-spec-v1/depth-wavetable-x86-typed8-metadata-v1/check-retained.py
```

It reads this packet and three immutable document pins only, verifies every
retained raw/pointer/header/command join and rejects13 false-promotion controls.
It never opens the original image/tool or imports the collector. The frozen
observed summaries are `author-check.json` and `retained-check.json`.

No C/native semantic acquisition, decoder, original/model/harness execution,
build or install occurred. No owner/case/grade/site/release/ready-X changed.
Unsupported behavior remainsU and whole-product coverage remainsOPEN.
Root owns adoption, any independent review and any separately selected next
metadata/source work; this packet selects no successor. No shared wiki or
previous immutable packet was edited.
