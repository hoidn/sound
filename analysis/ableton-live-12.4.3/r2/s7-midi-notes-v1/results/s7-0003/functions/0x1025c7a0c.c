
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1025c7a0c(long param_1,double *param_2)

{
  double dVar1;
  double dVar2;
  double dVar3;
  ushort uVar4;
  double dVar5;
  double dVar6;
  
  dVar3 = *(double *)(param_1 + 8);
  uVar4 = NEON_umaxv(CONCAT26(-(ushort)(dVar3 == _UNK_1055d9698),
                              CONCAT24(-(ushort)(dVar3 == _DAT_1055d9690),
                                       CONCAT22(-(ushort)(dVar3 == _UNK_1055d9688),
                                                -(ushort)(dVar3 == _DAT_1055d9680)))),2);
  if ((uVar4 & 1) == 0) {
    uVar4 = 0x3ff0;
    if (dVar3 < 0.0) {
      uVar4 = 0xbff0;
    }
    dVar3 = (double)((ulong)uVar4 << 0x30) *
            ((double)(long)(ABS(dVar3 + (double)((ulong)uVar4 << 0x30) * 2.6015651015651016e-07 *
                                        0.5) * 3843840.0) / 3843840.0);
  }
  *(undefined4 *)(param_2 + 1) = *(undefined4 *)(param_1 + 0x10);
  dVar2 = *(double *)(param_1 + 0x20);
  dVar1 = *(double *)(param_1 + 0x18);
  dVar6 = *(double *)(param_1 + 0x30);
  dVar5 = *(double *)(param_1 + 0x28);
  *param_2 = dVar3;
  param_2[3] = dVar2;
  param_2[2] = dVar1;
  param_2[5] = dVar6;
  param_2[4] = dVar5;
  return;
}

