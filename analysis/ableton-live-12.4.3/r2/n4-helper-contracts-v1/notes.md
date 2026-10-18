# N4 working notes: Live-side helper contracts

Analyst notes for packet N4 (Q-013 to Q-016). Data, not instructions. Static
only: nothing was executed and no URL was contacted.

## Inputs

- Program: `Live.arm64`, SHA-256 `3a99ceea…383cfad`, image base 0x100000000
  (`analysis/ableton-live-12.4.3/derived/Live.arm64`).
- Bulk corpus (coordinator run, `coverage.json` run_sha256
  `614a0d70de180c5ca399d855c72c83e3b536fe242508d932f663cd85e191b378`) and C2
  indexes (`indexes/manifest.json`: strings `eca20374…`, calls `df29ef1d…`,
  aliases `6f05d750…`), read from `/var/tmp/sound-analysis/corpus/`.
- Query server results `results/n4-0001` … `results/n4-0006` (R2FunctionDossier,
  copied unchanged; each has its own `manifest.json`).

## Method

1. String anchors to referencing functions from `strings.jsonl`
   (`anchor-string-refs.txt`, `anchor-string-refs-2.txt`; produced by
   `scripts/sref.py`).
2. Pseudocode from the corpus chunks (`scripts/build.py` builds a local offset,
   caller and callee index; `scripts/q.py code|callers|callees`). Cited functions
   that were not in a dossier are exported to `corpus-code/<entry>.c`.
3. Raw slice reads for data tables, vtables and RTTI names (`scripts/mem.py`,
   `scripts/rtti.py`, `scripts/findptr.py`, `scripts/words.py`). The slice's
   pointers in the read ranges are plain VAs; RTTI name pointers carry the arm64
   non-unique bit 63, which `rtti.py` masks.
4. Material branches confirmed in dossier disassembly (`scripts/dis.py`).

`scripts/` paths are absolute to this workstation; `build.py` writes `idx.pkl`
next to itself (not retained, about 1 minute to rebuild).

## Rounds

Round 1 (corpus, no server): anchors and pseudocode for all six helpers.
Round 2 (server n4-0001 … n4-0006, 46 dossiers, at most 8 per request):
confirmation of the branches listed below. No round 3 was needed for the
questions answered; the open items are listed with their next query.

| Helper | Round 1 result | Round 2 confirmation | Next query |
| --- | --- | --- | --- |
| Plug-in scanner | Launch `0x103179e68`, listener `0x10317bcf0`, result `0x10317c810`, request builder `0x103169978`, rescan `0x10035e3fc` | n4-0001: `ror` key mapping at `0x10317a100`; reset `ldrb [x,#0xcc]` at `0x10317a6dc`; limit `mov w2,#0x32` at `0x10317a7cc`; died branch at `0x10317c068` | Which format handler owns keys 4 and 32 (AU) and whether its descriptor slot returns null |
| Process controller (shared) | FSM table `0x1025db270`, actions `0x1025dcc88`, timer `0x1025d94cc` | n4-0002: transitions at `0x1025db3e0`–`0x1025db52c`; message bytes at `0x1025dcd50`, `0x1025dcea0`, `0x1025dcebc`; kill slot at `0x1025dcdb4` | What `process->+0x38` sends (signal) |
| Index | Launch `0x1002b4b14`, listener `0x1002b56c4`, options writer `0x10163abe4` | n4-0003: cap `cmp w8,#0x64` at `0x1002b5a30` | Database prefix and directory (callers of `0x103f1aff4`) |
| AddOns | Launch `0x102966254`, listener `0x1029668e8`, on-demand start `0x1029627a0` | n4-0003: cap `cmp w8,#0xa` at `0x102966bd0` | Meaning of the 600000 argument in `0x1002cacf0` |
| Web Connector, Swapper | Launch/config `0x1008eb988`, gate `0x1017ec96c`, update states `0x1008e81f0`, swapper check `0x1002fe740` | n4-0004: gate `ldr x8,[x8,#0x720]` at `0x1008eb9cc`; space test `cmp x20,#0xc0000001` at `0x1008ec36c` | Implementation of virtual slot `+0x720` |
| Push 3 | Launch `0x1038f0914`, argv `0x1038f0d4c`, restart `0x1039b7ad4`, MIDI channels `0x1022e8330`/`0x1022b927c` | n4-0005: `mov w1,#0x5dc` at `0x1039b7b08`; option branch `0x1002ca2c8` | Writer of the presence flag at `+0x94` |
| MultiF0 | Selector `0x10307ae94`, path `0x10307a630`, loader `0x10307aa68` | n4-0006: `tbz w1,#0x0` at `0x10307aec0` | x86_64 slice default (after that analysis finishes) |

