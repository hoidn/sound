"""Manifest skeleton, traceability evidence and deny list for the clip-launch-v2 candidate (analyst side)."""
from cases_v2 import PROV_S, PROV_X, R

TARGET = "Ableton Live 12 Suite 12.4.3 (2026-07-07_e3d8be4d07) / macOS arm64"
V1_MANIFEST_SHA = "ecf755b1c4ea2d3356bd31ff3fdc0efc4034b05a6ecb11c08d8502c86d945bea"

SCOPES = {
    "001": "Launch elements of session MIDI and audio clips and arrangement MIDI clips: location, types, reading rules, refusal of refused text and of a repeated launch element, saved form, relative order, and read-back value for Booleans and numbers of at most six significant digits. Saved text not released (unchanged from v1)",
    "002": "Follow-action compound: ten children, types, reading rules; saved with exactly these children in order. Scene compound only as converted by REQ-014 (unchanged)",
    "003": "GlobalQuantisation and AutoQuantisation location, integer type and reading rule. Saved form not released (unchanged)",
    "004": "Launch mode values 0-3 and their labels (unchanged)",
    "005": "Clip launch quantization 0-14 and global quantization 0-13 with labels; clip value k>=1 denotes the setting of global value k-1, clip value 0 the set's global setting; use at launch excluded (unchanged)",
    "006": "Record quantization values 0-8 and their labels; effect on recording excluded (unchanged)",
    "007": "Follow-action values 0-9 and their labels (unchanged)",
    "009": "Initial clip and follow-action values for absent Legato, VelocityAmount, FollowAction or follow-action children; written on save (unchanged)",
    "011": "Out-of-range launch mode, launch quantization or follow-action values of at most nine digits do not refuse the document; chances outside 0-100 within the stated ranges follow REQ-012; a launch quantization of -99 denotes Global in the REQ-016 value; nothing else",
    "012": "Follow-chance rescaling on opening in binary32 arithmetic with halves away from zero, each result limited to 0-100; chances 0-100, or -100 to 200 with |A+B| >= 1; negative zero counts as zero",
    "013": "Follow-time rounding on opening by the binary64 formula, for values 0 to below 1,000,000 (the near-half exclusion of v1 removed)",
    "014": "Conversion steps 406, 417 and 421 for clips of 11.0_405 documents and 12203 for scenes of 12.0_12117 documents, applied before reading; no conversion at 12.0_12402; other conversion steps excluded (unchanged)",
    "015": "Value contract: grid length in beats for a global value q and a time signature n/d (n 1-99, d 1, 2, 4, 8 or 16); 0 means no grid",
    "016": "Value contract: the grid a clip's stored launch quantization denotes, from the clip value (-99 counts as 0), the global value and the clip's and the song's time signatures given as inputs; which global value, time signatures and grid a launch uses, and its use at launch, excluded",
    "017": "Value contract: rounded beat (lattice rounding) and boundary arithmetic for a beat, a grid length and an anchor given as inputs; which beat and anchor a launch uses, whether a launch starts at the boundary, the pre-delay, the move to the next line and all sample timing excluded",
    "018": "Value contract: with no grid the boundary is the rounded beat; launch timing excluded",
}
UNRELEASED = ["008", "010", "019", "020", "021", "022", "023"]

