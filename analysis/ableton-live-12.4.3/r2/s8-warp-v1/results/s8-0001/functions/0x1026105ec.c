
undefined8 * FUN_1026105ec(undefined8 *param_1)

{
  undefined8 *puVar1;
  undefined *local_40;
  undefined8 *puStack_38;
  
  puVar1 = (undefined8 *)FUN_10155dc80();
  *puVar1 = &PTR_FUN_1067e6d10;
  FUN_101458fc8(puVar1 + 0xd,0);
  param_1[0xd] = &DAT_1067e8bd0;
  FUN_101486414(param_1);
  param_1[0xb] = &DAT_7fefffffffffffff;
  param_1[10] = &DAT_7fefffffffffffff;
  *(undefined4 *)(param_1 + 0xc) = 0x80000000;
  param_1[0x11] = 0;
  *param_1 = &PTR_FUN_1067e6f08;
  FUN_101486414(param_1);
  local_40 = PTR_CallMemberFunc<&AWarpMarker::OnValueChanged>_10652a8a0;
  puStack_38 = param_1;
  FUN_10155e028(param_1,&local_40);
  return param_1;
}

