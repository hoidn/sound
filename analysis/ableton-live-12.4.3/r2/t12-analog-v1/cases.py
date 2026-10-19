"""Reference renders for SPEC-DEVICE-ANALOG acceptance cases (DAN-xxx).

    python3 -I cases.py        # writes raw/<case>.wav, raw/<case>.script, results/cases.json

Each case: a parameter set (stored values on the table defaults, the Defaults-preset values, or the
probe set of measure.py), note events at absolute frames, a sample rate and a length. The render protocol
is an.script: create, rate, all 203 host values in index order, events, input flag 0, silent input,
host blocks of 512 frames (other sizes where a case says so). Output is written as IEEE-float 32-bit WAV,
mono when both channels are bit-identical, else stereo; the bytes are the render's binary32 samples
unchanged. Dependencies: numpy, an, measure (probe sets).
"""
import hashlib
import json
import struct
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import an  # noqa: E402
import measure  # noqa: E402

C1, C2, FE, AE = measure.C1, measure.C2, measure.FE, measure.AE
RAW = HERE / 'raw'
S1 = 44100


def wav(path, y, fs):
    """IEEE float WAV (format 3) with a fact chunk; y is frames x channels float32."""
    y = np.ascontiguousarray(y, '<f4')
    ch = y.shape[1]
    data = y.tobytes()
    fmt = struct.pack('<HHIIHHH', 3, ch, fs, fs * 4 * ch, 4 * ch, 32, 0)
    body = b'WAVE' + b'fmt ' + struct.pack('<I', len(fmt)) + fmt + b'fact' + struct.pack('<II', 4, len(y)) + b'data' + struct.pack('<I', len(data)) + data
    Path(path).write_bytes(b'RIFF' + struct.pack('<I', len(body)) + body)


def seq(notes, start=4400, step=None):
    """Events for (key, velocity, on_offset, off_offset) tuples relative to start."""
    ev = []
    for k, v, a, b in notes:
        ev.append((start + a, 0x90, k, v))
        if b is not None:
            ev.append((start + b, 0x80, k, 64))
    return ev


def P(**ch):
    return ('probe', ch)


def T(**ch):
    return ('table', ch)


def R(**ch):
    return ('preset', ch)


NOTE = seq([(60, 100, 0, 22050)])                        # C4 at frame 4,400 for 0.5 s
HOLD = seq([(60, 100, 0, None)])
CHORD = seq([(48, 100, 0, 22050), (55, 90, 4400, 22050), (64, 110, 8800, 22050)])
SAW, RECT = {C1 + 'OscillatorWaveShape': 1}, {C1 + 'OscillatorWaveShape': 2}
FON = {C1 + 'FilterToggle': 1, C1 + 'FilterCutoffFrequency': 0.5, C1 + 'FilterQFactor': 0.6}

