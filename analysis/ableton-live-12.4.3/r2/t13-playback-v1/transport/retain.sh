#!/bin/sh
# T1.3 transport: regenerate the retained static evidence (matching table, corpus excerpts, disassembly).
# Read-only on the corpora and slices; output is data. Requires python3, objdump; T13_CACHE (see ../lookup.py).
set -eu
here=$(cd "$(dirname "$0")" && pwd)
cd "$here"
L=/var/tmp/sound-analysis/helpers/Live_x86_64/Live_x86_64.x86_64
A=$here/../../../derived/Live.arm64
E=/var/tmp/sound-analysis/helpers/Ableton_Live_Engine_x86_64/Ableton_Live_Engine_x86_64.x86_64

# 1. Engine name -> Live x86_64 address: order-and-size match, then instruction-by-instruction comparison
cat > matching-eng-x86.txt <<'HDR'
# Engine (named) -> Live x86_64 matches. Line 1 per pair: order-and-size matcher (match_eng_x86.py); NO-MATCH there
# means a neighbour was split differently by Ghidra, not a mismatch. Line 2: instruction comparison (cmp_eng_x86.sh)
# at the listed Live address; 'identical modulo addresses' is the match criterion used.
HDR
while read -r eng size live; do
  python3 -I match_eng_x86.py "$eng" | head -1 >> matching-eng-x86.txt
  sh cmp_eng_x86.sh "$eng" "$size" "$live" >> matching-eng-x86.txt
done <<'LIST'
0x1096b0 31 0x101ad8a10
0x1096d0 43 0x101ad8a30
0x10c2e0 1056 0x101adb640
0x10f370 286 0x101ade6d0
0x10bee0 892 0x101adb240
0x10cff0 1478 0x101adc350
0x10d640 1283 0x101adc9a0
0x10a400 807 0x101ad9760
0x10a760 608 0x101ad9ac0
0x10f540 995 0x101ade8a0
0x110820 90 0x101adfb80
0x10dbc0 336 0x101adcf20
0x10bc50 515 0x101adafb0
0x10cb20 868 0x101adbe80
0x10cee0 260 0x101adc240
0x10f9d0 287 0x101aded30
0x1105a0 25 0x101adf900
0x109850 115 0x101ad8bb0
0x10e650 731 0x101add9b0
0x110c90 22 0x101adfff0
0x8a2aa0 180 0x1021d0020
0x8a30a0 254 0x1021d0620
0xa9350 519 0x101a788e0
0xa92b0 69 0x101a78840
0xa9920 154 0x101a78eb0
0xa9ca0 154 0x101a79230
0xa97c0 166 0x101a78d50
0x9c5a0 368 0x101a6bba0
0x9fdc0 318 0x101a6f3c0
0x9ff20 202 0x101a6f520
0xa0e80 278 0x101a70480
0xa07f0 819 0x101a6fdf0
0xa0ba0 562 0x101a701a0
0x9f690 241 0x101a6ec90
0x9f870 245 0x101a6ee70
0xa1260 27 0x101a70860
0x1185d0 33 0x101ae7930
0x99f30 13 0x101a69530
0x1634f0 6 0x101b32800
LIST

# 2. corpus excerpts (chunk, offset, line SHA-256, record) of every cited function
rm -f excerpts.jsonl
python3 -I ../lookup.py eng excerpt excerpts.jsonl 0x1096b0 0x1096d0 0x109700 0x10c2c0 0x10c2e0 0x10f370 0x1100e0 \
  0x10bee0 0x10cff0 0x10d640 0x10a400 0x10a740 0x10f540 0x109a00 0x110820 0x10dbc0 0x10bc50 0x10cee0 0x10cb20 0x10f9d0 \
  0x10f960 0x1105a0 0x109850 0x10e980 0x10e650 0x109ec0 0x10eca0 0x110600 0x10f070 0xa9350 0xa92b0 0xa9920 0xa9ca0 \
  0xa9be0 0xa9bc0 0x9c5a0 0xa97c0 0x9c590 0xa7420 0x9c4d0 0x9c560 0x9c720 0x9c460 0x9c440 0x9ce40 0x9ce70 0x110c90 \
  0x110880 0x8a2aa0 0x8a2d30 0x8a2e50 0x8cb540 0x8a30a0 0xa7af0 0xa07f0 0xa0ba0 0x9fc90 0x9fdc0 0x9ff20 0xa0e80 0xa0160 \
  0xa0330 0xa1260 0xa01f0 0xa1250 0xa1240 0xa1180 0xa1310 0xa13b0 0xa01d0 0x14d520 0x14edd0 0x14e9a0 0x9f4c0 0x9f690 \
  0x9f870 0xa9ec0 0x1185d0 0x99f30 0xe7570 0x149330 0x109320 0x15a5580
