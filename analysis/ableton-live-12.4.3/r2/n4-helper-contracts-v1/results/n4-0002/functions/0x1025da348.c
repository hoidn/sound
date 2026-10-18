
ulong FUN_1025da348(long param_1,undefined8 param_2,undefined8 param_3,undefined8 *param_4,
                   undefined4 param_5,undefined8 param_6)

{
  undefined **ppuVar1;
  int iVar2;
  undefined8 uVar3;
  long *plVar4;
  ulong uVar5;
  long lVar6;
  long *plVar7;
  undefined **local_d8;
  long *local_d0;
  long *local_c8;
  long *local_c0;
  long alStack_b8 [3];
  long *local_a0;
  undefined **local_98;
  long lStack_90;
  undefined ***local_80;
  undefined **local_78;
  long lStack_70;
  undefined ***local_60;
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_1064f8818;
  if (((DAT_10700b9e8 & 1) == 0) && (iVar2 = ___cxa_guard_acquire(&DAT_10700b9e8), iVar2 != 0)) {
    uVar3 = FUN_1011b89d0();
    DAT_10700b9a0 = FUN_1011b8ac4(uVar3,"Trace::ProcessController",1);
    ___cxa_guard_release(&DAT_10700b9e8);
  }
  uVar3 = FUN_1011b89d0();
  iVar2 = FUN_1011b8ab0(uVar3,DAT_10700b9a0);
  if (iVar2 != 0) {
    FUN_1011b6484("ProcessController","LaunchWithArguments");
  }
  uVar3 = *(undefined8 *)(param_1 + 0x90);
  local_d0 = (long *)*param_4;
  *param_4 = 0;
  local_a0 = (long *)0x0;
  FUN_1015daecc(&local_c8,uVar3,&local_d0,alStack_b8);
  uVar3 = *(undefined8 *)(param_1 + 0xa0);
  plVar4 = operator_new(0x78);
  local_c0 = local_c8;
  *plVar4 = 0;
  plVar4[1] = 0;
  local_c8 = (long *)0x0;
  local_78 = &PTR_FUN_1067e3688;
  local_60 = &local_78;
  local_98 = &PTR_FUN_1067e3718;
  lStack_90 = param_1;
  local_80 = &local_98;
  lStack_70 = param_1;
  FUN_1025db270(plVar4 + 2,&local_c0,&local_78,&local_98,uVar3);
  if (local_80 == &local_98) {
    lVar6 = 0x20;
LAB_1025da45c:
    (**(code **)((long)*local_80 + lVar6))();
  }
  else if (local_80 != (undefined ***)0x0) {
    lVar6 = 0x28;
    goto LAB_1025da45c;
  }
  if (local_60 == &local_78) {
    lVar6 = 0x20;
LAB_1025da48c:
    (**(code **)((long)*local_60 + lVar6))();
  }
  else if (local_60 != (undefined ***)0x0) {
    lVar6 = 0x28;
    goto LAB_1025da48c;
  }
  if (local_c0 != (long *)0x0) {
    (**(code **)(*local_c0 + 8))();
  }
  plVar7 = local_c8;
  lVar6 = *(long *)(param_1 + 0x38);
  *plVar4 = lVar6;
  plVar4[1] = param_1 + 0x38;
  *(long **)(lVar6 + 8) = plVar4;
  *(long **)(param_1 + 0x38) = plVar4;
  *(long *)(param_1 + 0x48) = *(long *)(param_1 + 0x48) + 1;
  local_c8 = (long *)0x0;
  if (plVar7 != (long *)0x0) {
    (**(code **)(*plVar7 + 8))();
  }
  if (local_a0 == alStack_b8) {
    lVar6 = 0x20;
  }
  else {
    if (local_a0 == (long *)0x0) goto LAB_1025da50c;
    lVar6 = 0x28;
  }
  (**(code **)(*local_a0 + lVar6))();
LAB_1025da50c:
  plVar4 = local_d0;
  local_d0 = (long *)0x0;
  if (plVar4 != (long *)0x0) {
    (**(code **)(*plVar4 + 8))();
  }
  local_98 = (undefined **)CONCAT44(local_98._4_4_,param_5);
  plVar4 = *(long **)(param_1 + 0x30);
  if (plVar4 == (long *)0x0) {
                    /* WARNING: Subroutine does not return */
    FUN_10025e3f8();
  }
  (**(code **)(*plVar4 + 0x30))(&local_78,plVar4,param_2,&local_98);
  (**(code **)(*local_78 + 0x28))(local_78,param_3);
  ppuVar1 = local_78;
  lVar6 = *(long *)(param_1 + 0x38);
  local_d8 = local_78;
  if (local_78 != (undefined **)0x0) {
    *(int *)(local_78 + 1) = *(int *)(local_78 + 1) + 1;
  }
  uVar5 = FUN_1025da84c(lVar6 + 0x10,&local_d8,param_6);
  if ((ppuVar1 != (undefined **)0x0) &&
     (iVar2 = *(int *)(ppuVar1 + 1), *(int *)(ppuVar1 + 1) = iVar2 + -1, iVar2 + -1 == 0)) {
    FUN_10128eea0(ppuVar1);
  }
  if (uVar5 >> 0x20 == 0) {
    if (((DAT_10700b9f0 & 1) == 0) && (iVar2 = ___cxa_guard_acquire(&DAT_10700b9f0), iVar2 != 0)) {
      uVar3 = FUN_1011b89d0();
      DAT_10700b9a4 = FUN_1011b8ac4(uVar3,"Trace::ProcessController",1);
      ___cxa_guard_release(&DAT_10700b9f0);
    }
    uVar3 = FUN_1011b89d0();
    iVar2 = FUN_1011b8ab0(uVar3,DAT_10700b9a4);
    if (iVar2 != 0) {
      FUN_1011b66f8("ProcessController","Launched ProcessObserver (%x)");
    }
  }
  else {
    plVar7 = *(long **)(param_1 + 0x38);
    lVar6 = *plVar7;
    plVar4 = (long *)plVar7[1];
    *(long **)(lVar6 + 8) = plVar4;
    *plVar4 = lVar6;
    *(long *)(param_1 + 0x48) = *(long *)(param_1 + 0x48) + -1;
    (**(code **)plVar7[2])();
    operator_delete(plVar7);
  }
  if ((local_78 != (undefined **)0x0) &&
     (iVar2 = *(int *)(local_78 + 1), *(int *)(local_78 + 1) = iVar2 + -1, iVar2 + -1 == 0)) {
    FUN_10128eea0();
  }
  if (*(long *)PTR____stack_chk_guard_1064f8818 != local_58) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return uVar5;
}

