
void FUN_102920db4(long param_1,ulong param_2)

{
  ulong uVar1;
  long lVar2;
  long alStack_60 [3];
  long *local_48;
  byte local_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_1064f8818;
  FUN_10155e744(alStack_60,*(undefined8 *)(param_1 + 0x30),0);
  uVar1 = FUN_101569984(*(undefined8 *)(param_1 + 0x30));
  if (uVar1 <= param_2) {
    uVar1 = param_2;
  }
  FUN_10156998c(*(undefined8 *)(param_1 + 0x30),uVar1);
  if (local_40 == 1) {
    if (local_48 == (long *)0x0) {
                    /* WARNING: Subroutine does not return */
      FUN_10025e3f8();
    }
    (**(code **)(*local_48 + 0x30))();
    if ((local_40 & 1) != 0) {
      if (local_48 == alStack_60) {
        lVar2 = 0x20;
      }
      else {
        if (local_48 == (long *)0x0) goto LAB_102920e64;
        lVar2 = 0x28;
      }
      (**(code **)(*local_48 + lVar2))();
    }
  }
LAB_102920e64:
  if (*(long *)PTR____stack_chk_guard_1064f8818 == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

