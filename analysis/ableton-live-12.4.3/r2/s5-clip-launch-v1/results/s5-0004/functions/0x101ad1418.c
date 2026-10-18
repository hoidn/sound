
void FUN_101ad1418(long *param_1,undefined8 param_2,undefined8 param_3,ulong param_4)

{
  long *plVar1;
  long lVar2;
  
  if ((param_4 & 1) != 0) {
    plVar1 = (long *)FUN_101acff34();
                    /* WARNING: Could not recover jumptable at 0x000101ad144c. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (**(code **)(*plVar1 + 0x48))(plVar1,param_3);
    return;
  }
  plVar1 = *(long **)(param_1[3] + 0xa0);
  (**(code **)(*param_1 + 0x28))();
  lVar2 = FUN_101ab4558();
                    /* WARNING: Could not recover jumptable at 0x000101ad1494. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (**(code **)(*plVar1 + 0x18))((double)*(float *)(lVar2 + 0x1c),plVar1,param_2,param_3);
  return;
}

