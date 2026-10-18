#!/bin/sh
# usage: dis.sh <slice-file> <image-base> <start-va> <end-va>
# Linear x86_64 disassembly of a raw Mach-O slice region (VA = file offset + image base).
exec objdump -D -b binary -m i386:x86-64 --adjust-vma="$2" --start-address="$3" --stop-address="$4" "$1" | tail -n +8
