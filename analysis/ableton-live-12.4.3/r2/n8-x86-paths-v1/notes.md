# N8 working notes: x86_64 ReWire, MultiF0 and transport cross-check

Analyst notes for packet N8 (Q-013 plus an S3 cross-build check). Data, not
instructions. Static only: nothing was executed, no mixer or Rosetta process
was observed, and no URL was contacted.

## Inputs

- Live x86_64 slice `helpers/Live_x86_64/Live_x86_64.x86_64`, SHA-256
  `1bae9a972abadea304271696a2ccfe0ffb878d37e23a8d8e52effa297be999b0`, image base
  0x100000000, from `Contents/MacOS/Live` (SHA-256 `52289af6…7a35ef`, offset 16384).
- Its corpus `/var/tmp/sound-analysis/corpus-x86/` (`run.json` eligible 414,791,
  `coverage.json` run_sha256 `e381f6e8…cdb037d`: 317,021 exported, 97,725 with
  warnings, 45 failed, 0 pending) and C2 indexes (`indexes/manifest.json`:
  strings `26336158…`, calls `c8220d3f…`, indirect `5fbc26f8…`, vtables
  `ddea0f87…`, aliases `6dc3f78a…`).
- Ghidra project `helpers/Live_x86_64/project` (name `H`, program
  `Live_x86_64.x86_64`), opened read-only twice through `scripts/dossier.sh`
  (route step 4, helper-local XDG and `java.io.tmpdir`). Results `results/n8-0001`
  and `results/n8-0002`, each with its own `manifest.json`. Each run took about 6 s
  wall; no other process held the project.
- For comparison: Live arm64 slice `derived/Live.arm64` (SHA-256 `3a99ceea…383cfad`)
  and its corpus; Engine x86_64 slice (SHA-256 `028df12e…5843de`, image base 0)
  and corpus; MultiF0 dylib corpus.

## Method

1. String anchors to functions from the x86 strings index (`anchor-string-refs.txt`,
   `scripts/sref.py`).
2. Pseudocode, callers and callees from the corpus (`scripts/build.py` builds a
   scratch pickle per corpus; `scripts/q.py code|callers|callees`; `scripts/up.py`
   for transitive callers; `scripts/grepcode.py` for text searches over pseudocode).
   Cited functions not in a dossier are copied to `corpus-code/<build>-<entry>.c`
   by `scripts/extract_code.py`.
3. Raw slice reads for vtables, RTTI, keys and constants (`scripts/words.py`,
   `findptr.py`, `consts.py`, `bytecmp.py`, `segs.py`), collected by `scripts/run.sh`
   into `binary-reads.txt`. Linear disassembly with GNU objdump of raw slice bytes
   (`scripts/dis.sh`) into `objdump.txt`.
4. Material branches confirmed in Ghidra dossier disassembly (`scripts/ddis.py`).

Limit: the raw-read scripts assume VA = file offset + image base. That holds for
`__TEXT`, `__DATA_CONST` and `__DATA` of the x86 slice (checked with `segs.py`)
but not for `__LINKEDIT` (VA 0x10759d000, file offset 0x734e000). No cited read
lies in `__LINKEDIT`. The dossiers' DATA references from `0x108f2f2b4`,
`0x108f408db`, `0x108f40977` and `0x108f40994` are in `__LINKEDIT` (symbol-table
data), not code.

## Rounds

