#### `Amp`

| Path below the device element | Class | Stored domain | Default when absent | Defaults preset (where different) |
| --- | --- | --- | --- | --- |
| `AmpType` | Enum | 0..6 | 2 |  |
| `Bass` | Float | 0..10 | 5 |  |
| `Middle` | Float | 0..10 | 5 |  |
| `Treble` | Float | 0..10 | 5 |  |
| `Presence` | Float | 0..10 | 5 |  |
| `Gain` | Float | 0..10 | 5 |  |
| `Volume` | Float | 0..10 | 9 |  |
| `DualMono` | Bool | true/false | false |  |
| `DryWet` | Float | 0..1 | 1 |  |

#### `Cabinet`

| Path below the device element | Class | Stored domain | Default when absent | Defaults preset (where different) |
| --- | --- | --- | --- | --- |
| `CabinetType` | Enum | 0..4 | 0 |  |
| `MicrophoneTypeSwitch` | Bool | true/false | false |  |
| `MicrophonePosition` | Enum | 0..2 | 0 |  |
| `DualMono` | Bool | true/false | false |  |
| `DryWet` | Float | 0..1 | 1 |  |

#### `UltraAnalog`

| Path below the device element | Class | Stored domain | Default when absent | Defaults preset (where different) |
| --- | --- | --- | --- | --- |
| `Polyphony` | Enum | 0..9 | 3 |  |
| `PitchBendRange` | Float | 0..1 | 0.1666666716 |  |
| `Volume` | Float | 0..1 | 0.7047889829 |  |
| `PerNotePitchBendRange` | Float | 0..48, integer steps | 0 | 48 |
| `ChannelPressureTarget{1,2}` | Enum | 0..46 | 0 |  |
| `ChannelPressureAmount{1,2}` | Float | -1..1 | 0.5 |  |
| `MpeCC74Target{1,2}` | Enum | 0..46 | 0 |  |
| `MpeCC74Amount{1,2}` | Float | -1..1 | 0.5 |  |
| `Octave` | Float | -3..3, integer steps | 0 |  |
| `Transpose` | Float | -12..12, integer steps | 0 |  |
| `KeyboardFineTune` | Float | 0..1 | 0.5 |  |
| `KeyboardUnisonToggle` | Bool | true/false | false |  |
| `KeyboardUnison` | Enum | 0..1 | 0 |  |
| `KeyboardDetune` | Float | 0..1 | 0 |  |
| `KeyboardUnisonDelay` | Float | 0..1 | 0 |  |
| `KeyboardPriority` | Enum | 0..2 | 2 |  |
| `KeyboardStretch` | Float | 0..1 | 0.5 |  |
| `KeyboardError` | Float | 0..1 | 0 |  |
| `VibratoToggle` | Bool | true/false | false |  |
| `VibratoSpeed` | Float | 0..1 | 0.5 |  |
| `VibratoFadeIn` | Float | 0..1 | 0 |  |
| `VibratoAmount` | Float | 0..1 | 0 |  |
| `VibratoError` | Float | 0..1 | 0 |  |
| `VibratoDelay` | Float | 0..1 | 0 |  |
| `VibratoModWheel` | Float | 0..1 | 0 |  |
| `PortamentoToggle` | Bool | true/false | false |  |
| `PortamentoTime` | Float | 0..1 | 0.5 |  |
| `PortamentoMode` | Enum | 0..1 | 0 |  |
| `PortamentoLegato` | Bool | true/false | false |  |
| `NoiseToggle` | Bool | true/false | false |  |
| `NoiseColor` | Float | 0..1 | 0.5 |  |
| `NoiseBalance` | Float | 0..1 | 0.5 | 1 |
| `NoiseLevel` | Float | 0..1 | 0.8062000275 |  |
| `SignalChain{1,2}/OscillatorToggle` | Bool | true/false | 1: true; 2: false | 2: true |
| `SignalChain{1,2}/OscillatorWaveShape` | Enum | 0..3 | 1 |  |
| `SignalChain{1,2}/OscillatorOct` | Float | -3..3, integer steps | 0 |  |
| `SignalChain{1,2}/OscillatorSemi` | Float | -12..12, integer steps | 0 |  |
| `SignalChain{1,2}/OscillatorMode` | Enum | 0..1 | 0 |  |
| `SignalChain{1,2}/OscillatorEnvTime` | Float | 0..1 | 0.5 |  |
| `SignalChain{1,2}/OscillatorDetune` | Float | 0..1 | 0.5 |  |
| `SignalChain{1,2}/OscillatorModulation1` | Float | 0..1 | 0.5 |  |
| `SignalChain{1,2}/OscillatorPulseWidth` | Float | 0..1 | 0.5 |  |
| `SignalChain{1,2}/OscillatorSubAmount` | Float | 0..1 | 0 |  |
| `SignalChain{1,2}/OscillatorBalance` | Float | 0..1 | 0.5 | 1: 1; 2: 1 |
| `SignalChain{1,2}/OscillatorEnvAmount` | Float | -1..1 | 0 |  |
| `SignalChain{1,2}/OscillatorLFOModPitch` | Float | -1..1 | 0 |  |
| `SignalChain{1,2}/OscillatorLFOModPW` | Float | -1..1 | 0 |  |
| `SignalChain{1,2}/OscillatorLevel` | Float | 0..1 | 0.8062000275 |  |
| `SignalChain{1,2}/FilterToggle` | Bool | true/false | false | 1: true |
| `SignalChain{1,2}/FilterType` | Enum | 0..9 | 0 | 1: 1 |
| `SignalChain{1,2}/FilterDrive` | Enum | 0..6 | 0 | 1: 1; 2: 1 |
| `SignalChain{1,2}/FilterKbdCutoffMod` | Float | -1..1 | 0 |  |
| `SignalChain{1,2}/FilterCutoffFrequency` | Float | 0..1 | 1 |  |
| `SignalChain{1,2}/FilterKbdQMod` | Float | -1..1 | 0 |  |
| `SignalChain{1,2}/FilterQFactor` | Float | 0..1 | 0 |  |
| `SignalChain{1,2}/FilterLFOCutoffMod` | Float | -1..1 | 0 |  |
| `SignalChain{1,2}/FilterEnvCutoffMod` | Float | -1..1 | 0 | 1: 0.7047610879; 2: 0.7047610879 |
| `SignalChain{1,2}/FilterLFOQMod` | Float | -1..1 | 0 |  |
| `SignalChain{1,2}/FilterEnvQMod` | Float | -1..1 | 0 |  |
| `SignalChain{1,2}/AmplifierToggle` | Bool | true/false | 1: true; 2: false |  |
| `SignalChain{1,2}/AmplifierKbdAmpMod` | Float | -1..1 | 0 |  |
| `SignalChain{1,2}/AmplifierLevel` | Float | 0..1 | 0.8690000176 | 1: 0.474311769; 2: 0.474311769 |
| `SignalChain{1,2}/AmplifierKbdPanMod` | Float | -1..1 | 0 |  |
| `SignalChain{1,2}/AmplifierPan` | Float | 0..1 | 0.5 |  |
| `SignalChain{1,2}/AmplifierLFOAmpMod` | Float | -1..1 | 0 |  |
| `SignalChain{1,2}/AmplifierLFOPanMod` | Float | -1..1 | 0 |  |
| `SignalChain{1,2}/AmplifierEnvPanMod` | Float | -1..1 | 0 |  |
| `SignalChain{1,2}/LFOToggle` | Bool | true/false | false |  |
| `SignalChain{1,2}/LFOWaveShape` | Enum | 0..4 | 0 |  |
| `SignalChain{1,2}/LFOSync` | Float | 0..23, integer steps | 13 |  |
| `SignalChain{1,2}/LFOSyncToggle` | Enum | 0..1 | 0 |  |
| `SignalChain{1,2}/LFOGateReset` | Bool | true/false | false |  |
| `SignalChain{1,2}/LFOPulseWidth` | Float | 0..1 | 0.5 |  |
| `SignalChain{1,2}/LFOSpeed` | Float | 0..1 | 0.5 |  |
| `SignalChain{1,2}/LFOPhase` | Float | 0..1 | 0 |  |
| `SignalChain{1,2}/LFODelay` | Float | 0..1 | 0 |  |
| `SignalChain{1,2}/LFOFadeIn` | Float | 0..1 | 0 |  |
| `SignalChain{1,2}/Envelope.{0,1}/ExponentialSlope` | Bool | true/false | true |  |
| `SignalChain{1,2}/Envelope.{0,1}/Loop` | Enum | 0..3 | 0 |  |
| `SignalChain{1,2}/Envelope.{0,1}/FreeRun` | Bool | true/false | false |  |
| `SignalChain{1,2}/Envelope.{0,1}/Legato` | Bool | true/false | false |  |
| `SignalChain{1,2}/Envelope.{0,1}/AttackMod` | Float | 0..1 | 0 |  |
| `SignalChain{1,2}/Envelope.{0,1}/AttackTime` | Float | 0..1 | 0 |  |
| `SignalChain{1,2}/Envelope.{0,1}/DecayTime` | Float | 0..1 | 0.6000000238 |  |
| `SignalChain{1,2}/Envelope.{0,1}/AmpMod` | Float | 0..1 | 0 | 1/1: 0.5; 2/1: 0.5 |
| `SignalChain{1,2}/Envelope.{0,1}/SustainLevel` | Float | 0..1 | 0 | 1/0: 0.5; 1/1: 0.5; 2/0: 0.5; 2/1: 0.5 |
| `SignalChain{1,2}/Envelope.{0,1}/SustainTime` | Float | 0..1 | 1 |  |
| `SignalChain{1,2}/Envelope.{0,1}/ReleaseTime` | Float | 0..1 | 0.6000000238 | 1/0: 0.4847841263; 1/1: 0.5718053579; 2/0: 0.4847841263; 2/1: 0.5718053579 |
| `SignalChain1/FilterToFilter2` | Float | 0..1 | 0 | 1 |
| `SignalChain2/FilterControllee` | Bool | true/false | false |  |