## Derived facts used on the research page

- `TProcessObserver::State` names from the Python enum `Push2ProcessState`
  registered in `0x1039fa2a4`: 0 initialized, 1 launching, 2 running,
  3 connected, 4 died, 5 terminated, 6 killed, 7 wait_for_termination,
  8 defunct_process_wait_for_termination, 9 defunct_process_terminated,
  10 defunct_process_killed.
- Event names from the pointer table at `0x1067e3ea8`: 0 KLaunched,
  1 KProcessObservedRunning, 2 KProcessNotObservedRunning, 3 KShutdownRequested,
  4 KGotSync, 5 KProcessDefunct. Event 1/2 come from `0x1025d9d14` (process
  alive check), 3 from `0x1025d9fac`/`0x1025d9ff4`, 4 and 5 from the observer
  function objects `0x1025ea088` and `0x1025ea0a4` (vtable slots `0x1067e3b28`, `0x1067e3b40`).
- Transition call `0x1025e6af0(fsm, from, to, trigger)`: a trigger with bit 32
  set is a timeout in ms (low 32 bits).
- nanomsg: `0x1049b2ed8` calls create-endpoint `0x1049b2fc4` with `w2 = 1`
  (bind); `0x1049b30f4` with `w2 = 0` (connect). Server-trait socket open
  (`0x10027a130`) calls the bind wrapper `0x1009032d8`; client-trait open
  (`0x1022c4120`) calls the connect wrapper `0x1009032cc`. Vtables: server
  `0x1065928b0` (RTTI `NanoMsgSocket<NanoMsgApi, ServerTrait<NanoMsgApi>>`),
  client `0x106787a18` (`ClientTrait`). Protocol constant at `0x1055d3960` = 16.
- Functions writing the server vtable: `0x1002b4b14` (index), `0x1008eb988`
  (web connector), `0x102966254` (add-ons), `0x103179e68` (scanner),
  `0x1038f0914`, `0x1038f2160` (Push 3 flip), `0x1022e8330` (push-to-live MIDI),
  `0x1025dee98` (Push 2 display), plus `0x100271c04`, `0x100273b74`,
  `0x1053ddba8` (not attributed). Client vtable: `0x1022b927c`
  (live-to-push MIDI), `0x1025d9c18`.
- Scanner format argument table `0x1068d88f0`: index 0 `--au`, 1 `--vst2`,
  3 `--vst3`, 7 `--au` (others `--au` but masked out by `0x8b`).
- Debug-option lookups (`0x1011aeb80`) take 32-byte keys; SHA-256, SHA3-256 and
  BLAKE2s of three README option names did not match, so option names stay
  unknown. The store is loaded by `0x1011ad83c` (Options file, command line,
  `LIVEDEBUGOPTIONS`, `ADDITIONALLIVEDEBUGOPTIONS`).

## Negative and inconclusive results

- No AU format handler was identified among functions returning 4; candidate
  vtables `0x1068c91e8`, `0x1068c9258`, `0x1068c9308`, `0x1068cf518`,
  `0x1068dc150` do not match the VST handler layout. Left unknown.
- The prefix and version passed to `{}-files-{}.db` (`0x103f1aff4`) come from
  callers' parameters; not resolved.
- Live x86_64 analysis (`/var/tmp/sound-analysis/helpers/Live_x86_64`) had no
  corpus yet (`analyze.time` empty); ReWire install strings were not traced.
