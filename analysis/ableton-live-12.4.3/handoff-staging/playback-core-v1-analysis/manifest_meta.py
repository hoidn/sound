"""Draft manifest metadata of the playback-core-v1 candidate (scope, exclusions, assumptions); text only.
Must agree with ../playback-core-v1/spec.md; seal_playback.py checks the requirement lists against it."""

P = "REQ-PLAYBACK-CORE-"
SCOPES = {
    P + "001": "Song clock: samples per beat (SR / T) x 60 and beats per sample in binary64; song beat at render sample n "
               "from the anchor; anchors at Play, Continue and song-loop jumps; results independent of buffer size",
    P + "002": "Placement of a beat event on render sample P(b), or on P(b) or P(b) + 1 where the exact position is an "
               "integer and the binary64 product exceeds it; at one beat, note-off before a clip's loop wrap before note-on",
    P + "003": "The song tempo is used as its binary32 value (tempos 90 to 140 BPM in the cases)",
    P + "004": "Play from stopped with a stated start beat: rounded to the lattice, a negative value raised to 0, the "
               "start beat plays on render sample 0",
    P + "005": "Stop holds the song beat of its request sample; Continue resumes from it with a new anchor",
    P + "006": "Song loop: length used as at least 1 beat; jump to the loop start where the song beat reaches the loop "
               "end, placed by the placement rule, with a new anchor; no jump when Play starts at or after the loop "
               "end; a playing session clip is not moved by a jump",
    P + "007": "Launch-button press: a quantized launch with no explicit time and fire velocity 1; grid from the clip's "
               "own value (2 to 14, clip signature), Global (the set's global value, song signature) or None; grid "
               "lengths of global values 1 to 13",
    P + "008": "Press beat; launch boundary B by the stated arithmetic; pre-delay 0 on a MIDI track and on an audio "
               "track with no clip playing",
    P + "009": "With pre-delay 0 the launch takes effect at B and the clip's start plays at B",
    P + "010": "No grid: the clip's start is the lattice-rounded press beat; launch while stopped with start beat 0 "
               "starts the transport and the clip on render sample 0",
    P + "011": "Warped session MIDI clip: start, loop start and end, loop switch; clip time; passes; song beat of each "
               "note in each pass; end of an unlooped clip",
    P + "012": "Note-on at Time with its Velocity unrounded; note-off at the rounded Time + Duration with OffVelocity; "
               "zero-length notes; disabled notes not sent",
    P + "013": "A note starts only inside a pass; a note under way at the clip's start is not started; a note-on at the "
               "loop end never plays; a note-off at the loop end is sent with its own velocity before the wrap",
    P + "014": "With loop start 0, a note held across the loop end is cut at the wrap with velocity 64; a note sounding "
               "at an unlooped clip's end gets velocity 64 there",
    P + "015": "With VelocityAmount 0, VelocityDeviation 0, Probability 1 and no groove, the stored velocity is sent "
               "unchanged, at the stored times, and every enabled note plays",
    P + "017": "Unwarped session audio clip: region in seconds; transposition; read step in 32.32 fixed point; first "
               "frame from LoopStart with fraction 0; output k reads first frame + k x step; output 0 on the launch sample",
    P + "018": "Direct copy for a step of exactly 1 whatever HiQ says; linear interpolation in binary32 with HiQ off",
    P + "019": "SampleVolume gain and its limits; a mono file on both channels; 16-bit PCM frames as int16 / 32768",
    P + "020": "Fade off: no fade; past the file's last frame the output is silence",
}
UNRELEASED = [P + "016", P + "021", P + "022", P + "023"]
ASSUMPTIONS = {
    "AS-1": "The macOS arm64 build follows the rules that were run on, or derived only from, the x86_64 build: the "
            "clock and launch arithmetic, the note order at one beat, the song beat of a note in a clip's first pass, "
            "which notes start or are cut in a pass, the note velocity path, the read step, the interpolation kernels "
            "(within the linear tolerance) and silence past the file's end.",
    "AS-2": "An audio clip's stored IsWarped, HiQ, Fade, SampleVolume, PitchCoarse and PitchFine are the values its "
            "playback uses, and a session clip never starts in a crossfade.",
    "AS-3": "While a set is open, the global launch quantization in effect is the stored GlobalQuantisation.",
    "AS-4": "In a set whose time signature never changes, launch grid lines lie at whole multiples of the grid "
            "length from song beat 0.",
    "AS-5": "For a transposition other than 0 and for the clip gain, the macOS C library gives the binary32 power and "
            "the decibel-to-gain values that the x86_64 runs got from glibc: the step and gain values stated in the "
            "cases.",
}
EXCLUSIONS = {  # the same items as spec.md "Excluded behavior and inputs"
    "unreleased_requirements": {
        P + "016": "per-note expression",
        P + "021": "an unwarped clip's end sample and its independence of tempo (with Fade false its end is not "
                   "visible in the clip signal)",
        P + "022": "clip stop buttons, Stop All Clips, empty-slot presses and quantized stops",
        P + "023": "clips after a transport Stop and a new Play"},
    "without_expectation": [
        "which start beat the original's own Play control uses after opening, what its transport controls do, and "
        "which gestures other than the launch button reach the launch path",
        "which of P(b) and P(b) + 1 occurs where both are listed",
        "tempo changes; the tempo limits; a second Stop; Play after Stop; Stop or Continue while a clip plays",
        "the song loop switched or changed during playback; a loop start below 0; a launch whose boundary is at or "
        "after the loop end; any event on the beat of a jump; a launch on the beat of a note event",
        "the launch sample and the audio during a crossfade between audio clips (pre-delay above 0); a launch on a "
        "track whose clip is playing",
        "note chasing; extra messages at a transport Stop; retriggered notes; the cut velocity when the loop does not "
        "start at 0",
        "notes overlapping another note of the same key, two notes at one time on a key, a zero-length note followed "
        "by a note at the same time, and probability groups; VelocityAmount, VelocityDeviation or Probability other "
        "than 0, 0 and 1; MIDI clips with IsWarped false",
        "LaunchQuantisation outside 0 to 14 and GlobalQuantisation outside 0 to 13; launch modes other than Trigger; "
        "legato",
        "audio clips with Fade true, HiQ true with a step other than exactly 1, StartRelative other than 0, LoopOn "
        "true, warping on, PitchFine other than 0 or a transposition other than 0 and 12; files other than 16-bit PCM "
        "mono WAV; a region shorter than the frames that remain after the first frame; fade values; the interpolated "
        "outputs next to the file's last frame",
        "set content other than the fixtures' form (spec.md preconditions): more than one track, scene or clip, "
        "devices, return or group tracks, automation beyond the one-event tempo and time-signature envelopes, "
        "enabled follow actions",
    ],
}
TOLERANCE = {
    "timing": "exact render sample, or either of two listed samples (REQ-PLAYBACK-CORE-002)",
    "direct_copy": "bit-exact",
    "gain": "relative 2.4e-7 (gain within 1.2e-7 relative plus one binary32 rounding)",
    "linear": "absolute per window: 2 binary32 units in the last place of the largest frame magnitude that the "
              "window reads",
    "velocity": "exact binary32",
}


