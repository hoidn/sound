// 0x1006e71c8 FUN_1006e71c8 state=exported-with-warnings body_bytes=812 warnings=2 chunk=chunk-00283.jsonl

/* WARNING: Removing unreachable block (ram,0x0001006e732c) */
/* WARNING: Type propagation algorithm not settling */

undefined8 FUN_1006e71c8(undefined8 param_1)

{
  long *******ppppppplVar1;
  uint uVar2;
  uint uVar3;
  int iVar4;
  ulong uVar5;
  undefined8 uVar6;
  long *******ppppppplVar7;
  void *local_90 [2];
  char local_79;
  long *******local_78;
  long *******ppppppplStack_70;
  byte bStack_61;
  long *******local_60;
  long *******ppppppplStack_58;
  undefined8 local_50;
  
  if (((DAT_100e75188 & 1) == 0) && (iVar4 = ___cxa_guard_acquire(&DAT_100e75188), iVar4 != 0)) {
    FUN_1001c2c04(&DAT_100e75268,"c55d131f-2661-5add-aece-29afb7099dfa([-_][a-zA-Z0-9-_]+)?.xmp",0);
    ___cxa_atexit(FUN_1001c0768,&DAT_100e75268,0x100000000);
    ___cxa_guard_release(&DAT_100e75188);
  }
  if (((DAT_100e75190 & 1) == 0) && (iVar4 = ___cxa_guard_acquire(&DAT_100e75190), iVar4 != 0)) {
    FUN_1001c2c04(&DAT_100e752a8,"b20da5c2-8ad7-5c68-866e-e0618da1d528([-_][a-zA-Z0-9-_]+)?.xmp",0);
    ___cxa_atexit(FUN_1001c0768,&DAT_100e752a8,0x100000000);
    ___cxa_guard_release(&DAT_100e75190);
  }
  FUN_1001e5250(&local_78);
  (*(code *)(*ppppppplStack_70)[0x25])(&local_60);
  if ((local_78 != (long *******)0x0) &&
     (iVar4 = *(int *)(local_78 + 1), *(int *)(local_78 + 1) = iVar4 + -1, iVar4 + -1 == 0)) {
    FUN_1002abea8();
  }
  ppppppplVar1 = ppppppplStack_58;
  ppppppplVar7 = local_60;
  if (local_60 == ppppppplStack_58) {
    uVar3 = 1;
  }
  else {
    do {
      while( true ) {
        FUN_10014bdb8(local_90,ppppppplVar7,&DAT_100e2ade8);
        FUN_10014bdb8(&local_78,local_90,&DAT_100e2add0);
        uVar3 = FUN_100713770(param_1,&local_78);
        if ((char)bStack_61 < '\0') break;
        if (-1 < local_79) goto LAB_1006e726c;
LAB_1006e72bc:
        operator_delete(local_90[0]);
        uVar2 = uVar3;
        if (ppppppplVar7 + 3 == ppppppplVar1) {
          uVar2 = 1;
        }
        ppppppplVar7 = ppppppplVar7 + 3;
        if ((uVar2 & 1) != 0) goto LAB_1006e72d4;
      }
      operator_delete(local_78);
      if (local_79 < '\0') goto LAB_1006e72bc;
LAB_1006e726c:
      uVar2 = uVar3;
      if (ppppppplVar7 + 3 == ppppppplVar1) {
        uVar2 = 1;
      }
      ppppppplVar7 = ppppppplVar7 + 3;
    } while ((uVar2 & 1) == 0);
LAB_1006e72d4:
    uVar3 = uVar3 ^ 1;
  }
  if (local_60 != (long *******)0x0) {
    if (ppppppplStack_58 == local_60) {
      ppppppplStack_58 = local_60;
      operator_delete(local_60);
    }
    else {
      do {
        ppppppplStack_58 = ppppppplStack_58 + -3;
      } while (ppppppplStack_58 != local_60);
      ppppppplStack_58 = local_60;
      operator_delete(local_60);
    }
  }
  if (uVar3 == 0) {
    return 1;
  }
  FUN_1007164bc(&local_78,param_1);
  if ((char)bStack_61 < '\0') {
    FUN_100147c88(&local_60,local_78,ppppppplStack_70);
    if ((char)bStack_61 < '\0') {
      operator_delete(local_78);
    }
  }
  else {
    ppppppplStack_58 = ppppppplStack_70;
    local_60 = local_78;
    local_50 = (ulong)bStack_61 << 0x38;
  }
  ppppppplVar1 = ppppppplStack_58;
  ppppppplVar7 = local_60;
  if (-1 < (long)local_50) {
    ppppppplVar1 = (long *******)(local_50 >> 0x38);
    ppppppplVar7 = (long *******)&local_60;
  }
  uVar5 = FUN_1004161f0(ppppppplVar7,(long)ppppppplVar7 + (long)ppppppplVar1,&DAT_100e75268,0);
  if ((uVar5 & 1) == 0) {
    ppppppplVar1 = ppppppplStack_58;
    ppppppplVar7 = local_60;
    if (-1 < (long)local_50) {
      ppppppplVar1 = (long *******)(ulong)local_50._7_1_;
      ppppppplVar7 = (long *******)&local_60;
    }
    uVar6 = FUN_1004161f0(ppppppplVar7,(long)ppppppplVar7 + (long)ppppppplVar1,&DAT_100e752a8,0);
  }
  else {
    uVar6 = 1;
  }
  if ((char)local_50._7_1_ < '\0') {
    operator_delete(local_60);
    return uVar6;
  }
  return uVar6;
}

