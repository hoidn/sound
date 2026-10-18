"""Stage the plugin-discovery-v1 release candidate (analyst side; not reviewed, not released).

Run from any directory with CPython 3.11 and -I:
  python3.11 -I build_pd.py build          # fixtures/ + cases.json + manifest.json (files[] empty)
  python3.11 -I build_pd.py seal           # manifest files[], author-validation.json, traceability.json
  python3.11 -I build_pd.py verify <dir>   # hashes, inventory, links, deny-list of an exported copy

Fixtures are scenario descriptions (JSON): settings plus a directory tree of empty placeholder
directories and empty files. No plug-in, executable or shipped file is read or written. Expected
candidate sets are the hand-authored static derivations in CASES. The seal step cross-checks each one
against model(), a restatement of the released rules over the description. It shares the same static
evidence and is not an oracle. README.md, AGENTS.md and spec.md in the stage directory are hand-written.
"""
import hashlib, itertools, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STAGE = HERE.parent / "plugin-discovery-v1"
TARGET = "Ableton Live 12 Suite 12.4.3 (2026-07-07_e3d8be4d07) / macOS arm64"
PROV = "static-derived; not observed reference output"
U3, L3 = "~/Library/Audio/Plug-Ins/VST3", "/Library/Audio/Plug-Ins/VST3"
U2, L2 = "~/Library/Audio/Plug-Ins/VST", "/Library/Audio/Plug-Ins/VST"
SYSTEM = {"vst3": [U3, L3], "vst2": [U2, L2]}
PDC, PDV = "/Users/Shared/PDC", "/Users/Shared/PDV"
MISS3, MISS2 = "/Users/Shared/PDMissing", "/Users/Shared/PDVMissing"
KEYS = ("system_folders_switch", "custom_folder_switch", "custom_folder")


def st(v3=(True, False, None), v2=(True, False, None)):
    return {"vst3": dict(zip(KEYS, v3)), "vst2": dict(zip(KEYS, v2))}


def D(path, mode=None):
    return {"path": path, "type": "directory", **({"mode": mode} if mode else {})}


def F(path):
    return {"path": path, "type": "file"}


A, B, C = U3 + "/A.vst3", L3 + "/B.vst3", PDC + "/C.vst3"
DD, E, P = U2 + "/D.vst", L2 + "/E.vst", PDV + "/P.vst"
OFF = (False, False, None)