CASES = {
    'DAN-001': ('Table defaults, C4', T(), NOTE, S1, 66150),
    'DAN-002': ('Table defaults, C4, 48 kHz', T(), seq([(60, 100, 0, 24000)], 4800), 48000, 72000),
    'DAN-003': ('Defaults preset, C4', R(), NOTE, S1, 66150),
    'DAN-004': ('Defaults preset, three-note chord', R(), CHORD, S1, 66150),
    'DAN-005': ('Defaults preset, chord, 48 kHz', R(), seq([(48, 100, 0, 24000), (55, 90, 4800, 24000), (64, 110, 9600, 24000)], 4800), 48000, 72000),
    'DAN-006': ('Probe, sine, C4', P(), HOLD, S1, 26460),
    'DAN-007': ('Probe, saw, C4', P(**SAW), HOLD, S1, 26460),
    'DAN-008': ('Probe, rectangle, PW 0.5', P(**RECT), HOLD, S1, 26460),
    'DAN-009a': ('Probe, rectangle, PW 0', P(**RECT, **{C1 + 'OscillatorPulseWidth': 0}), HOLD, S1, 26460),
    'DAN-009b': ('Probe, rectangle, PW 1', P(**RECT, **{C1 + 'OscillatorPulseWidth': 1}), HOLD, S1, 26460),
    'DAN-010': ('Probe, sine, release 0, keys 24, 69, 108 for 0.9 s each, 1 s apart', P(**{AE + 'ReleaseTime': 0}), seq([(24, 100, 0, 39690), (69, 100, 44100, 83790), (108, 100, 88200, 127890)]), S1, 136500),
    'DAN-011a': ('Probe, sine, Octave 1, Transpose 7, FineTune 0.75', P(Octave=1, Transpose=7, KeyboardFineTune=0.75), HOLD, S1, 26460),
    'DAN-011b': ('Probe, sine, OscillatorOct -1, OscillatorSemi -5, Detune 0.25', P(**{C1 + 'OscillatorOct': -1, C1 + 'OscillatorSemi': -5, C1 + 'OscillatorDetune': 0.25}), HOLD, S1, 26460),
    'DAN-011c': ('Probe, sine, key 96, Stretch 1', P(KeyboardStretch=1), seq([(96, 100, 0, None)]), S1, 26460),
    'DAN-012': ('Probe, noise only, Color 0.5 (not sample-graded)', P(**{C1 + 'OscillatorToggle': 0, 'NoiseToggle': 1, 'NoiseBalance': 1}), HOLD, S1, 48510),
    'DAN-013': ('Probe, saw C3, LP12 cutoff 0.5 Q 0.6', P(**SAW, **FON), seq([(48, 100, 0, None)]), S1, 26460),
}
for t, name in enumerate(('LP24', 'BP6', 'BP12', 'Notch2', 'Notch4', 'HP12', 'HP24', 'Formant6', 'Formant12'), start=1):
    CASES[f'DAN-{13 + t:03d}'] = (f'Probe, saw C3, {name} cutoff 0.5 Q 0.6', P(**SAW, **FON, **{C1 + 'FilterType': t}), seq([(48, 100, 0, None)]), S1, 26460)
