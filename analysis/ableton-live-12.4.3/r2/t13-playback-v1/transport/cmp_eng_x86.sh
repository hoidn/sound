#!/bin/sh
# Compare an Engine function with its Live x86_64 counterpart instruction by instruction (analyst tool; output is data).
# usage: sh cmp_eng_x86.sh ENG_START SIZE LIVE_START
# Addresses in the text (branch targets, rip-relative data) are normalized away; a remaining difference is printed.
E=/var/tmp/sound-analysis/helpers/Ableton_Live_Engine_x86_64/Ableton_Live_Engine_x86_64.x86_64
L=/var/tmp/sound-analysis/helpers/Live_x86_64/Live_x86_64.x86_64
es=$(($1)); n=$(($2)); ls=$(($3))
norm() { sed -n 's/^ *[0-9a-f]*:\t//p' | sed -E 's/0x[0-9a-f]+/A/g; s/ +# .*//; s/[0-9a-f]+ <[^>]*>/A/g' ; }
objdump -D -b binary -m i386:x86-64 --no-show-raw-insn --start-address=$es --stop-address=$((es+n)) "$E" | norm > /tmp/cmp_e.$$
objdump -D -b binary -m i386:x86-64 --no-show-raw-insn --adjust-vma=0x100000000 --start-address=$ls --stop-address=$((ls+n)) "$L" | norm > /tmp/cmp_l.$$
if cmp -s /tmp/cmp_e.$$ /tmp/cmp_l.$$; then echo "$1 $3 size $2: identical modulo addresses ($(wc -l < /tmp/cmp_e.$$) instructions)"; else echo "$1 $3 size $2: DIFFER"; diff /tmp/cmp_e.$$ /tmp/cmp_l.$$ | head -20; fi
rm -f /tmp/cmp_e.$$ /tmp/cmp_l.$$
