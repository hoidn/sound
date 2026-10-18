
float FUN_101577e70(float param_1,float param_2,float param_3,long param_4)

{
  bool bVar1;
  float fVar2;
  float fVar3;
  
  fVar2 = *(float *)(param_4 + 0x28);
  fVar3 = *(float *)(param_4 + 0x2c);
  bVar1 = false;
  if ((fVar2 == param_2) && (bVar1 = false, !NAN(fVar3) && !NAN(param_3))) {
    bVar1 = fVar3 == param_3;
  }
  if (!bVar1) {
    fVar2 = (param_1 - fVar2) / (fVar3 - fVar2);
    param_1 = (param_2 - param_2 * fVar2) + param_3 * fVar2;
  }
  if (param_1 <= param_3) {
    param_3 = param_1;
  }
  if (param_2 <= param_1) {
    param_2 = param_3;
  }
  return param_2;
}

