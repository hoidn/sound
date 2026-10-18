
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined1  [16] FUN_101aaae44(int *param_1,undefined4 param_2)

{
  double dVar1;
  undefined1 auVar2 [16];
  undefined1 auVar3 [16];
  undefined1 auVar4 [16];
  undefined1 auVar5 [16];
  undefined1 auVar6 [16];
  ushort uVar7;
  undefined2 uVar8;
  undefined2 uVar9;
  undefined2 uVar10;
  undefined2 uVar11;
  
  switch(param_2) {
  case 1:
    dVar1 = ((double)(long)*param_1 / (double)CONCAT26(param_1[1] >> 0x1f,(int6)param_1[1])) * 4.0;
    uVar7 = NEON_umaxv(CONCAT26(-(ushort)(dVar1 == _UNK_1055d9698),
                                CONCAT24(-(ushort)(dVar1 == _DAT_1055d9690),
                                         CONCAT22(-(ushort)(dVar1 == _UNK_1055d9688),
                                                  -(ushort)(dVar1 == _DAT_1055d9680)))),2);
    if ((uVar7 & 1) == 0) {
      uVar7 = 0x3ff0;
      if (dVar1 < 0.0) {
        uVar7 = 0xbff0;
      }
      dVar1 = (double)((ulong)uVar7 << 0x30) *
              ((double)(long)(ABS(dVar1 + (double)((ulong)uVar7 << 0x30) * 2.6015651015651016e-07 *
                                          0.5) * 3843840.0) / 3843840.0);
    }
    auVar2._0_8_ = dVar1 * 8.0;
    auVar2._8_8_ = 0;
    return auVar2;
  case 2:
    dVar1 = ((double)(long)*param_1 / (double)CONCAT26(param_1[1] >> 0x1f,(int6)param_1[1])) * 4.0;
    uVar8 = SUB82(dVar1,0);
    uVar9 = (undefined2)((ulong)dVar1 >> 0x10);
    uVar10 = (undefined2)((ulong)dVar1 >> 0x20);
    uVar11 = (undefined2)((ulong)dVar1 >> 0x30);
    uVar7 = NEON_umaxv(CONCAT26(-(ushort)(dVar1 == _UNK_1055d9698),
                                CONCAT24(-(ushort)(dVar1 == _DAT_1055d9690),
                                         CONCAT22(-(ushort)(dVar1 == _UNK_1055d9688),
                                                  -(ushort)(dVar1 == _DAT_1055d9680)))),2);
    if ((uVar7 & 1) == 0) {
      uVar7 = 0x3ff0;
      if (dVar1 < 0.0) {
        uVar7 = 0xbff0;
      }
      dVar1 = (double)((ulong)uVar7 << 0x30) *
              ((double)(long)(ABS(dVar1 + (double)((ulong)uVar7 << 0x30) * 2.6015651015651016e-07 *
                                          0.5) * 3843840.0) / 3843840.0);
      uVar8 = SUB82(dVar1,0);
      uVar9 = (undefined2)((ulong)dVar1 >> 0x10);
      uVar10 = (undefined2)((ulong)dVar1 >> 0x20);
      uVar11 = (undefined2)((ulong)dVar1 >> 0x30);
    }
    auVar5._0_8_ = (double)CONCAT26(uVar11,CONCAT24(uVar10,CONCAT22(uVar9,uVar8))) * 4.0;
    auVar5._8_8_ = 0;
    return auVar5;
  case 3:
    dVar1 = ((double)(long)*param_1 / (double)CONCAT26(param_1[1] >> 0x1f,(int6)param_1[1])) * 4.0;
    uVar7 = NEON_umaxv(CONCAT26(-(ushort)(dVar1 == _UNK_1055d9698),
                                CONCAT24(-(ushort)(dVar1 == _DAT_1055d9690),
                                         CONCAT22(-(ushort)(dVar1 == _UNK_1055d9688),
                                                  -(ushort)(dVar1 == _DAT_1055d9680)))),2);
    if ((uVar7 & 1) == 0) {
      uVar7 = 0x3ff0;
      if (dVar1 < 0.0) {
        uVar7 = 0xbff0;
      }
      dVar1 = (double)((ulong)uVar7 << 0x30) *
              ((double)(long)(ABS(dVar1 + (double)((ulong)uVar7 << 0x30) * 2.6015651015651016e-07 *
                                          0.5) * 3843840.0) / 3843840.0);
    }
    auVar3._0_8_ = dVar1 + dVar1;
    auVar3._8_8_ = 0;
    return auVar3;
  case 4:
    break;
  case 5:
    return ZEXT816(0x4000000000000000);
  case 6:
    return ZEXT816(0x3ff5555555555555);
  case 7:
    return ZEXT816(0x3ff0000000000000);
  case 8:
    return ZEXT816(0x3fe5555555555555);
  case 9:
    return ZEXT816(0x3fe0000000000000);
  case 10:
    return ZEXT816(0x3fd5555555555555);
  case 0xb:
    return ZEXT816(0x3fd0000000000000);
  case 0xc:
    return ZEXT816(0x3fc5555555555555);
  case 0xd:
    return ZEXT816(0x3fc0000000000000);
  default:
    return ZEXT816(0);
  }
  auVar4._0_8_ = ((double)(long)*param_1 / (double)CONCAT26(param_1[1] >> 0x1f,(int6)param_1[1])) *
                 4.0;
  uVar7 = NEON_umaxv(CONCAT26(-(ushort)(auVar4._0_8_ == _UNK_1055d9698),
                              CONCAT24(-(ushort)(auVar4._0_8_ == _DAT_1055d9690),
                                       CONCAT22(-(ushort)(auVar4._0_8_ == _UNK_1055d9688),
                                                -(ushort)(auVar4._0_8_ == _DAT_1055d9680)))),2);
  if ((uVar7 & 1) != 0) {
    auVar4._8_8_ = 0;
    return auVar4;
  }
  uVar7 = 0x3ff0;
  if (auVar4._0_8_ < 0.0) {
    uVar7 = 0xbff0;
  }
  auVar6._0_8_ = (double)((ulong)uVar7 << 0x30) *
                 ((double)(long)(ABS(auVar4._0_8_ +
                                     (double)((ulong)uVar7 << 0x30) * 2.6015651015651016e-07 * 0.5)
                                * 3843840.0) / 3843840.0);
  auVar6._8_8_ = 0;
  return auVar6;
}

