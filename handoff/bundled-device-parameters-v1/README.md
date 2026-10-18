# Device parameters in device presets, release 1

**Reviewed local release.** Read [the contract](spec.md),
[the cases](cases.json), [the role instructions](AGENTS.md),
[the manifest](manifest.json) and [the review disposition](REVIEW.md). The
stated partial scope, narrowed as recorded in the review, is approved as a
contract for a fresh, restricted implementation workspace. Such a workspace
has not been provisioned by this release.

The finite scope is how the decoded XML of a device preset of one document
format version stores seven devices that come with Live: Amp, Cabinet, Analog,
Tension, Collision, Electric and Corpus. It covers the element that stores each
device, the members of the device element in order, the shape of each
parameter element, each parameter's path, kind and value range, which value
text is accepted or refused when a preset is opened and the value then read,
what duplicated and unknown elements do, and the labels shown for seven
parameters. Requirement IDs are retained with explicit partial clauses.
Requirements 005, 008, 009, 010, 013 and 015 are not released: what is written
on save, the values of missing parameters and of newly inserted devices,
out-of-range values, rack macro bindings and the values and meaning of
position parameters. No application source, shipped file or public dependency
is included.

The package has 82 cases, each with one independently authored fixture written
from the parameter tables. All expected results are documented or
static-derived and unexecuted. They are not captured reference behavior. The
representation is a comparison convention, not an API claimed to exist in Live
and not a required architecture. No compatibility claim is made. After
publication the release is immutable; corrections require a new revision.
