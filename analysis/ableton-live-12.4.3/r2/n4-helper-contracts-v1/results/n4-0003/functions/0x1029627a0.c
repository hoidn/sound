
void FUN_1029627a0(long param_1)

{
  int iVar1;
  undefined *puVar2;
  long lVar3;
  long lVar4;
  undefined8 *puVar5;
  undefined8 *puVar6;
  undefined8 *puVar7;
  long local_68;
  undefined4 *local_60 [2];
  char local_49;
  long local_48;
  undefined *local_40;
  long lStack_38;
  
  if ((*(byte *)(param_1 + 0x38) & 1) != 0) {
    return;
  }
  FUN_101849958();
  local_49 = '\x06';
  local_60[0] = (undefined4 *)CONCAT17(local_60[0]._7_1_,0x736e6f646461);
  FUN_1026a00e0(&local_68);
  lVar3 = FUN_1025d90d4(local_60,&local_68);
  if (lVar3 != 0) {
    *(int *)(lVar3 + 8) = *(int *)(lVar3 + 8) + 1;
  }
  lVar4 = *(long *)(param_1 + 0x48);
  if ((lVar4 != 0) && (iVar1 = *(int *)(lVar4 + 8) + -1, *(int *)(lVar4 + 8) = iVar1, iVar1 == 0)) {
    FUN_10128eea0();
  }
  *(long *)(param_1 + 0x48) = lVar3;
  if ((local_68 != 0) &&
     (iVar1 = *(int *)(local_68 + 8) + -1, *(int *)(local_68 + 8) = iVar1, iVar1 == 0)) {
    FUN_10128eea0();
  }
  if (local_49 < '\0') {
    operator_delete(local_60[0]);
    lVar3 = FUN_1025d9f3c(*(undefined8 *)(param_1 + 0x48));
    puVar2 = PTR_CallMemberFunc<&TAddOnsMediator::ProcessStateChangedListener>_10652d548;
  }
  else {
    lVar3 = FUN_1025d9f3c(*(undefined8 *)(param_1 + 0x48));
    puVar2 = PTR_CallMemberFunc<&TAddOnsMediator::ProcessStateChangedListener>_10652d548;
  }
  PTR_CallMemberFunc<&TAddOnsMediator::ProcessStateChangedListener>_10652d548 = puVar2;
  if (lVar3 != 0) {
    lVar4 = *(long *)(lVar3 + 8);
    lVar3 = *(long *)(lVar3 + 0x10);
    if (lVar4 == lVar3) {
LAB_1029628bc:
      if (lVar4 != lVar3) goto LAB_102962974;
    }
    else {
      do {
        if ((*(long *)(lVar4 + 0x18) == param_1) &&
           (*(long *)(lVar4 + 0x28) == param_1 && *(undefined **)(lVar4 + 0x20) == puVar2))
        goto LAB_1029628bc;
        lVar4 = lVar4 + 0x30;
      } while (lVar4 != lVar3);
    }
  }
  lVar3 = FUN_1025d9f3c(*(undefined8 *)(param_1 + 0x48));
  FUN_101458fc8(local_60,param_1);
  local_60[0] = &DAT_106592510;
  puVar5 = *(undefined8 **)(lVar3 + 0x10);
  local_40 = puVar2;
  lStack_38 = param_1;
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
    puVar5[4] = puVar2;
    puVar5 = puVar5 + 6;
  }
  else {
    puVar5 = (undefined8 *)FUN_10027a5c8(lVar3 + 8,local_60);
  }
  *(undefined8 **)(lVar3 + 0x10) = puVar5;
  FUN_101459068(local_60);
LAB_102962974:
  FUN_102966254(param_1);
  if ((*(byte *)(param_1 + 0x38) & 1) == 0) {
    *(undefined1 *)(param_1 + 0x38) = 1;
    FUN_1017cde1c(param_1 + 0x18,1);
    return;
  }
  return;
}