INPUTS_WITHOUT_EXPECTATION = [
    "a clip without LaunchMode or LaunchQuantisation; a LiveSet without GlobalQuantisation or AutoQuantisation",
    "an item of the item table without a Value attribute, with other attributes or with child elements",
    "GlobalQuantisation outside 0-13 and AutoQuantisation outside 0-8",
    "VelocityAmount outside 0-1; jump indices outside -1 to 8,388,608; LoopIterations outside 1 to 1,073,741,823; FollowTime negative or 1,000,000 or more; chances outside 0-100 unless both lie in -100 to 200 and |A+B| >= 1",
    "non-finite values; negative zero except as a follow chance",
    "number text starting (after spaces and sign) with 0x, inf or nan; Invalid; text starting with #; leading whitespace other than U+0020",
    "integer text with spaces both before and after the digits, a plus sign with trailing spaces, any minus sign, or ten or more digits within 63 characters",
    "repeated or unknown children of FollowAction; unknown children or attributes of a clip element",
    "clips other than at the named locations, including take lanes and the groove pool; more than one clip at a named location",
    "in 11.0_405 documents: a clip that already has FollowAction, a clip without FollowActionA, FollowActionB, FollowChanceA or FollowChanceB, or with FollowActionEnabled or IsLinked; scenes other than the fixtures' form (an old scene list item holding only its name)",
    "in 12.0_12117 documents: a scene FollowAction without all ten children",
    "Live Sets that the structure rules refuse (fixtures are complete minimal sets) and documents that break more than one refusal rule",
    "other envelopes, format versions, compressed containers and document kinds",
    "value functions outside their stated argument ranges",
]
EXCLUDED_BEHAVIOR = [
    "launch timing: when a launched clip starts, the sample at which a launch takes effect, which beat, anchor, global value, time signatures and grid a launch uses at run time, whether a launch starts at the boundary of REQ-CLIP-LAUNCH-017, the pre-delay and the move to the next grid line, launching with the transport stopped; these belong to a separate playback release; the value functions of REQ-CLIP-LAUNCH-015 to 018 are not launch timing",
    "Gate, Toggle and Repeat, Legato, velocity scaling, follow-action timing, loop iterations, jump indices and chance selection",
    "displayed text, including where each follow-action label set is shown",
    "value held, displayed or saved for an out-of-range launch mode, launch quantization or follow-action value; for a follow time outside 0 to below 1,000,000, whether the document opens and the value then held",
    "text written for numbers and Booleans, and exact read-back of a written number with more than six significant digits; layout; save container and envelope; saved form of set-level values and of scenes",
    "initial launch mode and quantization of a new clip and the related preferences; set initial values; File > New; clip creation paths",
    "conversion steps other than 406, 417, 421 and 12203; the conversion error for a clip that has both forms; documents older than 11.0_405; the conversion of the fixtures' other content",
    "scripting interface names, properties and value assignment",
    "effect of record quantization; scene follow actions other than their conversion; the key and MIDI assignment of the global quantization",
    "reading of the clip and song time signatures; clips with several time-signature entries",
    "the fixtures' other content (tracks, mixers, notes, sample, automation, scenes); it makes each fixture a valid set and is not judged",
    "editing after opening, undo, refusal text and presentation",
]
CHANGES = [
    "fixtures: all 50 rebuilt as complete minimal Live Sets; v1 fixtures lack the freeze-sequencer slots and other set structure that opening requires (49 of 50 would be refused); every case record and every launch value of the fixtures unchanged",
    "precondition removed: v1's 'absence of other set content must not change a judged outcome' does not hold for set structure",
    "REQ-012: chances outside 0-100 (within -100 to 200, |A+B| >= 1) rescaled and limited to 0-100; v1's kept-value assumption settled; negative zero counts as zero; cases 051-059",
    "REQ-013: stated as the binary64 formula; equals v1's rule outside v1's near-half exclusion, which is removed; cases 060-062",
    "REQ-015 to 018 released as value contracts only (grid length, the grid a clip's setting denotes including -99 as Global, rounded beat and boundary including the triplet next-line case, no grid); not launch timing; cases 063-100",
    "REQ-011: out-of-range chances now have expectations through REQ-012; -99 denotes Global in the REQ-016 value",
    "provenance label extracted execution added with its assumptions; carried records keep static-derived",
]