# (number, purpose, requirement suffixes, settings, entries, absent, expected VST3, expected VST2)
CASES = [
    (1, "VST3 bundles in both VST3 system folders", ["002", "004"], st(), [D(A), D(B)], [], [A, B], []),
    (2, "Both VST3 switches off", ["002"], st(v3=OFF), [D(A), D(B)], [], [], []),
    (3, "VST3 system-folder switch off, custom-folder switch on", ["002", "004"], st(v3=(False, True, PDC)),
     [D(A), D(C)], [], [C], []),
    (4, "VST3 system folders and custom folder both on", ["002", "004"], st(v3=(True, True, PDC)),
     [D(A), D(B), D(C)], [], [A, B, C], []),
    (5, "VST3 custom folder set but its switch off", ["002"], st(v3=(True, False, PDC)), [D(A), D(C)], [], [A], []),
    (6, "VST3 custom-folder switch on with no custom folder set", ["002"], st(v3=(True, True, None)),
     [D(A), D(C)], [], [A], []),
    (7, "User VST3 system folder absent", ["002", "004"], st(), [D(B)], [U3], [B], []),
    (8, "VST3 custom folder switched on but missing", ["002", "004"], st(v3=(True, True, MISS3)),
     [D(A)], [MISS3], [A], []),
    (9, "VST2 bundles in both VST2 system folders", ["002", "005"], st(), [D(DD), D(E)], [], [], [DD, E]),
    (10, "User VST2 system folder absent", ["002", "005"], st(), [D(E)], [U2], [], [E]),
    (11, "Both VST2 switches off", ["002"], st(v2=OFF), [D(DD), D(E)], [], [], []),
    (12, "VST2 system-folder switch off, custom-folder switch on", ["002", "005"], st(v2=(False, True, PDV)),
     [D(DD), D(P)], [], [], [P]),
    (13, "VST2 system folders and custom folder both on", ["002", "005"], st(v2=(True, True, PDV)),
     [D(DD), D(E), D(P)], [], [], [DD, E, P]),
    (14, "VST2 custom folder switched on but missing", ["002", "005"], st(v2=(True, True, MISS2)),
     [D(DD)], [MISS2], [], [DD]),
    (15, "Switches of one format do not affect the other", ["002"], st(v3=OFF), [D(A), D(DD)], [], [], [DD]),
    (16, "Bundles in folders that are not searched", ["002"], st(),
     [D("~/Library/Audio/Plug-Ins/Components/X1.vst3"), D("~/Library/Audio/Plug-Ins/X2.vst3"),
      D("~/Library/Audio/Plug-Ins/X3.vst"), D("/Library/Audio/Plug-Ins/Components/X4.vst"),
      D(PDC + "/X5.vst3"), D(PDV + "/X6.vst")], [], [], []),
    (17, "VST3 bundle two levels below a VST3 folder", ["004"], st(), [D(U3 + "/Vendor/Sub/F.vst3")], [],
     [U3 + "/Vendor/Sub/F.vst3"], []),
    (18, "VST3 bundle six levels below a VST3 folder", ["004"], st(), [D(L3 + "/L1/L2/L3/L4/L5/Deep.vst3")], [],
     [L3 + "/L1/L2/L3/L4/L5/Deep.vst3"], []),
    (19, "Directory named G.VST3 (letter case differs)", ["004"], st(), [D(U3 + "/G.VST3")], [], [], []),
    (20, "VST3-named directory nested inside a VST3 candidate", ["004"], st(),
     [D(U3 + "/H.vst3"), D(U3 + "/H.vst3/Contents/Resources/I.vst3")], [], [U3 + "/H.vst3"], []),
    (21, "Empty plain file named J.vst3 beside a bundle", ["004"], st(), [F(U3 + "/J.vst3"), D(A)], [],
     [A, U3 + "/J.vst3"], []),
    (22, "Only the exact text after the last period counts (VST3)", ["004"], st(),
     [D(U3 + "/Multi.Dot.vst3"), D(U3 + "/Space Name.vst3"), D(U3 + "/Backup.vst3.bak"),
      D(U3 + "/Suffix.vst3x"), D(U3 + "/Mixed.Vst3")], [],
     [U3 + "/Multi.Dot.vst3", U3 + "/Space Name.vst3"], []),
    (23, "Directories that are not candidates are searched inside (VST3)", ["001", "004"], st(),
     [D(U3 + "/Wrap.vst"), D(U3 + "/Wrap.vst/Contents/W1.vst3"), D(U3 + "/Wrap.component"),
      D(U3 + "/Wrap.component/W2.vst3"), D(U3 + "/Wrap.clap"), D(U3 + "/Wrap.clap/W3.vst3"),
      D(U3 + "/Backup.vst3.bak"), D(U3 + "/Backup.vst3.bak/W4.vst3")], [],
     [U3 + "/Wrap.vst/Contents/W1.vst3", U3 + "/Wrap.component/W2.vst3", U3 + "/Wrap.clap/W3.vst3",
      U3 + "/Backup.vst3.bak/W4.vst3"], []),
    (24, "VST2 bundle one level below a VST2 folder", ["005"], st(), [D(U2 + "/Vendor/K.vst")], [], [],
     [U2 + "/Vendor/K.vst"]),
    (25, "VST2 bundle six levels below a VST2 folder", ["005"], st(), [D(L2 + "/L1/L2/L3/L4/L5/Deep.vst")], [], [],
     [L2 + "/L1/L2/L3/L4/L5/Deep.vst"]),
    (26, "Directory named L.VST", ["005"], st(), [D(U2 + "/L.VST")], [], [], [U2 + "/L.VST"]),
    (27, "Other letter cases of .vst", ["005"], st(), [D(U2 + "/Mixed.Vst"), D(U2 + "/Odd.vSt")], [], [],
     [U2 + "/Mixed.Vst", U2 + "/Odd.vSt"]),
    (28, "Empty plain file named M.vst", ["005"], st(), [F(U2 + "/M.vst")], [], [], []),
    (29, "VST3-named directory only in a VST2 folder", ["005"], st(), [D(U2 + "/N.vst3")], [], [], []),
    (30, "VST2 folder: a directory named *.vst3 is searched inside", ["005"], st(),
     [D(U2 + "/N2.vst3"), D(U2 + "/N2.vst3/Contents/Y.vst")], [], [], [U2 + "/N2.vst3/Contents/Y.vst"]),
    (31, "VST2-named directory nested inside a VST2 candidate", ["005"], st(),
     [D(U2 + "/Outer.vst"), D(U2 + "/Outer.vst/Contents/Inner.vst")], [], [], [U2 + "/Outer.vst"]),
    (32, "Only the text after the last period counts (VST2)", ["005"], st(),
     [D(U2 + "/Two.Dots.vst"), D(U2 + "/Space Name.vst"), D(U2 + "/Old.vst.bak"), D(U2 + "/Old.vst.bak/Z.vst"),
      D(U2 + "/Inst.vsti")], [], [],
     [U2 + "/Two.Dots.vst", U2 + "/Space Name.vst", U2 + "/Old.vst.bak/Z.vst"]),
    (33, "Unreadable directory beside a readable one (VST2)", ["005"], st(),
     [D(U2 + "/Locked", "000"), D(U2 + "/Locked/Q.vst"), D(U2 + "/Open/O.vst")], [], [], [U2 + "/Open/O.vst"]),
    (34, "Unreadable VST2 system folder", ["005"], st(), [D(L2, "000"), D(L2 + "/R.vst"), D(DD)], [], [], [DD]),
    (35, "CLAP bundles in CLAP, VST3 and VST2 folders", ["001", "002", "004", "005"], st(),
     [D("~/Library/Audio/Plug-Ins/CLAP/Cl1.clap"), D("/Library/Audio/Plug-Ins/CLAP/Cl2.clap"),
      D(U3 + "/Cl3.clap"), D(U2 + "/Cl4.clap")], [], [], []),
]

