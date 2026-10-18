
void FUN_101515508(undefined8 param_1)

{
  int iVar1;
  undefined8 uVar2;
  undefined2 local_2a;
  int *local_28;
  
  FUN_1011cb734(param_1);
  FUN_1011c4184();
  FUN_101427680(&local_28);
  uVar2 = FUN_10142da5c(param_1,&local_28);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  local_2a = 0x5f;
  FUN_10142d558(&local_28,&local_2a,1);
  uVar2 = FUN_10142da5c(uVar2,&local_28);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  FUN_101470ef4();
  FUN_101430a10(&local_28);
  FUN_10142da5c(uVar2,&local_28);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  return;
}

