// 0x1002b4894 FUN_1002b4894 exported  sig: undefined FUN_1002b4894()

void FUN_1002b4894(long *param_1)

{
  int iVar1;
  ulong uVar2;
  long lVar3;
  long lVar4;
  undefined8 *puVar5;
  undefined8 *puVar6;
  undefined8 *puVar7;
  long local_68;
  undefined4 *local_60 [2];
  char local_49;
  long local_48;
  code *local_40;
  long *plStack_38;
  
  uVar2 = (**(code **)(*param_1 + 0x28))();
  if ((uVar2 & 1) != 0) {
    return;
  }
  local_49 = '\a';
  local_60[0] = (undefined4 *)0x72657865646e69;
  FUN_1026a00e0(&local_68,param_1[5]);
  lVar3 = FUN_1025d90d4(local_60,&local_68);
  if (lVar3 != 0) {
    *(int *)(lVar3 + 8) = *(int *)(lVar3 + 8) + 1;
  }
  lVar4 = param_1[6];
  if ((lVar4 != 0) && (iVar1 = *(int *)(lVar4 + 8) + -1, *(int *)(lVar4 + 8) = iVar1, iVar1 == 0)) {
    FUN_10128eea0();
  }
  param_1[6] = lVar3;
  if ((local_68 != 0) &&
     (iVar1 = *(int *)(local_68 + 8) + -1, *(int *)(local_68 + 8) = iVar1, iVar1 == 0)) {
    FUN_10128eea0();
  }
  if (local_49 < '\0') {
    operator_delete(local_60[0]);
    lVar3 = FUN_1025d9f3c(param_1[6]);
  }
  else {
    lVar3 = FUN_1025d9f3c(param_1[6]);
  }
  if (lVar3 != 0) {
    lVar4 = *(long *)(lVar3 + 8);
    lVar3 = *(long *)(lVar3 + 0x10);
    if (lVar4 == lVar3) {
LAB_1002b49bc:
      if (lVar4 != lVar3) goto LAB_1002b4a74;
    }
    else {
      do {
        if ((*(long **)(lVar4 + 0x18) == param_1) &&
           (*(long **)(lVar4 + 0x28) == param_1 && *(code **)(lVar4 + 0x20) == thunk_FUN_1002b56c4))
        goto LAB_1002b49bc;
        lVar4 = lVar4 + 0x30;
      } while (lVar4 != lVar3);
    }
  }
  lVar3 = FUN_1025d9f3c(param_1[6]);
  FUN_101458fc8(local_60,param_1);
  local_60[0] = &DAT_106592510;
  local_40 = thunk_FUN_1002b56c4;
  puVar5 = *(undefined8 **)(lVar3 + 0x10);
  plStack_38 = param_1;
  if (puVar5 < *(undefined8 **)(lVar3 + 0x18)) {
    puVar6 = puVar5 + 2;
    *puVar6 = 0;
    puVar5[1] = 0;
    puVar5[3] = local_48;
    if (local_48 != 0) {
      lVar4 = *(long *)(local_48 + 0x10);
      puVar7 = puVar5;
      if (lVar4 != 0) {
        puVar6 = (undefined8 *)(lVar4 + 8);
        puVar7 = (undefined8 *)*puVar6;
        puVar5[2] = lVar4;
        puVar7[2] = puVar5;
      }
      puVar5[1] = puVar7;
      *puVar6 = puVar5;
      *(undefined8 **)(local_48 + 0x10) = puVar5;
    }
    *puVar5 = &DAT_106592510;
    puVar5[5] = param_1;
    puVar5[4] = thunk_FUN_1002b56c4;
    puVar5 = puVar5 + 6;
  }
  else {
    puVar5 = (undefined8 *)FUN_10027a5c8(lVar3 + 8,local_60);
  }
  *(undefined8 **)(lVar3 + 0x10) = puVar5;
  FUN_101459068(local_60);
LAB_1002b4a74:
  FUN_1002b4b14(param_1);
  *(undefined1 *)(param_1 + 4) = 1;
  return;
}


