"""Analyst-only tables for build_wm.py: evidence locators, inferred links, case and clause traceability,
the payload deny-list, the draft manifest and the evidence re-hash. Never shipped. Locators were re-read
on 2026-10-18."""
import hashlib, json
from pathlib import Path

S8 = "analysis/ableton-live-12.4.3/r2/s8-warp-v1/"
N1 = "analysis/ableton-live-12.4.3/r2/n1-transport-state-v1/results/"
D7 = "/var/tmp/sound-analysis/query-spool-2/results/"  # not yet retained in a run (spec appendix)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def evidence_identity(root):  # re-hash the S8 run, the image and the d7 dossier manifests
    s8, d7 = root / S8, Path(D7)
    man = json.loads((s8 / "manifest.json").read_text())
    bad = [k for k, v in man["files"].items() if sha((s8 / k).read_bytes()) != v["sha256"]]
    binary = sha((s8 / man["binary"]["path"]).resolve().read_bytes()) == man["binary"]["sha256"]
    prefixes = {f"{r}/{n}": sha((d7 / r / n).read_bytes())[:8] for r in ("d7-0001", "d7-0002")
                for n in ("queries.json", "manifest.json") if (d7 / r / n).is_file()}
    return {"s8_manifest_sha256": sha((s8 / "manifest.json").read_bytes()), "s8_files": len(man["files"]),
            "s8_mismatches": bad, "binary_matches": binary, "d7_prefixes": prefixes,
            "d7_prefixes_match_spec": prefixes == {"d7-0001/queries.json": "1dede799", "d7-0001/manifest.json": "90af824c",
                                             "d7-0002/queries.json": "ce8a537e", "d7-0002/manifest.json": "d55bc6f8"}}


