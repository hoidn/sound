
void FUN_10292c960(undefined8 param_1,long param_2,ulong param_3)

{
  ulong uVar1;
  long *plVar2;
  long *plVar3;
  code *pcVar4;
  int iVar5;
  long *plVar6;
  ulong uVar7;
  ulong uVar8;
  long *plVar9;
  ulong uVar10;
  size_t sVar11;
  long *plVar12;
  long lVar13;
  undefined2 uVar14;
  undefined8 uVar15;
  long *local_88;
  long *local_80;
  long *local_78;
  
  uVar8 = *(ulong *)(param_2 + 0x48);
  if (uVar8 != 0) {
    uVar15 = CONCAT17(POPCOUNT((char)(uVar8 >> 0x38)),
                      CONCAT16(POPCOUNT((char)(uVar8 >> 0x30)),
                               CONCAT15(POPCOUNT((char)(uVar8 >> 0x28)),
                                        CONCAT14(POPCOUNT((char)(uVar8 >> 0x20)),
                                                 CONCAT13(POPCOUNT((char)(uVar8 >> 0x18)),
                                                          CONCAT12(POPCOUNT((char)(uVar8 >> 0x10)),
                                                                   CONCAT11(POPCOUNT((char)(uVar8 >>
                                                                                           8)),
                                                                            POPCOUNT((char)uVar8))))
                                                ))));
    uVar14 = NEON_uaddlv(uVar15,1);
    uVar10 = CONCAT62((int6)((ulong)uVar15 >> 0x10),uVar14) & 0xffffffff;
    if (uVar10 < 2) {
      uVar7 = uVar8 - 1 & param_3;
    }
    else {
      uVar7 = param_3;
      if (uVar8 <= param_3) {
        uVar7 = 0;
        if (uVar8 != 0) {
          uVar7 = param_3 / uVar8;
        }
        uVar7 = param_3 - uVar7 * uVar8;
      }
    }
    plVar9 = *(long **)(*(long *)(param_2 + 0x40) + uVar7 * 8);
    if ((plVar9 != (long *)0x0) && (plVar9 = (long *)*plVar9, plVar9 != (long *)0x0)) {
      if (uVar10 < 2) {
        do {
          if (plVar9[1] == param_3) {
            if (plVar9[2] == param_3) {
LAB_10292ca5c:
              local_88 = (long *)0x0;
              local_80 = (long *)0x0;
              local_78 = (long *)0x0;
              plVar9 = (long *)plVar9[5];
              if (plVar9 == (long *)0x0) {
                return;
              }
              plVar6 = (long *)0x0;
              do {
                FUN_10292b9ec(param_1,plVar9[3]);
                iVar5 = FUN_10155ede4(*(undefined8 *)(plVar9[3] + 0x30));
                plVar2 = local_88;
                plVar12 = plVar6;
                plVar3 = local_80;
                if (iVar5 == 0) {
                  if (plVar6 < local_78) {
                    plVar12 = plVar6 + 1;
                    *plVar6 = plVar9[3];
                    plVar3 = plVar12;
                  }
                  else {
                    sVar11 = (long)plVar6 - (long)local_88;
                    lVar13 = (long)sVar11 >> 3;
                    uVar8 = lVar13 + 1;
                    if (uVar8 >> 0x3d != 0) {
                      FUN_10292ecfc(&local_88);
                    /* WARNING: Does not return */
                      pcVar4 = (code *)SoftwareBreakpoint(1,0x10292cbac);
                      (*pcVar4)();
                    }
                    uVar10 = (long)local_78 - (long)local_88 >> 2;
                    if (uVar10 <= uVar8) {
                      uVar10 = uVar8;
                    }
                    if (0x7ffffffffffffff7 < (ulong)((long)local_78 - (long)local_88)) {
                      uVar10 = 0x1fffffffffffffff;
                    }
                    if (uVar10 == 0) {
                      plVar6 = (long *)0x0;
                    }
                    else {
                      if (uVar10 >> 0x3d != 0) {
                    /* WARNING: Subroutine does not return */
                        FUN_10024a858();
                      }
                      plVar6 = operator_new(uVar10 << 3);
                    }
                    plVar12 = plVar6 + lVar13 + 1;
                    plVar6[lVar13] = plVar9[3];
                    _memcpy(plVar6,plVar2,sVar11);
                    local_88 = plVar6;
                    plVar3 = plVar12;
                    local_78 = plVar6 + uVar10;
                    if (plVar2 != (long *)0x0) {
                      operator_delete(plVar2);
                    }
                  }
                }
                local_80 = plVar3;
                plVar3 = local_88;
                plVar9 = (long *)*plVar9;
                plVar6 = plVar12;
                plVar2 = local_88;
              } while (plVar9 != (long *)0x0);
              for (; plVar2 != plVar12; plVar2 = plVar2 + 1) {
                FUN_10156d800(*(undefined8 *)(param_2 + 0x30),*plVar2);
              }
              if (plVar3 == (long *)0x0) {
                return;
              }
              operator_delete(plVar3);
              return;
            }
          }
          else if ((plVar9[1] & uVar8 - 1) != uVar7) {
            return;
          }
          plVar9 = (long *)*plVar9;
        } while (plVar9 != (long *)0x0);
      }
      else {
        do {
          uVar10 = plVar9[1];
          if (uVar10 == param_3) {
            if (plVar9[2] == param_3) goto LAB_10292ca5c;
          }
          else {
            if (uVar8 <= uVar10) {
              uVar1 = 0;
              if (uVar8 != 0) {
                uVar1 = uVar10 / uVar8;
              }
              uVar10 = uVar10 - uVar1 * uVar8;
            }
            if (uVar10 != uVar7) {
              return;
            }
          }
          plVar9 = (long *)*plVar9;
        } while (plVar9 != (long *)0x0);
      }
    }
  }
  return;
}

