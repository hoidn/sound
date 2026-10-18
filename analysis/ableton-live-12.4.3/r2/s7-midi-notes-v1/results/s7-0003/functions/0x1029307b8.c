
void FUN_1029307b8(double *param_1,double *param_2,ulong param_3,double *param_4,long param_5)

{
  undefined8 *puVar1;
  long lVar2;
  long lVar3;
  double *pdVar4;
  double dVar5;
  long lVar6;
  double *pdVar7;
  ulong uVar8;
  double *pdVar9;
  double *pdVar10;
  double dVar11;
  double dVar12;
  double dVar13;
  double dVar14;
  double dVar15;
  double dVar16;
  double dVar17;
  double dVar18;
  double dVar19;
  double dVar20;
  
  if (1 < param_3) {
    if (param_3 == 2) {
      pdVar4 = param_2 + -6;
      if (*pdVar4 < *param_1) {
        dVar5 = param_1[1];
        dVar11 = *param_1;
        dVar13 = param_1[3];
        dVar12 = param_1[2];
        dVar15 = param_1[5];
        dVar14 = param_1[4];
        dVar19 = param_2[-3];
        dVar18 = param_2[-4];
        dVar17 = param_2[-1];
        dVar16 = param_2[-2];
        dVar20 = *pdVar4;
        param_1[1] = param_2[-5];
        *param_1 = dVar20;
        param_1[3] = dVar19;
        param_1[2] = dVar18;
        param_1[5] = dVar17;
        param_1[4] = dVar16;
        param_2[-3] = dVar13;
        param_2[-4] = dVar12;
        param_2[-1] = dVar15;
        param_2[-2] = dVar14;
        param_2[-5] = dVar5;
        *pdVar4 = dVar11;
      }
    }
    else if ((long)param_3 < 0x81) {
      if ((param_1 != param_2) && (param_1 + 6 != param_2)) {
        lVar3 = 0;
        pdVar4 = param_1 + 6;
        pdVar7 = param_1;
        do {
          pdVar9 = pdVar4;
          dVar11 = *pdVar9;
          if (dVar11 < *pdVar7) {
            dVar13 = pdVar7[8];
            dVar12 = pdVar7[7];
            dVar15 = pdVar7[10];
            dVar14 = pdVar7[9];
            dVar5 = pdVar7[0xb];
            lVar2 = lVar3;
            do {
              lVar6 = lVar2;
              puVar1 = (undefined8 *)((long)param_1 + lVar6);
              puVar1[7] = puVar1[1];
              puVar1[6] = *puVar1;
              puVar1[9] = puVar1[3];
              puVar1[8] = puVar1[2];
              puVar1[0xb] = puVar1[5];
              puVar1[10] = puVar1[4];
              pdVar4 = param_1;
              if (lVar6 == 0) goto LAB_10293085c;
              lVar2 = lVar6 + -0x30;
            } while (dVar11 < (double)puVar1[-6]);
            pdVar4 = (double *)((long)param_1 + lVar6);
LAB_10293085c:
            *pdVar4 = dVar11;
            pdVar4[2] = dVar13;
            pdVar4[1] = dVar12;
            pdVar4[4] = dVar15;
            pdVar4[3] = dVar14;
            pdVar4[5] = dVar5;
          }
          lVar3 = lVar3 + 0x30;
          pdVar4 = pdVar9 + 6;
          pdVar7 = pdVar9;
        } while (pdVar9 + 6 != param_2);
      }
    }
    else {
      uVar8 = param_3 >> 1;
      pdVar4 = param_1 + uVar8 * 6;
      lVar3 = param_3 - uVar8;
      if (param_5 < (long)param_3) {
        FUN_1029307b8(param_1,pdVar4,uVar8);
        FUN_1029307b8(pdVar4,param_2,lVar3,param_4,param_5);
        FUN_102930c9c(param_1,pdVar4,param_2,uVar8,lVar3,param_4,param_5);
        return;
      }
      FUN_102930a38(param_1,pdVar4,uVar8);
      pdVar9 = param_4 + uVar8 * 6;
      FUN_102930a38(pdVar4,param_2,lVar3,pdVar9);
      pdVar7 = param_4 + param_3 * 6;
      pdVar4 = pdVar9;
      do {
        while( true ) {
          if (pdVar4 == pdVar7) {
            for (; param_4 != pdVar9; param_4 = param_4 + 6) {
              dVar5 = param_4[1];
              dVar11 = *param_4;
              dVar12 = param_4[2];
              dVar14 = param_4[5];
              dVar13 = param_4[4];
              param_1[3] = param_4[3];
              param_1[2] = dVar12;
              param_1[5] = dVar14;
              param_1[4] = dVar13;
              param_1[1] = dVar5;
              *param_1 = dVar11;
              param_1 = param_1 + 6;
            }
            return;
          }
          if (*param_4 <= *pdVar4) break;
          dVar5 = pdVar4[1];
          dVar11 = *pdVar4;
          dVar12 = pdVar4[2];
          dVar14 = pdVar4[5];
          dVar13 = pdVar4[4];
          param_1[3] = pdVar4[3];
          param_1[2] = dVar12;
          param_1[5] = dVar14;
          param_1[4] = dVar13;
          pdVar10 = param_1 + 6;
          param_1[1] = dVar5;
          *param_1 = dVar11;
          pdVar4 = pdVar4 + 6;
          param_1 = pdVar10;
          if (param_4 == pdVar9) goto LAB_102930a2c;
        }
        dVar5 = param_4[1];
        dVar11 = *param_4;
        dVar12 = param_4[2];
        dVar14 = param_4[5];
        dVar13 = param_4[4];
        param_1[3] = param_4[3];
        param_1[2] = dVar12;
        param_1[5] = dVar14;
        param_1[4] = dVar13;
        pdVar10 = param_1 + 6;
        param_1[1] = dVar5;
        *param_1 = dVar11;
        param_4 = param_4 + 6;
        param_1 = pdVar10;
      } while (param_4 != pdVar9);
LAB_102930a2c:
      for (; pdVar4 != pdVar7; pdVar4 = pdVar4 + 6) {
        dVar5 = pdVar4[1];
        dVar11 = *pdVar4;
        dVar12 = pdVar4[2];
        dVar14 = pdVar4[5];
        dVar13 = pdVar4[4];
        pdVar10[3] = pdVar4[3];
        pdVar10[2] = dVar12;
        pdVar10[5] = dVar14;
        pdVar10[4] = dVar13;
        pdVar10[1] = dVar5;
        *pdVar10 = dVar11;
        pdVar10 = pdVar10 + 6;
      }
    }
  }
  return;
}

