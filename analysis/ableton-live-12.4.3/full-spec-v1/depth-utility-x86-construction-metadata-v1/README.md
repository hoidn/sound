# Utility x86 construction frontier: three linker-start nominations

Analyst metadata only, 2026-10-20. Frozen for independent packet review; any
instruction capture requires a separate Root selection. No shared research,
specification, case, grade or release is changed by this packet.

Root explicitly selected exactly the named factory nomination `0x1022313c0`
and the two static direct-call targets `0x101ad08a0`/`0x102231400` from the
already reviewed pre-steering prefix. This follows amended plan revision 4's
parallel D03 route and the approved whole-six-gap Utility source/native work.
It is a supporting construction frontier, not a fresh architecture or another
numeric outcome example. [Pins](pins.json) identify the current selector and
canonical research as mutable as-of context, and eight immutable predecessors.

| Selected entry | LC_FUNCTION_STARTS ordinal (zero based) | Immediate next start | Proposed physical read bound |
| --- | --- | --- | --- |
| `0x101ad08a0` | 117275 | `0x101ad0910` | 112 bytes |
| `0x1022313c0` | 152730 | `0x102231400` | 64 bytes |
| `0x102231400` | 152731 | `0x102231490` | 144 bytes |

All three entries and successors are inside file-backed `__TEXT/__text`.
The disjoint half-open bounds total 320 bytes, below the proposed 8,192 bytes
per interval and 16,384 bytes per batch. These are possible future read caps,
not a selected capture, complete function sizes, all reachable instructions,
control flow or dynamic execution boundaries. A function may branch outside
an adjacent-start interval. Exact membership proves linker metadata only.

## Source custody and permitted reads

[Metadata](metadata.json) retains only the three selected row/successor pairs,
their immediately preceding accumulated addresses, ordinal/delta locations,
small raw ULEB witnesses, header geometry and table digest. Five distinct
table offsets contribute seven witness bytes (one shared successor is also
the next selected entry). The full table and global parsed address universe
are not copied. The 412,317 parsed starts are only metadata-processing count,
not functions, coverage units or a product denominator.

The existing thin x86 image is
`/var/tmp/sound-analysis/helpers/Live_x86_64/Live_x86_64.x86_64`,
163,716,848 bytes. Its full SHA256
`1bae9a972abadea304271696a2ccfe0ffb878d37e23a8d8e52effa297be999b0`
is inherited from reviewed header/nlist/prefix provenance; this task did not
rehash its full contents. Fresh file size and before/after device/inode/size/
mtime/ctime match. These checks qualify custody; they are not continuous
preservation or a fresh whole-image identity proof.

The one metadata read at 23:53:31 UTC opened only:

- 32 bytes at file offset 0: thin Mach-O header, matching the retained header;
- 6,832 bytes at offset 32: all 54 load commands, byte-identical to the retained
  header-map, SHA256 `df1dcfb46925870cf898004eb1d97ff632c25d068713a05c653af4c113ad26d4`;
- 559,744 bytes at offset 147,556,352: `LC_FUNCTION_STARTS`, command index 51
  at header file offset 6,816, wholly inside `__LINKEDIT`, SHA256
  `631d58cef27428cc74c2542dee96b82b643552f1efcc27b57740e4c2664b8fec`.

The table terminator occurs at relative byte 559,742 and has one zero padding
byte. Canonical uint64 ULEBs, positive cumulative deltas, monotonic unique
starts, executable/file-backed TEXT mapping and complete terminator/padding
were checked while traversing metadata. No ARM four-byte alignment rule is
applied to x86; an odd-address synthetic positive control protects that rule.
No image instruction window, raw code, callee body, decoder or original was
read/run. Total source-image reads were 566,608 metadata bytes.

## Roles and unresolved joins

The retained nlist query's
`/selection/rows/OStereoGainProcessor/0` is nlist index 8568, raw16
`a79712000f018000c013230201000000`, value `0x1022313c0`, section 1
`__TEXT/__text`, name
`__ZN23OProcessorCreateManager18SOnProcessorCreateI20OStereoGainProcessorEEvR14OThreadMessage`.
That exact name/value is the factory nomination; neither the name nor a
linker start proves a formal factory, constructor, allocation, ABI, actual
processor identity, successful construction or host admission. No fresh
nlist/string-table read or new symbol search was needed.

The independent pre-steering actual review's `/checks/3/calls` identifies
the two E8 targets from the already decoded prefix. Its reviewed manifest
and provenance remain predecessors, not renewed source-body analysis. The
old 240-byte selection, sixteen rows/47 decoded bytes and 193 opaque bytes
are unchanged. In particular, metadata membership of `0x102231400`, which
lies in that opaque suffix, does not interpret any suffix byte. No prefix
payload was reopened or rewritten here.

The approved ARM actual review narrows conditional register carriers only.
It neither identifies either x86 target as an ARM counterpart nor proves
constructor/base roles by analogy. All six existing bridges remain unknown:

- G01: actual construction/admission; this packet adds navigation only.
- G02: delivery of a current public value to the registered callback.
- G03: same receiver and order between callback and later processing.
- G04: result cells reaching the actual host output.
- G05: active load/default/migration/legacy and lifecycle relationships.
- G06: x86/ARM/public equivalence; separate metadata domains remain separate.

All 38 application outcomes and the predecessor 48-predicate inventory remain
unchanged. No ABI, public instance, indirect-site credit, X/S grade, criterion,
case, owner revision, release, complete profile or next code selection follows.

## Method and checks

[metadata.py](metadata.py) is a new, small stdlib-only metadata reader and
read-only checker. The existing `tools/index_macho_function_starts.py` was
fully inspected as data, never imported or executed. Its ARM64 alignment,
whole-image mmap/hash and global-index output were unsuitable here; only
header/load-command/ULEB parsing ideas were reused. No old collector/module
was imported or run. The collection branch is exclusive-output and requires
`--read-selected-metadata`; it refuses the already existing metadata output.
After that one metadata read, only the checker was strengthened; acquisition
logic and retained metadata bytes stayed unchanged.

Run the check from any directory with:

```sh
python3 -I -B /home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-x86-construction-metadata-v1/metadata.py --check
```

The check reads this packet and eight exact small retained source artifacts,
not the image or an old watched universe. [Author check](author-check.json)
records exact selected/next-start associations, retained header/TEXT mapping,
source pins, limits and sixteen malformed-data/false-promotion controls plus
the x86 odd-address positive control. Table payload hash/absolute ordinals
are receipts of the one metadata traversal, not independently replayed by
the read-only checker. The final manifest inventories all payload bytes;
independent review remains pending and external to that manifest.
