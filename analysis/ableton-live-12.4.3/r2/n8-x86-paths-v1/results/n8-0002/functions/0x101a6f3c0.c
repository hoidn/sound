
void FUN_101a6f3c0(long param_1,char param_2,char param_3)

{
  char cVar1;
  int iVar2;
  
  if (*(long **)(param_1 + 0x9b0) != (long *)0x0) {
    (**(code **)(**(long **)(param_1 + 0x9b0) + 0x10))();
  }
  FUN_101a6f520(*(undefined8 *)(param_1 + 0x30),param_2);
  if (DAT_1073e7c60 == '\0') {
    iVar2 = ___cxa_guard_acquire(&DAT_1073e7c60);
    if (iVar2 != 0) {
      FUN_10118ff00(&DAT_1073e7c50);
      ___cxa_guard_release(&DAT_1073e7c60);
    }
  }
  if (param_2 == '\0') {
    if (param_3 == '\0') {
      DAT_1073e7c4c = 0;
    }
    else {
      cVar1 = FUN_10118ffe0(&DAT_1073e7c50);
      if (cVar1 != '\0') {
        iVar2 = FUN_1011901d0(&DAT_1073e7c50);
        if (0xdac < iVar2) {
          DAT_1073e7c4c = 0;
        }
      }
      DAT_1073e7c4c = DAT_1073e7c4c + 1;
      FUN_10118ff20(&DAT_1073e7c50);
      if (DAT_1073e7c4c == 3) {
        if (DAT_10750a1d0 != (code *)0x0) {
          (*DAT_10750a1d0)();
        }
        if (DAT_10750a1d8 != (code *)0x0) {
          (*DAT_10750a1d8)();
        }
        if (DAT_10750a1e0 != (code *)0x0) {
          (*DAT_10750a1e0)();
        }
        goto LAB_101a6f405;
      }
    }
    if (DAT_10750a1f0 != (code *)0x0) {
      (*DAT_10750a1f0)();
    }
    if (DAT_10750a1f8 != (code *)0x0) {
                    /* WARNING: Could not recover jumptable at 0x000101a6f4cb. Too many branches */
                    /* WARNING: Treating indirect jump as call */
      (*DAT_10750a1f8)();
      return;
    }
  }
  else {
LAB_101a6f405:
    DAT_1073e7c4c = 0;
  }
  return;
}

