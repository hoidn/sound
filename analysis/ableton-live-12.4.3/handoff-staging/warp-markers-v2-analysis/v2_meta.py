"""Analyst-only tables for build_v2.py and check_v2.py: evidence locators, inferred links, case and clause
traceability, the payload deny-list, the draft manifest and the evidence re-hash. Never shipped.
Every locator below was re-read on 2026-10-18 by the author of warp-markers-v2."""
import hashlib, json

R2 = "analysis/ableton-live-12.4.3/r2/"
S8, D7, N1 = R2 + "s8-warp-v1/", R2 + "d7-warp-v1/", R2 + "n1-transport-state-v1/results/"
X2, T11, T13 = R2 + "x2-envelope-warp-v1/", R2 + "t11-structure-v1/", R2 + "t13-playback-v1/"
V1A = "analysis/ableton-live-12.4.3/handoff-staging/warp-markers-v1-analysis/"
V1 = "handoff/warp-markers-v1/"
V1_MANIFEST_SHA = "f8546a3e95788074a2cf1cd99564637b8689af853db705fd9beba1af1764ef46"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def _run(root, rel):  # re-hash one retained run against its manifest (two manifest shapes exist)
    d = root / rel
    man = json.loads((d / "manifest.json").read_text())
    files = {k: (v["sha256"] if isinstance(v, dict) else v) for k, v in man["files"].items()}
    bad = [k for k, v in files.items() if not (d / k).is_file() or sha((d / k).read_bytes()) != v]
    return {"manifest_sha256": sha((d / "manifest.json").read_bytes()), "files": len(files), "mismatches": bad}


def evidence_identity(root):
    out = {rel.split("/")[-2]: _run(root, rel) for rel in (S8, D7, X2, T11, T13)}
    s8 = json.loads((root / S8 / "manifest.json").read_text())
    out["arm64_image_matches"] = sha((root / S8 / s8["binary"]["path"]).resolve().read_bytes()) == s8["binary"]["sha256"]
    out["v1_release_manifest_matches"] = sha((root / V1 / "manifest.json").read_bytes()) == V1_MANIFEST_SHA
    out["v1_review_checks_sha256"] = sha((root / V1A / "review/review-checks.txt").read_bytes())
    return out


