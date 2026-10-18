"""Analyst-only traceability for midi-note-storage-v1: release case -> SPEC-MIDI-NOTE-STORAGE r1
case or clause, evidence locators and inferred links. Written to traceability.json by build_mns.py
seal; never shipped. Locators were re-read on 2026-10-18 (see the plan page).
"""
S7 = "analysis/ableton-live-12.4.3/r2/s7-midi-notes-v1/"
N1 = "analysis/ableton-live-12.4.3/r2/n1-transport-state-v1/"
D4 = "/var/tmp/sound-analysis/query-spool-2/results/d4-0001/ (not retained in the repository)"
REVIEW = "analysis/ableton-live-12.4.3/handoff-staging/midi-note-storage-v1-analysis/review/"
CORPUS = "/var/tmp/sound-analysis/corpus/decomp/chunks/chunk-00813.jsonl"

EVIDENCE = {
    "structure": S7 + "static-survey.json schema.segments (MidiNotes, KeyTrack, MidiNoteEvent, PerNoteEventList, "
                      "PerNoteEvent at 12.0_12402), documents.midinotes_child_orders, keytrack_child_orders",
    "array": S7 + "results/s7-0001/functions/0x101560424.c (each child's class compared with the array class; "
                  "mismatch -> 'Class mismatch for array member' thrown via 0x10148229c)",
    "attrs": S7 + "results/s7-0004/functions/0x1028e26c0 (eight flag-4 attribute members in schema order); "
                  "results/s7-0001/functions/0x101487284 (reset +0xc8, generic loader, post-load +0xd0)",
    "text": N1 + "results/n1-0006/functions/0x10152bfb8.c (double: length-7 'Invalid' -> 1.79769313486232e+308, "
                 "else strtod with a no-consumption throw; float: strtod then (float); bool via 0x10152bf4c; int64 "
                 "via 0x101533e14; int via 0x1002fd908)",
    "int64": S7 + "results/s7-0004/functions/0x101533e14 (leading-space scan, trailing-space count, one '+', length "
                  "min(len - start, end) < 0x40, '+-' check, ASCII check of the whole text, whole-span conversion); "
                  + CORPUS + " offset 61888, line SHA-256 d23d0462a5c583f6ea2e0f4dd39d20c247f497ca96beeb3f999f5ed3f0f2a2a9"
                  " (0x101524d8c: signed 64-bit from_chars; leading zeros skipped, '-' accepted, errc 0x22 above "
                  "INT64_MAX, errc 0x16 without digits)",
    "reset": S7 + "results/s7-0002/functions/0x1028e2fcc (sets only VelocityDeviation 0, Probability 1, IsEnabled true)",
    "omit": S7 + "results/s7-0001/functions/0x1028e2fe4 (omit predicate); " + N1 + "results/n1-0008/functions/"
                 "0x101486cdc (generic writer: flag-4 attributes in registration order, children in order); " + S7 +
                 "results/s7-0003/functions/0x101560258 (array writer, array order); results/s7-0004/functions/"
                 "0x1028e2f90 (copy-out, no rounding)",
    "limits": S7 + "results/s7-0001/functions/0x1028e2c80.json disassembly 0x1028e2c80-0x1028e2ce0 (Duration fcmp, "
                   "fccmp DBL_MAX, str xzr; Velocity fcsel gt then mi; OffVelocity and Probability fcmlt, fcmgt, bit, bic "
                   "against (127.0, 1.0) at 0x105896fa8)",
    "grid": S7 + "results/s7-0001/functions/0x1028e2e24.json disassembly (sentinels 0x1055d9680 and 0x1055d9690, "
                 "fcsel ge sign, h 0x3e9175746e8cba40, fmadd x 0.5, fabs, fmul 3843840.0 (0x414d538000000000), frintm, "
                 "fdiv, fmul sign); results/s7-0003/functions/0x1025c7a0c.json (TimeOffset, same sequence); "
                 "vtable-reads.txt (sentinel values)",
    "notes_post": S7 + "results/s7-0001/functions/0x1028f5864 (MidiNotes post-load); results/s7-0002/functions/"
                       "0x1028f6154 (non-zero ids collected and sorted, adjacent-equal throw), 0x102920db4 (next-id "
                       "raise, 1 without ids), 0x1028f6664 (zero-id pass: key track list order, then array order); "
                       "results/s7-0003/functions/0x1028db9b8 (id allocation)",
    "order": S7 + "notes.md (no sort after load: generic post-load 0x101486fa8 on KeyTrack and the array); "
                  "static-survey.json documents.checks (keytracks_sorted_by_key, order_time_decreasing 0, "
                  "order_time_equal 0, overlap_same_key 261)",
    "list_post": S7 + "results/s7-0002/functions/0x10292b730 (CC + 2 > 0x82 skip; validity 0x1011afdac; DBL_MAX "
                      "drop; clamp bounds results/s7-0003/functions/0x1011afc18, 0x1011afc2c; stable sort "
                      "results/s7-0003/functions/0x1029307b8); results/s7-0002/functions/0x1011afdac.c (not 0, 32, "
                      "120 to 128)",
    "store_post": S7 + "results/s7-0002/functions/0x10292cd70 (erase NoteId 0 or invalid CC; (NoteId, CC) set size "
                       "differing from the list count throws)",
    "orphans": S7 + "results/s7-0003/functions/0x1028f64d0 (lists whose NoteId is not in the pre-assignment id list "
                    "are removed)",
    "span": REVIEW + "corpus-excerpts.jsonl records 0x10292b9ec and 0x10292c960 (code SHA-256 equal to the d4-0001 "
                     ".c files 98be02fc, 33cdeee5), 0x1028da61c (NoteId at +0x28), 0x1028dea48 (Duration at +8); "
                     + REVIEW + "a64.py decode of the pinned image 0x10292ba50-0x10292ba70 (fcmp d0,#0.0; b.le; "
                     "fcmp d0,d1; b.mi); " + S7 + "results/s7-0001/functions/0x1028f5864.json 0x1028f5bec-0x1028f5c0c "
                     "(x0 store, x1 NoteId, d0 Duration); originally " + D4 + " functions/0x10292b9ec.json 0x10292ba50-0x10292ba70 (first offset > 0 and last < Duration: early "
                 "return) and 0x10292c960 (called per note; lists with no events removed); SHA-256 prefixes "
                 "313210f3, 98be02fc, 306f1071, 33cdeee5, queries.json 535d6a5d (match the spec appendix)",
    "gate": REVIEW + "corpus-excerpts.jsonl and review-checks.txt: the reader 0x101484108 builds its load context "
                     "through 0x101478258 -> 0x10151e0d8 (+0x2c = 1) and passes it to 0x101486fe4; every context "
                     "constructor stores 1; the only clear 0x1015192b8 is called only by 0x101546518 and 0x101547ef4 "
                     "(undo-history binary stream); post-read slot +0xd0 runs when +0x2c is set (0x101487284, "
                     "0x101487310, 0x101486fe4)",
    "event": S7 + "results/s7-0004/functions/0x1025c77fc (constructor: controls 0.5), 0x1025c7b04 (reset of the "
                  "four controls only), 0x1025c7b10 (omit when equal to 0.5)",
    "fmt": S7 + "results/s7-0001/functions/0x10152205c (Double 0x101520dbc, Float 0x101520c70, Int64 plain, Bool); "
                "static-survey.json documents.checks fmt_ok 2,054,618; rule as released in transport-state-v1 "
                "REQ-TRANSPORT-STATE-011",
    "xml": "handoff/als-container-v1/spec.md REQ-ALS-CONTAINER-001 clause 5 (not well-formed XML refused); a "
           "repeated attribute violates XML 1.0 well-formedness",
    "refusal": "throws via 0x101488e64 and 0x10148229c (spec appendix row 017); top-level catch untraced",
}

