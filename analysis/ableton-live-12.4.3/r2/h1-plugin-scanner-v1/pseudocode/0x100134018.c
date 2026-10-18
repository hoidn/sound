
undefined8
FUN_100134018(undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4,
             undefined8 param_5,undefined4 param_6)

{
  int iVar1;
  undefined8 uVar2;
  int *local_98;
  undefined **local_90;
  int *local_88;
  undefined8 local_80;
  undefined4 local_78;
  undefined4 uStack_74;
  undefined **local_70;
  void *local_68 [2];
  char local_51;
  
  local_70 = &PTR_FUN_100b43ab8;
  FUN_10043c3b0(local_68,param_4);
  FUN_100437728(&local_98,L"VST2");
  local_90 = &PTR_FUN_100b43b10;
  local_88 = local_98;
  local_80 = param_1;
  uStack_74 = param_6;
  if (local_98 == (int *)0x0) {
    local_78 = 0;
  }
  else {
    local_78 = 0;
    if (*local_98 == 0) {
      FUN_100454b40();
    }
  }
  uVar2 = FUN_1005aca28(param_2,param_3,param_5,&local_70,&local_90);
  local_90 = &PTR_FUN_100b43b10;
  if (local_88 != (int *)0x0) {
    iVar1 = *local_88;
    *local_88 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_100454b40();
    }
  }
  local_70 = &PTR_FUN_100b43ab8;
  if (local_51 < '\0') {
    operator_delete(local_68[0]);
  }
  return uVar2;
}

