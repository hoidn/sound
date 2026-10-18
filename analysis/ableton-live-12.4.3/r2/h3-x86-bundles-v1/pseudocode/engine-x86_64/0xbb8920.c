// 0xbb8920 ableton::system::runningOnNativeArch | undefined __stdcall runningOnNativeArch(void) | state=exported-with-warnings | chunk-00534.jsonl

/* ableton::system::runningOnNativeArch() */

undefined1 ableton::system::runningOnNativeArch(void)

{
  int iVar1;
  undefined1 *local_28;
  ulong local_20;
  undefined1 local_11;
  
  if (DAT_018aa9a8 == '\0') {
    iVar1 = ___cxa_guard_acquire(&DAT_018aa9a8);
    if (iVar1 != 0) {
      local_20 = FUN_00bb89c0("sysctl.proc_translated");
      if (local_20 >> 0x20 == 0xffffffff) {
                    /* WARNING: Subroutine does not return */
        FUN_00050ca0();
      }
      local_28 = &local_11;
      DAT_018aa9a0 = (*(code *)(&PTR_FUN_0178c2e8)[local_20 >> 0x20])(&local_28,&local_20);
      ___cxa_guard_release(&DAT_018aa9a8);
    }
  }
  return DAT_018aa9a0;
}

