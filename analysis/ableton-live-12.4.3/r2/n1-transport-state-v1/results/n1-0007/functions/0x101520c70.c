
void FUN_101520c70(float param_1,long *param_2)

{
  int iVar1;
  int *local_38 [2];
  long local_28;
  
  local_28 = *(long *)PTR____stack_chk_guard_1064f8818;
  if ((uint)ABS(param_1) < 0x7f800000) {
    if (param_1 == 3.4028235e+38) {
      if (*(long *)PTR____stack_chk_guard_1064f8818 == local_28) {
                    /* WARNING: Could not recover jumptable at 0x000101520d48. Too many branches */
                    /* WARNING: Treating indirect jump as call */
        (**(code **)(*param_2 + 0x38))(param_2,"Invalid");
        return;
      }
      goto LAB_101520d88;
    }
    FUN_10143157c(local_38);
    (**(code **)(*param_2 + 0x30))(param_2,local_38);
    if ((local_38[0] != (int *)0x0) &&
       (iVar1 = *local_38[0], *local_38[0] = iVar1 + -1, iVar1 + -1 == 0)) {
      FUN_101449efc();
    }
  }
  else {
    FUN_1011bfe14(local_38,10,"#%8.8X");
    (**(code **)(*param_2 + 0x38))(param_2,local_38);
  }
  if (*(long *)PTR____stack_chk_guard_1064f8818 == local_28) {
    return;
  }
LAB_101520d88:
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

