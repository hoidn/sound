
long FUN_10145f064(long param_1)

{
  int iVar1;
  undefined8 *puVar2;
  long lVar3;
  long lVar4;
  
  puVar2 = (undefined8 *)FUN_10128ed98();
  *puVar2 = &PTR_FUN_106672398;
  puVar2[3] = 0;
  puVar2[4] = 0;
  lVar3 = FUN_1012d9850(0x60);
  thunk_FUN_101246db4(lVar3,param_1);
  if (lVar3 != 0) {
    *(int *)(lVar3 + 8) = *(int *)(lVar3 + 8) + 1;
  }
  lVar4 = puVar2[4];
  if (lVar4 != 0) {
    iVar1 = *(int *)(lVar4 + 8) + -1;
    *(int *)(lVar4 + 8) = iVar1;
    if (iVar1 == 0) {
      FUN_10128eea0();
    }
  }
  *(long *)(param_1 + 0x20) = lVar3;
  return param_1;
}

