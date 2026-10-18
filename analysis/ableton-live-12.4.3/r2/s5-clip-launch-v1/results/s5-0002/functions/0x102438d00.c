
undefined * FUN_102438d00(void)

{
  int iVar1;
  undefined1 auStack_e8 [8];
  undefined1 auStack_e0 [8];
  undefined1 auStack_d8 [8];
  undefined1 auStack_d0 [8];
  undefined1 auStack_c8 [8];
  undefined1 auStack_c0 [8];
  undefined1 auStack_b8 [8];
  undefined1 auStack_b0 [8];
  undefined1 auStack_a8 [8];
  undefined1 auStack_a0 [8];
  undefined1 auStack_98 [8];
  undefined1 auStack_90 [8];
  undefined1 auStack_88 [8];
  undefined1 auStack_80 [8];
  undefined1 auStack_78 [8];
  long local_70;
  
  local_70 = *(long *)PTR____stack_chk_guard_1064f8818;
  if (((DAT_10700a0a8 & 1) == 0) && (iVar1 = ___cxa_guard_acquire(&DAT_10700a0a8), iVar1 != 0)) {
    FUN_101427680(auStack_e8,"Global");
    FUN_101427680("None");
    FUN_101427680("8 Bars");
    FUN_101427680("4 Bars");
    FUN_101427680("2 Bars");
    FUN_101427680(auStack_c0,"1 Bar");
    FUN_101427680(auStack_b8,"1/2");
    FUN_101427680(auStack_b0,"1/2T");
    FUN_101427680(auStack_a8,"1/4");
    FUN_101427680(auStack_a0,"1/4T");
    FUN_101427680(auStack_98,"1/8");
    FUN_101427680(auStack_90,"1/8T");
    FUN_101427680(auStack_88,"1/16");
    FUN_101427680(auStack_80,"1/16T");
    FUN_101427680(auStack_78,"1/32");
    FUN_1002c29cc(&DAT_10700a138,auStack_e8,0xf);
    FUN_100234444(auStack_78);
    FUN_100234444(auStack_80);
    FUN_100234444(auStack_88);
    FUN_100234444(auStack_90);
    FUN_100234444(auStack_98);
    FUN_100234444(auStack_a0);
    FUN_100234444(auStack_a8);
    FUN_100234444(auStack_b0);
    FUN_100234444(auStack_b8);
    FUN_100234444(auStack_c0);
    FUN_100234444(auStack_c8);
    FUN_100234444(auStack_d0);
    FUN_100234444(auStack_d8);
    FUN_100234444(auStack_e0);
    FUN_100234444(auStack_e8);
    ___cxa_atexit(FUN_1002343c8,&DAT_10700a138,0x100000000);
    ___cxa_guard_release(&DAT_10700a0a8);
  }
  if (*(long *)PTR____stack_chk_guard_1064f8818 == local_70) {
    return &DAT_10700a138;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

