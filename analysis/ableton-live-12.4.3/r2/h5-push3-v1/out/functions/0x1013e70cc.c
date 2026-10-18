// 0x1013e70cc FUN_1013e70cc state=exported-with-warnings role=USB sysinfo query
// source chunk chunk-00890.jsonl; code_sha256=58f2ce1947a65225616c299a6f5c23fa4d24c7f91e958125f3324aa176df7fe8

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1013e70cc(undefined8 *param_1,undefined8 *param_2)

{
  uint *puVar1;
  ulong *puVar2;
  byte bVar3;
  undefined2 uVar4;
  void *pvVar5;
  code *pcVar6;
  int iVar7;
  undefined8 uVar8;
  ulong uVar9;
  long lVar10;
  long lVar11;
  void *pvVar12;
  uint uVar13;
  uint uVar14;
  ulong uVar15;
  short sVar16;
  undefined1 uVar17;
  uint uVar18;
  ulong *puVar19;
  size_t sVar20;
  undefined1 auVar21 [16];
  uint local_fc;
  ulong local_f8;
  char local_f0 [8];
  void *local_e8;
  ulong *local_e0;
  ulong *local_d8;
  undefined1 local_d0 [16];
  undefined1 local_c0 [16];
  undefined8 local_b0;
  undefined1 local_a8;
  byte bStack_a7;
  undefined2 uStack_a6;
  short sStack_a4;
  undefined2 uStack_a2;
  uint local_a0;
  undefined1 uStack_9c;
  undefined1 uStack_9b;
  undefined2 uStack_9a;
  int local_98;
  undefined4 local_94;
  undefined4 local_8c;
  undefined4 local_88;
  undefined4 local_84;
  uint local_80;
  uint local_78;
  long local_70;
  
  local_70 = *(long *)PTR____stack_chk_guard_101b8c408;
  if (*(int *)((long)param_2 + 0x1a4) != 1) {
    param_1[3] = 0;
    param_1[2] = 0;
    param_1[5] = 0;
    param_1[4] = 0;
    param_1[1] = 0;
    *param_1 = 0;
    goto LAB_1013e7718;
  }
  local_e8 = (void *)0x0;
  local_e0 = (ulong *)0x0;
  local_d8 = (ulong *)0x0;
  uVar8 = std::chrono::system_clock::now();
  FUN_1003324b0(local_c0,2,uVar8);
  iVar7 = FUN_10032ece8(local_c0);
  if (iVar7 != 0) {
    FUN_10032bea8(local_c0,"Querying system info");
  }
  thunk_FUN_10032ba14(local_c0);
  uVar8 = *param_2;
  local_c0 = FUN_1013ed848();
  uVar9 = FUN_1013eff5c(uVar8,local_c0,0x10);
  if ((uVar9 & 1) == 0) {
    uVar8 = std::chrono::system_clock::now();
    FUN_1003324b0(local_c0,4,uVar8);
    iVar7 = FUN_10032ece8(local_c0);
    if (iVar7 != 0) {
      FUN_10032bea8(local_c0,"Failed to send sysinfo request");
    }
LAB_1013e7328:
    thunk_FUN_10032ba14(local_c0);
    uVar17 = 0;
    uVar18 = 0;
    local_fc = 0;
    local_f8 = 0;
    sVar16 = 0;
  }
  else {
    lVar10 = FUN_1013f0008(*param_2,&local_98,0x28);
    if (lVar10 != 0x28) {
      uVar8 = std::chrono::system_clock::now();
      FUN_1003324b0(local_c0,4,uVar8);
      iVar7 = FUN_10032ece8(local_c0);
      if (iVar7 != 0) {
        FUN_10032bea8(local_c0,"Failed to receive sysinfo response");
      }
      goto LAB_1013e7328;
    }
    if ((local_98 != -0xfff02) || ((char)local_94 == '\0')) {
      uVar8 = std::chrono::system_clock::now();
      FUN_1003324b0(local_c0,4,uVar8);
      iVar7 = FUN_10032ece8(local_c0);
      if (iVar7 != 0) {
        FUN_10032bea8(local_c0,"Unexpected response message for sysinfo request");
      }
      goto LAB_1013e7328;
    }
    local_f0[0] = (char)local_94;
    if ((char)local_94 != '\x01') {
      uVar8 = std::chrono::system_clock::now();
      FUN_1003324b0(local_c0,3,uVar8);
      iVar7 = FUN_10032ece8(local_c0);
      if (iVar7 != 0) {
        uVar8 = FUN_10032bea8(local_c0,"Sysinfo version higher than expected: ");
        FUN_1013eaa54(uVar8,local_f0);
      }
      thunk_FUN_10032ba14(local_c0);
    }
    uVar8 = std::chrono::system_clock::now();
    FUN_1003324b0(local_c0,2,uVar8);
    iVar7 = FUN_10032ece8(local_c0);
    if (iVar7 != 0) {
      uVar8 = FUN_10032bea8(local_c0,"Engineering run: ");
      uVar18 = (local_94 >> 8 & 0xff) - 5;
      iVar7 = 0;
      if (uVar18 < 3) {
        iVar7 = (uVar18 & 0xff) + 1;
      }
      local_d0._0_4_ = iVar7;
      FUN_1013ead04(uVar8,local_d0);
    }
    thunk_FUN_10032ba14(local_c0);
    if (local_94._3_1_ == '\0') {
      uVar8 = std::chrono::system_clock::now();
      FUN_1003324b0(local_c0,2,uVar8);
      iVar7 = FUN_10032ece8(local_c0);
      if (iVar7 != 0) {
        FUN_10032bea8(local_c0,"Flash lock flag: unset");
      }
    }
    else {
      uVar8 = std::chrono::system_clock::now();
      FUN_1003324b0(local_c0,2,uVar8);
      iVar7 = FUN_10032ece8(local_c0);
      if (iVar7 != 0) {
        FUN_10032bea8(local_c0,"Flash lock flag: set");
      }
    }
    thunk_FUN_10032ba14(local_c0);
    uVar13 = local_8c;
    uVar18 = local_8c >> 8 & 0xff;
    if ((uVar18 == 0) || (uVar18 == 0xff)) {
      uVar8 = std::chrono::system_clock::now();
      FUN_1003324b0(local_c0,2,uVar8);
      iVar7 = FUN_10032ece8(local_c0);
      if (iVar7 != 0) {
        FUN_10032bea8(local_c0,"Compute module not installed (or unknown)");
      }
    }
    else {
      uVar8 = std::chrono::system_clock::now();
      FUN_1003324b0(local_c0,2,uVar8);
      iVar7 = FUN_10032ece8(local_c0);
      if (iVar7 != 0) {
        FUN_10032bea8(local_c0,"Compute module installed");
      }
    }
    thunk_FUN_10032ba14(local_c0);
    uVar18 = uVar13 >> 0x10 & 0xff;
    if ((uVar18 == 0) || (uVar18 == 0xff)) {
      uVar8 = std::chrono::system_clock::now();
      FUN_1003324b0(local_c0,2,uVar8);
      iVar7 = FUN_10032ece8(local_c0);
      if (iVar7 != 0) {
        FUN_10032bea8(local_c0,"Battery not installed (or unknown)");
      }
    }
    else {
      uVar8 = std::chrono::system_clock::now();
      FUN_1003324b0(local_c0,2,uVar8);
      iVar7 = FUN_10032ece8(local_c0);
      if (iVar7 != 0) {
        FUN_10032bea8(local_c0,"Battery installed");
      }
    }
    thunk_FUN_10032ba14(local_c0);
    uVar8 = std::chrono::system_clock::now();
    FUN_1003324b0(local_c0,2,uVar8);
    iVar7 = FUN_10032ece8(local_c0);
    if (iVar7 != 0) {
      uVar8 = FUN_10032bea8(local_c0,"Serial number: ");
      FUN_10032dc3c(uVar8,local_88);
    }
    thunk_FUN_10032ba14(local_c0);
    uVar8 = std::chrono::system_clock::now();
    FUN_1003324b0(local_c0,2,uVar8);
    iVar7 = FUN_10032ece8(local_c0);
    if (iVar7 != 0) {
      uVar8 = FUN_10032bea8(local_c0,"Uptime: ");
      uVar8 = FUN_10032dc3c(uVar8,local_84);
      FUN_10032bea8(uVar8," s");
    }
    thunk_FUN_10032ba14(local_c0);
    uVar18 = local_80;
    if (local_80 != 0) {
      local_d0._0_4_ = local_80 << 0x10 | local_80 >> 8 & 0xff00 | local_80 >> 0x18;
      uVar8 = std::chrono::system_clock::now();
      FUN_1003324b0(local_c0,2,uVar8);
      iVar7 = FUN_10032ece8(local_c0);
      if (iVar7 != 0) {
        uVar8 = FUN_10032bea8(local_c0,"Firmware package version: ");
        uVar8 = FUN_10032dbe0(uVar8,uVar18 >> 0x18);
        uVar8 = FUN_10032bea8(uVar8,".");
        uVar8 = FUN_10032dbe0(uVar8,uVar18 >> 0x10 & 0xff);
        uVar8 = FUN_10032bea8(uVar8,".");
        FUN_1013eafc8(uVar8,(ulong)local_d0 | 2);
      }
      thunk_FUN_10032ba14(local_c0);
    }
    uVar18 = (local_94 >> 8) - 5 & 0xff;
    sVar16 = 0;
    if (uVar18 < 3) {
      sVar16 = (short)uVar18 + 1;
    }
    local_f8 = (ulong)CONCAT14((local_94 & 0xff000000) != 0,
                               (uint)(local_8c._1_1_ != '\0' && local_8c._1_1_ != -1));
    if (local_80 == 0) {
      uVar17 = 0;
      uVar18 = 0;
      local_fc = 0;
    }
    else {
      uVar18 = local_80 >> 0x18;
      local_fc = local_80 >> 8 & 0xff00 | local_80 << 0x10;
      uVar17 = 1;
    }
  }
  uVar8 = std::chrono::system_clock::now();
  FUN_1003324b0(local_c0,2,uVar8);
  iVar7 = FUN_10032ece8(local_c0);
  if (iVar7 != 0) {
    FUN_10032bea8(local_c0,"Querying Firmware versions");
  }
  thunk_FUN_10032ba14(local_c0);
  puVar19 = (ulong *)0x0;
  lVar10 = 0;
  local_c0._8_8_ = _UNK_1018090c8;
  local_c0._0_8_ = _DAT_1018090c0;
  local_a8 = (undefined1)_UNK_1018090d8;
  bStack_a7 = (byte)((ulong)_UNK_1018090d8 >> 8);
  uStack_a6 = (undefined2)((ulong)_UNK_1018090d8 >> 0x10);
  sStack_a4 = (short)((ulong)_UNK_1018090d8 >> 0x20);
  uStack_a2 = (undefined2)((ulong)_UNK_1018090d8 >> 0x30);
  local_b0 = _DAT_1018090d0;
  local_a0 = 5;
  uStack_9c = 9;
  uStack_9b = 0;
  uStack_9a = 0;
  do {
    while( true ) {
      puVar1 = (uint *)(local_c0 + lVar10);
      uVar8 = *param_2;
      auVar21 = FUN_1013ed834(*(undefined4 *)(local_c0 + lVar10 + 4));
      local_d0 = auVar21;
      uVar9 = FUN_1013eff5c(uVar8,local_d0,0x10);
      if ((uVar9 & 1) != 0) break;
      uVar8 = std::chrono::system_clock::now();
      FUN_1003324b0(local_d0,4,uVar8);
      iVar7 = FUN_10032ece8(local_d0);
      if (iVar7 != 0) {
        uVar8 = FUN_10032bea8(local_d0,"Failed to send firmware version request for ");
        FUN_1013ea790(uVar8,puVar1);
      }
LAB_1013e73cc:
      thunk_FUN_10032ba14(local_d0);
      lVar10 = lVar10 + 8;
      if (lVar10 == 0x28) goto LAB_1013e7680;
    }
    lVar11 = FUN_1013f0008(*param_2,&local_98,0x28);
    pvVar5 = local_e8;
    if (lVar11 != 0x28) {
      uVar8 = std::chrono::system_clock::now();
      FUN_1003324b0(local_d0,4,uVar8);
      iVar7 = FUN_10032ece8(local_d0);
      if (iVar7 != 0) {
        uVar8 = FUN_10032bea8(local_d0,"Failed to receive firmware version response for ");
        FUN_1013ea790(uVar8,puVar1);
      }
      goto LAB_1013e73cc;
    }
    if (local_98 != -0xfff01) {
      uVar8 = std::chrono::system_clock::now();
      FUN_1003324b0(local_d0,4,uVar8);
      iVar7 = FUN_10032ece8(local_d0);
      if (iVar7 != 0) {
        uVar8 = FUN_10032bea8(local_d0,"Unexpected response message for ");
        FUN_1013ea790(uVar8,puVar1);
      }
      goto LAB_1013e73cc;
    }
    uVar13 = *puVar1;
    uVar14 = local_78;
    if ((uVar13 & 0xfffffffd) == 1) {
      uVar9 = (ulong)(local_78 >> 8);
    }
    else if (uVar13 == 2) {
      uVar9 = (ulong)local_78;
      uVar14 = local_78 >> 0x10;
      uVar13 = 2;
    }
    else if (uVar13 == 4) {
      uVar9 = 0;
      uVar14 = local_78 & 0xff;
      uVar13 = 4;
    }
    else if (uVar13 == 5) {
      uVar9 = (ulong)(local_78 >> 0x10);
      uVar13 = 5;
    }
    else {
      uVar13 = 0;
      uVar14 = 0;
      uVar9 = 0;
    }
    uVar4 = local_d0._6_2_;
    local_d0._0_6_ = CONCAT24((ushort)uVar14 & 0xff | (ushort)((uVar9 << 0x28) >> 0x20),uVar13);
    local_d0._0_8_ = CONCAT26(uVar4,local_d0._0_6_) & 0xff00ffffffffffff;
    if (puVar19 < local_d8) {
      *puVar19 = local_d0._0_8_;
    }
    else {
      sVar20 = (long)puVar19 - (long)local_e8;
      lVar11 = (long)sVar20 >> 3;
      uVar9 = lVar11 + 1;
      if (uVar9 >> 0x3d != 0) {
        FUN_100265704(&local_e8);
        goto LAB_1013e7a20;
      }
      uVar15 = (long)local_d8 - (long)local_e8 >> 2;
      if (uVar15 <= uVar9) {
        uVar15 = uVar9;
      }
      if (0x7ffffffffffffff7 < (ulong)((long)local_d8 - (long)local_e8)) {
        uVar15 = 0x1fffffffffffffff;
      }
      if (uVar15 == 0) {
        pvVar12 = (void *)0x0;
      }
      else {
        if (uVar15 >> 0x3d != 0) {
                    /* WARNING: Subroutine does not return */
          FUN_10017f504();
        }
        pvVar12 = operator_new(uVar15 << 3);
      }
      puVar19 = (ulong *)((long)pvVar12 + lVar11 * 8);
      puVar2 = (ulong *)((long)pvVar12 + uVar15 * 8);
      *puVar19 = local_d0._0_8_;
      _memcpy(pvVar12,pvVar5,sVar20);
      local_e8 = pvVar12;
      local_d8 = puVar2;
      if (pvVar5 != (void *)0x0) {
        operator_delete(pvVar5);
      }
    }
    puVar19 = puVar19 + 1;
    local_e0 = puVar19;
    uVar8 = std::chrono::system_clock::now();
    FUN_1003324b0(local_f0,2,uVar8);
    iVar7 = FUN_10032ece8(local_f0);
    if (iVar7 != 0) {
      uVar8 = FUN_1013ea790(local_f0,local_d0);
      uVar8 = FUN_10032bea8(uVar8," firmware version: ");
      uVar8 = FUN_10032dbe0(uVar8,local_d0[4]);
      uVar8 = FUN_10032bea8(uVar8,".");
      FUN_10032dbe0(uVar8,local_d0[5]);
    }
    thunk_FUN_10032ba14(local_f0);
    lVar10 = lVar10 + 8;
  } while (lVar10 != 0x28);
LAB_1013e7680:
  pvVar5 = local_e8;
  local_c0._0_8_ = 0;
  local_c0._8_8_ = 0;
  local_b0 = 0;
  uVar9 = (long)puVar19 - (long)local_e8;
  if (uVar9 == 0) {
    lVar10 = 0;
    pvVar12 = (void *)0x0;
  }
  else {
    if ((long)uVar9 < 0) {
      FUN_100265704(local_c0);
LAB_1013e7a20:
                    /* WARNING: Does not return */
      pcVar6 = (code *)SoftwareBreakpoint(1,0x1013e7a24);
      (*pcVar6)();
    }
    pvVar12 = operator_new(uVar9);
    lVar10 = (long)pvVar12 + uVar9;
    _memcpy(pvVar12,pvVar5,uVar9 - 1);
  }
  local_a8 = (undefined1)local_f8;
  bVar3 = (byte)(local_f8 >> 0x20);
  bStack_a7 = bVar3 ^ 1;
  local_a0 = local_fc | uVar18;
  uStack_a2 = 0;
  *param_1 = pvVar12;
  param_1[1] = lVar10;
  param_1[2] = lVar10;
  param_1[3] = (ulong)CONCAT24(sVar16,CONCAT22(uStack_a6,CONCAT11(bVar3,local_a8))) ^ 0x100;
  *(ulong *)((long)param_1 + 0x1e) = (ulong)CONCAT15(uStack_9b,CONCAT14(uVar17,local_a0)) << 0x10;
  *(undefined1 *)(param_1 + 5) = 1;
  sStack_a4 = sVar16;
  uStack_9c = uVar17;
  if (pvVar5 != (void *)0x0) {
    operator_delete(pvVar5);
  }
LAB_1013e7718:
  if (*(long *)PTR____stack_chk_guard_101b8c408 == local_70) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

