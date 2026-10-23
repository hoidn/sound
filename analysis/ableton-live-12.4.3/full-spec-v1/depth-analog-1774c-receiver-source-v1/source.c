
undefined8 * FUN_0001774c(undefined8 *param_1)

{
  undefined8 uVar1;
  
  *param_1 = &DAT_00059338;
  param_1[1] = 0;
  param_1[2] = &DAT_00059400;
  param_1[3] = &DAT_00059460;
  param_1[0x1c005] = 0;
  param_1[0x1c004] = 0;
  FUN_0001b138(param_1 + 0x1c006);
  param_1[0x1c006] = &DAT_00059690;
  *(undefined1 *)(param_1 + 0x1c00f) = 0;
  param_1[0x1c00e] = 0;
  param_1[0x1c00d] = 0;
  param_1[0x1c00c] = 0;
  param_1[0x1c00b] = 0;
  *(undefined4 *)((long)param_1 + 0xe007c) = 0x472c4400;
  uVar1 = FUN_0001ac0c();
  param_1[0x1c005] = uVar1;
  FUN_0001b058(uVar1,0);
  FUN_0001b0fc(param_1[0x1c005],1);
  return param_1;
}

