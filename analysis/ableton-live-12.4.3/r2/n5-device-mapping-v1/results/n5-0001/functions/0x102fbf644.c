
void FUN_102fbf644(long param_1,long param_2)

{
  bool bVar1;
  undefined8 uVar2;
  long lVar3;
  long lVar4;
  
  if (param_2 != 0) {
    uVar2 = FUN_101a94314(param_2);
    lVar3 = FUN_102fbe25c();
    *(long *)(param_1 + 0x28) = lVar3;
    if (lVar3 != 0) {
      lVar4 = *(long *)(lVar3 + 0x28);
      if (*(int *)(lVar4 + 0x84) == 0) {
        *(undefined4 *)(lVar3 + 0x30) = *(undefined4 *)(param_1 + 0xc);
      }
      else {
        uVar2 = FUN_102fbe25c(uVar2);
        *(undefined8 *)(param_1 + 0x30) = uVar2;
        lVar3 = *(long *)(param_1 + 0x28);
        lVar4 = *(long *)(lVar3 + 0x28);
        *(undefined4 *)(lVar3 + 0x30) = *(undefined4 *)(param_1 + 0xc);
        if (lVar4 == 0) goto LAB_102fbf6b4;
      }
      FUN_102fbe580(lVar4,*(undefined8 *)(lVar3 + 0x10));
    }
  }
LAB_102fbf6b4:
  bVar1 = false;
  if (*(long *)(param_1 + 0x28) != 0) {
    if (*(int *)(*(long *)(*(long *)(param_1 + 0x28) + 0x28) + 0x84) == 0) {
      *(undefined1 *)(param_1 + 0x11294) = 1;
      return;
    }
    bVar1 = *(long *)(param_1 + 0x30) != 0;
  }
  *(bool *)(param_1 + 0x11294) = bVar1;
  return;
}

