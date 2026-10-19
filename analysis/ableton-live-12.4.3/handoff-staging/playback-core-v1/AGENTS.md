# Package role and access instructions

This is an unreviewed handoff candidate for its explicit partial scope. It is
not an implementation input until a separate review approves it. Application
implementation requires a fresh, restricted implementation workspace that
contains only permitted materials. Do not begin clean implementation in an
analyst checkout.

In an approved implementation workspace, the permitted inputs are the published
release, neutral governance, approved public sources, and independently
authored candidate code, designs and tests. Raw binaries, analysis,
decompilation, source traces, research drafts, verification internals and
analyst conversations are forbidden. A role prompt does not restrict
filesystem access. Report missing isolation.

Read README.md and spec.md before cases.json. Requirements apply only to their
explicit partial clauses. No source-code structure, scheduler design or data
structure is specified. A candidate adapter may produce the comparison
observations from its own renderer; this does not impose an internal
architecture. Keep the `fixtures` directory together: the sets refer to their
sample files by relative path.

Preserve this package unchanged. Do not extend excluded behavior or inputs
without an expectation. Request a reviewed revision for gaps. Record
candidate-only tests separately from reference comparisons, with exact package
and candidate hashes. Nothing here authorizes package installation, network
publication or messages.