E = {
    # carried from warp-markers-v1 (wm_meta.py), d7 now cited from its retained run
    "schema": S8 + "static-survey.json schema part (12.0_12402: AudioClip and SampleWarpProperties members, WarpMarker "
                   "attributes; FluctuationTexture present, no FluxTexture)",
    "shipped": S8 + "static-survey.json documents part: distributions, number_text_rule 44,058, *strictly_increasing "
                    "2,878 + 7,372, beat_on_1/3843840_grid 22,029, SampleWarpProperties count=0 4,244, last-step 1/32",
    "markerreg": S8 + "results/s8-0001/functions/0x10260fdd8.* (mSecTime +0x50, mBeatTime +0x58, attribute flag)",
    "getters64": D7 + "results/d7-0002/functions/0x102610264.*, 0x10261026c.* (64-bit Sec/Beat getters)",
    "loader": N1 + "n1-0008/functions/0x101487310.* (generic loader: present members only, direct store); "
                   + N1 + "n1-0006/functions/0x10152bfb8.* (text conversion; no-consumption throw)",
    "ctor": S8 + "results/s8-0001/functions/0x1027b0e40.* (enum inits 6 and 2; float parameter triples); "
                 + S8 + "getter-constants.txt; ComplexProEnvelope 128 (spec appendix)",
    "swppostload": S8 + "results/s8-0002/functions/0x10288538c.* (sample-part post-load: no empty test)",
    "shadow": S8 + "results/s8-0001/functions/0x1026102c0.* (is-shadow: the list's last element)",
    "convert": D7 + "results/d7-0001/functions/0x1033bf160.c, 0x1033bf250.c (audio-clip and warped tests before any "
                    "table use; t / rate; tail call to the clip conversion slot)",
    "builder": D7 + "results/d7-0001/functions/0x1028939a4.*, 0x102893b1c.*, 0x10277b71c.* (table built once on first "
                    "use, in list order, BeatTime array and SecTime array)",
    "rate": "corpus 0x1027b7514 (pseudocode: the divisor of sample_to_beat_time is the clip's sample rate)",
    "add": S8 + "results/s8-0001/functions/0x1033bf42c.c (class and warped tests; 0 <= p <= length, NaN refused; scan "
                "by SecTime with the shadow as last position; left check skipped for the first node; right check "
                "skipped for the shadow; q() block; bounds per neighbour; insert) re-read 2026-10-18",
    "bounds": S8 + "results/s8-0002/functions/0x1027afd40.* (bounds per neighbour; only caller the add)",
    "remove": S8 + "results/s8-0002/functions/0x1033bfa68.c (class test only; lookup; shadow and no-such-marker "
                   "refusals; delete) re-read 2026-10-18",
    "move": S8 + "results/s8-0003/functions/0x1033bfb94.c (class test only; lookup; shadow and no-such-marker refusals "
                 "before the untraced limits routine) re-read 2026-10-18",
    "lookup": V1A + "review/corpus-excerpts.jsonl record 0x1027c79d0 (pseudocode: q() of the argument, scan in list "
                    "order, first equal beat, stop once a beat exceeds it) re-read 2026-10-18",
    "insertdelete": V1A + "review/corpus-excerpts.jsonl records 0x1027baad8 (insert returns on an equal SecTime or "
                          "BeatTime) and 0x1027c6eec (delete returns below three markers; no throw) re-read 2026-10-18",
    "q": S8 + "results/s8-0001/functions/0x1033bf42c.c q() block; results/s8-0003/functions/0x1026101b4.* (beat setter)",
    "codes": S8 + "results/s8-0002/functions/0x1026a9ef8.*, 0x1027b279c.*, 0x1027b29e8.*; vtable-reads.txt",
    "length": "corpus 0x1027b6954 (sample length through the clip's sample object; source untraced)",
    # review of warp-markers-v1 (retained record)
    "review-a2": V1A + "review/review-checks.txt section 5 (a): static check of the read and of the completion steps "
                       "of clip, markers and sample part (no marker or value write); remainder untraced (RVW-01)",
    "review-015": V1A + "review/review-checks.txt section 5 (c): first node has no left check, inclusive bounds, NaN "
                        "refused, insert and delete early returns (F4), move has only the class test (F5)",
    "warpedtest": V1A + "review/review-checks.txt section 5, 'I7 confirmed' (RVW-06): the warped test reads the member "
                        "registered for IsWarped",
    # extracted execution X2 (x86_64 slice 1bae9a97...be999b0)
    "x2conv": X2 + "results/envelope-warp.json warp_WMK016_M1 and warp_WMK017_M2 (conversion cores on the M1 and M2 "
                   "tables; inputs in seconds = frames / 48,000; raw/runs.jsonl labels M1, M2)",
    "x2q": X2 + "results/envelope-warp.json warp_edges_REQ015_016.beat_grid_round (label beat-grid-q)",
    "x2bounds": X2 + "results/envelope-warp.json warp_edges_REQ015_016.add_bounds_lo_hi (label add-bounds-monotone)",
    "x2rules": X2 + "check_rules.py (q, bounds and conversion sequences; 'mismatches: none' re-run 2026-10-18)",
    "x2shadow": X2 + "results/envelope-warp.json warp_REQ007_shadow_* (append routine; operands untraced; no case)",
    # playback (REQ-009, statement only) and structure (fixture validity)
    "t13unwarped": T13 + "audio/match-x86.txt lines 1-4 and 94-98 (unwarped warper functions; marker-list conversion "
                         "callers); wiki/research/playback-core.md; SPEC-PLAYBACK-CORE r1 REQ-017; SPEC-WARP-MARKERS r4 "
                         "REQ-009 'warping off'",
    "t11min": T11 + "make_fixture.py (T11-MIN generator, imported unchanged), schema_check.py and fixture_audit.py "
                    "(run on every fixture); SPEC-LIVE-SET-STRUCTURE r1 REQ-002, 006, 013, 015, 016, 018",
}

