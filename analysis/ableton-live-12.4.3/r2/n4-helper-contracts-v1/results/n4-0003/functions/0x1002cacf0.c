
void FUN_1002cacf0(void)

{
  int iVar1;
  long lVar2;
  int *local_60;
  long local_58;
  long *local_50;
  undefined **local_48 [3];
  undefined ***local_30;
  long local_28;
  
  local_28 = *(long *)PTR____stack_chk_guard_1064f8818;
  FUN_1029650f8(&local_58);
  FUN_1011db828(&local_60);
  local_48[0] = &PTR_FUN_10659d0c8;
  local_30 = local_48;
  (**(code **)(*local_50 + 0x28))(local_50,&local_60,local_48,600000);
  if (local_30 == local_48) {
    lVar2 = 0x20;
  }
  else {
    if (local_30 == (undefined ***)0x0) goto LAB_1002cad84;
    lVar2 = 0x28;
  }
  (**(code **)((long)*local_30 + lVar2))();
LAB_1002cad84:
  if (local_60 != (int *)0x0) {
    iVar1 = *local_60;
    *local_60 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_58 != 0) {
    iVar1 = *(int *)(local_58 + 8) + -1;
    *(int *)(local_58 + 8) = iVar1;
    if (iVar1 == 0) {
      FUN_10128eea0();
    }
  }
  if (*(long *)PTR____stack_chk_guard_1064f8818 == local_28) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

