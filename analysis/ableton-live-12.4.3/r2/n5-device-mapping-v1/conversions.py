"""Static per-parameter conversion tables for Amp, Cabinet, Electric (LoungeLizard) and Corpus.

usage: python3 -I conversions.py <out-dir> <h4-out-dir>

Writes <out-dir>/conversions.tsv (all four devices) and <out-dir>/corpus_parameters.tsv (the Corpus
subset with the bundle-side mapping). Each row gives the stored (document) parameter, the SetParameterA
index, Live's construction arguments (internal range, user converter, default) and the value Live passes
for the constructor default. The SPEC rows are transcribed from the decompiled constructors cited in
notes.md (Live corpus) and FUN_0000d75c / FUN_000050c0 (Corpus helper corpus); they are data, not code
behaviour that was executed. Self-checks (assert): the index order equals out/live_index_map.tsv from
extract_mapping.py, every user domain equals the stored modal range in H4 param_table.tsv, and every
Corpus row's bundle rule is the one FUN_0000d75c selects for that index.
Depends on: out/live_index_map.tsv, <h4>/param_table.tsv. Standard library only.
"""
import csv, math, os, sys

# (device, stored name, converter, internal (p1,p2), user (c0,c1), default (user), mode, source);
# enum/bool rows: (device, stored name, converter, labels, default, mode, source)
# converter: linear | legacyint | quantizing | log10 | enum | bool. mode: 0 identity, 6 (mult, off), 7 table.
L01 = ('linear', (0, 1), (0, 1))
B11 = ('linear', (-1, 1), (-1, 1))
SPEC = [
    ('Amp', 'AmpType', 'enum', ('Clean', 'Boost', 'Blues', 'Rock', 'Lead', 'Heavy', 'Bass'), 2, (7, [4, 5, 0, 1, 2, 3, 6]), 'FUN_1030b4934 FUN_1026ef060(+0x250,2,...); table DAT_106e78580'),
] + [
    ('Amp', n, 'linear', (0, 1), (0, 10), d, 0, f'FUN_1030b4934 FUN_103197a6c({d}) -> FUN_1026f0bcc(0,1,{d}) ALinear(0,10)')
    for n, d in (('Bass', 5), ('Middle', 5), ('Treble', 5), ('Presence', 5), ('Gain', 5), ('Volume', 9))
] + [
    ('Cabinet', 'CabinetType', 'enum', ('1x12', '2x12', '4x12', '4x10', '4x10 Bass'), 0, 0, 'FUN_1030c9c90 FUN_1026ef060(+0x250,0,...)'),
    ('Cabinet', 'MicrophoneTypeSwitch', 'bool', ('Dynamic', 'Condenser'), 0, 0, 'FUN_1030c9c90 FUN_1026ec1cc(+0x268,0,...)'),
    ('Cabinet', 'MicrophonePosition', 'enum', ('Near On-Axis', 'Near Off-Axis', 'Far'), 0, 0, 'FUN_1030c9c90 FUN_1026ef060(+0x280,0,...)'),
    ('LoungeLizard', 'Polyphony', 'enum', tuple(str(v) for v in range(2, 33)), 30, 0, 'FUN_1030e9578 FUN_1026ef060(+0x250,0x1e,labels 2..32,"Voices")'),
    ('LoungeLizard', 'PitchBendRange', *L01, 1.0, 0, 'FUN_1030e9578 FUN_103192720(1.0,"Pitch Bend Range")'),
    ('LoungeLizard', 'Volume', *L01, 0.7047892213, 0, 'FUN_1030e9578 FUN_103192720(0x3f346d11,"Volume")'),
    ('LoungeLizard', 'KeyboardFineTune', *L01, 0.5, 0, 'FUN_1030e9578 FUN_103192720(0.5,"Detune")'),
] + [
    ('LoungeLizard', n, *L01, 0.5, 0, f'FUN_1030e9578 FUN_103192720(0.5,"{d}")') for n, d in (
        ('MalletStiffness', 'Mallet Stiffness'), ('MalletStiffnessKeyboard', 'Mallet Stiffness < Key'),
        ('MalletStiffnessVelocity', 'Mallet Stiffness < Vel'), ('MalletForceStrength', 'Mallet Force'),
        ('MalletForceKeyboard', 'Mallet Force < Key'), ('MalletForceVelocity', 'Mallet Force < Vel'),
        ('MalletNoisePitch', 'Mallet Noise Pitch'), ('MalletNoiseDecay', 'Mallet Noise Decay'),
        ('MalletNoiseAmount', 'Mallet Noise Amount'), ('MalletNoiseKeyboardScaling', 'Mallet Noise < Key'),
        ('ForkReleaseTime', 'Fork Release Time'), ('ForkTineDecay', 'Fork Tine Decay'),
        ('ForkTineVolume', 'Fork Tine Volume'), ('ForkTineKeyboardScaling', 'Fork Tine < Key'),
        ('ForkTineColor', 'Fork Tine Color'), ('ForkToneBarDecay', 'Fork Tone Bar Decay'),
        ('ForkToneBarVolume', 'Fork Tone Bar Volume'), ('PickupSymmetry', 'Pickup Symmetry'),
        ('PickupDistance', 'Pickup Distance'))
] + [
    ('LoungeLizard', 'PickupModel', 'enum', ('R', 'W'), 0, 0, 'FUN_1030e9578 FUN_1026ef060(+0x4c0,0,["R","W"],"Pickup Model")'),
] + [
    ('LoungeLizard', n, *L01, 0.5, 0, f'FUN_1030e9578 FUN_103192720(0.5,"{d}")') for n, d in (
        ('PickupAmpIn', 'Pickup Amp In'), ('PickupAmpOut', 'Pickup Amp Out'),
        ('PickupAmpKeyboardScaling', 'Pickup Amp < Key'), ('DamperTone', 'Damper Tone'),
        ('DamperAmount', 'Damper Amount'), ('DamperBalance', 'Damper Balance'))
] + [
    ('LoungeLizard', 'KeyboardTranspose', 'legacyint', (0, 24), (0, 24), 12, 0, 'FUN_1030e9578 FUN_1026f0b58(0,24,12,+0x2b0) ALegacyQuantingInt(0,24)'),
    ('LoungeLizard', 'KeyboardStretch', *L01, 0.5, 0, 'FUN_1030e9578 FUN_103192720(0.5,"Keyboard Stretch")'),
    ('LoungeLizard', '(DummyPerNotePitchBendRange, not stored)', 'quantizing', (0, 48), (0, 48), 48, 0, 'FUN_1030e9578 FUN_1026f0b58(0,48,48,+0x598) AQuantizing(1)'),
    ('LoungeLizard', 'PerNotePitchBendRange', 'quantizing', (0, 48), (0, 48), 0, None, 'FUN_1030e9578 FUN_1026f0b58(0,48,0,+0x280); not in the index vector'),
    ('Corpus', 'ResonanceType', 'enum', ('Beam', 'Marimba', 'String', 'Membrane', 'Plate', 'Pipe', 'Tube'), 0, 0, 'FUN_1030e277c FUN_1026ef060(+0x268,0,...)'),
    ('Corpus', 'Decay', *L01, 0.5, 0, 'FUN_1030e277c FUN_103192720(0.5,"Decay")'),
    ('Corpus', 'FreqDamping', *B11, 0, 0, 'FUN_1030e277c FUN_103192974(0,"Material") -> FUN_103197e1c(-1,1)'),
    ('Corpus', 'Inharmonics', *B11, 0, 0, 'FUN_1030e277c FUN_103192974(0,"Inharmonics")'),
    ('Corpus', 'Ratio', *L01, 0.5, 0, 'FUN_1030e277c FUN_103192720(0.5,"Ratio")'),
    ('Corpus', 'Radius', *L01, 0.5, 0, 'FUN_1030e277c FUN_103192720(0.5,"Radius")'),
    ('Corpus', 'Frequency', *L01, 0.5, 0, 'FUN_1030e277c FUN_103197830(0.5,"Tune",user ALinear(0,1,1/96,..))'),
    ('Corpus', 'Transpose', 'legacyint', (-48, 48), (-48, 48), 0, 0, 'FUN_1030e277c FUN_1026f0b58(-48,48,0) ALegacyQuantingInt(-48,48)'),
    ('Corpus', 'FineTranspose', 'legacyint', (-50, 50), (-50, 50), 0, 0, 'FUN_1030e277c FUN_1026f0b58(-50,50,0) ALegacyQuantingInt(-50,50)'),
    ('Corpus', 'Detune', *B11, 0, 0, 'FUN_1030e277c FUN_103192974(0,"Spread")'),
    ('Corpus', 'PitchBendRange', 'legacyint', (0, 24), (0, 24), 5, 0, 'FUN_1030e277c FUN_1026f0b58(0,24,5) ALegacyQuantingInt(0,24)'),
    ('Corpus', 'AmpFreq', *B11, 0, 0, 'FUN_1030e277c FUN_103192974(0,"Brightness")'),
    ('Corpus', 'MidiPitch', 'bool', ('off', 'on'), 0, 0, 'FUN_1030e277c FUN_10319285c(+0x3e8,"MIDI Frequency",0)'),
    ('Corpus', 'MidiGate', 'bool', ('off', 'on'), 0, 0, 'FUN_1030e277c FUN_10319285c(+0x418,"Note Off",0)'),
    ('Corpus', 'ExcitationX', *L01, 0.5, 0, 'FUN_1030e277c FUN_103192720(0.5,"Hit")'),
    ('Corpus', 'ListeningXL', *L01, 0.1, 0, 'FUN_1030e277c FUN_103192720(0x3dcccccd,"Listening L")'),
    ('Corpus', 'ListeningXR', *L01, 0.9, 0, 'FUN_1030e277c FUN_103192720(0x3f666666,"Listening R")'),
    ('Corpus', 'LfoOnOff', 'bool', ('off', 'on'), 0, 0, 'FUN_1030e3830 FUN_10319285c(+0x490,"LFO On/Off",0)'),
    ('Corpus', 'LfoType', 'enum', ('Sine', 'Square', 'Triangle', 'SawUp', 'SawDown', 'Sample & Hold', 'Random Ramp'), 0, 0, 'FUN_1030e3830 FUN_1026ef060(+0x4a8,0,...)'),
    ('Corpus', 'LfoSync', 'enum', ('Free', 'Sync'), 0, 0, 'FUN_1030e3830 FUN_1026ef060(+0x4c0,0,...)'),
    ('Corpus', 'LfoRate', *L01, 0.5, 0, 'FUN_1030e3830 FUN_103192720(0.5,"LFO Rate")'),
    ('Corpus', 'LfoSyncRate', 'legacyint', (0, 21), (0, 21), 4, 0, 'FUN_1030e3830 FUN_1026f0b58(0,22-1,FUN_1020ee0f4()=4) ALegacyQuantingInt(0,21)'),
    ('Corpus', 'LfoStereoMode', 'enum', ('Phase', 'Spin'), 0, 0, 'FUN_1030e3830 FUN_1026ef060(+0x520,0,...)'),
    ('Corpus', 'LfoSpin', 'linear', (0, 0.5), (0, 0.5), 0, 0, 'FUN_1030e3830 FUN_1026f0b58(0,0.5,0) ALinear(0,0.5)'),
    ('Corpus', 'LfoPhase', 'linear', (0, 360), (0, 360), 180, 0, 'FUN_1030e3830 FUN_1026f0b58(0,360,180) ALinear(0,360)'),
    ('Corpus', 'LfoOffset', 'linear', (0, 360), (0, 360), 0, 0, 'FUN_1030e3830 FUN_1026f0b58(0,360,0) ALinear(0,360)'),
    ('Corpus', 'LfoAmount', *L01, 0, 0, 'FUN_1030e3830 FUN_103192720(0,"LFO Amount")'),
    ('Corpus', 'FilterOn', 'bool', ('off', 'on'), 0, 0, 'FUN_1030e4c94 FUN_10319285c(+0x598,"Filter On/Off",0)'),
    ('Corpus', 'FilterMidFreq', 'log10', (0, 1), (50, 18000), 1000, 0, 'FUN_1030e4c94 FUN_1026f0b58(0,1,1000) ALog10(50,18000)'),
    ('Corpus', 'FilterBandWidth', 'linear', (0.5, 9), (0.5, 9), 4, 0, 'FUN_1030e4c94 FUN_1026f0b58(0.5,9,4) ALinear(0.5,9)'),
    ('Corpus', 'Drive', *L01, 0.5, 0, 'FUN_1030e12c8 FUN_103192720(0.5,"Gain")'),
    ('Corpus', 'StereoWidth', *L01, 1.0, 0, 'FUN_1030e12c8 FUN_103192720(1.0,"Width")'),
    ('Corpus', 'DryWet', *L01, 0.5, 0, 'FUN_1030e12c8 FUN_103192720(0.5,"Dry Wet")'),
    ('Corpus', 'ResonatorQuality', 'enum', ('Eco', 'Low', 'Med', 'High'), 2, 0, 'FUN_1030e277c FUN_1026ef060(+0x628,2,...)'),
    ('Corpus', 'DecayOnNoteOff', *L01, 0, (6, (-1.0, 1.0)), 'FUN_1030e277c FUN_103192720(0,"Note Off Decay"); FUN_1030e54e8 entry mode 6 (mult -1, off 1)'),
    ('Corpus', 'TubeOpening', *L01, 1.0, 0, 'FUN_1030e277c FUN_103192720(1.0,"Opening")'),
    ('Corpus', 'Bleed', *L01, 0, 0, 'FUN_1030e277c FUN_103192720(0,"Bleed")'),
    ('Corpus', 'MidiMode', 'enum', ('Last', 'Low'), 0, 0, 'FUN_1030e277c FUN_1026ef060(+0x400,0,["Last","Low"])'),
]
# CorpusWrapper::SetParameter (helper corpus FUN_0000d75c), then WrapperTemplate<CorpusSynth,37> (FUN_000050c0).
DEFAULT_RULE = 'default: kind 3 -> int(min(v,max)); else min(v,1) -> v<=0.5 ? 128v : 126v+1'
CORPUS_RULE = {0: 'int table[1,2,3,4,5,7,6][int(v)] if int(v)<7 else 0',
               2: 'v<0 ? 63.5v+63.5 : 63v+64', 3: 'v<0 ? 63.5v+63.5 : 63v+64',
               9: 'v<0 ? 63.5v+63.5 : 63v+64', 11: 'v<0 ? 63.5v+63.5 : 63v+64',
               5: '1-v<=0.5 ? 127(1-v) : 127-126v', 7: 'int(int(v)+48)', 8: '63.5+1.27v',
               14: '64+31.5v', 15: '64+31.5v', 16: '64+31.5v', 22: 'int(v!=0 ? 0 : 1)',
               23: 'v<=0.5 ? 127v : 126v+1', 24: 'v<180 ? 0.35277778v : 0.35v+1',
               25: 'v<180 ? 0.35277778v : 0.35v+1', 29: '14.941176v-7.470588',
               37: 'ignored (default path accepts index < 37 only)'}


