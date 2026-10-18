"""Rule-mutation check: which cases detect each flipped rule (analyst side; not shipped). Usage: python3.11 -I mutate_pd.py build_pd.py."""
import importlib.util, json, sys
from pathlib import Path
src = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("bpd", src); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
cases = json.loads((m.STAGE / "cases.json").read_text())["cases"]
orig3, orig2, origf = m.vst3, m.vst2, m.folders

def v3_ci(nodes, root):
    out, stack = [], [root] if nodes.get(root, ("file",))[0] == "directory" else []
    while stack:
        p = stack.pop()
        for c in m.children(nodes, p):
            if c.rsplit("/",1)[1].lower().endswith(".vst3"): out.append(c)
            elif nodes[c][0] == "directory": stack.append(c)
    return out
def v3_dirs_only(nodes, root): return [c for c in orig3(nodes, root) if nodes[c][0] == "directory"]
def v3_descend(nodes, root):
    out, stack = [], [root] if nodes.get(root, ("file",))[0] == "directory" else []
    while stack:
        p = stack.pop()
        for c in m.children(nodes, p):
            if c.rsplit("/",1)[1].endswith(".vst3"): out.append(c)
            if nodes[c][0] == "directory": stack.append(c)
    return out
def v3_no_descend_other(nodes, root):
    return [c for c in m.children(nodes, root) if c.rsplit("/",1)[1].endswith(".vst3")] if nodes.get(root, ("file",))[0] == "directory" else []
def v2_cs(nodes, root): return [c for c in orig2(nodes, root) if c.endswith(".vst")]
def v2_files(nodes, root): return orig2(nodes, root) + [q for q in nodes if q.startswith(root + "/") and nodes[q][0] == "file" and q.lower().endswith(".vst")]
def v2_no_skip(nodes, root):
    n2 = {p: (t, None) for p, (t, md) in nodes.items()}
    return orig2(n2, root)
def v2_stop_on_error(nodes, root):
    if any(nodes[q][1] == "000" for q in nodes if q == root or q.startswith(root + "/")): return []
    return orig2(nodes, root)
def v2_no_vst3_descend(nodes, root):
    return [c for c in orig2(nodes, root) if ".vst3/" not in c]
def f_custom_always(sc, fmt):
    s = sc["settings"][fmt]; r = (m.SYSTEM[fmt] if s["system_folders_switch"] else []) + ([s["custom_folder"]] if s["custom_folder"] else [])
    return r
def f_custom_replaces(sc, fmt):
    s = sc["settings"][fmt]
    if s["custom_folder_switch"] and s["custom_folder"]: return [s["custom_folder"]]
    return m.SYSTEM[fmt] if s["system_folders_switch"] else []
def f_user_only(sc, fmt): return [p for p in origf(sc, fmt) if not p.startswith("/Library")]
def f_shared_switch(sc, fmt):
    s = dict(sc["settings"][fmt]); s["system_folders_switch"] = sc["settings"]["vst3"]["system_folders_switch"]
    return origf({"settings": {fmt: s}}, fmt)
def f_plugins_root(sc, fmt): return origf(sc, fmt) + ["~/Library/Audio/Plug-Ins"]

muts = {"VST3 case-insensitive": ("vst3", v3_ci), "VST3 directories only": ("vst3", v3_dirs_only),
        "VST3 descends into candidates": ("vst3", v3_descend), "VST3 top level only": ("vst3", v3_no_descend_other),
        "VST2 case-sensitive": ("vst2", v2_cs), "VST2 accepts files": ("vst2", v2_files),
        "VST2 reads mode-000 folders": ("vst2", v2_no_skip), "VST2 stops a folder on an unreadable subfolder": ("vst2", v2_stop_on_error),
        "VST2 skips *.vst3 directories": ("vst2", v2_no_vst3_descend),
        "custom folder without its switch": ("folders", f_custom_always), "custom folder replaces system folders": ("folders", f_custom_replaces),
        "user system folders only": ("folders", f_user_only), "VST2 follows the VST3 system switch": ("folders", f_shared_switch),
        "Plug-Ins root searched": ("folders", f_plugins_root)}
res = {}
for name, (slot, fn) in muts.items():
    m.vst3, m.vst2, m.folders = orig3, orig2, origf
    setattr(m, slot, fn)
    hit = []
    for c in cases:
        try: got = m.model(json.loads((m.STAGE / c["input"]).read_text()))
        except m.NoExpectation as e: got = str(e)
        if got != c["expected"]: hit.append(c["id"][-3:])
    res[name] = hit
m.vst3, m.vst2, m.folders = orig3, orig2, origf
print(json.dumps(res, indent=0))
print("undetected:", [k for k, v in res.items() if not v])
