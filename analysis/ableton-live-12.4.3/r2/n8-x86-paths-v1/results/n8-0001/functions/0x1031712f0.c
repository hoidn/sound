
void FUN_1031712f0(undefined **param_1,undefined8 param_2,uint param_3,undefined8 param_4,
                  undefined8 param_5)

{
  int *piVar1;
  code *pcVar2;
  long *plVar3;
  char cVar4;
  int iVar5;
  undefined8 uVar6;
  long *plVar7;
  undefined **ppuVar8;
  long lVar9;
  undefined **ppuVar10;
  undefined *puVar11;
  undefined **ppuVar12;
  char *pcVar13;
  ulong uVar14;
  bool bVar15;
  undefined **ppuStack_c0;
  int *local_b0;
  int *local_a8;
  undefined **local_a0;
  undefined **local_98;
  undefined8 uStack_90;
  long *local_88;
  long *plStack_80;
  long *local_78;
  undefined **local_70;
  undefined **local_68;
  undefined **local_60;
  undefined8 uStack_58;
  undefined1 local_50;
  undefined ***local_48;
  long local_38;
  
  uVar14 = (ulong)param_3;
  local_38 = *(long *)PTR____stack_chk_guard_106a33b20;
  local_70 = (undefined **)param_4;
  uVar6 = FUN_1014f4b30();
  cVar4 = FUN_1014f9c80(uVar6);
  if (cVar4 == '\0') {
    FUN_101421a50(&local_68,
                  "products/live/Live/IceComplex/Src/AudioToMidi.cpp:455: silent exception thrown");
    FUN_101421a50(&local_a0,"products/live/Live/IceComplex/Src/AudioToMidi.cpp:455");
    FUN_101223140(&local_68,&local_a0);
    FUN_1002adbd0(&local_a0);
    FUN_1002adbd0(&local_68);
                    /* WARNING: Subroutine does not return */
    ___cxa_allocate_exception(0x30);
  }
  local_88 = (long *)0x0;
  plStack_80 = (long *)0x0;
  local_78 = (long *)0x0;
  uVar6 = FUN_1028f1df0(param_2);
  plVar7 = (long *)FUN_1029b5240(uVar6);
  cVar4 = (**(code **)(*plVar7 + 0x150))(plVar7);
  if (cVar4 == '\0') {
    FUN_101421a50(&local_b0,"Wait for Decoding");
    FUN_101440510(&local_a8,&DAT_1075566a0);
    ppuVar8 = (undefined **)FUN_1012bdaa0(0x60);
    local_68 = &PTR_FUN_106dff860;
    local_60 = (undefined **)param_2;
    local_48 = &local_68;
    FUN_103204d40(ppuVar8,&local_68,&local_b0,&local_a8);
    if (ppuVar8 != (undefined **)0x0) {
      *(int *)(ppuVar8 + 1) = *(int *)(ppuVar8 + 1) + 1;
    }
    if (local_48 == &local_68) {
      lVar9 = 0x20;
LAB_1031713fe:
      (**(code **)((long)*local_48 + lVar9))();
    }
    else {
      lVar9 = 0x28;
      if (local_48 != (undefined ***)0x0) goto LAB_1031713fe;
    }
    local_98 = ppuVar8 + 3;
    if (ppuVar8 == (undefined **)0x0) {
      local_98 = (undefined **)0x0;
    }
    if (plStack_80 < local_78) {
      *plStack_80 = (long)ppuVar8;
      local_a0 = (undefined **)0x0;
      plStack_80[1] = (long)local_98;
      local_98 = (undefined **)0x0;
      plStack_80 = plStack_80 + 2;
    }
    else {
      local_a0 = ppuVar8;
      plStack_80 = (long *)FUN_10317da60(&local_88,&local_a0);
      if (local_a0 != (undefined **)0x0) {
        ppuVar8 = local_a0 + 1;
        *(int *)ppuVar8 = *(int *)ppuVar8 + -1;
        if (*(int *)ppuVar8 == 0) {
          FUN_1012716c0();
        }
      }
    }
    if ((local_a8 != (int *)0x0) && (*local_a8 = *local_a8 + -1, *local_a8 == 0)) {
      FUN_101442b40();
    }
    if ((local_b0 != (int *)0x0) && (*local_b0 = *local_b0 + -1, *local_b0 == 0)) {
      FUN_101442b40();
    }
  }
  iVar5 = FUN_10118fec0();
  if ((iVar5 == 2) && (DAT_1074b89f8 == '\0')) {
    ppuVar8 = (undefined **)FUN_1012bdaa0(0x50);
    FUN_1031be970(ppuVar8,param_2,local_70,uVar14);
  }
  else if (param_3 < 2) {
    ppuVar8 = (undefined **)FUN_1012bdaa0(0x50);
    FUN_1031d7d40(ppuVar8,param_2,local_70,uVar14);
  }
  else {
    ppuVar8 = (undefined **)FUN_1012bdaa0(0x48);
    FUN_1031a5c70(ppuVar8,param_2,local_70);
  }
  if (ppuVar8 == (undefined **)0x0) {
    local_68 = (undefined **)0x0;
    ppuVar10 = (undefined **)0x0;
    local_60 = (undefined **)0x0;
    if (plStack_80 < local_78) goto LAB_103171557;
LAB_103171594:
    ppuStack_c0 = local_68;
    plStack_80 = (long *)FUN_10317da60(&local_88,&local_68);
    if (local_68 != (undefined **)0x0) {
      ppuVar8 = local_68 + 1;
      *(int *)ppuVar8 = *(int *)ppuVar8 + -1;
      if (*(int *)ppuVar8 == 0) {
        FUN_1012716c0();
      }
    }
  }
  else {
    *(int *)(ppuVar8 + 1) = *(int *)(ppuVar8 + 1) + 2;
    ppuVar10 = ppuVar8 + 3;
    local_68 = ppuVar8;
    local_60 = ppuVar10;
    if (local_78 <= plStack_80) goto LAB_103171594;
LAB_103171557:
    *plStack_80 = (long)local_68;
    plStack_80[1] = (long)ppuVar10;
    local_60 = (undefined **)0x0;
    plStack_80 = plStack_80 + 2;
    ppuStack_c0 = local_68;
  }
  if (param_3 < 3) {
    pcVar13 = (&PTR_s_H2M_106e00090)[uVar14];
  }
  else {
    pcVar13 = "?";
  }
  FUN_101421a50(&local_68,pcVar13);
  FUN_10316c080(param_5,&local_68);
  if ((local_68 != (undefined **)0x0) &&
     (*(int *)local_68 = *(int *)local_68 + -1, *(int *)local_68 == 0)) {
    FUN_101442b40();
  }
  FUN_103152560(&local_88,0);
  local_70 = ppuStack_c0;
  (**(code **)(*(long *)ppuStack_c0[8] + 8))();
  (**(code **)(*(long *)ppuStack_c0[8] + 0x10))();
  (**(code **)(*(long *)ppuStack_c0[8] + 0x48))(&local_a0);
  ppuVar10 = local_98;
  ppuVar8 = local_a0;
  local_68 = local_a0;
  local_60 = local_98;
  uStack_58 = uStack_90;
  local_50 = 1;
  *param_1 = (undefined *)0x0;
  param_1[1] = (undefined *)0x0;
  param_1[2] = (undefined *)0x0;
  local_98 = (undefined **)((ulong)local_98 & 0xffffffffffffff00);
  uVar14 = (long)ppuVar10 - (long)local_a0;
  if (uVar14 == 0) {
    bVar15 = local_a0 == (undefined **)0x0;
    ppuVar12 = local_70;
    local_a0 = param_1;
    if (bVar15) goto LAB_1031716fe;
  }
  else {
    if ((long)uVar14 < 0) {
      local_a0 = param_1;
      FUN_10317dd20(param_1);
                    /* WARNING: Does not return */
      pcVar2 = (code *)invalidInstructionException();
      (*pcVar2)();
    }
    local_a0 = param_1;
    puVar11 = operator_new(uVar14);
    *param_1 = puVar11;
    param_1[1] = puVar11;
    param_1[2] = puVar11 + uVar14;
    puVar11 = (undefined *)FUN_10317dd30(param_1 + 2,ppuVar8,ppuVar10,puVar11);
    ppuVar12 = local_70;
    param_1[1] = puVar11;
    if (ppuVar8 == (undefined **)0x0) goto LAB_1031716fe;
    do {
      puVar11 = ppuVar10[-3];
      if (puVar11 != (undefined *)0x0) {
        ppuVar10[-2] = puVar11;
        operator_delete(puVar11);
      }
      ppuVar10 = ppuVar10 + -8;
    } while (ppuVar10 != ppuVar8);
  }
  operator_delete(ppuVar8);
LAB_1031716fe:
  if (ppuVar12 != (undefined **)0x0) {
    ppuVar8 = ppuVar12 + 1;
    *(int *)ppuVar8 = *(int *)ppuVar8 + -1;
    if (*(int *)ppuVar8 == 0) {
      FUN_1012716c0(ppuVar12);
    }
  }
  plVar3 = local_88;
  plVar7 = plStack_80;
  if (local_88 != (long *)0x0) {
    for (; plVar7 != plVar3; plVar7 = plVar7 + -2) {
      if (plVar7[-2] != 0) {
        piVar1 = (int *)(plVar7[-2] + 8);
        *piVar1 = *piVar1 + -1;
        if (*piVar1 == 0) {
          FUN_1012716c0();
        }
      }
    }
    plStack_80 = plVar3;
    operator_delete(local_88);
  }
  DAT_1074b89f8 = 0;
  if (*(long *)PTR____stack_chk_guard_106a33b20 != local_38) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}

