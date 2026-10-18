
undefined8 FUN_101514864(void)

{
  int iVar1;
  undefined8 uVar2;
  undefined1 auStack_28 [8];
  
  if (((DAT_106f50408 & 1) == 0) && (iVar1 = ___cxa_guard_acquire(&DAT_106f50408), iVar1 != 0)) {
    uVar2 = FUN_10142a21c();
    FUN_101428230(auStack_28,"Schema");
    FUN_10142a698(&DAT_106f50400,uVar2,auStack_28);
    FUN_100234d5c(auStack_28);
    ___cxa_atexit(FUN_1014281f0,&DAT_106f50400,0x100000000);
    ___cxa_guard_release(&DAT_106f50408);
    return DAT_106f50400;
  }
  return DAT_106f50400;
}

