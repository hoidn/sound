
undefined8 FUN_1015176c4(undefined8 param_1,long param_2)

{
  long lVar1;
  int iVar2;
  void *pvVar3;
  long lVar4;
  undefined8 uVar5;
  long lVar6;
  long local_40;
  long local_38;
  
  local_38 = 0;
  FUN_101514954(&local_40);
  local_38 = local_40;
  if (local_40 == 0) {
    return 1;
  }
  lVar4 = *(long *)(local_40 + 8);
  lVar1 = *(long *)(local_40 + 0x10);
  lVar6 = *(long *)(param_2 + 8);
  if (lVar1 - lVar4 == *(long *)(param_2 + 0x10) - lVar6) {
    if (lVar4 == lVar1) {
      uVar5 = 0;
    }
    else {
      do {
        iVar2 = FUN_1014812e4(lVar4,lVar6);
        if (iVar2 == 0) {
          uVar5 = 2;
          goto joined_r0x000101517780;
        }
        lVar4 = lVar4 + 0x38;
        lVar6 = lVar6 + 0x38;
      } while (lVar4 != lVar1);
      uVar5 = 0;
joined_r0x000101517780:
      if (local_40 == 0) {
        return uVar5;
      }
    }
  }
  else {
    uVar5 = 2;
  }
  local_38 = 0;
  pvVar3 = (void *)FUN_10148dbd4(local_40);
  operator_delete(pvVar3);
  return uVar5;
}

