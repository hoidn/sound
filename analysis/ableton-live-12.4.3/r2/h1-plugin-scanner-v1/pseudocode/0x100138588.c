
void FUN_100138588(long param_1,undefined8 param_2,long *param_3)

{
  int iVar1;
  undefined8 uVar2;
  undefined8 *puVar3;
  int *local_48;
  int *local_40;
  int *local_38;
  
  FUN_1001b4e9c(&local_48);
  uVar2 = FUN_100437d1c(&local_48,param_1 + 8);
  FUN_100431940(&local_38,": ");
  uVar2 = FUN_100437d1c(uVar2,&local_38);
  if (local_38 != (int *)0x0) {
    iVar1 = *local_38;
    *local_38 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_100454b40();
    }
  }
  puVar3 = (undefined8 *)FUN_100437d1c(uVar2,param_2);
  local_40 = (int *)*puVar3;
  if (local_40 != (int *)0x0) {
    *local_40 = *local_40 + 1;
  }
  if (local_48 != (int *)0x0) {
    iVar1 = *local_48;
    *local_48 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_100454b40();
    }
  }
  if ((*param_3 == 0) || ((*(uint *)(*param_3 + 4) & 0xfffffffe) != 2)) {
    FUN_100431940(&local_38," [");
    uVar2 = FUN_100437d1c(&local_40,&local_38);
    if (local_38 != (int *)0x0) {
      iVar1 = *local_38;
      *local_38 = iVar1 + -1;
      if (iVar1 + -1 == 0) {
        FUN_100454b40();
      }
    }
    uVar2 = FUN_100437d1c(uVar2,param_3);
    FUN_100431940(&local_38,"]");
    FUN_100437d1c(uVar2,&local_38);
    if (local_38 != (int *)0x0) {
      iVar1 = *local_38;
      *local_38 = iVar1 + -1;
      if (iVar1 + -1 == 0) {
        FUN_100454b40();
      }
    }
  }
  (**(code **)(**(long **)(param_1 + 0x10) + 0x38))(*(long **)(param_1 + 0x10),&local_40);
  if (local_40 != (int *)0x0) {
    iVar1 = *local_40;
    *local_40 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_100454b40();
    }
  }
  return;
}

