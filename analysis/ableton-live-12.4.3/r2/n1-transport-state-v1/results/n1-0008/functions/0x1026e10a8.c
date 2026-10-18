
undefined8 * FUN_1026e10a8(void)

{
  undefined8 *puVar1;
  int iVar2;
  undefined8 *puVar3;
  code *pcVar4;
  undefined8 *puVar5;
  int *piVar6;
  uint uVar7;
  undefined8 *puVar8;
  undefined8 *puVar9;
  ulong uVar10;
  ulong uVar11;
  ulong uVar12;
  undefined8 *puVar13;
  ulong uVar14;
  int iVar15;
  undefined8 *puVar16;
  long lVar17;
  long lVar18;
  undefined8 uVar19;
  undefined8 uVar20;
  undefined8 uVar21;
  undefined8 uVar22;
  undefined8 uVar23;
  undefined8 uVar24;
  undefined8 uVar25;
  int *local_68;
  
  if ((DAT_10700cb80 & 1) == 0) {
    FUN_105423724();
    if (DAT_10700cca8 != DAT_10700ccb0) goto LAB_1026e10ec;
  }
  else if (DAT_10700cca8 != DAT_10700ccb0) goto LAB_1026e10ec;
  uVar7 = 0;
  do {
    iVar15 = 1;
    do {
      FUN_1026e0c6c(&local_68,iVar15,1 << (ulong)(uVar7 & 0x1f));
      puVar3 = DAT_10700ccb0;
      puVar16 = DAT_10700cca8;
      if (DAT_10700ccb0 < DAT_10700ccb8) {
        *DAT_10700ccb0 = 0;
        *DAT_10700ccb0 = local_68;
        DAT_10700ccb0 = DAT_10700ccb0 + 1;
      }
      else {
        lVar17 = (long)DAT_10700ccb0 - (long)DAT_10700cca8;
        lVar18 = lVar17 >> 3;
        uVar11 = lVar18 + 1;
        if (uVar11 >> 0x3d != 0) {
          FUN_100256758(&DAT_10700cca8);
                    /* WARNING: Does not return */
          pcVar4 = (code *)SoftwareBreakpoint(1,0x1026e1358);
          (*pcVar4)();
        }
        uVar10 = (long)DAT_10700ccb8 - (long)DAT_10700cca8 >> 2;
        if (uVar10 <= uVar11) {
          uVar10 = uVar11;
        }
        if (0x7ffffffffffffff7 < (ulong)((long)DAT_10700ccb8 - (long)DAT_10700cca8)) {
          uVar10 = 0x1fffffffffffffff;
        }
        if (uVar10 == 0) {
          puVar5 = (undefined8 *)0x0;
          puVar1 = (undefined8 *)(lVar18 * 8);
          *puVar1 = local_68;
          puVar13 = DAT_10700cca8;
        }
        else {
          if (uVar10 >> 0x3d != 0) {
                    /* WARNING: Subroutine does not return */
            FUN_10024a858();
          }
          puVar5 = operator_new(uVar10 << 3);
          puVar1 = puVar5 + lVar18;
          *puVar1 = local_68;
          puVar13 = DAT_10700cca8;
        }
        local_68 = (int *)0x0;
        puVar1 = puVar1 + 1;
        DAT_10700cca8 = puVar16;
        if (puVar16 != puVar3) {
          local_68 = (int *)0x0;
          uVar11 = lVar17 - 8;
          puVar8 = puVar5;
          puVar9 = puVar16;
          DAT_10700cca8 = puVar13;
          if ((uVar11 < 0x38) ||
             ((puVar5 < (undefined8 *)((long)puVar16 + (uVar11 & 0xfffffffffffffff8) + 8) &&
              (puVar16 < (undefined8 *)((long)puVar5 + (uVar11 & 0xfffffffffffffff8) + 8))))) {
LAB_1026e12b4:
            do {
              *puVar8 = *puVar9;
              puVar13 = puVar9 + 1;
              *puVar9 = 0;
              puVar8 = puVar8 + 1;
              puVar9 = puVar13;
            } while (puVar13 != puVar3);
          }
          else {
            uVar11 = (uVar11 >> 3) + 1;
            uVar12 = uVar11 & 0x3ffffffffffffff8;
            puVar13 = puVar5 + 4;
            puVar8 = puVar16 + 4;
            uVar14 = uVar12;
            do {
              uVar19 = puVar8[-4];
              uVar21 = puVar8[-1];
              uVar20 = puVar8[-2];
              uVar23 = puVar8[1];
              uVar22 = *puVar8;
              uVar25 = puVar8[3];
              uVar24 = puVar8[2];
              puVar13[-3] = puVar8[-3];
              puVar13[-4] = uVar19;
              puVar13[-1] = uVar21;
              puVar13[-2] = uVar20;
              puVar13[1] = uVar23;
              *puVar13 = uVar22;
              puVar13[3] = uVar25;
              puVar13[2] = uVar24;
              puVar8[-3] = 0;
              puVar8[-4] = 0;
              puVar8[-1] = 0;
              puVar8[-2] = 0;
              puVar8[1] = 0;
              *puVar8 = 0;
              puVar8[3] = 0;
              puVar8[2] = 0;
              uVar14 = uVar14 - 8;
              puVar13 = puVar13 + 8;
              puVar8 = puVar8 + 8;
            } while (uVar14 != 0);
            puVar8 = puVar5 + uVar12;
            puVar9 = puVar16 + uVar12;
            if (uVar11 != uVar12) goto LAB_1026e12b4;
          }
          do {
            piVar6 = (int *)*puVar16;
            if ((piVar6 != (int *)0x0) && (iVar2 = *piVar6, *piVar6 = iVar2 + -1, iVar2 + -1 == 0))
            {
              FUN_101449efc();
            }
            puVar16 = puVar16 + 1;
          } while (puVar16 != puVar3);
        }
        DAT_10700ccb8 = puVar5 + uVar10;
        if (DAT_10700cca8 != (undefined8 *)0x0) {
          puVar16 = DAT_10700cca8;
          DAT_10700cca8 = puVar5;
          DAT_10700ccb0 = puVar1;
          operator_delete(puVar16);
          puVar5 = DAT_10700cca8;
        }
        DAT_10700cca8 = puVar5;
        DAT_10700ccb0 = puVar1;
        if ((local_68 != (int *)0x0) && (iVar2 = *local_68, *local_68 = iVar2 + -1, iVar2 + -1 == 0)
           ) {
          FUN_101449efc();
        }
      }
      iVar15 = iVar15 + 1;
    } while (iVar15 != 100);
    uVar7 = uVar7 + 1;
  } while (uVar7 != 5);
LAB_1026e10ec:
  return &DAT_10700cca8;
}

