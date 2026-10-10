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
and understand analysis coverage. The generated files are local and ignored by
Git; the generator and wiki navigation are maintained in the repository.


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
