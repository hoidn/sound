"""Reviewer check (analyst-side): scan every payload file, and the decompressed text of every
fixture, for code, internal identifiers, analysis vocabulary, planning IDs, restricted links and
shipped-content names. Prints each hit with its context.
usage: python3 -I hygiene.py <package dir>"""
import re, sys, zlib
from pathlib import Path
DENY = [r"0x[0-9a-fA-F]{4,}", r"\b(FUN|DAT|PTR|LAB|UNK)_", r"\bA[A-Z][a-z]+[A-Z]\w*", r"[Rr]emoteable", r"[Tt]ranslat",
        r"vtable", r"post-?load", r"\bloader", r"[Cc]onstructor", r"\bflag", r"strtod|from_chars|printf|stoi|errc",
        r"DBL_MAX|FLT_MAX|INT64", r"Ghidra|REA\b|[Ee]xpat|libc|zlib|CPython|Python", r"[Dd]ecompil|pseudocode|[Dd]isassembl",
        r"dossier|corpus|chunk", r"History|\.cpp|\.c\b|\.h\b", r"Class mismatch|not unique|Multiple sets|Note-group|Unexpected value",
        r"\bPRB-|\bQ-0\d\d|\bMN-\d|\bs7-|\bd4-|\bn[12]-\d|\bRV[A1]?-|\bF\d\b|\b[AIB]\d\b", r"analysis/|raw/|wiki/|research|specs/|verification/",
        r"/home|/var|/tmp|\.\./", r"Core Library|\.alc\b|909|12\.4d1|Chuck|[Dd]emo\b|shipped statistic", r"memory|corrupt|slot|unsigned|hash\b|128 slots",
        r"\binherit|\breuse|\bobject\b|\bbuffer|\bpointer|\bthrow|\bexception|\bcatch", r"stable_sort|std::|\bmap\b"]
pkg = Path(sys.argv[1]); total = 0
for p in sorted(pkg.rglob("*")):
    if not p.is_file():
        continue
    data = p.read_bytes()
    text = zlib.decompress(data, 31).decode("utf-8") if data[:2] == b"\x1f\x8b" else data.decode("utf-8")
    for pat in DENY:
        for m in re.finditer(pat, text):
            total += 1
            s = text[max(0, m.start() - 50):m.end() + 50].replace("\n", " ")
            print(f"{p.relative_to(pkg)}: [{m.group(0)}] ...{s}...")
    if re.search(r"[^\x09\x0a\x20-\x7e]", text):
        print(f"{p.relative_to(pkg)}: non-ASCII characters:", sorted({c for c in text if not (c in '\t\n' or ' ' <= c <= '~')}))
print("hits:", total)
