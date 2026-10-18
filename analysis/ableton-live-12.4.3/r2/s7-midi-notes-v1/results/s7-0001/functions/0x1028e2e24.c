
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1028e2e24(long param_1,double *param_2)

{
  double dVar1;
  double dVar2;
  double dVar3;
  double dVar4;
  double dVar5;
  ushort uVar6;
  
  dVar4 = *(double *)(param_1 + 0x30);
  param_2[1] = (double)&DAT_7fefffffffffffff;
  *(undefined1 *)((long)param_2 + 0x21) = 0;
  param_2[5] = dVar4;
  dVar3 = _UNK_1055d9698;
  dVar2 = _DAT_1055d9690;
  dVar1 = _UNK_1055d9688;
  dVar4 = _DAT_1055d9680;
  dVar5 = *(double *)(param_1 + 8);
  uVar6 = NEON_umaxv(CONCAT26(-(ushort)(dVar5 == _UNK_1055d9698),
                              CONCAT24(-(ushort)(dVar5 == _DAT_1055d9690),
                                       CONCAT22(-(ushort)(dVar5 == _UNK_1055d9688),
                                                -(ushort)(dVar5 == _DAT_1055d9680)))),2);
  if ((uVar6 & 1) == 0) {
    uVar6 = 0x3ff0;
    if (dVar5 < 0.0) {
      uVar6 = 0xbff0;
    }
    dVar5 = (double)((ulong)uVar6 << 0x30) *
            ((double)(long)(ABS(dVar5 + (double)((ulong)uVar6 << 0x30) * 2.6015651015651016e-07 *
                                        0.5) * 3843840.0) / 3843840.0);
  }
  *param_2 = dVar5;
  dVar5 = *(double *)(param_1 + 0x10);
  uVar6 = NEON_umaxv(CONCAT26(-(ushort)(dVar5 == dVar3),
                              CONCAT24(-(ushort)(dVar5 == dVar2),
                                       CONCAT22(-(ushort)(dVar5 == dVar1),-(ushort)(dVar5 == dVar4))
                                      )),2);
  if ((uVar6 & 1) != 0) {
    param_2[1] = dVar5;
    dVar4 = *(double *)(param_1 + 0x18);
    param_2[3] = *(double *)(param_1 + 0x20);
    param_2[2] = dVar4;
    *(undefined1 *)(param_2 + 4) = *(undefined1 *)(param_1 + 0x28);
    return;
  }
  uVar6 = 0x3ff0;
  if (dVar5 < 0.0) {
    uVar6 = 0xbff0;
  }
  param_2[1] = (double)((ulong)uVar6 << 0x30) *
               ((double)(long)(ABS(dVar5 + (double)((ulong)uVar6 << 0x30) * 2.6015651015651016e-07 *
                                           0.5) * 3843840.0) / 3843840.0);
  dVar4 = *(double *)(param_1 + 0x18);
  param_2[3] = *(double *)(param_1 + 0x20);
  param_2[2] = dVar4;
  *(undefined1 *)(param_2 + 4) = *(undefined1 *)(param_1 + 0x28);
  return;
}

