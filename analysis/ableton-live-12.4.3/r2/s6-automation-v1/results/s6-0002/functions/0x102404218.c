
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_102404218(float *param_1,double param_2,double param_3,undefined8 param_4,
                  undefined8 param_5,undefined8 param_6)

{
  undefined8 uVar1;
  undefined8 uVar2;
  float fVar3;
  undefined8 uVar4;
  long lVar5;
  double *pdVar6;
  undefined8 *puVar7;
  float fVar8;
  float fVar9;
  undefined8 uVar10;
  undefined2 uVar11;
  undefined2 uVar12;
  undefined2 uVar13;
  undefined2 uVar14;
  ushort uVar15;
  double dVar16;
  double dVar17;
  undefined8 local_160;
  undefined8 uStack_158;
  undefined8 uStack_150;
  undefined8 uStack_148;
  undefined8 local_140;
  undefined8 uStack_138;
  undefined8 uStack_130;
  undefined8 uStack_128;
  undefined1 auStack_120 [64];
  undefined8 local_e0;
  undefined8 uStack_d8;
  undefined8 uStack_d0;
  undefined8 uStack_c8;
  undefined8 local_c0;
  undefined8 uStack_b8;
  undefined8 uStack_b0;
  undefined8 uStack_a8;
  undefined1 auStack_a0 [64];
  
  uVar4 = _UNK_10587de28;
  uVar10 = _DAT_10587de20;
  uVar2 = _UNK_10587de18;
  uVar1 = _DAT_10587de10;
  uVar11 = (undefined2)_DAT_10587de20;
  uVar13 = (undefined2)((ulong)_DAT_10587de20 >> 0x10);
  *(undefined8 *)(param_1 + 4) = _UNK_10587de18;
  *(undefined8 *)(param_1 + 2) = uVar1;
  *(undefined8 *)(param_1 + 8) = uVar4;
  *(undefined8 *)(param_1 + 6) = uVar10;
  *(undefined8 *)(param_1 + 0xc) = uVar2;
  *(undefined8 *)(param_1 + 10) = uVar1;
  *(undefined8 *)(param_1 + 0x10) = uVar4;
  *(undefined8 *)(param_1 + 0xe) = uVar10;
  FUN_1025bb900(auStack_a0);
  lVar5 = FUN_1025bb5ac(auStack_a0);
  dVar16 = *(double *)(lVar5 + 8);
  lVar5 = FUN_1025bb5b0(auStack_a0);
  dVar17 = *(double *)(lVar5 + 8);
  FUN_102778d24(param_6);
  fVar8 = (float)FUN_101574d54();
  uVar12 = SUB42(fVar8,0);
  uVar14 = (short)((uint)fVar8 >> 0x10);
  fVar3 = (float)CONCAT22(uVar13,uVar11);
  if (dVar16 <= dVar17) {
    uVar12 = uVar11;
    uVar14 = uVar13;
    fVar3 = fVar8;
  }
  FUN_1024713e8(&local_e0,(double)fVar3,SUB82((double)(float)CONCAT22(uVar14,uVar12),0),auStack_a0);
  pdVar6 = (double *)FUN_1025bb5ac(&local_e0);
  dVar17 = *pdVar6;
  pdVar6 = (double *)FUN_1025bb5b0(&local_e0);
  dVar16 = *pdVar6;
  uVar15 = NEON_umaxv(CONCAT26(-(ushort)(dVar17 == _UNK_1055d9698),
                               CONCAT24(-(ushort)(dVar17 == _DAT_1055d9690),
                                        CONCAT22(-(ushort)(dVar17 == _UNK_1055d9688),
                                                 -(ushort)(dVar17 == _DAT_1055d9680)))),2);
  if ((uVar15 & 1) == 0) {
    uVar15 = 0x3ff0;
    if (dVar17 < 0.0) {
      uVar15 = 0xbff0;
    }
    dVar17 = (double)((ulong)uVar15 << 0x30) *
             ((double)(long)(ABS(dVar17 + (double)((ulong)uVar15 << 0x30) * 2.6015651015651016e-07 *
                                          0.5) * 3843840.0) / 3843840.0);
  }
  uVar15 = NEON_umaxv(CONCAT26(-(ushort)(dVar16 == _UNK_1055d9698),
                               CONCAT24(-(ushort)(dVar16 == _DAT_1055d9690),
                                        CONCAT22(-(ushort)(dVar16 == _UNK_1055d9688),
                                                 -(ushort)(dVar16 == _DAT_1055d9680)))),2);
  if ((uVar15 & 1) == 0) {
    uVar15 = 0x3ff0;
    if (dVar16 < 0.0) {
      uVar15 = 0xbff0;
    }
    dVar16 = (double)((ulong)uVar15 << 0x30) *
             ((double)(long)(ABS(dVar16 + (double)((ulong)uVar15 << 0x30) * 2.6015651015651016e-07 *
                                          0.5) * 3843840.0) / 3843840.0);
  }
  if ((param_2 < dVar17) || (dVar16 < param_2)) {
    if (dVar17 <= param_2) {
      lVar5 = FUN_1025bb5b0(&local_e0);
    }
    else {
      lVar5 = FUN_1025bb5ac();
    }
    fVar9 = (float)*(double *)(lVar5 + 8);
    fVar3 = (float)CONCAT22(uVar13,uVar11);
    if (fVar9 <= (float)CONCAT22(uVar13,uVar11)) {
      fVar3 = fVar9;
    }
    if (fVar8 <= fVar9) {
      fVar8 = fVar3;
    }
    *param_1 = fVar8;
  }
  else {
    if ((dVar17 <= param_3) && (param_3 <= dVar16)) {
      FUN_1025bba10(param_3,&local_e0);
      FUN_1025bba50(&local_160,&local_e0);
      uStack_d8 = uStack_158;
      local_e0 = local_160;
      uStack_c8 = uStack_148;
      uStack_d0 = uStack_150;
      uStack_b8 = uStack_138;
      local_c0 = local_140;
      uStack_a8 = uStack_128;
      uStack_b0 = uStack_130;
    }
    FUN_1025bba10(param_2,&local_e0);
    FUN_1025bba50(&local_160,&local_e0);
    lVar5 = FUN_1025bb5ac(auStack_120);
    fVar9 = (float)*(double *)(lVar5 + 8);
    fVar3 = (float)CONCAT22(uVar13,uVar11);
    if (fVar9 <= (float)CONCAT22(uVar13,uVar11)) {
      fVar3 = fVar9;
    }
    if (fVar8 <= fVar9) {
      fVar8 = fVar3;
    }
    *param_1 = fVar8;
    puVar7 = (undefined8 *)FUN_1025bb5b8(auStack_120);
    uVar10 = *puVar7;
    uVar2 = puVar7[3];
    uVar1 = puVar7[2];
    *(undefined8 *)(param_1 + 4) = puVar7[1];
    *(undefined8 *)(param_1 + 2) = uVar10;
    *(undefined8 *)(param_1 + 8) = uVar2;
    *(undefined8 *)(param_1 + 6) = uVar1;
    puVar7 = (undefined8 *)FUN_1025bb5b8(&local_160);
    uVar10 = *puVar7;
    uVar2 = puVar7[3];
    uVar1 = puVar7[2];
    *(undefined8 *)(param_1 + 0xc) = puVar7[1];
    *(undefined8 *)(param_1 + 10) = uVar10;
    *(undefined8 *)(param_1 + 0x10) = uVar2;
    *(undefined8 *)(param_1 + 0xe) = uVar1;
  }
  return;
}