E = {
    "schema": S8 + "static-survey.json schema part (12.0_12402: AudioClip and SampleWarpProperties members, "
                   "WarpMarker attributes; FluctuationTexture present, no FluxTexture)",
    "shipped": S8 + "static-survey.json documents part: distributions (2,878 AudioClip defaults, WarpMode codes), "
                    "checks number_text_rule 44,058, *strictly_increasing 2,878 + 7,372, beat_on_1/3843840_grid 22,029, "
                    "SampleWarpProperties count=0 4,244",
    "paths": "decoded shipped demo set W0 (SHA-256 3f1c0f924b750c2a...) read 2026-10-18 for element paths only: "
             "Tracks/AudioTrack/DeviceChain/MainSequencer/ClipSlotList/ClipSlot/ClipSlot/Value/AudioClip and "
             "Tracks/MidiTrack/DeviceChain/DeviceChain/Devices/OriginalSimpler/Player/MultiSampleMap/SampleParts/"
             "MultiSamplePart/SampleWarpProperties; child order of both holders; no content copied",
    "markerreg": S8 + "results/s8-0001/functions/0x10260fdd8.* (mSecTime +0x50, mBeatTime +0x58, flags 4 attribute, "
                      "type -4); registrations.txt",
    "getters64": D7 + "d7-0002/functions/0x102610264.*, 0x10261026c.* (64-bit Sec/Beat getters)",
    "loader": N1 + "n1-0008/functions/0x101487310.* (generic loader: walks members, skips absent ones, stores "
                   "directly); " + N1 + "n1-0006/functions/0x10152bfb8.* (text conversion: bool, strtod with "
                   "no-consumption throw); throws carry the corrupt-document key 0x10148229c",
    "ctor": S8 + "results/s8-0001/functions/0x1027b0e40.* (TransientResolution mov w1,#0x6; TransientLoopMode "
                 "mov w1,#0x2; float parameter triples); getter-constants.txt; ComplexProEnvelope default 128 "
                 "(0x10224e2e8 movi 0x43 lsl 24, spec appendix)",
    "postread": S8 + "results/s8-0001/functions/0x1027c1c7c.* (empty test; then 0x1027b3928, which sets owner and "
                     "onset links of each marker without setting times: corpus 0x1027b3928, 0x1027b7cf0, 0x102610134)",
    "swppostload": S8 + "results/s8-0002/functions/0x10288538c.* (sample-part post-load: no empty test)",
    "shadow": S8 + "results/s8-0001/functions/0x1026102c0.* (is-shadow: marker is the list's last element)",
    "convert": D7 + "d7-0001/functions/0x1033bf160.c and 0x1033bf250.c (audio-clip class test, then slot +0x300 "
                    "warped test; both throw for an unwarped clip before any table use)",
    "add": S8 + "results/s8-0001/functions/0x1033bf42c.* (class test; warped test; 0 <= p <= length, NaN refused; "
                "scan by SecTime stopping at the shadow; left check q < left.beat and right check right.beat < q on "
                "the unrounded q; right check skipped for the shadow; q() then bounds per neighbour)",
    "bounds": S8 + "results/s8-0002/functions/0x1027afd40.* (beat bounds nb.beat + ds*999/60 and nb.beat + ds*5/60; "
                   "only caller the add)",
    "remove": S8 + "results/s8-0002/functions/0x1033bfa68.* (class test only; lookup; shadow refusal; "
                   "no-such-marker refusal; delete 0x1027c6eec)",
    "move": S8 + "results/s8-0003/functions/0x1033bfb94.* (class test only; lookup; shadow and no-such-marker "
                 "refusals before the untraced limits routine 0x1027b83bc)",
    "lookup": "corpus 0x1027c79d0 (pseudocode only, in " + S8 + "corpus-excerpts.jsonl): q() of the argument, scan "
              "in list order, return the first marker with an equal beat, stop once a beat exceeds it",
    "insertdelete": "corpus 0x1027baad8 (insert: returns without change when a marker has an equal SecTime or "
                    "BeatTime; no throw) and 0x1027c6eec (delete: returns without change below three markers; no "
                    "throw); callees untraced; looked up 2026-10-18 with " + S8 + "corpus_lookup.py",
    "q": S8 + "results/s8-0001/functions/0x1033bf42c.* q() block (|q +- step/2| * 3843840 truncated, sign "
              "restored; four sentinels skipped); results/s8-0003/functions/0x1026101b4.* (BeatTime setter rounds; "
              "not used by the loader's direct store)",
    "codes": S8 + "results/s8-0002/functions/0x1026a9ef8.* (7 WarpMode labels), 0x1027b279c.* (7 TransientResolution "
                  "labels), 0x1027b29e8.* (3 TransientLoopMode entries); vtable-reads.txt",
    "length": "corpus 0x1027b6954 (sample length through the clip's sample object, slot +0x1b0; source untraced)",
}

I = {
    "I1": "SecTime and BeatTime are binary64 members read by the 64-bit branch of the text conversion (type -4 like "
          "other double members; 64-bit getters; shipped text matches the 64-bit writer rule). The spec labels this "
          "'Double branch assumed'.",
    "I2": "A conversion error while a nested value is read stops the open (same mechanism as the transport-state-v1 "
          "refused cases, whose review accepted it).",
    "I3": "Nothing between reading the clip and the observation changes its markers or settings. The audio clip's "
          "post-read step only links markers (corpus); later steps are untraced. Spec A2 states this premise but "
          "scopes it to saved values (plan finding F1).",
    "I4": "The sample length used by add_warp_marker is the duration in seconds of the clip's sample. Cases keep at "
          "least 0.5 s from the 3 s length.",
    "I5": "After its checks pass, an add or remove raises no further error (insert and delete pseudocode contain "
          "no throw; callees untraced).",
    "I6": "The marker lookup behaves as its corpus pseudocode reads (not dossier-confirmed).",
    "I7": "The warped test of the conversions and of the add reflects the IsWarped value read from the document "
          "(slot +0x300 target not read in a dossier).",
}

