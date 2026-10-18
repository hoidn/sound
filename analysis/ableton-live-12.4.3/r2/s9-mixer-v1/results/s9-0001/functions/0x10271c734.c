
void FUN_10271c734(long param_1)

{
  int iVar1;
  undefined8 *puVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  long *plVar5;
  int *piVar6;
  undefined8 *puVar7;
  undefined8 uVar8;
  int *local_88;
  int *local_80;
  int *local_78;
  undefined8 *local_70;
  undefined8 *local_68;
  undefined8 *local_60;
  undefined8 **local_58;
  ulong local_50;
  int *local_48;
  int *local_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_1064f8818;
  FUN_101427680(&local_48,"Stereo");
  FUN_101427680(&local_40,"Split Stereo");
  local_70 = (undefined8 *)0x0;
  local_68 = (undefined8 *)0x0;
  local_58 = &local_70;
  local_60 = (undefined8 *)0x0;
  local_50 = local_50 & 0xffffffffffffff00;
  local_70 = operator_new(0x10);
  local_68 = local_70 + 2;
  *local_70 = local_48;
  if (local_48 != (int *)0x0) {
    *local_48 = *local_48 + 1;
  }
  local_70[1] = local_40;
  local_60 = local_68;
  if (local_40 != (int *)0x0) {
    *local_40 = *local_40 + 1;
    iVar1 = *local_40;
    *local_40 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc(local_40);
    }
  }
  if ((local_48 != (int *)0x0) && (iVar1 = *local_48, *local_48 = iVar1 + -1, iVar1 + -1 == 0)) {
    FUN_101449efc();
  }
  local_58 = (undefined8 **)PTR__lambda___1__ARemoteable__TRemoteableUpdate__106551c78;
  local_50 = 0;
  FUN_101567ad8(*(undefined8 *)(param_1 + 0x2b8),0,&local_70,&local_58);
  uVar8 = *(undefined8 *)(param_1 + 0x2d0);
  uVar3 = FUN_1012d9850(0x38);
  FUN_1015757c0(0xbf800000,0x3f800000,0x3c820821,0x3c23d70a);
  uVar4 = FUN_101439ec4();
  FUN_101427680(&local_78,"Track Panning");
  FUN_1026f0bcc(0xbf800000,0x3f800000,0,uVar8,param_1,uVar3,uVar4,&local_78,1);
  if ((local_78 != (int *)0x0) && (iVar1 = *local_78, *local_78 = iVar1 + -1, iVar1 + -1 == 0)) {
    FUN_101449efc();
  }
  FUN_1026faab4(*(undefined8 *)(param_1 + 0x2d0));
  plVar5 = (long *)FUN_1026f96b0(*(undefined8 *)(param_1 + 0x2d0));
  (**(code **)(*plVar5 + 0x240))();
  uVar8 = *(undefined8 *)(param_1 + 0x2e8);
  uVar3 = FUN_1012d9850(0x38);
  FUN_1015757c0(0xbf800000,0x3f800000,0x3c820821,0x3c23d70a);
  uVar4 = FUN_101439ec4();
  FUN_101427680(&local_80,"Left Split Stereo");
  FUN_1026f0bcc(0xbf800000,0x3f800000,0xbf800000,uVar8,param_1,uVar3,uVar4,&local_80,1);
  if ((local_80 != (int *)0x0) && (iVar1 = *local_80, *local_80 = iVar1 + -1, iVar1 + -1 == 0)) {
    FUN_101449efc();
  }
  FUN_1026faab4(*(undefined8 *)(param_1 + 0x2e8));
  plVar5 = (long *)FUN_1026f96b0(*(undefined8 *)(param_1 + 0x2e8));
  (**(code **)(*plVar5 + 0x240))();
  uVar8 = *(undefined8 *)(param_1 + 0x300);
  uVar3 = FUN_1012d9850(0x38);
  FUN_1015757c0(0xbf800000,0x3f800000,0x3c820821,0x3c23d70a);
  uVar4 = FUN_101439ec4();
  FUN_101427680(&local_88,"Right Split Stereo");
  FUN_1026f0bcc(0xbf800000,0x3f800000,0x3f800000,uVar8,param_1,uVar3,uVar4,&local_88,1);
  if ((local_88 != (int *)0x0) && (iVar1 = *local_88, *local_88 = iVar1 + -1, iVar1 + -1 == 0)) {
    FUN_101449efc();
  }
  FUN_1026faab4(*(undefined8 *)(param_1 + 0x300));
  plVar5 = (long *)FUN_1026f96b0(*(undefined8 *)(param_1 + 0x300));
  (**(code **)(*plVar5 + 0x240))();
  puVar2 = local_70;
  puVar7 = local_68;
  if (local_70 != (undefined8 *)0x0) {
    while (puVar7 != puVar2) {
      puVar7 = puVar7 + -1;
      piVar6 = (int *)*puVar7;
      if ((piVar6 != (int *)0x0) && (iVar1 = *piVar6, *piVar6 = iVar1 + -1, iVar1 + -1 == 0)) {
        FUN_101449efc();
      }
    }
    local_68 = puVar2;
    operator_delete(local_70);
  }
  if (*(long *)PTR____stack_chk_guard_1064f8818 == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

