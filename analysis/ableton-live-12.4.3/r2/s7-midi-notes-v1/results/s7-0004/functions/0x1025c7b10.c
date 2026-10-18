
ulong FUN_1025c7b10(long param_1,double *param_2)

{
  ulong uVar1;
  
  if (((((double *)(param_1 + 0x40) != param_2) && ((double *)(param_1 + 0x48) != param_2)) &&
      ((double *)(param_1 + 0x50) != param_2)) && ((double *)(param_1 + 0x58) != param_2)) {
    uVar1 = FUN_101483030();
    return uVar1;
  }
  return (ulong)(*param_2 == 0.5);
}

