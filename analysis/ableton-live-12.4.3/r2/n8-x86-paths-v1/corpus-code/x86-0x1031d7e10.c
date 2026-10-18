// x86 0x1031d7e10 FUN_1031d7e10 state=exported chunk=chunk-02323.jsonl code_sha256=5a4a2bc2f1cab9449f7666845d3ae80eae4943841a6238b0d936e9d4780e8215

long * FUN_1031d7e10(long *param_1,long param_2)

{
  int *piVar1;
  long *plVar2;
  int iVar3;
  undefined8 uVar4;
  undefined4 uVar5;
  long lVar6;
  long lVar7;
  undefined1 local_98 [4];
  undefined4 local_94;
  long *local_58;
  long local_50;
  long local_48;
  long local_40;
  long local_38;
  
  if ((*(double *)(param_2 + 0x28) != DAT_105b3ce00) ||
     (NAN(*(double *)(param_2 + 0x28)) || NAN(DAT_105b3ce00))) {
    if ((*(double *)(param_2 + 0x30) != DAT_105b3ce00) ||
       (NAN(*(double *)(param_2 + 0x30)) || NAN(DAT_105b3ce00))) {
      lVar6 = FUN_1012bdaa0(0x100);
      FUN_10316a580(lVar6,*(undefined8 *)(param_2 + 0x20),param_2 + 0x28);
      goto LAB_1031d7e87;
    }
  }
  lVar6 = FUN_1012bdaa0(0x100);
  FUN_10316a2b0(lVar6,*(undefined8 *)(param_2 + 0x20),0);
LAB_1031d7e87:
  if (lVar6 == 0) {
    local_48 = 0;
  }
  else {
    iVar3 = *(int *)(lVar6 + 8);
    *(int *)(lVar6 + 8) = iVar3 + 1;
    *(int *)(lVar6 + 8) = iVar3 + 2;
    local_48 = lVar6;
  }
  lVar7 = local_48;
  uVar4 = *(undefined8 *)(param_2 + 0x20);
  iVar3 = *(int *)(param_2 + 0x48);
  local_38 = lVar6;
  FUN_1031d6b30(&local_58);
  if (local_58 == (long *)0x0) {
    *param_1 = 0;
    param_1[1] = 0;
  }
  else {
    (**(code **)(*local_58 + 0x30))(local_98,local_58);
    if (iVar3 == 0) {
      uVar5 = 1;
    }
    else {
      uVar5 = 0;
      if (iVar3 != 1) {
        uVar5 = local_94;
      }
    }
    local_94 = uVar5;
    if (lVar7 != 0) {
      *(int *)(lVar7 + 8) = *(int *)(lVar7 + 8) + 1;
    }
    local_40 = lVar7;
    (**(code **)(*local_58 + 0x38))(&local_50,local_58,local_98,&local_40,uVar4);
    lVar6 = local_50 + 0x18;
    if (local_50 == 0) {
      lVar6 = 0;
    }
    param_1[1] = lVar6;
    *param_1 = local_50;
    local_50 = 0;
    if (local_40 != 0) {
      piVar1 = (int *)(local_40 + 8);
      *piVar1 = *piVar1 + -1;
      if (*piVar1 == 0) {
        FUN_1012716c0();
      }
    }
    plVar2 = local_58 + 1;
    *(int *)plVar2 = (int)*plVar2 + -1;
    if ((int)*plVar2 == 0) {
      FUN_1012716c0(local_58);
    }
  }
  if (lVar7 != 0) {
    piVar1 = (int *)(lVar7 + 8);
    *piVar1 = *piVar1 + -1;
    if ((*piVar1 != 0) || (FUN_1012716c0(lVar7), lVar7 = local_38, local_38 != 0)) {
      piVar1 = (int *)(lVar7 + 8);
      *piVar1 = *piVar1 + -1;
      if (*piVar1 == 0) {
        FUN_1012716c0(lVar7);
      }
    }
  }
  return param_1;
}

