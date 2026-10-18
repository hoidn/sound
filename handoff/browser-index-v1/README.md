# Browser content kinds and tag sidecars, release 1

**Reviewed local release.** Read [the contract](spec.md),
[the cases](cases.json), [the role instructions](AGENTS.md),
[the manifest](manifest.json) and [the review disposition](REVIEW.md). The
stated partial scope, narrowed as recorded in the review, is approved as a
contract for a fresh, restricted implementation workspace. Such a workspace
has not been provisioned by this release.

The finite scope is the content kind that a file's extension gives it in the
browser, and the tag sidecar file of a user folder: which sidecar files are
read, the sidecar form covered, how entries bind to the files directly inside
the folder, how tags and color labels are read, and the name, location and
content of the sidecar written when the user tags an item. It also gives the
file names of the sidecars that record the user's tags for the Core Library
and for built-in content. Requirement IDs are retained with explicit partial
clauses. Requirements 002 and 009 to 013 (indexed locations, previews, changes
on disk, unsupported files and the index itself) are not released. No
application source, shipped file or public dependency is included.

The package has 26 cases. Eleven classify file names and need no fixture
files. Ten read a user folder, three write a user folder's sidecar, and two
concern the user's tags for factory and built-in content. Each folder case
has its own independently authored folder. The identifiers BROWSER-INDEX-016
and 017 are not used.

All expected results are static-derived and unexecuted. They are not captured
reference behavior. The result representation is a comparison convention, not
an API claimed to exist in Live and not a required architecture. Whether and
when files are listed, and when a sidecar is written, are outside this
release. No compatibility claim is made. After publication the release is
immutable; corrections require a new revision.
