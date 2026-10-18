
void FUN_1014b82d8(long *param_1)

{
  bool bVar1;
  bool bVar2;
  bool bVar3;
  bool bVar4;
  int iVar5;
  ulong uVar6;
  undefined8 uVar7;
  long lVar8;
  byte bVar9;
  float fVar10;
  
  uVar6 = (**(code **)(*param_1 + 0x70))(param_1,"FollowActionEnabled");
  if ((uVar6 & 1) == 0) {
    uVar7 = FUN_1014766b4(param_1,"FollowActionA");
    lVar8 = FUN_1014766b4(uVar7,"Value");
    if (lVar8 == 0) {
      bVar3 = false;
    }
    else {
      iVar5 = AAbstractNode::GetValue<int>();
      bVar3 = iVar5 != 0;
    }
    uVar7 = FUN_1014766b4(param_1,"FollowActionB");
    lVar8 = FUN_1014766b4(uVar7,"Value");
    if (lVar8 == 0) {
      bVar4 = false;
    }
    else {
      iVar5 = AAbstractNode::GetValue<int>();
      bVar4 = iVar5 != 0;
    }
    uVar7 = FUN_1014766b4(param_1,"FollowChanceA");
    lVar8 = FUN_1014766b4(uVar7,"Value");
    if (lVar8 == 0) {
      bVar1 = false;
    }
    else {
      fVar10 = AAbstractNode::GetValue<float>();
      bVar1 = fVar10 != 0.0;
    }
    uVar7 = FUN_1014766b4(param_1,"FollowChanceB");
    lVar8 = FUN_1014766b4(uVar7,"Value");
    if (lVar8 == 0) {
      bVar2 = false;
    }
    else {
      fVar10 = AAbstractNode::GetValue<float>();
      bVar2 = fVar10 != 0.0;
    }
    if ((bool)(bVar3 & bVar1)) {
      bVar9 = 1;
    }
    else {
      bVar9 = bVar4 & bVar2;
    }
    uVar7 = (**(code **)(*param_1 + 0x80))(param_1,"RemoteableBool",1,"FollowActionEnabled");
    FUN_1014f78d8(uVar7,bVar9);
    return;
  }
  return;
}