# ---- analyst-only traceability: release case/clause -> SPEC-PLUGIN-DISCOVERY r1 source, evidence, inferences ----
H1 = "analysis/ableton-live-12.4.3/r2/h1-plugin-scanner-v1/"
N4 = "analysis/ableton-live-12.4.3/r2/n4-helper-contracts-v1/"
C1L = "C1 Live arm64 corpus /var/tmp/sound-analysis/corpus (not retained) "
C1S = "scanner corpus /var/tmp/sound-analysis/helpers/Ableton_Plugin_Scanner/corpus (not retained) "
E = {
    "vst3_folders": N4 + "corpus-code/0x1031c0f28.c (user = 0x103e9e3d8 home + 'Library/Audio/Plug-Ins/VST3' at 0x105be7c71, "
                         "added only for a non-empty home; local = '/Library/Audio/Plug-Ins/VST3' at 0x105be7c92, always); "
                    + C1L + "0x103e9e3d8 chunk-03248 code sha256 bad54697 (NSHomeDirectory)",
    "vst3_switches": N4 + "corpus-code/0x1031c0d2c.c (Boolean 0x1031d3ad4 gates 0x1031c0f28; Boolean 0x1031d3adc gates "
                          "0x1031c0144); called through thunk 0x1031c1208",
    "vst3_custom": N4 + "corpus-code/0x1031c0144.c (handler slot +0x98 path; 'custom' entry only when non-empty; no existence "
                        "check); Live string mpVst3CustomFolderPath 0x1062a784a",
    "vst2_folders": N4 + "corpus-code/0x1031b8e5c.c (user = 0x1030ad96c(2), local = 0x1030ad96c(3), both always added); "
                    + C1L + "0x1030ad96c chunk-02343 sha256 8d034202 (2 -> 0xffff8005, 3 -> 0xffff8003); 0x1030adbbc "
                            "chunk-02343 sha256 95d65a93 (FSFindFolder(domain, 'aplg', 0) + 'VST', kept only if 0x103e970a4 "
                            "passes, else empty); 0x103e970a4 chunk-03247 sha256 9f7983f6 -> 0x103e89910 chunk-03246 sha256 "
                            "1484a935 (status type == 3: is a directory)",
    "vst2_switches": N4 + "corpus-code/0x1031b8c68.c (Boolean +0x30 gates 0x1031b8e5c; Boolean +0x48 gates 0x1031b7f94); "
                          "called through thunk 0x1031b9024",
    "vst2_custom": N4 + "corpus-code/0x1031b7f94.c (as VST3, on the VST2 handler); Live string mpVstCustomFolderPath 0x1062a77c6",
    "argv": "wiki/research/helper-launch-live-side.md#plug-in-scanner argument table (n4-0001 0x103179e68: per format, ID=PATH "
            "items joined with ','; IDs user, local, custom only); " + H1 + "pseudocode/0x1001332fc.c (split on ',', then "
            "first '='); research plugin-scanner-static.md 'The scanner contains no plug-in folder path'",
    "formats": H1 + "pseudocode/0x1001308e0.c (VST3 scan when the --vst3 list is non-empty, then VST2 when --vst2 is "
                    "non-empty); options.json (no CLAP or AU option); Live C2 strings.jsonl sha256 eca20374: no string "
                    "containing '.clap'",
    "vst3_walk": H1 + "pseudocode/0x1005e8cb4.c (per root: recursive iterator option 5; resolved path 0x100674264 + "
                      "0x10067ac78; directory = status type 3 via " + C1S + "0x10066f1e4 chunk-00267 sha256 8ec6565d; a "
                      "directory already in the visited set is not descended; extension 0x1006c4724 compared with '.vst3' "
                      "by 0x100679138; on a match descent is disabled and the resolved path is inserted when its status has "
                      "no error, file or directory; a resolve error logs and continues; a listing error logs 'Reading "
                      "directory failed' and ends that root); " + H1 + "pseudocode/0x1005e9fd8.c lines 89-116 (one root per call)",
    "ext": C1S + "0x1006c4724 chunk-00278 sha256 c6b040ef (file name; '.' and '..' give empty; text from the last '.'; a "
                 "leading-period branch is rendered unreachable); 0x100679138 chunk-00268 sha256 0f1ef4e8 (component-wise "
                 "memcmp with length check: exact match)",
    "vst2_walk": H1 + "pseudocode/0x1005aad10.c (FIFO of roots; visited set on the popped path; per entry: resolved path, "
                      "is-directory 0x10066f240 (" + C1S + "chunk-00267 sha256 d7b11c36), extension 0x1006c4724 lowered by "
                      "0x1006ad5c8 (chunk-00275 sha256 006d11f7; per code point 0x1006b4f14), then length 4 and == '.vst' "
                      "-> candidate map, not queued; other directories queued; non-directories ignored; an open or "
                      "iteration failure logs 'Failed to scan folder' and continues with the queue); "
                 + H1 + "pseudocode/0x1005aca28.c lines 100-121 (one root per call)",
    "session": H1 + "pseudocode/0x1005e9fd8.c and 0x1005aca28.c (no stored module: every candidate is checked); "
                    "0x100138504.c (limit 50; stop when the limit is below the confirmed count: up to 51 per format)",
}
I = {
    "I1": "The user-domain and local-domain Audio Plug-Ins folders returned by the folder service ('aplg', domains "
          "0xffff8005 and 0xffff8003) are ~/Library/Audio/Plug-Ins and /Library/Audio/Plug-Ins (public API semantics; "
          "the returned path is not traced).",
    "I2": "Each format's first Boolean (system pair) and second Boolean (custom entry) are the user's system-folder and "
          "custom-folder switches and can be set independently (gating observed; mapping to the preference keys "
          "Vst3UseSystemFolders etc. and to labelled controls inferred).",
    "I3": "The VST3 recursive listing (option value 5, meaning unresolved) yields every entry of every readable "
          "non-candidate directory at any depth (standard recursive iteration assumed; links and permission errors excluded).",
    "I4": "The VST2 folder lister yields every entry of a readable folder and fails to open a mode-000 folder; the observed "
          "failure path then continues with the next queued folder (lister untraced).",
    "I5": "For trees without symbolic links the resolved path of an entry equals its path, so the tested name is the "
          "entry's own stored name (resolution helper untraced; letter case assumed unchanged).",
}
TRACE = {
    1: ("PD-001 (narrowed: candidates only; listing as effects and load counts excluded)", ["vst3_folders", "vst3_switches", "vst3_walk", "ext", "session"], ["I2", "I3", "I5"]),
    2: ("PD-002 (narrowed: candidates only)", ["vst3_switches", "formats"], ["I2"]),
    3: ("PD-003 (narrowed: candidates only)", ["vst3_switches", "vst3_custom", "vst3_walk"], ["I2", "I5"]),
    4: ("REQ-002 S clause 4 'searched after the system folders' without order (new case)", ["vst3_switches", "vst3_folders", "vst3_custom", "vst3_walk"], ["I2", "I5"]),
    5: ("REQ-002 S clause 4 'with its switch on' (new case)", ["vst3_switches", "vst3_custom"], ["I2"]),
    6: ("REQ-002 S clause 4 'and a custom folder set' (new case)", ["vst3_custom", "vst3_folders"], ["I2"]),
    7: ("REQ-002 S clause 3 last sentence, VST3 analogue (new case; finding F4)", ["vst3_folders", "vst3_walk"], ["I5"]),
    8: ("REQ-002 S clause 4 with a missing custom folder (new case; finding F4)", ["vst3_custom", "vst3_walk"], ["I2"]),
    9: ("PD-005 (narrowed: candidates only)", ["vst2_folders", "vst2_switches", "vst2_walk", "ext", "session"], ["I1", "I2", "I4", "I5"]),
    10: ("PD-006 ('scan completes' not graded)", ["vst2_folders", "vst2_walk"], ["I1", "I4"]),
    11: ("REQ-002 S clause 4 'both switches off' for VST2 (new case)", ["vst2_switches", "formats"], ["I2"]),
    12: ("REQ-002 S clauses 1 and 4 for VST2 (new case)", ["vst2_switches", "vst2_custom", "vst2_walk"], ["I2", "I4"]),
    13: ("REQ-002 S clause 4 for VST2 without order (new case)", ["vst2_switches", "vst2_folders", "vst2_custom", "vst2_walk"], ["I1", "I2", "I4"]),
    14: ("REQ-002 S clause 4 with a missing VST2 custom folder (new case; finding F4)", ["vst2_custom", "vst2_walk", "vst2_folders"], ["I1", "I2", "I4"]),
    15: ("REQ-002 S clause 1 'each format has two independent switches' (new case)", ["vst3_switches", "vst2_switches", "formats"], ["I1", "I2", "I4"]),
    16: ("REQ-002 S clauses 2-4 taken together: no other folder (new case)", ["argv", "formats", "vst3_folders", "vst2_folders"], ["I1"]),
    17: ("PD-008 (narrowed: candidates only)", ["vst3_walk", "ext"], ["I3", "I5"]),
    18: ("REQ-004 S clause 1 'at any depth' (new case)", ["vst3_walk", "ext"], ["I3", "I5"]),
    19: ("PD-009", ["vst3_walk", "ext"], ["I3", "I5"]),
    20: ("PD-010 (narrowed: candidates only)", ["vst3_walk", "ext"], ["I3", "I5"]),
    21: ("PD-011 (narrowed: J is a candidate; listing and scan completion excluded)", ["vst3_walk", "ext"], ["I3", "I5"]),
    22: ("REQ-004 S clause 1 'exact and case-sensitive' and the extension rule (new case)", ["vst3_walk", "ext"], ["I3", "I5"]),
    23: ("REQ-004 S clauses 1-2: non-candidate directories are descended (new case)", ["vst3_walk", "ext"], ["I3", "I5"]),
    24: ("PD-012 (narrowed: candidates only)", ["vst2_walk", "ext"], ["I1", "I4", "I5"]),
    25: ("REQ-005 S clause 1 'every other directory is searched' at depth (new case)", ["vst2_walk", "ext"], ["I1", "I4", "I5"]),
    26: ("PD-013 (narrowed: candidates only)", ["vst2_walk", "ext"], ["I4", "I5"]),
    27: ("REQ-005 S clause 1 'in any letter case' (new case)", ["vst2_walk", "ext"], ["I4", "I5"]),
    28: ("PD-014", ["vst2_walk"], ["I4"]),
    29: ("PD-015", ["vst2_walk", "ext"], ["I4", "I5"]),
    30: ("REQ-005 S clause 1 'including one named *.vst3' (new case)", ["vst2_walk", "ext"], ["I4", "I5"]),
    31: ("REQ-005 S clause 1 'not searched inside' (new case)", ["vst2_walk", "ext"], ["I4", "I5"]),
    32: ("REQ-005 S clause 1 extension rule (new case)", ["vst2_walk", "ext"], ["I4", "I5"]),
    33: ("PD-016 (Q.vst added inside the locked folder; finding F7)", ["vst2_walk"], ["I4"]),
    34: ("REQ-005 S clause 2 'search continues with the remaining folders' for an unreadable root (new case)", ["vst2_folders", "vst2_walk"], ["I1", "I4"]),
    35: ("PD-041 (narrowed: candidates only; extended to /Library CLAP and the VST2 folder)", ["formats", "argv", "vst3_walk", "vst2_walk", "ext"], ["I1", "I3", "I4"]),
}
CLAUSES = {
    "REQ-PLUGIN-DISCOVERY-001 clause 1 (.clap is not a VST3 or VST2 candidate)": ("r1 REQ-001 S clause 3, narrowed to VST3 and VST2 candidates", ["formats", "argv", "vst3_walk", "vst2_walk", "ext"]),
    "REQ-PLUGIN-DISCOVERY-002 clause 1 (two independent switches per format)": ("r1 REQ-002 S clause 1", ["vst3_switches", "vst2_switches"]),
    "REQ-PLUGIN-DISCOVERY-002 clause 2 (VST3 system folders)": ("r1 REQ-002 S clause 2, order dropped (finding F1)", ["vst3_folders"]),
    "REQ-PLUGIN-DISCOVERY-002 clause 3 (VST2 system folders)": ("r1 REQ-002 S clause 3, order dropped (finding F1)", ["vst2_folders"]),
    "REQ-PLUGIN-DISCOVERY-002 clause 4 (custom folder)": ("r1 REQ-002 S clause 4, order dropped", ["vst3_custom", "vst2_custom", "vst3_switches", "vst2_switches"]),
    "REQ-PLUGIN-DISCOVERY-002 clause 5 (both switches off)": ("r1 REQ-002 S clause 4, second sentence", ["vst3_switches", "vst2_switches", "formats"]),
    "REQ-PLUGIN-DISCOVERY-002 clause 6 (no other folder)": ("r1 REQ-002 S clauses 2-4 taken together", ["argv", "formats"]),
    "REQ-PLUGIN-DISCOVERY-002 clause 7 (missing folder)": ("r1 REQ-002 S clause 3 last sentence, generalized (finding F4)", ["vst2_folders", "vst3_walk", "vst2_walk"]),
    "REQ-PLUGIN-DISCOVERY-004 clauses 1-4 (VST3 candidates)": ("r1 REQ-004 S clauses 1-2; resolved-location clause excluded (finding F3)", ["vst3_walk", "ext"]),
    "REQ-PLUGIN-DISCOVERY-005 clauses 1-4 (VST2 candidates)": ("r1 REQ-005 S clauses 1-2; 'level by level' dropped (finding F6); resolved-folder clause excluded", ["vst2_walk", "ext"]),
}