I = {
    "I1": "SecTime and BeatTime are binary64 members read by the 64-bit branch of the text conversion (spec: 'Double "
          "branch assumed'; review RVW-07 accepted).",
    "I2": "A conversion error while a nested value is read stops the open (as the transport-state-v1 refusals).",
    "I3": "Opening leaves markers and settings as the document gives them (spec A2): the read and the completion steps "
          "were checked statically (review RVW-01); two onset helpers, five indirect calls and the auto-warp trigger "
          "were not traced. Later self-made changes are excluded; cases 001 and 002 are controls.",
    "I4": "The sample length used by add_warp_marker is the duration in seconds of the clip's sample (0x1027b6954 "
          "source untraced). Cases keep at least 0.5 s from the 3 s length; case 024 holds in s, ms or frames.",
    "I5": "After its checks pass, an add or remove raises no further error (insert and delete pseudocode contain no "
          "throw; callees untraced).",
    "I6": "The marker lookup behaves as its corpus pseudocode reads (not dossier-confirmed).",
    "I8": "The conversions divide and multiply by the sample rate of the clip's sample (divisor source pseudocode).",
    "I9": "The macOS arm64 build computes the conversion, the rounding and the bounds as the x86_64 slice did (spec: "
          "same operation order; arm64 fmsub/fmadd and x86_64 glibc fma are both single-rounding).",
    "I10": "The first conversion call after opening uses the marker list held after opening (spec A3: the table is "
           "built once on first use; a build before the call would use the same list).",
}