CASES.update({
    'DAN-023': ('Probe, saw C3, LP24, filter envelope 0.75 with decay 0.4 to sustain 0', P(**SAW, **{**FON, C1 + 'FilterType': 1, C1 + 'FilterCutoffFrequency': 0.3, C1 + 'FilterEnvCutoffMod': 0.75, FE + 'DecayTime': 0.4, FE + 'SustainLevel': 0}), seq([(48, 100, 0, None)]), S1, 44100),
    'DAN-024': ('Probe, saw, LP12, keyboard tracking 0.5, keys 48 and 72 in turn', P(**SAW, **FON, **{C1 + 'FilterKbdCutoffMod': 0.5}), seq([(48, 100, 0, 13230), (72, 100, 17640, 30870)]), S1, 35280),
    'DAN-025': ('Probe, saw C2, Drive Sym3, oscillator level 1', P(**SAW, **{C1 + 'FilterToggle': 1, C1 + 'FilterCutoffFrequency': 0.8, C1 + 'FilterDrive': 3, C1 + 'OscillatorLevel': 1, C1 + 'AmplifierLevel': 0.6}), seq([(36, 100, 0, None)]), S1, 26460),
    'DAN-026': ('Probe, saw C2, Drive Asym3, oscillator level 1', P(**SAW, **{C1 + 'FilterToggle': 1, C1 + 'FilterCutoffFrequency': 0.8, C1 + 'FilterDrive': 6, C1 + 'OscillatorLevel': 1, C1 + 'AmplifierLevel': 0.6}), seq([(36, 100, 0, None)]), S1, 26460),
    'DAN-027': ('Probe, saw C3, all levels at maximum (output saturator)', P(**SAW, **{C1 + 'OscillatorLevel': 1, C1 + 'AmplifierLevel': 1, 'Volume': 1}), seq([(48, 100, 0, None)]), S1, 26460),
    'DAN-028': ('Probe, rectangle, amplitude ADSR 0.4/0.4/0.5/0.4, exponential', P(**RECT, **{C1 + 'OscillatorPulseWidth': 1, AE + 'AttackTime': 0.4, AE + 'DecayTime': 0.4, AE + 'SustainLevel': 0.5, AE + 'ReleaseTime': 0.4}), seq([(60, 100, 0, 30870)]), S1, 44100),
    'DAN-029': ('As DAN-028, linear slopes', P(**RECT, **{C1 + 'OscillatorPulseWidth': 1, AE + 'AttackTime': 0.4, AE + 'DecayTime': 0.4, AE + 'SustainLevel': 0.5, AE + 'ReleaseTime': 0.4, AE + 'ExponentialSlope': 0}), seq([(60, 100, 0, 30870)]), S1, 44100),
    'DAN-030': ('Probe, rectangle, sustain 0.75, sustain time 0.5', P(**RECT, **{C1 + 'OscillatorPulseWidth': 1, AE + 'DecayTime': 0.2, AE + 'SustainLevel': 0.75, AE + 'SustainTime': 0.5}), seq([(60, 100, 0, None)]), S1, 66150),
    'DAN-031': ('Probe, amplitude envelope AmpMod 0.5, velocities 1, 64, 127 in turn', P(**{AE + 'AmpMod': 0.5}), seq([(60, 1, 0, 8820), (60, 64, 13230, 22050), (60, 127, 26460, 35280)]), S1, 39690),
    'DAN-032': ('Probe, attack 0.4 with AttackMod 0.5, velocity 127', P(**{AE + 'AttackTime': 0.4, AE + 'AttackMod': 0.5}), seq([(60, 127, 0, None)]), S1, 22050),
    'DAN-033': ('Probe, sine A5, LFO 1 sine at speed 0.75 on pitch 0.25', P(**{C1 + 'LFOToggle': 1, C1 + 'LFOSpeed': 0.75, C1 + 'OscillatorLFOModPitch': 0.25}), seq([(81, 100, 0, None)]), S1, 48510),
    'DAN-034': ('Probe, sine A5, LFO 1 square on pitch 0.25, PW 0.25', P(**{C1 + 'LFOToggle': 1, C1 + 'LFOWaveShape': 2, C1 + 'LFOSpeed': 0.75, C1 + 'LFOPulseWidth': 0.25, C1 + 'OscillatorLFOModPitch': 0.25}), seq([(81, 100, 0, None)]), S1, 48510),
    'DAN-035': ('Probe, sine A5, pitch envelope amount 0.5, time 0.5', P(**{C1 + 'OscillatorEnvAmount': 0.5, C1 + 'OscillatorEnvTime': 0.5}), seq([(81, 100, 0, None)]), S1, 26460),
    'DAN-036': ('Probe, sine A5, vibrato amount 0.75, delay 0.5, fade 0.5', P(VibratoToggle=1, VibratoAmount=0.75, VibratoDelay=0.5, VibratoFadeIn=0.5), seq([(81, 100, 0, None)]), S1, 88200),
    'DAN-037': ('Probe, saw, Sub amount 1', P(**SAW, **{C1 + 'OscillatorMode': 0, C1 + 'OscillatorSubAmount': 1}), HOLD, S1, 26460),
    'DAN-038': ('Probe, saw, Sync amount 0.5', P(**SAW, **{C1 + 'OscillatorMode': 1, C1 + 'OscillatorSubAmount': 0.5}), HOLD, S1, 26460),
    'DAN-039': ('Probe, Polyphony 1 (two voices), three overlapping notes', P(Polyphony=1), seq([(48, 100, 0, 30870), (72, 100, 4400, 30870), (96, 100, 17600, 30870)]), S1, 44100),
    'DAN-040': ('Probe, Polyphony 0 (mono), priority Last, key sequence', P(Polyphony=0), [(4400, 0x90, 60, 100), (13200, 0x90, 67, 100), (22000, 0x90, 64, 100), (30800, 0x80, 67, 64), (39600, 0x80, 64, 64), (48400, 0x80, 60, 64)], S1, 66150),
    'DAN-041': ('Chain 2: oscillator 2 into filter 2 (HP12 following filter 1), filter 1 into filter 2 at 1', P(**SAW, **FON, **{C2 + 'OscillatorToggle': 1, C2 + 'OscillatorWaveShape': 2, C2 + 'OscillatorBalance': 0, C2 + 'FilterToggle': 1, C2 + 'FilterType': 6, C2 + 'FilterCutoffFrequency': 0.4, C2 + 'FilterControllee': 1, C2 + 'AmplifierToggle': 1, C2 + 'Envelope.0/SustainLevel': 1, C2 + 'Envelope.1/SustainLevel': 1, C1 + 'FilterToFilter2': 1}), seq([(48, 100, 0, None)]), S1, 26460),
    'DAN-042': ('Event timing: note-on at frame 1,001 (off the control grid)', P(), [(1001, 0x90, 60, 100), (3011, 0x80, 60, 64)], S1, 8192),
    'DAN-043': ('Glide on, mono, legato C5 to C6 (not graded)', P(Polyphony=0, PortamentoToggle=1, PortamentoTime=0.75), [(4400, 0x90, 72, 100), (26400, 0x90, 84, 100)], S1, 66150),
    'DAN-044': ('Unison on, 4 voices, detune 0.5 (not graded)', P(**SAW, KeyboardUnisonToggle=1, KeyboardUnison=1, KeyboardDetune=0.5), HOLD, S1, 26460),
})
BLOCKS = {'DAN-045a': ('DAN-004', 64), 'DAN-045b': ('DAN-004', 2048)}


