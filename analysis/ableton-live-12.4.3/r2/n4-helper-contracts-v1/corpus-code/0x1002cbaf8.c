// 0x1002cbaf8 FUN_1002cbaf8 exported-with-warnings  sig: undefined FUN_1002cbaf8()

/* WARNING: Removing unreachable block (ram,0x0001002cbcc0) */
/* WARNING: Removing unreachable block (ram,0x0001002cbe0c) */
/* WARNING: Removing unreachable block (ram,0x0001002cc0a0) */
/* WARNING: Removing unreachable block (ram,0x0001002cc058) */
/* WARNING: Removing unreachable block (ram,0x0001002cc0b0) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1002cbaf8(long *param_1)

{
  ulong *puVar1;
  int iVar2;
  uint uVar3;
  ulong uVar4;
  long *plVar5;
  undefined8 uVar6;
  undefined8 uVar7;
  undefined1 *puVar8;
  ulong extraout_x1;
  ulong extraout_x1_00;
  ulong extraout_x1_01;
  int *local_2a0;
  undefined8 uStack_298;
  long lStack_290;
  undefined8 uStack_288;
  int *local_280;
  long lStack_278;
  long local_270;
  int *local_268;
  undefined1 auStack_260 [8];
  void *local_258;
  char local_241;
  void *local_240;
  char local_229;
  undefined1 auStack_220 [360];
  undefined1 auStack_b8 [32];
  int *local_98;
  undefined1 local_90;
  undefined1 uStack_8f;
  undefined1 uStack_8e;
  undefined5 uStack_8d;
  undefined1 local_81;
  int *local_80;
  long *local_78;
  undefined1 *local_70;
  long lStack_68;
  ulong local_60;
  undefined8 uStack_58;
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_1064f8818;
  FUN_101223370(auStack_260);
  iVar2 = (**(code **)(*param_1 + 0x718))(param_1);
  if (((iVar2 == 0) || (uVar4 = FUN_101221ffc(auStack_260), (uVar4 & 1) == 0)) &&
     (uVar4 = FUN_101221a10(auStack_260), (uVar4 & 1) == 0)) {
    FUN_101221cbc(&local_70,auStack_260);
    thunk_FUN_101432b6c(&local_2a0,&local_70);
    FUN_1011cb734(&local_98);
    FUN_1011cb734(&local_280);
    FUN_1011cb734(&local_80);
    FUN_1011cb734(&local_268);
    FUN_101241d1c(&DAT_106ec3340,&local_2a0,&local_98,&local_280,&local_80,&local_268);
    if ((local_268 != (int *)0x0) && (iVar2 = *local_268, *local_268 = iVar2 + -1, iVar2 + -1 == 0))
    {
      FUN_101449efc();
    }
    if ((local_80 != (int *)0x0) && (iVar2 = *local_80, *local_80 = iVar2 + -1, iVar2 + -1 == 0)) {
      FUN_101449efc();
    }
    if ((local_280 != (int *)0x0) && (iVar2 = *local_280, *local_280 = iVar2 + -1, iVar2 + -1 == 0))
    {
      FUN_101449efc();
    }
    if ((local_98 != (int *)0x0) && (iVar2 = *local_98, *local_98 = iVar2 + -1, iVar2 + -1 == 0)) {
      FUN_101449efc();
    }
    if ((local_2a0 != (int *)0x0) && (iVar2 = *local_2a0, *local_2a0 = iVar2 + -1, iVar2 + -1 == 0))
    {
      FUN_101449efc();
    }
    plVar5 = (long *)FUN_10125f068();
    (**(code **)(*plVar5 + 0x30))();
  }
  else {
    FUN_101223348(&local_70,auStack_260);
    puVar1 = (ulong *)(param_1 + 0xd4);
    if (*(char *)((long)param_1 + 0x6b7) < '\0') {
      operator_delete((void *)*puVar1);
    }
    param_1[0xd5] = lStack_68;
    *puVar1 = (ulong)local_70;
    param_1[0xd6] = local_60;
    plVar5 = (long *)FUN_10125f068();
    uVar3 = (**(code **)(*param_1 + 0x718))(param_1);
    uVar6 = FUN_10122ed30();
    uVar7 = FUN_10122ed88();
    (**(code **)(*plVar5 + 0x38))(plVar5,puVar1,uVar3 | 2,uVar6,uVar7);
  }
  FUN_1011db938(&local_98);
  (**(code **)(*(long *)CONCAT53(uStack_8d,CONCAT12(uStack_8e,CONCAT11(uStack_8f,local_90))) + 0x48)
  )(&local_2a0);
  FUN_1015ed930(&local_70,&local_2a0);
  puVar1 = (ulong *)(param_1 + 0xda);
  if (*(char *)((long)param_1 + 0x6e7) < '\0') {
    operator_delete((void *)*puVar1);
  }
  param_1[0xdb] = lStack_68;
  *puVar1 = (ulong)local_70;
  param_1[0xdc] = local_60;
  local_60 = local_60 & 0xffffffffffffff;
  local_70 = (undefined1 *)((ulong)local_70 & 0xffffffffffffff00);
  if (lStack_290 < 0) {
    operator_delete(local_2a0);
  }
  if ((local_98 != (int *)0x0) && (iVar2 = local_98[2], local_98[2] = iVar2 + -1, iVar2 + -1 == 0))
  {
    FUN_10128eea0();
  }
  uVar6 = std::chrono::system_clock::now();
  FUN_103f3ffec(&local_70,2,uVar6);
  iVar2 = FUN_103f3c8b8(&local_70);
  if (iVar2 != 0) {
    uVar6 = FUN_103f39a78(&local_70,"Plugin scanner database: ");
    FUN_100259ba4(uVar6,puVar1);
  }
  thunk_FUN_103f395e4(&local_70);
  FUN_1011db938(&local_80);
  (**(code **)(*local_78 + 0xc0))(&local_2a0);
  local_98 = (int *)0x6573616261746144;
  local_90 = 0;
  local_81 = 8;
  FUN_100241e54(&local_70,&local_2a0,&local_98);
  if (lStack_290 < 0) {
    operator_delete(local_2a0);
  }
  if ((local_80 != (int *)0x0) && (iVar2 = local_80[2], local_80[2] = iVar2 + -1, iVar2 + -1 == 0))
  {
    FUN_10128eea0();
  }
  iVar2 = FUN_103e970a4(&local_70);
  if (iVar2 == 0) {
    local_280 = (int *)0x0;
    lStack_278 = 0;
    local_270 = 0;
  }
  else {
    local_98 = (int *)s_filerefmap_105ab01d8._0_8_;
    local_90 = 0x61;
    uStack_8f = 0x70;
    uStack_8e = 0;
    local_81 = 10;
    FUN_100241e54(&local_2a0,&local_70,&local_98);
    FUN_101284b54(&local_280,&local_2a0,0x1f);
    if (lStack_290 < 0) {
      operator_delete(local_2a0);
    }
  }
  if (*(char *)((long)param_1 + 0x6cf) < '\0') {
    operator_delete((void *)param_1[0xd7]);
  }
  param_1[0xd8] = lStack_278;
  param_1[0xd7] = (long)local_280;
  param_1[0xd9] = local_270;
  puVar8 = (undefined1 *)FUN_1012d9850(0x38);
  thunk_FUN_1014eccb8(puVar8,param_1 + 0xd7,1);
  if (puVar8 != (undefined1 *)0x0) {
    *(int *)(puVar8 + 8) = *(int *)(puVar8 + 8) + 1;
  }
  local_70 = puVar8;
  FUN_1014ed534(&local_70);
  if ((local_70 != (undefined1 *)0x0) &&
     (iVar2 = *(int *)(local_70 + 8), *(int *)(local_70 + 8) = iVar2 + -1, iVar2 + -1 == 0)) {
    FUN_10128eea0();
  }
  plVar5 = (long *)FUN_10125f068();
  FUN_1011d9014(&local_70);
  (**(code **)(*plVar5 + 0x60))(plVar5,&local_70);
  if ((local_70 != (undefined1 *)0x0) &&
     (iVar2 = *(int *)(local_70 + 8), *(int *)(local_70 + 8) = iVar2 + -1, iVar2 + -1 == 0)) {
    FUN_10128eea0();
  }
  FUN_1011c6508(&local_70);
  FUN_1012081bc(&local_70);
  FUN_1002fca34(&lStack_68,local_60);
  lStack_68 = _UNK_1055d7d94;
  local_70 = _DAT_1055d7d8c;
  uStack_58 = _UNK_1055d7da4;
  local_60 = _DAT_1055d7d9c;
  FUN_1011aeb80(&local_70);
  if ((((extraout_x1 & 1) == 0) && (iVar2 = FUN_1011b59ec(), iVar2 != 2)) &&
     (iVar2 = FUN_1011b59ec(), iVar2 != 1)) {
    lStack_68 = _UNK_1055d8138;
    local_70 = _DAT_1055d8130;
    uStack_58 = _UNK_1055d8148;
    local_60 = _DAT_1055d8140;
    FUN_1011aeb80(&local_70);
    if ((extraout_x1_00 & 1) == 0) {
      uStack_298 = _UNK_1055d7db4;
      local_2a0 = _DAT_1055d7dac;
      uStack_288 = _UNK_1055d7dc4;
      lStack_290 = _DAT_1055d7dbc;
      FUN_1011aeb80(&local_2a0);
      if ((extraout_x1_01 & 1) == 0) {
        (**(code **)(*(long *)param_1[0xf2] + 0x10))();
      }
    }
  }
  local_70 = auStack_b8;
  FUN_100253b50(&local_70);
  FUN_1002fcaa8(auStack_220);
  if (local_229 < '\0') {
    operator_delete(local_240);
  }
  if (local_241 < '\0') {
    operator_delete(local_258);
    if (*(long *)PTR____stack_chk_guard_1064f8818 != local_48) goto LAB_1002cc08c;
  }
  else if (*(long *)PTR____stack_chk_guard_1064f8818 != local_48) {
LAB_1002cc08c:
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


