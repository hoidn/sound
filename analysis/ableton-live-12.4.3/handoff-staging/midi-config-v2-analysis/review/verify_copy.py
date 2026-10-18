import hashlib, json, re, sys
from pathlib import Path
pkg = Path(sys.argv[1]).resolve(); res = {}
m = json.loads((pkg / "manifest.json").read_text())
listed = {f["path"]: f for f in m["files"]}
actual = {str(p.relative_to(pkg)) for p in pkg.rglob("*") if p.is_file() and p.name != "manifest.json"}
res["symlinks"] = [str(p) for p in pkg.rglob("*") if p.is_symlink()]
res["inventory_diff"] = sorted(actual ^ set(listed))
res["hash_or_size_mismatch"] = [k for k, f in listed.items() if (pkg / k).is_file() and (hashlib.sha256((pkg / k).read_bytes()).hexdigest() != f["sha256"] or (pkg / k).stat().st_size != f["bytes"])]
def slug(h): return re.sub(r"[^\w\- ]", "", h.strip().lower()).replace(" ", "-")
links, bad = 0, []
for md in pkg.glob("*.md"):
    for t in re.findall(r"\]\(([^)\s]+)\)", md.read_text()):
        links += 1; path, _, anchor = t.partition("#")
        dest = (md.parent / path).resolve() if path else md
        ok = dest.is_file() and pkg in dest.parents and not re.match(r"[a-z]+:", t)
        if ok and anchor: ok = anchor in {slug(h) for h in re.findall(r"^#+ (.+)$", dest.read_text(), re.M)}
        if not ok: bad.append((md.name, t))
res["markdown_links"] = links; res["unresolved_links"] = bad
cases = json.loads((pkg / "cases.json").read_text())["cases"]
res["cases"] = len(cases); res["manifest_case_count"] = m["case_count"]
res["missing_inputs"] = [c["input"] for c in cases if not (pkg / c["input"]).is_file()]
badfix = []
for c in cases:
    b = (pkg / c["input"]).read_bytes()
    if not b.isascii() or not b.endswith(b"\n") or any(x < 32 and x != 10 for x in b): badfix.append(c["id"])
res["fixture_format_problems"] = badfix
deny = re.compile(r"_UserScript|_Generic|_Framework|GenericScript|ControlSurface|Component\b|ButtonMatrix|EncoderElement|ButtonElement|MidiMap|create_instance|parse_|getint|getboolean|configparser|ConfigParser|BOOLEAN_STATES|optionxform|MAX_14|NOTOGGLE|NORELEASE|INVERTMUTELEDS|PAD_TRANSLATION|TRANSPORT_BUTTON|c_instance|\.pyc|bytecode|disassembl|pseudocode|marshal|xdis|LOAD_[A-Z]|offset\b|\bL\d{2,}\b|Python|CPython|arm64|Ghidra|/var/|/home/|/tmp/|\.\./|analysis/|wiki/|raw/|derivation|locator|\bE[1-9]\b|\bD[1-7]\b|PRB-|\bS4-|\bR-[A-Z]|\bQ-0\d|ev_[0-9a-f]{6}|traceab|crosscheck|build_v2")
hits = {}
for p in pkg.rglob("*"):
    if p.is_file():
        f = sorted(set(deny.findall(p.read_text())))
        if f: hits[str(p.relative_to(pkg))] = f
res["deny_hits"] = hits
res["decompil_mentions"] = {str(p.relative_to(pkg)): p.read_text().count("decompil") for p in pkg.rglob("*") if p.is_file() and "decompil" in p.read_text()}
res["manifest_sha256"] = hashlib.sha256((pkg / "manifest.json").read_bytes()).hexdigest()
res["payload_files"] = len(actual)
print(json.dumps(res, indent=1))
