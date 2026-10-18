
void FUN_101515628(undefined8 *param_1)

{
  long lVar1;
  void *pvVar2;
  undefined8 uVar3;
  
  FUN_101515674(*param_1);
  uVar3 = *param_1;
  *param_1 = 0;
  lVar1 = DAT_106e0d200;
  DAT_106e0d200 = uVar3;
  if (lVar1 != 0) {
    pvVar2 = (void *)FUN_10148dbd4();
    operator_delete(pvVar2);
    return;
  }
  return;
}

