
undefined1  [16] FUN_101212e30(double param_1,double *param_2)

{
  undefined1 auVar1 [16];
  undefined1 auVar2 [16];
  double dVar3;
  double dVar4;
  double dVar5;
  double dVar6;
  double dVar7;
  double dVar8;
  
  dVar4 = *param_2;
  dVar5 = param_2[6];
  if (dVar5 <= dVar4) {
    dVar3 = 0.0;
    if ((dVar5 < param_1) && (dVar3 = 1.0, param_1 < dVar4)) {
      dVar7 = param_2[4] * 0.375 + dVar5 * 0.125 + param_2[2] * 0.375 + dVar4 * 0.125;
      dVar3 = 0.5;
      if (1e-08 < ABS(param_1 - dVar7)) {
        dVar6 = 0.0;
        dVar8 = 1.0;
        do {
          if (param_1 <= dVar7) {
            dVar8 = dVar3;
            dVar3 = dVar6;
          }
          dVar6 = dVar3;
          dVar3 = (dVar8 + dVar6) * 0.5;
          dVar7 = 1.0 - dVar3;
          dVar7 = param_2[4] * dVar3 * dVar7 * dVar7 * 3.0 + dVar5 * dVar7 * dVar7 * dVar7 +
                  param_2[2] * dVar3 * dVar3 * dVar7 * 3.0 + dVar4 * dVar3 * dVar3 * dVar3;
        } while (1e-08 < ABS(param_1 - dVar7));
      }
    }
    auVar2._8_8_ = 0;
    auVar2._0_8_ = 1.0 - dVar3;
    return auVar2;
  }
  dVar3 = 0.0;
  if ((dVar4 < param_1) && (dVar3 = 1.0, param_1 < dVar5)) {
    dVar7 = param_2[2] * 0.375 + dVar4 * 0.125 + param_2[4] * 0.375 + dVar5 * 0.125;
    dVar3 = 0.5;
    if (1e-08 < ABS(param_1 - dVar7)) {
      dVar6 = 0.0;
      dVar8 = 1.0;
      do {
        if (param_1 <= dVar7) {
          dVar8 = dVar3;
          dVar3 = dVar6;
        }
        dVar6 = dVar3;
        dVar3 = (dVar8 + dVar6) * 0.5;
        dVar7 = 1.0 - dVar3;
        dVar7 = param_2[2] * dVar3 * dVar7 * dVar7 * 3.0 + dVar4 * dVar7 * dVar7 * dVar7 +
                param_2[4] * dVar3 * dVar3 * dVar7 * 3.0 + dVar5 * dVar3 * dVar3 * dVar3;
      } while (1e-08 < ABS(param_1 - dVar7));
    }
  }
  auVar1._8_8_ = 0;
  auVar1._0_8_ = dVar3;
  return auVar1;
}

