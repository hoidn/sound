
void FUN_1026ec1cc(long param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4)

{
  undefined *local_40;
  long lStack_38;
  
  local_40 = PTR_CallMemberFunc<&ATimeableValue::OnValueChanged>_10652c2e0;
  lStack_38 = param_1;
  FUN_101564728(*(undefined8 *)(param_1 + 0x230),param_2,&local_40);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x230),1);
  (**(code **)(**(long **)(param_1 + 0x230) + 0x1c8))(*(long **)(param_1 + 0x230),param_3);
  local_40 = PTR_CallMemberFunc<&ATimeableBool::ValueChangedController>_10652b938;
  lStack_38 = param_1;
  FUN_101564768(*(undefined8 *)(param_1 + 0x230),&local_40);
  local_40 = PTR__lambda___1__ARemoteable__TRemoteableUpdate__106551c78;
  lStack_38 = 0;
  FUN_101564728(*(undefined8 *)(param_1 + 0x248),param_2,&local_40);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x248),1);
  FUN_1026fc44c(param_1,param_4);
  FUN_1026ec2b4(param_1,param_2);
  FUN_1026ec0c8(*(undefined8 *)(param_1 + 0x218));
  *(int *)(*(long *)(param_1 + 0x230) + 0x88) = (int)param_2;
  FUN_1024dd2ec(*(undefined8 *)(param_1 + 0x260));
  FUN_1026fe704(param_1);
  return;
}

