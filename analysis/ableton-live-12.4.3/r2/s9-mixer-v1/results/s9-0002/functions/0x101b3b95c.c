
void FUN_101b3b95c(undefined8 param_1,float *param_2,float *param_3)

{
  double dVar1;
  double dVar2;
  double dVar3;
  double dVar4;
  double dVar5;
  double dVar6;
  float fVar7;
  float fVar8;
  float fVar9;
  float fVar10;
  double dVar11;
  float fVar12;
  float fVar13;
  
  fVar12 = param_2[4];
  fVar13 = 0.0;
  fVar9 = 0.0;
  fVar10 = 0.0;
  fVar7 = 0.0;
  if (fVar12 != 0.0) {
    fVar13 = param_2[3];
    dVar11 = (double)param_2[2] * 0.7853981633974483 + 0.7853981633974483;
    dVar1 = (double)_cos(dVar11);
    dVar2 = (double)_cos(1.5707963267948966 - dVar11);
    dVar11 = (double)fVar13 * 0.7853981633974483 + 0.7853981633974483;
    dVar3 = (double)_cos(dVar11);
    dVar4 = (double)_cos(1.5707963267948966 - dVar11);
    dVar11 = (double)param_2[1] * 0.7853981633974483 + 0.7853981633974483;
    dVar5 = (double)_cos(dVar11);
    dVar6 = (double)_cos(1.5707963267948966 - dVar11);
    dVar11 = 1e-05;
    if (1e-05 <= dVar5 * 1.4142135623730951) {
      dVar11 = dVar5 * 1.4142135623730951;
    }
    dVar5 = 1e-05;
    if (1e-05 <= dVar6 * 1.4142135623730951) {
      dVar5 = dVar6 * 1.4142135623730951;
    }
    fVar7 = *param_2;
    fVar8 = 1.0 - fVar7;
    fVar13 = fVar12 * (fVar7 * (float)dVar1 + fVar8 * (float)dVar11);
    fVar9 = fVar12 * (fVar8 * 0.0 + fVar7 * (float)dVar2);
    fVar10 = fVar12 * (fVar8 * 0.0 + fVar7 * (float)dVar3);
    fVar7 = fVar12 * (fVar7 * (float)dVar4 + fVar8 * (float)dVar5);
  }
  *param_3 = fVar13;
  param_3[1] = fVar9;
  param_3[2] = fVar10;
  param_3[3] = fVar7;
  return;
}