# release case -> (SPEC-WARP-MARKERS r1 source, evidence keys, inferred links)
L = ["loader", "markerreg", "getters64"]
TRACE = {
    1: ("WMK-001 and WMK-002, load part only (saved text excluded: A2); settings re-authored to non-default values",
        ["schema", "paths", *L, "codes", "ctor"], ["I1", "I3"]),
    2: ("REQ-001 IsWarped clause, new; fixture shared with the scripting cases of WMK-020/028", ["schema", "loader"],
        ["I3"]),
    3: ("WMK-004, load part only", L, ["I1", "I3"]),
    4: ("REQ-002 reading rule (REQ-TRANSPORT-STATE-004 leading U+0020), new", L, ["I1", "I3"]),
    5: ("WMK-003, load part only", [*L, "q"], ["I1", "I3"]),
    6: ("REQ-002 reading rule (text after the prefix ignored), new", L, ["I1", "I3"]),
    7: ("WMK-005", L, ["I1", "I2"]),
    8: ("REQ-002 no-prefix clause (empty text), new", L, ["I1", "I2"]),
    9: ("WMK-021, load part only; TransientEnvelope dropped (finding F2)", ["ctor", "loader"], ["I3"]),
    10: ("REQ-010 'without its Value attribute', new", ["ctor", "loader"], ["I3"]),
    11: ("REQ-012 TransientResolution code, new (WMK-024 load part is in case 1)", ["codes", "loader"], ["I3"]),
    12: ("REQ-012 TransientLoopMode code, new", ["codes", "loader"], ["I3"]),
    **{n: (f"WMK-023 code {c}, load part only (display not graded)", ["codes", "loader", "shipped"], ["I3"])
       for n, c in zip(range(13, 18), (0, 1, 2, 3, 6))},
    18: ("WMK-007 narrowed to one Simpler sample part, load only (saved text excluded: A2)",
         ["swppostload", "schema", "shipped", "paths"], ["I3"]),
    19: ("WMK-020 first call", ["convert"], ["I7"]),
    20: ("WMK-020 second call", ["convert"], ["I7"]),
    21: ("WMK-028 re-authored on list M1 with (0.5 s, beat 1)", ["add"], ["I7"]),
    22: ("REQ-015 accepted counterpart of case 21, new", ["add", "bounds", "q", "insertdelete", "length"],
         ["I3", "I4", "I5"]),
    23: ("WMK-029 first call", ["add"], ["I3"]),
    24: ("WMK-029 second call (sample now 3 s)", ["add", "length"], ["I4"]),
    25: ("WMK-030", ["add", "shadow"], ["I3"]),
    26: ("REQ-015 'q, as given', new", ["add", "q"], ["I3"]),
    27: ("WMK-031", ["add", "shadow"], ["I3"]),
    28: ("WMK-032 first call", ["add", "q", "bounds"], ["I3"]),
    29: ("WMK-032 second call", ["add", "q", "bounds"], ["I3"]),
    30: ("REQ-015 upper tempo limit, new", ["add", "bounds"], ["I3"]),
    31: ("WMK-033", ["add", "q", "bounds", "insertdelete", "length"], ["I3", "I4", "I5"]),
    32: ("WMK-034", ["add", "bounds", "shadow", "insertdelete", "length"], ["I3", "I4", "I5"]),
    33: ("WMK-015 first call, re-authored on list M1", ["remove", "lookup", "shadow"], ["I3", "I6"]),
    34: ("WMK-015 second call, re-authored on list M1", ["move", "lookup", "shadow"], ["I3", "I6"]),
    35: ("WMK-035 first call", ["remove", "lookup", "q", "insertdelete"], ["I3", "I5", "I6"]),
    36: ("WMK-035 second call", ["remove", "lookup", "q"], ["I3", "I6"]),
    37: ("REQ-015 move with no matching marker, new", ["move", "lookup", "q"], ["I3", "I6"]),
    38: ("REQ-015 'the remove does not require the clip to be warped', new", ["remove", "lookup", "insertdelete"],
         ["I3", "I5", "I6"]),
}

