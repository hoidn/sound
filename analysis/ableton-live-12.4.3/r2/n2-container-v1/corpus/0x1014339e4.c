
void FUN_1014339e4(long param_1)

{
  int iVar1;
  int iVar2;
  long lVar3;
  
  lVar3 = *(long *)(param_1 + 0x20);
  if ((*(byte *)(lVar3 + 0x28) & 1) == 0) {
    iVar1 = *(int *)(lVar3 + 0x24);
  }
  else {
    *(undefined8 *)(lVar3 + 0x30) = 0;
    iVar1 = *(int *)(lVar3 + 0x24);
    do {
      *(int *)(lVar3 + 0x50) = *(int *)(lVar3 + 0x20) - iVar1;
      *(long *)(lVar3 + 0x48) = *(long *)(lVar3 + 0x18) + (long)iVar1;
      FUN_10119a6f8((undefined8 *)(lVar3 + 0x30),4);
      iVar1 = *(int *)(lVar3 + 0x20) - *(int *)(lVar3 + 0x50);
      *(int *)(lVar3 + 0x24) = iVar1;
      if (*(int *)(lVar3 + 0x50) != 0) break;
      iVar2 = 0;
      if (*(int *)(lVar3 + 0x20) != 0) {
        (**(code **)(**(long **)(lVar3 + 0xa0) + 0x90))
                  (*(long **)(lVar3 + 0xa0),*(undefined8 *)(lVar3 + 0x18));
        iVar1 = 0;
        *(undefined4 *)(lVar3 + 0x24) = 0;
        iVar2 = *(int *)(lVar3 + 0x50);
      }
    } while (iVar2 == 0);
  }
  if (iVar1 != 0) {
    (**(code **)(**(long **)(lVar3 + 0xa0) + 0x90))
              (*(long **)(lVar3 + 0xa0),*(undefined8 *)(lVar3 + 0x18));
    *(undefined4 *)(lVar3 + 0x24) = 0;
  }
  lVar3 = *(long *)(param_1 + 0x20);
  if (lVar3 != 0) {
    iVar1 = *(int *)(lVar3 + 8) + -1;
    *(int *)(lVar3 + 8) = iVar1;
    if (iVar1 == 0) {
      FUN_10128eea0();
      *(undefined8 *)(param_1 + 0x20) = 0;
      return;
    }
  }
  *(undefined8 *)(param_1 + 0x20) = 0;
  return;
}

