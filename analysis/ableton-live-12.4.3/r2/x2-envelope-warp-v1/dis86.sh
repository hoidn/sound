#!/bin/sh
# Disassemble x86_64 slice bytes [start, stop) at their image VAs (output is data).
# usage: sh dis86.sh START STOP     (the slice's __TEXT file offset equals VA - 0x100000000)
S=${XEXEC_SLICE:-/var/tmp/sound-analysis/helpers/Live_x86_64/Live_x86_64.x86_64}
objdump -D -b binary -m i386:x86-64 --adjust-vma=0x100000000 --no-show-raw-insn \
  --start-address="$1" --stop-address="$2" "$S" | sed -n '/^ *[0-9a-f]*:/p'