def stored_for(spec):
    which, ch = spec
    return measure.probe(**ch) if which == 'probe' else an.stored(which, **ch)


def main():
    RAW.mkdir(exist_ok=True)
    out = {}

    def run(item):
        cid, (desc, spec, ev, fs, frames) = item
        (Path(an.SCRATCH) / 'cases').mkdir(parents=True, exist_ok=True)
        f32 = Path(an.SCRATCH) / 'cases' / f'{cid}.f32'
        y, log = an.render(stored_for(spec), ev, fs=fs, frames=frames, out=f32)
        mono = bool(np.array_equal(y[:, 0].view(np.uint32), y[:, 1].view(np.uint32)))
        wav(RAW / f'{cid}.wav', y[:, :1] if mono else y, fs)
        (RAW / f'{cid}.script').write_text(f32.with_suffix('.script').read_text())
        f32.with_suffix('.script').unlink()
        rec = dict(description=desc, parameter_set=spec[0], changes=spec[1], events=[list(e) for e in ev], fs=fs, frames=frames,
                   block=512, channels=1 if mono else 2, f32_sha256=hashlib.sha256(f32.read_bytes()).hexdigest(),
                   wav_sha256=hashlib.sha256((RAW / f'{cid}.wav').read_bytes()).hexdigest(), imports=an.xdevpy.used_imports(log),
                   peak=float(np.abs(y).max()), first_nonzero=an.first_above(y, 0))
        f32.unlink()
        return cid, rec
    for cid, rec in an.pmap(run, CASES.items()):
        out[cid] = rec
    for cid, (src, block) in BLOCKS.items():
        desc, spec, ev, fs, frames = CASES[src]
        y, _ = an.render(stored_for(spec), ev, fs=fs, frames=frames, block=block)
        y0, _ = an.render(stored_for(spec), ev, fs=fs, frames=frames)
        out[cid] = dict(description=f'{src} in host blocks of {block}', source=src, block=block,
                        bit_identical_to_source=bool(np.array_equal(y.view(np.uint32), y0.view(np.uint32))))
    (HERE / 'results' / 'cases.json').write_text(json.dumps(dict(sorted(out.items())), indent=1) + '\n')
    for cid, rec in sorted(out.items()):
        print(cid, rec.get('wav_sha256', rec.get('bit_identical_to_source')), rec.get('peak'), rec.get('first_nonzero'))


if __name__ == '__main__':
    main()
