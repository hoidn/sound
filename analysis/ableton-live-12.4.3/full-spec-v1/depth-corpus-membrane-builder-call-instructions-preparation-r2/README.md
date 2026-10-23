# Membrane builder call: one static 12-byte decode preparation

Preparation only. Root must independently preflight this frozen packet and
separately select the one actual attempt. Neither collector nor decoder has run;
the instruction window has not been extracted. No original instructions execute.

The [approved source base join](../reviews/corpus-membrane-builder-base-review.json)
is limited to projected case4: builder B=M+0x148. Its call lists only one argument,
while the recovered builder declares two. [proposal.json](proposal.json) selects
only [0x24884,0x24890), ending at indexed call2488c. W1's origin outside these three
words remains unknown; stop without automatically adding an earlier prefix.

[inputs.json](inputs.json) pins the exact retained Corpus.arm64 image, existing
rizin0.9.1 tool, reviewed source providers and two fully inspected old patterns.
No old script is loaded, imported or replayed. Fresh full image SHA256 and only
MachO header/load-command metadata were checked. [header-map.json](header-map.json)
retains the unique file-backed TEXT mapping and full header/command bytes;
it retains no instruction-window bytes. No tooling is installed or rebuilt.

[collect-once.py](collect-once.py) is a dedicated future one-shot tool collector.
Its separate exclusive destination must be absent. It pins the preparation,
writes durable before/attempt/returned-PID/after/status records, extracts exactly
12 bytes and invokes only raw/noinit/noexecute static `pdj 3`, with `-f` for exact
file blocksize. Timeout is30seconds, core limit0; partial tool output and every
normal failure are retained, no retry. Failed spawn is distinct from returned
PID. Pre-directory refusals and catastrophic receipt I/O need coordinator outer
receipts; there is no blanket partial-output guarantee for disk failure.

Read [check.py](check.py) before its data-only command:

```sh
python3 -B analysis/ableton-live-12.4.3/full-spec-v1/depth-corpus-membrane-builder-call-instructions-preparation-r2/check.py --check
```

It never imports the collector, extracts the instruction window or launches the
decoder. It verifies metadata/input/seal identities and exact AST/source guards,
rejecting eight wrong range/length/row/flags/timeout/destination variants. The
original and proposal status stay unexecuted. A later successful static decode
would still require qualified register interpretation; it would not establish
actual count70, physical mode identity, rounded coefficients, x86 equivalence,
a numerical acceptance rule, public behavior or compatibility. All174+2 omitted
observations remain ungraded. No owner/case/shared/release change is proposed.

R2 addresses only MEMCALL-PREFLIGHT-001 from the [R1 review](../reviews/corpus-membrane-builder-call-code-preflight-r1.json).
The R1 eight-file tree stays immutable. Its permissive row predicate admitted
synthetic type `ill`/opcode `invalid` rows with otherwise correct metadata.
R2 explicitly rejects invalid/ill types and absent/None/invalid/ill/empty
opcodes. [correction.json](correction.json) reverses the two collector operations:
new exclusive destination and only the row predicate. The image, range, argv
flags, attempt/accounting/receipts and other collector logic are unchanged.
Focused synthetic AST-only row fixtures exercise the actual predicate; no
collector function/module is loaded and no original/window/decoder is run.
Ten malformed-row sets now reject while a valid synthetic three-row control
passes. R1's exact invalid/ill finding is reproduced using only its selected
AST predicate; no R1 main/module is loaded or replayed.