def manifest_meta(n):
    return {
        "schema": "handoff-manifest-v1", "release_id": "playback-core-v1", "release_status": "candidate-unreviewed",
        "release_date": None,
        "target": "Ableton Live 12 Suite 12.4.3 (2026-07-07_e3d8be4d07) / macOS (arm64 and x86_64 builds)",
        "specification": {"id": "SPEC-PLAYBACK-CORE", "parent_revision": 1, "release_revision": 1},
        "feature_ids": ["FEAT-TRANSPORT", "FEAT-SESSION", "FEAT-MIDI", "FEAT-AUDIO"],
        "partial_requirement_scopes": SCOPES, "unreleased_requirements": UNRELEASED,
        "compatibility_dimensions": {
            "timing": "render sample of note events, launches and audio clip starts; extracted-execution arithmetic "
                      "and static-derived expectations; reference execution not-run",
            "audio": "unwarped clip signal before devices and mixer: direct copy, linear interpolation and gain; "
                     "reference execution not-run",
            "behavior": "transport, launch and note emission as listed; everything else excluded",
            "project-files": "the fixtures must open; values after opening and saving not graded",
            "ui": "excluded", "mix": "excluded", "devices": "excluded"},
        "expectation_provenance_labels": {
            "extracted-execution arithmetic (x86_64 build, glibc in place of the macOS libraries); arm64 equivalence "
            "inferred; playback path static-derived; not observed reference output":
                "the arithmetic that gives each listed sample or value (clock, placement, Stop and Continue, song "
                "loop, launch boundary, clip position, note events, read step, kernels, gain) equals the original "
                "x86_64 code's results on the runs made; that playback reaches it with the case's values is "
                "static-derived",
            "static-derived; not observed reference output": "derived from static evidence about the pinned build"},
        "stated_assumptions": ASSUMPTIONS, "exclusions": EXCLUSIONS, "value_tolerance": TOLERANCE,
        "render_conventions": [
            "render sample 0 is the first sample after the script's first Play, or its first launch while stopped",
            "each action is handled at its stated render sample; actions at one sample in script order",
            "a render starts from a settled state: every ramp the loaded state starts has finished before render "
            "sample 0",
            "these conventions define the test vehicle; they describe no behavior of the original"],
        "fixture_origin": "independently generated minimal Live Sets (one track, one scene, one clip) and two generated "
                          "16-bit mono WAV files; no shipped file, schema content or program code",
        "approved_public_sources": [],
        "review": {"status": "pending", "reviewers": [], "date": None, "findings": [], "disposition": None,
                   "record": None},
        "supersedes": None, "entrypoint": "README.md", "case_count": n,
        "inventory_excludes": ["manifest.json (self-hash recorded outside package)"], "files": []}
