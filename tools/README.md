# Analyst navigation tools

These tools build views of retained research evidence. They are not code for the
independent application and must not be included in a clean implementation handoff.

## Artifact browser

From the repository root:

```sh
python3 tools/build_artifact_browser.py
```

Uses Python's standard library and the existing `analysis/ableton-live-12.4.3/`
captures. Produces an offline HTML browser, readable Push2 assembly/callee/string
extracts and a provenance manifest under `analysis/ableton-live-12.4.3/browse/`.
Only these replaceable views are regenerated. Original captured files and their
checksum manifests are preserved. Missing captures must be restored locally;
the generator does not launch Ableton, download evidence or run a decompiler.

Use the [artifact catalog](../wiki/research/artifacts/index.md) to browse outputs
and understand analysis coverage. Generated browsers are tracked in Git since
2026-10-17; extracted binaries and raw corpora are not (see `.gitignore`).


## Native decompilation transport and corpus

The [native export design](../wiki/research/native-export-design.md) and
[execution guide](../wiki/research/native-export-execution.md) describe identity,
resource limits, recovery and exact launch commands.

- [run_native_analysis.mjs](run_native_analysis.mjs) starts one installed REA MCP
  server and processes file-spooled requests sequentially. Starting it performs
  only handshake/catalog operations; binary opening and expensive analysis must
  be explicitly requested by the coordinator after resource preflight. It needs
  the installed Ghidra and JDK paths in its environment. Use the coordinator's
  [resource monitor](monitor_native_run.py) for owned-process limits/log capture.
- [rea-env.sh](rea-env.sh) sets the Linux workstation environment for the `rea`
  CLI: Ghidra/JDK paths, Node 24 and rizin. Source it before running `rea`.
- [export_native_corpus.py](export_native_corpus.py) ingests retained evidence
  without running an analyzer. `init` freezes the target/profile/inventory,
  `ingest` writes immutable function revisions, `queue` lists pending addresses,
  and `check` verifies all committed output against authoritative retained evidence.
  Its `--help` and the execution guide show command arguments. Warnings, failures
  and exclusions remain visible in `coverage.json`; failures are never counted as
  recovered source.

Run the native analyst-tooling tests with:

```sh
python3 -m unittest discover -s tools/tests -p 'test_native_*.py' -v
```

The synthetic fixtures validate tooling integrity and lifecycle behavior. They
are not original-versus-candidate behavioral tests. Source snapshots and evidence
remain analyst-only; no recovered code crosses the clean handoff boundary.

## Compact archive and offline code reader

[compact_native_corpus.py](compact_native_corpus.py) stores exact committed
revisions and their source evidence in a separate fresh ZIP archive. It checks
the same evidence authority as the original exporter without rewriting source
coverage. Existing captures remain intact. [Measured storage and the execution
plan](../wiki/research/native-compact-storage.md) distinguish preservation from
new decompilation coverage.

```sh
python3 tools/compact_native_corpus.py build --corpus CORPUS --output NEW_ARCHIVE
python3 tools/compact_native_corpus.py check --root NEW_ARCHIVE
python3 tools/compact_native_corpus.py extract --root NEW_ARCHIVE --address ADDRESS --revision REVISION --output NEW_DIRECTORY
python3 tools/build_compact_native_browser.py build --archive NEW_ARCHIVE --output NEW_VIEWER
python3 tools/build_compact_native_browser.py check --root NEW_VIEWER --archive NEW_ARCHIVE
```

