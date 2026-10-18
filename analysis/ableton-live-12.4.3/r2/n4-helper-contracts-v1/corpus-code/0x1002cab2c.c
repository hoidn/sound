// 0x1002cab2c FUN_1002cab2c exported-with-warnings  sig: undefined FUN_1002cab2c()

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1002cab2c(long *param_1)

{
  long *plVar1;
  int iVar2;
  ulong uVar3;
  undefined8 uVar4;
  ulong extraout_x1;
  long local_50 [2];
  long local_40;
  long *plStack_38;
  undefined8 uStack_30;
  undefined8 uStack_28;
  
  uVar3 = FUN_1011b5354();
  if (((uVar3 & 1) == 0) && (iVar2 = (**(code **)(*param_1 + 0x718))(param_1), iVar2 != 0)) {
    plStack_38 = _UNK_1055d7f40;
    local_40 = _DAT_1055d7f38;
    uStack_28 = _UNK_1055d7f50;
    uStack_30 = _DAT_1055d7f48;
    FUN_1011aeb80(&local_40);
    if (((extraout_x1 & 1) == 0) && (iVar2 = FUN_1011b59ec(), iVar2 == 0)) {
      FUN_1002a8800(local_50,param_1);
      if (local_50[0] != 0) {
        iVar2 = *(int *)(local_50[0] + 8) + -1;
        *(int *)(local_50[0] + 8) = iVar2;
        if (iVar2 == 0) {
          FUN_10128eea0();
        }
      }
      (**(code **)(*param_1 + 0xa50))(&local_40,param_1);
      plVar1 = plStack_38;
      if (local_40 != 0) {
        iVar2 = *(int *)(local_40 + 8) + -1;
        *(int *)(local_40 + 8) = iVar2;
        if (iVar2 == 0) {
          FUN_10128eea0();
        }
      }
      if (plVar1 != (long *)0x0) {
        (**(code **)(*param_1 + 0xa50))(&local_40,param_1);
        plVar1 = plStack_38;
        FUN_10296885c();
        uVar4 = FUN_1029730c8();
        (**(code **)(*plVar1 + 0x38))(plVar1,uVar4);
        if (local_40 != 0) {
          iVar2 = *(int *)(local_40 + 8) + -1;
          *(int *)(local_40 + 8) = iVar2;
          if (iVar2 == 0) {
            FUN_10128eea0();
          }
        }
      }
    }
  }
  return;
}


