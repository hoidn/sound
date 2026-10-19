"""Analyst-only traceability for automation-envelopes-v2 (never shipped). build_v2.py seal writes traceability.json.

Release case -> SPEC-AUTOMATION-ENVELOPES r4 case or clause, evidence locators and residual inferences; clause
disposition; value-case disposition (A1 per target, evaluator, playback); spec findings found while staging.
"""
import trace_aen as v1t  # v1 evidence keys (S6, N1), reused unchanged

A = "analysis/ableton-live-12.4.3/"
T11 = A + "r2/t11-structure-v1/"
HERE = A + "handoff-staging/automation-envelopes-v2-analysis/"
EV = dict(v1t.EV)
EV.update({
    "open_walk": T11 + "traces/a1a2/trace.txt (A1 settled: XML reader load step runs member post-load steps when context "
                 "+0x2c is set, which the XML reader's context sets, then the validation walk unconditionally; "
                 "x86 0x10147e23c-0x10147e26d); SPEC-LIVE-SET-STRUCTURE r1 A1 ('also settles SPEC-AUTOMATION-ENVELOPES's A3')",
    "structure": T11 + "released-fixture-audit.json (automation-envelopes-v1: REQ-006 refusal in all 21, minimal and "
                 "recommended additions); schema_check.py, fixture_audit.py; " + HERE + "t11-fixture-audit.json, "
                 "t11-schema-check.jsonl (v2 fixtures: no refusal, no unknown shape, no deviation)",
    "purge": HERE + "purge-excerpts.jsonl (arm64 corpus pseudocode, line SHA-256 re-checked by seal): LSong::AfterRead "
             "0x102695f78 per track, gate app+0x350 (0x10185138c), -> 0x102711584 -> clip purge 0x102456e98 -> "
             "0x1024559b8 (removed when relation 0x1024dd434 fails or event count == 1, 'empty') and track purge "
             "0x102406378 (removed when relation fails, or count <= 1 via AListAutomation +0x2b8 = 0x1025619e0 "
             "'1 < count', unless the target's +0x1e8 object reports +0x338 true; untraced); count = slot +0x398 "
             "0x1025654e8 over (-DBL_MAX, DBL_MAX) = list size; these run inside the root post-load, before the walk "
             "(T11 traces/a1a2) that applies REQ-007; vtable slots +0x2b8, +0x398 of AListAutomation 0x1067d06b8 in "
             "r2/s6-automation-v1/vtable-reads.txt lines 138, 166",
    "timeline": A + "r2/s6-automation-v1/vtable-reads.txt (AListAutomation +0x100 no-op 0x101487c3c); check reached "
                "only from AAutomationEnvelope +0x100 0x1024050d8 and AClipEnvelope +0x100 0x10245194c (s6-0003); "
                "schema TimeableMidiClip.ArrangerAutomation = ListAutomation; shipped sets hold empty timeline lists "
                "(documents-survey; SPEC-AUTOMATION-ENVELOPES r4 REQ-007 D)",
    "text_save_v2": "transport-state-v2 released REQ-TRANSPORT-STATE-011 step 1 (binary64 log10, band, assumption; "
                    "X: r2/x2-transport-v1/results/writer.json); SPEC-AUTOMATION-ENVELOPES r4 REQ-012 defers to it",
})
INF = {
    "I3": v1t.INF["I3"] + " Stated in the contract (assumption 1).",
    "I4": "Settled since v1 (no longer an assumption): opening a Live Set runs the validation walk ('open_walk').",
    "I5": v1t.INF["I5"] + " Stated in the contract (assumption 2).",
    "I7": "No other owner of an event list applies the REQ-007 check, and no open step refuses an empty "
          "ClipTimeable/ArrangerAutomation/Events; the post-load slots of TimeableMidiClip were not read "
          "(SPEC-AUTOMATION-ENVELOPES r4 REQ-007 timeline assumption). Stated in the contract (assumption 3).",
    "I8": "Envelopes with at least two events on a parameter of their own track's mixer or MIDI controllers are "
          "not removed by the further envelope removal on open ('purge'): the count test does not apply, and the "
          "relation test holds for these targets (SPEC-LIVE-SET-STRUCTURE REQ-014 fixture rule). An empty clip "
          "envelope is not removed (count != 1). Residual: the relation test was not evaluated for these targets.",
}
TRACE = {
    "AUTOMATION-ENVELOPES-001": ("v1 001 (AEN-003)", ["containers", "targets", "classes", "text_save", "structure"], ["I5", "I8"]),
    "AUTOMATION-ENVELOPES-002": ("v1 002 (AEN-032); opens whether or not the one-event envelope is removed", ["validate", "leading", "purge", "structure"], []),
    "AUTOMATION-ENVELOPES-005": ("v1 005 (AEN-006)", ["validate", "open_walk", "structure"], ["I8"]),
    "AUTOMATION-ENVELOPES-006": ("v1 006 (AEN-007)", ["validate", "text_load", "open_walk", "structure"], ["I8"]),
    "AUTOMATION-ENVELOPES-007": ("v1 007", ["validate", "text_load", "open_walk", "structure"], ["I8"]),
    "AUTOMATION-ENVELOPES-008": ("v1 008 (AEN-008)", ["validate", "open_walk", "structure"], ["I8"]),
    "AUTOMATION-ENVELOPES-009": ("v1 009 (AEN-009)", ["validate", "order", "open_walk", "structure"], ["I8"]),
    "AUTOMATION-ENVELOPES-010": ("v1 010 (clip positive control)", ["containers", "targets", "validate", "open_walk", "structure"], ["I8"]),
    "AUTOMATION-ENVELOPES-012": ("v1 012 (AEN-011); empty clip envelope kept by the further removal", ["validate", "open_walk", "purge", "structure"], ["I8"]),
    "AUTOMATION-ENVELOPES-013": ("v1 013 (AEN-027)", ["text_load", "structure"], []),
    "AUTOMATION-ENVELOPES-014": ("v1 014", ["text_load", "classes", "structure"], ["I3"]),
    "AUTOMATION-ENVELOPES-015": ("v1 015", ["text_load", "classes", "structure"], ["I3"]),
    "AUTOMATION-ENVELOPES-016": ("v1 016 (AEN-026)", ["text_load", "text_save", "text_save_v2", "structure"], ["I5", "I8"]),
    "AUTOMATION-ENVELOPES-017": ("v1 017 (AEN-012)", ["curve_save", "curve_load", "structure"], ["I5", "I8"]),
    "AUTOMATION-ENVELOPES-018": ("v1 018 (AEN-013)", ["curve_save", "curve_load", "text_save", "text_save_v2", "structure"], ["I5", "I8"]),
    "AUTOMATION-ENVELOPES-019": ("v1 019", ["curve_save", "curve_load", "structure"], ["I5", "I8"]),
    "AUTOMATION-ENVELOPES-020": ("v1 020", ["curve_save", "curve_load", "structure"], ["I5", "I8"]),
    "AUTOMATION-ENVELOPES-021": ("v1 021", ["classes", "targets", "text_save", "structure"], ["I3", "I5", "I8"]),
    "AUTOMATION-ENVELOPES-030": ("new: replaces v1 003 (AEN-004) with two events so the further removal cannot apply", ["validate", "open_walk", "purge", "structure"], ["I8"]),
    "AUTOMATION-ENVELOPES-031": ("new: replaces v1 011 (AEN-010) with two events", ["validate", "open_walk", "purge", "structure"], ["I8"]),
    "AUTOMATION-ENVELOPES-032": ("new: AEN-033 on the v1 case-010 document (r4's T0) plus the T11 additions", ["timeline", "validate", "open_walk", "structure"], ["I7", "I8"]),
}
NOT_CARRIED = {
    "AUTOMATION-ENVELOPES-003": "track envelope, one event at 4, expected refused (AEN-004): the further removal on open "
                                "removes a track envelope with at most one event unless an untraced target flag is set, "
                                "before the REQ-007 check ('purge'); outcome not established (probably opens)",
    "AUTOMATION-ENVELOPES-004": "track envelope, no event, expected refused (AEN-005): as 003",
    "AUTOMATION-ENVELOPES-011": "clip envelope, one event at 4, expected refused (AEN-010): the clip removal applies to "
                                "exactly one event ('purge'); by that reading the document opens",
}
CLAUSES = {
    "001": "v1 clauses + timeline clause (r2, REQ-001 D and REQ-007 S with assumption I7)",
    "002, 003, 006, 008, 009": "v1 clauses unchanged",
    "005": "v1 clause restated: opens; whether kept excluded ('purge')",
    "007": "clause 1 narrowed to clip envelopes; clause 2 to envelopes with >= 2 events; A3 settled (I4); timeline clause added",
    "012": "load rules as v1; save step 1 corrected to the binary64 logarithm (transport-state-v2; r4 defers to REQ-TRANSPORT-STATE-011)",
    "004, 010, 011, 013": "unreleased (value disposition below; 013 U)",
}
VALUES = {
    "A1_by_target": {
        "Pan": "identity on [-1, 1] (X2 A1_pan_converter_slot0x28_on_range; r4 A1 'X for Pan'); same value if the "
               "owner condition (SPEC-MIX-GRAPH A3) fails, since revision 3's identity reading also gives stored units",
        "Speaker, CrossFadeState": "no conversion (discrete interpolator requests none; X, r3/r4 REQ-011)",
        "ControllerTargets.6": "clip envelope; clip time base U (REQ-010), so no value case either way",
        "Volume, Send": "fader positions, S-cond on SPEC-MIX-GRAPH A3 (Q-019, Q-023 open): excluded; no fixture "
                        "has a Volume or Send target",
    },
    "evaluator_E(t)": "not released: r4 A2 says which user-visible reading shows E(t) is untraced (callers of the "
                      "evaluator entry), and playback does not apply E(t) to Float envelopes; no observable framing "
                      "exists without a traced reading",
    "playback_P(t)": "not released: every playback expectation rests on SPEC-MIX-GRAPH A8 (that a loaded track's "
                     "arrangement envelopes drive its parameters; initial automation index inferred), an open item "
                     "of Q-023; values are delivered through ramps (REQ-MIX-GRAPH-014, S (A6)) whose last ramp before "
                     "a point holds within one data step and whose per-sample interpolation is untraced, so the "
                     "applied value at a sample is not established to 32 bits; and playback is a runtime clause",
    "r4 cases": "AEN-015 to 025 not released; AEN-014 (reset of non-monotone controls) not released: r4 REQ-009 "
                "marks enablement U (finding SF-2)",
}
FINDINGS = {
    "SF-1": "r4 A3 and REQ-007's 'S (A3)' are stale: SPEC-LIVE-SET-STRUCTURE r1 A1 (settled) says it settles A3 for Live Sets",
    "SF-2": "r4 REQ-009 'U whether opening runs the normalization': its named static route is the reading context's "
            "post-load flag (+0x2c, getter 0x1015192c0 = the gate cited in r4's appendix), which T11's A1 trace shows set "
            "on every Live Set open; the reset to 0.5 (AEN-014 save part) looks static-derivable",
    "SF-3": "r4 REQ-007 omits the further envelope removal of the song post-load (SPEC-LIVE-SET-STRUCTURE REQ-014 U), "
            "which runs before the walk: track envelopes with <= 1 event (unless an untraced target flag) and clip "
            "envelopes with exactly 1 event are removed. REQ-007's refusals then fail for AEN-004, 005, 010 and the "
            "v1 cases 003, 004, 011; AEN-011 (empty clip) still refused; AEN-032 opens either way",
    "SF-4": "r4 AEN-033 is set on T0 (the v1 case-010 fixture), which the structural rules refuse (no freeze sequencer); "
            "v2 case 032 adds the T11 lines",
    "SF-5": "r4 'Released automation-envelopes-v1 is not contradicted' no longer holds (T11 audit; SF-3)",
    "SF-6": "r4's value comparator gives playback values exact at 32 bits, but REQ-MIX-GRAPH-014 delivers them through "
            "ramps (last ramp before a point within one data step; per-sample interpolation untraced): the playback "
            "column is the segment value P(t), not necessarily the applied value at a sample",
}


def trace(ids):
    cases = {i: {"source": s, "evidence": {k: EV[k] for k in ev}, "inferred": {k: INF[k] for k in inf}}
             for i, (s, ev, inf) in TRACE.items()}
    assert set(cases) == set(ids), set(cases) ^ set(ids)
    return {"schema": "automation-envelopes-traceability-v2", "spec": "SPEC-AUTOMATION-ENVELOPES r4",
            "superseded": "automation-envelopes-v1 (traceability: ../automation-envelopes-v1-analysis/traceability.json)",
            "evidence": EV, "inferred_links": INF, "cases": cases, "not_carried": NOT_CARRIED, "clauses": CLAUSES,
            "value_disposition": VALUES, "spec_findings": FINDINGS}
