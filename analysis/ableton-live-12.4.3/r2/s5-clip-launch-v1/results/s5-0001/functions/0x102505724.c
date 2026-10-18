
void FUN_102505724(undefined4 param_1,undefined8 *param_2,undefined8 param_3,undefined8 param_4,
                  undefined8 param_5,undefined8 param_6)

{
  undefined *puVar1;
  int iVar2;
  undefined8 uVar3;
  undefined *local_d0;
  undefined8 uStack_c8;
  undefined1 auStack_c0 [8];
  undefined1 auStack_b8 [8];
  undefined1 auStack_b0 [8];
  undefined1 auStack_a8 [8];
  undefined1 auStack_a0 [8];
  undefined1 auStack_98 [8];
  undefined1 auStack_90 [8];
  undefined1 auStack_88 [8];
  long local_80;
  
  local_80 = *(long *)PTR____stack_chk_guard_1064f8818;
  uVar3 = *param_2;
  FUN_102503ea0();
  if (((DAT_10700aad0 & 1) == 0) && (iVar2 = ___cxa_guard_acquire(&DAT_10700aad0), iVar2 != 0)) {
    FUN_101427680(&local_d0,"No Action");
    FUN_101427680("Stop");
    FUN_101427680("Again");
    FUN_101427680("Previous");
    FUN_101427680("Next");
    FUN_101427680("First");
    FUN_101427680("Last");
    FUN_101427680(auStack_98,"Any");
    FUN_101427680(auStack_90,"Other");
    FUN_101427680(auStack_88,"Jump");
    FUN_1002c29cc(&DAT_10700ab50,&local_d0,10);
    FUN_100234444(auStack_88);
    FUN_100234444(auStack_90);
    FUN_100234444(auStack_98);
    FUN_100234444(auStack_a0);
    FUN_100234444(auStack_a8);
    FUN_100234444(auStack_b0);
    FUN_100234444(auStack_b8);
    FUN_100234444(auStack_c0);
    FUN_100234444(&uStack_c8);
    FUN_100234444(&local_d0);
    ___cxa_atexit(FUN_1002343c8,&DAT_10700ab50,0x100000000);
    ___cxa_guard_release(&DAT_10700aad0);
  }
  puVar1 = PTR_CallMemberFunc<&AFollowAction::NotifyListeners>_10652b4d0;
  local_d0 = PTR_CallMemberFunc<&AFollowAction::NotifyListeners>_10652b4d0;
  uStack_c8 = uVar3;
  FUN_101567bfc(param_3,param_4,&DAT_10700ab38,&DAT_10700ab50,&local_d0);
  local_d0 = puVar1;
  uStack_c8 = uVar3;
  FUN_10157432c(0,0x42c80000,param_1,param_5,param_2[1],&local_d0);
  local_d0 = PTR_CallMemberFunc<&AFollowAction::FollowChanceController>_10652b4d8;
  uStack_c8 = uVar3;
  FUN_101568990(param_5,&local_d0);
  local_d0 = puVar1;
  uStack_c8 = uVar3;
  FUN_10157432c(0xbf800000,0x4b0000004b000000,0x3f800000,param_6,param_2[2],&local_d0);
  if (*(long *)PTR____stack_chk_guard_1064f8818 == local_80) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

