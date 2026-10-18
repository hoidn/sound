
bool FUN_1012132d8(double param_1,double param_2,double param_3,double param_4)

{
  bool bVar1;
  bool bVar2;
  double dVar3;
  double dVar4;
  double dVar5;
  
  bVar1 = false;
  if (((((ulong)ABS(param_1) < 0x7ff0000000000000) && ((ulong)ABS(param_2) < 0x7ff0000000000000)) &&
      ((ulong)ABS(param_3) < 0x7ff0000000000000)) && ((ulong)ABS(param_4) < 0x7ff0000000000000)) {
    if ((((param_1 <= param_2) && (param_2 <= param_3)) && (param_3 <= param_4)) ||
       (((param_2 <= param_1 && (param_3 <= param_2)) && (param_4 <= param_3)))) {
      return true;
    }
    bVar1 = false;
    dVar3 = param_2 * param_2;
    if ((dVar3 != INFINITY) && (!NAN(dVar3))) {
      dVar4 = param_3 * param_3;
      if ((dVar4 != INFINITY) &&
         ((((!NAN(dVar4) && ((ulong)ABS(param_1 * param_4) < 0x7ff0000000000000)) &&
           ((ulong)ABS(-(param_1 * param_3)) < 0x7ff0000000000000)) &&
          (((ulong)ABS(-(param_2 * param_3)) < 0x7ff0000000000000 &&
           ((ulong)ABS(-(param_2 * param_4)) < 0x7ff0000000000000)))))) {
        dVar4 = dVar4 + (dVar3 - dVar3);
        dVar5 = dVar3 + dVar4;
        dVar3 = param_1 * param_4 - ((dVar5 - dVar3) - dVar4);
        dVar4 = dVar5 + dVar3;
        dVar3 = -(param_1 * param_3) - ((dVar4 - dVar5) - dVar3);
        dVar5 = dVar4 + dVar3;
        dVar3 = -(param_2 * param_3) - ((dVar5 - dVar4) - dVar3);
        dVar4 = dVar5 + dVar3;
        dVar4 = dVar4 + (-(param_2 * param_4) - ((dVar4 - dVar5) - dVar3));
        if (dVar4 <= 2.220446049250313e-16) {
          return true;
        }
        dVar3 = param_1 + param_2 * -2.0 + param_3;
        dVar4 = SQRT(dVar4);
        param_4 = -param_1 + param_2 * 3.0 + param_3 * -3.0 + param_4;
        param_4 = param_4 + param_4;
        dVar5 = (dVar4 + dVar4 + dVar3 * -2.0) / param_4;
        bVar1 = false;
        bVar2 = false;
        if (0.0 < dVar5) {
          bVar1 = false;
          bVar2 = true;
          if (!NAN(dVar5)) {
            bVar1 = dVar5 < 1.0;
            bVar2 = false;
          }
        }
        if (bVar1 != bVar2) {
          return false;
        }
        param_4 = (dVar4 * -2.0 + dVar3 * -2.0) / param_4;
        bVar1 = param_4 <= 0.0;
        if (1.0 <= param_4) {
          bVar1 = true;
        }
      }
    }
  }
  return bVar1;
}

