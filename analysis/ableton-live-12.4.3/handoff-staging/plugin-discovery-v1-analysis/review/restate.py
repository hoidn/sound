"""Reviewer's independent restatement of the plugin-discovery-v1 rules, plus fixture and package checks.

Usage: python3 -I restate.py PACKAGE_DIR
Written from the payload spec.md wording only; does not import or copy build_pd.py.
"""
import hashlib, json, re, sys
from pathlib import Path

pkg = Path(sys.argv[1])
SYS = {"vst3": ["~/Library/Audio/Plug-Ins/VST3", "/Library/Audio/Plug-Ins/VST3"],
       "vst2": ["~/Library/Audio/Plug-Ins/VST", "/Library/Audio/Plug-Ins/VST"]}
NAME_OK = re.compile(r"[A-Za-z0-9 _.\-]+\Z")
HOME = "/Users/" + "u" * 32  # generous home length for the 255-byte check
problems = []


def below(p, root):
    return p == root or p.startswith(root + "/")


def ext(name):  # spec Terms: from the last period to the end; names never begin with a period here
    return name[name.rfind("."):] if "." in name else ""


def searched(settings, fmt):
    s = settings[fmt]
    out = list(SYS[fmt]) if s["system_folders_switch"] else []
    if s["custom_folder_switch"] and s["custom_folder"]:
        out.append(s["custom_folder"])
    return out


def build_tree(sc):
    kinds, modes = {}, {}
    for e in sc["entries"]:
        p = e["path"]
        parts = p.split("/")
        for i in range(2, len(parts)):
            kinds.setdefault("/".join(parts[:i]), "directory")
        kinds[p] = e["type"]
        if "mode" in e:
            modes[p] = e["mode"]
    return kinds, modes


def kids(kinds, d):
    return [q for q in kinds if q.rsplit("/", 1)[0] == d]


def walk(fmt, kinds, modes, root):
    """Candidates of one format under one folder, per REQ-004 / REQ-005 partial clauses."""
    if kinds.get(root) != "directory":  # REQ-002 clause 7: missing (or empty) folder gives nothing
        return set()
    found, pending = set(), [root]
    while pending:
        d = pending.pop()
        if modes.get(d) == "000":
            assert fmt == "vst2", "unreadable directory in a VST3 folder has no expectation"
            continue  # REQ-005 clause 4
        for c in kids(kinds, d):
            name, kind = c.rsplit("/", 1)[1], kinds[c]
            if fmt == "vst3":
                if ext(name) == ".vst3":  # clause 1-2: exact, case-sensitive, files and directories
                    found.add(c)  # clause 3: not searched inside
                elif kind == "directory":
                    pending.append(c)  # clause 4
            else:
                if kind != "directory":
                    continue  # clause 3
                if ext(name).lower() == ".vst":
                    found.add(c)  # clause 1-2
                else:
                    pending.append(c)
    return found


cases = json.loads((pkg / "cases.json").read_text())["cases"]
blobs = set()
for c in cases:
    raw = (pkg / c["input"]).read_bytes()
    blobs.add(raw)
    sc = json.loads(raw)
    cid = c["id"]
    if not raw.isascii() or b"\r" in raw or b"\t" in raw or not raw.endswith(b"\n"):
        problems.append((cid, "not ASCII/LF/final newline"))
    if set(sc) != {"schema", "settings", "entries", "absent"}:
        problems.append((cid, f"members {sorted(sc)}"))
    kinds, modes = build_tree(sc)
    for p in [e["path"] for e in sc["entries"]] + sc["absent"] + [
            sc["settings"][f]["custom_folder"] for f in ("vst3", "vst2") if sc["settings"][f]["custom_folder"]]:
        head, *names = p.split("/")
        if head not in ("", "~") or not names or p.endswith("/"):
            problems.append((cid, f"path form {p}"))
        for n in names:
            if not NAME_OK.match(n) or n.startswith("."):
                problems.append((cid, f"excluded name {n!r}"))
        if len(p.replace("~", HOME, 1).encode()) > 255:
            problems.append((cid, f"long path {p}"))
    for p, m in modes.items():
        if m != "000" or kinds[p] != "directory" or re.search(r"\.vst3?\Z", p, re.I):
            problems.append((cid, f"mode on {p}"))
    for a in sc["absent"]:
        if any(below(q, a) for q in kinds):
            problems.append((cid, f"absent {a} has content"))
    roots = {f: searched(sc["settings"], f) for f in ("vst3", "vst2")}
    if not roots["vst3"] and not roots["vst2"]:
        problems.append((cid, "no folder of either format"))
    for f, rs in roots.items():
        for i, a in enumerate(rs):
            for b in rs[i + 1:]:
                if below(a, b) or below(b, a):
                    problems.append((cid, f"equal/nested {f} folders"))
    for p in kinds:  # obligation 3 attribution: each entry below folders of at most one format
        fm = {f for f, rs in roots.items() for r in rs if p != r and below(p, r)}
        if len(fm) > 1:
            problems.append((cid, f"{p} below folders of both formats"))
    got = {f"{f}_candidates": sorted(set().union(*[walk(f, kinds, modes, r) for r in roots[f]]))
           for f in ("vst3", "vst2")}
    if any(len(v) > 50 for v in got.values()):
        problems.append((cid, "more than 50"))
    if got != c["expected"]:
        problems.append((cid, f"restated {got} != expected {c['expected']}"))
    print(cid, {k: len(v) for k, v in got.items()}, "folders", {f: len(r) for f, r in roots.items()},
          "agree" if got == c["expected"] else "DISAGREE")

print("cases", len(cases), "distinct fixtures", len(blobs))
man = json.loads((pkg / "manifest.json").read_text())
listed = {f["path"]: f for f in man["files"]}
actual = {str(p.relative_to(pkg)) for p in pkg.rglob("*") if p.is_file() and p.name != "manifest.json"}
print("inventory equal:", set(listed) == actual, len(actual))
bad = [p for p, f in listed.items() if not (pkg / p).is_file()
       or hashlib.sha256((pkg / p).read_bytes()).hexdigest() != f["sha256"] or (pkg / p).stat().st_size != f["bytes"]]
print("hash/size mismatches:", bad)
print("symlinks:", [str(p) for p in pkg.rglob("*") if p.is_symlink()])
print("problems:", problems or "none")
