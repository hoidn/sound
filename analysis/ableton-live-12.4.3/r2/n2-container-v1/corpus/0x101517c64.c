
void FUN_101517c64(void)

{
  int iVar1;
  undefined8 uVar2;
  undefined1 auStack_28 [8];
  
  uVar2 = std::chrono::system_clock::now();
  FUN_103f3ffec(auStack_28,4,uVar2);
  iVar1 = FUN_103f3c8b8(auStack_28);
  if (iVar1 != 0) {
    FUN_103f39a78(auStack_28,"Schema: Current schema not found");
  }
  thunk_FUN_103f395e4(auStack_28);
                    /* WARNING: Subroutine does not return */
  FUN_1011b5244();
}

