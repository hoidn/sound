
undefined * FUN_1026a9ef8(void)

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
  if (((DAT_10700c530 & 1) == 0) && (iVar1 = ___cxa_guard_acquire(&DAT_10700c530), iVar1 != 0)) {
    FUN_101427680(auStack_90,"Beats");
    FUN_101427680(auStack_88,"Tones");
    FUN_101427680(auStack_80,"Texture");
    FUN_101427680(auStack_78,"Re-Pitch");
    FUN_101427680(auStack_70,"Complex");
    FUN_101427680(auStack_68,"REX");
    FUN_101427680(auStack_60,"Complex Pro");
    FUN_1002c29cc(&DAT_10700c860,auStack_90,7);
    FUN_100234444(auStack_60);
    FUN_100234444(auStack_68);
    FUN_100234444(auStack_70);
    FUN_100234444(auStack_78);
    FUN_100234444(auStack_80);
    FUN_100234444(auStack_88);
    FUN_100234444(auStack_90);
    ___cxa_atexit(FUN_1002343c8,&DAT_10700c860,0x100000000);
    ___cxa_guard_release(&DAT_10700c530);
  }
  if (*(long *)PTR____stack_chk_guard_1064f8818 == local_58) {
    return &DAT_10700c860;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