DENY = [r"analysis/", r"wiki/", r"raw/", r"\.\./", r"0x[0-9a-fA-F]{4,}", r"\+0x", r"FUN_", r"disassembl", r"decompil",
        r"pseudocode", r"Ghidra", r"Python", r"boost", r"std::", r"[Ii]terator", r"\bqueue", r"breadth", r"level by level",
        r"visited", r"canonical", r"realpath", r"FSFindFolder", r"NSHomeDirectory", r"\bdomain", r"\b(?:user|local|custom)=",
        r"--(?:vst2|vst3|reset|db|cid|limit|lang|au)\b", r"[Ss]canner", r"\bhelper", r"nanomsg", r"\bSQL", r"[Dd]atabase",
        r"scanstate", r"unconfirmed", r"on-retry", r"not-a-plugin", r"[Ff]ingerprint", r"Vst3?Use", r"mpVst", r"Mediator",
        r"PreferencesModel", r"Live-plugins", r"Failed to scan", r"Reading directory", r"resolve path", r"derivation",
        r"\bPD-\d", r"\bPRB-", r"\bQ-0", r"\bI\d\b", r"\bF\d\b", r"/home/", r"/var/", r"/tmp/", r"ev_[0-9a-f]", r"corpus",
        r"dossier", r"vtable", r"chunk-", r"handler"]
