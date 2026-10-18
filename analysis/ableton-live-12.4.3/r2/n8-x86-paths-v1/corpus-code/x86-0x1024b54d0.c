// x86 0x1024b54d0 FUN_1024b54d0 state=exported-with-warnings chunk=chunk-01671.jsonl code_sha256=ab682e4cca9fd754402b22b2c0c46418d619f2c724d8bee27442f283e14df8a6

undefined4 FUN_1024b54d0(undefined8 param_1)

{
  undefined4 uVar1;
  undefined1 local_34 [4];
  undefined1 local_30 [8];
  undefined1 local_28 [16];
  long local_18;
  
  local_18 = *(long *)PTR____stack_chk_guard_106a33b20;
  _fegetenv(local_28);
  FUN_10119c880(local_34,0x100500);
  FUN_1011930a0(local_30);
  uVar1 = FUN_101b2e700(param_1);
  FUN_1011930c0(local_30);
  FUN_10119c8c0(local_34);
  _fesetenv(local_28);
  if (*(long *)PTR____stack_chk_guard_106a33b20 == local_18) {
    return uVar1;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

