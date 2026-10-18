// 0x1038f022c FUN_1038f022c exported-with-warnings  sig: undefined FUN_1038f022c()

undefined *
FUN_1038f022c(undefined *param_1,undefined8 *param_2,undefined8 *param_3,undefined8 *param_4,
             undefined8 param_5,long *param_6,undefined4 param_7,undefined4 param_8)

{
  int iVar1;
  undefined8 *puVar2;
  long lVar3;
  undefined **ppuVar4;
  long lVar5;
  undefined **ppuVar6;
  undefined **ppuVar7;
  undefined **ppuVar8;
  undefined8 uVar9;
  undefined8 uVar10;
  long local_98;
  long local_90;
  undefined **local_88;
  undefined *puStack_80;
  undefined ***local_70;
  undefined *local_68;
  undefined *puStack_60;
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_1064f8818;
  puVar2 = (undefined8 *)FUN_10128ed98();
  *puVar2 = &PTR_thunk_FUN_1038f0668_106a3e188;
  uVar10 = param_2[1];
  uVar9 = *param_2;
  puVar2[5] = param_2[2];
  puVar2[4] = uVar10;
  puVar2[3] = uVar9;
  param_2[1] = 0;
  param_2[2] = 0;
  *param_2 = 0;
  puVar2[6] = 0;
  puVar2[7] = 0;
  puVar2[8] = 0;
  uVar9 = *param_3;
  puVar2[7] = param_3[1];
  puVar2[6] = uVar9;
  puVar2[8] = param_3[2];
  *param_3 = 0;
  param_3[1] = 0;
  param_3[2] = 0;
  if (*(char *)((long)param_4 + 0x17) < '\0') {
    FUN_10023448c(puVar2 + 9,*param_4,param_4[1]);
  }
  else {
    uVar10 = param_4[1];
    uVar9 = *param_4;
    puVar2[0xb] = param_4[2];
    puVar2[10] = uVar10;
    puVar2[9] = uVar9;
  }
  local_98 = *param_6;
  *param_6 = 0;
  lVar3 = FUN_1025d90d4(param_5,&local_98);
  *(long *)(param_1 + 0x60) = lVar3;
  if (lVar3 != 0) {
    *(int *)(lVar3 + 8) = *(int *)(lVar3 + 8) + 1;
  }
  if ((local_98 != 0) &&
     (iVar1 = *(int *)(local_98 + 8) + -1, *(int *)(local_98 + 8) = iVar1, iVar1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined8 *)(param_1 + 0x68) = 0;
  FUN_1038fd584(param_1 + 0x68,param_1 + 0x60);
  *(long *)(param_1 + 0x80) = 0;
  *(undefined4 *)(param_1 + 0x70) = param_7;
  *(undefined4 *)(param_1 + 0x74) = param_8;
  param_1[0x78] = 0;
  lVar3 = FUN_1012d9850(0x30);
  local_88 = &PTR_FUN_106a3e578;
  local_70 = &local_88;
  puStack_80 = param_1;
  FUN_10141f260(lVar3,&local_88);
  if (lVar3 != 0) {
    *(int *)(lVar3 + 8) = *(int *)(lVar3 + 8) + 1;
  }
  local_90 = lVar3;
  if (local_70 == &local_88) {
    lVar5 = 0x20;
  }
  else {
    if (local_70 == (undefined ***)0x0) goto LAB_1038f03c0;
    lVar5 = 0x28;
  }
  (**(code **)((long)*local_70 + lVar5))();
LAB_1038f03c0:
  lVar5 = *(long *)(param_1 + 0x80);
  if ((lVar5 != 0) && (iVar1 = *(int *)(lVar5 + 8) + -1, *(int *)(lVar5 + 8) = iVar1, iVar1 == 0)) {
    FUN_10128eea0();
  }
  *(long *)(param_1 + 0x80) = lVar3;
  *(undefined ***)(param_1 + 0x88) = &PTR_FUN_1067e3578;
  *(undefined8 *)(param_1 + 0x98) = 0;
  *(undefined8 *)(param_1 + 0xa0) = 0;
  *(undefined8 *)(param_1 + 0x90) = 0;
  lVar3 = FUN_1025d9f3c(*(undefined8 *)(param_1 + 0x60));
  FUN_101458fc8(&local_88,param_1);
  local_88 = (undefined **)&DAT_106592510;
  local_68 = PTR_CallMemberFunc<&TExternalAppLauncher::OnChildProcessStateChanged>_106530090;
  ppuVar4 = *(undefined ***)(lVar3 + 0x10);
  puStack_60 = param_1;
  if (ppuVar4 < *(undefined ***)(lVar3 + 0x18)) {
    ppuVar6 = ppuVar4 + 2;
    *ppuVar6 = (undefined *)0x0;
    ppuVar4[1] = (undefined *)0x0;
    ppuVar4[3] = (undefined *)local_70;
    if (local_70 != (undefined ***)0x0) {
      ppuVar8 = local_70[2];
      ppuVar7 = ppuVar4;
      if (ppuVar8 != (undefined **)0x0) {
        ppuVar6 = ppuVar8 + 1;
        ppuVar7 = (undefined **)*ppuVar6;
        ppuVar4[2] = (undefined *)ppuVar8;
        ppuVar7[2] = (undefined *)ppuVar4;
      }
      ppuVar4[1] = (undefined *)ppuVar7;
      *ppuVar6 = (undefined *)ppuVar4;
      local_70[2] = ppuVar4;
    }
    *ppuVar4 = (undefined *)&DAT_106592510;
    ppuVar4[5] = puStack_60;
    ppuVar4[4] = local_68;
    ppuVar4 = ppuVar4 + 6;
  }
  else {
    ppuVar4 = (undefined **)FUN_10027a5c8(lVar3 + 8,&local_88);
  }
  *(undefined ***)(lVar3 + 0x10) = ppuVar4;
  FUN_101459068(&local_88);
  if (*(long *)PTR____stack_chk_guard_1064f8818 != local_58) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return param_1;
}


