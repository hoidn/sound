// 0x1028cf5c0 FUN_1028cf5c0 state=exported-with-warnings body=[['0x1028cf5c0', '0x1028cfc03'], ['0x1028cfc08', '0x1028cfc0b'], ['0x1028cfc10', '0x1028cfc13']]

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1028cf5c0(undefined4 *param_1,undefined4 param_2,long param_3,uint param_4,
                  undefined8 param_5,long param_6)

{
  int *piVar1;
  float fVar2;
  float fVar3;
  double dVar4;
  double dVar5;
  double dVar6;
  double dVar7;
  bool bVar8;
  bool bVar9;
  int iVar10;
  int iVar11;
  uint uVar12;
  undefined4 uVar13;
  undefined8 uVar14;
  undefined4 *puVar15;
  undefined8 uVar16;
  long *plVar17;
  undefined8 *puVar18;
  int *piVar19;
  long lVar20;
  bool bVar21;
  long lVar22;
  undefined8 *puVar23;
  undefined4 *puVar24;
  double *pdVar25;
  ulong uVar26;
  double *pdVar27;
  int iVar28;
  ulong uVar29;
  undefined8 *puVar30;
  float *pfVar31;
  long lVar32;
  double *pdVar33;
  undefined8 *puVar34;
  undefined2 extraout_h0;
  undefined2 extraout_h0_00;
  undefined2 extraout_h0_01;
  undefined2 extraout_h0_02;
  undefined2 extraout_h0_03;
  undefined2 extraout_h0_04;
  undefined2 extraout_h0_05;
  undefined2 extraout_h0_06;
  undefined2 extraout_h0_07;
  undefined2 extraout_h0_08;
  undefined2 extraout_h0_09;
  undefined2 extraout_h0_10;
  undefined2 extraout_h0_11;
  ushort uVar35;
  undefined2 extraout_var;
  undefined2 extraout_var_00;
  undefined2 extraout_var_01;
  undefined2 extraout_var_02;
  undefined2 extraout_var_03;
  undefined2 extraout_var_04;
  undefined2 extraout_var_05;
  undefined2 extraout_var_06;
  undefined2 extraout_var_07;
  undefined2 extraout_var_08;
  undefined2 extraout_var_09;
  undefined2 extraout_var_10;
  undefined2 extraout_var_11;
  undefined2 extraout_var_12;
  undefined2 extraout_var_13;
  undefined2 extraout_var_14;
  undefined2 extraout_var_15;
  undefined2 extraout_var_16;
  undefined2 extraout_var_17;
  undefined2 extraout_var_18;
  undefined2 extraout_var_19;
  undefined2 extraout_var_20;
  undefined2 extraout_var_21;
  undefined2 extraout_var_22;
  undefined2 extraout_var_23;
  undefined2 extraout_var_24;
  undefined2 extraout_var_25;
  undefined2 extraout_var_26;
  undefined2 extraout_var_27;
  undefined2 extraout_var_28;
  undefined2 extraout_var_29;
  undefined2 extraout_var_30;
  undefined2 extraout_var_31;
  undefined2 extraout_var_32;
  undefined2 extraout_var_33;
  undefined2 extraout_var_34;
  undefined2 extraout_var_35;
  undefined2 extraout_var_36;
  undefined2 extraout_var_37;
  undefined1 *puVar36;
  double dVar37;
  undefined1 *local_500;
  double *local_4f0;
  double *local_4e8;
  undefined8 local_4d8;
  int local_4d0 [262];
  long local_b8;
  long local_b0;
  
  local_b0 = *(long *)PTR____stack_chk_guard_1064f8818;
  uVar13 = 1;
  if (param_4 == 0) {
    iVar11 = 1;
  }
  else {
    lVar22 = (long)(int)param_4 * 0x30;
    iVar11 = 1;
    lVar32 = param_3;
    do {
      iVar10 = FUN_1028d8cdc(lVar32);
      iVar28 = iVar11 + 2;
      if (iVar10 == 0) {
        iVar28 = iVar11;
      }
      uVar14 = FUN_1028da61c(lVar32);
      iVar11 = FUN_10292ae68(uVar14,param_5);
      iVar11 = iVar11 + iVar28;
      lVar32 = lVar32 + 0x30;
      lVar22 = lVar22 + -0x30;
    } while (lVar22 != 0);
  }
  uVar14 = FUN_101aa0314(iVar11 << 3);
  *(undefined8 *)(param_1 + 2) = uVar14;
  puVar15 = (undefined4 *)FUN_101aa0314(iVar11 * 0x1c);
  *(undefined4 **)(param_1 + 4) = puVar15;
  puVar23 = *(undefined8 **)(param_1 + 2);
  FUN_101505400();
  iVar11 = FUN_10150a894();
  *puVar23 = DAT_1058464f8;
  *puVar15 = 1;
  puVar15[1] = param_2;
  *(undefined8 *)(puVar15 + 2) = DAT_105868330;
  *(undefined8 *)(puVar15 + 4) = 0x800000003f800000;
  *(undefined2 *)(puVar15 + 6) = 0;
  dVar7 = _UNK_1055d9698;
  dVar6 = _DAT_1055d9690;
  dVar5 = _UNK_1055d9688;
  dVar4 = _DAT_1055d9680;
  uVar14 = DAT_1055d1ad8;
  if (0 < (int)param_4) {
    uVar26 = 0;
    puVar36 = &DAT_7fefffffffffffff;
    local_500 = &DAT_7fefffffffffffff;
    uVar29 = 1;
    do {
      lVar32 = param_3 + uVar26 * 0x30;
      uVar12 = FUN_1028d8cdc(lVar32);
      if ((param_4 - 1 <= uVar26) ||
         (FUN_1028dea48(lVar32),
         NAN((double)CONCAT26(extraout_var_25,
                              CONCAT24(extraout_var_12,CONCAT22(extraout_var,extraout_h0)))) ||
         (double)CONCAT26(extraout_var_25,
                          CONCAT24(extraout_var_12,CONCAT22(extraout_var,extraout_h0))) != 0.0)) {
        bVar8 = false;
        bVar21 = false;
        if ((double)puVar36 != 1.79769313486232e+308) goto LAB_1028cf7e0;
LAB_1028cf7c4:
        bVar9 = false;
        if (!bVar21 && ((uVar12 ^ 0xffffffff) & 1) == 0) {
LAB_1028cf7f8:
          if (!bVar9) {
            uVar16 = FUN_1028da61c(lVar32);
            FUN_10292a4b8(&local_4f0,uVar16,param_5);
            pdVar25 = local_4f0;
            _bzero(local_4d0,0x420);
            pdVar27 = pdVar25;
            pdVar33 = pdVar25;
            if (pdVar25 != local_4e8) {
              lVar22 = 0;
              do {
                while( true ) {
                  if (0.0 < *pdVar33) goto LAB_1028cf8b8;
                  iVar28 = *(int *)((long)pdVar33 + 0xc);
                  piVar19 = local_4d0;
                  piVar1 = piVar19 + lVar22 * 2;
                  if (lVar22 == 0) break;
                  lVar20 = lVar22 << 3;
                  piVar19 = local_4d0;
                  do {
                    if (*piVar19 == *(int *)(pdVar33 + 1)) goto LAB_1028cf838;
                    piVar19 = piVar19 + 2;
                    lVar20 = lVar20 + -8;
                  } while (lVar20 != 0);
LAB_1028cf890:
                  if (lVar22 == 0x83) {
                    /* WARNING: Subroutine does not return */
                    FUN_100d96804();
                  }
                  *piVar1 = *(int *)(pdVar33 + 1);
                  local_4d0[lVar22 * 2 + 1] = 0;
                  lVar20 = lVar22 + 1;
                  local_b8 = lVar20;
                  local_4d0[lVar22 * 2 + 1] = iVar28;
                  pdVar33 = pdVar33 + 2;
                  lVar22 = lVar20;
                  if (pdVar33 == local_4e8) goto LAB_1028cf8b8;
                }
LAB_1028cf838:
                if (piVar19 == piVar1) goto LAB_1028cf890;
                piVar19[1] = iVar28;
                pdVar33 = pdVar33 + 2;
              } while (pdVar33 != local_4e8);
LAB_1028cf8b8:
              pdVar27 = local_4e8;
              if (lVar22 != 0) {
                iVar28 = (int)uVar29;
                uVar29 = (ulong)iVar28;
                lVar22 = lVar22 << 3;
                puVar34 = (undefined8 *)(puVar15 + (long)iVar28 * 7 + -7);
                puVar30 = puVar23 + iVar28;
                pfVar31 = (float *)((ulong)local_4d0 | 4);
                do {
                  FUN_1028d8ce4(lVar32);
                  if ((double)CONCAT26(extraout_var_30,
                                       CONCAT24(extraout_var_17,
                                                CONCAT22(extraout_var_04,extraout_h0_04))) ==
                      (double)local_500) {
                    *puVar30 = puVar30[-1];
                    *(undefined8 *)((long)puVar34 + 0x24) = puVar34[1];
                    *(undefined8 *)((long)puVar34 + 0x1c) = *puVar34;
                    *(undefined8 *)((long)puVar34 + 0x2e) = *(undefined8 *)((long)puVar34 + 0x12);
                    *(undefined8 *)((long)puVar34 + 0x26) = *(undefined8 *)((long)puVar34 + 10);
                    FUN_1028d8ce4(lVar32);
                    puVar30[-1] = CONCAT26(extraout_var_31,
                                           CONCAT24(extraout_var_18,
                                                    CONCAT22(extraout_var_05,extraout_h0_05)));
                    fVar3 = *pfVar31;
                    puVar18 = puVar34;
                  }
                  else {
                    FUN_1028d8ce4(lVar32);
                    *puVar30 = CONCAT26(extraout_var_29,
                                        CONCAT24(extraout_var_16,
                                                 CONCAT22(extraout_var_03,extraout_h0_03)));
                    fVar3 = *pfVar31;
                    puVar18 = (undefined8 *)(puVar15 + uVar29 * 7);
                  }
                  fVar2 = pfVar31[-1];
                  *(undefined4 *)puVar18 = 0;
                  *(float *)((long)puVar18 + 4) = fVar2;
                  *(int *)(puVar18 + 1) = (int)fVar3;
                  *(undefined8 *)((long)puVar18 + 0xc) = uVar14;
                  uVar29 = uVar29 + 1;
                  *(undefined4 *)((long)puVar18 + 0x14) = 0x80000000;
                  *(undefined2 *)(puVar18 + 3) = 1;
                  pfVar31 = pfVar31 + 2;
                  puVar34 = (undefined8 *)((long)puVar34 + 0x1c);
                  puVar30 = puVar30 + 1;
                  lVar22 = lVar22 + -8;
                  pdVar27 = local_4e8;
                  pdVar25 = local_4f0;
                } while (lVar22 != 0);
              }
            }
            FUN_1028d8ce4(lVar32);
            uVar12 = (uint)uVar29;
            puVar23[(int)uVar12] =
                 CONCAT26(extraout_var_32,
                          CONCAT24(extraout_var_19,CONCAT22(extraout_var_06,extraout_h0_06)));
            uVar13 = FUN_1028e22bc(lVar32);
            puVar24 = puVar15 + (long)(int)uVar12 * 7;
            *puVar24 = 2;
            puVar24[1] = param_2;
            puVar24[2] = uVar13;
            *(undefined8 *)(puVar24 + 3) = uVar14;
            puVar24[5] = 0x80000000;
            *(undefined1 *)(puVar24 + 6) = 0;
            *(bool *)((long)puVar24 + 0x19) = pdVar25 != pdVar27;
            if (iVar11 != 0) {
              uVar13 = FUN_1028e22dc(lVar32);
              puVar24[3] = uVar13;
              uVar13 = FUN_1028e22f4(lVar32);
              puVar24[4] = uVar13;
            }
            local_4d8 = FUN_1028da61c(lVar32);
            plVar17 = *(long **)(param_6 + 0x18);
            if (plVar17 == (long *)0x0) {
                    /* WARNING: Subroutine does not return */
              FUN_10025e3f8();
            }
            uVar13 = (**(code **)(*plVar17 + 0x30))(plVar17,&local_4d8);
            puVar24[5] = uVar13;
            FUN_1028d8ce4(lVar32);
            puVar36 = (undefined1 *)
                      CONCAT26(extraout_var_33,
                               CONCAT24(extraout_var_20,CONCAT22(extraout_var_07,extraout_h0_07)));
            iVar28 = uVar12 + 1;
            if (pdVar33 != local_4e8) {
              lVar22 = (long)puVar15 + (long)iVar28 * 0x1c + 0x19;
              pdVar25 = (double *)(puVar23 + iVar28);
              do {
                uVar12 = (uint)uVar29;
                dVar37 = *pdVar33;
                FUN_1028dea48(lVar32);
                if ((double)CONCAT26(extraout_var_34,
                                     CONCAT24(extraout_var_21,
                                              CONCAT22(extraout_var_08,extraout_h0_08))) <= dVar37
                    && dVar37 != (double)CONCAT26(extraout_var_34,
                                                  CONCAT24(extraout_var_21,
                                                           CONCAT22(extraout_var_08,extraout_h0_08))
                                                 )) break;
                *pdVar25 = (double)puVar36 + *pdVar33;
                uVar13 = *(undefined4 *)(pdVar33 + 1);
                fVar3 = *(float *)((long)pdVar33 + 0xc);
                *(undefined4 *)(lVar22 + -0x19) = 0;
                *(undefined4 *)(lVar22 + -0x15) = uVar13;
                *(int *)(lVar22 + -0x11) = (int)fVar3;
                *(undefined8 *)(lVar22 + -0xd) = uVar14;
                *(undefined4 *)(lVar22 + -5) = 0x80000000;
                *(undefined2 *)(lVar22 + -1) = 0;
                pdVar33 = pdVar33 + 2;
                uVar12 = uVar12 + 1;
                uVar29 = (ulong)uVar12;
                lVar22 = lVar22 + 0x1c;
                pdVar25 = pdVar25 + 1;
              } while (pdVar33 != local_4e8);
              iVar28 = uVar12 + 1;
            }
            FUN_1028dea48(lVar32);
            bVar21 = NAN((double)CONCAT26(extraout_var_35,
                                          CONCAT24(extraout_var_22,
                                                   CONCAT22(extraout_var_09,extraout_h0_09))));
            if ((bVar21 ||
                (double)CONCAT26(extraout_var_35,
                                 CONCAT24(extraout_var_22,CONCAT22(extraout_var_09,extraout_h0_09)))
                != 0.0) &&
                (!bVar21 &&
                (double)CONCAT26(extraout_var_35,
                                 CONCAT24(extraout_var_22,CONCAT22(extraout_var_09,extraout_h0_09)))
                < 0.0) == bVar21) {
              FUN_1028d8cec(lVar32);
              local_500 = (undefined1 *)
                          CONCAT26(extraout_var_36,
                                   CONCAT24(extraout_var_23,CONCAT22(extraout_var_10,extraout_h0_10)
                                           ));
            }
            else {
              FUN_1028d8ce4(lVar32);
              local_500 = (undefined1 *)
                          ((double)CONCAT26(extraout_var_37,
                                            CONCAT24(extraout_var_24,
                                                     CONCAT22(extraout_var_11,extraout_h0_11))) +
                          2.6015651015651016e-07);
              uVar35 = NEON_umaxv(CONCAT26(-(ushort)((double)local_500 == dVar7),
                                           CONCAT24(-(ushort)((double)local_500 == dVar6),
                                                    CONCAT22(-(ushort)((double)local_500 == dVar5),
                                                             -(ushort)((double)local_500 == dVar4)))
                                          ),2);
              if ((uVar35 & 1) == 0) {
                uVar35 = 0x3ff0;
                if ((double)local_500 < 0.0) {
                  uVar35 = 0xbff0;
                }
                local_500 = (undefined1 *)
                            ((double)((ulong)uVar35 << 0x30) *
                            ((double)(long)(ABS((double)local_500 +
                                                (double)((ulong)uVar35 << 0x30) *
                                                2.6015651015651016e-07 * 0.5) * 3843840.0) /
                            3843840.0));
              }
            }
            puVar23[iVar28] = local_500;
            uVar13 = FUN_1028e22e4(lVar32);
            puVar24 = puVar15 + (long)iVar28 * 7;
            *puVar24 = 1;
            puVar24[1] = param_2;
            puVar24[2] = uVar13;
            *(undefined8 *)(puVar24 + 3) = uVar14;
            puVar24[5] = 0x80000000;
            *(undefined2 *)(puVar24 + 6) = 0;
            if (local_4f0 != (double *)0x0) {
              local_4e8 = local_4f0;
              operator_delete(local_4f0);
            }
            uVar29 = (ulong)(uVar12 + 2);
          }
        }
      }
      else {
        FUN_1028d8ce4(lVar32 + 0x30);
        FUN_1028d8ce4(lVar32);
        bVar8 = (double)CONCAT26(extraout_var_26,
                                 CONCAT24(extraout_var_13,CONCAT22(extraout_var_00,extraout_h0_00)))
                == (double)CONCAT26(extraout_var_27,
                                    CONCAT24(extraout_var_14,
                                             CONCAT22(extraout_var_01,extraout_h0_01)));
        bVar21 = bVar8;
        if ((double)puVar36 == 1.79769313486232e+308) goto LAB_1028cf7c4;
LAB_1028cf7e0:
        FUN_1028d8ce4(lVar32);
        bVar9 = (double)CONCAT26(extraout_var_28,
                                 CONCAT24(extraout_var_15,CONCAT22(extraout_var_02,extraout_h0_02)))
                == (double)puVar36;
        if (!bVar8 && ((uVar12 ^ 0xffffffff) & 1) == 0) goto LAB_1028cf7f8;
      }
      uVar13 = (undefined4)uVar29;
      uVar26 = uVar26 + 1;
    } while (uVar26 != param_4);
  }
  *param_1 = uVar13;
  if (*(long *)PTR____stack_chk_guard_1064f8818 == local_b0) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