#### `StringStudio`

| Path below the device element | Class | Stored domain | Default when absent | Defaults preset (where different) |
| --- | --- | --- | --- | --- |
| `Polyphony` | Enum | 0..9 | 4 |  |
| `PitchBendRange` | Float | 0..12, integer steps | 2 |  |
| `Octave` | Float | -3..3, integer steps | 0 |  |
| `Transpose` | Float | -12..12, integer steps | 0 |  |
| `KeyboardFineTune` | Float | 0..1 | 0.5 |  |
| `KeyboardPriority` | Enum | 0..2 | 0 |  |
| `KeyboardUnisonToggle` | Bool | true/false | false |  |
| `KeyboardUnison` | Enum | 0..1 | 0 |  |
| `KeyboardDetune` | Float | 0..1 | 0.5 | 0 |
| `KeyboardUnisonDelay` | Float | 0..1 | 0.5 |  |
| `KeyboardStretch` | Float | 0..1 | 0.5 |  |
| `KeyboardError` | Float | 0..1 | 0 |  |
| `VibratoToggle` | Bool | true/false | false |  |
| `VibratoSpeed` | Float | 0..1 | 0.5 |  |
| `VibratoFadeIn` | Float | 0..1 | 0.5 |  |
| `VibratoAmount` | Float | 0..1 | 0.5 |  |
| `VibratoError` | Float | 0..1 | 0.5 |  |
| `VibratoDelay` | Float | 0..1 | 0.5 |  |
| `VibratoModWheel` | Float | 0..1 | 0.5 |  |
| `PortamentoToggle` | Bool | true/false | false |  |
| `PortamentoTime` | Float | 0..1 | 0.5 |  |
| `PortamentoProportional` | Bool | true/false | false |  |
| `PortamentoLegato` | Bool | true/false | false |  |
| `GeoExcitatorPosition` | Float | 0..1 | 0.5 |  |
| `GeoExcitatorAbsolute` | Bool | true/false | false |  |
| `GeoExcitatorKbdModulation` | Float | -1..1 | 0 |  |
| `GeoExcitatorVelModulation` | Float | -1..1 | 0 |  |
| `GeoDamperPosition` | Float | 0..1 | 0.5 |  |
| `GeoDamperAbsolute` | Bool | true/false | false |  |
| `GeoDamperKbdModulation` | Float | -1..1 | 0 |  |
| `GeoDamperVelModulation` | Float | -1..1 | 0 |  |
| `ExcitatorToggle` | Bool | true/false | true |  |
| `ExcitatorType` | Enum | 0..3 | 3 |  |
| `ExcitatorParameterX` | Float | 0..1 | 0.75 | 0.5 |
| `ExcitatorParameterXKbdMod` | Float | -1..1 | 0 |  |
| `ExcitatorParameterXVelMod` | Float | -1..1 | 0 |  |
| `ExcitatorStiffness` | Float | 0..1 | 0.5 |  |
| `ExcitatorStiffnessKbdMod` | Float | -1..1 | 0 |  |
| `ExcitatorStiffnessVelMod` | Float | -1..1 | 0 |  |
| `ExcitatorVelocity` | Float | 0..1 | 0.5 |  |
| `ExcitatorVelocityKbdMod` | Float | -1..1 | 0 |  |
| `ExcitatorVelocityVelMod` | Float | -1..1 | 0 |  |
| `ExcitatorDamping` | Float | 0..1 | 0.5 |  |
| `PickupToggle` | Bool | true/false | false |  |
| `PickupPosition` | Float | 0..1 | 0.5 |  |
| `DamperToggle` | Bool | true/false | false |  |
| `DamperMass` | Float | 0..1 | 0.5 |  |
| `DamperMassKbdMod` | Float | -1..1 | 0 |  |
| `DamperStiffness` | Float | 0..1 | 0.5 |  |
| `DamperStiffnessKbdMod` | Float | -1..1 | 0 |  |
| `DamperVelocity` | Float | 0..1 | 0.5 |  |
| `DamperVelocityKbdMod` | Float | -1..1 | 0 |  |
| `DamperDamping` | Float | 0..1 | 0.5 |  |
| `DamperGated` | Bool | true/false | false |  |
| `StringDamping` | Float | 0..1 | 0.5 |  |
| `StringDampingKbdMod` | Float | -1..1 | 0 |  |
| `StringDecay` | Float | 0..1 | 0.75 | 1 |
| `StringDecayKbdMod` | Float | -1..1 | 0 |  |
| `StringDecayRatio` | Float | 0..1 | 0.5 |  |
| `StringInharmonicity` | Float | 0..1 | 0.5 |  |
| `TerminationToggle` | Bool | true/false | false |  |
| `TerminationFingerStiffness` | Float | 0..1 | 0.5 |  |
| `TerminationFingerForce` | Float | 0..1 | 0.5 |  |
| `TerminationFingerForceKbdMod` | Float | -1..1 | 0 |  |
| `TerminationFingerForceVelMod` | Float | -1..1 | 0 |  |
| `TerminationFretStiffness` | Float | 0..1 | 0.5 |  |
| `LFOToggle` | Bool | true/false | false |  |
| `LFOWaveShape` | Enum | 0..4 | 0 |  |
| `LFOSync` | Float | 0..23, integer steps | 13 |  |
| `LFOSyncToggle` | Enum | 0..1 | 0 |  |
| `LFODelay` | Float | 0..1 | 0.5 |  |
| `LFOSpeed` | Float | 0..1 | 0.5 |  |
| `LFOFadeIn` | Float | 0..1 | 0.5 |  |
| `FilterToggle` | Bool | true/false | false | true |
| `FilterType` | Enum | 0..9 | 0 | 1 |
| `FilterCutoffFrequency` | Float | 0..1 | 0.5 | 1 |
| `FilterCutoffFrequencyKbdMod` | Float | -1..1 | 0 |  |
| `FilterCutoffFrequencyLFOMod` | Float | -1..1 | 0 |  |
| `FilterCutoffFrequencyEnvMod` | Float | -1..1 | 0 |  |
| `FilterQFactor` | Float | 0..1 | 0 |  |
| `FilterQFactorKbdMod` | Float | -1..1 | 0 |  |
| `FilterQFactorLFOMod` | Float | -1..1 | 0 |  |
| `FilterQFactorEnvMod` | Float | -1..1 | 0 |  |
| `FilterEnvelopeToggle` | Bool | true/false | false |  |
| `FilterEnvelopeAttack` | Float | 0..1 | 0 |  |
| `FilterEnvelopeDecay` | Float | 0..1 | 0.5 |  |
| `FilterEnvelopeSustain` | Float | 0..1 | 0.5 |  |
| `FilterEnvelopeRelease` | Float | 0..1 | 0.5 |  |
| `FilterEnvelopeAttackMod` | Float | 0..1 | 0 |  |
| `FilterEnvelopeAmpMod` | Float | 0..1 | 0 |  |
| `BodyToggle` | Bool | true/false | false |  |
| `BodyType` | Enum | 0..3 | 0 |  |
| `BodySize` | Enum | 0..4 | 2 |  |
| `BodyDecay` | Float | 0..1 | 0 |  |
| `BodyLowCut` | Float | 0..1 | 0 |  |
| `BodyHighCut` | Float | 0..1 | 0 |  |
| `BodyLevel` | Float | 0..1 | 0.7049999833 |  |
| `BodyMix` | Float | 0..1 | 0.5 |  |
| `PerNotePitchBendRange` | Float | 0..48, integer steps | 0 | 48 |
| `ChannelPressureTarget{1,2}` | Enum | 0..12 | 0 | 1: 5 |
| `ChannelPressureRange{1,2}` | Float | -1..1 | 0.5 | 1: 0.25 |
| `SlideTarget{1,2}` | Enum | 0..12 | 0 |  |
| `SlideRange{1,2}` | Float | -1..1 | 0.5 |  |

