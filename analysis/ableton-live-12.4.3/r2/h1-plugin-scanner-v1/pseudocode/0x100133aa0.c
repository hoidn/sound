
undefined8
FUN_100133aa0(undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4,
             undefined4 param_5)

{
  int iVar1;
  undefined8 uVar2;
  int *local_70;
  undefined **local_68;
  int *local_60;
  undefined8 local_58;
  undefined4 local_50;
  undefined4 uStack_4c;
  undefined **local_48;
  
  local_48 = &PTR_FUN_100b43b78;
  FUN_100437728(&local_70,L"VST3");
  local_68 = &PTR_FUN_100b43b10;
  local_60 = local_70;
  local_58 = param_1;
  uStack_4c = param_5;
  if (local_70 == (int *)0x0) {
    local_50 = 0;
  }
  else {
    local_50 = 0;
    if (*local_70 == 0) {
      FUN_100454b40();
    }
  }
  uVar2 = FUN_1005e9fd8(param_2,param_3,param_4,&local_48,&local_68);
  local_68 = &PTR_FUN_100b43b10;
  if (local_60 != (int *)0x0) {
    iVar1 = *local_60;
    *local_60 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_100454b40();
    }
  }
  return uVar2;
}

