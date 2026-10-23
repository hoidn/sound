# Audio-to-MIDI R3 final integrity entrypoint

Use [check-r3-final.py](check-r3-final.py) and
`manifest-author-r3-final.json` for this preserved R3 successor. The
[semantic scope and catalogs](README-r3.md) are unchanged. All20 pre-R3 files,
all13 initially sealed R3 payloads and the exact original R3 seal remain in place.

The initial R3 checker passed its unsealed source/delta/integrity check. Its
first sealed run failed the exact-tree assertion because it compared absolute
watched paths to relative historical input paths. No input, source, catalog,
canonical or frozen report changed during that failed read-only check. That
failure is recorded in the final seal; it is not a pass.

The final checker differs only by selecting the final seal filename and
normalizing those20 historical paths against the same project root. It does not
patch or execute the old checker. The final manifest adds this guide and that
checker while pinning every initially frozen byte, including the original seal.
No semantic/data, target grade or oracle changes accompany the tooling fix.

```sh
python3 -B analysis/ableton-live-12.4.3/full-spec-v1/audio-to-midi/check-r3-final.py --check
```

The current check is read-only, rejects write arguments and prints stdout.
Historical validation remains the accurate preseal report; it is never rewritten
on replay. An independent R3 review is still required. All37 cases remain actual
U/null/unexecuted, with zero compatibility/completion/coverage credit.