#### `Collision`

| Path below the device element | Class | Stored domain | Default when absent | Defaults preset (where different) |
| --- | --- | --- | --- | --- |
| `Mallet/OnOff` | Bool | true/false | true |  |
| `Mallet/Volume` | Float | 0..1 | 0.5 |  |
| `Mallet/VelToVolume` | Float | -5..5 | 0 |  |
| `Mallet/KeyToVolume` | Float | -2..2 | 0 |  |
| `Mallet/Stiffness` | Float | 0..1 | 0.5 |  |
| `Mallet/VelToStiffness` | Float | -5..5 | 0 |  |
| `Mallet/KeyToStiffness` | Float | -2..2 | 0 |  |
| `Mallet/NoiseAmount` | Float | 0..1 | 0.5 |  |
| `Mallet/VelToNoiseAmount` | Float | -5..5 | 0 |  |
| `Mallet/KeyToNoiseAmount` | Float | -2..2 | 0 |  |
| `Mallet/NoiseColor` | Float | 0..1 | 0.5 |  |
| `Noise/OnOff` | Bool | true/false | false |  |
| `Noise/Volume` | Float | 0..1 | 0.5 |  |
| `Noise/VelToVolume` | Float | -5..5 | 0 |  |
| `Noise/KeyToVolume` | Float | -2..2 | 0 |  |
| `Noise/FilterType` | Enum | 0..3 | 0 |  |
| `Noise/Freq` | Float | 0..1 | 0.5 |  |
| `Noise/VelToFreq` | Float | -8..8 | 0 |  |
| `Noise/KeyToFreq` | Float | -2..2 | 0 |  |
| `Noise/EnvToFreq` | Float | -5..5 | 0 |  |
| `Noise/Q` | Float | 0..1 | 0 |  |
| `Noise/Attack` | Float | 0..1 | 0 |  |
| `Noise/Decay` | Float | 0..1 | 0.200000003 |  |
| `Noise/Sustain` | Float | 0..1 | 0 |  |
| `Noise/Release` | Float | 0..1 | 0.200000003 |  |
| `Resonator{1,2}/OnOff` | Bool | true/false | false | 1: true |
| `Resonator{1,2}/Type` | Enum | 0..6 | 0 |  |
| `Resonator{1,2}/Quality` | Enum | 0..3 | 2 |  |
| `Resonator{1,2}/Transpose` | Float | -48..48, integer steps | 0 |  |
| `Resonator{1,2}/FineTranspose` | Float | -50..50, integer steps | 0 |  |
| `Resonator{1,2}/KeyToTranspose` | Float | -2..2 | 1 |  |
| `Resonator{1,2}/StartTranspose` | Float | -1..1 | 0 |  |
| `Resonator{1,2}/VelToStartTranspose` | Float | -5..5 | 0 |  |
| `Resonator{1,2}/StartTime` | Float | 0..1 | 0.5 |  |
| `Resonator{1,2}/Decay` | Float | 0..1 | 0.5 |  |
| `Resonator{1,2}/VelToDecay` | Float | -5..5 | 0 |  |
| `Resonator{1,2}/KeyToDecay` | Float | -2..2 | 0 |  |
| `Resonator{1,2}/DecayOnNoteOff` | Float | 0..1 | 0 |  |
| `Resonator{1,2}/Damp` | Float | -1..1 | 0 |  |
| `Resonator{1,2}/VelToDamp` | Float | -5..5 | 0 |  |
| `Resonator{1,2}/KeyToDamp` | Float | -2..2 | 0 |  |
| `Resonator{1,2}/Radius` | Float | 0..1 | 0.5 |  |
| `Resonator{1,2}/VelToRadius` | Float | -5..5 | 0 |  |
| `Resonator{1,2}/KeyToRadius` | Float | -2..2 | 0 |  |
| `Resonator{1,2}/Ratio` | Float | 0..1 | 0 |  |
| `Resonator{1,2}/AmpFreq` | Float | -1..1 | 0 |  |
| `Resonator{1,2}/Bleed` | Float | 0..1 | 0 |  |
| `Resonator{1,2}/Inharmonics` | Float | -1..1 | 0 |  |
| `Resonator{1,2}/VelToInharmonics` | Float | -5..5 | 0 |  |
| `Resonator{1,2}/TubeOpening` | Float | 0..1 | 1 |  |
| `Resonator{1,2}/VelToTubeOpening` | Float | -5..5 | 0 |  |
| `Resonator{1,2}/HitX` | Float | 0..1 | 0.5 |  |
| `Resonator{1,2}/RandomToHitX` | Float | 0..1 | 0 |  |
| `Resonator{1,2}/ListeningXL` | Float | 0..1 | 0.1000000015 |  |
| `Resonator{1,2}/ListeningXR` | Float | 0..1 | 0.8999999762 |  |
| `Resonator{1,2}/Pan` | Float | -1..1 | 0 |  |
| `Resonator{1,2}/KeyToPan` | Float | -1..1 | 0 |  |
| `Resonator{1,2}/Volume` | Float | 0..1 | 0.5 |  |
| `ResonatorOrder` | Enum | 0..1 | 0 |  |
| `Lfo{1,2}/OnOff` | Bool | true/false | false |  |
| `Lfo{1,2}/Type` | Enum | 0..6 | 0 |  |
| `Lfo{1,2}/Retrigger` | Bool | true/false | true |  |
| `Lfo{1,2}/Sync` | Enum | 0..1 | 0 |  |
| `Lfo{1,2}/Rate` | Float | 0..1 | 0.5 |  |
| `Lfo{1,2}/SyncRate` | Float | 0..21, integer steps | 4 |  |
| `Lfo{1,2}/KeyToRate` | Float | -2..2 | 0 |  |
| `Lfo{1,2}/Phase` | Float | 0..360 | 0 |  |
| `Lfo{1,2}/Amount` | Float | 0..1 | 0.5 |  |
| `Lfo{1,2}/VelToAmount` | Float | -5..5 | 0 |  |
| `Lfo{1,2}/Target{1,2}/Target` | Enum | 0..16 | 0 |  |
| `Lfo{1,2}/Target{1,2}/Amount` | Float | -5..5 | 2.5 |  |
| `PitchBendRange` | Float | 0..24, integer steps | 5 |  |
| `PitchBendTarget1/Target` | Enum | 0..17 | 0 |  |
| `PitchBendTarget1/Amount` | Float | -5..5 | 2.5 |  |
| `ModWheelTarget{1,2}/Target` | Enum | 0..17 | 0 |  |
| `ModWheelTarget{1,2}/Amount` | Float | -5..5 | 2.5 |  |
| `ChannelPressureTarget{1,2}/Target` | Enum | 0..17 | 0 |  |
| `ChannelPressureTarget{1,2}/Amount` | Float | -5..5 | 2.5 |  |
| `Polyphony` | Enum | 0..8 | 2 |  |
| `Retrigger` | Bool | true/false | false |  |
| `Volume` | Float | 0..1 | 0.7047892213 |  |
| `PerNotePitchBendRange` | Float | 0..48, integer steps | 0 | 48 |
| `MpeCC74Target{1,2}/Target` | Enum | 0..17 | 0 |  |
| `MpeCC74Target{1,2}/Amount` | Float | -5..5 | 2.5 |  |

