// 0x1031b8e5c FUN_1031b8e5c exported  sig: undefined FUN_1031b8e5c()

void FUN_1031b8e5c(undefined8 *param_1)

{
  undefined8 *puVar1;
  int iVar2;
  undefined8 uVar3;
  int *local_40;
  void *local_38;
  undefined8 uStack_30;
  long local_28;
  
  *param_1 = 0;
  param_1[1] = 0;
  param_1[2] = 0;
  FUN_1030ad96c(&local_38,2);
  FUN_10142d468(&local_40,L"user");
  puVar1 = (undefined8 *)param_1[1];
  if (puVar1 < (undefined8 *)param_1[2]) {
    puVar1[2] = local_28;
    puVar1[3] = local_40;
    puVar1[1] = uStack_30;
    *puVar1 = local_38;
    uStack_30 = 0;
    local_28 = 0;
    local_38 = (void *)0x0;
    param_1[1] = puVar1 + 4;
  }
  else {
    uVar3 = FUN_1031c342c(param_1,&local_38,&local_40);
    param_1[1] = uVar3;
    if (local_40 != (int *)0x0) {
      iVar2 = *local_40;
      *local_40 = iVar2 + -1;
      if (iVar2 + -1 == 0) {
        FUN_101449efc();
      }
    }
  }
  if (local_28 < 0) {
    operator_delete(local_38);
  }
  FUN_1030ad96c(&local_38,3);
  FUN_10142d468(&local_40,L"local");
  puVar1 = (undefined8 *)param_1[1];
  if (puVar1 < (undefined8 *)param_1[2]) {
    puVar1[2] = local_28;
    puVar1[3] = local_40;
    puVar1[1] = uStack_30;
    *puVar1 = local_38;
    uStack_30 = 0;
    local_28 = 0;
    local_38 = (void *)0x0;
    param_1[1] = puVar1 + 4;
  }
  else {
    uVar3 = FUN_1031c342c(param_1,&local_38,&local_40);
    param_1[1] = uVar3;
    if (local_40 != (int *)0x0) {
      iVar2 = *local_40;
      *local_40 = iVar2 + -1;
      if (iVar2 + -1 == 0) {
        FUN_101449efc();
      }
    }
  }
  if (-1 < local_28) {
    return;
  }
  operator_delete(local_38);
  return;
}


