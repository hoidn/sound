# Handoff directory rules

Follow the root routing and schema. This directory stages approved releases.
No release exists at initialization.

- `index.md` is mutable catalog state.
- A release payload becomes immutable when its passing review and manifest
  digest are recorded in the catalog. Correct it with a new release.
- Never publish recovered source, decompilation, original internal architecture,
  restricted source links, or analyst transcripts in a release.
- Include a release-specific `AGENTS.md` that overrides irrelevant staging
  routes and permits only released specs, approved sources, and candidate work.
- Verify the export's links and checksums in a workspace without analyst files.
- A released spec is authoritative only for its declared scope and version.
- Do not claim that review or an isolated implementation environment exists
  merely because the manifest template includes fields for them.
