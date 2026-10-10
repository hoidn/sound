# Ableton reconstruction project

This workspace holds the research, behavioral specifications, implementation
documentation, and validation record for an independent desktop application
informed by Ableton Live. The documentation system is established; application
implementation and behavioral verification have not started. Retained package evidence, helper pseudocode and MIDI bytecode traces are
available through the analyst artifact catalog.

Start with [agent instructions](AGENTS.md) and [project status](wiki/project.md).

| Work | Entry point |
| --- | --- |
| Browse the documentation as an analyst or maintainer | [Wiki index](wiki/index.md) |
| Learn page formats and authority rules | [Schema](wiki/schema.md) |
| Ingest, query, update, release, or lint | [Workflows](wiki/workflows.md) |
| Browse binaries, pseudocode and disassembly (analyst) | [Artifact catalog](wiki/research/artifacts/index.md) |
| Research the original application | [Research](wiki/research/index.md) |
| Define observable behavior | [Specifications](wiki/specs/index.md) |
| Build from a reviewed specification | [Released handoffs](handoff/index.md), then [implementation](wiki/implementation/index.md) |
| Compare reference and replacement behavior | [Verification](wiki/verification/index.md) |

The three layers follow the user-supplied LLM Wiki pattern:

- `raw/`: immutable source captures and externally stored artifact references.
- `wiki/`: maintained synthesis, specifications, decisions, and implementation docs.
- `AGENTS.md` plus `wiki/schema.md`: routing and maintenance rules.

`handoff/` adds an immutable, reviewed specification boundary between analysis
and independent implementation. The [first finite release](handoff/midi-config-v1/README.md)
covers three MIDI configuration assignments; its expected results remain
unexecuted against the reference. Directory names
alone do not enforce clean-room isolation.

Open this directory as an Obsidian vault if useful. Standard relative Markdown
links also work in ordinary editors. The local [Neovim setup](wiki/editor-navigation.md)
adds rendered Markdown and link navigation; start with `nvim wiki/index.md`.
No Obsidian plugins, embeddings, or search
service are required. Git records documentation changes; no remote is configured
by this setup.
