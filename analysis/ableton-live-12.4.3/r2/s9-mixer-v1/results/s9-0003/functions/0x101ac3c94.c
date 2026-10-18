
ulong FUN_101ac3c94(ulong param_1,ulong param_2)

{
  ulong uVar1;
  long lVar2;
  float *pfVar3;
  float *pfVar4;
  ulong uVar5;
  ulong uVar6;
  
  if ((DAT_106f7e914 & 1) == 0) {
    lVar2 = FUN_101ab9e24(10);
    pfVar3 = *(float **)(*(long *)(lVar2 + (param_2 & 0xffffffff) * 8 + 8) + 0x30);
    uVar5 = 0x65;
    pfVar4 = pfVar3;
    do {
      uVar6 = uVar5 >> 1;
      uVar1 = uVar5 + ~uVar6;
      uVar5 = uVar6;
      if (pfVar4[uVar6] <= (float)param_1) {
        uVar5 = uVar1;
        pfVar4 = pfVar4 + uVar6 + 1;
      }
    } while (uVar5 != 0);
    if ((long)pfVar4 - (long)pfVar3 == 0) {
      param_1 = 0;
    }
    else if (pfVar4 == pfVar3 + 0x65) {
      param_1 = 0x3f800000;
    }
    else {
      param_1 = (ulong)(uint)((((float)param_1 - pfVar4[-1]) / (*pfVar4 - pfVar4[-1]) +
                              (float)(((long)pfVar4 - (long)pfVar3 >> 2) + -1)) * 0.01);
    }
  }
  return param_1;
}