INFERRED = {
    "I1": "Resolved by review RVN-01 (evidence key 'gate'). The load-context flag +0x2c gates every post-read step, "
          "not only the note limits: note limits, MidiNotes post-load (ids, next id, orphans, per-note list step, "
          "zero ids), store and list post-loads. The reviewer established that it is set for Live Set reads. Spec "
          "assumption A1 should be widened accordingly and marked established; PRB-S7-03 remains a reference check.",
    "I2": "Opening a Live Set and saving it without other changes alters the notes only by the released rules. Spec "
          "assumption A2 restated for an open-save of a set instead of placing a clip file (PRB-S7-09).",
    "I3": "A refusal raised while the notes are read stops the reading of the document; the catch site is untraced. "
          "What remains open is excluded (REQ-017 U); the comparison convention accepts a set not opened or opened "
          "without the clip. The transport-state-v1 review accepted the same inference for other read errors.",
    "I4": "A carrier set holding only the elements on the path to the clip, and the clip's Loop, reads the clip's "
          "notes as a full set would; the reference obligation embeds the notes element in a full set.",
    "I5": "strtod is correctly rounded and the save formatter prints exact binary values (accepted in the "
          "transport-state-v1 review); no case value lies on a tie or near a power of ten.",
    "I6": "gzip of the fixtures' form is decompressed in the standard way (als-container-v1 RVA-09, accepted).",
    "I7": "MidiKey, CC and the Id attributes are read by the int parser 0x1002fd908, whose converter 0x1002fda78 is "
          "from_chars-shaped and accepts a leading '-' (CC -2, -1, -3); every shipped clip with per-note lists "
          "carries CC -1 or -2 text.",
}

