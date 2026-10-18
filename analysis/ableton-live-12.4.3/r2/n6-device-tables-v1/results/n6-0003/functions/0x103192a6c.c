
void FUN_103192a6c(undefined8 param_1,undefined8 param_2,undefined8 *param_3)

{
  undefined8 uVar1;
  int iVar2;
  long lVar3;
  int *local_50;
  undefined8 local_48;
  
  if (((DAT_107027d80 & 1) == 0) && (iVar2 = ___cxa_guard_acquire(&DAT_107027d80), iVar2 != 0)) {
    lVar3 = FUN_1012d9850(0x38);
    FUN_101575868(0xbf800000,0x3f800000,0x3c23d70a,0x3a83126f);
    DAT_107027d78 = lVar3;
    if (lVar3 != 0) {
      *(int *)(lVar3 + 8) = *(int *)(lVar3 + 8) + 1;
    }
    ___cxa_atexit(FUN_1019a2da0,&DAT_107027d78,0x100000000);
    ___cxa_guard_release(&DAT_107027d80);
  }
  if (((DAT_107027d90 & 1) == 0) && (iVar2 = ___cxa_guard_acquire(&DAT_107027d90), iVar2 != 0)) {
    FUN_103198044(&local_48);
    DAT_107027d88 = local_48;
    local_48 = 0;
    FUN_1030ee830(&local_48);
    ___cxa_atexit(FUN_101437c58,&DAT_107027d88,0x100000000);
    ___cxa_guard_release(&DAT_107027d90);
  }
  uVar1 = DAT_107027d88;
  lVar3 = DAT_107027d78;
  local_50 = (int *)*param_3;
  if (local_50 != (int *)0x0) {
    *local_50 = *local_50 + 1;
  }
  FUN_1026f0b58(0xbf800000,0x3f800000,0x3f000000,param_1,param_2,lVar3,uVar1,&local_50,2);
  if (local_50 != (int *)0x0) {
    iVar2 = *local_50;
    *local_50 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  return;
}

