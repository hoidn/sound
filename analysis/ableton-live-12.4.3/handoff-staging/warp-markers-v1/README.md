# Warp markers and warp settings, release 1

**Reviewed local release.** Read [the contract](spec.md),
[the cases](cases.json), [the role instructions](AGENTS.md),
[the manifest](manifest.json) and [the review disposition](REVIEW.md). The
stated partial scope, narrowed as recorded in the review, is approved as a
contract for a fresh, restricted implementation workspace. Such a workspace
has not been provisioned by this release.

The finite scope is how a decoded Live Set stores the warp markers and warp
settings of an audio clip, and the marker list of a Simpler sample: where they
are, how their text is read when a document is opened, the defaults of absent
settings, the stored codes, and which edits of warp markers
through the scripting interface are refused or accepted. Requirement IDs are
retained with explicit partial clauses. Requirements 005, 006, 009 and 014 are
not released. Nothing that is saved, played or heard is graded, and no
conversion value between sample time and beat time is released.

The package has 38 cases over 18 authored XML documents and one generated WAV
file of three seconds of silence.

All expected outcomes are static-derived and unexecuted. They are not captured
reference behavior. The outcome representation is a comparison convention, not
an API claimed to exist in Live and not a required architecture. No
compatibility claim is made. After publication the release is immutable;
corrections require a new revision.
