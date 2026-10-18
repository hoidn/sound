
ulong FUN_102778828(long param_1,double *param_2)

{
  ulong uVar1;
  
  if (((((double *)(param_1 + 0x60) != param_2) && ((double *)(param_1 + 0x68) != param_2)) &&
      ((double *)(param_1 + 0x70) != param_2)) && ((double *)(param_1 + 0x78) != param_2)) {
    uVar1 = FUN_101483030();
    return uVar1;
  }
  return (ulong)(*param_2 == 0.5);
}

