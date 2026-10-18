"""Reviewer check of a package copy: inventory, SHA-256 and size of every listed file, links, case inputs.

usage: python3 -I verify_copy.py <package dir> [--rehash]
--rehash rewrites manifest.json "files" with the current digests (manifest itself excluded).
"""
import hashlib, json, re, sys
from pathlib import Path

pkg = Path(sys.argv[1]).resolve()
man_path = pkg / "manifest.json"
man = json.loads(man_path.read_text())
files = sorted(p for p in pkg.rglob("*") if p.is_file() and p.name != "manifest.json")
if "--rehash" in sys.argv:
    man["files"] = [{"path": str(p.relative_to(pkg)), "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
                     "bytes": p.stat().st_size} for p in files]
    man_path.write_text(json.dumps(man, indent=1) + "\n")
listed = {f["path"]: f for f in man["files"]}
mism = [k for k, f in listed.items() if not (pkg / k).is_file()
        or hashlib.sha256((pkg / k).read_bytes()).hexdigest() != f["sha256"] or (pkg / k).stat().st_size != f["bytes"]]
inv = sorted({str(p.relative_to(pkg)) for p in files} ^ set(listed))
bad_links, n_links = [], 0
for md in pkg.glob("*.md"):
    heads = None
    for target in re.findall(r"\]\(([^)\s]+)\)", md.read_text()):
        n_links += 1
        path, _, anchor = target.partition("#")
        dest = (md.parent / path).resolve() if path else md
        ok = not re.match(r"[a-z]+:", target) and dest.is_file() and pkg in dest.parents
        if ok and anchor:
            heads = {re.sub(r"[^\w\- ]", "", h.strip().lower()).replace(" ", "-")
                     for h in re.findall(r"^#+ (.+)$", dest.read_text(), re.M)}
            ok = anchor in heads
        if not ok:
            bad_links.append(f"{md.name}: {target}")
cases = json.loads((pkg / "cases.json").read_text())["cases"]
missing = [c["input"] for c in cases if not (pkg / c["input"]).is_file()]
symlinks = [str(p) for p in pkg.rglob("*") if p.is_symlink()]
print(json.dumps({"listed": len(listed), "hash_or_size_mismatches": mism, "inventory_differences": inv,
                  "markdown_links": n_links, "unresolved_links": bad_links, "cases": len(cases),
                  "manifest_case_count": man["case_count"], "missing_case_inputs": missing, "symlinks": symlinks,
                  "manifest_sha256": hashlib.sha256(man_path.read_bytes()).hexdigest()}, indent=1))
