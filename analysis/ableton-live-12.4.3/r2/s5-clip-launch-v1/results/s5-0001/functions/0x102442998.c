
undefined1  [16] FUN_102442998(long param_1,long param_2)

{
  int iVar1;
  undefined1 auVar2 [16];
  undefined8 local_28;
  
  iVar1 = FUN_1015661b8(*(undefined8 *)(param_1 + 600));
  if (iVar1 != 0) {
    local_28 = FUN_1026e3698(*(undefined8 *)(param_1 + 0x1d8));
    iVar1 = FUN_1015661b8(*(undefined8 *)(param_1 + 600));
    auVar2 = FUN_101aaae44(&local_28,iVar1 + -1);
    return auVar2;
  }
  if (param_2 != 0) {
    auVar2 = FUN_10268ce9c(param_2);
    return auVar2;
  }
  return ZEXT816(0xbff0000000000000);
}