# release clause -> (summary, support, evidence keys, inferred links)
CLAUSES = {
    "001.1": ("AudioClip warp children and empty single-Value form", "D", ["schema", "shipped"], []),
    "001.2": ("Sampler/Simpler marker list and settings in SampleWarpProperties under MultiSamplePart", "D",
              ["schema", "shipped", "paths"], []),
    "001.3": ("FluctuationTexture name", "D", ["schema"], []),
    "001.4": ("IsWarped true/false", "S", ["loader"], ["I3"]),
    "002.1": ("WarpMarker attributes Id, SecTime, BeatTime; binary64", "D; S", ["schema", "markerreg", "getters64"],
              ["I1"]),
    "002.2": ("number text read by the released 64-bit prefix rule", "S", ["loader"], ["I1"]),
    "002.3": ("no numeric prefix refused", "S", ["loader"], ["I2"]),
    "002.4": ("loaded value kept without rounding, clamp or range check", "S", ["loader", "q"], ["I3"]),
    "003.1": ("strictly increasing list of two or more loads as read, in document order", "S; D",
              ["loader", "shipped", "postread"], ["I3"]),
    "004.1": ("empty sample-part list not refused", "S; D", ["swppostload", "shipped"], ["I3"]),
    "007.1": ("last element of an audio clip list is the shadow marker", "S", ["shadow"], []),
    "007.2": ("scripting remove and move refuse the shadow marker", "S", ["remove", "move", "shadow"], ["I6"]),
    "008.1": ("conversions refused on a clip that is not warped", "D; S", ["convert"], ["I7"]),
    "010.1": ("absent or value-less settings take the creation defaults", "S", ["ctor", "loader"], ["I3"]),
    "011.1": ("WarpMode code table", "S", ["codes"], []),
    "011.2": ("WarpMode 0-4, 6 held as stored", "S", ["loader", "shipped"], ["I3"]),
    "012.1": ("TransientResolution codes, labels, default 6", "S", ["codes", "ctor"], []),
    "012.2": ("TransientLoopMode codes 0-2, default 2", "S", ["codes", "ctor"], []),
    "012.3": ("codes in the lists held as stored", "S", ["loader"], ["I3"]),
    "013.1": ("ranges and defaults of five settings (TransientEnvelope excluded)", "S", ["ctor"], []),
    "013.2": ("integer values in range held as stored", "S", ["loader"], ["I3"]),
    "015.1": ("add refused when not warped", "S", ["add"], ["I7"]),
    "015.2": ("add refused when p < 0 or p > sample length", "S", ["add", "length"], ["I4"]),
    "015.3": ("insertion position and neighbours; shadow is never a right neighbour", "S", ["add", "shadow"], []),
    "015.4": ("neighbour beat checks on q as given", "S", ["add"], []),
    "015.5": ("grid rounding, then 5-999 BPM per neighbour, none toward the shadow", "S", ["add", "q", "bounds"], []),
    "015.6": ("otherwise accepted (no error)", "S, inferred", ["insertdelete"], ["I5"]),
    "015.7": ("remove/move lookup by rounded beat; no-such-marker and shadow refusals", "S",
              ["remove", "move", "lookup"], ["I6"]),
    "015.8": ("remove accepted without the warped condition", "S", ["remove", "insertdelete"], ["I5", "I6"]),
    "016.1": ("grid rounding definition, used by the add and the lookup", "S; D", ["q", "lookup", "shipped"], ["I6"]),
    "016.2": ("load does not round", "S", ["loader", "q"], []),
}

DENY = [r"analysis/", r"wiki/", r"\.\./", r"0x[0-9a-fA-F]{5,}", r"FUN_", r"disassembl", r"decompil", r"pseudocode",
        r"Ghidra", r"vtable", r"dossier", r"corpus", r"\bWMK-", r"PRB-", r"\bQ-0", r"\b[AIF][1-9]\b", r"\bM[0-2]\b",
        r"AAudioClip", r"ASampleWarp", r"A(?:Abstract|Pseudo)?WarpMarker", r"OWarper", r"NWarperTypes", r"FWarpMarker",
        r"\bm(?:Sec|Beat)Time", r"DisplayWarpMode", r"RightTempo", r"LoopOs|LoopFwd|LoopAlt", r"[Uu]nwarped",
        r"adjacent marker", r"Segment length", r"can't be", r"doesn't exist", r"only available for",
        r"Empty warp marker", r"Conversion is only", r"is out of range\.", r"AfterRead", r"AddWarpMarker",
        r"derivation", r"Live\.arm64", r"/home/", r"/var/", r"/tmp/", r"ev_[0-9a-f]", r"from_chars", r"strto",
        r"\+0x", r"Patience", r"Chuck Sutton", r"Core Library", r"Vocal", r"\b[ds][78]-000", r"\bS8\b",
        r"Spectral envelope|spectral envelope", r"DBL_MAX", r"Python", r"expat|Expat",
        r"1 Bar", r"\bREX\b", r"[Pp]ost-?(load|read)", r"\bslot \+"]  # review: labels and structure words
