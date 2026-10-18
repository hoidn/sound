
void FUN_10145f264(long param_1,long param_2)

{
  int iVar1;
  long lVar2;
  
  if (param_2 != 0) {
    *(int *)(param_2 + 8) = *(int *)(param_2 + 8) + 1;
  }
  lVar2 = *(long *)(param_1 + 0x18);
  if ((lVar2 != 0) && (iVar1 = *(int *)(lVar2 + 8) + -1, *(int *)(lVar2 + 8) = iVar1, iVar1 == 0)) {
    FUN_10128eea0(lVar2);
    *(long *)(param_1 + 0x18) = param_2;
    return;
  }
  *(long *)(param_1 + 0x18) = param_2;
  return;
}

