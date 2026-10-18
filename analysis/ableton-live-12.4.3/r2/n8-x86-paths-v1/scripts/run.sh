#!/bin/sh
# Regenerates binary-reads.txt and objdump.txt in the packet directory (read-only inputs; nothing executed).
set -eu
S=$(dirname "$0"); P=$S/..
L=/var/tmp/sound-analysis/helpers/Live_x86_64/Live_x86_64.x86_64
A=/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/derived/Live.arm64
E=/var/tmp/sound-analysis/helpers/Ableton_Live_Engine_x86_64/Ableton_Live_Engine_x86_64.x86_64
py() { python3 -I "$@"; }
{
echo '## sha256'; sha256sum "$L" "$A" "$E"
echo '## x86 segments'; py $S/segs.py "$L" 0x108f40977 0x108f2f2b4 0x106cea3a0
echo '## x86 LReWireHost vtable (typeinfo 0x106ceb210) and AReWireHost vtable'
py $S/words.py "$L" 0x100000000 0x106cea200 3; py $S/words.py "$L" 0x100000000 0x106cea378 10; py $S/words.py "$L" 0x100000000 0x106cea3d8 3; py $S/words.py "$L" 0x100000000 0x106cea570 2
echo '## x86 typeinfo chain LReWireHost -> AReWireHost -> ACompound'
py $S/words.py "$L" 0x100000000 0x106ceb210 3; py $S/words.py "$L" 0x100000000 0x106ceb1f8 3; py $S/words.py "$L" 0x100000000 0x106bb7c30 3
echo '## arm64 LReWireHost vtable (typeinfo 0x1067a5f38) slots 0x180-0x1a8, AReWireHost slot 0x188/0x190'
py $S/words.py "$A" 0x100000000 0x1067a55b8 3; py $S/words.py "$A" 0x100000000 0x1067a5748 6; py $S/words.py "$A" 0x100000000 0x1067a5928 2
echo '## stored pointers'
py $S/findptr.py "$L" 0x100000000 0x1024b5060 0x1024b0300 0x1024b0650 0x1024b0d30 0x1024b4840 0x1024b5e50 0x101ab6780 0x101ab68f0 0x1031d7e10 0x1031d6b30 0x106dff788
py $S/findptr.py "$A" 0x100000000 0x10587ca09 0x10587c9fb 0x1067a5f38 0x1067a5f20
echo '## Engine/Live ReWire predicate region byte comparison (Engine 0xe73f0 vs Live 0x101ab6780, 0x180 bytes)'
py $S/bytecmp.py "$E" 0x0 0xe73f0 "$L" 0x100000000 0x101ab6780 0x180
echo '## debug-option keys (32 bytes): x86 MultiF0, arm64 MultiF0, x86 ReWire install, x86 ReWire host, x86 interactive gate'
py $S/consts.py "$L" 0x100000000 hex:0x105e2c7b8; py $S/consts.py "$A" 0x100000000 hex:0x1058c29f8
py $S/consts.py "$L" 0x100000000 hex:0x105de826c hex:0x105de828c hex:0x105d5fe44
echo '## MultiF0 interface vtables (dynamic 0x106e026a8, builtin 0x106e02758) and RTTI'
py $S/words.py "$L" 0x100000000 0x106e026a8 16; py $S/words.py "$L" 0x100000000 0x106e02740 2
py $S/words.py "$L" 0x100000000 0x106e02758 16; py $S/words.py "$L" 0x100000000 0x106e027d8 2
echo '## builtin MultiF0 default floats (12 at 0x105fa8480)'
py $S/consts.py "$L" 0x100000000 f32:0x105fa8480:12
echo '## TMultiF0Analysis vtable 0x106e01c60, TMultiF0Task vtable 0x106e01dc0 and RTTI'
py $S/words.py "$L" 0x100000000 0x106e01c60 16; py $S/words.py "$L" 0x100000000 0x106e01e58 2
py $S/words.py "$L" 0x100000000 0x106e01dc0 11; py $S/words.py "$L" 0x100000000 0x106e01ea8 3
echo '## TAudioToMidiTask subclasses (typeinfos whose base is 0x106dff788)'
py $S/words.py "$L" 0x100000000 0x106e014f0 3; py $S/words.py "$L" 0x100000000 0x106e01ea8 3; py $S/words.py "$L" 0x100000000 0x106e01990 3
echo '## TDtmAnalysis secondary vtable (typeinfo 0x106e01658) holding 0x1031ac1a0'
py $S/words.py "$L" 0x100000000 0x106e015d0 12; py $S/words.py "$L" 0x100000000 0x106e01658 2
echo '## task log labels 0x106e00090'
py $S/words.py "$L" 0x100000000 0x106e00090 3
echo '## note conversion constants'
py $S/consts.py "$L" 0x100000000 f64:0x105e04d90 f64:0x105c22740 f64:0x105e1d228 f64:0x105bcba70 f64:0x105a57808 f64:0x105a577f0 f64:0x105b500f0 f32:0x105b8419c f64:0x105ddb7a8
echo '## OSendThreadMessage vtable (x86) 0x106c98f08 and RTTI'
py $S/words.py "$L" 0x100000000 0x106c98f08 5; py $S/words.py "$L" 0x100000000 0x106c99090 2
} > $P/binary-reads.txt
{
echo '## Live x86 0x101ab6780 / 0x101ab68f0'; $S/dis.sh "$L" 0x100000000 0x101ab6780 0x101ab6788; $S/dis.sh "$L" 0x100000000 0x101ab68f0 0x101ab68f8
echo '## Engine SIsReWireDeviceEnabled, SIsReWireHostEnabled, _RWDEFOpenDevice head'
$S/dis.sh "$E" 0x0 0xe73f0 0xe73f8; $S/dis.sh "$E" 0x0 0xe7560 0xe7568; $S/dis.sh "$E" 0x0 0x3ae20 0x3ae50
echo '## arm64 LReWireHost slot 0x190..0x1a8 bytes'; xxd -s 0x239f0c4 -l 32 "$A"
echo '## Live x86 0x1024b5060 head (install and host-open gates)'; $S/dis.sh "$L" 0x100000000 0x1024b5060 0x1024b50d6
echo '## Live x86 0x1024b0dc9..0x1024b0f7c (alias installer paths)'; $S/dis.sh "$L" 0x100000000 0x1024b0dc9 0x1024b0f7c
echo '## Live x86 song-agent call into host slot 0x190'; $S/dis.sh "$L" 0x100000000 0x1027c8437 0x1027c85ce
echo '## Live x86 task factory branch'; $S/dis.sh "$L" 0x100000000 0x1031714ae 0x103171506
echo '## Live x86 Convert menu callbacks (algorithm type in esi)'
for a in 0x103950040 0x103950060 0x103950070 0x103dc88b0 0x103dc88f0 0x103dc8900 0x103fecf80 0x103fecfa0 0x103fecfb0; do $S/dis.sh "$L" 0x100000000 $a $(printf '0x%x' $((a+0xf))); done
echo '## Live x86 MultiF0 record to note (0x1031d7578..0x1031d7646)'; $S/dis.sh "$L" 0x100000000 0x1031d7578 0x1031d7646
echo '## Live x86 Stop body 0x1028a0460'; $S/dis.sh "$L" 0x100000000 0x1028a0460 0x1028a05e4
echo '## Live x86 SetPlaying(false) compares'; $S/dis.sh "$L" 0x100000000 0x101a6f3c0 0x101a6f520 | grep -E 'cmp'
} > $P/objdump.txt
