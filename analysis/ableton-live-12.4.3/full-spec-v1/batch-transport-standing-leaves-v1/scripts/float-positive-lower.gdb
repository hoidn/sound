set pagination off
set confirm off
break xcall
run
delete 1
break *0x105a4d446
commands
silent
printf "HIT 0x105a4d446 %lx\n", (unsigned long)($rsi)
return
continue
end
break *0x105a4d44c
commands
silent
printf "HIT 0x105a4d44c %lx\n", (unsigned long)($xmm0.v2_int64[0])
return
continue
end
break *0x105a4d452
commands
silent
printf "HIT 0x105a4d452 %lx\n", (unsigned long)($xmm0.v4_int32[0])
return
continue
end
break *0x105a4d458
commands
silent
printf "HIT 0x105a4d458 %lx\n", (unsigned long)($rsi)
return
continue
end
continue
