
void FUN_101484108(undefined8 param_1,undefined8 param_2,undefined8 *param_3)

{
  int iVar1;
  void *pvVar2;
  undefined8 *puVar3;
  long *plVar4;
  code *pcVar5;
  bool bVar6;
  long *plVar7;
  undefined4 *puVar8;
  ulong uVar9;
  undefined8 uVar10;
  long lVar11;
  int *piVar12;
  undefined8 uVar13;
  undefined8 extraout_x8;
  void *pvVar14;
  long lVar15;
  undefined1 auVar16 [16];
  undefined4 local_1818 [2];
  int *local_1810;
  long *local_1808;
  long *local_1800;
  long *plStack_17f8;
  undefined8 local_17f0;
  void *pvStack_17e8;
  undefined8 uStack_17e0;
  undefined8 *local_17d8;
  undefined8 local_17d0;
  undefined4 local_17c8;
  undefined4 local_17b4;
  long *local_17b0;
  long *local_17a8;
  undefined8 local_17a0;
  undefined1 auStack_1798 [8];
  int *local_1790;
  undefined *puStack_1788;
  undefined4 local_1780 [2];
  undefined1 auStack_1778 [5816];
  undefined1 auStack_c0 [120];
  long local_48;
  
  auVar16 = (*(code *)PTR____chkstk_darwin_1064f8810)();
  uVar13 = auVar16._8_8_;
  local_17a0 = auVar16._0_8_;
  local_48 = *(long *)PTR____stack_chk_guard_1064f8818;
  local_17a8 = (long *)0x0;
  local_1780[0] = 0;
  FUN_101478258(&local_17a8,&local_17a0,local_1780);
  FUN_10146ad9c(local_1780,local_17a0,local_17a8);
  local_17b0 = (long *)0x0;
  plVar7 = (long *)FUN_1012d9850(0xd8);
  thunk_FUN_1015286a4();
  if (plVar7 != (long *)0x0) {
    *(int *)(plVar7 + 1) = (int)plVar7[1] + 1;
  }
  local_1800 = plVar7;
  if ((local_17b0 != (long *)0x0) &&
     (iVar1 = *(int *)((long)local_17b0 + 8) + -1, *(int *)((long)local_17b0 + 8) = iVar1,
     iVar1 == 0)) {
    FUN_10128eea0();
  }
  local_17b0 = plVar7;
  (**(code **)(*plVar7 + 0x28))(plVar7,local_17a0);
  local_17b4 = 0x80000000;
  local_17d0 = 0;
  pvStack_17e8 = (void *)0x0;
  local_17f0 = 0;
  local_17d8 = (undefined8 *)0x0;
  uStack_17e0 = 0;
  plStack_17f8 = (long *)0x0;
  local_1800 = (long *)0x0;
  local_17c8 = 0x3f800000;
  FUN_1015289c8(&local_1808,local_17b0,1,&local_17b4,&local_1800);
  FUN_10146adfc(local_1780,local_1808);
  puVar8 = (undefined4 *)(**(code **)(*local_1808 + 0x28))();
  local_1818[0] = *puVar8;
  local_1810 = *(int **)(puVar8 + 2);
  if (local_1810 != (int *)0x0) {
    *local_1810 = *local_1810 + 1;
  }
  uVar9 = FUN_1014c0c28(local_1818);
  uVar10 = local_17a0;
  if ((uVar9 & 1) == 0) {
    local_1790 = (int *)FUN_10120e26c(local_1818);
    puStack_1788 = PTR_format_custom<TString>_106509e70;
    FUN_10143e88c(auStack_1798,L"Unknown class \"{}\" found",0x18,0xf,&local_1790);
                    /* WARNING: Subroutine does not return */
    FUN_10148229c(uVar10,auStack_1798);
  }
  uVar10 = FUN_10120e26c(local_1818);
  lVar11 = FUN_10148d8c8(&DAT_106f4f780,uVar10);
  if ((lVar11 == 0) || (lVar15 = *(long *)(lVar11 + 0x18), *(long *)(lVar11 + 0x18) == 0)) {
    uVar9 = FUN_10120e048(local_1818,uVar13);
    if ((uVar9 & 1) != 0) {
LAB_1014842b8:
      FUN_101486fe4(extraout_x8,local_1808,local_17a8);
      if (param_3 != (undefined8 *)0x0) {
        FUN_1015298e4(&local_1790,local_17b0);
        piVar12 = (int *)*param_3;
        *param_3 = local_1790;
        local_1790 = piVar12;
        if ((piVar12 != (int *)0x0) && (iVar1 = *piVar12, *piVar12 = iVar1 + -1, iVar1 + -1 == 0)) {
          FUN_101449efc();
        }
      }
      if ((local_1810 != (int *)0x0) &&
         (iVar1 = *local_1810, *local_1810 = iVar1 + -1, iVar1 + -1 == 0)) {
        FUN_101449efc();
      }
      pvVar2 = pvStack_17e8;
      puVar3 = local_17d8;
      if ((local_1808 != (long *)0x0) &&
         (iVar1 = (int)local_1808[1] + -1, *(int *)(local_1808 + 1) = iVar1, iVar1 == 0)) {
        FUN_10128eea0();
        pvVar2 = pvStack_17e8;
        puVar3 = local_17d8;
      }
      while (puVar3 != (void *)0x0) {
        pvVar14 = (void *)*puVar3;
        piVar12 = (int *)puVar3[2];
        pvStack_17e8 = pvVar2;
        if ((piVar12 != (int *)0x0) && (iVar1 = *piVar12, *piVar12 = iVar1 + -1, iVar1 + -1 == 0)) {
          FUN_101449efc();
        }
        operator_delete(puVar3);
        pvVar2 = pvStack_17e8;
        puVar3 = pvVar14;
      }
      pvStack_17e8 = (void *)0x0;
      if (pvVar2 != (void *)0x0) {
        operator_delete(pvVar2);
      }
      plVar4 = local_1800;
      plVar7 = plStack_17f8;
      if (local_1800 != (long *)0x0) {
        while (plVar7 != plVar4) {
          plVar7 = plVar7 + -1;
          lVar11 = *plVar7;
          *plVar7 = 0;
          if (lVar11 != 0) {
            FUN_101478454(plVar7);
          }
        }
        plStack_17f8 = plVar4;
        operator_delete(local_1800);
      }
      if (((local_17b0 != (long *)0x0) &&
          ((**(code **)(*local_17b0 + 0x18))(), local_17b0 != (long *)0x0)) &&
         (iVar1 = (int)local_17b0[1] + -1, *(int *)(local_17b0 + 1) = iVar1, iVar1 == 0)) {
        FUN_10128eea0();
      }
      thunk_FUN_10146b404(auStack_c0);
      thunk_FUN_10146b174(auStack_1778);
      if (((local_17a8 != (long *)0x0) &&
          ((**(code **)(*local_17a8 + 0x18))(), local_17a8 != (long *)0x0)) &&
         (iVar1 = (int)local_17a8[1] + -1, *(int *)(local_17a8 + 1) = iVar1, iVar1 == 0)) {
        FUN_10128eea0();
      }
      if (*(long *)PTR____stack_chk_guard_1064f8818 == local_48) {
        return;
      }
                    /* WARNING: Subroutine does not return */
      ___stack_chk_fail();
    }
  }
  else {
    do {
      uVar9 = FUN_10120e048(lVar15,uVar13);
      if ((uVar9 & 1) != 0) goto LAB_1014842b8;
      bVar6 = *(long *)(lVar15 + 0x18) != lVar15;
      lVar15 = *(long *)(lVar15 + 0x18);
    } while (bVar6);
  }
  FUN_101488490(local_17a0,uVar13,local_1818);
                    /* WARNING: Does not return */
  pcVar5 = (code *)SoftwareBreakpoint(1,0x1014844c8);
  (*pcVar5)();
}