#### `LoungeLizard`

| Path below the device element | Class | Stored domain | Default when absent | Defaults preset (where different) |
| --- | --- | --- | --- | --- |
| `Polyphony` | Enum | 0..30 | 30 |  |
| `PitchBendRange` | Float | 0..1 | 1 |  |
| `PerNotePitchBendRange` | Float | 0..48, integer steps | 0 |  |
| `Volume` | Float | 0..1 | 0.7047892213 |  |
| `KeyboardTranspose` | Float | 0..24, integer steps | 12 |  |
| `KeyboardFineTune` | Float | 0..1 | 0.5 |  |
| `KeyboardStretch` | Float | 0..1 | 0.5 |  |
| `MalletStiffness` | Float | 0..1 | 0.5 |  |
| `MalletStiffnessKeyboard` | Float | 0..1 | 0.5 |  |
| `MalletStiffnessVelocity` | Float | 0..1 | 0.5 |  |
| `MalletForceStrength` | Float | 0..1 | 0.5 |  |
| `MalletForceKeyboard` | Float | 0..1 | 0.5 |  |
| `MalletForceVelocity` | Float | 0..1 | 0.5 |  |
| `MalletNoisePitch` | Float | 0..1 | 0.5 |  |
| `MalletNoiseDecay` | Float | 0..1 | 0.5 |  |
| `MalletNoiseAmount` | Float | 0..1 | 0.5 |  |
| `MalletNoiseKeyboardScaling` | Float | 0..1 | 0.5 |  |
| `ForkReleaseTime` | Float | 0..1 | 0.5 |  |
| `ForkTineDecay` | Float | 0..1 | 0.5 |  |
| `ForkTineVolume` | Float | 0..1 | 0.5 |  |
| `ForkTineKeyboardScaling` | Float | 0..1 | 0.5 |  |
| `ForkTineColor` | Float | 0..1 | 0.5 |  |
| `ForkToneBarDecay` | Float | 0..1 | 0.5 |  |
| `ForkToneBarVolume` | Float | 0..1 | 0.5 |  |
| `PickupSymmetry` | Float | 0..1 | 0.5 |  |
| `PickupDistance` | Float | 0..1 | 0.5 |  |
| `PickupModel` | Enum | 0..1 | 0 |  |
| `PickupAmpIn` | Float | 0..1 | 0.5 | 0.4199999869 |
| `PickupAmpOut` | Float | 0..1 | 0.5 | 0.4199999869 |
| `PickupAmpKeyboardScaling` | Float | 0..1 | 0.5 |  |
| `DamperTone` | Float | 0..1 | 0.5 |  |
| `DamperAmount` | Float | 0..1 | 0.5 |  |
| `DamperBalance` | Float | 0..1 | 0.5 |  |

