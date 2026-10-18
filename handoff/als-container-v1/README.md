# Live Set container and version envelope, release 1

**Reviewed local release.** Read [the contract](spec.md),
[the cases](cases.json), [the role instructions](AGENTS.md),
[the manifest](manifest.json) and [the review disposition](REVIEW.md). The
stated partial scope, narrowed as recorded in the review, is approved as a
contract for a fresh, restricted implementation workspace. Such a workspace
has not been provisioned by this release.

The finite scope is the outer layer of a Live Set file: how its first bytes
select a gzip or uncompressed XML container, the root element, the presence,
syntax and range of the version attributes, refusal of documents from a newer
version, the MinorVersion schema check, and the optional and ignored root
attributes. Requirement IDs are retained with explicit partial clauses.
Requirements 007 to 009 (what is written on save, and how a refusal is
presented) are not released. No application source, shipped file or public
dependency is included.

The package has 35 cases, each with one independently authored fixture. An
accepted case means that the envelope rules in this release do not refuse the
file. It does not mean that the set opens.

All expected outcomes are static-derived and unexecuted. They are not captured
reference behavior. The outcome representation is a comparison convention, not
an API claimed to exist in Live and not a required architecture. No
compatibility claim is made. After publication the release is immutable;
corrections require a new revision.
