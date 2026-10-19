#!/bin/sh
# Disassemble raw bytes [START, STOP) of an x86_64 slice at image VAs (output is data).
# usage: sh dis.sh {live|eng} START STOP
# live: Live x86_64 slice, __TEXT file offset = VA - 0x100000000; eng: Live Engine x86_64 slice, file offset = VA.
case "$1" in
  live) S=/var/tmp/sound-analysis/helpers/Live_x86_64/Live_x86_64.x86_64; V=0x100000000;;
  eng) S=/var/tmp/sound-analysis/helpers/Ableton_Live_Engine_x86_64/Ableton_Live_Engine_x86_64.x86_64; V=0;;
esac
objdump -D -b binary -m i386:x86-64 --adjust-vma=$V --no-show-raw-insn \
  --start-address="$2" --stop-address="$3" "$S" | sed -n '/^ *[0-9a-f]*:/p'
