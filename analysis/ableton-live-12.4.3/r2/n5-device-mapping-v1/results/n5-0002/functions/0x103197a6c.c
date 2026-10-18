
void FUN_103197a6c(undefined4 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4)

{
  int iVar1;
  undefined8 uVar2;
  long lVar3;
  int *local_58;
  
  if (((DAT_107027d40 & 1) == 0) && (iVar1 = ___cxa_guard_acquire(&DAT_107027d40), iVar1 != 0)) {
    lVar3 = FUN_1012d9850(0x38);
    FUN_101575868(0,0x41200000,0x3dcccccd,0x3c23d70a);
    DAT_107027d38 = lVar3;
    if (lVar3 != 0) {
      *(int *)(lVar3 + 8) = *(int *)(lVar3 + 8) + 1;
    }
    ___cxa_atexit(FUN_1019a2da0,&DAT_107027d38,0x100000000);
    ___cxa_guard_release(&DAT_107027d40);
  }
  lVar3 = DAT_107027d38;
  uVar2 = FUN_1014380fc();
  FUN_101427680(&local_58,param_4);
  FUN_1026f0bcc(0,0x3f800000,param_1,param_3,param_2,lVar3,uVar2,&local_58,0);
  if (local_58 != (int *)0x0) {
    iVar1 = *local_58;
    *local_58 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  return;
}

