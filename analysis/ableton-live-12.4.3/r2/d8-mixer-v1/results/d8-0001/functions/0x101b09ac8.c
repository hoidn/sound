
float FUN_101b09ac8(float param_1,float param_2,char *param_3)

{
  char cVar1;
  float fVar2;
  float fVar3;
  float fVar4;
  
  cVar1 = *param_3;
  if (cVar1 == '\x02') {
    if (param_3[1] != '\x02') {
      if (param_3[1] != '\0') {
        return 0.0;
      }
      param_2 = *(float *)(param_3 + 0x10) *
                (param_2 - *(float *)(param_3 + 0x1c)) * *(float *)(param_3 + 0x20);
    }
    param_1 = param_1 + param_2;
    fVar4 = *(float *)(param_3 + 4);
    fVar2 = *(float *)(param_3 + 8);
  }
  else {
    if (cVar1 != '\x01') {
      if (cVar1 != '\0') {
        return 0.0;
      }
      fVar2 = (param_2 - *(float *)(param_3 + 0x14)) * *(float *)(param_3 + 0x20);
      return *(float *)(param_3 + 4) * (1.0 - fVar2) + fVar2 * param_1;
    }
    if (param_1 <= *(float *)(param_3 + 0xc)) {
      fVar3 = *(float *)(param_3 + 0x24) * (param_2 - *(float *)(param_3 + 0x14));
      fVar4 = *(float *)(param_3 + 4);
      fVar2 = *(float *)(param_3 + 8);
      param_1 = fVar4 * (1.0 - fVar3) + fVar3 * param_1;
    }
    else {
      fVar3 = *(float *)(param_3 + 0x24) * (*(float *)(param_3 + 0x18) - param_2);
      fVar4 = *(float *)(param_3 + 4);
      fVar2 = *(float *)(param_3 + 8);
      param_1 = fVar3 * param_1 + (1.0 - fVar3) * fVar2;
    }
  }
  if (param_1 <= fVar2) {
    fVar2 = param_1;
  }
  if (fVar4 <= param_1) {
    fVar4 = fVar2;
  }
  return fVar4;
}

