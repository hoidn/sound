
undefined * FUN_1027b279c(void)

{
  int iVar1;
  undefined1 auStack_90 [8];
  undefined1 auStack_88 [8];
  undefined1 auStack_80 [8];
  undefined1 auStack_78 [8];
  undefined1 auStack_70 [8];
  undefined1 auStack_68 [8];
  undefined1 auStack_60 [8];
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_1064f8818;
  if (((DAT_10701aec0 & 1) == 0) && (iVar1 = ___cxa_guard_acquire(&DAT_10701aec0), iVar1 != 0)) {
    FUN_101427680(auStack_90,"1 Bar");
    FUN_101427680(auStack_88,"1/2");
    FUN_101427680(auStack_80,"1/4");
    FUN_101427680(auStack_78,"1/8");
    FUN_101427680(auStack_70,"1/16");
    FUN_101427680(auStack_68,"1/32");
    FUN_101427680(auStack_60,"Transients");
    FUN_1002c29cc(&DAT_10701b060,auStack_90,7);
    FUN_100234444(auStack_60);
    FUN_100234444(auStack_68);
    FUN_100234444(auStack_70);
    FUN_100234444(auStack_78);
    FUN_100234444(auStack_80);
    FUN_100234444(auStack_88);
    FUN_100234444(auStack_90);
    ___cxa_atexit(FUN_1002343c8,&DAT_10701b060,0x100000000);
    ___cxa_guard_release(&DAT_10701aec0);
  }
  if (*(long *)PTR____stack_chk_guard_1064f8818 == local_58) {
    return &DAT_10701b060;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

