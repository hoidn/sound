
void FUN_101560258(long *param_1,undefined8 param_2)

{
  int iVar1;
  int iVar2;
  long *plVar3;
  int iVar4;
  int *local_50;
  long *local_48;
  
  FUN_101485a6c(param_1 + 0x12);
  (**(code **)(*param_1 + 0xd8))(param_1);
  FUN_1014c0c44(&local_48,param_1 + 0x12);
  if (local_48 == (long *)0x0) {
    plVar3 = (long *)0x0;
  }
  else {
    plVar3 = (long *)___dynamic_cast(local_48,&PTR_vtable_1066749a8,&PTR_vtable_106673618,
                                     0xfffffffffffffffe);
  }
  iVar2 = 0;
  if ((int)param_1[0x14] != 0) {
    iVar2 = ((int)param_1[0x16] - (int)param_1[0x15]) / (int)param_1[0x14];
  }
  if (0 < iVar2) {
    iVar4 = 0;
    do {
      FUN_101485b54(&local_50,local_48);
      FUN_1015170e0(param_2,&local_50);
      if (local_50 != (int *)0x0) {
        iVar1 = *local_50;
        *local_50 = iVar1 + -1;
        if (iVar1 + -1 == 0) {
          FUN_101449efc();
        }
      }
      (**(code **)(*plVar3 + 8))(plVar3,param_1[0x15] + (long)(int)param_1[0x14] * (long)iVar4);
      (**(code **)(*local_48 + 0x138))(local_48,param_2);
      FUN_10151752c(param_2);
      iVar4 = iVar4 + 1;
    } while (iVar2 != iVar4);
  }
  (**(code **)(*param_1 + 0xe0))(param_1);
  if (local_48 != (long *)0x0) {
    iVar2 = (int)local_48[1] + -1;
    *(int *)(local_48 + 1) = iVar2;
    if (iVar2 == 0) {
      FUN_10128eea0();
    }
  }
  return;
}

