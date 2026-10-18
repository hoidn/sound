
void FUN_101514954(undefined8 *param_1,undefined8 param_2)

{
  int iVar1;
  long *plVar2;
  ulong uVar3;
  int *local_40;
  long *local_38;
  int *local_30;
  int *local_28;
  
  FUN_10142dd4c(&local_28,param_2,".txt");
  plVar2 = (long *)FUN_101514864();
  FUN_101428384(&local_30,&local_28);
  uVar3 = (**(code **)(*plVar2 + 0x28))(plVar2,&local_30);
  if (local_30 != (int *)0x0) {
    iVar1 = *local_30;
    *local_30 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if ((uVar3 & 1) == 0) {
    *param_1 = 0;
  }
  else {
    plVar2 = (long *)FUN_101514864();
    FUN_101428384(&local_40,&local_28);
    (**(code **)(*plVar2 + 0x48))(&local_38,plVar2,&local_40);
    if (local_40 != (int *)0x0) {
      iVar1 = *local_40;
      *local_40 = iVar1 + -1;
      if (iVar1 + -1 == 0) {
        FUN_101449efc();
      }
    }
    FUN_101514b14(param_1,local_38);
    (**(code **)(*local_38 + 0x70))();
    if (local_38 != (long *)0x0) {
      iVar1 = (int)local_38[1] + -1;
      *(int *)(local_38 + 1) = iVar1;
      if (iVar1 == 0) {
        FUN_10128eea0();
      }
    }
  }
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  return;
}