SAVE = ["I2", "I4", "I5", "I6"]
REFUSE = ["I3", "I4", "I6"]
NEW = "new case for an r1 clause without a case: "


TRACE = {
    "MNS-001": ("MNS-001; group generator value and group content not compared (finding F2)",
                   ["structure", "attrs", "omit", "order", "notes_post", "fmt"], SAVE),
    "MNS-002": ("MNS-002", ["reset", "omit", "fmt"], SAVE),
    "MNS-003": ("MNS-003; n2 expectation added (per-note defaults, REQ-003)", ["reset", "omit", "fmt"], SAVE),
    "MNS-004": ("MNS-004", ["attrs", "reset", "omit"], SAVE),
    "MNS-005": ("MNS-005", ["text", "omit"], SAVE),
    "MNS-006": ("MNS-006", ["text"], REFUSE),
    "MNS-007": ("MNS-007", ["text", "int64"], REFUSE),
    "MNS-008": ("MNS-008", ["text", "int64"], REFUSE),
    "MNS-009": ("MNS-009", ["text", "int64"], REFUSE),
    "MNS-010": ("MNS-010", ["int64", "notes_post"], SAVE),
    "MNS-012": ("MNS-012", ["xml"], REFUSE),
    "MNS-013": ("MNS-013", ["array"], REFUSE),
    "MNS-014": ("MNS-014", ["limits", "fmt"], ["I1"] + SAVE),
    "MNS-015": ("MNS-015", ["limits", "fmt"], ["I1"] + SAVE),
    "MNS-016": ("MNS-016", ["limits", "omit"], ["I1"] + SAVE),
    "MNS-017": ("MNS-017; REQ-002 added (Invalid text)", ["text", "limits", "grid"], ["I1"] + SAVE),
    "MNS-018": ("MNS-018", ["limits", "fmt"], SAVE),
    "MNS-019": ("MNS-019", ["text", "limits", "fmt"], SAVE),
    "MNS-020": ("MNS-020", ["grid", "fmt"], SAVE),
    "MNS-021": ("MNS-021", ["grid", "fmt"], SAVE),
    "MNS-022": ("MNS-022", ["grid", "fmt"], SAVE),
    "MNS-025": ("MNS-025", ["limits", "grid", "order"], SAVE),
    "MNS-026": ("MNS-026", ["notes_post"], REFUSE),
    "MNS-027": ("MNS-027", ["notes_post"], REFUSE),
    "MNS-028": ("MNS-028", ["notes_post"], SAVE),
    "MNS-029": ("MNS-029", ["notes_post"], SAVE),
    "MNS-030": ("MNS-030", ["notes_post", "attrs"], SAVE),
    "MNS-031": ("MNS-031", ["notes_post"], SAVE),
    "MNS-032": ("MNS-032", ["notes_post"], SAVE),
    "MNS-033": ("MNS-033", ["notes_post"], SAVE),
    "MNS-036": ("MNS-036 narrowed to the outcome (saved text U, PRB-S7-06)", ["order", "notes_post"], ["I4", "I6"]),
    "MNS-039": ("MNS-039", ["event", "list_post", "store_post", "span", "fmt"], SAVE),
    "MNS-040": ("MNS-040", ["event", "fmt"], SAVE),
    "MNS-041": ("MNS-041 (event Value 1 chosen)", ["store_post"], REFUSE),
    "MNS-042": ("MNS-042", ["store_post", "span"], SAVE),
    **{f"MNS-043{v}": (f"MNS-043 variant ({v})", ["list_post", "store_post"], SAVE) for v in "abcdef"},
    **{f"MNS-044{v}": (f"MNS-044 variant ({v})", ["list_post", "store_post", "span"], SAVE) for v in "abc"},
    "MNS-045a": ("MNS-045 variant (a)", ["store_post"], SAVE),
    "MNS-045b": ("MNS-045 variant (b)", ["orphans"], SAVE),
    "MNS-046": ("MNS-046 (event Value 1 chosen)", ["store_post", "orphans"], REFUSE),
    "MNS-047": ("MNS-047", ["list_post", "fmt"], SAVE),
    "MNS-048": ("MNS-048", ["list_post"], SAVE),
    "MNS-049a": ("MNS-049 variant (a)", ["list_post"], SAVE),
    "MNS-049b": ("MNS-049 variant (b)", ["list_post"], SAVE),
    "MNS-050": ("MNS-050", ["span", "store_post"], SAVE),
    "MNS-051a": ("MNS-051 variant (a); REQ-002 added", ["text", "grid", "list_post"], SAVE),
    "MNS-051b": ("MNS-051 variant (b); REQ-002 added", ["text", "grid", "list_post", "span"], SAVE),
    "MNS-052": ("MNS-052 (event Value 1 chosen)", ["orphans", "notes_post"], SAVE),
    "MNS-061": (NEW + "REQ-002 accepted spellings ' 7', '+7', '7 '", ["int64"], SAVE),
    "MNS-062": (NEW + "REQ-002 '+-7'", ["int64"], REFUSE),
    "MNS-063": (NEW + "REQ-002 all-space value", ["int64"], REFUSE),
    "MNS-064": (NEW + "REQ-002 non-ASCII byte", ["int64"], REFUSE),
    "MNS-065": (NEW + "REQ-002 more than 63 characters", ["int64"], REFUSE),
    "MNS-066": (NEW + "REQ-002 value must fit in 64 bits", ["int64"], REFUSE),
    "MNS-067": (NEW + "REQ-002 64-bit text (REQ-TRANSPORT-STATE-004: leading spaces, trailing text)",
                   ["text", "fmt"], SAVE),
    "MNS-068": (NEW + "REQ-002 32-bit text without a numeric prefix", ["text"], REFUSE),
    "MNS-069": (NEW + "REQ-006 and REQ-013 TimeOffset rounding", ["grid", "list_post", "span", "fmt"], SAVE),
    "MNS-070": (NEW + "REQ-010 notes sharing a Time do not refuse", ["order", "notes_post"], ["I4", "I6"]),
    "MNS-071a": (NEW + "REQ-014 CC 31 kept (edge of the excluded 32)", ["list_post", "store_post", "span"], SAVE),
    "MNS-071b": (NEW + "REQ-014 CC 33 kept (edge of the excluded 32)", ["list_post", "store_post", "span"], SAVE),
}


