
void FUN_101a4ac8c(long param_1,int param_2,undefined8 param_3,int param_4)

{
  int iVar1;
  ulong uVar2;
  undefined8 *puVar3;
  long *plVar4;
  
  if (param_2 == 0) {
    if (((*(byte *)(param_1 + 0x8e0) & 1) == 0) || ((*(byte *)(param_1 + 0x8e1) & 1) == 0)) {
      if (DAT_106e2b628 != (code *)PTR__lambda___1___106551f08) {
                    /* WARNING: Could not recover jumptable at 0x000101a4ad18. Too many branches */
                    /* WARNING: Treating indirect jump as call */
        (*DAT_106e2b628)(DAT_106e2b630);
        return;
      }
    }
    FUN_101a4adec(param_1,0);
    return;
  }
  if ((((*(byte *)(param_1 + 0x8e0) & 1) == 0) || ((*(byte *)(param_1 + 0x8e1) & 1) == 0)) &&
     (DAT_106e2b638 != (code *)PTR__lambda___1___106551f08)) {
                    /* WARNING: Could not recover jumptable at 0x000101a4acdc. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (*DAT_106e2b638)(DAT_106e2b640);
    return;
  }
  if (((param_4 == 0) || (puVar3 = *(undefined8 **)(param_1 + 0x9b0), puVar3 == (undefined8 *)0x0))
     || (uVar2 = (**(code **)*puVar3)(puVar3), (uVar2 & 1) == 0)) {
    plVar4 = *(long **)(param_1 + 0x9b0);
    if (plVar4 != (long *)0x0) {
      (**(code **)(*plVar4 + 0x10))(plVar4);
    }
    FUN_101a4af58(*(undefined8 *)(param_1 + 0x30),1);
    if (((DAT_106f55d30 & 1) == 0) && (iVar1 = ___cxa_guard_acquire(&DAT_106f55d30), iVar1 != 0)) {
      FUN_1011b5a40(&DAT_106f55ff8);
      ___cxa_guard_release(&DAT_106f55d30);
    }
    DAT_106f55d24 = 0;
  }
  return;
}

