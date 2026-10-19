# Playback core: transport, launch timing and clip playback, release 1

**Unreviewed candidate.** Read [the contract](spec.md), [the cases](cases.json),
[the role instructions](AGENTS.md) and [the manifest](manifest.json). The
partial scope stated there is proposed for review. It is not approved, and no
implementation workspace has been provisioned.

The finite scope is an offline render of a Live Set's session at a stated
sample rate, driven by a script of transport and launch actions on stated
render samples, up to the point where a track's clip output enters its device
chain:

- the song clock: beats to render samples, Play from a stated start beat, Stop,
  Continue and the song loop;
- the render sample on which a clip launched with its launch button starts, in
  Trigger mode, under each global launch quantization value and with the
  clip's own setting;
- the note-on and note-off events a MIDI clip sends, with their velocities and
  render samples;
- the file positions and values an audio clip with warping off produces, by
  direct copy or linear interpolation, with its gain.

Requirement IDs are retained with explicit partial clauses. Requirements 016
and 021 to 023 are not released. No application source, shipped file or public
dependency is included.

The package has 92 cases on 58 generated Live Sets and two generated 16-bit
WAV files. Where the original's result can fall on either of two adjacent
render samples, a case lists both and accepts either. Expected results carry
one of two provenance labels: extracted-execution arithmetic (the original
x86_64 code run on stated inputs, with a static-derived path) or
static-derived. None is a captured run of the application, and the comparison
representation is a convention, not an API claimed to exist in Live or a
required architecture. No compatibility claim is made. After publication the
release is immutable; corrections require a new revision.
