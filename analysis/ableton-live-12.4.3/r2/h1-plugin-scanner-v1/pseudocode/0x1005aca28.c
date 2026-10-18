
/* WARNING: Removing unreachable block (ram,0x0001005ad3d4) */
/* WARNING: Removing unreachable block (ram,0x0001005acc14) */
/* WARNING: Removing unreachable block (ram,0x0001005ad024) */
/* WARNING: Removing unreachable block (ram,0x0001005ad358) */
/* WARNING: Removing unreachable block (ram,0x0001005acc34) */
/* WARNING: Type propagation algorithm not settling */

uint FUN_1005aca28(long *param_1,int param_2,long *param_3,long *param_4,long *param_5)

{
  size_t sVar1;
  undefined8 *******pppppppuVar2;
  byte bVar3;
  char cVar4;
  ulong uVar5;
  undefined4 *puVar6;
  undefined4 *puVar7;
  bool bVar8;
  int iVar9;
  int iVar10;
  undefined8 uVar11;
  undefined8 *puVar12;
  int *piVar13;
  ulong uVar14;
  undefined4 *puVar15;
  undefined8 *puVar16;
  ulong uVar17;
  undefined8 *puVar18;
  undefined8 *puVar19;
  long *plVar20;
  void *pvVar21;
  undefined4 *puVar22;
  undefined8 *puVar23;
  undefined8 *puVar24;
  int iVar25;
  uint uVar26;
  ulong uVar27;
  undefined1 *puVar28;
  long lVar29;
  undefined4 *puVar30;
  ulong uVar31;
  size_t sVar32;
  undefined2 uVar33;
  uint local_15c;
  undefined1 auStack_138 [8];
  undefined8 *******local_130;
  size_t local_128;
  byte local_119;
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
  undefined1 *local_a8;
  undefined1 *local_a0;
  undefined1 local_91;
  undefined4 *local_90;
  undefined4 *puStack_88;
  undefined8 local_80;
  long local_70;
  
  local_70 = *(long *)PTR____stack_chk_guard_100b1c378;
  local_e0 = (undefined8 *)CONCAT17(8,(undefined7)local_e0);
  local_f0 = (undefined8 *)&DAT_6e61637367756c70;
  puStack_e8 = (undefined8 *)((ulong)puStack_e8 & 0xffffffffffffff00);
  uVar11 = std::chrono::system_clock::now();
  FUN_1006a284c(&local_a8,2,&local_f0,uVar11);
  if ((long)local_e0 < 0) {
    operator_delete(local_f0);
  }
  iVar9 = FUN_10069f1d8(&local_a8);
  if (iVar9 != 0) {
    FUN_10069c398(&local_a8,"VST2: start scanning plugins");
  }
  thunk_FUN_10069bf04(&local_a8);
  local_b8 = 0;
  local_b0 = 0;
  puVar19 = (undefined8 *)*param_3;
  puVar23 = (undefined8 *)param_3[1];
  local_c0 = &local_b8;
  if (puVar19 == puVar23) {
    iVar9 = 0;
  }
  else {
    do {
      local_e0 = (undefined8 *)CONCAT17(8,(undefined7)local_e0);
      local_f0 = (undefined8 *)&DAT_6e61637367756c70;
      puStack_e8 = (undefined8 *)((ulong)puStack_e8 & 0xffffffffffffff00);
      uVar11 = std::chrono::system_clock::now();
      FUN_1006a284c(&local_a8,2,&local_f0,uVar11);
      if ((long)local_e0 < 0) {
        operator_delete(local_f0);
      }
      iVar9 = FUN_10069f1d8(&local_a8);
      if (iVar9 != 0) {
        uVar11 = FUN_10069c398(&local_a8,"VST2: scanning plugins in ");
        uVar11 = FUN_10013300c(uVar11,puVar19);
        uVar11 = FUN_10069c398(uVar11," (");
        uVar11 = FUN_10043d2b0(uVar11,puVar19 + 3);
        FUN_10069c398(uVar11,")");
      }
      thunk_FUN_10069bf04(&local_a8);
      if (*(char *)((long)puVar19 + 0x17) < '\0') {
        FUN_100135b64(&local_90,*puVar19,puVar19[1]);
      }
      else {
        puStack_88 = (undefined4 *)puVar19[1];
        local_90 = (undefined4 *)*puVar19;
        local_80 = puVar19[2];
      }
      FUN_1001bafbc(&local_a8,&local_90,1);
      FUN_1005aad10(&local_f0);
      if (local_a8 != (undefined1 *)0x0) {
        for (; local_a0 != local_a8; local_a0 = local_a0 + -0x18) {
        }
        local_a0 = local_a8;
        operator_delete(local_a8);
      }
      puVar12 = (undefined8 *)FUN_1005e7064(&local_c0,&local_a8,puVar19 + 3);
      puVar24 = (undefined8 *)*puVar12;
      puVar16 = local_e0;
      if (puVar24 == (undefined8 *)0x0) {
        puVar24 = operator_new(0x50);
        piVar13 = (int *)puVar19[3];
        puVar24[4] = piVar13;
        if (piVar13 != (int *)0x0) {
          *piVar13 = *piVar13 + 1;
        }
        puVar24[8] = 0;
        puVar24[7] = 0;
        puVar24[6] = 0;
        puVar24[5] = 0;
        *(undefined4 *)(puVar24 + 9) = 0x3f800000;
        *puVar24 = 0;
        puVar24[1] = 0;
        puVar24[2] = local_a8;
        *puVar12 = puVar24;
        puVar16 = puVar24;
        if ((undefined8 *)*local_c0 != (undefined8 *)0x0) {
          puVar16 = (undefined8 *)*puVar12;
          local_c0 = (undefined8 *)*local_c0;
        }
        FUN_100135bf0(local_b8,puVar16);
        local_b0 = local_b0 + 1;
        puVar16 = local_e0;
      }
      for (; puVar16 != (undefined8 *)0x0; puVar16 = (undefined8 *)*puVar16) {
        FUN_1005e71cc(puVar24 + 5,puVar16 + 2,puVar16 + 2);
      }
      iVar9 = 0;
      puVar24 = local_c0;
      while (puVar24 != &local_b8) {
        puVar16 = (undefined8 *)puVar24[1];
        puVar12 = puVar24;
        if ((undefined8 *)puVar24[1] == (undefined8 *)0x0) {
          do {
            puVar18 = (undefined8 *)puVar12[2];
            bVar8 = (undefined8 *)*puVar18 != puVar12;
            puVar12 = puVar18;
          } while (bVar8);
        }
        else {
          do {
            puVar18 = puVar16;
            puVar16 = (undefined8 *)*puVar18;
          } while ((undefined8 *)*puVar18 != (undefined8 *)0x0);
        }
        iVar9 = iVar9 + *(int *)(puVar24 + 8);
        puVar24 = puVar18;
      }
      (**(code **)(*param_5 + 0x28))(param_5,iVar9,0);
      puVar24 = local_f0;
      puVar16 = local_e0;
      while (puVar16 != (void *)0x0) {
        pvVar21 = (void *)*puVar16;
        local_f0 = puVar24;
        if (*(char *)((long)puVar16 + 0x3f) < '\0') {
          operator_delete((void *)puVar16[5]);
          cVar4 = *(char *)((long)puVar16 + 0x27);
        }
        else {
          cVar4 = *(char *)((long)puVar16 + 0x27);
        }
        if (cVar4 < '\0') {
          operator_delete((void *)puVar16[2]);
        }
        operator_delete(puVar16);
        puVar24 = local_f0;
        puVar16 = pvVar21;
      }
      local_f0 = (undefined8 *)0x0;
      if (puVar24 != (undefined8 *)0x0) {
        operator_delete(puVar24);
      }
      puVar19 = puVar19 + 4;
    } while (puVar19 != puVar23);
  }
  (**(code **)(*param_1 + 0x48))(param_1,2);
  if (param_2 != 0) {
    FUN_1005ad724(&local_f0,&local_c0);
    (**(code **)(*param_1 + 0x50))(param_1,2,2,&local_f0);
    puVar23 = local_f0;
    puVar19 = puStack_e8;
    if (local_f0 != (undefined8 *)0x0) {
      while (puVar19 != puVar23) {
        puVar19 = puVar19 + -1;
        piVar13 = (int *)*puVar19;
        if ((piVar13 != (int *)0x0) && (iVar25 = *piVar13, *piVar13 = iVar25 + -1, iVar25 + -1 == 0)
           ) {
          FUN_100454b40();
        }
      }
      puStack_e8 = puVar23;
      operator_delete(local_f0);
    }
  }
  if (local_c0 == &local_b8) {
LAB_1005ad4b0:
    local_e0 = (undefined8 *)CONCAT17(8,(undefined7)local_e0);
    local_f0 = (undefined8 *)&DAT_6e61637367756c70;
    puStack_e8 = (undefined8 *)((ulong)puStack_e8 & 0xffffffffffffff00);
    uVar11 = std::chrono::system_clock::now();
    FUN_1006a284c(&local_a8,2,&local_f0,uVar11);
    if ((long)local_e0 < 0) {
      operator_delete(local_f0);
    }
    iVar9 = FUN_10069f1d8(&local_a8);
    if (iVar9 != 0) {
      FUN_10069c398(&local_a8,"VST2: finished scanning plugins");
    }
    thunk_FUN_10069bf04(&local_a8);
    local_15c = 1;
LAB_1005ad528:
    FUN_1005e6f78(&local_c0,local_b8);
    if (*(long *)PTR____stack_chk_guard_100b1c378 == local_70) {
      return local_15c & 1;
    }
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  iVar25 = 0;
  puVar19 = local_c0;
LAB_1005ace8c:
  (**(code **)(*param_1 + 0x58))(&local_90,param_1,2,2,puVar19 + 4);
  puVar7 = puStack_88;
  local_108 = (undefined4 *)0x0;
  local_100 = (undefined4 *)0x0;
  local_f8 = (undefined4 *)0x0;
  puStack_e8 = (undefined8 *)0x0;
  local_f0 = (undefined8 *)0x0;
  uStack_d8 = 0;
  local_e0 = (undefined8 *)0x0;
  local_d0 = 0x3f800000;
  puVar22 = local_90;
  if (local_90 != puStack_88) {
LAB_1005aced0:
    uVar14 = FUN_100678e10(puVar22 + 2);
    uVar31 = puVar19[6];
    if (uVar31 != 0) {
      uVar11 = CONCAT17(POPCOUNT((char)(uVar31 >> 0x38)),
                        CONCAT16(POPCOUNT((char)(uVar31 >> 0x30)),
                                 CONCAT15(POPCOUNT((char)(uVar31 >> 0x28)),
                                          CONCAT14(POPCOUNT((char)(uVar31 >> 0x20)),
                                                   CONCAT13(POPCOUNT((char)(uVar31 >> 0x18)),
                                                            CONCAT12(POPCOUNT((char)(uVar31 >> 0x10)
                                                                             ),
                                                                     CONCAT11(POPCOUNT((char)(uVar31
                                                                                             >> 8)),
                                                                              POPCOUNT((char)uVar31)
                                                                             )))))));
      uVar33 = NEON_uaddlv(uVar11,1);
      uVar17 = CONCAT62((int6)((ulong)uVar11 >> 0x10),uVar33) & 0xffffffff;
      if (uVar17 < 2) {
        uVar27 = uVar31 - 1 & uVar14;
      }
      else {
        uVar27 = uVar14;
        if (uVar31 <= uVar14) {
          uVar27 = 0;
          if (uVar31 != 0) {
            uVar27 = uVar14 / uVar31;
          }
          uVar27 = uVar14 - uVar27 * uVar31;
        }
      }
      plVar20 = *(long **)(puVar19[5] + uVar27 * 8);
      if ((plVar20 != (long *)0x0) && (plVar20 = (long *)*plVar20, plVar20 != (long *)0x0)) {
        if (uVar17 < 2) {
          do {
            if (uVar14 == plVar20[1]) {
              iVar10 = FUN_100679138(plVar20 + 2,puVar22 + 2);
              if (iVar10 == 0) goto LAB_1005acfb4;
            }
            else if ((plVar20[1] & uVar31 - 1) != uVar27) break;
            plVar20 = (long *)*plVar20;
          } while (plVar20 != (long *)0x0);
        }
        else {
          do {
            uVar17 = plVar20[1];
            if (uVar14 == uVar17) {
              iVar10 = FUN_100679138(plVar20 + 2,puVar22 + 2);
              if (iVar10 == 0) goto LAB_1005acfb4;
            }
            else {
              if (uVar31 <= uVar17) {
                uVar5 = 0;
                if (uVar31 != 0) {
                  uVar5 = uVar17 / uVar31;
                }
                uVar17 = uVar17 - uVar5 * uVar31;
              }
              if (uVar17 != uVar27) break;
            }
            plVar20 = (long *)*plVar20;
          } while (plVar20 != (long *)0x0);
        }
      }
    }
    puVar6 = local_108;
    if (local_100 < local_f8) {
      *local_100 = *puVar22;
      local_100 = local_100 + 1;
    }
    else {
      sVar32 = (long)local_100 - (long)local_108;
      lVar29 = (long)sVar32 >> 2;
      uVar14 = lVar29 + 1;
      if (uVar14 >> 0x3e != 0) {
                    /* WARNING: Subroutine does not return */
        FUN_1001839ec(&local_108);
      }
      uVar31 = (long)local_f8 - (long)local_108 >> 1;
      if (uVar31 <= uVar14) {
        uVar31 = uVar14;
      }
      if (0x7ffffffffffffffb < (ulong)((long)local_f8 - (long)local_108)) {
        uVar31 = 0x3fffffffffffffff;
      }
      if (uVar31 == 0) {
        puVar15 = (undefined4 *)0x0;
      }
      else {
        if (uVar31 >> 0x3e != 0) {
                    /* WARNING: Subroutine does not return */
          FUN_100134fb4();
        }
        puVar15 = operator_new(uVar31 << 2);
      }
      puVar30 = puVar15 + lVar29 + 1;
      puVar15[lVar29] = *puVar22;
      _memcpy(puVar15,puVar6,sVar32);
      local_108 = puVar15;
      local_100 = puVar30;
      local_f8 = puVar15 + uVar31;
      if (puVar6 != (undefined4 *)0x0) {
        operator_delete(puVar6);
        local_100 = puVar30;
      }
    }
    goto LAB_1005ad18c;
  }
  goto LAB_1005ad1cc;
LAB_1005acfb4:
  local_118[0] = 0;
  local_110 = std::system_category();
  (**(code **)(*param_4 + 0x18))(&local_130,param_4,puVar22 + 2,local_118);
  if (local_118[0] != 0) {
    local_91 = 8;
    local_a8 = &DAT_6e61637367756c70;
    local_a0 = (undefined1 *)((ulong)local_a0 & 0xffffffffffffff00);
    uVar11 = std::chrono::system_clock::now();
    FUN_1006a284c(auStack_138,3,&local_a8,uVar11);
    iVar10 = FUN_10069f1d8(auStack_138);
    if (iVar10 != 0) {
      uVar11 = FUN_10069c398(auStack_138,
                             "VST2: couldn\'t determine fingerprint for plugin candidate: ");
      FUN_10013300c(uVar11,puVar22 + 2);
    }
    thunk_FUN_10069bf04(auStack_138);
  }
  uVar26 = (uint)(char)local_119;
  sVar32 = local_128;
  if (-1 < (int)uVar26) {
    sVar32 = (ulong)local_119;
  }
  bVar3 = *(byte *)((long)puVar22 + 0x67);
  sVar1 = *(size_t *)(puVar22 + 0x16);
  if (-1 < (char)bVar3) {
    sVar1 = (ulong)bVar3;
  }
  if (sVar32 == sVar1) {
    pppppppuVar2 = local_130;
    if (-1 < (int)uVar26) {
      pppppppuVar2 = &local_130;
    }
    puVar23 = *(void **)(puVar22 + 0x14);
    if (-1 < (char)bVar3) {
      puVar23 = (undefined8 *)(puVar22 + 0x14);
    }
    iVar10 = _memcmp(pppppppuVar2,puVar23,sVar32);
    if ((iVar10 == 0) && (puVar22[0x10] != 0)) {
      FUN_1005e64f0(&local_f0,puVar22 + 2,puVar22 + 2);
      uVar26 = (uint)local_119;
    }
  }
  if ((uVar26 >> 7 & 1) != 0) {
    operator_delete(local_130);
  }
LAB_1005ad18c:
  puVar22 = puVar22 + 0x1a;
  if (puVar22 == puVar7) goto LAB_1005ad1a8;
  goto LAB_1005aced0;
LAB_1005ad1a8:
  if (local_108 != local_100) {
    (**(code **)(*param_1 + 0x60))(param_1,&local_108,puVar19 + 4);
  }
LAB_1005ad1cc:
  puVar23 = puVar19 + 7;
  while (puVar23 = (undefined8 *)*puVar23, puVar24 = local_f0, puVar16 = local_e0,
        puVar23 != (undefined8 *)0x0) {
    iVar10 = (**(code **)(*param_5 + 0x10))(param_5);
    if (iVar10 == 1) {
      local_91 = 8;
      local_a8 = &DAT_6e61637367756c70;
      local_a0 = (undefined1 *)((ulong)local_a0._1_7_ << 8);
      uVar11 = std::chrono::system_clock::now();
      FUN_1006a284c(&local_130,2,&local_a8,uVar11);
      iVar10 = FUN_10069f1d8(&local_130);
      if (iVar10 != 0) {
        FUN_10069c398(&local_130,"VST2: stopped scanning plugins");
      }
      thunk_FUN_10069bf04(&local_130);
      local_15c = 1;
      puVar24 = local_f0;
      puVar16 = local_e0;
      break;
    }
    if (iVar10 == 2) {
      local_91 = 8;
      local_a8 = &DAT_6e61637367756c70;
      local_a0 = (undefined1 *)((ulong)local_a0._1_7_ << 8);
      uVar11 = std::chrono::system_clock::now();
      FUN_1006a284c(&local_130,2,&local_a8,uVar11);
      iVar10 = FUN_10069f1d8(&local_130);
      if (iVar10 != 0) {
        FUN_10069c398(&local_130,"VST2: interrupted scanning plugins");
      }
      thunk_FUN_10069bf04(&local_130);
      local_15c = 0;
      puVar24 = local_f0;
      puVar16 = local_e0;
      break;
    }
    puVar16 = (undefined8 *)FUN_100678e10(puVar23 + 2);
    puVar24 = puStack_e8;
    if (puStack_e8 != (undefined8 *)0x0) {
      uVar11 = CONCAT17(POPCOUNT((char)((ulong)puStack_e8 >> 0x38)),
                        CONCAT16(POPCOUNT((char)((ulong)puStack_e8 >> 0x30)),
                                 CONCAT15(POPCOUNT((char)((ulong)puStack_e8 >> 0x28)),
                                          CONCAT14(POPCOUNT((char)((ulong)puStack_e8 >> 0x20)),
                                                   CONCAT13(POPCOUNT((char)((ulong)puStack_e8 >>
                                                                           0x18)),
                                                            CONCAT12(POPCOUNT((char)((ulong)
                                                  puStack_e8 >> 0x10)),
                                                  CONCAT11(POPCOUNT((char)((ulong)puStack_e8 >> 8)),
                                                           POPCOUNT((char)puStack_e8))))))));
      uVar33 = NEON_uaddlv(uVar11,1);
      uVar14 = CONCAT62((int6)((ulong)uVar11 >> 0x10),uVar33) & 0xffffffff;
      if (uVar14 < 2) {
        puVar12 = (undefined8 *)((ulong)((long)puStack_e8 + -1) & (ulong)puVar16);
      }
      else {
        puVar12 = puVar16;
        if (puStack_e8 <= puVar16) {
          uVar31 = 0;
          if (puStack_e8 != (undefined8 *)0x0) {
            uVar31 = (ulong)puVar16 / (ulong)puStack_e8;
          }
          puVar12 = (undefined8 *)((long)puVar16 - uVar31 * (long)puStack_e8);
        }
      }
      if (((long *)local_f0[(long)puVar12] != (long *)0x0) &&
         (plVar20 = *(long **)local_f0[(long)puVar12], plVar20 != (long *)0x0)) {
        if (uVar14 < 2) {
          puVar28 = (undefined1 *)((long)puStack_e8 + -1);
          do {
            if (puVar16 == (undefined8 *)plVar20[1]) {
              iVar10 = FUN_100679138(plVar20 + 2,puVar23 + 2);
              if (iVar10 == 0) goto LAB_1005ad2f8;
            }
            else if ((undefined8 *)((ulong)plVar20[1] & (ulong)puVar28) != puVar12) break;
            plVar20 = (long *)*plVar20;
          } while (plVar20 != (long *)0x0);
        }
        else {
          do {
            puVar18 = (undefined8 *)plVar20[1];
            if (puVar16 == puVar18) {
              iVar10 = FUN_100679138(plVar20 + 2,puVar23 + 2);
              if (iVar10 == 0) goto LAB_1005ad2f8;
            }
            else {
              if (puVar24 <= puVar18) {
                uVar14 = 0;
                if (puVar24 != (undefined8 *)0x0) {
                  uVar14 = (ulong)puVar18 / (ulong)puVar24;
                }
                puVar18 = (undefined8 *)((long)puVar18 - uVar14 * (long)puVar24);
              }
              if (puVar18 != puVar12) break;
            }
            plVar20 = (long *)*plVar20;
          } while (plVar20 != (long *)0x0);
        }
      }
    }
    FUN_1005aba10(param_1,puVar19 + 4,puVar23 + 2,puVar23 + 5,param_4,param_5);
LAB_1005ad2f8:
    iVar25 = iVar25 + 1;
    (**(code **)(*param_5 + 0x28))(param_5,iVar9,iVar25);
  }
  while (puVar16 != (undefined8 *)0x0) {
    puVar12 = (undefined8 *)*puVar16;
    local_f0 = puVar24;
    if (*(char *)((long)puVar16 + 0x27) < '\0') {
      operator_delete((void *)puVar16[2]);
    }
    operator_delete(puVar16);
    puVar24 = local_f0;
    puVar16 = puVar12;
  }
  local_f0 = (undefined8 *)0x0;
  if (puVar24 != (undefined8 *)0x0) {
    operator_delete(puVar24);
  }
  if (local_108 != (undefined4 *)0x0) {
    local_100 = local_108;
    operator_delete(local_108);
  }
  if (local_90 != (undefined4 *)0x0) {
    FUN_1005cf354(&local_90);
    operator_delete(local_90);
  }
  if (puVar23 != (undefined8 *)0x0) goto LAB_1005ad528;
  puVar23 = (undefined8 *)puVar19[1];
  puVar24 = puVar19;
  if ((undefined8 *)puVar19[1] == (undefined8 *)0x0) {
    do {
      puVar19 = (undefined8 *)puVar24[2];
      bVar8 = (undefined8 *)*puVar19 != puVar24;
      puVar24 = puVar19;
    } while (bVar8);
  }
  else {
    do {
      puVar19 = puVar23;
      puVar23 = (undefined8 *)*puVar19;
    } while ((undefined8 *)*puVar19 != (undefined8 *)0x0);
  }
  if (puVar19 == &local_b8) goto LAB_1005ad4b0;
  goto LAB_1005ace8c;
}