def sent(conv, p, c, u):
    """Value placed on the index for stored user value u (static derivation)."""
    if conv in ('enum', 'bool'):
        return float(u)
    lo, hi = p
    if conv == 'log10':
        v = lo if u <= 0 else math.log10(u / c[0]) / math.log10(c[1] / c[0])
    elif conv == 'quantizing':
        v = u
    else:
        v = u if (c[0], c[1]) == (lo, hi) else lo + (u - c[0]) / (c[1] - c[0]) * (hi - lo)
    v = min(max(v, lo), hi)
    if conv == 'legacyint':  # ConvertQuantingInt (0x101bb9f34): frinta to 1/32768, then fcvtzs (toward 0)
        q = v * 32768.0
        q = math.copysign(math.floor(abs(q) + 0.5), q)
        v = float(math.trunc(q * 3.0517578125e-05))
    return v


def selfcheck():
    assert sent('legacyint', (0, 24), (0, 24), 11.99999) == 12.0  # rounds within 1/65536 of the next integer
    assert sent('legacyint', (-48, 48), (-48, 48), -3.7) == -3.0    # otherwise truncates toward zero
    assert sent('linear', (0, 1), (0, 10), 12) == 1.0                # Amp: stored/10, clamped
    assert abs(sent('log10', (0, 1), (50, 18000), 1000) - 0.508950) < 1e-6
    assert sent('log10', (0, 1), (50, 18000), 0) == 0                # u <= 0 -> internal minimum


