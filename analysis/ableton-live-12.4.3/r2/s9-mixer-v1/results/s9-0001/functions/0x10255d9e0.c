
float FUN_10255d9e0(long param_1)

{
  float fVar1;
  float fVar2;
  float fVar3;
  
  fVar1 = (float)FUN_101ac3bac(*(undefined4 *)(param_1 + 0x28));
  fVar3 = *(float *)(param_1 + 0x30);
  if (fVar1 <= *(float *)(param_1 + 0x30)) {
    fVar3 = fVar1;
  }
  fVar2 = *(float *)(param_1 + 0x2c);
  if (*(float *)(param_1 + 0x2c) <= fVar1) {
    fVar2 = fVar3;
  }
  return fVar2;
}

