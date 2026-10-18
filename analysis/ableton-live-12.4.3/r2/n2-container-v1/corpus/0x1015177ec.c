
undefined4 FUN_1015177ec(void)

{
  undefined4 uVar1;
  void *pvVar2;
  long local_28;
  
  FUN_101514954(&local_28);
  if (local_28 != 0) {
    uVar1 = *(undefined4 *)(local_28 + 4);
    local_28 = 0;
    pvVar2 = (void *)FUN_10148dbd4();
    operator_delete(pvVar2);
    return uVar1;
  }
  return 0;
}

