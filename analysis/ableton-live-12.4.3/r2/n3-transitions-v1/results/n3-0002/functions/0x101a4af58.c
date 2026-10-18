
void FUN_101a4af58(long param_1,undefined8 param_2)

{
  uint uVar1;
  int iVar2;
  ulong uVar3;
  undefined8 uVar4;
  long lVar5;
  long local_50;
  undefined8 local_48;
  
  if ((uint)*(byte *)(param_1 + 0x60) != (uint)param_2) {
    if (*(int *)(param_1 + 8) != -1) {
      FUN_101ab7348(&local_50,&DAT_106f56018,0x10100,0x100500,0);
      FUN_101a9c534(local_48,*(undefined4 *)(param_1 + 8));
      FUN_101a9c504(local_48,param_2);
      (**(code **)(local_50 + 0x10))(&local_50);
      FUN_101ab786c(&local_50);
    }
    *(char *)(param_1 + 0x60) = (char)param_2;
    lVar5 = *(long *)(param_1 + 0x10);
    if (lVar5 != 0) {
      iVar2 = FUN_101a40264(lVar5);
      uVar3 = FUN_101a4025c(lVar5);
      if ((int)uVar3 <= iVar2) {
        do {
          uVar4 = FUN_101a4022c(lVar5,uVar3);
          FUN_101a54364(uVar4,param_2);
          uVar1 = (int)uVar3 + 1;
          uVar3 = (ulong)uVar1;
        } while (iVar2 + 1U != uVar1);
      }
    }
  }
  return;
}