ALLOWED_HITS = {"AGENTS.md": {"decompil"}}  # forbidden-inputs list, same wording as released packages

UNRELEASED = ["REQ-WARP-MARKERS-005", "REQ-WARP-MARKERS-006", "REQ-WARP-MARKERS-009", "REQ-WARP-MARKERS-014"]
SCOPES = {
    "REQ-WARP-MARKERS-001": "AudioClip warp children and their empty single-Value form; Sampler/Simpler list and settings in SampleWarpProperties; FluctuationTexture name; IsWarped true/false",
    "REQ-WARP-MARKERS-002": "WarpMarker attributes; SecTime/BeatTime binary64 read by the decimal-prefix rule; no prefix refused; no rounding on load",
    "REQ-WARP-MARKERS-003": "Strictly increasing audio clip list of two or more markers held as read, in document order",
    "REQ-WARP-MARKERS-004": "Empty marker list of a sample part not refused",
    "REQ-WARP-MARKERS-007": "Last marker of an audio clip list is the shadow marker; scripting remove and move refuse it",
    "REQ-WARP-MARKERS-008": "Both conversions refused on a clip that is not warped",
    "REQ-WARP-MARKERS-010": "Seven absent or value-less audio clip settings take their defaults",
    "REQ-WARP-MARKERS-011": "WarpMode codes 0 to 4 and 6 with their chooser labels; held as stored",
    "REQ-WARP-MARKERS-012": "TransientResolution and TransientLoopMode codes and defaults, without labels; codes held as stored",
    "REQ-WARP-MARKERS-013": "Ranges and defaults of five settings; integer in-range values held as stored",
    "REQ-WARP-MARKERS-015": "add_warp_marker refusal conditions, insertion neighbours, beat checks, grid rounding and 5 to 999 BPM limits; remove/move lookup and refusals; remove without the warped condition",
    "REQ-WARP-MARKERS-016": "Grid rounding in the scripting add and lookup; no rounding on load",
}


REVIEW = {  # review: separate reviewer's record, 2026-10-18 (REVIEW.md in the package)
    "status": "approved",
    "reviewers": ["separate review agent (Claude Opus 5.5) in a coordinator-launched handoff-review context; not the author; will not implement"],
    "date": "2026-10-18",
    "findings": [
        "RVW-01 high: the opening premise underlies every held value and every list-dependent call; confirmed by the reviewer's static check for the document read and each object's own completion step; later changes the application makes by itself excluded; cases 001 and 002 act as controls in the comparison obligation; no case changed",
        "RVW-02 medium: 'any TransientEnvelope value' had no expectation although every fixture carries one; reworded to values other than 100; the fixture value equals the creation value stored without a clamp and the value of every shipped audio clip; no expectation depends on the open range",
        "RVW-03 medium: the tempo-limit and rounding-tie bands (0.000001) were narrower than the floating-point arithmetic the evidence shows; widened to 0.001 BPM, 0.001 grid step and a 0.0005 s neighbour gap; no case affected",
        "RVW-04 low: case 024 relied on the unit of the sample length; sample time raised to 900,000 s so the refusal holds in seconds, milliseconds or frames",
        "RVW-05 low: TransientResolution labels and the code-5 label came from stored enumeration lists, not established display text; removed from the contract and case 011",
        "RVW-06 info: the warped test reads the IsWarped value that opening stores; confirmed; the assumption is dropped from the contract",
        "RVW-07 info: REQ-015 clauses, the 5 to 999 BPM bounds, as-given beat checks, the shadow exception and the lookup re-derived from the evidence; all 38 expectations agree with the reviewer's restatement",
        "RVW-08 info: fixtures, WAV and sharing; evidence identity re-checked; unretained query rounds acceptable for this release",
        "RVW-09 editorial: payload status set to reviewed release; review record added; inventory re-hashed",
    ],
    "disposition": "Approved with listed narrowing (RVW-01, RVW-03, RVW-04, RVW-05), only for the explicit partial clauses; expectations static-derived; reference and candidate execution not-run; restricted implementation workspace required",
    "record": "REVIEW.md",
}


