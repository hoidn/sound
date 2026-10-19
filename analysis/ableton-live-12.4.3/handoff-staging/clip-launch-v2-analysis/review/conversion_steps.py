"""List the conversion steps above 405 with their class filters and error paths (analyst side; never shipped).

usage: python3 -I -B conversion_steps.py > conversion-steps.txt
Reads the step registry (arm64 0x10148ec98) and each step's pseudocode from the decompiled corpus
(/var/tmp/sound-analysis/corpus, read-only). For each step: number, function, class filter, whether it
reports an error (0x101471a98) and whether it has a no-return path other than the stack guard.
The reviewer read the steps marked in READ below; see review-checks.txt for what each does.
"""
import json, re, subprocess

C = "/var/tmp/sound-analysis/corpus/decomp/chunks"
READ = {406, 407, 411, 413, 414, 417, 419, 421, 423, 11201, 12020, 12021, 12037, 12039, 12045, 12105, 12109,
        12116, 12117, 12119, 12120, 12203, 12205, 12401}


def code(entries):
    files = subprocess.run(f"grep -l -E '\"entry\": ?\"({'|'.join(entries)})\"' {C}/*.jsonl", shell=True,
                           capture_output=True, text=True).stdout.split()
    out = {}
    for f in files:
        for line in open(f):
            r = json.loads(line)
            if r["entry"] in entries:
                out[r["entry"]] = r["code"] or r.get("partial_code") or ""
    return out


reg = code({"0x10148ec98"})["0x10148ec98"]
steps = [(int(m.group(1), 0), "0x" + m.group(2)[4:], m.group(3))
         for m in re.finditer(r'FUN_1014714fc\((0x[0-9a-f]+|\d+),(FUN_[0-9a-f]+),\s*"([^"]*)"', reg, re.S)]
steps = [s for s in steps if s[0] > 405]
body = code({a for _, a, _ in steps})
for n, a, cls in steps:
    c = body.get(a, "")
    err = "error-report" if "FUN_101471a98" in c else ""
    noret = "no-return" if re.search(r"does not return \*/\s*\n\s*(?!___stack_chk_fail)", c, re.I) else ""
    print(n, a, err, noret, "read" if n in READ else "", "|", cls)
print(len(steps), "steps above 405")
