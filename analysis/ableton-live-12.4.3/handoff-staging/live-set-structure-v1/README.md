# Live Set structure, release 1

**Reviewed local release.** Read [the contract](spec.md),
[the cases](cases.json), [the role instructions](AGENTS.md),
[the manifest](manifest.json) and [the review disposition](REVIEW.md). The
stated partial scope, with the narrowing recorded in the review, is approved
as a contract for a fresh, restricted implementation workspace. Such a
workspace has not been provisioned by this release.

The finite scope is the structure of a Live Set document once its envelope is
accepted: which elements a set holds and where; when a set is refused because
of its track list, its slot lists, its send holders, its target Ids,
`NextPointeeId` or its list-item Ids; which defects are repaired while the set
opens; how a sample reference names and finds its file, and the size and
checksum values that identify the file; and the reference minimal set T11-MIN
with the status of each of its elements. Requirement IDs are retained with
explicit partial clauses. Requirements 011, 012 and 017 (what a save writes,
and where devices may be placed) are not released. No application source,
shipped file or public dependency is included.

The package has 34 cases. Their inputs are the generated minimal set T11-MIN,
whose device lists are empty,
30 variants of it that each make one stated change, and one generated sine-tone
sample. Two stated assumptions support four of the expectations; the contract
names them, and each case lists those it needs.

All expected outcomes are documented, static-derived or, for one checksum,
taken from extracted execution of the original's own routine. None is a
captured run of the original application. The outcome representation is a
comparison convention, not an API claimed to exist in Live and not a required
architecture. No compatibility claim is made. After publication the release is
immutable; corrections require a new revision.
