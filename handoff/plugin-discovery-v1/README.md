# Plug-in discovery folders and candidates, release 1

**Reviewed local release.** Read [the contract](spec.md),
[the cases](cases.json), [the role instructions](AGENTS.md),
[the manifest](manifest.json) and [the review disposition](REVIEW.md). The
stated partial scope, with the clarifications recorded in the review, is
approved as a contract for a fresh, restricted implementation workspace.
Such a workspace has not been provisioned by this release.

The finite scope is where the application looks for VST3 and VST2 plug-ins on
macOS, and which entries it examines there: the system folders and the custom
folder of each format and the switches that add them, the VST3 and VST2 rules
for which directories and files are candidates, and the exclusion of `.clap`
bundles. Requirement IDs are retained with explicit partial clauses.
Requirements 003 and 006 to 016 (examination order, what a module contributes,
later scans, progress, failures, scale and duplicates) are not released. No
application source, shipped file, plug-in or public dependency is included.

The package has 35 cases, each with one independently authored scenario
description: switch settings and a tree of empty placeholder directories and
empty files. The expected result of each case is the set of entries examined
for each format. It says nothing about whether a plug-in is then listed.

All expected results are static-derived and unexecuted. They are not captured
reference behavior. The result representation is a comparison convention, not
an API claimed to exist in Live and not a required architecture. No
compatibility claim is made. After publication the release is immutable;
corrections require a new revision.