# Cross-check for the six priority Corpus parameters. Live side: this packet. Bundle wrapper (FUN_0000d75c /
# FUN_000050c0): read here. Engine drivers: copied from corpus-dsp-v1/report-chain.md and report-resonator.md
# (another session), NOT re-verified here. Resonator parameters use c = trunc(controller); the Modulator keeps
# floats (report-resonator.md); the filter module is assumed to keep floats (not stated there).
def _lin(c, lo, hi):
    n = 0.5 if c == 64 else c / 127
    return lo + (hi - lo) * n


def _d(v):
    v = min(v, 1.0)
    return 128 * v if v <= 0.5 else 126 * v + 1


PRIORITY = [  # name, host index, Live conversion, bundle rule, engine mapping, sample stored values
    ('Frequency', 6, lambda s: sent('linear', (0, 1), (0, 1), s), _d,
     lambda c: 261.62 * 2 ** _lin(c, -4, 4), 'Hz (Mod:4 fixed_pitch, -4..4 oct around 261.62 Hz, float)', (0, 0.25, 0.5, 0.75, 1)),
    ('Radius', 5, lambda s: sent('linear', (0, 1), (0, 1), s),
     lambda v: 127 * (1 - v) if 1 - v <= 0.5 else 127 - 126 * v,
     lambda c: 0.005 * 80 ** (math.trunc(c) / 127), 'tube_radius (Res:71 exp 0.005..0.4, truncated c)', (0, 0.25, 0.5, 0.75, 1)),
    ('ExcitationX', 14, lambda s: sent('linear', (0, 1), (0, 1), s), lambda v: 64 + 31.5 * v,
     lambda c: _lin(math.trunc(c), 0.05, 0.95), 'exci_x (Res:34 lin 0.05..0.95, truncated c)', (0, 0.5, 1)),
    ('ListeningXL', 15, lambda s: sent('linear', (0, 1), (0, 1), s), lambda v: 64 + 31.5 * v,
     lambda c: _lin(math.trunc(c), 0.01, 0.99), 'list_l_x (Res:30 lin 0.01..0.99, truncated c)', (0, 0.1, 1)),
    ('ListeningXR', 16, lambda s: sent('linear', (0, 1), (0, 1), s), lambda v: 64 + 31.5 * v,
     lambda c: _lin(math.trunc(c), 0.01, 0.99), 'list_r_x (Res:32 lin 0.01..0.99, truncated c)', (0, 0.9, 1)),
    ('FilterMidFreq', 28, lambda s: sent('log10', (0, 1), (50, 18000), s), _d,
     lambda c: 50 * 360 ** (c / 127), 'Hz (Filters:1 mid_freq exp 50..18000, float assumed)', (50, 948.68, 1000, 5000, 18000)),
]


