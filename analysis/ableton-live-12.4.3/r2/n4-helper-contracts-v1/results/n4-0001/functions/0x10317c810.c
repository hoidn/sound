
void FUN_10317c810(long param_1,undefined8 param_2)

{
  int iVar1;
  long lVar2;
  
  lVar2 = *(long *)(param_1 + 8);
  iVar1 = FUN_1014289f4(param_2,"done");
  if (iVar1 != 0) {
    *(undefined4 *)(lVar2 + 200) = 1;
    return;
  }
  iVar1 = FUN_1014289f4(param_2,"interrupted");
  if (iVar1 != 0) {
    *(undefined4 *)(lVar2 + 200) = 2;
    return;
  }
  *(undefined4 *)(lVar2 + 200) = 0;
  return;
}

