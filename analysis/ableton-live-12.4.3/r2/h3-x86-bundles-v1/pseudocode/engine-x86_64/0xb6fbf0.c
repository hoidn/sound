// 0xb6fbf0 FUN_00b6fbf0 | undefined FUN_00b6fbf0() | state=exported-with-warnings | chunk-00521.jsonl

undefined1 FUN_00b6fbf0(undefined8 *param_1,undefined8 param_2)

{
  char cVar1;
  short sVar2;
  undefined8 uVar3;
  undefined1 uVar4;
  undefined1 local_c8 [80];
  undefined1 local_78 [80];
  long local_28;
  
  local_28 = *(long *)PTR____stack_chk_guard_01727258;
  sVar2 = _FSFindFolder(0xffff8003,0x61737570,0,local_78);
  if (((((sVar2 == 0) &&
        (cVar1 = FUN_00b6fd50(local_78,local_78,"Propellerhead Software"), cVar1 != '\0')) &&
       (cVar1 = FUN_00b6fd50(local_78,local_78,"ReWire"), cVar1 != '\0')) &&
      (cVar1 = FUN_00b6fd50(local_c8,local_78,param_2), cVar1 != '\0')) ||
     (((sVar2 = _FSFindFolder(0xffff8004,0x61737570,0,local_78), sVar2 == 0 &&
       (cVar1 = FUN_00b6fd50(local_78,local_78,"Propellerhead Software"), cVar1 != '\0')) &&
      ((cVar1 = FUN_00b6fd50(local_78,local_78,"ReWire"), cVar1 != '\0' &&
       (cVar1 = FUN_00b6fd50(local_c8,local_78,param_2), cVar1 != '\0')))))) {
    uVar3 = _CFURLCreateFromFSRef(*(undefined8 *)PTR__kCFAllocatorDefault_01727060,local_c8);
    *param_1 = uVar3;
    uVar4 = 1;
    if (*(long *)PTR____stack_chk_guard_01727258 != local_28) goto LAB_00b6fd3e;
  }
  else {
    uVar4 = 0;
    if (*(long *)PTR____stack_chk_guard_01727258 != local_28) {
LAB_00b6fd3e:
                    /* WARNING: Subroutine does not return */
      ___stack_chk_fail();
    }
  }
  return uVar4;
}

