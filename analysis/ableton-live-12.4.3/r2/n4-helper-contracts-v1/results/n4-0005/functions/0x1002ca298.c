
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1002ca298(long param_1)

{
  int iVar1;
  long lVar2;
  long lVar3;
  undefined8 uVar4;
  uint extraout_w1;
  ulong extraout_x1;
  long local_68;
  long local_60;
  long local_58;
  long local_50;
  undefined8 uStack_48;
  undefined8 uStack_40;
  undefined8 uStack_38;
  
  uStack_48 = _UNK_1055d7d34;
  local_50 = _DAT_1055d7d2c;
  uStack_38 = _UNK_1055d7d44;
  uStack_40 = _DAT_1055d7d3c;
  FUN_1011aeb80(&local_50);
  if ((extraout_x1 & 1) == 0) {
    uStack_48 = _UNK_1055d7fa0;
    local_50 = _DAT_1055d7f98;
    uStack_38 = _UNK_1055d7fb0;
    uStack_40 = _DAT_1055d7fa8;
    FUN_1011aeb80(&local_50);
    FUN_1026a00e0(&local_68,param_1);
    FUN_1038f0d4c(&local_60,&local_68,extraout_w1 & 1,0xffffffff);
    uVar4 = *(undefined8 *)(param_1 + 0x670);
    lVar2 = FUN_1012d9850(0x198);
    local_50 = local_60;
    local_60 = 0;
    thunk_FUN_10390bbb4(lVar2,&local_50,uVar4);
    if (lVar2 != 0) {
      *(int *)(lVar2 + 8) = *(int *)(lVar2 + 8) + 1;
    }
    local_58 = lVar2;
    if (local_50 != 0) {
      iVar1 = *(int *)(local_50 + 8) + -1;
      *(int *)(local_50 + 8) = iVar1;
      if (iVar1 == 0) {
        FUN_10128eea0();
      }
    }
    lVar3 = *(long *)(param_1 + 0x678);
    if (lVar3 != 0) {
      iVar1 = *(int *)(lVar3 + 8) + -1;
      *(int *)(lVar3 + 8) = iVar1;
      if (iVar1 == 0) {
        FUN_10128eea0();
      }
    }
    *(long *)(param_1 + 0x678) = lVar2;
    local_58 = 0;
    if (local_60 != 0) {
      iVar1 = *(int *)(local_60 + 8) + -1;
      *(int *)(local_60 + 8) = iVar1;
      if (iVar1 == 0) {
        FUN_10128eea0();
      }
    }
    if (local_68 != 0) {
      iVar1 = *(int *)(local_68 + 8) + -1;
      *(int *)(local_68 + 8) = iVar1;
      if (iVar1 == 0) {
        FUN_10128eea0();
      }
    }
  }
  else {
    local_58 = *(long *)(param_1 + 0x670);
    FUN_1002ca4b8(&local_50,&local_58);
    lVar2 = *(long *)(param_1 + 0x678);
    if (lVar2 != 0) {
      iVar1 = *(int *)(lVar2 + 8) + -1;
      *(int *)(lVar2 + 8) = iVar1;
      if (iVar1 == 0) {
        FUN_10128eea0();
      }
    }
    *(long *)(param_1 + 0x678) = local_50;
  }
  iVar1 = FUN_10184d7e0(param_1);
  if (iVar1 == 0) {
    uVar4 = 0;
  }
  else {
    uVar4 = FUN_10184a7f4(param_1);
  }
  FUN_1039061fc(*(undefined8 *)(param_1 + 0x670),uVar4,1,0);
  return;
}