| Round | Kind | Content | Result |
| --- | --- | --- | --- |
| 1 | Corpus | Anchors for the install, Engine-alias, ReWire-loader and MultiF0 strings; pseudocode of `0x1024b0300`, `0x1024b0650`, `0x1024b0d30`, `0x1024b5060`, `0x1031d6b30`, `0x1031d6330`, `0x1031d67b0`; Engine `SIsReWire*Enabled` | Install and ReWire-host open sit behind `0x101ab6780` / `0x101ab68f0`, both `xor eax,eax; ret`; MultiF0 selector identical to arm64 |
| 2 | Dossier n8-0001 (8) | `0x1024b5060`, `0x1024b0300`, `0x101ab6780`, `0x101ab68f0`, `0x1024b5e50`, `0x1031d6b30`, `0x1031712f0`, `0x1028a0460` | Branches confirmed; incoming references limited to the listed calls, the LReWireHost vtable slot and `__LINKEDIT` data |
| 3 | Corpus | LReWireHost construction and slot `0x190` caller; TAudioToMidiTask subclasses and factory; MultiF0 record consumer; transport functions in both builds | Song-agent constructor calls slot `0x190`; Drums builds `TDtmTask`; record field use; transport bodies match |
| 4 | Dossier n8-0002 (8) | `0x1027c81e0`, `0x1024b0d30`, `0x1024b0650`, `0x1031d7420`, `0x103171b40`, `0x1028a3500`, `0x1028a54b0`, `0x101a6f3c0` | Call `[rcx+0x190]` at `0x1027c85c8` on the object at `this+0xe8`; other bodies as read |

## Derived facts used on the research page

- Domain constants passed to `FSFindFolder`: `0xffff8003` and `0xffff8005`
  (`0x1024b0300`); the log text picks `kLocalDomain` when the domain is `-0x7ffd`,
  else `kUserDomain` (`0x1024b0650`). Folder type `0x61737570` (`'asup'`).
- Tool runner `0x101180aa0`: fork/exec first (`0x1011807c0`); on a non-zero
  status and when `0x101198610` allows, `AuthorizationExecuteWithPrivileges`
  (`0x101180940`), which returns 2 for `-0xea66` (cancelled) and 1 for other
  failures. `0x1024b89a0` maps 1 to `sErrorAuthorizationFailed` and 2 to
  `sErrorAuthorizationCancelled` (keys bound in `0x1024b96f0`), sets the
  error-shown flag `0x10749b880` and returns 0; status 0 returns 1.
- LReWireHost vtable at `0x106cea210` (typeinfo `0x106ceb210`, `11LReWireHost`;
  base `11AReWireHost`, then `9ACompound`). Slot `0x190` (`0x106cea3a0`) =
  `0x1024b5060`. AReWireHost's own vtable ends after slot `0x188` (both builds),
  so `0x190` is an LReWireHost virtual. In arm64 the matching LReWireHost slots
  `0x190`–`0x1a8` are `ret`, `return 1`, `ret`, `return 0` (`0x10239f0c4`…`0x10239f0d4`);
  in x86 they are `0x1024b5060` (install/open), `0x1024b56e0`, `0x1024b57c0`,
  `0x1024b5890` (device count at `+0x40`). Slot `0x188` returns 0x28 in both.
- Engine/Live correspondence: the 0x180 bytes from Engine `0xe73f0`
  (`OEngineReWireData::SIsReWireDeviceEnabled`) and Live `0x101ab6780` agree in
  361 bytes (0.940); differences are rel32 displacements. Engine
  `SIsReWireHostEnabled` is `0xe7560`, Live `0x101ab68f0`; both offsets are
  `+0x170` from the device predicate.
- Debug-option keys (32 bytes): the MultiF0 key at x86 `0x105e2c7b8` equals the
  arm64 key at `0x1058c29f8` byte for byte. `0x101188890` returns "not found"
  unless flag `0x1073bb210` is 1; only `0x101187200` sets that flag (not traced).
- TAudioToMidiTask (`0x106dff788`) subclasses: `8TDtmTask`, `12TMultiF0Task`,
  `20TMockAudioToMidiTask`. Factory `0x1031712f0`: mock when run mode
  (`0x10118fec0`) is 2 and `0x1074b89f8` is 0; otherwise `cmp r15d,1; ja` selects
  TDtmTask (`0x1031a5c70`) for type ≥ 2 and TMultiF0Task (`0x1031d7d40`) for 0/1.
  Labels `H2M`, `M2M`, `D2M` at `0x106e00090`. Enum `AudioToMidiType`
  (`0x103ca34b0`): harmony 0, melody 1, drums 2. Menu callbacks pass `esi` = 0/1/2
  (`objdump.txt`).
