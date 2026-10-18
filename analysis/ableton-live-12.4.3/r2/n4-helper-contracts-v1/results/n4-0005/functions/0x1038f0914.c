
/* WARNING: Removing unreachable block (ram,0x0001038f09cc) */
/* WARNING: Removing unreachable block (ram,0x0001038f09e0) */
/* WARNING: Removing unreachable block (ram,0x0001038f0a74) */
/* WARNING: Removing unreachable block (ram,0x0001038f09fc) */
/* WARNING: Removing unreachable block (ram,0x0001038f0aac) */
/* WARNING: Removing unreachable block (ram,0x0001038f0ac0) */
/* WARNING: Removing unreachable block (ram,0x0001038f0b88) */

void FUN_1038f0914(long param_1)

{
  long *plVar1;
  int iVar2;
  ulong uVar3;
  undefined8 uVar4;
  long *local_a8;
  undefined8 ***local_a0;
  long lStack_98;
  undefined8 local_90;
  undefined8 ***local_80;
  long lStack_78;
  undefined8 local_70;
  void *local_68 [2];
  char local_51;
  undefined8 ***local_50;
  long lStack_48;
  undefined7 local_40;
  byte bStack_39;
  
  uVar3 = FUN_103e9728c(param_1 + 0x18);
  if ((uVar3 & 1) == 0) {
    FUN_103f63014(&local_50,param_1 + 0x18);
    lStack_98 = lStack_48;
    local_a0 = local_50;
    local_90 = (ulong)bStack_39 << 0x38;
    if ((char)bStack_39 < '\0') {
      FUN_10023448c(&local_80,local_50,lStack_48);
    }
    else {
      lStack_78 = lStack_48;
      local_80 = local_50;
      local_70 = local_90;
    }
    local_50 = local_80;
    if (-1 < (long)local_70._7_1_) {
      local_50 = &local_80;
    }
    lStack_48 = lStack_78;
    if (-1 < local_70) {
      lStack_48 = (long)local_70._7_1_;
    }
    FUN_103f94148(local_68,"{}  not found",0xd,0xd,&local_50);
    if (local_70._7_1_ < '\0') {
      operator_delete(local_80);
      if (local_90._7_1_ < '\0') goto LAB_1038f0c58;
    }
    else if (local_90 < 0) {
LAB_1038f0c58:
      operator_delete(local_a0);
    }
    uVar4 = std::chrono::system_clock::now();
    FUN_103f3ffec(&local_50,3,uVar4);
    iVar2 = FUN_103f3c8b8(&local_50);
    if (iVar2 != 0) {
      FUN_103f3a958(&local_50,local_68);
    }
    goto LAB_1038f0c1c;
  }
  uVar4 = *(undefined8 *)(param_1 + 0x60);
  FUN_1002725dc(&local_50,param_1 + 0x48,0);
  local_a8 = operator_new(0x58);
  *local_a8 = (long)&PTR_thunk_FUN_10027a25c_1065928b0;
  local_a8[1] = (long)(local_a8 + 2);
  *(undefined8 *)((long)local_a8 + 0x14) = DAT_1055d3960;
  *(undefined4 *)((long)local_a8 + 0x1c) = 0xffffffff;
  local_a8[5] = lStack_48;
  local_a8[4] = (long)local_50;
  local_a8[6] = CONCAT17(bStack_39,local_40);
  *(undefined4 *)(local_a8 + 7) = 0;
  local_a8[9] = 0;
  local_a8[10] = 0;
  local_a8[8] = 0;
  uVar3 = FUN_1025da348(uVar4,param_1 + 0x18,param_1 + 0x30,&local_a8,
                        *(undefined4 *)(param_1 + 0x70),0);
  plVar1 = local_a8;
  local_a8 = (long *)0x0;
  if (plVar1 != (long *)0x0) {
    (**(code **)(*plVar1 + 8))();
  }
  if (uVar3 >> 0x20 == 0) {
    return;
  }
  FUN_103f63014(&local_50,param_1 + 0x18);
  lStack_98 = lStack_48;
  local_a0 = local_50;
  local_90 = (ulong)bStack_39 << 0x38;
  if ((char)bStack_39 < '\0') {
    FUN_10023448c(&local_80,local_50,lStack_48);
  }
  else {
    lStack_78 = lStack_48;
    local_80 = local_50;
    local_70 = local_90;
  }
  local_50 = local_80;
  if (-1 < (long)local_70._7_1_) {
    local_50 = &local_80;
  }
  lStack_48 = lStack_78;
  if (-1 < local_70) {
    lStack_48 = (long)local_70._7_1_;
  }
  FUN_103f94148(local_68,"Failed to start {}",0x12,0xd,&local_50);
  if (local_70._7_1_ < '\0') {
    operator_delete(local_80);
    if (local_90._7_1_ < '\0') goto LAB_1038f0b7c;
  }
  else if (local_90 < 0) {
LAB_1038f0b7c:
    operator_delete(local_a0);
  }
  uVar4 = std::chrono::system_clock::now();
  FUN_103f3ffec(&local_50,3,uVar4);
  iVar2 = FUN_103f3c8b8(&local_50);
  if (iVar2 != 0) {
    FUN_103f3a958(&local_50,local_68);
  }
LAB_1038f0c1c:
  thunk_FUN_103f395e4(&local_50);
  if (-1 < local_51) {
    return;
  }
  operator_delete(local_68[0]);
  return;
}

