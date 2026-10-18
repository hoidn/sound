
undefined1  [16] FUN_101b39d8c(double param_1,long *param_2)

{
  ulong uVar1;
  double *pdVar2;
  double *pdVar3;
  double *pdVar4;
  int iVar5;
  long lVar6;
  ulong uVar7;
  ulong uVar8;
  double dVar9;
  undefined1 auVar10 [16];
  double dVar11;
  
  pdVar3 = (double *)*param_2;
  lVar6 = (long)(int)param_2[1] * 8 + -8;
  pdVar4 = pdVar3;
  if (lVar6 != 0) {
    uVar7 = lVar6 >> 3;
    do {
      uVar8 = uVar7 >> 1;
      uVar1 = uVar7 + ~uVar8;
      uVar7 = uVar8;
      if (pdVar4[uVar8] <= param_1) {
        uVar7 = uVar1;
        pdVar4 = pdVar4 + uVar8 + 1;
      }
    } while (uVar7 != 0);
  }
  pdVar2 = pdVar3;
  if (pdVar4 != pdVar3) {
    pdVar2 = pdVar4 + -1;
  }
  iVar5 = (int)((ulong)((long)pdVar2 - (long)pdVar3) >> 3);
  dVar11 = *(double *)(param_2[2] + (long)iVar5 * 8);
  lVar6 = ((long)pdVar2 - (long)pdVar3) * 0x20000000 + 0x100000000 >> 0x20;
  dVar9 = (param_1 - pdVar3[iVar5]) / (pdVar3[lVar6] - pdVar3[iVar5]);
  auVar10._0_8_ = (dVar11 - dVar11 * dVar9) + *(double *)(param_2[2] + lVar6 * 8) * dVar9;
  auVar10._8_8_ = 0;
  return auVar10;
}

