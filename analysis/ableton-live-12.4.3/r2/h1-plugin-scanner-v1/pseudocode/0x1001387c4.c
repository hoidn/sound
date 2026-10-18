
void FUN_1001387c4(undefined8 *param_1,undefined8 param_2,undefined8 param_3)

{
  long *plVar1;
  long *plVar2;
  int iVar3;
  undefined8 uVar4;
  undefined1 auStack_240 [8];
  long *local_238;
  void *local_230;
  undefined8 uStack_228;
  long local_220;
  undefined4 local_218;
  uint uStack_214;
  char local_201;
  undefined8 local_50;
  undefined8 local_48;
  undefined8 uStack_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_100b1c378;
  local_230 = (void *)0x0;
  uStack_228 = 0;
  local_220 = 0;
  FUN_100144a3c(&local_238,param_3,&local_230);
  plVar2 = local_238;
  if (local_238 == (long *)0x0) {
    local_201 = '\x04';
    local_218 = 0x72726563;
    uStack_214 = uStack_214 & 0xffffff00;
    uVar4 = std::chrono::system_clock::now();
    FUN_1006a284c(auStack_240,4,&local_218,uVar4);
    if (local_201 < '\0') {
      operator_delete((void *)CONCAT44(uStack_214,local_218));
    }
    iVar3 = FUN_10069f1d8(auStack_240);
    if (iVar3 != 0) {
      uVar4 = FUN_10069c398(auStack_240,"Failed to load plugin: ");
      FUN_10069d278(uVar4,&local_230);
    }
    thunk_FUN_10069bf04(auStack_240);
    plVar1 = local_238;
  }
  else {
    FUN_1001441a4(&local_218,local_238 + 2);
    FUN_1001442c4(&local_50,local_238 + 2);
    _memcpy(param_1,&local_218,0x1c4);
    param_1[0x39] = local_50;
    param_1[0x3b] = uStack_40;
    param_1[0x3a] = local_48;
    *(undefined1 *)(param_1 + 0x3c) = 1;
    plVar1 = local_238;
  }
  local_238 = (long *)0x0;
  if (plVar1 != (long *)0x0) {
    local_238 = (long *)0x0;
    (**(code **)(*plVar1 + 8))();
  }
  if (plVar2 == (long *)0x0) {
    param_1[0x3c] = 0;
    param_1[0x39] = 0;
    param_1[0x38] = 0;
    param_1[0x3b] = 0;
    param_1[0x3a] = 0;
    param_1[0x35] = 0;
    param_1[0x34] = 0;
    param_1[0x37] = 0;
    param_1[0x36] = 0;
    param_1[0x31] = 0;
    param_1[0x30] = 0;
    param_1[0x33] = 0;
    param_1[0x32] = 0;
    param_1[0x2d] = 0;
    param_1[0x2c] = 0;
    param_1[0x2f] = 0;
    param_1[0x2e] = 0;
    param_1[0x29] = 0;
    param_1[0x28] = 0;
    param_1[0x2b] = 0;
    param_1[0x2a] = 0;
    param_1[0x25] = 0;
    param_1[0x24] = 0;
    param_1[0x27] = 0;
    param_1[0x26] = 0;
    param_1[0x21] = 0;
    param_1[0x20] = 0;
    param_1[0x23] = 0;
    param_1[0x22] = 0;
    param_1[0x1d] = 0;
    param_1[0x1c] = 0;
    param_1[0x1f] = 0;
    param_1[0x1e] = 0;
    param_1[0x19] = 0;
    param_1[0x18] = 0;
    param_1[0x1b] = 0;
    param_1[0x1a] = 0;
    param_1[0x15] = 0;
    param_1[0x14] = 0;
    param_1[0x17] = 0;
    param_1[0x16] = 0;
    param_1[0x11] = 0;
    param_1[0x10] = 0;
    param_1[0x13] = 0;
    param_1[0x12] = 0;
    param_1[0xd] = 0;
    param_1[0xc] = 0;
    param_1[0xf] = 0;
    param_1[0xe] = 0;
    param_1[9] = 0;
    param_1[8] = 0;
    param_1[0xb] = 0;
    param_1[10] = 0;
    param_1[5] = 0;
    param_1[4] = 0;
    param_1[7] = 0;
    param_1[6] = 0;
    param_1[1] = 0;
    *param_1 = 0;
    param_1[3] = 0;
    param_1[2] = 0;
  }
  if (local_220 < 0) {
    operator_delete(local_230);
    if (*(long *)PTR____stack_chk_guard_100b1c378 != local_38) goto LAB_100138990;
  }
  else if (*(long *)PTR____stack_chk_guard_100b1c378 != local_38) {
LAB_100138990:
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}

