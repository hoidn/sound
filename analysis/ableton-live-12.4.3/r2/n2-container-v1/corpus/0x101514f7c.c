
/* WARNING: Removing unreachable block (ram,0x00010151529c) */
/* WARNING: Removing unreachable block (ram,0x000101515040) */
/* WARNING: Removing unreachable block (ram,0x0001015150dc) */
/* WARNING: Removing unreachable block (ram,0x0001015150f0) */
/* WARNING: Removing unreachable block (ram,0x00010151512c) */
/* WARNING: Removing unreachable block (ram,0x000101515350) */

bool FUN_101514f7c(int param_1,int param_2,int *param_3)

{
  ushort uVar1;
  int *piVar2;
  long *plVar3;
  long *plVar4;
  ushort *puVar5;
  int iVar6;
  ushort *puVar7;
  long *plVar8;
  undefined8 uVar9;
  ushort *puVar10;
  ushort *puVar11;
  int iVar12;
  ushort *puVar13;
  ushort *puVar14;
  uint uVar15;
  int iVar16;
  long lVar17;
  long *plVar18;
  undefined4 local_e8;
  undefined2 uStack_e4;
  undefined1 uStack_e2;
  undefined1 uStack_e1;
  char local_d1;
  long local_d0;
  long *local_c8;
  void *local_c0;
  undefined8 uStack_b8;
  long local_b0;
  long *local_a0;
  long *local_98;
  int local_88 [2];
  undefined8 local_80;
  undefined4 local_78;
  uint uStack_74;
  undefined8 uStack_70;
  undefined7 local_68;
  undefined1 uStack_61;
  
  *param_3 = -0x40000000;
  local_88[0] = 0;
  local_80 = std::system_category();
  FUN_1011db938(&local_d0);
  (**(code **)(*local_c8 + 0xc0))(&local_c0);
  uStack_e4 = 0x616d;
  local_e8 = 0x65686353;
  uStack_e2 = 0;
  local_d1 = '\x06';
  FUN_100241e54(&local_78,&local_c0,&local_e8);
  FUN_103e71880(&local_a0,&local_78,0x40,local_88);
  if (local_d1 < '\0') {
    operator_delete((void *)CONCAT17(uStack_e1,CONCAT16(uStack_e2,CONCAT24(uStack_e4,local_e8))));
  }
  if (local_b0 < 0) {
    operator_delete(local_c0);
  }
  plVar8 = local_a0;
  plVar3 = local_a0;
  plVar18 = local_98;
  if ((local_d0 != 0) &&
     (iVar6 = *(int *)(local_d0 + 8) + -1, *(int *)(local_d0 + 8) = iVar6, iVar6 == 0)) {
    FUN_10128eea0();
    plVar8 = local_a0;
    plVar3 = local_a0;
    plVar18 = local_98;
  }
  for (; plVar4 = local_98, local_a0 = plVar3, plVar8 != local_98; plVar8 = plVar8 + 1) {
    local_98 = plVar18;
    FUN_103e7c174(plVar8);
    FUN_103f62660(&local_78);
    local_c0 = (void *)CONCAT44(uStack_74,local_78);
    uStack_b8 = uStack_70;
    local_b0 = CONCAT17(uStack_61,local_68);
    local_78 = 0x7478742e;
    uStack_74 = uStack_74 & 0xffffff00;
    uStack_61 = 4;
    iVar6 = FUN_103e93790(&local_c0,&local_78);
    if (local_b0 < 0) {
      operator_delete(local_c0);
    }
    if (iVar6 == 0) {
      FUN_103e7c174(plVar8);
      FUN_103e96958(&local_78);
      local_c0 = (void *)0x0;
      uStack_b8 = 0;
      local_b0 = 0;
      FUN_103f62520(&local_78,&local_c0);
      thunk_FUN_101432b6c(&local_e8,&local_78);
      if (local_b0 < 0) {
        operator_delete(local_c0);
      }
      puVar7 = (ushort *)FUN_10142d764(&local_e8);
      uVar15 = (uint)*puVar7;
      if (*puVar7 - 0x30 < 10) {
        iVar6 = 0;
        puVar13 = puVar7 + 1;
        puVar5 = puVar7 + 3;
        puVar7 = puVar7 + 4;
        do {
          puVar10 = puVar7;
          puVar11 = puVar5;
          iVar6 = uVar15 + iVar6 * 10 + -0x30;
          puVar14 = puVar13 + 1;
          uVar15 = (uint)*puVar13;
          puVar13 = puVar14;
          puVar5 = puVar11 + 1;
          puVar7 = puVar10 + 1;
        } while (uVar15 - 0x30 < 10);
        if ((uVar15 == 0x2e) && (uVar1 = *puVar14, uVar15 = (uint)uVar1, uVar1 - 0x30 < 10)) {
          iVar12 = 0;
          do {
            iVar12 = uVar15 + iVar12 * 10 + -0x30;
            puVar7 = puVar11 + 1;
            uVar15 = (uint)*puVar11;
            puVar10 = puVar10 + 1;
            puVar11 = puVar7;
          } while (uVar15 - 0x30 < 10);
          if ((uVar15 == 0x5f) && (uVar1 = *puVar7, uVar15 = (uint)uVar1, uVar1 - 0x30 < 10)) {
            lVar17 = 0;
            iVar16 = 0;
            do {
              iVar16 = uVar15 + iVar16 * 10 + -0x30;
              uVar15 = (uint)*(ushort *)((long)puVar10 + lVar17);
              lVar17 = lVar17 + 2;
            } while (uVar15 - 0x30 < 10);
            if (((uVar15 == 0 && iVar6 == param_1) && iVar12 == param_2) && (*param_3 < iVar16)) {
              *param_3 = iVar16;
            }
          }
        }
      }
      piVar2 = (int *)CONCAT17(uStack_e1,CONCAT16(uStack_e2,CONCAT24(uStack_e4,local_e8)));
      if ((piVar2 != (int *)0x0) && (iVar6 = *piVar2, *piVar2 = iVar6 + -1, iVar6 + -1 == 0)) {
        FUN_101449efc();
      }
    }
    plVar3 = local_a0;
    plVar18 = local_98;
    local_98 = plVar4;
  }
  if (plVar3 != (long *)0x0) {
    while (plVar18 != plVar3) {
      plVar18 = plVar18 + -1;
      plVar8 = (long *)*plVar18;
      *plVar18 = 0;
      if (plVar8 != (long *)0x0) {
        (**(code **)(*plVar8 + 8))();
      }
    }
    operator_delete(local_a0);
  }
  if (local_88[0] != 0) {
    uVar9 = std::chrono::system_clock::now();
    FUN_103f3ffec(&local_a0,4,uVar9);
    iVar6 = FUN_103f3c8b8(&local_a0);
    if (iVar6 != 0) {
      uVar9 = FUN_103f39a78(&local_a0,"Live: Finding schema file failed: ");
      std::error_code::message();
      FUN_103f3a958(uVar9,&local_78);
    }
    thunk_FUN_103f395e4(&local_a0);
  }
  return *param_3 != -0x40000000;
}