L = ["loader", "markerreg", "getters64"]
# release case -> (SPEC-WARP-MARKERS r4 source, evidence keys, inferred links); 001-038 carried from v1
TRACE = {
    1: ("WMK-001/002 load part (v1 case 001; control)", ["schema", *L, "codes", "ctor", "t11min"], ["I1", "I3"]),
    2: ("REQ-001 IsWarped (v1 case 002; control)", ["schema", "loader", "t11min"], ["I3"]),
    3: ("WMK-004 load part", [*L, "t11min"], ["I1", "I3"]),
    4: ("REQ-002 leading U+0020", [*L, "t11min"], ["I1", "I3"]),
    5: ("WMK-003 load part", [*L, "q", "t11min"], ["I1", "I3"]),
    6: ("REQ-002 trailing text", [*L, "t11min"], ["I1", "I3"]),
    7: ("WMK-005 (now isolates the text refusal)", [*L, "t11min"], ["I1", "I2"]),
    8: ("REQ-002 empty text (now isolates the text refusal)", [*L, "t11min"], ["I1", "I2"]),
    9: ("WMK-021 load part, TransientEnvelope kept", ["ctor", "loader", "t11min"], ["I3"]),
    10: ("REQ-010 value-less elements (UserFloat/RemoteableEnum compounds: no Value member, loader skips)",
         ["ctor", "loader", "schema", "t11min"], ["I3"]),
    11: ("REQ-012 TransientResolution 0", ["codes", "loader", "t11min"], ["I3"]),
    12: ("REQ-012 TransientLoopMode 0", ["codes", "loader", "t11min"], ["I3"]),
    **{n: (f"WMK-023 code {c}, load part", ["codes", "loader", "shipped", "t11min"], ["I3"])
       for n, c in zip(range(13, 18), (0, 1, 2, 3, 6))},
    19: ("WMK-020 first call", ["convert", "warpedtest", "t11min"], ["I3"]),
    20: ("WMK-020 second call", ["convert", "warpedtest", "t11min"], ["I3"]),
    21: ("WMK-028 on the three-marker list", ["add", "warpedtest", "t11min"], ["I3"]),
    22: ("REQ-015 accepted counterpart of 021", ["add", "bounds", "q", "insertdelete", "length", "x2rules", "t11min"],
         ["I3", "I4", "I5"]),
    23: ("WMK-029 first call", ["add", "t11min"], ["I3"]),
    24: ("WMK-029 second call (900,000 s)", ["add", "length", "t11min"], ["I4"]),
    25: ("WMK-030", ["add", "shadow", "t11min"], ["I3"]),
    26: ("REQ-015 'q as given'", ["add", "q", "x2rules", "t11min"], ["I3"]),
    27: ("WMK-031", ["add", "shadow", "t11min"], ["I3"]),
    28: ("WMK-032 first call", ["add", "q", "bounds", "x2rules", "t11min"], ["I3"]),
    29: ("WMK-032 second call", ["add", "q", "bounds", "x2rules", "t11min"], ["I3"]),
    30: ("REQ-015 upper limit", ["add", "bounds", "x2rules", "t11min"], ["I3"]),
    31: ("WMK-033", ["add", "q", "bounds", "insertdelete", "length", "x2bounds", "t11min"], ["I3", "I4", "I5"]),
    32: ("WMK-034", ["add", "bounds", "shadow", "insertdelete", "length", "x2rules", "t11min"], ["I3", "I4", "I5"]),
    33: ("WMK-015 first call on the three-marker list", ["remove", "lookup", "shadow", "t11min"], ["I3", "I6"]),
    34: ("WMK-015 second call on the three-marker list", ["move", "lookup", "shadow", "t11min"], ["I3", "I6"]),
    35: ("WMK-035 first call (q(2.0000001) = 2 also run by X2)", ["remove", "lookup", "q", "x2q", "insertdelete",
                                                                  "t11min"], ["I3", "I5", "I6"]),
    36: ("WMK-035 second call (q(2.001) also run by X2)", ["remove", "lookup", "q", "x2q", "t11min"], ["I3", "I6"]),
    37: ("REQ-015 move without a match", ["move", "lookup", "q", "t11min"], ["I3", "I6"]),
    38: ("WMK-036 first call (remove without the warped condition)", ["remove", "lookup", "insertdelete", "t11min"],
         ["I3", "I5", "I6"]),
    # new in v2
    **{n: (f"WMK-016 t = {t} at 48 kHz (here {t // 6} frames at 8 kHz; the same seconds)",
           ["convert", "builder", "rate", "x2conv", "t11min"], ["I3", "I8", "I9", "I10"])
       for n, t in zip(range(39, 46), (-24000, 24000, 48000, 72000, 96000, 120000, 2400000))},
    46: ("WMK-017 t = 0", ["convert", "builder", "rate", "x2conv", "t11min"], ["I3", "I8", "I9", "I10"]),
    47: ("WMK-017 t = 12000 at 48 kHz (2000 at 8 kHz)", ["convert", "builder", "rate", "x2conv", "t11min"],
         ["I3", "I8", "I9", "I10"]),
    **{n: (f"WMK-018 b = {b}", ["convert", "builder", "rate", "x2conv", "t11min"], ["I3", "I8", "I9", "I10"])
       for n, b in zip(range(48, 51), (0.5, 2.5, 4))},
    51: ("WMK-019 (not run by X2: computed with the X-confirmed sequence)", ["convert", "builder", "rate", "x2rules",
                                                                           "t11min"], ["I3", "I8", "I9", "I10"]),
    52: ("WMK-037 first call (q and both bounds run by X2)", ["add", "x2q", "x2bounds", "insertdelete", "length",
                                                              "t11min"], ["I3", "I4", "I5", "I9"]),
    53: ("WMK-037 second call (q not run; bounds run)", ["add", "x2bounds", "x2rules", "t11min"], ["I3", "I9"]),
    54: ("WMK-038 first call (computed)", ["add", "x2rules", "insertdelete", "length", "t11min"],
         ["I3", "I4", "I5", "I9"]),
    55: ("WMK-038 second call (computed)", ["add", "x2rules", "t11min"], ["I3", "I9"]),
    56: ("WMK-039 first call (q run by X2)", ["remove", "lookup", "x2q", "t11min"], ["I3", "I6", "I9"]),
    57: ("REQ-016 X clause: one unit below the halfway point still rounds up (q run by X2); new",
         ["remove", "lookup", "x2q", "t11min"], ["I3", "I6", "I9"]),
    58: ("WMK-039 second call (computed)", ["remove", "lookup", "x2rules", "insertdelete", "t11min"],
         ["I3", "I5", "I6", "I9"]),
    59: ("REQ-015 zero distance, q' = b (left bounds run by X2); new", ["add", "review-015", "x2bounds", "x2rules",
                                                                       "insertdelete", "length", "t11min"],
         ["I3", "I4", "I5", "I9"]),
    60: ("REQ-015 zero distance, q' != b (left bounds run by X2); new", ["add", "review-015", "x2bounds", "x2rules",
                                                                        "t11min"], ["I3", "I9"]),
    61: ("REQ-015 no left neighbour before the first marker; new", ["add", "review-015", "x2rules", "insertdelete",
                                                                   "length", "t11min"], ["I3", "I4", "I5"]),
    62: ("WMK-036 second call (move has no warped check)", ["move", "review-015", "lookup", "t11min"], ["I3", "I6"]),
    63: ("REQ-015 remove on a two-marker list accepted (revision 2 example)", ["remove", "lookup", "insertdelete",
                                                                             "review-015", "t11min"],
         ["I3", "I5", "I6"]),
    64: ("WMK-014 load part, re-authored on the three-marker list (shadow 1/16 beat after)",
         [*L, "shadow", "review-a2", "shipped", "t11min"], ["I1", "I3"]),
}

