
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined1  [16] FUN_1011be6c8(double param_1,double param_2,double param_3,int param_4)

{
  undefined1 auVar1 [16];
  undefined1 auVar2 [16];
  ushort uVar3;
  
  param_1 = param_1 - param_3;
  if ((param_2 != 0.0) && (((param_4 == 2 || (param_4 == 1)) || (param_4 == 0)))) {
    param_1 = (double)(long)(param_1 / param_2) * param_2;
  }
  auVar1._0_8_ = param_1 + param_3;
  uVar3 = NEON_umaxv(CONCAT26(-(ushort)(auVar1._0_8_ == _UNK_1055d9698),
                              CONCAT24(-(ushort)(auVar1._0_8_ == _DAT_1055d9690),
                                       CONCAT22(-(ushort)(auVar1._0_8_ == _UNK_1055d9688),
                                                -(ushort)(auVar1._0_8_ == _DAT_1055d9680)))),2);
  if ((uVar3 & 1) != 0) {
    auVar1._8_8_ = 0;
    return auVar1;
  }
  uVar3 = 0x3ff0;
  if (auVar1._0_8_ < 0.0) {
    uVar3 = 0xbff0;
  }
  auVar2._0_8_ = (double)((ulong)uVar3 << 0x30) *
                 ((double)(long)(ABS(auVar1._0_8_ +
                                     (double)((ulong)uVar3 << 0x30) * 2.6015651015651016e-07 * 0.5)
                                * 3843840.0) / 3843840.0);
  auVar2._8_8_ = 0;
  return auVar2;
}

