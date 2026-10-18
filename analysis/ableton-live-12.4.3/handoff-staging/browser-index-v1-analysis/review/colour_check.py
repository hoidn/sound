"""Reviewer's re-derivation of the colour-entry rule (finding F3) and of cases 019 to 021.

Model, from the retained colour-read record (D2 entry 0x1006ed324) and the reviewer's
reading of its machine code words (see review-checks.txt): an empty entry is skipped;
any other entry goes to the system C++ library's unsigned-long conversion in base 10
with no end check; only the low 32 bits of the result are kept (32-bit subtract and
compare); label n is set when that value is 1 to 7 (bit n). The conversion follows
the C library's strtoul: leading white space, an optional sign, then digits; no digit
is an invalid-argument exception; a value above 2**64 - 1 is an out-of-range exception.

Usage: python3 -I colour_check.py STAGE_DIR
"""
import re, sys
from pathlib import Path

SIDE = "Ableton Folder Info/dc66a3fa-0fe1-5352-91cf-3ec237e9ee90.xmp"


def stoul10(text):
    m = re.match(r"[ \t\n\v\f\r]*([+-]?)([0-9]+)", text)
    if not m:
        raise ValueError("invalid_argument")
    v = int(m.group(2))
    if v > 2**64 - 1:
        raise OverflowError("out_of_range")
    return (-v) % 2**64 if m.group(1) == "-" else v


def label(text):
    """Label number given by one colour entry, or None."""
    if text == "":
        return None
    w = stoul10(text) & 0xFFFFFFFF
    return w if (w - 1) & 0xFFFFFFFF < 7 else None


def main(stage):
    examples = {"03": 3, "4294967298": 2, " 3": 3, "3x": 3, "+3": 3, "-4294967295": 1,
                "0": None, "8": None, "": None, "4294967296": None, "1": 1, "7": 7}
    for text, want in examples.items():
        got = label(text)
        print(f"{text!r:16} -> {got}" + ("" if got == want else f"   EXPECTED {want}"))
        assert got == want
    for text in ("x", "99999999999999999999"):
        try:
            label(text)
        except (ValueError, OverflowError) as e:
            print(f"{text!r:16} -> exception {e}")
    want = {19: [2, 5], 20: [3], 21: [1, 2, 3, 4, 5, 6, 7]}
    for n, labels in want.items():
        t = (Path(stage) / f"fixtures/BROWSER-INDEX-{n:03d}/F" / SIDE).read_text()
        bag = re.search(r"<ablFR:colors>.*?</ablFR:colors>", t, re.S).group(0)
        got = sorted({label(v) for v in re.findall(r"<rdf:li>(.*?)</rdf:li>", bag)} - {None})
        print(f"BROWSER-INDEX-{n:03d} colour entries give {got}; case expects {labels}")
        assert got == labels
    print("colour check: all assertions passed")


if __name__ == "__main__":
    main(sys.argv[1])