ALLOWED_HITS = {"AGENTS.md": {"decompil"}}  # forbidden-inputs list, same wording as released packages


def sha(b):
    return hashlib.sha256(b).hexdigest()


def cid(n):
    return f"PLUGIN-DISCOVERY-{n:03d}"


def scenario(settings, entries, absent):
    return {"schema": "plugin-discovery-scenario-v1", "settings": settings, "absent": absent, "entries": entries}


def manifest_meta():
    return {
        "schema": "handoff-manifest-v1", "release_id": "plugin-discovery-v1", "release_status": "candidate-unreviewed",
        "release_date": None, "target": TARGET,
        "specification": {"id": "SPEC-PLUGIN-DISCOVERY", "parent_revision": 1, "release_revision": 1},
        "feature_ids": ["FEAT-HOSTING"],
        "partial_requirement_scopes": {
            "REQ-PLUGIN-DISCOVERY-001": "Bundles named *.clap are not VST3 or VST2 candidates in any folder",
            "REQ-PLUGIN-DISCOVERY-002": "Two independent switches per format; VST3 and VST2 system folders; custom folder only with its switch on and a folder set; both off gives no candidates; no other folder searched; a missing folder contributes nothing; order not specified",
            "REQ-PLUGIN-DISCOVERY-004": "VST3 candidates: entries at any depth whose name ends exactly in .vst3, directories and plain files; candidates not searched inside; every other directory searched",
            "REQ-PLUGIN-DISCOVERY-005": "VST2 candidates: directories at any depth whose name ends in .vst in any ASCII letter case; not searched inside; every other directory searched, including *.vst3; plain files never; unreadable directories skipped and the search continues",
        },
        "unreleased_requirements": [f"REQ-PLUGIN-DISCOVERY-{n:03d}" for n in (3, *range(6, 17))],
        "compatibility_dimensions": {
            "discovery-candidate-selection": "static-derived expectations; reference execution not-run",
            "examination-order": "excluded (REQ-PLUGIN-DISCOVERY-003)",
            "plugin-listing-and-classification": "excluded (REQ-PLUGIN-DISCOVERY-006, 007)",
            "persistence-change-and-rescan": "excluded (REQ-PLUGIN-DISCOVERY-008 to 010, 016)",
            "ui": "excluded (REQ-PLUGIN-DISCOVERY-011; control labels and defaults)",
            "failure-and-scale": "excluded (REQ-PLUGIN-DISCOVERY-012 to 015)",
            "audio": "excluded", "timing": "excluded",
        },
        "exclusions": {
            "inputs_without_expectation": [
                "symbolic links anywhere in a tree or in a folder path; entries other than directories and plain files",
                "names or folder paths with characters other than ASCII letters, digits, space, hyphen, underscore, period and the path separator, including a comma; names beginning with a period",
                "custom folders that are not absolute or that end with a separator; folder paths that name a plain file",
                "paths longer than 255 bytes once ~ is expanded",
                "permissions other than the description form (normal access, or mode 000 on a directory as allowed)",
                "in a VST3 folder, any directory that cannot be read; any permission change on an entry whose name ends in .vst3 or .vst in any letter case",
                "folders of one format that are equal or nested, including a custom folder at or below a system folder of its format",
                "more than 50 candidates of one format",
                "a home folder other than the account's own, including a different HOME environment value; stored letter case of a folder path that differs from this release",
                "trees changed while a scan runs",
            ],
            "behavior": [
                "examination order, including VST3 before VST2 and the order of folders (REQ-PLUGIN-DISCOVERY-003)",
                "what a candidate contributes: listing, names, instrument or effect, code signatures, entry points (REQ-PLUGIN-DISCOVERY-006, 007)",
                "later scans: unchanged, changed, removed and returning modules; Rescan and its reset variant; quitting during a scan (REQ-PLUGIN-DISCOVERY-008 to 010, 016)",
                "progress information and its presentation (REQ-PLUGIN-DISCOVERY-011)",
                "crashing and hanging modules, more than 50 new modules, duplicates (REQ-PLUGIN-DISCOVERY-012 to 015)",
                "Audio Unit discovery; process isolation; activation of plug-in sources (REQ-PLUGIN-DISCOVERY-001 remainder)",
                "control labels, defaults, effects of changing a switch or custom folder, when scans start, custom folders containing a comma (REQ-PLUGIN-DISCOVERY-002 remainder)",
                "symbolic links and unreadable subfolders in VST3 folders; the folder structure presented to the user (REQ-PLUGIN-DISCOVERY-004, 005 remainder)",
            ],
        },
        "fixture_origin": "independently authored scenario descriptions (settings and a tree of empty placeholder directories and empty files); no plug-in, executable, bundle content or shipped file",
        "approved_public_sources": [],
        "review": {"status": "pending", "reviewers": [], "date": None, "findings": [], "disposition": None, "record": None},
        "supersedes": None, "entrypoint": "README.md", "case_count": len(CASES),
        "inventory_excludes": ["manifest.json (self-hash recorded outside package)"],
        "files": [],
    }