E = {
    "fields": "S5 static-survey.json field order, homonyms; clip-records.tsv; registry-order-check.txt (as v1)",
    "text": "handoff/transport-state-v1 REQ-003 to 006; N1 text conversion (as v1)",
    "dup": "N1 add-member duplicate refusal (as v1)",
    "enums": "S5 label lists s5-0001, s5-0002 (as v1)",
    "init": "S5 s5-0001 clip and follow-action constructors (as v1)",
    "absent": "generic loader leaves absent members at constructor values (A2; as v1)",
    "enumload": "N1: loader stores the enum index directly (as v1)",
    "postload": "S5 follow-action post-load slot (A3; as v1)",
    "chance": "S5 s5-0003 0x1025044b4; X2 results/follow.json chances (setter limit 0-100, A7 settled); spec r3/r4 REQ-012",
    "chance_range": "spec r3 A2: member load step does not limit out-of-range values (S, both slices); X2 out-of-range chance runs",
    "ftround": "X2 results/follow.json follow_time (flag 1): binary64 formula equals X for 66 of 66; spec REQ-013 r3",
    "migration": "S5 s5-0002 to s5-0004 steps 406, 417, 421, 12203; reviewer review/other-steps.c (as v1)",
    "grid": "X2 results/launch.json grid: 6,463 (n, d, q) equal to the REQ-015 table; static jump table (s5-0001)",
    "clipgrid": "S5 s5-0001 0x102442998 (k != 0: grid(clip signature, k - 1); 0: song grid); research clip-launch.md 'Which grid a clip uses'",
    "getter": "X2 results/launch.json enum_getter: -99 -> 0, others unchanged",
    "boundary": "X2 results/launch.json boundary_cases and gridline_sweep (lattice helper mode 3, boundary helper mode 1)",
    "nogrid": "spec r4 REQ-018 S: lattice helper skips the ceiling when g == 0 (s5-0001; X2 addresses.json role)",
    "structure": "SPEC-LIVE-SET-STRUCTURE r1; r2/t11-structure-v1 make_fixture.py (T11-MIN), schema_check.py, fixture_audit.py, released-fixture-audit.json",
}
EV = {"001": ["fields", "text", "dup"], "002": ["fields", "text"], "003": ["fields", "text"], "004": ["enums"],
      "005": ["enums", "clipgrid"], "006": ["enums"], "007": ["enums"], "009": ["init", "absent"],
      "011": ["enumload", "text", "chance_range", "getter"], "012": ["chance", "chance_range", "postload"],
      "013": ["ftround", "postload"], "014": ["migration"], "015": ["grid"], "016": ["clipgrid", "getter", "grid"],
      "017": ["boundary"], "018": ["nogrid", "boundary"]}
AS = {"009": ["A2"], "011": ["A2"], "012": ["A2", "A3"], "013": ["A2", "A3"], "014": ["A2", "A3", "A5"]}
A = {"A2": "absent items keep initial values; present in-range values (and out-of-range chances until the "
           "correction) kept as read (spec A2, r3 extension). Payload: first assumption bullet.",
     "A3": "opening corrections run for every clip, after conversion (spec A3). Payload: second bullet.",
     "A5": "conversion order (spec A5). Payload: third bullet.",
     "ARM": "arm64 computes as the x86_64 slice (X label). Payload: fourth bullet.",
     "CONV": "conversion of the fixtures' other content from 12.0_12117 and 11.0_405 does not refuse (new; "
             "fixtures now carry a complete set). Payload: fifth bullet."}
NOT_RELEASED = {
    "CLC-013": "REQ-010 unreleased", "CLC-016, CLC-017, CLC-018 (API part)": "scripting interface excluded",
    "CLC-030": "REQ-008 unreleased", "CLC-055": "U (anchor after a time-signature change); its arithmetic is in case 099",
    "CLC-056": "U (stopped launch, REQ-019)",
    "CLC-061": "out-of-range follow time: spec labels X, but its A2 r3 text leaves a later step untraced for it (finding)",
    "CLC-031 to 054, 062 to 064 (timing)": "carried only as beat values; the sample timing belongs to SPEC-PLAYBACK-CORE",
}

