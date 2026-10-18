
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1026101b4(double param_1,long *param_2)

{
  ushort uVar1;
  
  uVar1 = NEON_umaxv(CONCAT26(-(ushort)(param_1 == _UNK_1055d9698),
                              CONCAT24(-(ushort)(param_1 == _DAT_1055d9690),
                                       CONCAT22(-(ushort)(param_1 == _UNK_1055d9688),
                                                -(ushort)(param_1 == _DAT_1055d9680)))),2);
  if ((uVar1 & 1) != 0) {
    param_2[0xb] = (long)param_1;
                    /* WARNING: Could not recover jumptable at 0x0001026101f4. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (**(code **)(*param_2 + 0x1b8))(param_2,1);
    return;
  }
  uVar1 = 0x3ff0;
  if (param_1 < 0.0) {
    uVar1 = 0xbff0;
  }
  param_2[0xb] = (long)((double)((ulong)uVar1 << 0x30) *
                       ((double)(long)(ABS(param_1 + (double)((ulong)uVar1 << 0x30) *
                                                     2.6015651015651016e-07 * 0.5) * 3843840.0) /
                       3843840.0));
                    /* WARNING: Could not recover jumptable at 0x000102610258. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (**(code **)(*param_2 + 0x1b8))(param_2,1);
  return;
}