# release clause -> (summary, support, evidence keys, inferred links)
CLAUSES = {
    "001.1": ("AudioClip warp children and empty single-Value form", "D", ["schema", "shipped"], []),
    "001.3": ("FluctuationTexture name", "D", ["schema"], []),
    "001.4": ("IsWarped true/false", "S", ["loader", "warpedtest"], ["I3"]),
    "002.1-5": ("marker attributes, binary64, prefix rule, no prefix refused, no rounding on load", "D; S",
                ["schema", *L, "q"], ["I1", "I2", "I3"]),
    "003.1": ("strictly increasing list of two or more held as read, in order", "S; D", ["loader", "shipped",
                                                                                         "review-a2"], ["I3"]),
    "007.1-2": ("last element is the shadow; remove/move refuse it; never a right neighbour", "S",
                ["shadow", "add", "remove", "move"], ["I6"]),
    "007.3": ("shadow segment extends the conversions past the last visible marker", "S; X", ["builder", "x2conv"],
              ["I9"]),
    "007.4": ("a different shadow spacing is kept on opening", "S (A2)", ["review-a2", "loader"], ["I3"]),
    "008.1": ("conversions refused when not warped", "D; S", ["convert", "warpedtest"], []),
    "008.2-5": ("conversion formulas, segment choice, extensions, fused evaluation, rate", "S; X",
                ["convert", "builder", "rate", "x2conv", "x2rules"], ["I3", "I8", "I9", "I10"]),
    "010.1": ("seven absent or value-less settings take creation defaults", "S", ["ctor", "loader", "schema"], ["I3"]),
    "011.1-2": ("WarpMode code table and chooser labels; 0-4, 6 held", "S", ["codes", "loader", "shipped"], ["I3"]),
    "012.1-3": ("transient codes and defaults; held", "S", ["codes", "ctor", "loader"], ["I3"]),
    "013.1-2": ("five ranges and defaults; in-range integers held", "S", ["ctor", "loader"], ["I3"]),
    "015.1-2": ("not warped; sample time range", "S", ["add", "warpedtest", "length"], ["I4"]),
    "015.3": ("position, neighbours, no left neighbour before the first marker", "S", ["add", "review-015"], []),
    "015.4": ("beat checks on q as given; none for a missing neighbour", "S", ["add", "review-015"], []),
    "015.5": ("bounds per neighbour as the 64-bit sequence, inclusive; none toward shadow or missing left", "S; X",
              ["add", "bounds", "review-015", "x2bounds", "x2rules"], ["I9"]),
    "015.6": ("otherwise accepted", "S", ["insertdelete"], ["I5"]),
    "015.7": ("remove/move lookup; no-such-marker and shadow refusals", "S", ["remove", "move", "lookup"], ["I6"]),
    "015.8": ("no warped check for remove and move; remove accepted, also on two markers", "S",
              ["remove", "move", "insertdelete", "review-015"], ["I5", "I6"]),
    "016.1": ("grid rounding as the 64-bit sequence", "S; X; D", ["q", "lookup", "x2q", "x2rules", "shipped"],
              ["I6", "I9"]),
    "016.2-3": ("used by the add and the lookup; load does not round", "S", ["q", "loader", "lookup"], []),
}

