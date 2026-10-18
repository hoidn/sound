
void FUN_101486fe4(undefined8 *param_1,long *param_2,undefined8 param_3)

{
  int iVar1;
  undefined8 uVar2;
  long lVar3;
  long *local_68;
  undefined **local_60;
  undefined1 *puStack_58;
  ulong local_50;
  undefined ***local_48;
  byte local_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_1064f8818;
  FUN_1011b5224();
  *param_1 = 0;
  local_50 = (ulong)DAT_106e0cec1;
  DAT_106e0cec1 = 1;
  local_60 = &PTR_FUN_10665b840;
  puStack_58 = &DAT_106e0cec1;
  local_48 = &local_60;
  local_40 = 1;
  (**(code **)(*param_2 + 0x28))(param_2);
  FUN_1014c0c44(&local_68);
  *param_1 = local_68;
  (**(code **)(*local_68 + 200))(local_68);
  (**(code **)(*local_68 + 0x140))(local_68,param_2,param_3);
  if (local_40 == 1) {
    if (local_48 == (undefined ***)0x0) {
                    /* WARNING: Subroutine does not return */
      FUN_10025e3f8();
    }
    (*(code *)(*local_48)[6])();
    if ((local_40 & 1) != 0) {
      if (local_48 == &local_60) {
        lVar3 = 0x20;
      }
      else {
        if (local_48 == (undefined ***)0x0) goto LAB_1014870e8;
        lVar3 = 0x28;
      }
      (**(code **)((long)*local_48 + lVar3))();
    }
  }
LAB_1014870e8:
  iVar1 = FUN_1015192c0(param_3);
  if (iVar1 != 0) {
    uVar2 = FUN_1015183fc(param_3);
    (**(code **)(*local_68 + 0xd0))(local_68,uVar2);
  }
  uVar2 = FUN_1015183fc(param_3);
  FUN_101487198(local_68,local_68,uVar2);
  if (*(long *)PTR____stack_chk_guard_1064f8818 == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