def priority(out):
    with open(os.path.join(out, 'corpus_priority.tsv'), 'w') as f:
        f.write('stored_name\thost_index\tstored\tvalue_passed\tcontroller\tengine_value\tengine_target\n')
        for name, i, live, rule, eng, unit, samples in PRIORITY:
            for s in samples:
                v = live(s)
                c = rule(v)
                f.write(f'{name}\t{i}\t{s:g}\t{v:.6g}\t{c:.6g}\t{eng(c):.6g}\t{unit}\n')


def main(out, h4):
    selfcheck()
    order = {}
    for r in csv.DictReader(open(os.path.join(out, 'live_index_map.tsv')), delimiter='\t'):
        order.setdefault(r['device'], []).append(r['name'])
    stored = {(r['device'], r['path']): r for r in csv.DictReader(open(os.path.join(h4, 'param_table.tsv')), delimiter='\t')}
    rows, idx = [], {}
    for spec in SPEC:
        if len(spec) == 7:  # enum/bool rows carry labels instead of (internal, user)
            dev, name, conv, p, d, mode, src = spec
            c = None
        else:
            dev, name, conv, p, c, d, mode, src = spec
        key = name.split(',')[0].strip('(') if name.startswith('(') else name
        i = order[dev].index(key) if key in order[dev] else None
        st = stored.get((dev, name))
        if conv in ('enum', 'bool'):
            labels, dom = p, ('64..127' if conv == 'bool' else f'0..{len(p) - 1}')
            internal = f'0..{len(p) - 1}'
            v = float(d)
        else:
            labels, dom = None, f'{c[0]:g}..{c[1]:g}'
            internal = f'{p[0]:g}..{p[1]:g}'
            v = sent(conv, p, c, d)
        if isinstance(mode, tuple) and mode[0] == 6:
            v, mtxt = mode[1][1] + mode[1][0] * v, f'6 MultiplyOffset {mode[1][1]:g}{mode[1][0]:+g}*v'
        elif isinstance(mode, tuple) and mode[0] == 7:
            v, mtxt = float(mode[1][int(v)]), f'7 IntegerMapping {mode[1]}'
        else:
            mtxt = 'not sent' if mode is None else '0 identity'
        if st:
            assert st['range'] == dom, (dev, name, st['range'], dom)
        row = {'device': dev, 'index': '' if i is None else i, 'stored_name': name, 'class': conv,
               'stored_domain': dom, 'labels': '|'.join(labels) if labels else '', 'default': f'{d:g}',
               'default_preset': st['default'] if st else '', 'internal_range': internal, 'mode': mtxt,
               'sent_for_default': f'{v:.6g}' if mode is not None else '',
               'bundle_rule': (CORPUS_RULE.get(i, DEFAULT_RULE) if dev == 'Corpus' else ''), 'source': src}
        rows.append(row)
        idx.setdefault(dev, []).append(key)
    for dev, names in order.items():  # every vector entry described, in the extracted order
        assert [n for n in idx[dev] if n in names] == names, dev
    cols = list(rows[0])
    for fn, sel in (('conversions.tsv', rows), ('corpus_parameters.tsv', [r for r in rows if r['device'] == 'Corpus'])):
        with open(os.path.join(out, fn), 'w') as f:
            f.write('\t'.join(cols) + '\n')
            for r in sel:
                f.write('\t'.join(str(r[k]) for k in cols) + '\n')
    priority(out)
    print(f'{len(rows)} rows; checks passed')


if __name__ == '__main__':
    main(*sys.argv[1:3])
