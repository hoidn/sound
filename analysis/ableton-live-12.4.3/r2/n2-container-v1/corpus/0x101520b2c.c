
void FUN_101520b2c(long *param_1,undefined8 param_2)

{
  int iVar1;
  int *local_30;
  int *local_28;
  
  FUN_1011cb734(&local_30);
  FUN_101430a10(&local_28,param_2);
  FUN_10142da5c(&local_30,&local_28);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  (**(code **)(*param_1 + 0x30))(param_1,&local_30);
  if (local_30 != (int *)0x0) {
    iVar1 = *local_30;
    *local_30 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  return;
}