# Review 2026-10-18: I1 established (RVN-01) and recorded as evidence 'gate' on every case that depends on a
# post-read step; REQ-014 clauses 4 and 5 ('span') apply to every saved kept list (RVN-02); I7 applies to every
# base-list fixture (RVN-11).
_POST_READ = {"limits", "notes_post", "store_post", "list_post", "orphans", "span"}
_SPAN_ADDED = {"MNS-040", "MNS-047", "MNS-048", "MNS-049a", "MNS-049b", "MNS-051a"}
_BASE_LIST = {"MNS-039", "MNS-040", "MNS-041", "MNS-042", "MNS-043a", "MNS-043b", "MNS-043c", "MNS-043d",
              "MNS-043e", "MNS-043f", "MNS-044a", "MNS-044b", "MNS-044c", "MNS-045a", "MNS-045b", "MNS-046",
              "MNS-047", "MNS-048", "MNS-049a", "MNS-049b", "MNS-050", "MNS-051a", "MNS-051b", "MNS-052", "MNS-069",
              "MNS-071a", "MNS-071b"}
for _cid, (_src, _ev, _inf) in list(TRACE.items()):
    _ev = _ev + ["span"] * (_cid in _SPAN_ADDED)
    _ev = _ev + ["gate"] * bool(_POST_READ & set(_ev))
    _inf = [i for i in _inf if i != "I1"] + ["I7"] * (_cid in _BASE_LIST)
    TRACE[_cid] = (_src, _ev, _inf)
