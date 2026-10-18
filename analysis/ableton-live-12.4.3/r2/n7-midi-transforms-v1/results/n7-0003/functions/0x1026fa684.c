
undefined1  [16] FUN_1026fa684(long *param_1,int param_2)

{
  bool bVar1;
  int iVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  ulong uVar5;
  long lVar6;
  undefined4 uVar7;
  long lVar8;
  undefined4 uVar9;
  undefined4 local_58;
  undefined4 uStack_54;
  undefined1 local_50 [16];
  
  uVar3 = (**(code **)(*param_1 + 0x170))();
  uVar4 = FUN_1026f0200();
  uVar5 = FUN_10147fd68(uVar3,uVar4);
  if ((uVar5 & 1) == 0) {
    uVar3 = (**(code **)(*param_1 + 0x170))(param_1);
    uVar4 = FUN_1026eb7a8();
    uVar5 = FUN_10147fd68(uVar3,uVar4);
    if ((uVar5 & 1) == 0) {
      uVar3 = (**(code **)(*param_1 + 0x170))(param_1);
      uVar4 = FUN_1026ee884();
      iVar2 = FUN_10147fd68(uVar3,uVar4);
      uVar7 = 3;
      if (iVar2 == 0) {
        uVar7 = 0;
      }
      lVar8 = *param_1;
      goto joined_r0x0001026fa754;
    }
    uVar7 = 2;
    lVar8 = *param_1;
    if (param_2 == 0) goto LAB_1026fa70c;
LAB_1026fa758:
    lVar8 = (**(code **)(lVar8 + 0x388))(param_1);
    if (lVar8 == 0) {
      uVar9 = (**(code **)(*param_1 + 0x2f0))(param_1);
      lVar8 = (**(code **)(*param_1 + 0x388))(param_1);
    }
    else {
      uVar9 = FUN_102585a18();
      lVar8 = (**(code **)(*param_1 + 0x388))(param_1);
    }
    if (lVar8 != 0) {
      uStack_54 = FUN_102585a28();
      local_58 = uVar9;
      uVar5 = (**(code **)(*param_1 + 0x2e0))(param_1);
      goto joined_r0x0001026fa82c;
    }
  }
  else {
    uVar7 = 1;
    lVar8 = *param_1;
joined_r0x0001026fa754:
    if (param_2 != 0) goto LAB_1026fa758;
LAB_1026fa70c:
    uVar9 = (**(code **)(lVar8 + 0x2f0))(param_1);
  }
  uStack_54 = (**(code **)(*param_1 + 0x2f8))(param_1);
  local_58 = uVar9;
  uVar5 = (**(code **)(*param_1 + 0x2e0))(param_1);
joined_r0x0001026fa82c:
  if ((uVar5 & 1) == 0) {
    lVar6 = (**(code **)(*param_1 + 0x2b8))(param_1);
    lVar8 = 0x2a8;
    if (lVar6 != 0) {
      lVar8 = 0x2b8;
    }
    (**(code **)(*param_1 + lVar8))(param_1);
    iVar2 = FUN_1024dd61c();
    bVar1 = iVar2 == 2;
  }
  else {
    bVar1 = true;
  }
  FUN_101b7c16c(local_50,uVar7,&local_58,bVar1,*(undefined1 *)((long)param_1 + 0xb9));
  return local_50;
}

