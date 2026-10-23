
undefined8 * FUN_00015860(undefined8 *param_1)

{
  *param_1 = &DAT_0005d5c0;
  param_1[1] = 0;
  *(undefined4 *)(param_1 + 2) = 0x472c4400;
  param_1[3] = 0x2c;
  *(undefined4 *)(param_1 + 4) = 0;
  param_1[0x405] = 0x401;
  param_1[0x807] = 0;
  param_1[0x806] = 0;
  FUN_000162ec(param_1 + 0x808,0x400);
  return param_1;
}

