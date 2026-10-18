
void FUN_1014b8b00(long *param_1)

{
  bool bVar1;
  int iVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  double dVar5;
  
  (**(code **)(*param_1 + 0x48))(param_1,"FollowActionEnabled/Value");
  bVar1 = AAbstractNode::GetValue<bool>();
  if (!bVar1) {
    (**(code **)(*param_1 + 0x48))(param_1,"FollowActionA/Value");
    iVar2 = AAbstractNode::GetValue<int>();
    if (iVar2 == 0) {
      (**(code **)(*param_1 + 0x48))(param_1,"FollowActionB/Value");
      iVar2 = AAbstractNode::GetValue<int>();
      if (iVar2 == 0) {
        (**(code **)(*param_1 + 0x48))(param_1,"FollowTime/Value");
        dVar5 = AAbstractNode::GetValue<double>();
        if (dVar5 == 4.0) {
          iVar2 = (**(code **)(*param_1 + 0x48))(param_1,"FollowActionA/Value");
          AAbstractNode::SetValue<int>(iVar2);
          uVar4 = 1;
          goto LAB_1014b8b70;
        }
      }
    }
  }
  uVar4 = 0;
LAB_1014b8b70:
  uVar3 = (**(code **)(*param_1 + 0x80))(param_1,"RemoteableBool",1,"IsLinked");
  FUN_1014f78d8(uVar3,uVar4);
  return;
}

