
undefined * FUN_1026aa13c(void)

{
  int iVar1;
  undefined1 auStack_88 [8];
  undefined1 auStack_80 [8];
  undefined1 auStack_78 [8];
  undefined1 auStack_70 [8];
  undefined1 auStack_68 [8];
  undefined1 auStack_60 [8];
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_1064f8818;
  if (((DAT_10700c538 & 1) == 0) && (iVar1 = ___cxa_guard_acquire(&DAT_10700c538), iVar1 != 0)) {
    FUN_101427680(auStack_88,"Beats");
    FUN_101427680(auStack_80,"Tones");
    FUN_101427680(auStack_78,"Texture");
    FUN_101427680(auStack_70,"Re-Pitch");
    FUN_101427680(auStack_68,"Complex");
    FUN_101427680(auStack_60,"Complex Pro");
    FUN_1002c29cc(&DAT_10700c878,auStack_88,6);
    FUN_100234444(auStack_60);
    FUN_100234444(auStack_68);
    FUN_100234444(auStack_70);
    FUN_100234444(auStack_78);
    FUN_100234444(auStack_80);
    FUN_100234444(auStack_88);
    ___cxa_atexit(FUN_1002343c8,&DAT_10700c878,0x100000000);
    ___cxa_guard_release(&DAT_10700c538);
  }
  if (*(long *)PTR____stack_chk_guard_1064f8818 == local_58) {
    return &DAT_10700c878;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

