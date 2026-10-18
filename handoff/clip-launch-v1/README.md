# Clip launch settings in Live Set documents, release 1

**Reviewed local release.** Read [the contract](spec.md), [the cases](cases.json),
[the role instructions](AGENTS.md), [the manifest](manifest.json) and
[the review disposition](REVIEW.md). The stated partial scope, narrowed as
recorded in the review, is approved as a contract for a fresh, restricted
implementation workspace. Such a workspace has not been provisioned by this
release.

The finite scope is how the decoded XML of a Live Set stores each clip's launch
settings and the set's global and record quantization: where each value is,
what each value means and how it is labeled, which text is accepted or refused
when a document is opened, what missing and repeated items do, the
follow-chance and follow-time corrections made on opening, the conversion of
follow actions in two older format versions, and what is written on save.
Requirement IDs are retained with explicit partial clauses. Requirements 008,
010 and 015 to 023, and every effect on launching or playback, remain
unreleased. No application source, shipped file or public dependency is
included.

The 50 cases use independently authored minimal XML fixtures. All expected
outputs are static-derived and unexecuted, not captured reference behavior.
The representation is a comparison convention, not an API claimed to exist in
Live or a required architecture. No compatibility claim is made. After
publication the release is immutable; corrections require a new revision.
