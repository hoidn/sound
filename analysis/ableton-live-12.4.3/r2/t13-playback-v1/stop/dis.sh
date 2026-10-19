#!/bin/sh
# Disassemble [START, STOP) of a slice at its image VAs (output is data).
# usage: sh dis.sh eng|x86 START STOP   (eng: Engine x86_64 slice, base 0; x86: Live x86_64 slice, base 0x100000000;
#        in both, __TEXT file offset = VA - base)
case "$1" in
  eng) S=/var/tmp/sound-analysis/helpers/Ableton_Live_Engine_x86_64/Ableton_Live_Engine_x86_64.x86_64; B=0 ;;
  x86) S=/var/tmp/sound-analysis/helpers/Live_x86_64/Live_x86_64.x86_64; B=0x100000000 ;;
esac
objdump -D -b binary -m i386:x86-64 --adjust-vma=$B --no-show-raw-insn \
  --start-address="$2" --stop-address="$3" "$S" | sed -n '/^ *[0-9a-f]*:/p'
