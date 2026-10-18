
void FUN_1018536d4(undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined4 *param_4)

{
  int iVar1;
  undefined8 uVar2;
  int *local_68;
  undefined4 local_60 [2];
  int *local_58;
  long *local_50;
  int *local_48;
  long *local_40;
  long *local_38;
  
  local_40 = (long *)0x0;
  FUN_101463eb4(&local_38);
  if (local_40 != (long *)0x0) {
    iVar1 = *(int *)((long)local_40 + 8) + -1;
    *(int *)((long)local_40 + 8) = iVar1;
    if (iVar1 == 0) {
      FUN_10128eea0();
    }
  }
  local_40 = local_38;
  (**(code **)(*local_38 + 0x98))(local_38,param_3);
  (**(code **)(*local_40 + 0x68))(local_40,0);
  FUN_1011cb734(&local_48);
  uVar2 = std::chrono::system_clock::now();
  FUN_103f3ffec(&local_38,2,uVar2);
  iVar1 = FUN_103f3c8b8(&local_38);
  if (iVar1 != 0) {
    uVar2 = FUN_103f39a78(&local_38,"Loading document ");
    FUN_100259ba4(uVar2,param_3);
  }
  thunk_FUN_103f395e4(&local_38);
  local_60[0] = *param_4;
  local_58 = *(int **)(param_4 + 2);
  if (local_58 != (int *)0x0) {
    *local_58 = *local_58 + 1;
  }
  FUN_10148389c(&local_38,local_40,local_60,&local_48);
  local_50 = local_38;
  if ((local_38 != (long *)0x0) && ((int)local_38[1] == 0)) {
    FUN_10128eea0();
  }
  if (local_58 != (int *)0x0) {
    iVar1 = *local_58;
    *local_58 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar2 = std::chrono::system_clock::now();
  FUN_103f3ffec(&local_38,2,uVar2);
  iVar1 = FUN_103f3c8b8(&local_38);
  if (iVar1 != 0) {
    uVar2 = FUN_103f39a78(&local_38,"Loaded document was created by ");
    FUN_101432ff0(uVar2,&local_48);
  }
  thunk_FUN_103f395e4(&local_38);
  local_68 = local_48;
  if (local_48 != (int *)0x0) {
    *local_48 = *local_48 + 1;
  }
  FUN_101573d24(&local_68,0);
  if (local_68 != (int *)0x0) {
    iVar1 = *local_68;
    *local_68 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  (**(code **)(*local_40 + 0x70))();
  FUN_10153f480(param_1,&local_50);
  if (local_50 != (long *)0x0) {
    iVar1 = (int)local_50[1] + -1;
    *(int *)(local_50 + 1) = iVar1;
    if (iVar1 == 0) {
      FUN_10128eea0();
    }
  }
  if (local_48 != (int *)0x0) {
    iVar1 = *local_48;
    *local_48 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_40 != (long *)0x0) {
    (**(code **)(*local_40 + 0x18))();
    if (local_40 != (long *)0x0) {
      iVar1 = (int)local_40[1] + -1;
      *(int *)(local_40 + 1) = iVar1;
      if (iVar1 == 0) {
        FUN_10128eea0();
      }
    }
  }
  return;
}

