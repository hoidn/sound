
void FUN_101483d00(void)

{
  int iVar1;
  void *pvVar2;
  undefined8 *puVar3;
  long *plVar4;
  code *pcVar5;
  bool bVar6;
  undefined4 *puVar7;
  ulong uVar8;
  undefined8 uVar9;
  long lVar10;
  int *piVar11;
  undefined8 uVar12;
  undefined8 extraout_x8;
  long *plVar13;
  void *pvVar14;
  long lVar15;
  undefined1 auVar16 [16];
  undefined4 local_1808 [2];
  int *local_1800;
  long *local_17f8;
  long *local_17f0;
  long *plStack_17e8;
  undefined8 local_17e0;
  void *pvStack_17d8;
  undefined8 uStack_17d0;
  undefined8 *local_17c8;
  undefined8 local_17c0;
  undefined4 local_17b8;
  undefined1 auStack_17b0 [4];
  undefined4 local_17ac;
  undefined1 auStack_17a8 [8];
  int *local_17a0;
  long *local_1798;
  undefined8 local_1790;
  undefined1 auStack_1788 [8];
  undefined8 local_1780;
  undefined *puStack_1778;
  undefined4 local_1770 [2];
  undefined1 auStack_1768 [5816];
  undefined1 auStack_b0 [120];
  long local_38;
  
  auVar16 = (*(code *)PTR____chkstk_darwin_1064f8810)();
  uVar12 = auVar16._8_8_;
  local_1790 = auVar16._0_8_;
  local_38 = *(long *)PTR____stack_chk_guard_1064f8818;
  local_1798 = (long *)0x0;
  local_1770[0] = 0;
  FUN_101478258(&local_1798,&local_1790,local_1770);
  FUN_10146ad9c(local_1770,local_1790,local_1798);
  FUN_10120d708(auStack_17a8);
  local_17c0 = 0;
  pvStack_17d8 = (void *)0x0;
  local_17e0 = 0;
  local_17c8 = (undefined8 *)0x0;
  uStack_17d0 = 0;
  plStack_17e8 = (long *)0x0;
  local_17f0 = (long *)0x0;
  local_17b8 = 0x3f800000;
  FUN_101485d48(local_1798,auStack_17a8,&local_17ac,auStack_17b0,&local_17f0);
  FUN_101470f18(&local_17f8,local_1798,auStack_17a8,local_17ac,1,&local_17f0);
  FUN_10146adfc(local_1770,local_17f8);
  puVar7 = (undefined4 *)(**(code **)(*local_17f8 + 0x28))();
  local_1808[0] = *puVar7;
  local_1800 = *(int **)(puVar7 + 2);
  if (local_1800 != (int *)0x0) {
    *local_1800 = *local_1800 + 1;
  }
  uVar8 = FUN_1014c0c28(local_1808);
  uVar9 = local_1790;
  if ((uVar8 & 1) == 0) {
    local_1780 = FUN_10120e26c(local_1808);
    puStack_1778 = PTR_format_custom<TString>_106509e70;
    FUN_10143e88c(auStack_1788,L"Unknown class \"{}\" found",0x18,0xf,&local_1780);
                    /* WARNING: Subroutine does not return */
    FUN_10148229c(uVar9,auStack_1788);
  }
  uVar9 = FUN_10120e26c(local_1808);
  lVar10 = FUN_10148d8c8(&DAT_106f4f780,uVar9);
  if ((lVar10 == 0) || (lVar15 = *(long *)(lVar10 + 0x18), *(long *)(lVar10 + 0x18) == 0)) {
    uVar8 = FUN_10120e048(local_1808,uVar12);
    if ((uVar8 & 1) != 0) {
LAB_101483e68:
      FUN_101486fe4(extraout_x8,local_17f8,local_1798);
      if ((local_1800 != (int *)0x0) &&
         (iVar1 = *local_1800, *local_1800 = iVar1 + -1, iVar1 + -1 == 0)) {
        FUN_101449efc();
      }
      pvVar2 = pvStack_17d8;
      puVar3 = local_17c8;
      if ((local_17f8 != (long *)0x0) &&
         (iVar1 = (int)local_17f8[1] + -1, *(int *)(local_17f8 + 1) = iVar1, iVar1 == 0)) {
        FUN_10128eea0();
        pvVar2 = pvStack_17d8;
        puVar3 = local_17c8;
      }
      while (puVar3 != (void *)0x0) {
        pvVar14 = (void *)*puVar3;
        piVar11 = (int *)puVar3[2];
        pvStack_17d8 = pvVar2;
        if ((piVar11 != (int *)0x0) && (iVar1 = *piVar11, *piVar11 = iVar1 + -1, iVar1 + -1 == 0)) {
          FUN_101449efc();
        }
        operator_delete(puVar3);
        pvVar2 = pvStack_17d8;
        puVar3 = pvVar14;
      }
      pvStack_17d8 = (void *)0x0;
      if (pvVar2 != (void *)0x0) {
        operator_delete(pvVar2);
      }
      plVar4 = local_17f0;
      plVar13 = plStack_17e8;
      if (local_17f0 != (long *)0x0) {
        while (plVar13 != plVar4) {
          plVar13 = plVar13 + -1;
          lVar10 = *plVar13;
          *plVar13 = 0;
          if (lVar10 != 0) {
            FUN_101478454(plVar13);
          }
        }
        plStack_17e8 = plVar4;
        operator_delete(local_17f0);
      }
      if ((local_17a0 != (int *)0x0) &&
         (iVar1 = *local_17a0, *local_17a0 = iVar1 + -1, iVar1 + -1 == 0)) {
        FUN_101449efc();
      }
      thunk_FUN_10146b404(auStack_b0);
      thunk_FUN_10146b174(auStack_1768);
      if (((local_1798 != (long *)0x0) &&
          ((**(code **)(*local_1798 + 0x18))(), local_1798 != (long *)0x0)) &&
         (iVar1 = (int)local_1798[1] + -1, *(int *)(local_1798 + 1) = iVar1, iVar1 == 0)) {
        FUN_10128eea0();
      }
      if (*(long *)PTR____stack_chk_guard_1064f8818 == local_38) {
        return;
      }
                    /* WARNING: Subroutine does not return */
      ___stack_chk_fail();
    }
  }
  else {
    do {
      uVar8 = FUN_10120e048(lVar15,uVar12);
      if ((uVar8 & 1) != 0) goto LAB_101483e68;
      bVar6 = *(long *)(lVar15 + 0x18) != lVar15;
      lVar15 = *(long *)(lVar15 + 0x18);
    } while (bVar6);
  }
  FUN_101488490(local_1790,uVar12,local_1808);
                    /* WARNING: Does not return */
  pcVar5 = (code *)SoftwareBreakpoint(1,0x101484028);
  (*pcVar5)();
}

