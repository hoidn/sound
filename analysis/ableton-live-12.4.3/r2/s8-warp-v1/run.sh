#!/bin/sh
# Regenerate S8 (warp markers and settings) evidence. Read-only on the bundle, Live.arm64 and the C1/C2 corpus.
# Query-server dossiers (results/s8-000N) are retained copies and are not regenerated here.
set -eu
B="/home/ollie/Ableton Live 12 Suite.app/Contents"
H=$(cd "$(dirname "$0")" && pwd)
BIN="$H/../../derived/Live.arm64"
export S8_CACHE="${S8_CACHE:-${TMPDIR:-/tmp}/s8-entry-map.pickle}"
cd "$H"
python3 -I s8_static.py "$B" static-survey.json inputs-documents.tsv audioclip-warp-records.jsonl
# Native lookups (corpus and image); outputs are data.
python3 -I corpus_lookup.py str '^(m|mp)?(SecTime|BeatTime|WarpMarkers?|WarpMode|IsWarped|isWarped|GranularityTones|GranularityTexture|FluctuationTexture|FluxTexture|TransientResolution|TransientLoopMode|TransientEnvelope|ComplexProFormants|ComplexProEnvelope|SavedWarpMarkersForStretched|MarkersGenerated|DefaultDuration|DefaultSampleRate|SamplesToAutoWarp|TempoAfterLastMarker|tempoAfterLastMarker)$|^(Beats|Tones|Texture|Re-Pitch|Complex|REX|Complex Pro|Pro|1 Bar|1/2|1/4|1/8|1/16|1/32|Transients|Off|LoopOs|LoopFwd|LoopAlt|Loop Forward|Loop Back-and-Forth|Transient Loop Mode|Warp Mode|Segment BPM)$|(?i:warp marker|shadow marker|segment length|segmentbpmlimit|kMinSegmentBpm|sample_to_beat_time|beat_to_sample_time|invalid warp mode|empty warp marker)' > strings-lookup.txt
grep -i -E '"name":"[^"]*warp' /var/tmp/sound-analysis/corpus/indexes/aliases.jsonl \
  | python3 -I -c 'import sys,json
for l in sys.stdin:
    r=json.loads(l); n=r["name"]
    if "boost::python" not in n: print(r["entry"], n)' > symbols-warp.txt
python3 -I -B regs.py 0x10260fdd8 0x1027aff6c 0x102882a38 0x102875ec0 > registrations.txt
python3 -I read_words.py "$BIN" 0x10224a6fc 0x10224a704 0x10224a70c 0x10224a718 0x10224a720 0x10225a340 0x10225a348 0x10225a354 \
  0x10225978c 0x102259794 0x1022597a4 0x1022597b0 0x1022597b8 0x1022597c4 0x10224e2b4 0x10224e2bc 0x10224e2dc \
  0x10224e2c8 0x10224e2d0 0x10224e2e8 0x1027b2794 0x1027b29e0 > getter-constants.txt
{
  echo '# AAudioClip vtable 0x10680bea0 slots +0xd0 (post-load) +0x138 (write) +0x140 (load) +0x148 (skip predicate)'
  for s in 0xd0 0x138 0x140 0x148; do python3 -I read_ptrs.py "$BIN" "$(printf '0x%x' $((0x10680bea0 + s)))" 1; done
  echo '# AWarpMarker vtable 0x1067e6f08 slots +0xd0 +0x138 +0x140'
  for s in 0xd0 0x138 0x140; do python3 -I read_ptrs.py "$BIN" "$(printf '0x%x' $((0x1067e6f08 + s)))" 1; done
  echo '# ASampleWarpProperties vtable 0x10681ca80 slots +0xd0 +0x140'
  for s in 0xd0 0x140; do python3 -I read_ptrs.py "$BIN" "$(printf '0x%x' $((0x10681ca80 + s)))" 1; done
  echo '# int32 table 0x105889f90 used by 0x1026a9ec4 (preference index -> stored WarpMode); first 6 entries apply'
  python3 -I read_ptrs.py "$BIN" 0x105889f90 3
  echo '# C strings at 0x105af67ac (TransientLoopMode labels, display/short pairs)'
  python3 -I -c 'import sys; b=open(sys.argv[1],"rb").read(); o=0x5af67ac; print(b[o:o+0x48])' "$BIN"
} > vtable-reads.txt
python3 -I corpus_lookup.py excerpt corpus-excerpts.jsonl \
  0x10147e954 0x101487310 0x101488e64 0x10156da34 0x10156d4c8 0x101467280 0x1014670e8 0x1015743b0 0x1021862f0 \
  0x10260fda4 0x10260fdd8 0x10260ff00 0x102610134 0x1026101a0 0x1026101b4 0x102610264 0x10261026c 0x102610274 \
  0x10261027c 0x102610290 0x102610298 0x1026102c0 0x102610518 0x1026105ec 0x102610910 0x10261093c 0x10261097c \
  0x102610b30 0x102610b6c 0x102610bc4 0x102610fb0 0x102612464 0x1026127e0 0x1026128ac 0x102617370 \
  0x1026a9820 0x1026a9a08 0x1026a9ec4 0x1026a9ef8 0x1026aa13c 0x1026aa354 0x1026aa56c \
  0x1027aff04 0x1027aff6c 0x1027afd40 0x1027b0e40 0x1027b279c 0x1027b29e8 0x1027b3928 0x1027b7cf0 0x1027b91a0 \
  0x1027bf6bc 0x1027c1c7c 0x1027c2458 0x1027c28dc 0x1027c724c 0x1027c79d0 0x1027cd2b0 0x1027cd2b4 0x1027d304c \
  0x102875ec0 0x102882a38 0x1028829d0 0x102883578 0x10288538c 0x10285d098 \
  0x1033bded8 0x1033be004 0x1033bf42c 0x1033bfa68 0x1033bfb94
