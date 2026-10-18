
void FUN_1026f0bcc(undefined4 param_1,undefined4 param_2,undefined4 param_3,long *param_4,
                  undefined8 param_5,undefined8 param_6,undefined8 param_7,undefined8 param_8,
                  undefined8 param_9)

{
  undefined8 uVar1;
  long lVar2;
  undefined4 uVar3;
  undefined4 uVar4;
  undefined *local_80;
  long *plStack_78;
  
  local_80 = PTR_CallMemberFunc<&ATimeableFloat::OnValueChanged>_10652c2c8;
  plStack_78 = param_4;
  FUN_10157432c(param_4[0x46],param_6,&local_80);
  FUN_10155baa4(param_4[0x46],1);
  (**(code **)(*(long *)param_4[0x46] + 0x1c8))((long *)param_4[0x46],param_8);
  local_80 = PTR_CallMemberFunc<&ATimeableFloat::ValueChangedController>_10652c2d0;
  plStack_78 = param_4;
  FUN_101568990(param_4[0x46],&local_80);
  local_80 = PTR__lambda___1__ARemoteable__TRemoteableUpdate__106551c78;
  plStack_78 = (long *)0x0;
  FUN_101568960(param_3,param_4[0x49],&local_80);
  FUN_10155baa4(param_4[0x49],1);
  lVar2 = param_4[0x43];
  uVar3 = FUN_10157486c(param_4[0x46]);
  uVar4 = FUN_101574874(param_4[0x46]);
  uVar1 = FUN_101574630(param_4[0x46]);
  FUN_1025856a0(param_1,param_2,uVar3,uVar4,lVar2,uVar1);
  FUN_1026fe704(param_4);
  FUN_1026fc44c(param_4,param_7);
  FUN_1026f0d84(param_3,param_4);
  FUN_1024dd2ec(param_4[0x4d]);
  lVar2 = param_4[0x50];
  *(long **)(lVar2 + 0xb8) = param_4;
  uVar3 = (**(code **)(*param_4 + 0x2f0))(param_4);
  uVar4 = (**(code **)(*param_4 + 0x2f8))(param_4);
  uVar1 = (**(code **)(*param_4 + 800))(param_4);
  FUN_1025b9d70(uVar3,uVar4,lVar2,param_5,param_9,uVar1);
  FUN_10260d93c(param_4[0x1a],1);
  return;
}

