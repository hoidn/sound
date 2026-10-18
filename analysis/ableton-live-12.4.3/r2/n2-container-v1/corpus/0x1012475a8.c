
void FUN_1012475a8(long param_1,undefined8 param_2)

{
  int iVar1;
  long lVar2;
  ulong uVar3;
  int local_2c;
  int *local_28;
  
  FUN_101246fb8();
  (**(code **)(**(long **)(param_1 + 0x38) + 0x58))();
  lVar2 = FUN_1049f8370(*(undefined8 *)(param_1 + 0x18),*(undefined4 *)(param_1 + 0x48));
  while( true ) {
    if (lVar2 == 0) {
      FUN_101427680(&local_28,"Internal error (out of memory)");
      FUN_101247760(param_1,0xffffffff,&local_28);
      if ((local_28 != (int *)0x0) && (iVar1 = *local_28, *local_28 = iVar1 + -1, iVar1 + -1 == 0))
      {
        FUN_101449efc();
      }
      return;
    }
    uVar3 = FUN_101433700(param_2,lVar2,*(undefined4 *)(param_1 + 0x48),&local_2c);
    if ((uVar3 & 1) == 0) {
      FUN_101427680(&local_28,"Parse error (IO error)");
      FUN_101247760(param_1,0xffffffff,&local_28);
      if (local_28 == (int *)0x0) {
        return;
      }
      iVar1 = *local_28;
      *local_28 = iVar1 + -1;
      if (iVar1 + -1 != 0) {
        return;
      }
      FUN_101449efc();
      return;
    }
    iVar1 = FUN_1049f861c(*(undefined8 *)(param_1 + 0x18),local_2c,local_2c == 0);
    if (iVar1 == 0) break;
    if (local_2c == 0) {
      (**(code **)(**(long **)(param_1 + 0x38) + 0x60))();
      return;
    }
    lVar2 = FUN_1049f8370(*(undefined8 *)(param_1 + 0x18),*(undefined4 *)(param_1 + 0x48));
  }
  iVar1 = FUN_1049f8b64(*(undefined8 *)(param_1 + 0x18));
  if (iVar1 != 0x23) {
    FUN_101247828(param_1);
    return;
  }
  if ((*(byte *)(param_1 + 0x58) & 1) != 0) {
    return;
  }
  FUN_101247760(param_1,0xffffffff,param_1 + 0x50);
  return;
}

