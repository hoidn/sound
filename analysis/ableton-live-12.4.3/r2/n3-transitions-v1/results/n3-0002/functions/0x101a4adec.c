
void FUN_101a4adec(long param_1,ulong param_2,int param_3)

{
  int iVar1;
  
  if (*(long **)(param_1 + 0x9b0) != (long *)0x0) {
    (**(code **)(**(long **)(param_1 + 0x9b0) + 0x10))();
  }
  FUN_101a4af58(*(undefined8 *)(param_1 + 0x30),param_2);
  if (((DAT_106f55d30 & 1) == 0) && (iVar1 = ___cxa_guard_acquire(&DAT_106f55d30), iVar1 != 0)) {
    FUN_1011b5a40(&DAT_106f55ff8);
    ___cxa_guard_release(&DAT_106f55d30);
  }
  if ((param_2 & 1) == 0) {
    if (param_3 == 0) {
      DAT_106f55d24 = 0;
    }
    else {
      iVar1 = FUN_1011b5b54(&DAT_106f55ff8);
      if ((iVar1 != 0) && (iVar1 = FUN_1011b5d7c(&DAT_106f55ff8), 0xdac < iVar1)) {
        DAT_106f55d24 = 0;
      }
      DAT_106f55d24 = DAT_106f55d24 + 1;
      FUN_1011b5a50(&DAT_106f55ff8);
      if (DAT_106f55d24 == 3) {
        if (DAT_106e2b6b0 != (code *)0x0) {
          (*DAT_106e2b6b0)();
        }
        if (DAT_106e2b6b8 != (code *)0x0) {
          (*DAT_106e2b6b8)();
        }
        if (DAT_106e2b6c0 != (code *)0x0) {
          (*DAT_106e2b6c0)();
        }
        goto LAB_101a4ae3c;
      }
    }
    if (DAT_106e2b6c8 != (code *)0x0) {
      (*DAT_106e2b6c8)();
    }
    if (DAT_106e2b6d0 != (code *)0x0) {
                    /* WARNING: Could not recover jumptable at 0x000101a4af10. Too many branches */
                    /* WARNING: Treating indirect jump as call */
      (*DAT_106e2b6d0)();
      return;
    }
  }
  else {
LAB_101a4ae3c:
    DAT_106f55d24 = 0;
  }
  return;
}