DENY = [r"analysis/", r"wiki/", r"\.\./", r"0x[0-9a-fA-F]{5,}", r"FUN_", r"disassembl", r"decompil", r"pseudocode",
        r"Ghidra", r"vtable", r"dossier", r"corpus", r"\bWMK-", r"PRB-", r"\bQ-0", r"\b[AIF][1-9]\b", r"\bI10\b",
        r"\bM[0-2]\b", r"AAudioClip", r"ASampleWarp", r"A(?:Abstract|Pseudo)?WarpMarker", r"OWarp", r"NWarperTypes",
        r"FWarpMarker", r"\bm(?:Sec|Beat)Time", r"DisplayWarpMode", r"RightTempo", r"LoopOs|LoopFwd|LoopAlt",
        r"[Uu]nwarped", r"adjacent marker", r"Segment length", r"can't be", r"doesn't exist", r"only available for",
        r"Empty warp marker", r"Conversion is only", r"is out of range\.", r"AfterRead", r"AddWarpMarker",
        r"derivation", r"Live\.arm64", r"/home/", r"/var/", r"/tmp/", r"ev_[0-9a-f]", r"from_chars", r"strto",
        r"\+0x", r"Patience", r"Chuck Sutton", r"Core Library", r"Vocal", r"\b[ds][78]-000", r"\bS8\b",
        r"Spectral envelope|spectral envelope", r"DBL_MAX", r"Python", r"expat|Expat", r"1 Bar", r"\bREX\b",
        r"[Pp]ost-?(load|read)", r"\bslot \+",
        # new in v2: planning, harness, instruction, library-call and engine-name patterns
        r"T11", r"\bT1\.\d", r"\bT1\b", r"\bX2\b", r"x2-", r"check_rules", r"harness", r"\bgdb\b", r"\bfma\b",
        r"frint|roundsd|fmsub|fmadd|fcsel|fdiv|fccmp", r"PlayPos|FileSmpl|StartSample|WarpMarkerList|Warper",
        r"\bADR\b", r"SPEC-(?!WARP-MARKERS)", r"\bslice\b", r"xexec", r"\bEngine\b", r"run_x", r"\bLAB_"]
ALLOWED_HITS = {"AGENTS.md": {"decompil"}}  # forbidden-inputs list, same wording as released packages

UNRELEASED = ["REQ-WARP-MARKERS-004", "REQ-WARP-MARKERS-005", "REQ-WARP-MARKERS-006", "REQ-WARP-MARKERS-009",
              "REQ-WARP-MARKERS-014"]  # review: 004 (RVW2-01) and 009 (RVW2-02) added
SCOPES = {
    "REQ-WARP-MARKERS-001": "AudioClip warp children and their empty single-Value form; FluctuationTexture name; IsWarped true/false",
    "REQ-WARP-MARKERS-002": "WarpMarker attributes; SecTime/BeatTime binary64 read by the decimal-prefix rule; no prefix refused; no rounding on load",
    "REQ-WARP-MARKERS-003": "Strictly increasing audio clip list of two or more markers held as read, in document order",
    "REQ-WARP-MARKERS-007": "Last marker of an audio clip list is the shadow marker; scripting remove and move refuse it; it is never a right neighbour; its segment extends the conversions past the last visible marker; a spacing other than 1/32 beat is kept on opening",
    "REQ-WARP-MARKERS-008": "Both conversions refused on a clip that is not warped; on a warped clip, the piecewise-linear conversion values with both extensions, as binary64 sequences, for a call right after opening",
    "REQ-WARP-MARKERS-010": "Seven absent or value-less audio clip settings take their defaults",
    "REQ-WARP-MARKERS-011": "WarpMode codes 0 to 4 and 6 with their chooser labels; held as stored",
    "REQ-WARP-MARKERS-012": "TransientResolution and TransientLoopMode codes and defaults, without labels; codes held as stored",
    "REQ-WARP-MARKERS-013": "Ranges and defaults of five settings; integer in-range values held as stored",
    "REQ-WARP-MARKERS-015": "add_warp_marker refusal conditions in order, insertion neighbours including none before the first marker, as-given beat checks, grid rounding and the binary64 beat bounds per neighbour; remove/move lookup and refusals; no warped check for remove and move; remove accepted, also on two markers",
    "REQ-WARP-MARKERS-016": "Grid rounding as a binary64 operation sequence in the scripting add and lookup; no rounding on load",
}

