// 0x1011a68f8 FUN_1011a68f8 exported-with-warnings  sig: undefined FUN_1011a68f8()

void FUN_1011a68f8(undefined8 param_1)

{
  int iVar1;
  undefined8 uVar2;
  undefined1 auStack_28 [8];
  
  std::chrono::system_clock::now();
  FUN_103f40190(auStack_28);
  iVar1 = FUN_103f3c8b8(auStack_28);
  if (iVar1 != 0) {
    uVar2 = FUN_103f39a78(auStack_28,"Aborting with error code: ");
    FUN_103f3b7b0(uVar2,param_1);
  }
  thunk_FUN_103f395e4(auStack_28);
                    /* WARNING: Subroutine does not return */
  __exit(param_1);
}


