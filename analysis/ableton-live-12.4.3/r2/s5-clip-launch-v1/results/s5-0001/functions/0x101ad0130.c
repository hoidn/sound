
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_101ad0130(uint *param_1,double param_2,undefined4 param_3,undefined4 param_4,long *param_5,
                  long param_6,undefined8 param_7,undefined8 param_8,int param_9,undefined4 param_10
                  ,undefined8 *param_11)

{
  uint uVar1;
  uint uVar2;
  double dVar3;
  byte bVar4;
  bool bVar5;
  byte bVar6;
  byte bVar7;
  undefined1 uVar8;
  int iVar9;
  uint uVar10;
  ulong uVar11;
  undefined8 uVar12;
  long lVar13;
  ulong uVar14;
  long *plVar15;
  long lVar16;
  bool bVar17;
  long lVar18;
  byte bVar19;
  uint uVar20;
  int iVar21;
  bool bVar22;
  byte bVar23;
  uint uVar24;
  undefined2 extraout_h0;
  undefined2 uVar25;
  ushort uVar26;
  undefined2 extraout_h0_00;
  undefined2 extraout_h0_01;
  undefined2 extraout_h0_02;
  undefined2 extraout_var;
  undefined2 uVar27;
  undefined2 extraout_var_00;
  undefined2 extraout_var_01;
  undefined2 extraout_var_02;
  undefined2 extraout_var_03;
  undefined2 uVar28;
  undefined2 extraout_var_04;
  undefined2 extraout_var_05;
  undefined2 extraout_var_06;
  undefined2 extraout_var_07;
  undefined2 uVar29;
  undefined2 extraout_var_08;
  undefined2 extraout_var_09;
  undefined2 extraout_var_10;
  double dVar30;
  double dVar31;
  double dVar32;
  double dVar33;
  long local_1f0;
  double local_1c0;
  undefined8 uStack_1b8;
  undefined1 *local_1b0;
  undefined1 *puStack_1a8;
  undefined1 *local_1a0;
  double dStack_198;
  undefined1 *local_190;
  byte local_188;
  undefined1 local_180 [24];
  undefined1 local_168;
  double dStack_158;
  undefined1 *local_150;
  byte local_148;
  undefined4 local_138;
  uint uStack_134;
  undefined8 uStack_130;
  undefined1 local_128;
  undefined1 local_127;
  byte local_126;
  undefined5 uStack_125;
  undefined8 local_120;
  double local_118;
  double dStack_110;
  undefined1 *local_108;
  undefined1 *puStack_100;
  undefined8 local_f8;
  undefined1 *puStack_f0;
  undefined1 local_e8;
  undefined1 uStack_e7;
  undefined1 uStack_e6;
  undefined1 uStack_e5;
  uint local_e4;
  undefined4 local_e0;
  undefined4 local_dc;
  undefined8 local_d8;
  undefined8 uStack_d0;
  undefined8 uStack_c8;
  undefined8 uStack_c0;
  undefined8 local_b8;
  long lStack_b0;
  undefined1 local_a8;
  undefined7 uStack_a7;
  
  uVar11 = FUN_101aea470(param_11);
  uVar24 = (uint)param_7;
  if (((int)uVar24 < 0) && (param_9 == 1)) goto LAB_101ad01a0;
  iVar9 = FUN_101ae9cc4(param_5 + 0x20);
  uVar20 = (uint)uVar11;
  if (iVar9 == 0) {
    bVar6 = 0;
    if ((int)uVar24 < 0) goto LAB_101ad0250;
LAB_101ad0278:
    lVar13 = 0xa8;
    if (*(char *)(param_5[3] + 0xb0) == '\0') {
      lVar13 = 0xa0;
    }
    lVar13 = FUN_101aeb300(*(undefined8 *)(param_5[3] + lVar13),param_7);
    if ((*(long *)(lVar13 + 0x50) == 0) || (*(int *)(lVar13 + 0x20) < 2)) {
      if ((*(byte *)(lVar13 + 0x39) & 1) == 0) goto LAB_101ad01a0;
      uVar10 = 4;
    }
    else {
      uVar10 = *(uint *)(*(long *)(lVar13 + 0x50) + 0x48);
      if (uVar10 == 5) goto LAB_101ad01a0;
    }
    uVar1 = uVar20;
    if (uVar20 != 3) {
      uVar1 = uVar10;
    }
    uVar2 = 0;
    if ((param_2 == 1.79769313486232e+308 || uVar10 == 4) && 1 < uVar20 - 1) {
      uVar2 = uVar1;
    }
    iVar9 = FUN_101ae9cc4(param_5 + 0x20);
    bVar5 = false;
    if (iVar9 != 0) {
      uVar10 = FUN_101aea014(param_5 + 0x20);
      bVar5 = uVar10 == uVar24;
    }
    bVar22 = false;
    uVar10 = *(uint *)(param_5[3] + 0x70);
    if ((int)uVar2 < 2) {
      if (uVar2 == 0) {
LAB_101ad03d4:
        if (param_9 == 1) goto LAB_101ad01a0;
      }
      else {
        bVar17 = false;
        bVar4 = 0;
        if (uVar2 != 1) goto LAB_101ad0438;
        if (param_9 == 1) {
          if (uVar10 != uVar24 && bVar5 == false) goto LAB_101ad0388;
          goto LAB_101ad03f4;
        }
      }
      bVar4 = 0;
      bVar22 = false;
      bVar17 = false;
    }
    else if (uVar2 == 2) {
      if (param_9 == 1) {
LAB_101ad0388:
        param_1[0x24] = 0;
        param_1[0x25] = 0;
        param_1[0x1e] = 0;
        param_1[0x1f] = 0;
        param_1[0x1c] = 0;
        param_1[0x1d] = 0;
        param_1[0x22] = 0;
        param_1[0x23] = 0;
        param_1[0x20] = 0;
        param_1[0x21] = 0;
        param_1[0x16] = 0;
        param_1[0x17] = 0;
        param_1[0x14] = 0;
        param_1[0x15] = 0;
        param_1[0x1a] = 0;
        param_1[0x1b] = 0;
        param_1[0x18] = 0;
        param_1[0x19] = 0;
        param_1[0xe] = 0;
        param_1[0xf] = 0;
        param_1[0xc] = 0;
        param_1[0xd] = 0;
        param_1[0x12] = 0;
        param_1[0x13] = 0;
        param_1[0x10] = 0;
        param_1[0x11] = 0;
        param_1[6] = 0;
        param_1[7] = 0;
        param_1[4] = 0;
        param_1[5] = 0;
        param_1[10] = 0;
        param_1[0xb] = 0;
        param_1[8] = 0;
        param_1[9] = 0;
        param_1[2] = 0;
        param_1[3] = 0;
        param_1[0] = 0;
        param_1[1] = 0;
        FUN_101ad0bec(param_1);
        return;
      }
LAB_101ad03f4:
      bVar4 = 0;
      bVar22 = bVar5;
      bVar17 = uVar10 == uVar24;
    }
    else if (uVar2 == 3) {
      if (param_9 == 1) {
        FUN_101ad0bec(param_1);
        *param_1 = uVar20;
        param_1[1] = uVar24;
        *(undefined1 *)((long)param_1 + 0x53) = 1;
        *(undefined1 *)(param_1 + 0x14) = 1;
        return;
      }
      bVar4 = 1;
      bVar22 = false;
      bVar17 = false;
    }
    else {
      bVar17 = false;
      bVar4 = 0;
      if (uVar2 == 4) goto LAB_101ad03d4;
    }
LAB_101ad0438:
    uVar12 = FUN_101b0cf84(*(undefined8 *)(param_5[3] + 0x20));
    (**(code **)(*param_5 + 0x28))(param_5);
    lVar16 = FUN_101ab4558();
    bVar7 = FUN_101b35b00(uVar12,lVar13,param_10,*(undefined1 *)(lVar16 + 0xa0),
                          *(undefined1 *)((long)param_11 + 0x24));
    bVar23 = bVar7;
    if ((uVar20 & 0xfffffffe) == 2) goto LAB_101ad0490;
LAB_101ad04a0:
    uVar8 = 1;
    bVar23 = bVar17 | bVar22 ^ 0xffU | bVar6;
  }
  else {
    bVar6 = FUN_101aea01c(param_5 + 0x20);
    if (-1 < (int)uVar24) goto LAB_101ad0278;
LAB_101ad0250:
    bVar22 = false;
    bVar17 = false;
    bVar7 = 0;
    bVar4 = 0;
    bVar23 = 0;
    if ((uVar20 & 0xfffffffe) != 2) goto LAB_101ad04a0;
LAB_101ad0490:
    bVar7 = bVar23;
    if (*(uint *)(param_5[3] + 0x70) == uVar24) goto LAB_101ad04a0;
    uVar14 = FUN_101aea47c(param_11);
    if ((uVar14 & 1) == 0) goto LAB_101ad01a0;
    uVar8 = 0;
    uVar11 = uVar11 & 0xffffffff;
    bVar23 = bVar17 | bVar22 ^ 0xffU | bVar6;
  }
  if ((bVar23 & 1) == 0) {
    *(undefined1 **)(param_1 + 2) = &DAT_7fefffffffffffff;
    *(undefined2 *)(param_1 + 4) = 0;
    *(undefined1 *)((long)param_1 + 0x12) = 0;
    *(undefined1 **)(param_1 + 8) = &DAT_7fefffffffffffff;
    *(undefined1 **)(param_1 + 6) = &DAT_7fefffffffffffff;
    *(undefined1 **)(param_1 + 0xc) = &DAT_7fefffffffffffff;
    *(undefined1 **)(param_1 + 10) = &DAT_7fefffffffffffff;
    param_1[0xe] = 0;
    param_1[0xf] = 0;
    param_1[0x10] = 0;
    param_1[0x11] = 0;
    *(undefined1 **)(param_1 + 0x12) = &DAT_7fefffffffffffff;
    param_1[0x14] = 0;
    *(undefined1 *)(param_1 + 0x15) = 0;
    param_1[0x16] = 0x7f7fffff;
    param_1[0x17] = 0x7f7fffff;
    param_1[0x18] = 0;
    *(undefined1 **)(param_1 + 0x1c) = &DAT_7fefffffffffffff;
    *(undefined1 **)(param_1 + 0x1a) = &DAT_7fefffffffffffff;
    *(undefined1 **)(param_1 + 0x1e) = &DAT_7fefffffffffffff;
    param_1[0x20] = 0x80000000;
    *(undefined1 *)(param_1 + 0x21) = 0;
    param_1[0x22] = 0;
    param_1[0x23] = 0;
    *(undefined1 *)(param_1 + 0x24) = 0;
    *param_1 = 0xffffffff;
    param_1[1] = uVar24;
    *(undefined1 *)((long)param_1 + 0x53) = 1;
    *(undefined1 *)(param_1 + 0x14) = 1;
    return;
  }
  lVar16 = param_5[3];
  iVar9 = *(int *)(lVar16 + 0x70);
  lVar13 = 0xa8;
  if (*(char *)(lVar16 + 0xb0) == '\0') {
    lVar13 = 0xa0;
  }
  lVar13 = FUN_101aeb300(*(undefined8 *)(lVar16 + lVar13),iVar9);
  if ((iVar9 < 0) || (*(int *)(lVar13 + 0x20) < 2)) {
    local_1f0 = 0;
  }
  else {
    local_1f0 = *(long *)(*(long *)(lVar13 + 0x40) + 8);
  }
  uVar20 = 0xfffffffe;
  if (bVar17 == false && (bVar22 & bVar6) == 0) {
    uVar20 = uVar24;
  }
  lVar16 = 0xa8;
  if (*(char *)(param_5[3] + 0xb0) == '\0') {
    lVar16 = 0xa0;
  }
  lVar16 = FUN_101aeb300(*(undefined8 *)(param_5[3] + lVar16),uVar20);
  iVar21 = (int)uVar11;
  if (((int)uVar20 < 0) || (*(int *)(lVar16 + 0x20) < 2)) {
    lVar18 = 0;
  }
  else {
    lVar18 = *(long *)(*(long *)(lVar16 + 0x40) + 8);
  }
  if (((iVar21 == 1) && (lVar18 != local_1f0)) || ((iVar21 != 0 && (lVar18 == 0)))) {
LAB_101ad01a0:
    param_1[6] = 0;
    param_1[7] = 0;
    param_1[4] = 0;
    param_1[5] = 0;
    param_1[10] = 0;
    param_1[0xb] = 0;
    param_1[8] = 0;
    param_1[9] = 0;
    param_1[0xe] = 0;
    param_1[0xf] = 0;
    param_1[0xc] = 0;
    param_1[0xd] = 0;
    param_1[0x12] = 0;
    param_1[0x13] = 0;
    param_1[0x10] = 0;
    param_1[0x11] = 0;
    param_1[0x1e] = 0;
    param_1[0x1f] = 0;
    param_1[0x1c] = 0;
    param_1[0x1d] = 0;
    param_1[0x22] = 0;
    param_1[0x23] = 0;
    param_1[0x20] = 0;
    param_1[0x21] = 0;
    param_1[0x16] = 0;
    param_1[0x17] = 0;
    param_1[0x14] = 0;
    param_1[0x15] = 0;
    param_1[0x1a] = 0;
    param_1[0x1b] = 0;
    param_1[0x18] = 0;
    param_1[0x19] = 0;
    param_1[0] = 0xffffffff;
    param_1[1] = 0x80000000;
    *(undefined1 **)(param_1 + 2) = &DAT_7fefffffffffffff;
    *(undefined1 *)((long)param_1 + 0x11) = 0;
    *(undefined1 **)(param_1 + 8) = &DAT_7fefffffffffffff;
    *(undefined1 **)(param_1 + 6) = &DAT_7fefffffffffffff;
    *(undefined1 **)(param_1 + 0xc) = &DAT_7fefffffffffffff;
    *(undefined1 **)(param_1 + 10) = &DAT_7fefffffffffffff;
    param_1[0xe] = 0;
    param_1[0xf] = 0;
    param_1[0x10] = 0;
    param_1[0x11] = 0;
    *(undefined1 **)(param_1 + 0x12) = &DAT_7fefffffffffffff;
    param_1[0x14] = 0;
    *(undefined1 *)(param_1 + 0x15) = 0;
    param_1[0x16] = 0x7f7fffff;
    param_1[0x17] = 0x7f7fffff;
    *(undefined1 **)(param_1 + 0x1c) = &DAT_7fefffffffffffff;
    *(undefined1 **)(param_1 + 0x1a) = &DAT_7fefffffffffffff;
    *(undefined1 **)(param_1 + 0x1e) = &DAT_7fefffffffffffff;
    param_1[0x20] = 0x80000000;
    param_1[0x22] = 0;
    param_1[0x23] = 0;
    param_1[0x24] = 0;
    param_1[0x25] = 0;
    return;
  }
  bVar23 = 0;
  if (uVar20 == 0xfffffffe) {
    bVar19 = 1;
  }
  else {
    bVar19 = *(int *)(lVar16 + 0x20) < 2 & (bVar7 ^ 1);
    if ((-1 < (int)uVar20) && (1 < *(int *)(lVar16 + 0x20))) {
      bVar23 = -1 < iVar9 & *(byte *)(*(long *)(lVar16 + 0x50) + 0x58) |
               *(byte *)((long)param_11 + 0x24);
    }
  }
  FUN_101acffa4(param_5,param_8,iVar9,lVar13,lVar16,uVar11,*(undefined4 *)(param_11 + 4),
                param_2 == 1.79769313486232e+308,bVar19);
  dVar3 = (double)CONCAT26(extraout_var_07,
                           CONCAT24(extraout_var_03,CONCAT22(extraout_var,extraout_h0)));
  uVar12 = param_11[2];
  uVar25 = (undefined2)uVar12;
  uVar27 = (undefined2)((ulong)uVar12 >> 0x10);
  uVar28 = (undefined2)((ulong)uVar12 >> 0x20);
  uVar29 = (undefined2)((ulong)uVar12 >> 0x30);
  if (iVar21 != 3) {
    uVar25 = extraout_h0;
    uVar27 = extraout_var;
    uVar28 = extraout_var_03;
    uVar29 = extraout_var_07;
  }
  uVar12 = 0;
  if (((bVar23 | bVar4 ^ 0xff) & 1) == 0) {
    uVar12 = CONCAT26(uVar29,CONCAT24(uVar28,CONCAT22(uVar27,uVar25)));
  }
  (**(code **)(*param_5 + 0x28))(param_5);
  lVar13 = FUN_101ab4558();
  dVar30 = *(double *)(lVar13 + 0x70);
  uVar26 = NEON_umaxv(CONCAT26(-(ushort)(dVar30 == _UNK_1055d9698),
                               CONCAT24(-(ushort)(dVar30 == _DAT_1055d9690),
                                        CONCAT22(-(ushort)(dVar30 == _UNK_1055d9688),
                                                 -(ushort)(dVar30 == _DAT_1055d9680)))),2);
  if ((uVar26 & 1) == 0) {
    uVar26 = 0x3ff0;
    if (dVar30 < 0.0) {
      uVar26 = 0xbff0;
    }
    dVar30 = (double)((ulong)uVar26 << 0x30) *
             ((double)(long)(ABS(dVar30 + (double)((ulong)uVar26 << 0x30) * 2.6015651015651016e-07 *
                                          0.5) * 3843840.0) / 3843840.0);
  }
  dVar32 = dVar30;
  if (param_2 != 1.79769313486232e+308) {
    dVar32 = param_2;
  }
  if (0.0 < dVar3) {
    FUN_101abf294(SUB82(dVar32,0),dVar3,lVar13 + 0x38,1);
    dVar32 = (double)CONCAT26(extraout_var_08,
                              CONCAT24(extraout_var_04,CONCAT22(extraout_var_00,extraout_h0_00)));
  }
  local_128 = 0;
  local_127 = 0;
  if (iVar21 != 0) {
    local_127 = uVar8;
  }
  local_f8 = 0;
  puStack_f0 = &DAT_7fefffffffffffff;
  local_e8 = 0;
  uStack_e5 = 0;
  uStack_e7 = (undefined1)param_10;
  uStack_e6 = 0;
  if (param_2 != 1.79769313486232e+308) {
    uStack_e6 = uStack_e7;
  }
  local_138 = 0xffffffff;
  local_e4 = CONCAT31(local_e4._1_3_,bVar17 | bVar6) & 0xffffff01;
  local_120 = 0;
  local_108 = &DAT_7fefffffffffffff;
  puStack_100 = (undefined1 *)0x0;
  uStack_d0 = param_11[1];
  local_d8 = *param_11;
  uStack_c0 = param_11[3];
  uStack_c8 = param_11[2];
  lStack_b0 = param_11[5];
  local_b8 = param_11[4];
  local_a8 = *(undefined1 *)(param_11 + 6);
  uStack_134 = uVar20;
  uStack_130 = uVar12;
  local_126 = bVar19;
  local_118 = dVar32;
  dStack_110 = dVar32;
  local_e0 = param_3;
  local_dc = param_4;
  iVar9 = FUN_101aea470(param_11);
  local_d8 = CONCAT44(local_d8._4_4_,iVar9);
  if (iVar9 == 1) {
    local_f8 = uStack_d0;
  }
  if ((lStack_b0 != 0) && (lVar16 = FUN_101a94314(), lVar16 != 0)) {
    FUN_101b0d344();
    puStack_f0 = (undefined1 *)
                 CONCAT26(extraout_var_09,
                          CONCAT24(extraout_var_05,CONCAT22(extraout_var_01,extraout_h0_01)));
  }
  FUN_101ad0d08(local_180,&local_138,param_5[3]);
  if ((local_148 & 1) == 0) goto LAB_101ad0ab0;
  dVar33 = dVar32;
  if (param_2 == 1.79769313486232e+308) {
    FUN_101b0cf84(*(undefined8 *)(param_5[3] + 0x20));
    bVar6 = FUN_101b357a0();
    dVar31 = 0.0;
    if (((bVar6 | bVar7) & 1) == 0) goto LAB_101ad08d4;
  }
  else {
LAB_101ad08d4:
    FUN_101ad1418(param_5,local_1f0,lVar18,param_2 == 1.79769313486232e+308);
    dVar31 = (double)CONCAT26(extraout_var_10,
                              CONCAT24(extraout_var_06,CONCAT22(extraout_var_02,extraout_h0_02)));
    if (dVar32 - dVar30 < dVar31) {
      bVar6 = FUN_101acfe68(param_5);
      dVar33 = dVar3 + dVar32;
      if ((bVar6 & dVar3 != 0.0) == 0) {
        dVar31 = dVar32 - dVar30;
        dVar33 = dVar32;
      }
    }
  }
  dVar32 = dStack_158;
  if (((dStack_158 == 1.79769313486232e+308) || (param_6 == 0)) ||
     ((bVar23 & 1) == 0 && iVar21 == 0)) {
    if (param_6 == 0) goto joined_r0x000101ad0a9c;
  }
  else {
    lVar16 = 0xa8;
    if (*(char *)(param_5[3] + 0xb0) == '\0') {
      lVar16 = 0xa0;
    }
    plVar15 = (long *)FUN_101aeb218(*(undefined8 *)(param_5[3] + lVar16));
    uVar11 = (**(code **)(*plVar15 + 0x18))();
    if ((uVar11 & 1) == 0) {
      FUN_101aea7b0(SUB82(dVar32,0),&local_1c0,lVar18,local_180);
      FUN_101aea898(param_6,&local_1c0);
      FUN_101ae9a84(&local_1c0);
      iVar9 = FUN_101acfe68(param_5);
      if ((iVar9 != 0) && ((bVar23 & dVar3 == 0.0) == 0)) {
        FUN_101aeab54(SUB82(dVar33,0),dVar3,param_6,lVar13);
        FUN_101ad0c78(&local_1c0);
        dVar3 = local_1c0;
        if (local_1c0 != dVar33) {
          dStack_110 = local_1c0 - dVar31;
          local_118 = local_1c0;
          puStack_100 = &DAT_7fefffffffffffff;
          local_108 = &DAT_7fefffffffffffff;
          local_e8 = 0;
          FUN_101ad0d08(&local_1c0,&local_138,param_5[3]);
          if (local_148 == local_188) {
            if (local_148 == 0) {
LAB_101ad0ab0:
              param_1[0x24] = 0;
              param_1[0x25] = 0;
              param_1[0x1e] = 0;
              param_1[0x1f] = 0;
              param_1[0x1c] = 0;
              param_1[0x1d] = 0;
              param_1[0x22] = 0;
              param_1[0x23] = 0;
              param_1[0x20] = 0;
              param_1[0x21] = 0;
              param_1[0x16] = 0;
              param_1[0x17] = 0;
              param_1[0x14] = 0;
              param_1[0x15] = 0;
              param_1[0x1a] = 0;
              param_1[0x1b] = 0;
              param_1[0x18] = 0;
              param_1[0x19] = 0;
              param_1[0xe] = 0;
              param_1[0xf] = 0;
              param_1[0xc] = 0;
              param_1[0xd] = 0;
              param_1[0x12] = 0;
              param_1[0x13] = 0;
              param_1[0x10] = 0;
              param_1[0x11] = 0;
              param_1[6] = 0;
              param_1[7] = 0;
              param_1[4] = 0;
              param_1[5] = 0;
              param_1[10] = 0;
              param_1[0xb] = 0;
              param_1[8] = 0;
              param_1[9] = 0;
              param_1[2] = 0;
              param_1[3] = 0;
              param_1[0] = 0;
              param_1[1] = 0;
              FUN_101ad0bec(param_1);
              return;
            }
          }
          else {
            if (local_148 != 0) {
              local_148 = 0;
              goto LAB_101ad0ab0;
            }
            local_148 = 1;
          }
          local_150 = local_190;
          dStack_158 = dStack_198;
          local_168 = puStack_1a8._0_1_;
          FUN_101aea7b0(SUB82(dStack_198,0),&local_1c0,lVar18,local_180);
          FUN_101aea898(param_6,&local_1c0);
          FUN_101ae9a84(&local_1c0);
          FUN_101aeab50(SUB82(dVar3,0),param_6,lVar13);
          dVar33 = dVar3;
        }
      }
      goto joined_r0x000101ad0a9c;
    }
  }
  uStack_1b8 = 0;
  local_1c0 = 0.0;
  puStack_1a8 = &DAT_7fefffffffffffff;
  local_1b0 = &DAT_7fefffffffffffff;
  dStack_198 = 0.0;
  local_1a0 = &DAT_7fefffffffffffff;
  local_190 = &DAT_7fefffffffffffff;
  FUN_101aea898(param_6,&local_1c0);
  FUN_101ae9a84(&local_1c0);
joined_r0x000101ad0a9c:
  if (dVar30 < dVar33 - dVar31) {
    uVar8 = 0;
  }
  else if ((local_126 & 1) == 0) {
    uVar8 = FUN_101acfe68(param_5);
  }
  else {
    uVar8 = 1;
  }
  *(undefined8 *)(param_1 + 0x1a) = uStack_d0;
  *(undefined8 *)(param_1 + 0x18) = local_d8;
  *(undefined8 *)(param_1 + 0x1e) = uStack_c0;
  *(undefined8 *)(param_1 + 0x1c) = uStack_c8;
  *(long *)(param_1 + 0x22) = lStack_b0;
  *(undefined8 *)(param_1 + 0x20) = local_b8;
  *(ulong *)(param_1 + 0x24) = CONCAT71(uStack_a7,local_a8);
  *(undefined8 *)(param_1 + 2) = uStack_130;
  *(ulong *)param_1 = CONCAT44(uStack_134,local_138);
  *(undefined8 *)(param_1 + 6) = local_120;
  *(ulong *)(param_1 + 4) = CONCAT53(uStack_125,CONCAT12(local_126,CONCAT11(local_127,local_128)));
  *(double *)(param_1 + 10) = dVar33 - dVar31;
  *(double *)(param_1 + 8) = dVar33;
  *(undefined1 **)(param_1 + 0xe) = local_150;
  *(double *)(param_1 + 0xc) = dStack_158;
  *(undefined1 **)(param_1 + 0x12) = puStack_f0;
  *(undefined8 *)(param_1 + 0x10) = local_f8;
  *(ulong *)(param_1 + 0x16) = CONCAT44(local_dc,local_e0);
  *(ulong *)(param_1 + 0x14) =
       CONCAT44(local_e4,CONCAT13(uStack_e5,CONCAT12(uStack_e6,CONCAT11(uStack_e7,uVar8))));
  return;
}