DENY_EXTRA = [r"xexec", r"\bgdb\b", r"run_x2", r"harness", r"getter", r"helper", r"\bstub", r"fmaxnm", r"maxsd",
              r"cvttss2si", r"fcvtzs", r"FireManager", r"ClipFire", r"Predelay", r"PlayingBefore", r"SCrossfade",
              r"T11-MIN", r"t11-", r"x2-notes", r"\bX2\b", r"\bT1\.\d", r"\bADR\b", r"LSS-", r"PBC-",
              r"REQ-PLAYBACK", r"REQ-LIVE-SET", r"\bQ-02\d", r"sentinel", r"jump table", r"poke", r"vector",
              r"\bE\d\b", r"\bF\d\b", r"\bRVC-", r"REVIEW\.md"]
PROVENANCE_LABELS = {
    PROV_S: "derived from evidence reviewed before sanitization",
    PROV_X: "the original program's x86_64 build computed the judged values on the case's inputs on a Linux x86_64 host; "
            "these computations call no system library; reading the text, locating, opening, saving and the selection "
            "of a clip's grid remain static-derived (per-computation basis in cases.json)",
}
STATED_ASSUMPTIONS = [
    "An item absent from a clip or follow action keeps its initial value; a present value inside the stated ranges is kept as read apart from the opening corrections, and a chance outside 0 to 100 is kept as read until the follow-chance correction.",
    "The opening corrections run for every clip read from a document, after any conversion.",
    "An older document is converted by every conversion step above its suffix number, in increasing order, before its values are read.",
    "The macOS arm64 build computes the extracted-execution values as the x86_64 build does. Every case with that label depends on it.",
    "Converting the fixtures' other content (tracks, mixers, notes, sample reference, scenes) from 12.0_12117 and 11.0_405 does not refuse the document. Cases CLIP-LAUNCH-041 to 049 depend on it.",
]


def manifest_skeleton(case_count):
    return {
        "schema": "handoff-manifest-v1", "release_id": "clip-launch-v2",
        "release_status": "candidate-unreviewed", "release_date": None, "target": TARGET,
        "specification": {"id": "SPEC-CLIP-LAUNCH", "parent_revision": 4, "release_revision": 4},
        "feature_ids": ["FEAT-SESSION", "FEAT-PERSISTENCE", "FEAT-TRANSPORT"],
        "partial_requirement_scopes": {R + k: v for k, v in SCOPES.items()},
        "unreleased_requirements": [R + k for k in UNRELEASED],
        "compatibility_dimensions": {
            "project-files": "static-derived and extracted-execution expectations for the listed document values; reference execution not-run",
            "behavior": "quantization grid values as a value contract of explicit inputs (extracted execution and static-derived); not launch timing; launching excluded",
            "timing": "excluded (launch timing belongs to a separate playback release)",
            "ui": "excluded (labels define meaning; displayed text not graded)", "audio": "excluded"},
        "expectation_provenance_labels": PROVENANCE_LABELS,
        "stated_assumptions": STATED_ASSUMPTIONS,
        "exclusions": {"inputs_without_expectation": INPUTS_WITHOUT_EXPECTATION, "behavior": EXCLUDED_BEHAVIOR},
        "fixture_origin": "independently authored complete minimal Live Sets (decoded XML) generated from one authored template, and one generated sine-wave sample; no shipped file content",
        "approved_public_sources": [],
        "review": {"status": "pending", "reviewers": [], "date": None, "findings": [], "disposition": None,
                   "record": None},
        "supersedes": "clip-launch-v1",
        "supersession": {
            "relationship": "superset in scope; within clip-launch-v1's clauses both give the same expectations; clip-launch-v1 stays immutable, but its fixtures are not openable Live Sets and must not be used for its 'opens' expectations",
            "superseded_manifest_sha256": V1_MANIFEST_SHA,
            "restated_cases": "CLIP-LAUNCH-001 to 050: case records identical to clip-launch-v1; fixtures rebuilt (see README change list)",
            "changes": CHANGES},
        "entrypoint": "README.md", "case_count": case_count,
        "inventory_excludes": ["manifest.json (self-hash recorded outside package)"],
        "files": [],
    }
