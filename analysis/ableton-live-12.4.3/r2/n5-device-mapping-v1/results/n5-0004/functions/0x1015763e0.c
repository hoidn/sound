
float FUN_1015763e0(float param_1,float param_2,float param_3,long param_4)

{
  float fVar1;
  double dVar2;
  
  if (0.0 < param_1) {
    dVar2 = (double)_log10((double)param_1 / (double)*(float *)(param_4 + 0x28));
    fVar1 = (float)(dVar2 / *(double *)(param_4 + 0x40));
    if (fVar1 <= param_3) {
      param_3 = fVar1;
    }
    if (param_2 <= fVar1) {
      param_2 = param_3;
    }
  }
  return param_2;
}

