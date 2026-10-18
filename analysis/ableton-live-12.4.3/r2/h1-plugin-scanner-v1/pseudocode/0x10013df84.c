
undefined8 FUN_10013df84(long param_1)

{
  int iVar1;
  undefined8 uVar2;
  
  iVar1 = FUN_100190a0c(param_1 + 0x28);
  if ((iVar1 != 0) &&
     (iVar1 = FUN_100190c34(param_1 + 0x28),
     iVar1 < (int)(*(uint *)(*(long *)(param_1 + 0x20) + 8) >> 1))) {
    return 0;
  }
  uVar2 = FUN_1001806e4();
  FUN_100190908(param_1 + 0x28);
  return uVar2;
}