#### `Corpus`

| Path below the device element | Class | Stored domain | Default when absent | Defaults preset (where different) |
| --- | --- | --- | --- | --- |
| `ResonanceType` | Enum | 0..6 | 0 |  |
| `ResonatorQuality` | Enum | 0..3 | 2 |  |
| `Frequency` | Float | 0..1 | 0.5 |  |
| `Transpose` | Float | -48..48, integer steps | 0 |  |
| `FineTranspose` | Float | -50..50, integer steps | 0 |  |
| `Detune` | Float | -1..1 | 0 |  |
| `Decay` | Float | 0..1 | 0.5 |  |
| `FreqDamping` | Float | -1..1 | 0 |  |
| `Radius` | Float | 0..1 | 0.5 |  |
| `AmpFreq` | Float | -1..1 | 0 |  |
| `Inharmonics` | Float | -1..1 | 0 |  |
| `TubeOpening` | Float | 0..1 | 1 |  |
| `Ratio` | Float | 0..1 | 0.5 |  |
| `ExcitationX` | Float | 0..1 | 0.5 |  |
| `ListeningXL` | Float | 0..1 | 0.1000000015 |  |
| `ListeningXR` | Float | 0..1 | 0.8999999762 |  |
| `LfoOnOff` | Bool | true/false | false |  |
| `LfoType` | Enum | 0..6 | 0 |  |
| `LfoSync` | Enum | 0..1 | 0 |  |
| `LfoRate` | Float | 0..1 | 0.5 |  |
| `LfoSyncRate` | Float | 0..21, integer steps | 4 |  |
| `LfoStereoMode` | Enum | 0..1 | 0 |  |
| `LfoSpin` | Float | 0..0.5 | 0 |  |
| `LfoPhase` | Float | 0..360 | 180 |  |
| `LfoOffset` | Float | 0..360 | 0 |  |
| `LfoAmount` | Float | 0..1 | 0 |  |
| `FilterOn` | Bool | true/false | false |  |
| `FilterMidFreq` | Float | 50..18000 | 1000 |  |
| `FilterBandWidth` | Float | 0.5..9 | 4 |  |
| `MidiPitch` | Bool | true/false | false |  |
| `MidiMode` | Enum | 0..1 | 0 |  |
| `PitchBendRange` | Float | 0..24, integer steps | 5 |  |
| `MidiGate` | Bool | true/false | false |  |
| `DecayOnNoteOff` | Float | 0..1 | 0 |  |
| `Drive` | Float | 0..1 | 0.5 |  |
| `StereoWidth` | Float | 0..1 | 1 |  |
| `Bleed` | Float | 0..1 | 0 |  |
| `DryWet` | Float | 0..1 | 0.5 |  |
