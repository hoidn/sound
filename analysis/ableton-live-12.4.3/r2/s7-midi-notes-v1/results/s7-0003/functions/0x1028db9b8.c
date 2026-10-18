
void FUN_1028db9b8(undefined8 *param_1,undefined8 *param_2,long param_3)

{
  long lVar1;
  undefined8 uVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  
  lVar1 = FUN_101569984(*(undefined8 *)(param_3 + 0x30));
  FUN_10156998c(*(undefined8 *)(param_3 + 0x30),lVar1 + 1);
  uVar2 = *param_2;
  uVar4 = param_2[3];
  uVar3 = param_2[2];
  param_1[1] = param_2[1];
  *param_1 = uVar2;
  param_1[3] = uVar4;
  param_1[2] = uVar3;
  *(undefined2 *)(param_1 + 4) = *(undefined2 *)(param_2 + 4);
  param_1[5] = lVar1;
  return;
}

