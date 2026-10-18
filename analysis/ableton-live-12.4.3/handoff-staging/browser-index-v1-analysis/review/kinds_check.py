"""Reviewer's independent check of BROWSER-INDEX-001 to 011 (content kinds).

The kind returned for each four-character type code was transcribed by hand by
the reviewer from the retained kind-map record (D2, entry 0x10016b758); the
author's compiled evaluator is not used. Bit names are from the retained
bit-name record (0x10016b3e8). Extensions come from the H2 registry table.

Usage: python3 -I kinds_check.py REGISTRY.tsv CASES.json
"""
import csv, json, sys

KIND = {  # fourcc -> returned bit, hand transcription
    '----': 0, 'alc-': 2, 'als-': 1, 'amp-': 0x10, 'ams-': 4, 'asd-': 0,
    'aupr': 0x4000, 'auz-': 0, 'appc': 1, 'appl': 0, 'aac-': 0x2000,
    'aad-': 0, 'abl-': 1, 'ablb': 1, 'abpb': 0, 'adg-': 0x20, 'adv-': 0x20,
    'agr-': 8, 'aiff': 4, 'exs-': 1, 'fidb': 0, 'flac': 0x800,
    'fldr': 0x200, 'gig-': 1, 'jpeg': 0x400, 'json': 0, 'gzip': 0,
    'ini-': 0, 'isoi': 1, 'avi-': 0x40, 'back': 0x200, 'bmp-': 0x400,
    'bnd-': 0, 'bwf-': 4, 'cidb': 0, 'dfld': 0x100, 'digv': 0x40,
    'dmp-': 0, 'eflc': 4, 'lang': 0, 'lfld': 0x200, 'lock': 0, 'log-': 0,
    'midi': 1, 'mp3-': 0x800, 'mp4-': 0x40, 'mp7-': 4, 'mpg-': 0x40,
    'nki-': 1, 'pack': 1, 'qtmv': 0x40, 'rex-': 0x80, 'rex1': 0x80,
    'png-': 0x400, 'pref': 0, 'pysc': 0, 'pcx-': 0x400, 'pfld': 0x200,
    'plug': 0x8000, 'oggv': 0x800, 'scl-': 1, 'sd2-': 4, 'sfnt': 1,
    'skin': 0, 'stak': 1, 'text': 0, 'tiff': 0x400, 'timg': 1,
    'tmpl': 0x200, 'vstp': 0, 'wav-': 4, 'wavp': 4, 'vst3': 0x4000,
    'vstb': 0, 'wma-': 0x1000, 'wmv-': 0x40, 'wvdb': 0, 'xml-': 0,
    'xmp-': 0, 'zipf': 0,
}
LABEL = {  # bit -> release label (paraphrase of the bit names)
    0: 'none', 1: 'other files', 2: 'clips', 4: 'other audio', 8: 'grooves',
    0x10: 'Max devices', 0x20: 'live presets', 0x40: 'video',
    0x80: 'REX files', 0x400: 'images', 0x800: 'encoded audio',
    0x1000: 'Windows Media audio', 0x2000: 'MPEG-4 audio',
    0x4000: 'plug-in presets',
}

def main(registry, cases):
    ext_kind, unmapped = {}, []
    for row in csv.DictReader(open(registry), delimiter='\t'):
        for ext in row['extensions'].split():
            if row['fourcc'] in KIND:
                ext_kind[ext] = LABEL[KIND[row['fourcc']]]
            else:
                unmapped.append(ext)
    seen, bad = [], 0
    for case in json.load(open(cases))['cases']:
        for name, want in case['expected'].get('content_kind', {}).items():
            ext = name[name.rindex('.'):]
            seen.append(ext)
            got = ext_kind.get(ext)
            if got != want:
                bad += 1
                print('MISMATCH', case['id'], name, want, got)
    print('registry extensions:', len(ext_kind) + len(unmapped),
          'mapped:', len(ext_kind), 'unmapped:', unmapped)
    print('case extensions:', len(seen), 'distinct:', len(set(seen)))
    print('mapped extensions not in any case:', sorted(set(ext_kind) - set(seen)))
    print('mismatches:', bad)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
