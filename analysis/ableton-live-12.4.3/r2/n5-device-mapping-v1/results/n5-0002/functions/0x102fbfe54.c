
void FUN_102fbfe54(long param_1,undefined4 *param_2)

{
  long lVar1;
  ulong uVar2;
  undefined4 uVar3;
  byte *pbVar4;
  ulong uVar5;
  
  if (((*(long *)(param_1 + 0x28) != 0) &&
      (*(int *)(*(long *)(*(long *)(param_1 + 0x28) + 0x28) + 0x90) != 0)) &&
     (*(char *)(param_2 + 1) == '\x01')) {
    *(undefined4 *)(param_1 + 0x11290) = *param_2;
  }
  if (0 < (int)param_2[0x240]) {
    uVar5 = 0;
    do {
      if (uVar5 < 0x100) {
        uVar2 = (ulong)*(byte *)((long)(param_2 + 0x200) + uVar5);
        uVar2 = uVar2 | (ulong)(uint)param_2[uVar2 * 2] << 0x20;
      }
      else {
        uVar2 = 0x80000000;
      }
      uVar3 = (undefined4)(uVar2 >> 0x20);
      FUN_102fbec58(uVar3,*(undefined8 *)(param_1 + 0x28),(long)(int)uVar2);
      if (*(long *)(param_1 + 0x30) != 0) {
        FUN_102fbec58(uVar3,*(long *)(param_1 + 0x30),(long)(int)uVar2);
      }
      uVar5 = uVar5 + 1;
      lVar1 = (long)(int)param_2[0x240];
    } while ((long)uVar5 < lVar1);
    pbVar4 = (byte *)(param_2 + 0x200);
    if (0 < (int)param_2[0x240]) {
      do {
        *(undefined8 *)(param_2 + (ulong)*pbVar4 * 2) = 0;
        lVar1 = lVar1 + -1;
        pbVar4 = pbVar4 + 1;
      } while (lVar1 != 0);
    }
  }
  param_2[0x240] = 0;
  return;
}

