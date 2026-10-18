
void FUN_101afb494(long param_1)

{
  undefined8 uVar1;
  undefined4 local_44;
  undefined4 local_40;
  undefined4 local_3c;
  undefined4 local_38;
  undefined4 local_34;
  undefined4 local_30;
  undefined4 local_2c;
  undefined4 local_28;
  undefined4 local_24;
  
  uVar1 = FUN_101aff570(0,*(undefined4 *)(param_1 + 0x10));
  uVar1 = FUN_101aff570(uVar1,*(undefined4 *)(param_1 + 0x28));
  uVar1 = FUN_101aff570(uVar1,*(undefined4 *)(param_1 + 0x40));
  uVar1 = FUN_101aff570(uVar1,*(undefined4 *)(param_1 + 0x58));
  uVar1 = FUN_101aff570(uVar1,*(undefined4 *)(param_1 + 0x70));
  local_34 = FUN_101aff494(param_1,uVar1);
  local_30 = FUN_101aff494(param_1 + 0x18,uVar1);
  local_2c = FUN_101aff494(param_1 + 0x30,uVar1);
  local_28 = FUN_101aff494(param_1 + 0x48,uVar1);
  local_24 = FUN_101aff494(param_1 + 0x60,uVar1);
  FUN_101b3b95c(param_1 + 0xd8,&local_34,&local_44);
  FUN_101aff3a0(local_44,param_1 + 0x78,uVar1);
  FUN_101aff3a0(local_40,param_1 + 0x90,uVar1);
  FUN_101aff3a0(local_3c,param_1 + 0xa8,uVar1);
  FUN_101aff3a0(local_38,param_1 + 0xc0,uVar1);
  return;
}

