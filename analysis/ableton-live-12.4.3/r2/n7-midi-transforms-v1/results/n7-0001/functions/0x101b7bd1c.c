
float FUN_101b7bd1c(float param_1,float param_2,float *param_3)

{
  int iVar1;
  float fVar2;
  
  if (param_3[2] == 0.0 || param_3[2] == 7.00649e-45) {
    if (((DAT_106fba130 & 1) == 0) && (iVar1 = ___cxa_guard_acquire(&DAT_106fba130), iVar1 != 0)) {
      DAT_106fba128 = (float)FUN_1011afc2c(0);
      ___cxa_guard_release(&DAT_106fba130);
    }
    return (*param_3 - param_3[1]) * ((param_2 - param_1) / DAT_106fba128);
  }
  fVar2 = (float)FUN_101b7b96c(*param_3);
  return (param_2 - param_1) * fVar2 * param_3[3] * 0.00390625;
}

