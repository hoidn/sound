
void FUN_1014b6d14(long *param_1)

{
  code *pcVar1;
  int iVar2;
  long lVar3;
  undefined8 uVar4;
  undefined8 uVar5;
  long *plVar6;
  undefined8 uVar7;
  long lVar8;
  undefined4 uVar9;
  undefined4 uVar10;
  double unaff_d8;
  long *local_a8;
  undefined **local_a0;
  long *local_98;
  char *pcStack_90;
  undefined ***pppuStack_88;
  undefined **local_80;
  long *local_78;
  char *pcStack_70;
  undefined ***local_68;
  byte local_60;
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_1064f8818;
  local_a8 = param_1;
  lVar3 = FUN_1014766b4(param_1,"FollowTime");
  if (lVar3 != 0) {
    local_a0 = &PTR_FUN_106674f80;
    pppuStack_88 = &local_a0;
    pcStack_90 = "FollowTime";
    local_68 = &local_80;
    local_80 = &PTR_FUN_106674f80;
    pcStack_70 = "FollowTime";
    local_60 = 1;
    local_98 = param_1;
    local_78 = param_1;
    lVar3 = FUN_1014766b4(lVar3,"Value");
    if (lVar3 != 0) {
      unaff_d8 = AAbstractNode::GetValue<double>();
    }
    if (local_60 == 1) {
      if (local_68 == (undefined ***)0x0) {
                    /* WARNING: Subroutine does not return */
        FUN_10025e3f8();
      }
      (*(code *)(*local_68)[6])();
      if ((local_60 & 1) != 0) {
        if (local_68 == &local_80) {
          lVar8 = 0x20;
        }
        else {
          if (local_68 == (undefined ***)0x0) goto LAB_1014b6e10;
          lVar8 = 0x28;
        }
        (**(code **)((long)*local_68 + lVar8))();
      }
    }
LAB_1014b6e10:
    if (lVar3 != 0) goto LAB_1014b6e18;
  }
  unaff_d8 = 1.0;
LAB_1014b6e18:
  uVar4 = FUN_1014f6ff0(&local_a8,"FollowActionA");
  uVar5 = FUN_1014f6ff0(&local_a8,"FollowActionB");
  uVar9 = FUN_1014f7140(0x3f800000,&local_a8,"FollowChanceA");
  uVar10 = FUN_1014f7140(0,&local_a8,"FollowChanceB");
  iVar2 = (**(code **)(*param_1 + 0x70))(param_1,"FollowAction");
  if (iVar2 != 0) {
    FUN_101471a98(param_1,"Unexpected member FollowAction");
                    /* WARNING: Does not return */
    pcVar1 = (code *)SoftwareBreakpoint(1,0x1014b6fdc);
    (*pcVar1)();
  }
  plVar6 = (long *)(**(code **)(*param_1 + 0x80))(param_1,"FollowAction",1,"FollowAction");
  (**(code **)(*plVar6 + 0x80))(plVar6,"RemoteableDouble",1,"FollowTime");
  FUN_1014f7548(unaff_d8);
  uVar7 = (**(code **)(*plVar6 + 0x80))(plVar6,"RemoteableEnum",1,"FollowActionA");
  FUN_1014f75e0(uVar7,uVar4);
  uVar4 = (**(code **)(*plVar6 + 0x80))(plVar6,"RemoteableEnum",1,"FollowActionB");
  FUN_1014f75e0(uVar4,uVar5);
  (**(code **)(*plVar6 + 0x80))(plVar6,"UserFloat",1,"FollowChanceA");
  FUN_1014f7678(uVar9);
  (**(code **)(*plVar6 + 0x80))(plVar6,"UserFloat",1,"FollowChanceB");
  FUN_1014f7678(uVar10);
  if (*(long *)PTR____stack_chk_guard_1064f8818 != local_58) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}