def manifest_meta(case_count, target):
    return {
        "schema": "handoff-manifest-v1", "release_id": "warp-markers-v1", "release_status": "released",
        "release_date": "2026-10-18", "target": target,
        "specification": {"id": "SPEC-WARP-MARKERS", "parent_revision": 1, "release_revision": 1},
        "feature_ids": ["FEAT-WARP", "FEAT-PERSISTENCE"],
        "partial_requirement_scopes": SCOPES, "unreleased_requirements": UNRELEASED,
        "compatibility_dimensions": {
            "document-load-state": "static-derived expectations; reference execution not-run",
            "scripting-edit-checks": "static-derived expectations; reference execution not-run",
            "file-format-written": "excluded (nothing saved is graded)",
            "scripting-conversion-values": "excluded",
            "playback": "excluded (REQ-WARP-MARKERS-009)", "audio": "excluded", "ui": "excluded",
            "timing": "excluded",
        },
        "exclusions": {
            "inputs_without_expectation": [
                "SecTime or BeatTime text starting, after spaces and a sign, with 0x, inf or nan; the text Invalid; text starting with #; leading whitespace other than U+0020; a missing SecTime or BeatTime; values outside -1,000,000 to 1,000,000",
                "marker Id values that are missing, repeated or not decimal integers; content inside WarpMarker; children of WarpMarkers other than WarpMarker",
                "audio clip marker lists with fewer than two markers or not strictly increasing in both positions",
                "code and setting text other than plain decimal digits; codes outside their lists; settings outside their ranges or not integers; IsWarped other than true or false; a missing IsWarped or WarpMode; a TransientEnvelope value other than 100 (every fixture carries 100; the held value is not judged)",
                "other children of AudioClip or SampleWarpProperties, other child orders, repeated children",
                "scripting arguments that are not finite or have magnitude 1,000,000 or more; an add whose sample time, within the sample, is below the first marker's SecTime or less than 0.0005 s from a neighbour's SecTime; a segment tempo within 0.001 BPM of 5 or 999; a beat within 0.001 grid step of a rounding tie; remove or move on a list of fewer than three markers; a call that breaks more than one rule",
                "any other envelope, format version, compressed container or document kind",
            ],
            "behavior": [
                "everything written on save (REQ-002, 003, 004, 007, 010 save clauses)",
                "an audio clip whose marker list is empty (REQ-004); one-marker, out-of-order and equal-position lists (REQ-005); missing or Invalid positions (REQ-006)",
                "the value used, shown and saved for codes and settings outside their ranges (REQ-014); the TransientEnvelope range and default",
                "conversion values of sample_to_beat_time and beat_to_sample_time; playback position (REQ-009); audio output of every warp mode",
                "the default WarpMode of an audio clip or sample part and the default warp mode preference; sample-part defaults",
                "where and when the application creates or re-places the shadow marker; the marker list after an accepted add or remove; move limits and accepted moves; the scripting warp_mode setter; non-audio clips",
                "display of markers, codes, labels and settings; interactive edits, auto-warp, recording and undo",
                "any change the application makes by itself after reading the document, such as automatic warping or sample analysis; whether the original makes one on opening is not established",
                "refusal presentation and the state after a refusal; error text of scripting calls",
                "progress, cancellation and timing",
            ],
        },
        "fixture_origin": "independently authored minimal documents from one template and one generated silent WAV; no shipped file content, audio or program code",
        "approved_public_sources": [],
        "review": REVIEW,
        "supersedes": None, "entrypoint": "README.md", "case_count": case_count,
        "inventory_excludes": ["manifest.json (self-hash recorded outside package)"],
        "files": [],
    }