def build():
    (STAGE / "fixtures").mkdir(parents=True, exist_ok=True)
    cases = []
    for n, purpose, reqs, settings, entries, absent, exp3, exp2 in CASES:
        rel = f"fixtures/{cid(n)}.json"
        (STAGE / rel).write_text(json.dumps(scenario(settings, entries, absent), indent=1) + "\n")
        cases.append({"id": cid(n), "purpose": purpose, "requirements": [f"REQ-PLUGIN-DISCOVERY-{r}" for r in reqs],
                      "input": rel, "expected": {"vst3_candidates": sorted(exp3), "vst2_candidates": sorted(exp2)},
                      "expectation_provenance": PROV, "reference_execution": "not-run", "candidate_execution": "not-run",
                      "comparator": "per format, set of candidate paths exact; order and examination count not compared"})
    doc_ = {"schema": "plugin-discovery-cases-v1", "target": TARGET,
            "scope": "plugin-discovery-v1 partial requirement clauses only (see spec.md)", "status": "candidate-unreviewed",
            "fixture_origin": "Independently authored scenario descriptions; no plug-in or shipped file",
            "oracle_status": "Static-derived expectations; neither reference nor candidate executed",
            "representation": {
                "vst3_candidates": "sorted paths, in the description's form, of the entries examined as VST3 modules",
                "vst2_candidates": "sorted paths, in the description's form, of the entries examined as VST2 modules",
                "note": "project comparison representation, not an API of the original application or a required design"},
            "cases": cases}
    (STAGE / "cases.json").write_text(json.dumps(doc_, indent=1) + "\n")
    (STAGE / "manifest.json").write_text(json.dumps(manifest_meta(), indent=1) + "\n")
    print(len(cases), "cases staged")


# ---- cross-check model: the released rules restated over a scenario description ----
class NoExpectation(Exception):
    pass


NAME = re.compile(r"[A-Za-z0-9 _.-]+")


def check_path(p):
    head, *names = p.split("/")
    if head not in ("", "~") or not names or p.endswith("/"):
        raise NoExpectation(f"path form {p!r}")
    for name in names:
        if not NAME.fullmatch(name) or name.startswith("."):
            raise NoExpectation(f"name {name!r}")