PROV_S = "static-derived; not observed reference output"
PROV_X = "extracted execution; not observed reference output"
PROV_XS = "computed by extracted-execution rules; not observed reference output"
PROV_LABELS = {
    PROV_S: "derived for the target build without running it, from evidence reviewed before sanitization",
    PROV_X: "the deciding binary64 values of the case (the conversion result, or the rounded beat and the beat bounds "
            "that decide the outcome) were computed by the original program's x86_64 code for this case's inputs, run "
            "on a Linux x86_64 host outside the application; for a conversion, that code computed the step between "
            "seconds and beats, and the division of a position in frames by the sample rate and the multiplication "
            "of a result by it are static-derived and exact for every case with this label; the grid rounding ran "
            "in another part of the original program that rounds a beat with the same operations as the add and the "
            "marker lookup (static-derived); the macOS arm64 build is inferred to compute the same; opening, the "
            "comparisons of the deciding values, the call's other checks and the sample rate are static-derived",
    PROV_XS: "computed for this case's inputs with the binary64 operation sequences that extracted execution of the "
             "original x86_64 code confirmed on other inputs; this input was not run; otherwise as static-derived",
}
ASSUMPTIONS = [
    "The base set, whose device lists are empty, opens in the target build. Its structure follows static-derived rules (every case).",
    "Marker times are held as binary64 values read by the decimal rule of REQ-WARP-MARKERS-002 (every case).",
    "The sample length that add_warp_marker compares with is the duration of the clip's sample, 3 s (cases 021 to 032, 052 to 055 and 059 to 061). Every add whose sample time lies in the sample stays at least 0.5 s before its end, and the 900,000 s of case 024 lies beyond it whether it is counted in seconds, milliseconds or frames.",
    "The sample rate that both conversions use is the rate of the clip's sample, 8,000 Hz, which the clip also stores (cases 039 to 051).",
    "An add or remove whose checks all pass raises no further error (cases 022, 031, 032, 035, 038, 052, 054, 058, 059, 061 and 063).",
    "The marker lookup of REQ-WARP-MARKERS-015 clause 7 behaves as stated (cases 033 to 038, 056 to 058, 062 and 063).",
    "The macOS arm64 build computes the conversions, the grid rounding and the beat bounds with the same binary64 operations as the x86_64 build (cases 039 to 060).",
    "A conversion made right after opening uses the marker list held after opening (cases 039 to 051).",
]

REVIEW_PENDING = {"status": "pending", "reviewers": [], "date": None, "findings": [],
                  "disposition": "pending: separate handoff review required before release", "record": None}


def manifest_meta(case_count, target, exclusions, changes):
    return {
        "schema": "handoff-manifest-v1", "release_id": "warp-markers-v2", "release_status": "candidate-unreviewed",
        "release_date": None, "target": target,
        "specification": {"id": "SPEC-WARP-MARKERS", "parent_revision": 4, "release_revision": 4},
        "feature_ids": ["FEAT-WARP", "FEAT-PERSISTENCE"],
        "partial_requirement_scopes": SCOPES, "unreleased_requirements": UNRELEASED,
        "compatibility_dimensions": {
            "document-load-state": "static-derived expectations; reference execution not-run",
            "scripting-edit-checks": "static-derived and extracted-execution expectations as labelled; reference execution not-run",
            "scripting-conversion-values": "extracted-execution expectations as labelled; reference execution not-run",
            "file-format-written": "excluded (nothing saved is graded)",
            "playback": "excluded",
            "audio": "excluded", "ui": "excluded", "timing": "excluded",
        },
        "expectation_provenance_labels": PROV_LABELS, "stated_assumptions": ASSUMPTIONS,
        "exclusions": exclusions,
        "fixture_origin": "independently authored complete Live Set documents built from one base set, and one generated silent WAV; no shipped file content, audio or program code",
        "approved_public_sources": [], "review": REVIEW_PENDING, "supersedes": "warp-markers-v1",
        "supersession": {
            "relationship": "supersedes with one case withdrawn: carries 37 of the 38 warp-markers-v1 case records unchanged with rebuilt fixtures; WARP-MARKERS-018 is withdrawn and has no expectation; for every other case and clause of warp-markers-v1 both give the same expectations; warp-markers-v1 stays immutable, but its fixtures must not be used (the target build refuses 17 of its 18 documents)",
            "superseded_manifest_sha256": V1_MANIFEST_SHA,
            "restated_cases": "WARP-MARKERS-001 to 017 and 019 to 038: case records identical to warp-markers-v1; fixture names and the WAV bytes identical; every XML fixture rebuilt as a complete Live Set without devices",
            "withdrawn_cases": {"WARP-MARKERS-018": "its document needs a Simpler in a track's device list; whether the target build accepts a device there is not established, so the case has no expectation; REQ-001 clause 2 and REQ-004 are withdrawn with it"},
            "changes": changes,
        },
        "entrypoint": "README.md", "case_count": case_count,
        "inventory_excludes": ["manifest.json (self-hash recorded outside package)"], "files": [],
    }
