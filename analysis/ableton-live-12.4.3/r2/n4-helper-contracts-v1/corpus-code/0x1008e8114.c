// 0x1008e8114 FUN_1008e8114 exported  sig: undefined FUN_1008e8114()

void FUN_1008e8114(long param_1)

{
  int iVar1;
  undefined8 *puVar2;
  int *local_30;
  int *local_28;
  
  puVar2 = *(undefined8 **)(param_1 + 0x28);
  FUN_101427680(&local_28,"continue");
  FUN_101427680(&local_30,"");
  (**(code **)*puVar2)(puVar2,&local_28,&local_30);
  if (local_30 != (int *)0x0) {
    iVar1 = *local_30;
    *local_30 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  FUN_1008e81f0(param_1,2);
  return;
}