def tree(sc):
    nodes = {}
    for e in sc["entries"]:
        p, typ, mode = e["path"], e["type"], e.get("mode")
        check_path(p)
        if typ not in ("directory", "file") or mode not in (None, "000") or (mode and typ != "directory"):
            raise NoExpectation(f"entry kind {e}")
        parts = p.split("/")
        for i in range(2, len(parts)):
            anc = "/".join(parts[:i])
            if nodes.get(anc, ("directory",))[0] != "directory":
                raise ValueError(f"inconsistent tree at {anc}")
            nodes.setdefault(anc, ("directory", None))
        if p in nodes and (nodes[p] != ("directory", None) or typ != "directory"):
            raise ValueError(f"duplicate entry {p}")
        nodes[p] = (typ, mode)
    for a in sc["absent"]:
        check_path(a)
        if any(q == a or q.startswith(a + "/") for q in nodes):
            raise ValueError(f"absent path {a} has content")
    return nodes


def folders(sc, fmt):
    s = sc["settings"][fmt]
    r = (SYSTEM[fmt] if s["system_folders_switch"] else []) + \
        ([s["custom_folder"]] if s["custom_folder_switch"] and s["custom_folder"] else [])
    for p in r:
        check_path(p)
    for a, b in itertools.combinations(r, 2):
        if a == b or a.startswith(b + "/") or b.startswith(a + "/"):
            raise NoExpectation("nested or equal folders of one format")
    return r


def children(nodes, p):
    return sorted(q for q in nodes if q.rsplit("/", 1)[0] == p)


def vst3(nodes, root):
    if nodes.get(root, ("file",))[0] != "directory":
        return []  # absent (or empty, which is the same) folder
    out, stack = [], [root]
    while stack:
        p = stack.pop()
        if nodes[p][1]:
            raise NoExpectation("unreadable directory in a VST3 folder")
        for c in children(nodes, p):
            typ, mode = nodes[c]
            if c.rsplit("/", 1)[1].endswith(".vst3"):
                out.append(c)
            elif typ == "directory":
                stack.append(c)
    return out


def vst2(nodes, root):
    if nodes.get(root, ("file",))[0] != "directory":
        return []
    out, todo = [], [root]
    while todo:
        p = todo.pop()
        if nodes[p][1] == "000":
            continue  # unreadable: skipped, the search continues
        for c in children(nodes, p):
            if nodes[c][0] != "directory":
                continue
            if c.rsplit("/", 1)[1].lower().endswith(".vst"):
                out.append(c)
            else:
                todo.append(c)
    return out


def model(sc):
    nodes = tree(sc)
    for p, (typ, mode) in nodes.items():
        if mode and re.search(r"\.vst3?$", p.rsplit("/", 1)[1], re.I):
            raise NoExpectation("permission change on a bundle-named entry")
    res = {}
    for fmt, walk in (("vst3", vst3), ("vst2", vst2)):
        found = sorted({c for root in folders(sc, fmt) for c in walk(nodes, root)})
        if len(found) > 50:
            raise NoExpectation("more than 50 candidates")
        res[f"{fmt}_candidates"] = found
    return res


def probes():
    """Excluded inputs must be rejected by the model rather than given an expectation."""
    base = st()
    bad = {
        "symbolic link": scenario(base, [{"path": U3 + "/S.vst3", "type": "symlink"}], []),
        "comma in custom folder": scenario(st(v3=(True, True, "/Users/Shared/pd,c")), [D("/Users/Shared/pd,c/C.vst3")], []),
        "name beginning with a period": scenario(base, [D(U3 + "/.vst3")], []),
        "non-ASCII name": scenario(base, [D(U3 + "/Café.vst3")], []),
        "custom folder inside a system folder": scenario(st(v3=(True, True, U3 + "/Sub")), [D(U3 + "/Sub/C.vst3")], []),
        "unreadable directory in a VST3 folder": scenario(base, [D(U3 + "/Locked", "000"), D(A)], []),
        "permission change on a bundle-named entry": scenario(base, [D(U2 + "/K.vst", "000")], []),
        "51 candidates": scenario(base, [D(f"{U3}/M{i}.vst3") for i in range(51)], []),
        "relative custom folder": scenario(st(v2=(True, True, "Shared/PDV")), [D(DD)], []),
    }
    out = {}
    for k, sc in bad.items():
        try:
            out[k] = f"NOT REJECTED: {model(sc)}"
        except NoExpectation as e:
            out[k] = f"rejected ({e})"
    return out


# ---- checks ----
def payload(d):
    return sorted(p for p in d.rglob("*") if p.is_file() and p.name != "manifest.json")


def links(md_path, root):
    out = []
    for target in re.findall(r"\]\(([^)\s]+)\)", md_path.read_text()):
        if re.match(r"[a-z]+:", target):
            out.append((target, "external URL not allowed"))
            continue
        path, _, anchor = target.partition("#")
        dest = (md_path.parent / path).resolve() if path else md_path
        ok = dest.is_file() and root.resolve() in dest.parents
        if ok and anchor:
            slugs = {re.sub(r"[^\w\- ]", "", h.strip().lower()).replace(" ", "-")
                     for h in re.findall(r"^#+ (.+)$", dest.read_text(), re.M)}
            ok = anchor in slugs
        out.append((target, "ok" if ok else "UNRESOLVED"))
    return out


