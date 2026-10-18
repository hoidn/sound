
void FUN_1026ef0dc(long *param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4,
                  undefined8 *param_5,undefined8 param_6)

{
  int iVar1;
  int *local_58;
  undefined *local_50;
  long *plStack_48;
  
  local_50 = PTR_CallMemberFunc<&ATimeableValue::OnValueChanged>_10652c2e0;
  plStack_48 = param_1;
  FUN_101567bfc(param_1[0x46]);
  local_50 = PTR__lambda___1__ARemoteable__TRemoteableUpdate__106551c78;
  plStack_48 = (long *)0x0;
  FUN_101567bfc(param_1[0x49],param_2,param_3,param_4,&local_50);
  local_58 = (int *)*param_5;
  if (local_58 != (int *)0x0) {
    *local_58 = *local_58 + 1;
  }
  (**(code **)(*param_1 + 0x458))(param_1,param_2,&local_58,param_6);
  if (local_58 != (int *)0x0) {
    iVar1 = *local_58;
    *local_58 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  return;
}

