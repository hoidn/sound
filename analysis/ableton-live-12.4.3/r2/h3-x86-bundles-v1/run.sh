#!/bin/sh
# Packet H3 reproduction (2026-10-17). Read-only against the Ableton bundle; never executes it.
# Full macho_inspect outputs for the Engine (21 MB) and Live (62 MB) were kept only in
# $S and are summarized by compact_overlap.py; their SHA-256 values are in manifest.json.
set -eu
A="/home/ollie/Ableton Live 12 Suite.app/Contents"
D=/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/r2/h3-x86-bundles-v1
S=/var/tmp/sound-analysis/scratch/h3
H=/var/tmp/sound-analysis/helpers
mkdir -p "$S"/str-engine "$S"/str-rewire "$S"/str-multif0 "$S"/str-makealias
py() { python3 -I "$@"; }
py $D/macho_inspect.py "$A/Resources/Ableton Live Engine.bundle/Contents/MacOS/Ableton Live Engine" $S/engine.macho.json $S/str-engine
py $D/macho_inspect.py "$A/Resources/ReWire-Mach-O/ReWire.bundle/Contents/MacOS/ReWire" $S/rewire.macho.json $S/str-rewire
py $D/macho_inspect.py "$A/App-Resources/Misc/MultiF0/Mac/libmultif0_64.dylib" $S/multif0.macho.json $S/str-multif0
py $D/macho_inspect.py "$A/Resources/MakeAlias" $S/makealias.macho.json $S/str-makealias
py $D/macho_inspect.py "$A/MacOS/Live" $S/live.macho.json
py $D/compact_overlap.py $S/engine.macho.json $S/live.macho.json $D/macho
for n in engine rewire multif0 makealias; do for f in "$S"/str-$n/*.tsv; do cp "$f" "$D/strings/$n.$(basename "$f")"; done; done
cp $S/rewire.macho.json $S/multif0.macho.json $S/makealias.macho.json $D/macho/
L="$A/MacOS/Live"
py $D/needle_scan.py "$L" $D/needles/live-bundle-names.json "Ableton Live Engine" "live-engine" "ReWire-Mach-O" "ReWire.bundle" "ReWire" "multif0" "MultiF0" "RWPRegisterReWireDevice" "RWMOpen" "RWDEF" "proc_translated" "Rosetta" "OSharedMemory" "omessage-factory"
py $D/needle_scan.py "$L" $D/needles/live-install-and-mf0.json "mf0p_" "Audio2Midi" "MultiF0" "InstallPropellerheadDlls" "Running as ReWire" "Propellerhead Software" "Ableton Live Engine" "RWP" "ReWire: "
py $D/needle_scan.py "$L" $D/needles/live-engine-classes.json "OEngine.Decouple" "OEngine.SetSessionOverdub" "7OEngine" "OFireManager" "OSharedMemory::SInit" "OceanEngineInitO" "TransportEngineStateChanged" "products/live/Live/OceanEngine"
py $D/needle_scan.py "$L" $D/needles/live-oengine-symbols.json "OEngine10SetPlaying" "OEngine11SetBeatTime" "OEngine8BeatTime" "RWDEF"
py $D/needle_scan.py "$L" $D/needles/live-convert-to-midi.json "Convert Harmony" "Convert Melody" "Convert Drums" "ConvertHarmony" "ConvertMelody" "ConvertDrums" "Audio2Midi" "AudioToMidi"
py $D/needle_scan.py "$L" $D/needles/live-rewire-sdk-loader.json "ReWire Debugging.bundle" "ReWire Testing.bundle" "ReWire.bundle" "Propellerhead Software"
py $D/needle_scan.py "$A/Resources/ReWire-Mach-O/ReWire.bundle/Contents/MacOS/ReWire" $D/needles/rewire-library.json "ReWire" "Propellerhead" "Application Support" "Library" "rewire" "Smuggler" "bootstrap" "TopHat"
py $D/corpus_extract.py $H/Ableton_Live_Engine_x86_64/corpus/decomp/chunks $D/pseudocode/engine-x86_64 0x3ab70 0x3ac20 0x3ace0 0x3ae20 0x3b0c0 0x3b110 0x3b120 0x3b320 0x3b370 0x3b380 0x3b3d0 0x3b3e0 0xe71a0 0xf7770 0x112150 0xbb8920 0x750e0 0xb6fa70 0xb6fb50 0xb6fbf0 0x15f3f0 0x15f620
py $D/corpus_extract.py $H/libmultif0_64_dylib_x86_64/corpus/decomp/chunks $D/pseudocode/multif0 0x193ca0 0x193cb0 0x193cc0 0x193cd0 0x193ce0 0x193cf0 0x193d40 0x193dc0 0x193de0 0x193e70 0x194050 0x1956d0
# Dossiers: the one-shot analyzeHeadless form in wiki/research/r2-query-route.md with
#   Ableton_Live_Engine_x86_64 -> $D/dossier/engine-x86_64     @$D/dossier/engine-x86_64.queries.txt
#   Ableton_Live_Engine (arm64) -> $D/dossier/engine-arm64-stub @$D/dossier/engine-arm64-stub.queries.txt
