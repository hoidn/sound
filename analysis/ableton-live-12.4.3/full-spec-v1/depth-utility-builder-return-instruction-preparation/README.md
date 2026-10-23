# Utility builder return: instruction-data preparation

AS OF AUTHOR FREEZE: independent preflight and Root execution selection are pending. This preparation has not extracted image bytes or run the decoder. It preserves the old pattern and all source providers.

The one proposed window is `[0x101aa80cc, 0x101aa812c)`: final 96 bytes of the exact complete 456-byte `101aa7f64` body, 24 instruction slots. It is a candidate tail, not an already identified normal epilogue. The source projection appends kind 7 but has a void/bare return; the caller consumes a returned pointer. The selected data could narrow only that return-value gap.

`plan.json` fixes the image/tool identities, window, mapping and exact one-attempt `pdj 24` argv. `source-delta.json` records every literal change from the retained 16-byte pattern. The new code permits only `python3 -B extract-decode-once.py --extract-decode-selected-once <exact-manifest-sha256>` after separate Root selection. It refuses an existing destination; no retry or override is available. Do not run it as a readiness check.

Future results retain exact raw data/decoder output, PID/exit/exception and durable before/after maps, including ordinary failures. A returned decoder PID is not original instruction execution. No semantic result is computed automatically. Unresolved non-call control flow outside the window stops interpretation; opaque ordinary BL return/effects and ABI can remain explicit premises, without following targets. Missing normal return/value origins also stop interpretation. Filesystem failures or uncatchable termination can prevent complete receipts and must be disclosed.

All 38 Utility application outcomes stay U/unexecuted. No public Mute binding, runtime invocation, processor identity, numeric law, case, grade or release change is adopted.
