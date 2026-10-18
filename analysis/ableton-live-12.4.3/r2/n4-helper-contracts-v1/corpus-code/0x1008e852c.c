// 0x1008e852c FUN_1008e852c exported  sig: undefined FUN_1008e852c()

void FUN_1008e852c(long param_1)

{
  int iVar1;
  long lVar2;
  undefined8 *puVar3;
  int *local_38;
  int *local_30;
  undefined4 local_28;
  
  puVar3 = *(undefined8 **)(param_1 + 0x28);
  FUN_101427680(&local_30,"cancel");
  FUN_101427680(&local_38,"");
  (**(code **)*puVar3)(puVar3,&local_30,&local_38);
  if (local_38 != (int *)0x0) {
    iVar1 = *local_38;
    *local_38 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_30 != (int *)0x0) {
    iVar1 = *local_30;
    *local_30 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  FUN_10185128c(*(undefined8 *)(param_1 + 0x18),*(undefined8 *)(param_1 + 0x30));
  local_30 = (int *)0x0;
  local_28 = 0;
  lVar2 = *(long *)(param_1 + 0x30);
  if (lVar2 != 0) {
    iVar1 = *(int *)(lVar2 + 8) + -1;
    *(int *)(lVar2 + 8) = iVar1;
    if (iVar1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined8 *)(param_1 + 0x30) = 0;
  return;
}


