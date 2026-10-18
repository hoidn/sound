
/* WARNING: Removing unreachable block (ram,0x000101516058) */

void FUN_101515ed8(long *param_1,undefined4 param_2)

{
  undefined4 uVar1;
  int iVar2;
  void *pvVar3;
  undefined4 *puVar4;
  void *local_98 [2];
  char local_81;
  void *local_80 [2];
  char local_69;
  void *local_68;
  undefined8 uStack_60;
  long local_58;
  void *local_50;
  undefined8 uStack_48;
  undefined8 local_40;
  
  iVar2 = FUN_1015176c4(param_1 + 2,param_1[1]);
  if (iVar2 == 3) {
                    /* WARNING: Could not recover jumptable at 0x000101515f28. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (**(code **)(*(long *)param_1[4] + 8))((long *)param_1[4],param_1 + 2);
    return;
  }
  puVar4 = (undefined4 *)param_1[1];
  *puVar4 = param_2;
  FUN_101514954(&local_50,param_1 + 2);
  if (local_50 == (void *)0x0) {
    puVar4[1] = 0;
    local_50 = (void *)0x0;
  }
  else {
    uVar1 = *(undefined4 *)((long)local_50 + 4);
    local_50 = (void *)0x0;
    pvVar3 = (void *)FUN_10148dbd4();
    operator_delete(pvVar3);
    puVar4[1] = uVar1;
  }
  if (iVar2 != 0) {
    if (iVar2 == 2) {
      (*(code *)**(undefined8 **)param_1[4])();
      *(int *)(param_1[1] + 4) = *(int *)(param_1[1] + 4) + 1;
    }
    else {
      (**(code **)(*(long *)param_1[4] + 0x10))((long *)param_1[4],param_1 + 2);
    }
    (**(code **)(*param_1 + 8))(local_80,param_1);
    FUN_1011c74dc(local_98,param_1 + 2);
    FUN_100241e54(&local_68,local_80,local_98);
    FUN_10025dc7c(&local_68,".txt","");
    uStack_48 = uStack_60;
    local_50 = local_68;
    local_40 = local_58;
    uStack_60 = 0;
    local_58 = 0;
    local_68 = (void *)0x0;
    (**(code **)*param_1)(param_1,&local_50);
    if (local_58 < 0) {
      operator_delete(local_68);
    }
    if (local_81 < '\0') {
      operator_delete(local_98[0]);
    }
    if (local_69 < '\0') {
      operator_delete(local_80[0]);
      return;
    }
  }
  return;
}

