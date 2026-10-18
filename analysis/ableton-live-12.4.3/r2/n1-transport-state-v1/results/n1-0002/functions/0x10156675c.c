
void FUN_10156675c(long *param_1,undefined8 param_2)

{
  int iVar1;
  undefined8 uVar2;
  int *local_48;
  int *local_40;
  undefined1 auStack_38 [24];
  
  iVar1 = (int)param_2;
  if ((-1 < iVar1) &&
     (iVar1 < (int)((ulong)(((long *)param_1[0x12])[1] - *(long *)param_1[0x12]) >> 3))) {
    if ((int)param_1[0x1b] != iVar1) {
      thunk_FUN_10155a3b4(auStack_38,param_1,1);
      *(int *)(param_1 + 0x1b) = iVar1;
      FUN_101482dac(param_1);
      thunk_FUN_10155a56c(auStack_38);
    }
    return;
  }
  uVar2 = std::chrono::system_clock::now();
  FUN_103f3ffec(auStack_38,4,uVar2);
  iVar1 = FUN_103f3c8b8(auStack_38);
  if (iVar1 != 0) {
    uVar2 = FUN_103f39a78(auStack_38,"Value ");
    uVar2 = FUN_103f3b7b0(uVar2,param_2);
    uVar2 = FUN_103f39a78(uVar2," out of range for \'");
    (**(code **)(*param_1 + 0x1c0))(&local_40,param_1);
    uVar2 = FUN_101432ff0(uVar2,&local_40);
    uVar2 = FUN_103f39a78(uVar2,"\' (");
    FUN_1014861d8(&local_48,param_1);
    uVar2 = FUN_101432ff0(uVar2,&local_48);
    FUN_103f39a78(uVar2,")");
    if (local_48 != (int *)0x0) {
      iVar1 = *local_48;
      *local_48 = iVar1 + -1;
      if (iVar1 + -1 == 0) {
        FUN_101449efc();
      }
    }
    if (local_40 != (int *)0x0) {
      iVar1 = *local_40;
      *local_40 = iVar1 + -1;
      if (iVar1 + -1 == 0) {
        FUN_101449efc();
      }
    }
  }
  thunk_FUN_103f395e4(auStack_38);
  return;
}

