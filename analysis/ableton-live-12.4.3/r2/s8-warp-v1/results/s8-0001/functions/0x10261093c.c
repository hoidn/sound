
undefined1  [16] FUN_10261093c(long param_1,long param_2)

{
  double dVar1;
  undefined1 auVar2 [16];
  
  dVar1 = *(double *)(param_2 + 0x50) - *(double *)(param_1 + 0x50);
  if (0.0 < dVar1) {
    auVar2._0_8_ = ((*(double *)(param_2 + 0x58) - *(double *)(param_1 + 0x58)) / dVar1) * 60.0;
    auVar2._8_8_ = 0;
    return auVar2;
  }
  return ZEXT816(0xc04e000000000000);
}

