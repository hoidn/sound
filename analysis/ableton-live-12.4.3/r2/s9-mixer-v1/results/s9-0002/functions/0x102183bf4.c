
void FUN_102183bf4(undefined8 param_1,double param_2,long param_3)

{
  long *plVar1;
  float fVar2;
  
  plVar1 = *(long **)(param_3 + 0x18);
  if (0.0 < (float)param_2) {
    fVar2 = (float)_log10f();
                    /* WARNING: Could not recover jumptable at 0x000102183c3c. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (**(code **)(*plVar1 + 0x28))(param_1,(double)(fVar2 * 20.0),plVar1);
    return;
  }
                    /* WARNING: Could not recover jumptable at 0x000102183c60. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (**(code **)(*plVar1 + 0x28))(0xc061800000000000,plVar1);
  return;
}

