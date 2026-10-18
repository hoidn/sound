
undefined4 FUN_1024b5e50(void)

{
  undefined4 uVar1;
  undefined1 local_2c [4];
  undefined1 local_28 [16];
  long local_18;
  
  local_18 = *(long *)PTR____stack_chk_guard_106a33b20;
  _fegetenv(local_28);
  FUN_10119c880(local_2c,0x100500);
  uVar1 = FUN_101b2e930();
  FUN_10119c8c0(local_2c);
  _fesetenv(local_28);
  if (*(long *)PTR____stack_chk_guard_106a33b20 == local_18) {
    return uVar1;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