def verify(d):
    d = Path(d)
    man = json.loads((d / "manifest.json").read_text())
    files = payload(d)
    mismatches = [f["path"] for f in man["files"] if not (d / f["path"]).is_file()
                  or sha((d / f["path"]).read_bytes()) != f["sha256"] or (d / f["path"]).stat().st_size != f["bytes"]]
    inventory = sorted({str(p.relative_to(d)) for p in files} ^ {f["path"] for f in man["files"]})
    link_rows = {str(p.relative_to(d)): links(p, d) for p in d.glob("*.md")}
    bad_links = {k: [t for t, s in v if s != "ok"] for k, v in link_rows.items() if any(s != "ok" for _, s in v)}
    cases = json.loads((d / "cases.json").read_text())["cases"]
    missing_inputs = [c["input"] for c in cases if not (d / c["input"]).is_file()]
    deny = {}
    for p in [*files, d / "manifest.json"]:
        text = p.read_text()
        hits = sorted({m if isinstance(m, str) else m[0] for pat in DENY for m in re.findall(pat, text)})
        hits = [h for h in hits if not any(h.startswith(a) for a in ALLOWED_HITS.get(p.name, ()))]
        if hits:
            deny[str(p.relative_to(d))] = hits
    symlinks = [str(p.relative_to(d)) for p in d.rglob("*") if p.is_symlink()]
    return {"dir": str(d), "payload_files": len(files), "files_including_manifest": len(files) + 1,
            "manifest_sha256": sha((d / "manifest.json").read_bytes()), "hash_or_size_mismatches": mismatches,
            "inventory_differences": inventory, "markdown_links": {k: len(v) for k, v in link_rows.items()},
            "unresolved_links": bad_links, "missing_case_inputs": missing_inputs, "deny_list_hits": deny,
            "symlinks": symlinks, "allowed_hits": {k: sorted(v) for k, v in ALLOWED_HITS.items()}}


def seal():
    cases = json.loads((STAGE / "cases.json").read_text())["cases"]
    problems, fixtures = {}, {}
    for c in cases:
        raw = (STAGE / c["input"]).read_bytes()
        errs = []
        if not raw.isascii() or b"\r" in raw or not raw.endswith(b"\n") or b"\t" in raw:
            errs.append("fixture not ASCII with LF endings")
        sc = json.loads(raw)
        try:
            got = model(sc)
        except NoExpectation as e:
            got = f"no expectation: {e}"
        if got != c["expected"]:
            errs.append(f"model {got} != expected")
        if errs:
            problems[c["id"]] = errs
        fixtures[c["id"]] = {"bytes": len(raw), "entries": len(sc["entries"]), "absent": len(sc["absent"]),
                             "candidates": len(c["expected"]["vst3_candidates"]) + len(c["expected"]["vst2_candidates"])}
    distinct = len({(STAGE / c["input"]).read_bytes() for c in cases})
    man = json.loads((STAGE / "manifest.json").read_text())
    man["files"] = [{"path": str(p.relative_to(STAGE)), "sha256": sha(p.read_bytes()), "bytes": p.stat().st_size}
                    for p in payload(STAGE)]
    (STAGE / "manifest.json").write_text(json.dumps(man, indent=1) + "\n")
    report = {"schema": "author-validation-v1", "package": "plugin-discovery-v1 (staged candidate)",
              "python": sys.version.split()[0], "cases": len(cases), "distinct_fixtures": distinct,
              "case_problems": problems, "exclusion_probes": probes(), "fixtures": fixtures, **verify(STAGE),
              "limits": "Checks authored consistency only: no reference or candidate executed; the model restates the "
                        "same static evidence and is not an oracle."}
    (HERE / "author-validation.json").write_text(json.dumps(report, indent=1) + "\n")
    trace = {"schema": "plugin-discovery-traceability-v1", "spec": "SPEC-PLUGIN-DISCOVERY r1",
             "evidence_identity": {"scanner_arm64_slice_sha256": "6ce847b0f56d842d638ca638546636ecdba66f5942fa668f4d2d3403f2a97ad6",
                                   "live_arm64_sha256": "3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad",
                                   "h1_manifest_sha256": sha((HERE.parents[1] / "r2/h1-plugin-scanner-v1/manifest.json").read_bytes()),
                                   "n4_manifest_sha256": sha((HERE.parents[1] / "r2/n4-helper-contracts-v1/manifest.json").read_bytes())},
             "evidence": E, "inferred_links": I,
             "clauses": {k: {"source": s, "evidence": ev} for k, (s, ev) in CLAUSES.items()},
             "cases": {cid(n): {"source": src, "evidence": ev, "inferred": inf} for n, (src, ev, inf) in TRACE.items()}}
    assert set(trace["cases"]) == {c["id"] for c in cases}
    assert all(k in E for v in [*TRACE.values()] for k in v[1]) and all(k in E for _, ev in CLAUSES.values() for k in ev)
    (HERE / "traceability.json").write_text(json.dumps(trace, indent=1) + "\n")
    print(json.dumps({k: report[k] for k in ("cases", "distinct_fixtures", "case_problems", "exclusion_probes",
                                             "payload_files", "hash_or_size_mismatches", "inventory_differences",
                                             "unresolved_links", "missing_case_inputs", "deny_list_hits", "symlinks",
                                             "manifest_sha256")}, indent=1))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "verify":
        print(json.dumps(verify(sys.argv[2]), indent=1))
    else:
        {"build": build, "seal": seal}[cmd]()
