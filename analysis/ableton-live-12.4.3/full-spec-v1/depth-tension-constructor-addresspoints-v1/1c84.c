
long FUN_00001c84(long param_1)

{
  undefined8 *puVar1;
  
  puVar1 = (undefined8 *)FUN_000136d0();
  *puVar1 = &DAT_0005c0c0;
  *(undefined8 *)(param_1 + 0xe0080) = &DAT_0005c188;
  *(undefined8 *)(param_1 + 0xe0090) = 0;
  *(undefined8 *)(param_1 + 0xe0098) = 0;
  *(undefined8 *)(param_1 + 0xe00a0) = 0;
  *(undefined8 *)(param_1 + 0xe00d8) = &DAT_0005c188;
  *(undefined8 *)(param_1 + 0xe00e8) = 0;
  *(undefined8 *)(param_1 + 0xe00f0) = 0;
  *(undefined8 *)(param_1 + 0xe00f8) = 0;
  FUN_00019db8(0x3a83126f,0x3f800000,0x3ba3d70a,(undefined8 *)(param_1 + 0xe0080),0,"",0);
  FUN_00019db8(0x3b03126f,0x3dcccccd,0x3ba3d70a,(undefined8 *)(param_1 + 0xe00d8),0,"",0);
  return param_1;
}

