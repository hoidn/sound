// 0x10141f8b4 FUN_10141f8b4 exported  sig: undefined FUN_10141f8b4()

void FUN_10141f8b4(long param_1,undefined8 param_2)

{
  undefined *puVar1;
  undefined *local_40;
  long lStack_38;
  
  puVar1 = PTR_CallMemberFunc<&TOneShotTimer::OnTimer>_10652bfa0;
  if (*(int *)(param_1 + 0x18) == 1) {
    local_40 = PTR_CallMemberFunc<&TOneShotTimer::OnTimer>_10652bfa0;
    lStack_38 = param_1;
    FUN_101447ec0(&local_40);
    *(undefined4 *)(param_1 + 0x18) = 0;
  }
  if (*(long *)(param_1 + 0x28) != 0) {
    local_40 = puVar1;
    lStack_38 = param_1;
    FUN_101447d84(param_2,&local_40,"TOneShotTimer");
    *(undefined4 *)(param_1 + 0x18) = 1;
  }
  return;
}


