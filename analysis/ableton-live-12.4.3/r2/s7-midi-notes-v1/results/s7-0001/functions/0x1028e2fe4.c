
ulong FUN_1028e2fe4(long param_1,float *param_2)

{
  ulong uVar1;
  
  if ((float *)(param_1 + 0x44) == param_2) {
    return (ulong)(*(float *)(param_1 + 0x44) == 0.0);
  }
  if ((float *)(param_1 + 0x4c) != param_2) {
    if ((float *)(param_1 + 0x50) != param_2) {
      uVar1 = FUN_101483030();
      return uVar1;
    }
    return (ulong)(*(byte *)(param_1 + 0x50) & 1);
  }
  return (ulong)(*(float *)(param_1 + 0x4c) == 1.0);
}

