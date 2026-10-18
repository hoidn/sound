
float FUN_101b7b96c(float param_1,int param_2)

{
  uint uVar1;
  int iVar2;
  int iVar3;
  float fVar4;
  
  iVar2 = (int)param_1;
  if (param_2 < 6) {
    param_1 = 0.0;
    if (param_2 < 3) {
      if (param_2 == 1) {
        iVar3 = -0x41;
        if (iVar2 < 0x41) {
          iVar3 = -1;
        }
        uVar1 = iVar3 + iVar2;
        fVar4 = 20.0;
        if ((-1 < (int)uVar1) &&
           (fVar4 = 20.0, (int)uVar1 < (int)((ulong)(DAT_106fba2c8 - DAT_106fba2c0) >> 2))) {
          fVar4 = *(float *)(DAT_106fba2c0 + (ulong)uVar1 * 4);
        }
        iVar3 = -1;
        if (iVar2 < 0x41) {
          iVar3 = 1;
        }
        return fVar4 * (float)iVar3;
      }
      if (param_2 == 2) {
        uVar1 = iVar2 - 0x41;
        if (iVar2 < 0x40) {
          uVar1 = 0x3f - iVar2;
        }
        if ((-1 < (int)uVar1) && ((int)uVar1 < (int)((ulong)(DAT_106fba2b0 - DAT_106fba2a8) >> 2)))
        {
          iVar3 = -1;
          if (0x3f < iVar2) {
            iVar3 = 1;
          }
          return *(float *)(DAT_106fba2a8 + (ulong)uVar1 * 4) * (float)iVar3;
        }
        iVar3 = -1;
        if (0x3f < iVar2) {
          iVar3 = 1;
        }
        return (float)iVar3 * 50.0;
      }
    }
    else {
      if (param_2 == 3) {
        uVar1 = iVar2 - 1;
        if (0x41 < iVar2) {
          uVar1 = 0x7f - iVar2;
        }
        if ((-1 < (int)uVar1) && ((int)uVar1 < (int)((ulong)(DAT_106fba2b0 - DAT_106fba2a8) >> 2)))
        {
          iVar3 = -1;
          if (iVar2 < 0x42) {
            iVar3 = 1;
          }
          return *(float *)(DAT_106fba2a8 + (ulong)uVar1 * 4) * (float)iVar3;
        }
        iVar3 = -1;
        if (iVar2 < 0x42) {
          iVar3 = 1;
        }
        return (float)iVar3 * 50.0;
      }
      if (param_2 == 4) {
        iVar3 = -0x41;
        if (iVar2 < 0x41) {
          iVar3 = -1;
        }
        uVar1 = iVar3 + iVar2;
        if ((-1 < (int)uVar1) && ((int)uVar1 < (int)((ulong)(DAT_106fba2b0 - DAT_106fba2a8) >> 2)))
        {
          iVar3 = -1;
          if (0x40 < iVar2) {
            iVar3 = 1;
          }
          return *(float *)(DAT_106fba2a8 + (ulong)uVar1 * 4) * (float)iVar3;
        }
        iVar3 = -1;
        if (0x40 < iVar2) {
          iVar3 = 1;
        }
        return (float)iVar3 * 50.0;
      }
    }
  }
  else {
    if (param_2 < 8) {
      if (param_2 != 6) {
        fVar4 = param_1 + -64.0;
        if (param_2 != 7) {
          fVar4 = 0.0;
        }
        return fVar4;
      }
      fVar4 = 64.0 - param_1;
    }
    else {
      if (param_2 != 8) {
        if (param_2 != 9) {
          return 0.0;
        }
        fVar4 = -param_1;
        if (0x40 < iVar2) {
          fVar4 = param_1 + -64.0;
        }
        return fVar4;
      }
      fVar4 = param_1 + -128.0;
    }
    if (0x40 < iVar2) {
      param_1 = fVar4;
    }
  }
  return param_1;
}

