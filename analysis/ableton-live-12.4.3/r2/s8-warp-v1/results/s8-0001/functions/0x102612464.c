
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_102612464(double param_1,double param_2,long *param_3)

{
  int iVar1;
  undefined8 *puVar2;
  long lVar3;
  long *plVar4;
  long lVar5;
  undefined8 uVar6;
  ushort uVar7;
  double local_60;
  
  puVar2 = (undefined8 *)(**(code **)(*param_3 + 0x60))();
  lVar3 = (**(code **)*puVar2)(puVar2,param_3);
  uVar6 = *(undefined8 *)(lVar3 + 0x20);
  lVar3 = FUN_1012d9734(0x90);
  FUN_1026105ec();
  if (lVar3 != 0) {
    *(int *)(lVar3 + 8) = *(int *)(lVar3 + 8) + 1;
  }
  FUN_101482718(lVar3);
  plVar4 = (long *)(**(code **)(*param_3 + 0x60))(param_3);
  lVar5 = (**(code **)(*plVar4 + 0x20))(plVar4,param_3,uVar6);
  local_60 = *(double *)(*(long *)(lVar5 + 8) + 0x58) + 0.03125;
  uVar7 = NEON_umaxv(CONCAT26(-(ushort)(local_60 == _UNK_1055d9698),
                              CONCAT24(-(ushort)(local_60 == _DAT_1055d9690),
                                       CONCAT22(-(ushort)(local_60 == _UNK_1055d9688),
                                                -(ushort)(local_60 == _DAT_1055d9680)))),2);
  if ((uVar7 & 1) == 0) {
    uVar7 = 0x3ff0;
    if (local_60 < 0.0) {
      uVar7 = 0xbff0;
    }
    local_60 = (double)((ulong)uVar7 << 0x30) *
               ((double)(long)(ABS(local_60 +
                                   (double)((ulong)uVar7 << 0x30) * 2.6015651015651016e-07 * 0.5) *
                              3843840.0) / 3843840.0);
  }
  plVar4 = (long *)(**(code **)(*param_3 + 0x60))(param_3);
  lVar5 = (**(code **)(*plVar4 + 0x20))(plVar4,param_3,uVar6);
  *(double *)(lVar3 + 0x50) =
       *(double *)(*(long *)(lVar5 + 8) + 0x50) + ((param_2 * 60.0) / param_1) * 0.03125;
  *(double *)(lVar3 + 0x58) = local_60;
  FUN_10156d360(param_3,lVar3);
  iVar1 = *(int *)(lVar3 + 8) + -1;
  *(int *)(lVar3 + 8) = iVar1;
  if (iVar1 == 0) {
    FUN_10128eea0(lVar3);
  }
  return;
}

