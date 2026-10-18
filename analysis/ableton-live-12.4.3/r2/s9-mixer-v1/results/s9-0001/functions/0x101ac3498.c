
float FUN_101ac3498(float param_1,long param_2)

{
  float *pfVar1;
  int iVar2;
  double dVar3;
  double dVar4;
  
  if (param_1 <= 0.0) {
    return **(float **)(param_2 + 0x30);
  }
  if (param_1 < 1.0) {
    iVar2 = (int)((double)param_1 * 100.0);
    dVar4 = (double)param_1 * 100.0 - (double)iVar2;
    dVar3 = 0.0;
    if ((7.62939453125e-06 < dVar4) && (dVar3 = dVar4, 0.9999923706054688 <= dVar4)) {
      dVar3 = 1.0;
    }
    pfVar1 = (float *)(*(long *)(param_2 + 0x30) + (long)iVar2 * 4);
    return (float)(dVar3 * (double)pfVar1[1] + (1.0 - dVar3) * (double)*pfVar1);
  }
  return *(float *)(*(long *)(param_2 + 0x30) + 400);
}