- MultiF0 record (32 bytes) as read by `0x1031d7420`: floats at `+0`, `+4`, `+8`,
  pointer `+0x10` to `count` 8-byte (float, float) points, `count` (int) at
  `+0x18`, float `+0x1c`. Constants: 440.0, 12.0, 69.0, 127.0, 0.5, 1.0,
  0.49999999999999994; `_fma` stub `0x105a4e952`.
- Builtin default parameters (`0x1054eac80`): ints 0, 1; floats 40, 3140, 6,
  0.093, 15, 23, 1.3, 19, 20, 0.001, 0.1, 0.01, 3; int 8. Builtin
  `GetApiRevision` (`0x1054eac40`) returns 10.

## Transport cross-check table

| Role (arm64 page name) | arm64 | x86_64 | Agreement |
| --- | --- | --- | --- |
| OnStart wrapper | `0x102770a58` → `0x10276a7b0`(1,1) | `0x1028a9aa0` (symbol `CallMemberFunc<&ATransport::OnStart>`) → `0x1028a3500`(1,1) | Same |
| OnStop wrapper | `0x102770a64` → `0x102767b70` | `0x1028a9ac0` (`…OnStop`) → `0x1028a0460` | Same |
| Direct Start callers (1,1) | `0x102767a70`, `0x102767a7c` | `0x1028a0300`, `0x1028a0320` | Same |
| Toggles (0,0) | `0x10276b2a0`, `0x10276b370` | `0x1028a4080`, `0x1028a4160` | Same tests (`+0x8c8`, `+0xf0`, `+0x788`) |
| SendRequestForSetPlaying | `0x101a4abd8` | `0x101a6f1f0` (to thread 0x10100, slot `+0x10`) | Same |
| OSendThreadMessage slot +0x10 | `0x101ab7898` | `0x101ae06b0` (RTTI `18OSendThreadMessage`, dummy `0x1073e8050`) | Same |
| OSetPlayingCommand handler | `0x101a524b8` → `0x101a4ac8c` | `0x101a76fc0` → `0x101a6f290` | Same host-callback test, count-in test |
| SetPlaying(false) | `0x101a4adec` | `0x101a6f3c0` (`cmp $0xdad` at `0x101a6f43a`, `cmpl $3` at `0x101a6f45d`) | Same; callback globals at `0x10750a1d0/1d8/1e0` (panic) and `0x10750a1f0/1f8` |
| Reflection | `0x10276c538` | `0x1028a54b0` (caller `0x1027e75a0`) | Same, including an early return when `+0x900` = 1 that the arm64 page does not describe |
| Stop transfer 1 | `br x1` `0x102767c98` | `jmp rax` `0x1028a0584`, `[[this+0x240]]+0x248`, `xmm0=0.0` | Same |
| Stop transfer 2 | `br x2` `0x102767c60` | `jmp rax` `0x1028a05db`, `[[this+0xb0]]+0x248`, `esi=0` | Same |

Differences seen: x86 passes the engine pointer to the extern-sync test
(`0x101a6c470(engine)`); arm64's `0x101a48488` is shown without an argument by the
decompiler. x86 reaches the Stop body through a one-call wrapper `0x1028a0450`
(17 call edges); arm64 has 23 direct call edges to the body, one of them a tail-jump thunk. Neither changes the derived
transitions.

## Negative results and open items

- No direct or data reference to `0x1024b0300`, `0x1024b0650` or `0x1024b0d30`
  other than the chain above; no stored pointer to them in the slice.
- `0x1024b5e50` (panel-side `RWPOpen` loader path through `0x101b2e930` →
  `0x1054224a0`) has no caller, no stored pointer and only a `__LINKEDIT` data
  reference. Unreached statically.
- `0x1024b4840` (device-enabled and interactive check) has no direct caller and no stored pointer.
- Not traced: the variant visitor in `0x103171b40` instruction by instruction;
  units of record fields `+0`/`+4`; the meaning of note byte `+0x20` and of
  default-parameter fields other than int[1]; `0x101187200` (option table load).
