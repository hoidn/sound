
void FUN_1014c04d0(long *param_1)

{
  bool bVar1;
  int iVar2;
  long *plVar3;
  undefined8 uVar4;
  float fVar5;
  double dVar6;
  
  plVar3 = (long *)FUN_1014766b4(param_1,"FollowAction");
  if (plVar3 == (long *)0x0) {
    bVar1 = true;
    plVar3 = (long *)(**(code **)(*param_1 + 0x80))(param_1,"FollowAction",1,"FollowAction");
    (**(code **)(*plVar3 + 0x80))(plVar3,"RemoteableDouble",1,"FollowTime");
    FUN_1014f7548(0x4010000000000000);
    uVar4 = (**(code **)(*plVar3 + 0x80))(plVar3,"RangedRemoteableInt",1,"LoopIterations");
    FUN_1014f75e0(uVar4,1);
    uVar4 = (**(code **)(*plVar3 + 0x80))(plVar3,"RemoteableEnum",1,"FollowActionA");
    FUN_1014f75e0(uVar4,0);
    uVar4 = (**(code **)(*plVar3 + 0x80))(plVar3,"RemoteableEnum",1,"FollowActionB");
    FUN_1014f75e0(uVar4,0);
    (**(code **)(*plVar3 + 0x80))(plVar3,"UserFloat",1,"FollowChanceA");
    FUN_1014f7678(0x42c80000);
    (**(code **)(*plVar3 + 0x80))(plVar3,"UserFloat",1,"FollowChanceB");
    FUN_1014f7678(0);
    uVar4 = (**(code **)(*plVar3 + 0x80))(plVar3,"RemoteableBool",1,"FollowActionEnabled");
    FUN_1014f78d8(uVar4,0);
    (**(code **)(*plVar3 + 0x80))(plVar3,"UserFloat",1,"JumpIndexA");
    FUN_1014f7678(0x3f800000);
    (**(code **)(*plVar3 + 0x80))(plVar3,"UserFloat",1,"JumpIndexB");
    FUN_1014f7678(0x3f800000);
    goto LAB_1014c0768;
  }
  (**(code **)(*plVar3 + 0x48))(plVar3,"FollowActionEnabled/Value");
  bVar1 = AAbstractNode::GetValue<bool>();
  if (bVar1) {
LAB_1014c0580:
    bVar1 = false;
  }
  else {
    (**(code **)(*plVar3 + 0x48))(plVar3,"FollowTime/Value");
    dVar6 = AAbstractNode::GetValue<double>();
    if (dVar6 != 4.0) goto LAB_1014c0580;
    (**(code **)(*plVar3 + 0x48))(plVar3,"FollowActionA/Value");
    iVar2 = AAbstractNode::GetValue<int>();
    if (iVar2 != 4) goto LAB_1014c0580;
    (**(code **)(*plVar3 + 0x48))(plVar3,"FollowActionB/Value");
    iVar2 = AAbstractNode::GetValue<int>();
    if (iVar2 != 0) goto LAB_1014c0580;
    (**(code **)(*plVar3 + 0x48))(plVar3,"FollowChanceA/Value");
    fVar5 = AAbstractNode::GetValue<float>();
    if (fVar5 != 100.0) goto LAB_1014c0580;
    (**(code **)(*plVar3 + 0x48))(plVar3,"FollowChanceB/Value");
    fVar5 = AAbstractNode::GetValue<float>();
    bVar1 = fVar5 == 0.0;
  }
  iVar2 = (**(code **)(*plVar3 + 0x70))(plVar3,"IsLinked");
  if (iVar2 != 0) {
    (**(code **)(*plVar3 + 0xc0))(plVar3,"IsLinked");
  }
LAB_1014c0768:
  uVar4 = (**(code **)(*plVar3 + 0x80))(plVar3,"RemoteableBool",1,"IsLinked");
  FUN_1014f78d8(uVar4,bVar1);
  return;
}

