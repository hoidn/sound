# Mix graph, mixer gains and automation playback, release 1

**Reviewed local release.** Read [the contract](spec.md),
[the cases](cases.json), [the role instructions](AGENTS.md),
[the manifest](manifest.json) and [the review disposition](REVIEW.md). The
stated partial scope, with the narrowing recorded in the review, is approved
as a contract for a fresh, restricted implementation workspace. Such a
workspace has not been provisioned by this release.

The finite scope is how the project's offline render of a Live Set turns
per-track signals into the main output: the order of device chain and mixer,
pre- and post-fader sends, summing at return tracks and the main track, the
volume gain and its silence limit, the pan law and pan mode, the track switch,
the main and send gates for each solo category, per-sample ramps and the
75-sample fade length, a settled start, and how an automation envelope's
events become the values it plays under the default automation settings.
Requirement IDs are retained with explicit partial clauses. Requirements 012,
015 and 016 (which envelope drives a parameter, the units of automated values,
automated against manual values) are not released.

The package has 28 cases. The 17 computation cases are labeled extracted
execution (the original program's own x86_64 code computed the values) or
static-derived. The 11 render cases use 11 authored minimal Live Sets and two
generated 64-frame test signals. Their expectations are **composed render
expectations: spec conformance, not measured compatibility**. No render of
the original application exists to compare against. No case is an observed
run of the original application.

The representation is a comparison convention, not an API claimed to exist in
Live and not a required architecture. No compatibility claim is made. No
application source, shipped file, shipped audio or public dependency is
included. After publication the release is immutable; corrections require a
new revision.
