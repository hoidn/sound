---
id: DESIGN-MACHO-FUNCTION-STARTS
type: research
status: draft
updated: 2026-10-09
access: analysis
---

# Linker-declared function-start index

This bounded addition makes shipped binary structure discoverable while the
separate native analyzer runs. The pinned thin arm64 Mach-O contains one
`LC_FUNCTION_STARTS` command at file offset 6,928, pointing to 560,280 bytes at
137,089,496. This initial observation comes from reading its header/load commands;
it does not establish how many valid starts the payload contains.

## Design and scope

A reusable, read-only Python extractor will map the file, validate a little-endian
64-bit arm64 executable header, bound every load command and segment, and decode
the command's delta-encoded unsigned LEB128 stream relative to `__TEXT.vmaddr`.
Each nonzero delta advances a strictly increasing address. Require a zero
terminator, zero-only trailing padding, canonical bounded uint64 encodings,
aligned arm64 addresses, and a unique executable file-backed segment mapping.
Reject malformed, duplicate or ambiguous metadata rather than inventing
starts. An absent command produces an explicit absent result, never an empty
successful inventory.

Output is a new `derived/function-starts-v1` directory with an address/file-offset
TSV, summary, exact method copy and SHA-256 manifest. Pin the full target digest;
hash incrementally and write rows incrementally. No target execution, binary
modification, imports or native analysis are needed. The process uses mmap and
small buffers; the wall-clock deadline is sixty seconds. The resource goal is
less than 128MiB incremental resident memory, measured on the actual extraction.

These are **linker-declared starts**, not a Ghidra-discovered function inventory,
body ranges, names, type recovery or proof that all code is represented. Do not
merge these records into the default native corpus denominator. Gaps between
starts are not function sizes. They can nominate bounded future investigations.

## Task plan and acceptance

1. Retain the observed command and inspect installed format/decoder sources.
2. Implement strict header/load-command/segment and ULEB validation, with streaming
   output staged before a final directory commit.
3. Test malformed ULEB, truncation, command bounds, unsupported architecture,
   segment mapping and ambiguous mapping; reject bad target identity.
4. Extract the pinned input once into a fresh artifact directory and record
   measured time/memory and exact method/output hashes.
5. Obtain independent scope and quality reviews before claiming the index is
   accepted; the coordinator updates navigation and the shared log.

No application implementation changes or native-analysis retries are part of this task.

## Actual capture and review state

The extractor and twelve parser/export tests are implemented. The [sealed
summary](../../analysis/ableton-live-12.4.3/derived/function-starts-v1/summary.json)
records **413,794 linker-declared starts**, from `0x100002000` to `0x1054d20c4`,
for the pinned SHA-256
`3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad`.
Extraction took 1.04 seconds with 31,539,200 bytes peak process RSS, below the
128MiB goal. The [TSV](../../analysis/ableton-live-12.4.3/derived/function-starts-v1/addresses.tsv)
contains address, file offset, segment and source ULEB byte offset; the [manifest](../../analysis/ableton-live-12.4.3/derived/function-starts-v1/manifest.json)
hashes the exact extractor copy, TSV and summary. The target remained unchanged.

The retained [format-source manifest](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/function-starts-source-v1/manifest.json)
pins Apple's installed macOS 15.2 SDK `mach-o/loader.h` and Ghidra 12.1.4's
`FunctionStartsCommand.java` and `MachoFunctionStartsAnalyzer.java`. The former
Ghidra class explicitly accumulates ULEB deltas from the `__TEXT` base. The latter
warns that some reported starts are not real functions and applies further code
analysis before creating them. This explains why a large address index cannot
be substituted for successfully recovered functions or an analyzed inventory.

Reproduce into a **new** output directory:

```sh
python3 tools/index_macho_function_starts.py \
  --target analysis/ableton-live-12.4.3/derived/Live.arm64 \
  --output PATH_TO_NEW_OUTPUT_DIRECTORY
python3 -m unittest discover -s tools/tests -p test_macho_function_starts.py -v
```

The CLI enforces a sixty-second alarm. Existing outputs are rejected, not
rewritten. An absent command produces a summary with `status: absent` and no TSV;
malformed input fails without committing a directory. The tests cover explicit
absence, duplicate commands, header/architecture rejection, command/segment
bounds, nonzero segment file offsets, overflow, noncanonical/truncated ULEB,
termination/padding, alignment, ambiguous/non-executable/unbacked addresses,
target identity, staged failure and manifest consistency. They passed locally;
independent [scope review](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/function-starts-scope-review-v1.json)
and [quality review](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/function-starts-quality-review-v1.json)
passed, including an independent full-table decode. The
[focused navigation review](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/function-starts-navigation-quality-review-v1.json)
checks the atlas/source claims. No native analyzer or original application was
launched by this extraction.
