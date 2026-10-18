
long FUN_100138504(long param_1)

{
  int iVar1;
  ulong uVar2;
  
  (**(code **)(**(long **)(param_1 + 0x10) + 0x40))();
  iVar1 = (**(code **)(**(long **)(param_1 + 0x10) + 0x10))();
  if ((iVar1 != 0) &&
     (uVar2 = (**(code **)(**(long **)(param_1 + 0x10) + 0x18))(), (uVar2 & 1) == 0)) {
    return (ulong)(*(int *)(param_1 + 0x1c) < *(int *)(param_1 + 0x18)) << 1;
  }
  return 1;
}

