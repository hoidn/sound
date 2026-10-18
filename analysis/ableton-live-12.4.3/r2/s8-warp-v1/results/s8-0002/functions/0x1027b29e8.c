
undefined * FUN_1027b29e8(void)

{
  int iVar1;
  undefined1 auStack_50 [8];
  undefined1 auStack_48 [8];
  undefined1 auStack_40 [8];
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_1064f8818;
  if (((DAT_10701aec8 & 1) == 0) && (iVar1 = ___cxa_guard_acquire(&DAT_10701aec8), iVar1 != 0)) {
    FUN_101427680(auStack_50,"LoopOs");
    FUN_101427680(auStack_48,"LoopFwd");
    FUN_101427680(auStack_40,"LoopAlt");
    FUN_1002c29cc(&DAT_10701b078,auStack_50,3);
    FUN_100234444(auStack_40);
    FUN_100234444(auStack_48);
    FUN_100234444(auStack_50);
    ___cxa_atexit(FUN_1002343c8,&DAT_10701b078,0x100000000);
    ___cxa_guard_release(&DAT_10701aec8);
  }
  if (*(long *)PTR____stack_chk_guard_1064f8818 == local_38) {
    return &DAT_10701b078;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

