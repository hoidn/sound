"""Analyst-only traceability data for browser-index-v1 (never shipped): release case -> SPEC-BROWSER-INDEX r1
case or clause, evidence locators and inferred links. Imported by build_bi.py (seal)."""

D2R = "analysis/ableton-live-12.4.3/r2/d2-browser-index-v1/cited-functions.jsonl"
H2R = "analysis/ableton-live-12.4.3/r2/h2-index-v1/"
ADR = "analysis/ableton-live-12.4.3/handoff-staging/browser-index-v1-analysis/kept/corpus-addendum.jsonl"
E = {
    "registry": H2R + "out/file-type-registry.tsv (80 registrations: four-character code, extensions)",
    "kindmap": D2R + " 0x10016b758 (type code -> kind bit; unknown code logs 'Unknown file typeId' and returns 0), "
               "evaluated for all 80 codes by compiling the pseudocode (kindmap_eval in crosscheck_bi.py); "
               "0x100289f8c names it MapFileTypeToFileKind; 0x10016b3e8 bit names",
    "gate": D2R + " 0x1006e6d40 (parent leaf == 'Ableton Folder Info' constant DAT_100e2add0, else parent == override "
            "folder 0x1006e5d68); reader 0x1006d2624 calls the gate first and returns an empty result when it fails",
    "reader": D2R + " 0x1006d2624 (parse 0x1006e4778; error -> 'Error reading xmp file: ' and empty result; resource "
              "kind 1 branch: R = parent(parent(sidecar)), items applied only when R is an indexed folder)",
    "caller": ADR + " 0x10013f420 (single caller of 0x1006d2624; pops a queued path; enqueueing untraced)",
    "items": D2R + " 0x1006ee124 (item fields filePath, colors, keywords, hideKeywords, assetId, contentHash), 0x1006e34b4",
    "keywords": D2R + " 0x1006ed554 (array items; empty skipped; inserted into a set)",
    "colors_read": D2R + " 0x1006ed324 (std::stoul base 10; value-1 < 7 sets bit; empty skipped; conversion failure "
                   "path untraced)",
    "colors_write": D2R + " 0x1006edbbc (bits 1..7 -> to_string 1..7 appended in ascending order)",
    "item_write": D2R + " 0x1006ef218 (deletes colors, keywords, hideKeywords, assetId, contentHash; writes colors if "
                  "non-zero, keywords and hideKeywords if present; assetId and contentHash under an untraced condition)",
    "folder_writer": D2R + " 0x1006d03b8 (sidecar path 0x1006e637c mode 1; reuses an existing parsable folder sidecar, "
                     "else new 0x1006e4394; entry key = leaf name of the item path via 0x10075f5c0; write 0x1006cce78)",
    "new_doc": ADR + " 0x1006e4394 -> 0x1006f07c8(kind 1, platform 2) -> header 0x1006f09d8; tables decoded with "
               "h2 read_ptrs.py: format 0x100dbd650 ['', folder, factory-pack, plugin-device, app-builtin], resource "
               "0x100dbd678 [folder, pack, plugin, app-builtin], platform 0x100dbd698 [win, mac, linux]",
    "file_write": ADR + " 0x1006cce78 (skips 0x1006e71c8 paths; empty document -> 'Remove empty Metadata file' and "
                  "empty parent removal; else create_directories(parent) 0x10070aa50 then serialize 0x1006e5140)",
    "names": D2R + " 0x1006e637c (uuid5(uuid5(nil,'folder'),'.')), 0x1006e60e4 (uuid text + type 68 '.xmp'), "
             "0x1006efb30 and 0x1006f02dc (uuid5), recomputed with Python uuid.uuid5",
    "factory": D2R + " 0x1006e5f48 (uuid5(uuid5(nil,'factory-pack'), id) under 0x1006e5d68 = base/'Ableton Folder "
               "Info'/to_string(0x1001c2380())), writer 0x1006cf838 (base from a config accessor; 'No UserLibrary.  "
               "Can't write factory pack metadata'; entry key relative to the pack root)",
    "builtin": D2R + " 0x1006e67dc (uuid5(uuid5(nil,'app-resource'),'builtin') under 0x1006e5d68)",
    "legacy_names": "shipped Legacy Pack Data sidecars: name == uuid5(c55d131f..., packUniqueId) for 159 of 160 "
                    "(recomputed in seal when the application copy is present)",
    "core_id": "shipped Core Library sidecar c55d131f-2661-5add-aece-29afb7099dfa.xmp, ablFR:packUniqueId "
               "www.ableton.com/0 (read 2026-10-18)",
    "binding": "reviewer static check (browser-index-v1-analysis/review/binding_check.py): the folder-resource branch "
               "of reader 0x1006d2624 enumerates index slot 0x108 -> interface slot 0x38 = 0x100288fc8 -> 0x1002af190, "
               "'SELECT ... FROM files WHERE parent_id = :parentid AND file_kind & 0x300 = 0' (files directly in F, no "
               "folders), keyed by normalized name (0x10071eb3c) and looked up in the entry map (0x1006dd9a8, "
               "0x1006de554) by apply step 0x1006dbf98; the pack branch uses slot 0x40 = 0x1002890e0 -> 0x1002af23c "
               "(ancestors, any depth); unmatched entries removed by 0x1006e3fc8",
    "shipped": H2R + "out/shipped-inventory.json (162 sidecars; per_file resolution; no xpacket)",
}
I = {
    "I1": "The indexer passes each sidecar file of a location's sidecar folder to the reader when it indexes the "
          "location. Only the reader and its single caller (a queue pop) are read; the enqueueing is untraced. "
          "Shipped content depends on it. Affects every read case.",
    "I2": "A file's type, and so its kind, is determined from its lowercase extension through the registered "
          "extension list; the lookup function is not in kept evidence. Affects cases 1-11.",
    "I3": "An entry whose filePath names no indexed item is skipped without affecting other entries (the apply step "
          "0x1006dbf98 is not traced; the shipped built-in sidecar has one such entry). Affects case 18. "
          "Review: confirmed by the 'binding' evidence (entries are only looked up by the names of F's files; "
          "unmatched entries are removed from the in-memory document afterwards).",
    "I4": "Assigned tags and labels are observable per item without inheritance from its folder. Affected 16 and 17, "
          "removed in review; no released case depends on it.",
    "I5": "The base folder of factory and built-in override sidecars is the User Library (config accessor untraced; "
          "the refusal message names it). Affects 26, 27.",
    "I6": "The pack identifier given to the override-name construction is the pack's packUniqueId as recorded in "
          "its own sidecar (supported by 159 of 160 Legacy Pack Data names). Affects 26 and the general rule.",
    "I7": "UUID text is lowercase with hyphens (formatter 0x100616d44 not kept; every shipped sidecar name is). "
          "Affects 23-27.",
}
TRACE = {
    1: ("BI-001 (narrowed: kind only; listing dropped, PRB-BI-01)", ["registry", "kindmap"], ["I2"]),
    2: ("BI-002 (narrowed: no kind; 'none listed' dropped)", ["registry", "kindmap"], ["I2"]),
    3: ("BI-003 (narrowed: no kind; 'none listed' dropped)", ["registry", "kindmap"], ["I2"]),
    4: ("REQ-001 table, row other audio (new case)", ["registry", "kindmap"], ["I2"]),
    5: ("REQ-001 table, rows encoded audio, Windows Media audio, MPEG-4 audio (new case; BI-004 listing excluded)",
        ["registry", "kindmap"], ["I2"]),
    6: ("REQ-001 table, rows Max devices and REX files (new case)", ["registry", "kindmap"], ["I2"]),
    7: ("REQ-001 table, row video (new case)", ["registry", "kindmap"], ["I2"]),
    8: ("REQ-001 table, row images (new case)", ["registry", "kindmap"], ["I2"]),
    9: ("REQ-001 table, row plug-in presets (new case)", ["registry", "kindmap"], ["I2"]),
    10: ("REQ-001 table, row others (new case)", ["registry", "kindmap"], ["I2"]),
    11: ("REQ-001 table, row no kind (new case)", ["registry", "kindmap"], ["I2"]),
    12: ("BI-020 (narrowed: '.xmp not listed' dropped)", ["gate", "reader", "caller", "items", "binding", "keywords", "shipped"],
         ["I1"]),
    13: ("BI-021 (narrowed: '.xmp not listed' dropped)", ["gate", "reader"], []),
    14: ("BI-030", ["reader", "items", "keywords"], ["I1"]),
    15: ("BI-031 (narrowed: no tags only; other effects excluded)", ["reader"], ["I1"]),
    # 16 (BI-040) and 17 (BI-041) removed in review (RVB-01): contradicted by the "binding" evidence.
    18: ("BI-042 (narrowed: 'no entry or error for gone.wav' dropped)", ["reader", "items", "binding"], ["I1"]),
    19: ("BI-050", ["colors_read", "items"], ["I1"]),
    20: ("BI-051", ["colors_read", "items"], ["I1"]),
    21: ("REQ-006 colour rule bounds 1 and 7 (new case)", ["colors_read", "items"], ["I1"]),
    22: ("BI-053 (narrowed: grouping dropped)", ["keywords", "items"], ["I1"]),
    23: ("BI-060 (narrowed: timing, 'nothing else in F changes', assetId/contentHash dropped)",
         ["folder_writer", "new_doc", "item_write", "file_write", "names"], ["I7"]),
    24: ("BI-061 (narrowed as BI-060)", ["folder_writer", "new_doc", "item_write", "colors_write", "file_write", "names"],
         ["I7"]),
    25: ("REQ-006/007 writer encoding of tags and colours together (new case)",
         ["folder_writer", "new_doc", "item_write", "colors_write", "file_write", "names"], ["I7"]),
    26: ("BI-064 (narrowed: name only; <n>, content and timing excluded)", ["factory", "names", "core_id", "legacy_names"],
         ["I5", "I6", "I7"]),
    27: ("BI-065 (narrowed: name only; <n>, content and timing excluded)", ["builtin", "names"], ["I5", "I7"]),
    28: ("BI-071", ["gate", "reader", "items", "keywords"], ["I1"]),
}
CLAUSES = {
    "REQ-BROWSER-INDEX-001": "Static-derived kind table for lowercase registered extensions (spec REQ-001 bullet 1)",
    "REQ-BROWSER-INDEX-003": "Parent-name test; F/Ableton Folder Info/<user-folder name> read (bullets 1-2)",
    "REQ-BROWSER-INDEX-004": "Folder-resource property set as written and read; informational xmp properties; "
                             "unparsable sidecar contributes no tags (bullets 1-2, narrowed to the folder resource)",
    "REQ-BROWSER-INDEX-005": "filePath relative to the folder containing the sidecar folder, / separators, files and "
                             "folders; unresolved entries skipped (bullets 1-2)",
    "REQ-BROWSER-INDEX-006": "keywords entries give tags; colors entries 1-7 give labels, 0, 8 and empty ignored "
                             "(narrowed from 'other numeric entries ignored'); writer encoding",
    "REQ-BROWSER-INDEX-007": "User-folder sidecar name, location and content of a new sidecar; override file names "
                             "for the Core Library and built-in content (bullets 1-2; <n>, timing, merge excluded)",
    "REQ-BROWSER-INDEX-008": "A folder copied with its sidecar folder keeps its tags on another installation (bullet 1)",
}
