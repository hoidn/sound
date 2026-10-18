
/* WARNING: Removing unreachable block (ram,0x0001005ea94c) */
/* WARNING: Removing unreachable block (ram,0x0001005ea1ac) */
/* WARNING: Removing unreachable block (ram,0x0001005ea8cc) */
/* WARNING: Removing unreachable block (ram,0x0001005ea1cc) */
/* WARNING: Type propagation algorithm not settling */

uint FUN_1005e9fd8(long *param_1,int param_2,long *param_3,long *param_4,long *param_5)

{
  undefined8 *******pppppppuVar1;
  undefined8 *******pppppppuVar2;
  byte bVar3;
  ulong uVar4;
  undefined4 *puVar5;
  undefined4 *puVar6;
  bool bVar7;
  int iVar8;
  int iVar9;
  undefined8 uVar10;
  undefined8 *puVar11;
  int *piVar12;
  ulong uVar13;
  undefined4 *puVar14;
  undefined8 *puVar15;
  ulong uVar16;
  undefined8 *puVar17;
  undefined8 *puVar18;
  long *plVar19;
  void *pvVar20;
  undefined4 *puVar21;
  undefined1 *puVar22;
  undefined8 *puVar23;
  int iVar24;
  uint uVar25;
  ulong uVar26;
  long lVar27;
  undefined4 *puVar28;
  ulong uVar29;
  size_t sVar30;
  undefined8 *puVar31;
  undefined2 uVar32;
  uint local_144;
  undefined1 auStack_120 [8];
  int local_118 [2];
  undefined8 local_110;
  undefined4 *local_108;
  undefined4 *local_100;
  undefined4 *local_f8;
  undefined8 *local_f0;
  undefined8 *puStack_e8;
  undefined8 local_e0;
  undefined8 uStack_d8;
  undefined4 local_d0;
  undefined8 *local_c0;
  undefined8 local_b8;
  long local_b0;
  undefined8 *******local_a8;
  undefined8 *******local_a0;
  byte local_91;
  undefined4 *local_90;
  undefined4 *puStack_88;
  undefined8 local_80;
  long local_70;
  
  local_70 = *(long *)PTR____stack_chk_guard_100b1c378;
  local_e0 = (undefined8 *)CONCAT17(8,(undefined7)local_e0);
  local_f0 = (undefined8 *)&DAT_6e61637367756c70;
  puStack_e8 = (undefined8 *)((ulong)puStack_e8 & 0xffffffffffffff00);
  uVar10 = std::chrono::system_clock::now();
  FUN_1006a284c(&local_a8,2,&local_f0,uVar10);
  if ((long)local_e0 < 0) {
    operator_delete(local_f0);
  }
  iVar8 = FUN_10069f1d8(&local_a8);
  if (iVar8 != 0) {
    FUN_10069c398(&local_a8,"VST3: start scanning plugins");
  }
  thunk_FUN_10069bf04(&local_a8);
  local_b8 = 0;
  local_b0 = 0;
  puVar18 = (undefined8 *)*param_3;
  puVar31 = (undefined8 *)param_3[1];
  local_c0 = &local_b8;
  if (puVar18 == puVar31) {
    iVar8 = 0;
  }
  else {
    do {
      local_e0 = (undefined8 *)CONCAT17(8,(undefined7)local_e0);
      local_f0 = (undefined8 *)&DAT_6e61637367756c70;
      puStack_e8 = (undefined8 *)((ulong)puStack_e8 & 0xffffffffffffff00);
      uVar10 = std::chrono::system_clock::now();
      FUN_1006a284c(&local_a8,2,&local_f0,uVar10);
      if ((long)local_e0 < 0) {
        operator_delete(local_f0);
      }
      iVar8 = FUN_10069f1d8(&local_a8);
      if (iVar8 != 0) {
        uVar10 = FUN_10069c398(&local_a8,"VST3: scanning plugins in ");
        uVar10 = FUN_10013300c(uVar10,puVar18);
        uVar10 = FUN_10069c398(uVar10," (");
        uVar10 = FUN_10043d2b0(uVar10,puVar18 + 3);
        FUN_10069c398(uVar10,")");
      }
      thunk_FUN_10069bf04(&local_a8);
      if (*(char *)((long)puVar18 + 0x17) < '\0') {
        FUN_100135b64(&local_90,*puVar18,puVar18[1]);
      }
      else {
        puStack_88 = (undefined4 *)puVar18[1];
        local_90 = (undefined4 *)*puVar18;
        local_80 = puVar18[2];
      }
      FUN_1001bafbc(&local_a8,&local_90,1);
      FUN_1005e8cb4(&local_f0);
      if (local_a8 != (undefined8 *******)0x0) {
        for (; local_a0 != local_a8; local_a0 = local_a0 + -3) {
        }
        local_a0 = local_a8;
        operator_delete(local_a8);
      }
      puVar11 = (undefined8 *)FUN_1005ec6ec(&local_c0,&local_a8,puVar18 + 3);
      puVar23 = (undefined8 *)*puVar11;
      puVar15 = local_e0;
      if (puVar23 == (undefined8 *)0x0) {
        puVar23 = operator_new(0x50);
        piVar12 = (int *)puVar18[3];
        puVar23[4] = piVar12;
        if (piVar12 != (int *)0x0) {
          *piVar12 = *piVar12 + 1;
        }
        puVar23[8] = 0;
        puVar23[7] = 0;
        puVar23[6] = 0;
        puVar23[5] = 0;
        *(undefined4 *)(puVar23 + 9) = 0x3f800000;
        *puVar23 = 0;
        puVar23[1] = 0;
        puVar23[2] = local_a8;
        *puVar11 = puVar23;
        puVar15 = puVar23;
        if ((undefined8 *)*local_c0 != (undefined8 *)0x0) {
          puVar15 = (undefined8 *)*puVar11;
          local_c0 = (undefined8 *)*local_c0;
        }
        FUN_100135bf0(local_b8,puVar15);
        local_b0 = local_b0 + 1;
        puVar15 = local_e0;
      }
      for (; puVar15 != (undefined8 *)0x0; puVar15 = (undefined8 *)*puVar15) {
        FUN_1005e64f0(puVar23 + 5,puVar15 + 2,puVar15 + 2);
      }
      if (local_c0 == &local_b8) {
        iVar8 = 0;
      }
      else {
        iVar8 = 0;
        puVar23 = local_c0;
        do {
          puVar15 = (undefined8 *)puVar23[1];
          puVar11 = puVar23;
          if ((undefined8 *)puVar23[1] == (undefined8 *)0x0) {
            do {
              puVar17 = (undefined8 *)puVar11[2];
              bVar7 = (undefined8 *)*puVar17 != puVar11;
              puVar11 = puVar17;
            } while (bVar7);
          }
          else {
            do {
              puVar17 = puVar15;
              puVar15 = (undefined8 *)*puVar17;
            } while ((undefined8 *)*puVar17 != (undefined8 *)0x0);
          }
          iVar8 = iVar8 + *(int *)(puVar23 + 8);
          puVar23 = puVar17;
        } while (puVar17 != &local_b8);
      }
      (**(code **)(*param_5 + 0x28))(param_5,iVar8,0);
      puVar23 = local_f0;
      puVar15 = local_e0;
      while (puVar15 != (void *)0x0) {
        pvVar20 = (void *)*puVar15;
        local_f0 = puVar23;
        if (*(char *)((long)puVar15 + 0x27) < '\0') {
          operator_delete((void *)puVar15[2]);
        }
        operator_delete(puVar15);
        puVar23 = local_f0;
        puVar15 = pvVar20;
      }
      local_f0 = (undefined8 *)0x0;
      if (puVar23 != (undefined8 *)0x0) {
        operator_delete(puVar23);
      }
      puVar18 = puVar18 + 4;
    } while (puVar18 != puVar31);
  }
  uVar10 = FUN_1005aa7cc();
  (**(code **)(*param_1 + 0x48))(param_1,uVar10);
  if (param_2 != 0) {
    uVar10 = FUN_1005aa7cc();
    FUN_1005eac54(&local_f0,&local_c0);
    (**(code **)(*param_1 + 0x50))(param_1,3,uVar10,&local_f0);
    puVar31 = local_f0;
    puVar18 = puStack_e8;
    if (local_f0 != (undefined8 *)0x0) {
      while (puVar18 != puVar31) {
        puVar18 = puVar18 + -1;
        piVar12 = (int *)*puVar18;
        if ((piVar12 != (int *)0x0) && (iVar24 = *piVar12, *piVar12 = iVar24 + -1, iVar24 + -1 == 0)
           ) {
          FUN_100454b40();
        }
      }
      puStack_e8 = puVar31;
      operator_delete(local_f0);
    }
  }
  if (local_c0 == &local_b8) {
LAB_1005eaa1c:
    local_e0 = (undefined8 *)CONCAT17(8,(undefined7)local_e0);
    local_f0 = (undefined8 *)&DAT_6e61637367756c70;
    puStack_e8 = (undefined8 *)((ulong)puStack_e8 & 0xffffffffffffff00);
    uVar10 = std::chrono::system_clock::now();
    FUN_1006a284c(&local_a8,2,&local_f0,uVar10);
    if ((long)local_e0 < 0) {
      operator_delete(local_f0);
    }
    iVar8 = FUN_10069f1d8(&local_a8);
    if (iVar8 != 0) {
      FUN_10069c398(&local_a8,"VST3: finished scanning plugins");
    }
    thunk_FUN_10069bf04(&local_a8);
    local_144 = 1;
LAB_1005eaa84:
    FUN_1005ec61c(&local_c0,local_b8);
    if (*(long *)PTR____stack_chk_guard_100b1c378 == local_70) {
      return local_144 & 1;
    }
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  iVar24 = 0;
  puVar18 = local_c0;
LAB_1005ea41c:
  uVar10 = FUN_1005aa7cc();
  (**(code **)(*param_1 + 0x58))(&local_90,param_1,3,uVar10,puVar18 + 4);
  puVar6 = puStack_88;
  local_108 = (undefined4 *)0x0;
  local_100 = (undefined4 *)0x0;
  local_f8 = (undefined4 *)0x0;
  puStack_e8 = (undefined8 *)0x0;
  local_f0 = (undefined8 *)0x0;
  uStack_d8 = 0;
  local_e0 = (undefined8 *)0x0;
  local_d0 = 0x3f800000;
  puVar21 = local_90;
  if (local_90 != puStack_88) {
LAB_1005ea464:
    do {
      uVar13 = FUN_100678e10(puVar21 + 2);
      uVar29 = puVar18[6];
      if (uVar29 != 0) {
        uVar10 = CONCAT17(POPCOUNT((char)(uVar29 >> 0x38)),
                          CONCAT16(POPCOUNT((char)(uVar29 >> 0x30)),
                                   CONCAT15(POPCOUNT((char)(uVar29 >> 0x28)),
                                            CONCAT14(POPCOUNT((char)(uVar29 >> 0x20)),
                                                     CONCAT13(POPCOUNT((char)(uVar29 >> 0x18)),
                                                              CONCAT12(POPCOUNT((char)(uVar29 >>
                                                                                      0x10)),
                                                                       CONCAT11(POPCOUNT((char)(
                                                  uVar29 >> 8)),POPCOUNT((char)uVar29))))))));
        uVar32 = NEON_uaddlv(uVar10,1);
        uVar16 = CONCAT62((int6)((ulong)uVar10 >> 0x10),uVar32) & 0xffffffff;
        if (uVar16 < 2) {
          uVar26 = uVar29 - 1 & uVar13;
        }
        else {
          uVar26 = uVar13;
          if (uVar29 <= uVar13) {
            uVar26 = 0;
            if (uVar29 != 0) {
              uVar26 = uVar13 / uVar29;
            }
            uVar26 = uVar13 - uVar26 * uVar29;
          }
        }
        plVar19 = *(long **)(puVar18[5] + uVar26 * 8);
        if ((plVar19 != (long *)0x0) && (plVar19 = (long *)*plVar19, plVar19 != (long *)0x0)) {
          if (uVar16 < 2) {
            do {
              if (uVar13 == plVar19[1]) {
                iVar9 = FUN_100679138(plVar19 + 2,puVar21 + 2);
                if (iVar9 == 0) goto LAB_1005ea548;
              }
              else if ((plVar19[1] & uVar29 - 1) != uVar26) break;
              plVar19 = (long *)*plVar19;
            } while (plVar19 != (long *)0x0);
          }
          else {
            do {
              uVar16 = plVar19[1];
              if (uVar13 == uVar16) {
                iVar9 = FUN_100679138(plVar19 + 2,puVar21 + 2);
                if (iVar9 == 0) goto LAB_1005ea548;
              }
              else {
                if (uVar29 <= uVar16) {
                  uVar4 = 0;
                  if (uVar29 != 0) {
                    uVar4 = uVar16 / uVar29;
                  }
                  uVar16 = uVar16 - uVar4 * uVar29;
                }
                if (uVar16 != uVar26) break;
              }
              plVar19 = (long *)*plVar19;
            } while (plVar19 != (long *)0x0);
          }
        }
      }
      puVar5 = local_108;
      if (local_100 < local_f8) {
        puVar28 = local_100 + 1;
        *local_100 = *puVar21;
      }
      else {
        sVar30 = (long)local_100 - (long)local_108;
        lVar27 = (long)sVar30 >> 2;
        uVar13 = lVar27 + 1;
        if (uVar13 >> 0x3e != 0) {
                    /* WARNING: Subroutine does not return */
          FUN_1001839ec(&local_108);
        }
        uVar29 = (long)local_f8 - (long)local_108 >> 1;
        if (uVar29 <= uVar13) {
          uVar29 = uVar13;
        }
        if (0x7ffffffffffffffb < (ulong)((long)local_f8 - (long)local_108)) {
          uVar29 = 0x3fffffffffffffff;
        }
        if (uVar29 == 0) {
          puVar14 = (undefined4 *)0x0;
        }
        else {
          if (uVar29 >> 0x3e != 0) {
                    /* WARNING: Subroutine does not return */
            FUN_100134fb4();
          }
          puVar14 = operator_new(uVar29 << 2);
        }
        puVar28 = puVar14 + lVar27 + 1;
        puVar14[lVar27] = *puVar21;
        _memcpy(puVar14,puVar5,sVar30);
        local_108 = puVar14;
        local_f8 = puVar14 + uVar29;
        if (puVar5 != (undefined4 *)0x0) {
          local_100 = puVar28;
          operator_delete(puVar5);
        }
      }
      puVar21 = puVar21 + 0x1a;
      local_100 = puVar28;
    } while (puVar21 != puVar6);
    goto LAB_1005ea6fc;
  }
  goto LAB_1005ea720;
LAB_1005ea548:
  local_118[0] = 0;
  local_110 = std::system_category();
  (**(code **)(*param_4 + 0x18))(&local_a8,param_4,puVar21 + 2,local_118);
  if (local_118[0] != 0) {
    uVar10 = std::chrono::system_clock::now();
    FUN_1006a290c(auStack_120,3,uVar10);
    iVar9 = FUN_10069f1d8(auStack_120);
    if (iVar9 != 0) {
      uVar10 = FUN_10069c398(auStack_120,
                             "VST3: couldn\'t determine fingerprint for plugin candidate: ");
      FUN_10013300c(uVar10,puVar21 + 2);
    }
    thunk_FUN_10069bf04(auStack_120);
  }
  uVar25 = (uint)(char)local_91;
  pppppppuVar1 = local_a0;
  if (-1 < (int)uVar25) {
    pppppppuVar1 = (undefined8 *******)(ulong)local_91;
  }
  bVar3 = *(byte *)((long)puVar21 + 0x67);
  pppppppuVar2 = *(undefined8 ********)(puVar21 + 0x16);
  if (-1 < (char)bVar3) {
    pppppppuVar2 = (undefined8 *******)(ulong)bVar3;
  }
  if (pppppppuVar1 == pppppppuVar2) {
    pppppppuVar2 = local_a8;
    if (-1 < (int)uVar25) {
      pppppppuVar2 = &local_a8;
    }
    puVar31 = *(void **)(puVar21 + 0x14);
    if (-1 < (char)bVar3) {
      puVar31 = (undefined8 *)(puVar21 + 0x14);
    }
    iVar9 = _memcmp(pppppppuVar2,puVar31,(size_t)pppppppuVar1);
    if ((iVar9 == 0) && (puVar21[0x10] != 0)) {
      FUN_1005e64f0(&local_f0,puVar21 + 2,puVar21 + 2);
      uVar25 = (uint)local_91;
    }
  }
  if ((uVar25 >> 7 & 1) != 0) {
    operator_delete(local_a8);
  }
  puVar21 = puVar21 + 0x1a;
  if (puVar21 == puVar6) goto LAB_1005ea6fc;
  goto LAB_1005ea464;
LAB_1005ea6fc:
  if (local_108 != local_100) {
    (**(code **)(*param_1 + 0x60))(param_1,&local_108,puVar18 + 4);
  }
LAB_1005ea720:
  puVar31 = puVar18 + 7;
  while (puVar31 = (undefined8 *)*puVar31, puVar23 = local_f0, puVar15 = local_e0,
        puVar31 != (undefined8 *)0x0) {
    iVar9 = (**(code **)(*param_5 + 0x10))();
    if (iVar9 == 1) {
      local_91 = 8;
      local_a8 = (undefined8 *******)&DAT_6e61637367756c70;
      local_a0 = (undefined8 *******)((ulong)local_a0._1_7_ << 8);
      uVar10 = std::chrono::system_clock::now();
      FUN_1006a284c(local_118,2,&local_a8,uVar10);
      iVar9 = FUN_10069f1d8(local_118);
      if (iVar9 != 0) {
        FUN_10069c398(local_118,"VST3: stopped scanning plugins");
      }
      thunk_FUN_10069bf04(local_118);
      local_144 = 1;
      puVar23 = local_f0;
      puVar15 = local_e0;
      break;
    }
    if (iVar9 == 2) {
      local_91 = 8;
      local_a8 = (undefined8 *******)&DAT_6e61637367756c70;
      local_a0 = (undefined8 *******)((ulong)local_a0._1_7_ << 8);
      uVar10 = std::chrono::system_clock::now();
      FUN_1006a284c(local_118,2,&local_a8,uVar10);
      iVar9 = FUN_10069f1d8(local_118);
      if (iVar9 != 0) {
        FUN_10069c398(local_118,"VST3: interrupted scanning plugins");
      }
      thunk_FUN_10069bf04(local_118);
      local_144 = 0;
      puVar23 = local_f0;
      puVar15 = local_e0;
      break;
    }
    puVar15 = (undefined8 *)FUN_100678e10(puVar31 + 2);
    puVar23 = puStack_e8;
    if (puStack_e8 != (undefined8 *)0x0) {
      uVar10 = CONCAT17(POPCOUNT((char)((ulong)puStack_e8 >> 0x38)),
                        CONCAT16(POPCOUNT((char)((ulong)puStack_e8 >> 0x30)),
                                 CONCAT15(POPCOUNT((char)((ulong)puStack_e8 >> 0x28)),
                                          CONCAT14(POPCOUNT((char)((ulong)puStack_e8 >> 0x20)),
                                                   CONCAT13(POPCOUNT((char)((ulong)puStack_e8 >>
                                                                           0x18)),
                                                            CONCAT12(POPCOUNT((char)((ulong)
                                                  puStack_e8 >> 0x10)),
                                                  CONCAT11(POPCOUNT((char)((ulong)puStack_e8 >> 8)),
                                                           POPCOUNT((char)puStack_e8))))))));
      uVar32 = NEON_uaddlv(uVar10,1);
      uVar13 = CONCAT62((int6)((ulong)uVar10 >> 0x10),uVar32) & 0xffffffff;
      if (uVar13 < 2) {
        puVar11 = (undefined8 *)((ulong)((long)puStack_e8 + -1) & (ulong)puVar15);
      }
      else {
        puVar11 = puVar15;
        if (puStack_e8 <= puVar15) {
          uVar29 = 0;
          if (puStack_e8 != (undefined8 *)0x0) {
            uVar29 = (ulong)puVar15 / (ulong)puStack_e8;
          }
          puVar11 = (undefined8 *)((long)puVar15 - uVar29 * (long)puStack_e8);
        }
      }
      if (((long *)local_f0[(long)puVar11] != (long *)0x0) &&
         (plVar19 = *(long **)local_f0[(long)puVar11], plVar19 != (long *)0x0)) {
        if (uVar13 < 2) {
          puVar22 = (undefined1 *)((long)puStack_e8 + -1);
          do {
            if (puVar15 == (undefined8 *)plVar19[1]) {
              iVar9 = FUN_100679138(plVar19 + 2,puVar31 + 2);
              if (iVar9 == 0) goto LAB_1005ea848;
            }
            else if ((undefined8 *)((ulong)plVar19[1] & (ulong)puVar22) != puVar11) break;
            plVar19 = (long *)*plVar19;
          } while (plVar19 != (long *)0x0);
        }
        else {
          do {
            puVar17 = (undefined8 *)plVar19[1];
            if (puVar15 == puVar17) {
              iVar9 = FUN_100679138(plVar19 + 2,puVar31 + 2);
              if (iVar9 == 0) goto LAB_1005ea848;
            }
            else {
              if (puVar23 <= puVar17) {
                uVar13 = 0;
                if (puVar23 != (undefined8 *)0x0) {
                  uVar13 = (ulong)puVar17 / (ulong)puVar23;
                }
                puVar17 = (undefined8 *)((long)puVar17 - uVar13 * (long)puVar23);
              }
              if (puVar17 != puVar11) break;
            }
            plVar19 = (long *)*plVar19;
          } while (plVar19 != (long *)0x0);
        }
      }
    }
    FUN_1005e91fc(param_1,puVar18 + 4,puVar31 + 2,param_4,param_5);
LAB_1005ea848:
    iVar24 = iVar24 + 1;
    (**(code **)(*param_5 + 0x28))(param_5,iVar8,iVar24);
  }
  while (puVar15 != (undefined8 *)0x0) {
    puVar11 = (undefined8 *)*puVar15;
    local_f0 = puVar23;
    if (*(char *)((long)puVar15 + 0x27) < '\0') {
      operator_delete(*(void **)((long)puVar15 + 0x10));
    }
    operator_delete(puVar15);
    puVar23 = local_f0;
    puVar15 = puVar11;
  }
  local_f0 = (undefined8 *)0x0;
  if (puVar23 != (undefined8 *)0x0) {
    operator_delete(puVar23);
  }
  if (local_108 != (undefined4 *)0x0) {
    local_100 = local_108;
    operator_delete(local_108);
  }
  if (local_90 != (undefined4 *)0x0) {
    FUN_1005cf354(&local_90);
    operator_delete(local_90);
  }
  if (puVar31 != (undefined8 *)0x0) goto LAB_1005eaa84;
  puVar31 = (undefined8 *)puVar18[1];
  puVar23 = puVar18;
  if ((undefined8 *)puVar18[1] == (undefined8 *)0x0) {
    do {
      puVar18 = (undefined8 *)puVar23[2];
      bVar7 = (undefined8 *)*puVar18 != puVar23;
      puVar23 = puVar18;
    } while (bVar7);
  }
  else {
    do {
      puVar18 = puVar31;
      puVar31 = (undefined8 *)*puVar18;
    } while ((undefined8 *)*puVar18 != (undefined8 *)0x0);
  }
  if (puVar18 == &local_b8) goto LAB_1005eaa1c;
  goto LAB_1005ea41c;
}

