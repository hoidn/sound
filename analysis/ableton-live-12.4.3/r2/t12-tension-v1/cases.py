"""Reference-render cases for Tension (SPEC-DEVICE-TENSION). Each case is a set of stored-value changes
(applied to the constructor defaults, or to a shipped preset), note events and a sample rate.

    from cases import CASES        # name -> dict(changes, base, events, fs, frames, group)

Default event pattern: C4 (note 60), velocity 100, note-on at frame 4096, note-off 0.5 s later
(frame 26146 at 44.1 kHz); 1 s rendered in host blocks of 512 frames.
"""
import tension as T

ON, HELD = 4096, 22050


def _c(changes=None, n=60, vel=100, fs=44100, base=None, group='', preset=None):
    held = HELD if fs == 44100 else 24000
    return dict(changes=changes or {}, preset=preset, base=base, events=T.note(n, vel, ON, held), fs=fs, frames=fs, group=group,
                note=n, vel=vel, on=ON, off=ON + held)


BRIGHT = {'ExcitatorType': 1, 'ExcitatorStiffness': 1, 'StringDamping': 1, 'StringDecay': 1, 'StringInharmonicity': 0}
PRESETS = {'preset_defaults': 'Defaults/Instruments/Tension.adv',
           'preset_steel_guitar': 'Devices/Instruments/Tension/Guitar & Plucked/Steel Basic Guitar.adv',
           'preset_clav_clicky': 'Devices/Instruments/Tension/Piano & Keys/Clav Clicky.adv',
           'preset_nice_harp': 'Devices/Instruments/Tension/Guitar & Plucked/Nice Harp.adv',
           'preset_cello': 'Devices/Instruments/Tension/Strings/Cello Strings.adv'}

CASES = {
    'defaults_44': _c(group='P'),
    'defaults_48': _c(fs=48000, group='P'),
    'note_36': _c(n=36, group='N'), 'note_48': _c(n=48, group='N'), 'note_72': _c(n=72, group='N'), 'note_84': _c(n=84, group='N'),
    'vel_1': _c(vel=1, group='N'), 'vel_127': _c(vel=127, group='N'),
    'velmod_1': _c({'ExcitatorVelocityVelMod': 0.5}, vel=1, group='N'), 'velmod_64': _c({'ExcitatorVelocityVelMod': 0.5}, vel=64, group='N'),
    'velmod_127': _c({'ExcitatorVelocityVelMod': 0.5}, vel=127, group='N'),
    'exc_bow': _c({'ExcitatorType': 0}, group='E'), 'exc_hammer': _c({'ExcitatorType': 1}, group='E'),
    'exc_bounce': _c({'ExcitatorType': 2}, group='E'),
    'plk_x0': _c({'ExcitatorParameterX': 0}, group='E'), 'plk_x1': _c({'ExcitatorParameterX': 1}, group='E'),
    'plk_stiff0': _c({'ExcitatorStiffness': 0}, group='E'), 'plk_damp0': _c({'ExcitatorDamping': 0}, group='E'),
    'ham_x1': _c({'ExcitatorType': 1, 'ExcitatorParameterX': 1}, group='E'),
    'ham_stiff1': _c({'ExcitatorType': 1, 'ExcitatorStiffness': 1}, group='E'),
    'ham_damp1': _c({'ExcitatorType': 1, 'ExcitatorDamping': 1}, group='E'),
    'bow_x1': _c({'ExcitatorType': 0, 'ExcitatorParameterX': 1}, group='E'),
    'pos_0': _c({'GeoExcitatorPosition': 0}, group='E'), 'pos_1': _c({'GeoExcitatorPosition': 1}, group='E'),
    'str_decay_0.25': _c({'StringDecay': 0.25}, group='S'), 'str_decay_1': _c({'StringDecay': 1}, group='S'),
    'str_damp_0': _c({'StringDamping': 0}, group='S'), 'str_damp_1': _c({'StringDamping': 1}, group='S'),
    'str_ratio_0': _c({'StringDecayRatio': 0}, group='S'), 'str_ratio_1': _c({'StringDecayRatio': 1}, group='S'),
    'str_inharm_0': _c({'StringInharmonicity': 0}, group='S'), 'str_inharm_1': _c({'StringInharmonicity': 1}, group='S'),
    'damper_on': _c({'DamperToggle': 1}, group='D'), 'damper_gated': _c({'DamperToggle': 1, 'DamperGated': 1}, group='D'),
    'damper_pos_0': _c({'DamperToggle': 1, 'GeoDamperPosition': 0}, group='D'),
    'damper_mass_0': _c({'DamperToggle': 1, 'DamperMass': 0}, group='D'),
    'term_on': _c({'TerminationToggle': 1}, group='T'),
    'term_force_0': _c({'TerminationToggle': 1, 'TerminationFingerForce': 0}, group='T'),
    'pickup_on': _c({'PickupToggle': 1}, group='K'), 'pickup_pos_0': _c({'PickupToggle': 1, 'PickupPosition': 0}, group='K'),
    **{f'body_type_{t}': _c({'BodyToggle': 1, 'BodyType': t}, group='B') for t in range(4)},
    'body_size_0': _c({'BodyToggle': 1, 'BodySize': 0}, group='B'), 'body_size_4': _c({'BodyToggle': 1, 'BodySize': 4}, group='B'),
    'body_decay_1': _c({'BodyToggle': 1, 'BodyDecay': 1}, group='B'), 'body_mix_1': _c({'BodyToggle': 1, 'BodyMix': 1}, group='B'),
    'filt_base': _c(BRIGHT, n=36, group='F'),
    **{f'filt_t{t}': _c({**BRIGHT, 'FilterToggle': 1, 'FilterType': t}, n=36, group='F') for t in range(10)},
    'filt_t1_c0.25': _c({**BRIGHT, 'FilterToggle': 1, 'FilterType': 1, 'FilterCutoffFrequency': 0.25}, n=36, group='F'),
    'filt_t1_c0.75': _c({**BRIGHT, 'FilterToggle': 1, 'FilterType': 1, 'FilterCutoffFrequency': 0.75}, n=36, group='F'),
    'filt_t1_q0.5': _c({**BRIGHT, 'FilterToggle': 1, 'FilterType': 1, 'FilterQFactor': 0.5}, n=36, group='F'),
    'filt_t1_q1': _c({**BRIGHT, 'FilterToggle': 1, 'FilterType': 1, 'FilterQFactor': 1}, n=36, group='F'),
    **{k: _c(preset=v, group='M') for k, v in PRESETS.items()},
}


def host(case):
    base = T.preset_values(case['preset']) if case['preset'] else None
    return T.host_values(case['changes'], base)


def script(case, **kw):
    return T.script(host(case), case['events'], fs=case['fs'], frames=case['frames'], **kw)
