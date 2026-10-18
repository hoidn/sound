"""Locate MIDI-loader string anchors in the Live arm64 slice (read-only byte search).

Run: python3 -I native_anchors.py <Live.arm64 slice> > native-anchors.json
Records each anchor's file offsets and the NUL-separated strings around the
first hit. String adjacency is a lead for native tracing, not a call edge.
"""
import hashlib, json, sys

ANCHORS = [b"3.11.6", b"UserConfiguration.txt", b"User Remote Scripts", b"HIDE_SCRIPT", b"_UserScript",
           b"create_instance", b"Script could not be loaded.", b"OMidiPadTranslator"]


def main(path):
    data = open(path, "rb").read()
    out = {"slice": path, "sha256": hashlib.sha256(data).hexdigest(), "anchors": []}
    for a in ANCHORS:
        offs, i = [], data.find(a)
        while i != -1 and len(offs) < 8:
            offs.append(i)
            i = data.find(a, i + 1)
        ctx = [s.decode("latin1") for s in data[max(0, offs[0] - 160):offs[0] + 200].split(b"\0") if s] if offs else []
        out["anchors"].append({"string": a.decode(), "offsets": offs, "neighbors": ctx})
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main(sys.argv[1])