python3 -I ../lookup.py x86 excerpt excerpts.jsonl 0x101ad8a10 0x101ad8a30 0x101adb640 0x101adc350 0x101adc9a0 \
  0x101ade8a0 0x101ad9760 0x101adbe80 0x101aded30 0x101ad8bb0 0x101adfb80 0x101ade6d0 0x101adc240 0x1028a21d0 \
  0x1028a6de0 0x1028a3500 0x1028a2540 0x1027b6140 0x10280fcc0 0x102815430 0x102814eb0 0x102404cc0 0x1011999d0 \
  0x1028a1f80 0x1028a4270 0x102774df0 0x1021d0620 0x1021d0020 0x101add9b0 0x101adf900
python3 -I ../lookup.py arm excerpt excerpts.jsonl 0x101ab05b0 0x101ab05cc 0x101ab2d50 0x101ab3a4c 0x101ab4038 \
  0x101ab4558 0x101ab26cc 0x101ab2954 0x101ab3948 0x101ab086c 0x101ab5cec 0x101ab10ec 0x101ab3594 0x101ab60c8 \
  0x101ab5b70 0x101abb4b0 0x1020f1db4 0x1020f55d4

# 3. disassembly used for operation order and constants
{
  echo '## Live x86_64 PredictedBeatTime 0x101ad8a10 and PredictedLongSampleTime 0x101ad8a30'
  objdump -D -b binary -m i386:x86-64 --adjust-vma=0x100000000 --start-address=0x101ad8a10 --stop-address=0x101ad8a5b "$L" | sed -n '/^ *[0-9a-f]*:/p'
  echo '## Live x86_64 DoSetTempo 0x101adb640: samples per beat and beats per sample'
  objdump -D -b binary -m i386:x86-64 --adjust-vma=0x100000000 --start-address=0x101adb86b --stop-address=0x101adb8b2 "$L" | sed -n '/^ *[0-9a-f]*:/p'
  echo '## Live x86_64 ProcessNextEvents 0x101ade8a0: countdown to the next beat event'
  objdump -D -b binary -m i386:x86-64 --adjust-vma=0x100000000 --start-address=0x101adebf2 --stop-address=0x101adec7a "$L" | sed -n '/^ *[0-9a-f]*:/p'
  echo '## constants (Live x86_64)'
  python3 -I ../peek.py "$L" d 0x105b38988 1
  python3 -I ../peek.py "$L" d 0x105a577f0 1
  python3 -I ../peek.py "$L" f 0x105b35820 1
  echo '## OLoopBraceEvent vtable 0x106c98e80 (slot +0x10 OEvent::CallProcess, +0x18 Process)'
  python3 -I ../peek.py "$L" q 0x106c98e80 5
  echo '## Engine constants'
  python3 -I ../peek.py "$E" d 0x15caf58 1
  python3 -I ../peek.py "$E" f 0x15bf2c8 1
  python3 -I ../peek.py "$E" f 0x15bab88 1
  python3 -I ../peek.py "$E" f 0x15bad68 1
  python3 -I ../peek.py "$E" f 0x15cd8e8 1
  python3 -I ../peek.py "$E" d 0x15cb5c8 1
  python3 -I ../peek.py "$E" f 0x15bab9c 1
  python3 -I ../peek.py "$E" d 0x15bac48 1
} > disasm-x86.txt
{
  echo '## arm64 PredictedBeatTime 0x101ab05b0, PredictedLongSampleTime 0x101ab05cc (fmadd, fcvtps)'
  python3 -I a64.py "$A" 0x101ab05b0 14
  echo '## arm64 DoSetTempo 0x101ab2d50: FP instructions'
  python3 -I a64.py "$A" 0x101ab2d50 261 | grep -E 'fdiv|fmul|fmadd|fcvt|scvtf|frint'
  echo '## arm64 ProcessNextEvents 0x101ab5cec: FP instructions'
  python3 -I a64.py "$A" 0x101ab5cec 207 | grep -E 'fmadd|fcvtps|frint|fmul|fsub|fadd|scvtf|bl '
} > disasm-arm64.txt
echo done
