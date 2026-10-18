
void FUN_102fbec58(undefined4 param_1,long param_2,undefined8 param_3)

{
  ulong uVar1;
  undefined1 auStack_60 [16];
  undefined1 auStack_50 [8];
  ulong local_48;
  
  _fegetenv(auStack_60);
  _fegetenv(auStack_50);
  uVar1 = local_48;
  _fegetenv(auStack_50);
  local_48 = local_48 | 0x1000000;
  _fesetenv(auStack_50);
  (**(code **)(param_2 + 0x20))(param_1,*(undefined8 *)(param_2 + 0x10),param_3);
  _fegetenv(auStack_50);
  local_48 = local_48 & (uVar1 | 0xfffffffffeffffff);
  _fesetenv(auStack_50);
  _fesetenv(auStack_60);
  return;
}

