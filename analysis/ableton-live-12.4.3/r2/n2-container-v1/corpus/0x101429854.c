
bool FUN_101429854(long *param_1,long *param_2)

{
  bool bVar1;
  long lVar2;
  short *psVar3;
  long lVar4;
  short *psVar5;
  ulong uVar6;
  
  lVar2 = *param_2;
  if (lVar2 == 0) {
    uVar6 = 0xffffffffffffffff;
    lVar4 = *param_1;
  }
  else {
    uVar6 = (ulong)(*(int *)(lVar2 + 4) / 2 + -1);
    lVar4 = *param_1;
  }
  if ((lVar4 != 0) && ((ulong)(long)(*(int *)(lVar4 + 4) / 2 + -1) < uVar6)) {
    return false;
  }
  if (uVar6 == 0) {
    return true;
  }
  psVar3 = (short *)(lVar2 + 0x10);
  psVar5 = (short *)(lVar4 + 0x10);
  do {
    uVar6 = uVar6 - 1;
    bVar1 = *psVar3 == *psVar5;
    if (*psVar3 != *psVar5) {
      return bVar1;
    }
    psVar3 = psVar3 + 1;
    psVar5 = psVar5 + 1;
  } while (uVar6 != 0);
  return bVar1;
}

