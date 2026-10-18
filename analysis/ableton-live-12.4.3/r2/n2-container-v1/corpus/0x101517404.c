
void FUN_101517404(long *param_1,undefined8 param_2,undefined8 param_3)

{
  int iVar1;
  int *local_48;
  undefined4 local_40;
  undefined1 auStack_35 [5];
  
  FUN_101449838(&local_48);
  local_40 = 0;
  FUN_101522b50(&local_48,param_3);
  (**(code **)(*param_1 + 0x38))(param_1," ");
  (**(code **)(*param_1 + 0x38))(param_1,param_2);
  FUN_1011bfe14(auStack_35,5,"=%c");
  (**(code **)(*param_1 + 0x38))(param_1,auStack_35);
  *(undefined4 *)(param_1 + 3) = 4;
  FUN_101522dfc(param_1[10],&local_48);
  FUN_1011bfe14(auStack_35,5,"%c");
  (**(code **)(*param_1 + 0x38))(param_1,auStack_35);
  *(undefined4 *)(param_1 + 3) = 2;
  if (local_48 != (int *)0x0) {
    iVar1 = *local_48;
    *local_48 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  return;
}

