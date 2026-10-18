
float FUN_101b7c508(float param_1,float param_2,float param_3,float param_4,float param_5,
                   undefined8 param_6,int param_7,undefined8 param_8,undefined8 param_9)

{
  float fVar1;
  bool bVar2;
  bool bVar3;
  float fVar4;
  float fVar5;
  float fVar6;
  float fVar7;
  float fVar8;
  float local_60 [2];
  int iStack_58;
  undefined4 local_54;
  
  fVar7 = param_5;
  if (param_1 <= param_5) {
    fVar7 = param_1;
  }
  fVar1 = param_4;
  if (param_4 <= param_1) {
    fVar1 = fVar7;
  }
  fVar7 = param_2;
  if (DAT_106fb2110 != 0) {
    local_60[1] = 3.4028235e+38;
    local_54 = 0x3f800000;
    fVar7 = fVar1;
    if ((param_3 != -129.0) &&
       (local_60[0] = param_3, iStack_58 = param_7,
       fVar4 = (float)FUN_101b76bf0(fVar1,param_4,param_5,local_60,param_9), fVar4 != -129.0)) {
      fVar5 = param_5 - param_4;
      fVar6 = 16384.0;
      if (param_7 != 5) {
        fVar6 = 128.0;
      }
      fVar7 = (fVar5 * 0.5) / fVar6;
      fVar8 = fVar1 + fVar7;
      bVar2 = true;
      bVar3 = false;
      if (fVar1 - fVar7 <= fVar4) {
        bVar2 = false;
        bVar3 = true;
        if (!NAN(fVar8) && !NAN(fVar4)) {
          bVar2 = fVar8 < fVar4;
          bVar3 = false;
        }
      }
      fVar7 = param_2;
      if (bVar2 != bVar3) {
        if (DAT_106fb2110 == 2) {
          fVar6 = (fVar5 + fVar5) / fVar6;
          fVar7 = fVar1 + fVar6;
          bVar2 = true;
          bVar3 = false;
          if (fVar1 - fVar6 <= param_2) {
            bVar2 = false;
            bVar3 = true;
            if (!NAN(fVar7) && !NAN(param_2)) {
              bVar2 = fVar7 < param_2;
              bVar3 = false;
            }
          }
          fVar7 = param_2;
          if ((bVar2 != bVar3) && (fVar7 = fVar1, fVar4 != param_2)) {
            fVar7 = (param_5 - fVar1) * ((param_2 - fVar4) / (param_5 - fVar4));
            fVar6 = (fVar1 - param_4) * ((fVar4 - param_2) / (fVar4 - param_4));
            bVar2 = fVar7 < 0.0;
            if (param_2 < fVar4) {
              bVar2 = 0.0 < fVar6;
              fVar7 = fVar6;
            }
            fVar4 = -1.0;
            if (!bVar2) {
              fVar4 = 1.0;
            }
            fVar7 = fVar1 + fVar4 * fVar7;
          }
        }
        else if (DAT_106fb2110 == 1) {
          fVar7 = (float)FUN_101b7c344(fVar1,param_2,fVar4,param_4,param_5,param_6,param_7 == 5);
        }
      }
    }
  }
  if (fVar7 <= param_5) {
    param_5 = fVar7;
  }
  if (param_4 <= fVar7) {
    param_4 = param_5;
  }
  return param_4;
}

