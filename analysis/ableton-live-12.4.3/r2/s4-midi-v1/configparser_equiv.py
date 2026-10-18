"""Compare Live's shipped configparser.pyc with the analysis interpreter's stdlib source.

Run: python3.11 -I configparser_equiv.py "<bundle .app path>"
Loads Live's code object with marshal.loads (never executed) and compiles the
host CPython 3.11 stdlib configparser.py source (compile only). Compares every
nested code object's bytecode, constants, names, variables and exception table,
ignoring filename and line-number metadata. Prints a JSON verdict.
"""
import json, marshal, sys, sysconfig, types
from pathlib import Path


def sig(co):
    consts = tuple(sig(c) if isinstance(c, types.CodeType) else repr(c) for c in co.co_consts)
    return (co.co_qualname, co.co_code, consts, co.co_names, co.co_varnames,
            co.co_freevars, co.co_cellvars, co.co_exceptiontable, co.co_argcount,
            co.co_kwonlyargcount, co.co_flags)


def walk(co):
    yield co
    for c in co.co_consts:
        if isinstance(c, types.CodeType):
            yield from walk(c)


def main(bundle):
    live = marshal.loads((Path(bundle) / "Contents/App-Resources/Python/lib/configparser.pyc").read_bytes()[16:])
    src = Path(sysconfig.get_paths()["stdlib"]) / "configparser.py"
    out = {"host_python": sys.version.split()[0], "host_source": str(src), "by_optimize_level": {}}
    for opt in (0, 2):  # 2 strips docstrings/asserts, matching a -OO build
        host = compile(src.read_text(), "configparser.py", "exec", dont_inherit=True, optimize=opt)
        L = {c.co_qualname: sig(c) for c in walk(live)}
        H = {c.co_qualname: sig(c) for c in walk(host)}
        out["by_optimize_level"][opt] = {"live_code_objects": len(L), "host_code_objects": len(H),
            "differing_qualnames": sorted(q for q in L.keys() | H.keys() if L.get(q) != H.get(q))}
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main(sys.argv[1])
