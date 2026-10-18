
bool FUN_101514e30(undefined8 param_1,int *param_2,int *param_3,int *param_4)

{
  ushort *puVar1;
  ushort *puVar2;
  uint uVar3;
  int iVar4;
  
  puVar1 = (ushort *)FUN_10142d764();
  uVar3 = (uint)*puVar1;
  if (9 < *puVar1 - 0x30) {
    *param_2 = 0;
    return false;
  }
  iVar4 = 0;
  puVar1 = puVar1 + 3;
  do {
    puVar2 = puVar1;
    iVar4 = uVar3 + iVar4 * 10 + -0x30;
    uVar3 = (uint)puVar2[-2];
    puVar1 = puVar2 + 1;
  } while (uVar3 - 0x30 < 10);
  *param_2 = iVar4;
  if (uVar3 == 0x2e) {
    uVar3 = (uint)puVar2[-1];
    if (9 < puVar2[-1] - 0x30) {
      *param_3 = 0;
      return false;
    }
    iVar4 = 0;
    do {
      puVar2 = puVar1;
      iVar4 = uVar3 + iVar4 * 10 + -0x30;
      uVar3 = (uint)puVar2[-1];
      puVar1 = puVar2 + 1;
    } while (uVar3 - 0x30 < 10);
    *param_3 = iVar4;
    if (uVar3 == 0x5f) {
      uVar3 = (uint)*puVar2;
      if (*puVar2 - 0x30 < 10) {
        iVar4 = 0;
        do {
          iVar4 = uVar3 + iVar4 * 10 + -0x30;
          uVar3 = (uint)*puVar1;
          puVar1 = puVar1 + 1;
        } while (uVar3 - 0x30 < 10);
        *param_4 = iVar4;
        return uVar3 == 0;
      }
      *param_4 = 0;
      return false;
    }
  }
  return false;
}