The [reader builder](build_compact_native_browser.py) produces local HTML and
JavaScript files. Open its `index.html`, search an address or alias, and select an
exact revision to read warnings, provenance and pseudocode or download original
UTF-8 code bytes. Code loads on selection, with bounded chunks and a two-chunk
cache. This reader covers archived attempts, not pending inventory entries.
The [current reader](../analysis/ableton-live-12.4.3/native-compact-view-v2/index.html)
and [interaction fix](../wiki/research/native-compact-storage.md#read-revisions-interaction-fix--2026-10-12)
are available in this workspace. “Read revisions” reveals and focuses the reader;
code appears before its expandable provenance. “Back to function list” returns
to browsing. Multiple revisions still require an explicit choice.
Build outputs into a fresh directory outside the immutable archive. Never
overwrite evidence to update a viewer.

The main browser prefers `native-compact-view-v2`, falling back to
`native-compact-view-v1` only when v2 is absent. Both require current-method
validation against `native-compact-mirror-v1`; an invalid v2 is reported rather
than silently replaced by v1. Regenerate the main browser after generating the
reader. Its `#python` navigation remains stable. Node fixtures cover reader logic;
the retained v2 Chrome check additionally covers one real local-file interaction.
Run all analyst-tool tests with `python3 -m unittest discover -s tools/tests -v`.


## Persistent Ghidra checkpoints

[run_persistent_native.py](run_persistent_native.py) provides a separately profiled
saved-project route. The [recovery design](../wiki/research/native-analysis-recovery.md)
and [readable author guide](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-author-v4/README.md)
explain resource gates, exact evidence and proof limits. Corrected target/fixture
profiles pass scope and quality reviews. The actual Live import/save passes;
its first reopen is blocked by fresh-launch disk capacity. See the
[execution report](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-execution-v2/README.md).
No accepted Live checkpoint or analyzed cold-decompilation result exists.

```sh
python3 tools/run_persistent_native.py import --target TARGET --output NEW_BASELINE_JOB
python3 tools/run_persistent_native.py analyze --checkpoint BASELINE_JOB/checkpoint --output NEW_ANALYSIS_JOB
python3 tools/run_persistent_native.py inventory --checkpoint VERIFIED_JOB/checkpoint --output NEW_INVENTORY_JOB
python3 tools/run_persistent_native.py export --checkpoint VERIFIED_JOB/checkpoint --inventory NEW_INVENTORY_JOB/export --entry 'ram:0xENTRY' --output NEW_EXPORT_JOB
```

These commands launch Ghidra; the coordinator must admit each target job first.
Import disables analysis and requires two disposable read-only reopens before
committing a closed checkpoint. Analysis runs once with a 900-second cooperative
limit and a 1,200-second whole-job limit; an accepted timeout checkpoint remains
partial. Exports require entries from that checkpoint's own qualified inventory,
first one entry then at most five per batch. Outputs stay outside the default
REA corpus. The `.incomplete` guard marks unaccepted jobs; its absence alone is
insufficient without the validated manifest, stages and result.

Target import requires 6 GiB fresh free disk, a 600-second whole-job limit and
at most 2 GiB retained allocation, including all four project representations.
Analysis requires the stronger measured four-copy reserve documented in the
recovery design, above its original minimum. Copies are charged at full allocated
size. The monitor stops below 3 GiB free disk or after two successive owned-RSS
samples above 6 GiB. No capacity gate is lowered to make a job fit.

The coordinator recommends at least 10 GiB free before another fresh target import,
to cover retained copies and observed global disk movement. Use a new output;
do not reuse either incomplete target attempt. Analysis still needs its separate
reserve after an accepted baseline; the current closed-import estimate is 13.54 GiB.

`--fixture` selects independently authored eight-byte ARM64 data for synthetic
proofs; those bytes are never executed. Fixture timeout/expansion flags are
rejected in target mode. Run the 56 scoped tooling tests with
`python3 -m unittest discover -s tools/tests -p test_persistent_native.py -v`.
The retained author guide distinguishes actual Ghidra proofs from mocked and
injected failure tests. None is an application compatibility test.

## Conditional selected-entry fallback

[run_targeted_native.py](run_targeted_native.py) and its
[Ghidra script](ghidra/SelectedNativeExport.java) prepare a separately profiled,
bounded export of selected entries without whole-program auto-analysis. The
[execution guide](../wiki/research/native-export-execution.md#conditional-fallback-preparation)
explains its inputs, distinct evidence format, resource limits and activation
condition. Preparation is the default; actual target import requires `--execute`
after the coordinator has stopped the unsuccessful default-profile run. This
route is not a replacement for full-inventory coverage. Compilation and synthetic
model tests do not establish native-output correctness.

## Revision 2 saved-project scripts (C1/C2 and queries)

All three scripts open a saved, analyzed project read-only (`-process PROGRAM
-noanalysis -readOnly`) and never re-run analysis. Ghidra lets only one process
hold a project, even read-only, so the bulk jobs hold `projects/LiveR2` while the
dossier server holds its own copy under `/var/tmp/sound-analysis/query/`.

- [R2FunctionDossier.java](ghidra/R2FunctionDossier.java) answers investigator
  queries (address, symbol or `str:` string) with function dossiers, pseudocode
  and reference reports, one-shot or as a spool-directory server; its header
  comment gives the usage line. See the [query route](../wiki/research/r2-query-route.md).

[R2BulkDecompile.java](ghidra/R2BulkDecompile.java) decompiles every non-external
function in one headless JVM with one decompiler per worker thread and a
60-second per-function timeout. It writes
`run.json`, fixed-size `chunks/chunk-NNNNN.jsonl` files (one record per function:
entry, name, body ranges, signature, state, warnings/error, code bytes, SHA-256
and the exact code) and `coverage.json`. Reruns validate and skip committed
chunks; `instances=K` spreads threads over K read-only program instances in the
same JVM to avoid the program database lock; `shard=i/n` selects every n-th
chunk for a spread sample or for several JVMs on separate project copies
writing into the same output.
[R2ExportIndexes.java](ghidra/R2ExportIndexes.java) writes deterministic
`strings`, `calls`, `indirect`, `vtables` and `aliases` JSONL files plus a
manifest; it can be a second `-postScript` in the same invocation.
[r2_corpus.py](r2_corpus.py) verifies both outputs without running Ghidra.
The [corpus tooling page](../wiki/research/r2-corpus-tooling.md) records the
design, Push2 measurements, Live projection and the exact Live command.

```sh
analyzeHeadless PROJECT_DIR PROJECT -process PROGRAM -noanalysis -readOnly \
  -scriptPath tools/ghidra \
  -postScript R2BulkDecompile.java out=CORPUS threads=N [instances=K] [chunk=200] [shard=i/n] \
  -postScript R2ExportIndexes.java out=INDEXES
python3 tools/r2_corpus.py corpus CORPUS
python3 tools/r2_corpus.py indexes INDEXES
python3 -m unittest discover -s tools/tests -p 'test_r2_*.py' -v
```

The chunk corpus is not the `export_native_corpus.py` layout and cannot be
ingested by it: that ingester accepts only REA `ev_` evidence records. The page
gives the conversion path.

## Revision 2 corpus browser (C3)

[r2_browser.py](r2_browser.py) builds one offline browser per verified C1 corpus and its C2
indexes, and refreshes an `r2-index.html` catalog of every browser in the same output directory.
It runs both `r2_corpus.py` checks first and writes nothing if either fails or the two describe
different programs. It reads JSONL only, never a Ghidra project, and streams chunks one at a time:
the page loads a function index, and each function's code, callers, callees, string references
and indirect sites load from its `chunks/chunk-NNNNN.js` file when opened. OUT is replaced as a
whole and must be absent or an earlier r2 browser.

```sh
python3 tools/r2_browser.py CORPUS INDEXES analysis/ableton-live-12.4.3/browse/r2/<slug> [--title TEXT]
python3 -m unittest discover -s tools/tests -p 'test_r2_browser.py' -v
```

Write output under `analysis/` in the home directory: the snap-packaged Chromium and Firefox on
the Linux workstation cannot open `file:///var/tmp/...` pages.

## Corpus resonator demo

[corpus_demo.py](corpus_demo.py) extracts the Corpus field list, preset values and ranges from the
shipped schema and presets, then fills [corpus_demo.html](corpus_demo.html) into an offline page.
The page's sound is a labelled textbook stand-in, not decompiled code. Output is tracked with the rest of `analysis/`.

```sh
python3 tools/corpus_demo.py            # writes analysis/ableton-live-12.4.3/demos/corpus/
python3 -m unittest tools/tests/test_corpus_demo.py -v
# self-test: open demos/corpus/index.html#selftest (also works in headless Chromium --dump-dom)
```

## Requirements browser

[spec_browser.py](spec_browser.py) collects every requirement of the draft specs (`type: spec`
pages in `wiki/specs/`, from `### REQ-…` headings or `| REQ-… |` table rows) and every row under
a `## Candidate requirements …` heading in `wiki/research/`, and writes one searchable static page
with links back to each source section. Rerun it after a spec or packet changes.

```sh
python3 tools/spec_browser.py    # writes analysis/ableton-live-12.4.3/browse/specs/index.html
python3 -m unittest tools/tests/test_spec_browser.py -v
```
