
undefined8 FUN_101514c6c(undefined8 param_1)

{
  long lVar1;
  undefined8 uVar2;
  long lVar3;
  void *pvVar4;
  long local_28;
  
  if ((DAT_106f50488 & 1) == 0) {
    FUN_10541448c();
    lVar1 = FUN_1015236c4(&DAT_106f504a8,param_1);
  }
  else {
    lVar1 = FUN_1015236c4(&DAT_106f504a8,param_1);
  }
  if ((DAT_106f50488 & 1) == 0) {
    FUN_1054144d4();
  }
  if (lVar1 == 0) {
    if ((DAT_106f50488 & 1) == 0) {
      FUN_10541451c();
    }
    FUN_101514954(&local_28,param_1);
    lVar3 = FUN_1015239d0(&DAT_106f504a8,param_1,param_1,&local_28);
    lVar1 = local_28;
    uVar2 = *(undefined8 *)(lVar3 + 0x18);
    local_28 = 0;
    if (lVar1 != 0) {
      pvVar4 = (void *)FUN_10148dbd4(lVar1);
      operator_delete(pvVar4);
      return uVar2;
    }
  }
  else {
    uVar2 = *(undefined8 *)(lVar1 + 0x18);
  }
  return uVar2;
}

