"""Check the stored value text of the seven devices' parameters against the N1 32-bit writer rule (analyst
tool; output is data).

usage: python3 -I number_text_check.py <out-dir> <h4-out-dir> <App-Resources dir>

For every shipped document that H4 found to contain one of the seven device elements (h4 occurrences.jsonl;
SHA-256 re-checked against h4 inputs.jsonl), every parameter below the device element is classified by
its children: TimeableFloat (has ModulationTarget), TimeableBool (has MidiCCOnOffThresholds), otherwise
TimeableEnum. Float Manual and MidiControllerRange Min/Max text must equal the N1 writer rule for 32-bit
values applied to the parsed value (fmt from ../n1-transport-state-v1/check_number_format.py); Enum
Manual text must be a plain decimal integer; Bool Manual text must be true or false.
Writes <out>/number_text_check.json. Reads shipped files read-only.
"""
import collections, gzip, hashlib, importlib.util, json, os, re, sys
sys.dont_write_bytecode = True  # do not leave __pycache__ in other packets' directories
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('n1n', os.path.join(HERE, '../n1-transport-state-v1/check_number_format.py'))
n1n = importlib.util.module_from_spec(spec)
spec.loader.exec_module(n1n)
DEVICES = {'Amp', 'Cabinet', 'UltraAnalog', 'StringStudio', 'Collision', 'LoungeLizard', 'Corpus'}


def classify(el):
    kids = {c.tag for c in el}
    if 'Manual' not in kids or 'AutomationTarget' not in kids:
        return None
    return 'float' if 'ModulationTarget' in kids else 'bool' if 'MidiCCOnOffThresholds' in kids else 'enum'


def main(out, h4, app):
    sha = {json.loads(l)['path']: json.loads(l)['sha256'] for l in open(os.path.join(h4, 'inputs.jsonl'))}
    docs = sorted({json.loads(l)['doc'] for l in open(os.path.join(h4, 'occurrences.jsonl'))})
    res = collections.defaultdict(lambda: collections.Counter())
    bad = []
    for doc in docs:
        raw = open(os.path.join(app, doc), 'rb').read()
        assert hashlib.sha256(raw).hexdigest() == sha[doc], doc
        root = ET.fromstring(gzip.decompress(raw))
        for dev in root.iter():
            if dev.tag not in DEVICES:
                continue
            for el in dev.iter():
                kind = classify(el)
                if kind is None:
                    continue
                v = el.find('Manual').get('Value')
                if kind == 'float':
                    texts = [v] + [el.find('MidiControllerRange/' + t).get('Value') for t in ('Min', 'Max')
                                   if el.find('MidiControllerRange/' + t) is not None]
                    for t in texts:
                        ok = n1n.fmt(n1n.f32(t), 9, 8) == t
                        res[dev.tag]['float_ok' if ok else 'float_bad'] += 1
                        if not ok and len(bad) < 20:
                            bad.append((doc, dev.tag, el.tag, t, n1n.fmt(n1n.f32(t), 9, 8)))
                elif kind == 'enum':
                    ok = re.fullmatch(r'-?\d+', v) is not None
                    res[dev.tag]['enum_ok' if ok else 'enum_bad'] += 1
                else:
                    ok = v in ('true', 'false')
                    res[dev.tag]['bool_ok' if ok else 'bool_bad'] += 1
    summary = {'documents': len(docs), 'per_device': {k: dict(v) for k, v in sorted(res.items())},
               'mismatch_examples': bad,
               'all_match': not any(k.endswith('_bad') for v in res.values() for k in v)}
    json.dump(summary, open(os.path.join(out, 'number_text_check.json'), 'w'), indent=1)
    print(json.dumps(summary, indent=1))


if __name__ == '__main__':
    main(*sys.argv[1:4])
