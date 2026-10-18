
float FUN_101b76bf0(float param_1,float param_2,float param_3,float *param_4,int param_5,int param_6
                   )

{
  int iVar1;
  float fVar2;
  float fVar3;
  
  fVar3 = param_4[2];
  if (fVar3 == 0.0 || fVar3 == 7.00649e-45) {
    fVar3 = *param_4;
    if (((DAT_106fba140 & 1) == 0) && (iVar1 = ___cxa_guard_acquire(&DAT_106fba140), iVar1 != 0)) {
      DAT_106fba12c = (float)FUN_1011afc2c(0);
      ___cxa_guard_release(&DAT_106fba140);
    }
    fVar2 = DAT_106fba12c - fVar3;
    if (param_6 == 0) {
      fVar2 = fVar3;
    }
    param_2 = param_2 * (1.0 - fVar2 / DAT_106fba12c) + (fVar2 / DAT_106fba12c) * param_3;
  }
  else {
    fVar2 = (float)FUN_101b7b96c(*param_4,fVar3);
    fVar3 = 1.0;
    if (fVar2 * param_4[3] <= 0.0) {
      fVar3 = -1.0;
    }
    if (param_5 == 0) {
      fVar3 = (param_3 - param_2) * 0.00390625 * fVar2 * param_4[3];
    }
    fVar2 = -fVar3;
    if (param_6 == 0) {
      fVar2 = fVar3;
    }
    fVar2 = fVar2 + param_1;
    if (fVar2 <= param_3) {
      param_3 = fVar2;
    }
    if (param_2 <= fVar2) {
      param_2 = param_3;
    }
  }
  fVar3 = (float)(int)param_2;
  if (param_5 == 0) {
    fVar3 = param_2;
  }
  return fVar3;
}

