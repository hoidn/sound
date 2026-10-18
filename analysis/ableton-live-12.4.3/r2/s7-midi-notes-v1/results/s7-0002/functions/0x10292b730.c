
void FUN_10292b730(long param_1)

{
  bool bVar1;
  undefined *puVar2;
  code *pcVar3;
  int iVar4;
  uint uVar5;
  long lVar6;
  void *pvVar7;
  undefined8 uVar8;
  ulong uVar9;
  void *pvVar10;
  undefined8 *puVar11;
  ulong uVar12;
  void *pvVar13;
  float fVar14;
  float fVar15;
  double dVar16;
  float fVar17;
  double local_d8;
  float local_d0;
  undefined8 local_cc;
  undefined8 uStack_c4;
  undefined8 local_bc;
  undefined8 uStack_b4;
  undefined4 local_ac;
  void *local_a8;
  void *pvStack_a0;
  void *local_98;
  undefined8 local_90;
  undefined8 uStack_88;
  undefined8 uStack_80;
  undefined8 uStack_78;
  undefined4 local_70;
  long local_68;
  
  local_68 = *(long *)PTR____stack_chk_guard_1064f8818;
  FUN_101486fa8();
  if ((0x82 < *(int *)(param_1 + 0x48) + 2U) || (iVar4 = FUN_1011afdac(), iVar4 == 0))
  goto LAB_10292b950;
  uVar8 = *(undefined8 *)(param_1 + 0x30);
  iVar4 = FUN_10155ede4(uVar8);
  if (iVar4 == 0) {
LAB_10292b868:
    pvVar10 = (void *)0x0;
    pvVar13 = (void *)0x0;
  }
  else {
    lVar6 = FUN_10155ee2c(uVar8,0);
    uVar5 = FUN_10155ede4(uVar8);
    if (uVar5 == 0) goto LAB_10292b868;
    if ((int)uVar5 < 1) {
      FUN_105425030();
                    /* WARNING: Does not return */
      pcVar3 = (code *)SoftwareBreakpoint(1,0x10292b994);
      (*pcVar3)();
    }
    uVar9 = (ulong)uVar5 * 0x30;
    local_a8 = operator_new(uVar9);
    local_98 = (void *)((long)local_a8 + uVar9);
    puVar11 = (undefined8 *)(lVar6 + 0xc);
    pvStack_a0 = local_a8;
    do {
      dVar16 = *(double *)((long)puVar11 + -0xc);
      if (dVar16 != 1.79769313486232e+308) {
        fVar17 = *(float *)((long)puVar11 + -4);
        uStack_88 = puVar11[1];
        local_90 = *puVar11;
        uStack_78 = puVar11[3];
        uStack_80 = puVar11[2];
        local_70 = *(undefined4 *)(puVar11 + 4);
        fVar14 = (float)FUN_1011afc18(*(undefined4 *)(param_1 + 0x48));
        fVar15 = (float)FUN_1011afc2c(*(undefined4 *)(param_1 + 0x48));
        if (fVar17 <= fVar15) {
          fVar15 = fVar17;
        }
        local_d0 = fVar14;
        if (fVar14 <= fVar17) {
          local_d0 = fVar15;
        }
        uStack_c4 = uStack_88;
        local_cc = local_90;
        uStack_b4 = uStack_78;
        local_bc = uStack_80;
        local_ac = local_70;
        local_d8 = dVar16;
        FUN_10292ebc0(&local_a8,&local_d8,0);
      }
      puVar11 = puVar11 + 6;
      uVar9 = uVar9 - 0x30;
      pvVar10 = local_a8;
      pvVar13 = pvStack_a0;
    } while (uVar9 != 0);
  }
  puVar2 = PTR_nothrow_1064f8658;
  uVar12 = ((long)pvVar13 - (long)pvVar10 >> 4) * -0x5555555555555555;
  uVar9 = uVar12;
  if (0x1800 < (long)pvVar13 - (long)pvVar10) {
    do {
      pvVar7 = operator_new(uVar9 * 0x30,(nothrow_t *)puVar2);
      if (pvVar7 != (void *)0x0) goto LAB_10292b8d8;
      bVar1 = 1 < uVar9;
      uVar9 = uVar9 >> 1;
    } while (bVar1);
  }
  pvVar7 = (void *)0x0;
  uVar9 = 0;
LAB_10292b8d8:
  FUN_1029307b8(pvVar10,pvVar13,uVar12,pvVar7,uVar9);
  if (pvVar7 != (void *)0x0) {
    operator_delete(pvVar7);
  }
  if (pvVar10 != pvVar13) {
    FUN_10155faa0(*(undefined8 *)(param_1 + 0x30),pvVar10,uVar12,0);
  }
  iVar4 = FUN_10155ede4(*(undefined8 *)(param_1 + 0x30));
  if ((int)uVar12 < iVar4) {
    uVar8 = *(undefined8 *)(param_1 + 0x30);
    iVar4 = FUN_10155ede4(uVar8);
    FUN_10155f6d8(uVar8,uVar12,iVar4 - (int)uVar12);
  }
  if (pvVar10 != (void *)0x0) {
    operator_delete(pvVar10);
  }
LAB_10292b950:
  if (*(long *)PTR____stack_chk_guard_1064f8818 == local_68) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

