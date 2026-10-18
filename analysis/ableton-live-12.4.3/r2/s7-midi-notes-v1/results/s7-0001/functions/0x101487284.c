
void FUN_101487284(long *param_1,undefined8 param_2,undefined8 param_3)

{
  int iVar1;
  undefined8 uVar2;
  
  FUN_1011b5224();
  (**(code **)(*param_1 + 200))(param_1);
  (**(code **)(*param_1 + 0x140))(param_1,param_2,param_3);
  iVar1 = FUN_1015192c0(param_3);
  if (iVar1 != 0) {
    uVar2 = FUN_1015183fc(param_3);
                    /* WARNING: Could not recover jumptable at 0x0001014872fc. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (**(code **)(*param_1 + 0xd0))(param_1,uVar2);
    return;
  }
  return;
}

