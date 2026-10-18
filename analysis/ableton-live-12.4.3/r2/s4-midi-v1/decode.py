"""S4 MIDI closure: hash pinned sources and statically disassemble bytecode.

Run with the CPython whose magic matches the .pyc (3.11, magic 3495):
  python3.11 -I decode.py "<bundle .app path>" <out dir>
Reads only; never imports, execs or evals target code. marshal.loads + dis only.
Writes: hashes.json, listings/<module>.dis.txt (code-object addresses stripped).
"""
import dis, hashlib, importlib.util, json, marshal, re, sys, types
from pathlib import Path

MRS = "Contents/App-Resources/MIDI Remote Scripts"
DOCS = {  # recorded in wiki/research/sources/midi-user-mapping-12.4.3.md
    f"{MRS}/_Tools/UserConfiguration.txt": "52ec71be0a51fd89a0d1cebebc9a3f7c2a2cb62f6a55d25e7a4be3b3228322a4",
    f"{MRS}/_Tools/InstantMappings-HowTo.txt": "6d710bba5610cba5c17213fc46472fb87843857fcba8d28f6f838d69aa1554ef",
}
MODULES = [f"{MRS}/{m}.pyc" for m in (
    "_UserScript/__init__", "_UserScript/DeviceComponent", "_Generic/GenericScript",
    "_Generic/SpecialMixerComponent", "_Generic/SelectChanStripComponent",
    "_Framework/InputControlElement", "_Framework/EncoderElement", "_Framework/ButtonElement",
    "_Framework/ButtonMatrixElement", "_Framework/DeviceComponent", "_Framework/ChannelStripComponent",
    "_Framework/TransportComponent", "_Framework/ToggleComponent", "_Framework/MixerComponent",
    "_Framework/ControlSurface",  # supplemental in S4: pad-translation and component_guard boundary
    "ableton/v3/control_surface/__init__", "ableton/v3/control_surface/elements_base",
)] + ["Contents/App-Resources/Python/lib/configparser.pyc"]
ADDR = re.compile(r" at 0x[0-9a-f]+")


def walk(co, path=""):
    name = f"{path}.{co.co_qualname}" if path else co.co_qualname
    yield name, co
    for c in co.co_consts:
        if isinstance(c, types.CodeType):
            yield from walk(c, path)


def listing(co):
    out = []
    for name, c in walk(co):
        out.append(f"\n## code {c.co_qualname} | firstlineno {c.co_firstlineno} | file {c.co_filename}\n")
        out.append(ADDR.sub("", dis.Bytecode(c).dis()))
    return "".join(out)


def main(bundle, out):
    bundle, out = Path(bundle), Path(out)
    assert importlib.util.MAGIC_NUMBER == b"\xa7\x0d\x0d\x0a", "need CPython 3.11 (magic 3495)"
    rows = []
    for rel, want in list(DOCS.items()) + [(m, None) for m in MODULES]:
        data = (bundle / rel).read_bytes()
        got = hashlib.sha256(data).hexdigest()
        rows.append({"path": rel, "bytes": len(data), "sha256": got, "recorded_sha256": want,
                     "comparison": "match" if got == want else ("mismatch" if want else "unknown: recorded digest not available on this host")})
        if rel.endswith(".pyc"):
            assert data[:4] == importlib.util.MAGIC_NUMBER, rel
            mod = rel.removeprefix(f"{MRS}/").removeprefix("Contents/App-Resources/Python/lib/").removesuffix(".pyc")
            dst = out / "listings" / f"{mod}.dis.txt"
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(f"# source {rel}\n# sha256 {got}\n# decoder CPython {sys.version.split()[0]} dis; marshal.loads only, not executed\n"
                           + listing(marshal.loads(data[16:])))
    (out / "hashes.json").write_text(json.dumps({"bundle": str(bundle), "python": sys.version.split()[0], "files": rows}, indent=1) + "\n")
    for r in rows:
        print(r["comparison"][:8], r["sha256"][:16], r["path"])


if __name__ == "__main__":
    main(*sys.argv[1:3])
