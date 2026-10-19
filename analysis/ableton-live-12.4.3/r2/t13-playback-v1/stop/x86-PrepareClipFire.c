// 0x101af9eb0 FUN_101af9eb0 state=exported-with-warnings body=[['0x101af9eb0', '0x101afab8c']]

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 *
FUN_101af9eb0(double param_1,undefined4 param_2,undefined4 param_3,undefined8 *param_4,long *param_5
             ,long param_6,ulong param_7,undefined4 param_8,int param_9,byte param_10,
             undefined4 *param_11)

{
  undefined1 auVar1 [16];
  undefined1 auVar2 [16];
  char cVar3;
  byte bVar4;
  undefined1 uVar5;
  undefined4 uVar6;
  undefined8 uVar7;
  long lVar8;
  undefined8 uVar9;
  long lVar10;
  long *plVar11;
  int iVar12;
  ulong uVar13;
  uint uVar14;
  long *plVar15;
  uint uVar16;
  int iVar17;
  bool bVar18;
  uint uVar19;
  undefined4 uVar20;
  undefined4 in_XMM0_Dc;
  undefined4 extraout_XMM0_Dc;
  undefined4 uVar21;
  undefined4 in_XMM0_Dd;
  undefined4 extraout_XMM0_Dd;
  undefined4 uVar22;
  double dVar23;
  undefined1 auVar24 [16];
  undefined1 auVar25 [16];
  undefined1 auVar26 [16];
  undefined4 local_200;
  undefined4 local_1fc;
  double local_1f8;
  undefined1 local_1f0;
  byte local_1ef;
  char local_1ee;
  undefined8 local_1e8;
  double local_1e0;
  double local_1d8;
  undefined8 local_1d0;
  undefined8 uStack_1c8;
  undefined8 uStack_1c0;
  undefined8 local_1b8;
  uint local_1b0;
  byte local_1ac;
  undefined4 local_1a8;
  undefined4 local_1a4;
  int local_1a0;
  undefined4 uStack_19c;
  undefined4 uStack_198;
  undefined4 uStack_194;
  undefined4 local_190;
  undefined4 uStack_18c;
  undefined4 uStack_188;
  undefined4 uStack_184;
  undefined8 local_180;
  long lStack_178;
  undefined1 local_170;
  undefined1 local_168 [24];
  undefined1 local_150;
  double dStack_140;
  undefined8 local_138;
  char local_130;
  long local_128;
  long local_120;
  double local_118 [2];
  undefined4 local_108;
  undefined4 uStack_104;
  undefined4 uStack_100;
  undefined4 uStack_fc;
  undefined8 local_f8;
  double dStack_f0;
  undefined8 local_e8;
  char local_e0;
  undefined4 local_d0;
  undefined4 local_cc;
  long local_c8;
  long *local_c0;
  double local_b8;
  undefined4 uStack_b0;
  undefined4 uStack_ac;
  undefined8 local_a8;
  ulong uStack_a0;
  undefined4 local_8c;
  double local_88;
  double local_80;
  undefined1 local_78 [16];
  uint local_5c;
  long *local_58;
  double local_50;
  byte local_41;
  double local_40;
  uint local_34;
  
  local_88 = (double)CONCAT44(local_88._4_4_,param_8);
  uVar13 = param_7;
  local_d0 = param_3;
  local_cc = param_2;
  local_b8 = param_1;
  uStack_b0 = in_XMM0_Dc;
  uStack_ac = in_XMM0_Dd;
  local_40 = (double)FUN_101b16120(param_11);
  uVar13 = uVar13 & 0xffffffffffffff00;
  if (param_9 == 1 && (int)param_7 < 0) goto LAB_101af9f11;
  local_50 = (double)CONCAT44(local_50._4_4_,(int)param_7);
  plVar11 = param_5 + 0x20;
  cVar3 = FUN_101b159b0();
  local_128 = param_6;
  if (cVar3 != '\0') {
    uVar6 = FUN_101b15cb0();
    if (-1 < local_50._0_4_) goto LAB_101afa022;
LAB_101af9ff8:
    bVar18 = false;
    local_34 = 0;
    local_8c = 0;
    local_a8 = (double)((ulong)local_a8 & 0xffffffff00000000);
    iVar17 = local_50._0_4_;
    bVar4 = (byte)uVar6;
    goto LAB_101afa1ff;
  }
  uVar6 = 0;
  if (local_50._0_4_ < 0) goto LAB_101af9ff8;
LAB_101afa022:
  local_80 = (double)CONCAT44(local_80._4_4_,uVar6);
  local_c8 = FUN_101b17140(*(undefined8 *)
                            (param_5[3] + 0xa0 + (ulong)*(byte *)(param_5[3] + 0xb0) * 8));
  if ((*(long *)(local_c8 + 0x50) == 0) || (*(int *)(local_c8 + 0x20) < 2)) {
    uVar14 = 4;
    if (*(char *)(local_c8 + 0x39) == '\0') goto LAB_101af9f11;
  }
  else {
    uVar14 = *(uint *)(*(long *)(local_c8 + 0x50) + 0x48);
    if (uVar14 == 5) goto LAB_101af9f11;
  }
  uVar19 = uVar14;
  if (SUB84(local_40,0) == 3) {
    uVar19 = 3;
  }
  bVar18 = false;
  if (SUB84(local_40,0) - 1U < 2) {
    uVar19 = 0;
  }
  uVar16 = uVar19;
  if (local_b8 != DAT_105b3ce00) {
    uVar16 = 0;
  }
  if (NAN(local_b8) || NAN(DAT_105b3ce00)) {
    uVar16 = 0;
  }
  if (uVar14 == 4) {
    uVar16 = uVar19;
  }
  plVar15 = plVar11;
  local_58 = param_5;
  cVar3 = FUN_101b159b0(plVar11);
  if (cVar3 != '\0') {
    iVar12 = FUN_101b15ca0(plVar11);
    bVar18 = iVar12 == local_50._0_4_;
    plVar15 = plVar11;
  }
  param_5 = local_58;
  iVar12 = *(int *)(local_58[3] + 0x70);
  iVar17 = local_50._0_4_;
  if (4 < uVar16) {
    bVar18 = false;
    local_34 = 0;
    local_a8 = (double)((ulong)local_a8._4_4_ << 0x20);
    goto LAB_101afa1b5;
  }
  switch(uVar16) {
  default:
    if (param_9 == 1) goto LAB_101af9f11;
    goto LAB_101afa156;
  case 1:
    if (param_9 == 1) {
      if (iVar12 != local_50._0_4_ && !bVar18) goto LAB_101afaa9a;
      goto LAB_101afa17a;
    }
LAB_101afa156:
    bVar18 = false;
    local_34 = 0;
    local_a8 = (double)((ulong)local_a8._4_4_ << 0x20);
    break;
  case 2:
    if (param_9 == 1) goto LAB_101afaa9a;
LAB_101afa17a:
    local_34 = (uint)CONCAT71((int7)((ulong)plVar15 >> 8),iVar12 == local_50._0_4_);
    local_a8 = (double)((ulong)local_a8._4_4_ << 0x20);
    break;
  case 3:
    if (param_9 == 1) {
      FUN_101afabc0(param_4);
      *(int *)((long)param_4 + 4) = iVar17;
      *(int *)param_4 = SUB84(local_40,0);
      goto LAB_101afa33c;
    }
    local_a8 = (double)CONCAT44(local_a8._4_4_,(int)CONCAT71((uint7)(uint3)((uint)iVar12 >> 8),1));
    bVar18 = false;
    local_34 = 0;
  }
LAB_101afa1b5:
  uVar9 = FUN_101b3d000(*(undefined8 *)(local_58[3] + 0x20));
  uVar7 = (**(code **)(*param_5 + 0x28))(param_5);
  lVar8 = FUN_101adcf20(uVar7);
  uVar13 = (ulong)*(byte *)(lVar8 + 0xa0);
  local_8c = FUN_101b6b1b0(uVar9,local_c8,param_10,uVar13,*(undefined1 *)(param_11 + 9));
  bVar4 = local_80._0_1_;
LAB_101afa1ff:
  uVar6 = (undefined4)CONCAT71((int7)(uVar13 >> 8),1);
  if (((SUB84(local_40,0) & 0xfffffffe) == 2) && (*(int *)(param_5[3] + 0x70) != iVar17)) {
    cVar3 = FUN_101b16130(param_11);
    if (cVar3 == '\0') goto LAB_101af9f11;
    uVar6 = 0;
  }
  local_41 = (byte)local_34 | bVar4;
  if (((~bVar18 | local_41) & 1) == 0) {
    param_4[1] = 0x7fefffffffffffff;
    *(undefined2 *)(param_4 + 2) = 0;
    *(undefined1 *)((long)param_4 + 0x12) = 0;
    uVar9 = CONCAT44(_UNK_105b84144,_DAT_105b84140);
    uVar7 = CONCAT44(_UNK_105b8414c,_UNK_105b84148);
    param_4[3] = uVar9;
    param_4[4] = uVar7;
    param_4[5] = uVar9;
    param_4[6] = uVar7;
    param_4[7] = 0;
    param_4[8] = 0;
    param_4[9] = 0x7fefffffffffffff;
    *(undefined4 *)(param_4 + 10) = 0;
    *(undefined1 *)((long)param_4 + 0x54) = 0;
    param_4[0xb] = DAT_105d82210;
    *(undefined4 *)(param_4 + 0xc) = 0;
    param_4[0xd] = uVar9;
    param_4[0xe] = uVar7;
    param_4[0xf] = 0x7fefffffffffffff;
    *(undefined4 *)(param_4 + 0x10) = 0x80000000;
    *(undefined1 *)((long)param_4 + 0x84) = 0;
    param_4[0x11] = 0;
    *(undefined1 *)(param_4 + 0x12) = 0;
    *(int *)((long)param_4 + 4) = local_50._0_4_;
    *(undefined4 *)param_4 = 0xffffffff;
LAB_101afa33c:
    *(undefined1 *)((long)param_4 + 0x53) = 1;
    *(undefined1 *)(param_4 + 10) = 1;
    return param_4;
  }
  local_c8 = CONCAT44(local_c8._4_4_,uVar6);
  lVar8 = param_5[3];
  iVar12 = *(int *)(lVar8 + 0x70);
  lVar8 = FUN_101b17140(*(undefined8 *)(lVar8 + 0xa0 + (ulong)*(byte *)(lVar8 + 0xb0) * 8),iVar12);
  local_80 = (double)CONCAT44(local_80._4_4_,iVar12);
  if ((iVar12 < 0) || (*(int *)(lVar8 + 0x20) < 2)) {
    local_58 = (long *)0x0;
  }
  else {
    local_58 = *(long **)(*(long *)(lVar8 + 0x40) + 8);
  }
  iVar12 = local_50._0_4_;
  if ((bVar18 & bVar4) != 0) {
    iVar12 = -2;
  }
  if ((char)local_34 != '\0') {
    iVar12 = -2;
  }
  auVar26 = FUN_101b17140(*(undefined8 *)
                           (param_5[3] + 0xa0 + (ulong)*(byte *)(param_5[3] + 0xb0) * 8),iVar12);
  lVar10 = auVar26._0_8_;
  local_50 = (double)CONCAT44(local_50._4_4_,iVar12);
  iVar17 = local_40._0_4_;
  if ((iVar12 < 0) || (*(int *)(lVar10 + 0x20) < 2)) {
    local_c0 = (long *)0x0;
  }
  else {
    local_c0 = *(long **)(*(long *)(lVar10 + 0x40) + 8);
  }
  if (((local_40._0_4_ == 1) && (local_c0 != local_58)) ||
     ((local_40._0_4_ != 0 && (local_c0 == (long *)0x0)))) {
LAB_101af9f11:
    param_4[2] = 0;
    param_4[3] = 0;
    param_4[4] = 0;
    param_4[5] = 0;
    param_4[6] = 0;
    param_4[7] = 0;
    param_4[8] = 0;
    param_4[9] = 0;
    param_4[10] = 0;
    param_4[0xb] = 0;
    param_4[0x10] = 0;
    param_4[0x11] = 0;
    param_4[0xe] = 0;
    param_4[0xf] = 0;
    param_4[0xc] = 0;
    param_4[0xd] = 0;
    param_4[0x12] = 0;
    *param_4 = 0x80000000ffffffff;
    param_4[1] = 0x7fefffffffffffff;
    *(undefined1 *)((long)param_4 + 0x11) = 0;
    uVar9 = CONCAT44(_UNK_105b84144,_DAT_105b84140);
    uVar7 = CONCAT44(_UNK_105b8414c,_UNK_105b84148);
    param_4[3] = uVar9;
    param_4[4] = uVar7;
    param_4[5] = uVar9;
    param_4[6] = uVar7;
    param_4[7] = 0;
    param_4[8] = 0;
    param_4[9] = 0x7fefffffffffffff;
    *(undefined4 *)(param_4 + 10) = 0;
    *(undefined1 *)((long)param_4 + 0x54) = 0;
    param_4[0xb] = DAT_105d82210;
    param_4[0xd] = uVar9;
    param_4[0xe] = uVar7;
    param_4[0xf] = 0x7fefffffffffffff;
    *(undefined4 *)(param_4 + 0x10) = 0x80000000;
    param_4[0x11] = 0;
    return param_4;
  }
  if (iVar12 == -2) {
    bVar4 = 1;
    local_5c = 0;
  }
  else {
    bVar4 = ((byte)local_8c ^ 1) & *(int *)(lVar10 + 0x20) < 2;
    local_5c = 0;
    if ((-1 < iVar12) && (1 < *(int *)(lVar10 + 0x20))) {
      local_5c = (uint)CONCAT71(auVar26._9_7_,
                                -1 < local_80._0_4_ & *(byte *)(*(long *)(lVar10 + 0x50) + 0x58) |
                                *(byte *)(param_11 + 9));
    }
  }
  uVar19 = (uint)-(ulong)(DAT_105b3ce00 == local_b8);
  local_78._8_8_ = 0;
  local_78._0_8_ = -(ulong)(DAT_105b3ce00 == local_b8);
  uVar14 = local_34 & 0xff;
  local_34 = CONCAT31(local_34._1_3_,bVar4);
  local_88 = (double)FUN_101af9d50(param_5,(ulong)local_88 & 0xff,(ulong)local_80 & 0xffffffff,lVar8
                                   ,lVar10,(ulong)local_40 & 0xffffffff,param_11[8],uVar19 & 1,bVar4
                                   ,uVar14);
  uVar6 = (undefined4)lVar8;
  dVar23 = local_88;
  if (iVar17 == 3) {
    dVar23 = *(double *)(param_11 + 4);
  }
  local_80 = 0.0;
  if ((local_5c & 1) == 0) {
    local_80 = dVar23;
  }
  if ((char)local_a8 == '\0') {
    local_80 = 0.0;
  }
  uVar9 = (**(code **)(*param_5 + 0x28))(param_5);
  local_120 = FUN_101adcf20(uVar9);
  local_a8 = *(double *)(local_120 + 0x70);
  uStack_a0 = 0;
  auVar26._4_4_ = -(uint)(local_a8 == _UNK_105b3eb18);
  auVar26._0_4_ = -(uint)(local_a8 == _DAT_105b3eb10);
  auVar26._8_4_ = -(uint)(_DAT_105b3eb00 == local_a8);
  auVar26._12_4_ = -(uint)(_UNK_105b3eb08 == local_a8);
  iVar12 = movmskps(uVar6,auVar26);
  if (iVar12 == 0) {
    auVar2._8_8_ = 0;
    auVar2._0_8_ = (double)((ulong)(DAT_105b3eac0 *
                                    *(double *)(&DAT_105b3eb20 + (ulong)(0.0 <= local_a8) * 8) *
                                    DAT_105a57808 + local_a8) & _DAT_105b35690) * DAT_105b3eac8;
    auVar26 = roundsd(ZEXT816(0),auVar2,9);
    uStack_a0 = auVar26._8_8_;
    local_a8 = (auVar26._0_8_ / DAT_105b3eac8) *
               *(double *)(&DAT_105b3eb20 + (ulong)(0.0 <= local_a8) * 8);
  }
  auVar24._0_8_ = ~local_78._0_8_ & (ulong)local_b8;
  auVar24._8_8_ = ~local_78._8_8_ & CONCAT44(uStack_ac,uStack_b0);
  auVar1._8_4_ = (int)(local_78._8_8_ & uStack_a0);
  auVar1._0_8_ = local_78._0_8_ & (ulong)local_a8;
  auVar1._12_4_ = (int)((local_78._8_8_ & uStack_a0) >> 0x20);
  auVar25 = auVar24 | auVar1;
  if (0.0 < local_88) {
    uVar9 = FUN_101ae8280(auVar25._0_4_,local_120 + 0x38,1);
    auVar25._12_4_ = extraout_XMM0_Dd;
    auVar25._8_4_ = extraout_XMM0_Dc;
    auVar25._0_8_ = uVar9;
  }
  local_1ef = local_40._0_4_ != 0 & (byte)local_c8;
  local_200 = 0xffffffff;
  local_1f0 = 0;
  uStack_1c8 = 0;
  uStack_1c0 = 0;
  local_1b8 = 0x7fefffffffffffff;
  local_1ac = local_41 & 1;
  local_1fc = local_50._0_4_;
  local_1f8 = local_80;
  local_1ee = (char)local_34;
  local_1e8 = 0;
  local_1e0 = auVar25._0_8_;
  local_1d0 = 1.79769313486232e+308;
  local_1b0 = (uint)CONCAT11(local_b8 != DAT_105b3ce00 & param_10,param_10) << 8;
  local_1a8 = local_cc;
  local_1a4 = local_d0;
  local_170 = *(undefined1 *)(param_11 + 0xc);
  local_1a0 = *param_11;
  uStack_19c = param_11[1];
  uStack_198 = param_11[2];
  uStack_194 = param_11[3];
  local_190 = param_11[4];
  uStack_18c = param_11[5];
  uStack_188 = param_11[6];
  uStack_184 = param_11[7];
  local_180 = *(undefined8 *)(param_11 + 8);
  lStack_178 = *(long *)(param_11 + 10);
  local_1d8 = local_1e0;
  local_78 = auVar25;
  local_1a0 = FUN_101b16120();
  lVar8 = local_128;
  if (local_1a0 == 1) {
    uStack_1c0 = CONCAT44(uStack_194,uStack_198);
  }
  if ((lStack_178 != 0) && (lVar10 = FUN_101abb210(), lVar10 != 0)) {
    local_1b8 = FUN_101b3d3a0(lVar10);
  }
  FUN_101afad10(local_168,&local_200,param_5[3]);
  if (local_130 == '\0') goto LAB_101afaa9a;
  if ((local_b8 != DAT_105b3ce00) || (NAN(local_b8) || NAN(DAT_105b3ce00))) {
LAB_101afa774:
    local_50 = (double)FUN_101afb500(param_5,local_58,local_c0,uVar19 & 1);
    if ((double)local_78._0_8_ - local_a8 < local_50) {
      local_b8 = (double)local_78._0_8_ - local_a8;
      cVar3 = FUN_101af9bb0(param_5);
      if (cVar3 == '\0') {
        uVar6 = SUB84(local_b8,0);
        uVar20 = (undefined4)((ulong)local_b8 >> 0x20);
        goto LAB_101afa7f4;
      }
      if ((local_88 != 0.0) || (NAN(local_88))) {
        local_78._0_8_ = (double)local_78._0_8_ + local_88;
      }
      else {
        local_50 = local_b8;
      }
    }
  }
  else {
    uVar9 = FUN_101b3d000(*(undefined8 *)(param_5[3] + 0x20));
    bVar4 = FUN_101b6ad80(uVar9);
    if (((bVar4 | (byte)local_8c) & 1) == 0) goto LAB_101afa774;
    uVar6 = 0;
    uVar20 = 0;
LAB_101afa7f4:
    local_50 = (double)CONCAT44(uVar20,uVar6);
  }
  if ((dStack_140 != DAT_105b3ce00) || (NAN(dStack_140) || NAN(DAT_105b3ce00))) {
    if ((lVar8 == 0) || (local_40._0_4_ == 0 && (char)local_5c == '\0')) goto LAB_101afa9b7;
    local_40 = dStack_140;
    plVar11 = (long *)FUN_101b17050(*(undefined8 *)
                                     (param_5[3] + 0xa0 + (ulong)*(byte *)(param_5[3] + 0xb0) * 8));
    cVar3 = (**(code **)(*plVar11 + 0x18))(plVar11);
    if (cVar3 != '\0') goto LAB_101afa9bc;
    FUN_101b164e0(SUB84(local_40,0),local_118,local_c0,local_168);
    FUN_101b16600(lVar8,local_118);
    FUN_101b157b0(local_118);
    cVar3 = FUN_101af9bb0(param_5);
    if (cVar3 != '\0') {
      uVar6 = local_78._0_4_;
      uVar20 = local_78._4_4_;
      uVar21 = local_78._8_4_;
      uVar22 = local_78._12_4_;
      if (((byte)local_5c & local_88 == 0.0) == 0) {
        FUN_101b168a0(lVar8,local_120);
        FUN_101afac80(local_118);
        if ((local_118[0] != local_78._0_8_) ||
           (uVar6 = local_78._0_4_, uVar20 = local_78._4_4_, uVar21 = local_78._8_4_,
           uVar22 = local_78._12_4_, NAN(local_118[0]) || NAN(local_78._0_8_))) {
          local_1d8 = local_118[0] - local_50;
          local_40 = local_118[0];
          local_1e0 = local_118[0];
          local_1d0 = (double)CONCAT44(_UNK_105b84144,_DAT_105b84140);
          uStack_1c8 = CONCAT44(_UNK_105b8414c,_UNK_105b84148);
          local_1b0 = local_1b0 & 0xffffff00;
          FUN_101afad10(local_118,&local_200,param_5[3]);
          if (local_130 == local_e0) {
            if (local_130 == '\0') {
LAB_101afaa9a:
              param_4[0x10] = 0;
              param_4[0x11] = 0;
              param_4[0xe] = 0;
              param_4[0xf] = 0;
              param_4[0xc] = 0;
              param_4[0xd] = 0;
              param_4[10] = 0;
              param_4[0xb] = 0;
              param_4[8] = 0;
              param_4[9] = 0;
              param_4[6] = 0;
              param_4[7] = 0;
              param_4[4] = 0;
              param_4[5] = 0;
              param_4[2] = 0;
              param_4[3] = 0;
              *param_4 = 0;
              param_4[1] = 0;
              param_4[0x12] = 0;
              FUN_101afabc0(param_4);
              return param_4;
            }
          }
          else {
            if (local_130 != '\0') {
              local_130 = '\0';
              goto LAB_101afaa9a;
            }
            local_130 = '\x01';
          }
          local_138 = local_e8;
          dStack_140 = dStack_f0;
          local_150 = (undefined1)uStack_100;
          FUN_101b164e0(SUB84(dStack_f0,0),local_118,local_c0,local_168);
          FUN_101b16600(lVar8,local_118);
          FUN_101b157b0(local_118);
          FUN_101b16890(SUB84(local_40,0),lVar8,local_120);
          uVar6 = SUB84(local_40,0);
          uVar20 = (int)((ulong)local_40 >> 0x20);
          uVar21 = 0;
          uVar22 = 0;
        }
      }
      goto LAB_101afaa0e;
    }
  }
  else {
LAB_101afa9b7:
    if (lVar8 != 0) {
LAB_101afa9bc:
      dStack_f0 = 0.0;
      local_118[0] = 0.0;
      local_118[1] = 0.0;
      local_108 = _DAT_105b84140;
      uStack_104 = _UNK_105b84144;
      uStack_100 = _UNK_105b84148;
      uStack_fc = _UNK_105b8414c;
      local_f8 = 0x7fefffffffffffff;
      local_e8 = 0x7fefffffffffffff;
      FUN_101b16600(lVar8,local_118);
      FUN_101b157b0(local_118);
    }
  }
  uVar6 = local_78._0_4_;
  uVar20 = local_78._4_4_;
  uVar21 = local_78._8_4_;
  uVar22 = local_78._12_4_;
LAB_101afaa0e:
  dVar23 = (double)CONCAT44(uVar20,uVar6) - local_50;
  if (dVar23 <= local_a8) {
    uVar5 = 1;
    if (local_1ee == '\0') {
      local_78._4_4_ = uVar20;
      local_78._0_4_ = uVar6;
      local_78._8_4_ = uVar21;
      local_78._12_4_ = uVar22;
      local_40 = dVar23;
      uVar5 = FUN_101af9bb0(param_5);
      uVar6 = local_78._0_4_;
      uVar20 = local_78._4_4_;
      dVar23 = local_40;
    }
  }
  else {
    uVar5 = 0;
  }
  local_1e0 = (double)CONCAT44(uVar20,uVar6);
  local_1d0 = dStack_140;
  uStack_1c8 = local_138;
  local_1b0 = CONCAT31(local_1b0._1_3_,uVar5);
  local_1d8 = dVar23;
  _memcpy(param_4,&local_200,0x98);
  return param_4;
}


