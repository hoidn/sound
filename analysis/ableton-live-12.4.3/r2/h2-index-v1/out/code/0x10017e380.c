// 0x10017e380 FUN_10017e380 state=exported-with-warnings body_bytes=2120 warnings=2 chunk=chunk-00064.jsonl

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_10017e380(long *param_1,char *param_2)

{
  int *piVar1;
  int iVar2;
  int *piVar3;
  undefined8 uVar4;
  undefined8 uVar5;
  undefined8 uVar6;
  long *plVar7;
  undefined8 *puVar8;
  void *pvVar9;
  undefined8 *puVar10;
  char *pcVar11;
  char *pcVar12;
  long lVar13;
  long *extraout_x8;
  long lVar14;
  ulong uVar15;
  long lVar16;
  long extraout_x9;
  ushort *puVar17;
  int extraout_w10;
  int iVar18;
  long *extraout_x11;
  long *plVar19;
  long *plVar20;
  long local_140;
  long *local_138;
  long lStack_130;
  long local_128;
  char *local_118;
  undefined1 auStack_110 [3];
  undefined1 auStack_10d [5];
  undefined1 *local_108;
  undefined8 uStack_100;
  undefined1 *local_f8;
  undefined1 *puStack_f0;
  long local_e8;
  undefined8 uStack_e0;
  undefined1 local_d8;
  char *local_d0;
  void *pvStack_c8;
  void *local_c0;
  ulong local_b0;
  long *plStack_a8;
  undefined8 local_a0;
  undefined8 *puStack_98;
  undefined8 *puStack_90;
  undefined8 uStack_88;
  undefined8 local_80;
  undefined8 uStack_78;
  undefined8 uStack_70;
  undefined8 uStack_68;
  undefined8 local_60;
  uint local_58;
  void *local_50;
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_100d60390;
  local_108 = auStack_110;
  local_e8 = 4;
  uStack_e0 = 0;
  local_d8 = 0;
  local_f8 = auStack_10d;
  uStack_100 = 4;
  local_118 = param_2;
  puStack_f0 = local_108;
  plVar7 = (long *)std::istream::read(param_2,(long)local_108);
  if ((*(byte *)((long)plVar7 + *(long *)(*plVar7 + -0x18) + 0x20) & 5) != 0) {
    lVar13 = *(long *)(local_118 + 8);
    local_108[lVar13] = 0;
    local_d8 = 1;
    local_f8 = local_108 + lVar13;
    local_e8 = lVar13;
  }
  uStack_78 = 0;
  local_80 = 0;
  uStack_68 = 0;
  uStack_70 = 0;
  puStack_98 = (undefined8 *)0x0;
  local_a0 = 0;
  uStack_88 = 0;
  puStack_90 = (undefined8 *)0x0;
  plStack_a8 = (long *)0x0;
  local_b0 = 0;
  local_60 = 0x400;
  local_58 = 0;
  local_50 = (void *)0x0;
  puVar8 = operator_new(0x18);
  *puVar8 = 0x10000;
  pvVar9 = operator_new(1);
  puVar10 = _malloc(0x38);
  puVar8[1] = pvVar9;
  puVar8[2] = puVar10;
  puVar10[4] = 0;
  *puVar10 = puVar10 + 4;
  puVar10[1] = pvVar9;
  puVar10[5] = 0;
  puVar10[6] = 0;
  *(undefined1 *)(puVar10 + 3) = 1;
  puVar10[2] = 1;
  puStack_98 = puVar8;
  puStack_90 = puVar8;
  FUN_100183a7c(&local_b0,&local_118);
  if (local_58 == 0) {
    uVar15 = local_b0 & 0xffffffff;
    plVar7 = plStack_a8;
    if ((int)local_b0 == 0) {
LAB_10017e568:
      if (plVar7 == plStack_a8 + uVar15 * 6) goto LAB_10017e570;
LAB_10017e624:
      if ((int)local_b0 != 0) {
        iVar18 = 0x656c6946;
        lVar16 = uVar15 * 0x30;
        pcVar12 = "Files";
        lVar13 = lVar16;
        plVar7 = plStack_a8;
        do {
          iVar2 = (int)*plVar7;
          if ((*(ushort *)((long)plVar7 + 0x16) & 0x1000) != 0) {
            iVar2 = 0x15 - *(char *)((long)plVar7 + 0x15);
          }
          if (iVar2 == 5) {
            plVar19 = (long *)plVar7[1];
            if ((*(ushort *)((long)plVar7 + 0x16) & 0x1000) != 0) {
              plVar19 = plVar7;
            }
            if ((plVar19 == (long *)"Files") ||
               ((int)*plVar19 == 0x656c6946 && *(char *)((long)plVar19 + 4) == 's')) {
              if (lVar13 != 0) {
                lVar13 = 0;
                goto LAB_10017e6c4;
              }
              break;
            }
          }
          plVar7 = plVar7 + 6;
          lVar13 = lVar13 + -0x30;
        } while (lVar13 != 0);
      }
      goto LAB_10017e89c;
    }
    lVar13 = uVar15 * 0x30;
    do {
      iVar18 = (int)*plVar7;
      if ((*(ushort *)((long)plVar7 + 0x16) & 0x1000) != 0) {
        iVar18 = 0x15 - *(char *)((long)plVar7 + 0x15);
      }
      if (iVar18 == 0x14) {
        plVar19 = (long *)plVar7[1];
        if ((*(ushort *)((long)plVar7 + 0x16) & 0x1000) != 0) {
          plVar19 = plVar7;
        }
        if ((plVar19 == (long *)"SoundAnalyzerVersion") ||
           ((*plVar19 == 0x616e41646e756f53 && plVar19[1] == 0x72655672657a796c) &&
            (int)plVar19[2] == 0x6e6f6973)) goto LAB_10017e568;
      }
      plVar7 = plVar7 + 6;
      lVar13 = lVar13 + -0x30;
    } while (lVar13 != 0);
LAB_10017e570:
    plVar7 = plStack_a8;
    if ((int)local_b0 == 0) {
LAB_10017e610:
      if (plVar7 == plStack_a8 + uVar15 * 6) goto LAB_10017e768;
      if ((*(ushort *)((long)plVar7 + 0x2e) >> 5 & 1) != 0) goto LAB_10017e624;
    }
    else {
      lVar13 = uVar15 * 0x30;
      do {
        iVar18 = (int)*plVar7;
        if ((*(ushort *)((long)plVar7 + 0x16) & 0x1000) != 0) {
          iVar18 = 0x15 - *(char *)((long)plVar7 + 0x15);
        }
        if (iVar18 == 0x14) {
          plVar19 = (long *)plVar7[1];
          if ((*(ushort *)((long)plVar7 + 0x16) & 0x1000) != 0) {
            plVar19 = plVar7;
          }
          if ((plVar19 == (long *)"SoundAnalyzerVersion") ||
             ((*plVar19 == 0x616e41646e756f53 && plVar19[1] == 0x72655672657a796c) &&
              (int)plVar19[2] == 0x6e6f6973)) goto LAB_10017e610;
        }
        plVar7 = plVar7 + 6;
        lVar13 = lVar13 + -0x30;
      } while (lVar13 != 0);
LAB_10017e768:
      puVar8 = (undefined8 *)(**(code **)PTR_buffer_100d617b8)();
      *puVar8 = 0;
      puVar8[1] = 0;
      puVar8[2] = 0;
    }
    pcVar12 = operator_new(0x38);
    uVar6 = s_Sound_similarity_feature_file_do_100c1e4ed._24_8_;
    uVar5 = s_Sound_similarity_feature_file_do_100c1e4ed._16_8_;
    uVar4 = s_Sound_similarity_feature_file_do_100c1e4ed._0_8_;
    *(undefined8 *)(pcVar12 + 8) = s_Sound_similarity_feature_file_do_100c1e4ed._8_8_;
    *(undefined8 *)pcVar12 = uVar4;
    *(undefined8 *)(pcVar12 + 0x18) = uVar6;
    *(undefined8 *)(pcVar12 + 0x10) = uVar5;
    uVar4 = s_Sound_similarity_feature_file_do_100c1e4ed._32_8_;
    *(ulong *)(pcVar12 + 0x28) =
         CONCAT17(s_Sound_similarity_feature_file_do_100c1e4ed[0x2f],
                  s_Sound_similarity_feature_file_do_100c1e4ed._40_7_);
    *(undefined8 *)(pcVar12 + 0x20) = uVar4;
    *(ulong *)(pcVar12 + 0x2f) =
         CONCAT71(s_Sound_similarity_feature_file_do_100c1e4ed._48_7_,
                  s_Sound_similarity_feature_file_do_100c1e4ed[0x2f]);
    pcVar12[0x37] = '\0';
    *param_1 = (long)pcVar12;
    lVar13 = _DAT_100ba1750;
    lVar16 = _UNK_100ba1758;
    goto LAB_10017e8d4;
  }
  if (local_58 < 0x12) {
    local_d0 = (&PTR_typeinfo_100d8a9b8)[(int)local_58];
  }
  else {
    local_d0 = "Unknown error.";
  }
  local_c0 = local_50;
  FUN_100762008(&local_138,"Json Parsing Error: {} at: {}",0x1d,0x4c,&local_d0);
  param_1[1] = lStack_130;
  *param_1 = (long)local_138;
  param_1[2] = local_128;
  goto LAB_10017e8d8;
LAB_10017e928:
  do {
    iVar2 = (int)*plVar20;
    if ((*(ushort *)((long)plVar20 + 0x16) & 0x1000) != 0) {
      iVar2 = 0x15 - *(char *)((long)plVar20 + 0x15);
    }
    if (iVar2 == 0x14) {
      plVar19 = (long *)plVar20[1];
      if ((*(ushort *)((long)plVar20 + 0x16) & 0x1000) != 0) {
        plVar19 = plVar20;
      }
      if ((plVar19 == (long *)"SoundAnalyzerVersion") ||
         ((*plVar19 == 0x616e41646e756f53 && plVar19[1] == 0x72655672657a796c) &&
          (int)plVar19[2] == 0x6e6f6973)) {
        if (lVar13 != 0) {
          if ((int)plVar20[3] != 0x12) goto LAB_10017eb08;
          lStack_130 = 0;
          local_128 = 0;
          goto LAB_10017ea04;
        }
        break;
      }
    }
    lVar13 = lVar13 + -0x30;
    plVar20 = plVar20 + 6;
  } while (lVar13 != 0);
  puVar8 = (undefined8 *)(**(code **)PTR_buffer_100d617b8)();
  *puVar8 = 0;
  puVar8[1] = 0;
  puVar8[2] = 0;
LAB_10017eb08:
  pcVar12 = operator_new(0x30);
  uVar6 = s_Sound_similarity_feature_file_is_100c1e585._16_8_;
  uVar5 = s_Sound_similarity_feature_file_is_100c1e585._0_8_;
  uVar4 = CONCAT71(s_Sound_similarity_feature_file_is_100c1e585._25_7_,
                   s_Sound_similarity_feature_file_is_100c1e585[0x18]);
  *(undefined8 *)(pcVar12 + 8) = s_Sound_similarity_feature_file_is_100c1e585._8_8_;
  *(undefined8 *)pcVar12 = uVar5;
  *(undefined8 *)(pcVar12 + 0x18) = uVar4;
  *(undefined8 *)(pcVar12 + 0x10) = uVar6;
  uVar4 = CONCAT17(s_Sound_similarity_feature_file_is_100c1e585[0x20],
                   s_Sound_similarity_feature_file_is_100c1e585._25_7_);
  *(undefined8 *)(pcVar12 + 0x21) = s_Sound_similarity_feature_file_is_100c1e585._33_8_;
  *(undefined8 *)(pcVar12 + 0x19) = uVar4;
  pcVar12[0x29] = '\0';
  *param_1 = (long)pcVar12;
  lVar13 = _DAT_100ba1720;
  lVar16 = _UNK_100ba1728;
LAB_10017e9e8:
  param_1[2] = lVar16;
  param_1[1] = lVar13;
  *(undefined1 *)(param_1 + 3) = 0;
  goto LAB_10017e8e0;
LAB_10017ea04:
  iVar2 = (int)*plVar7;
  if ((*(ushort *)((long)plVar7 + 0x16) & 0x1000) != 0) {
    iVar2 = 0x15 - *(char *)((long)plVar7 + 0x15);
  }
  local_138 = &lStack_130;
  if (iVar2 != 5) goto LAB_10017e9f8;
  plVar19 = (long *)plVar7[1];
  if ((*(ushort *)((long)plVar7 + 0x16) & 0x1000) != 0) {
    plVar19 = plVar7;
  }
  if ((plVar19 != (long *)pcVar12) &&
     (iVar18 != (int)*plVar19 || *(char *)((long)plVar19 + 4) != 's')) goto LAB_10017e9f8;
  if (lVar16 != 0) {
    if (*(uint *)(plVar7 + 3) != 0) {
      lVar13 = plVar7[4];
      lVar16 = lVar13 + (ulong)*(uint *)(plVar7 + 3) * 0x30;
      do {
        if (*(short *)(lVar13 + 0x2e) == 4) {
          if (*(uint *)(lVar13 + 0x18) != 0) {
            lVar14 = (ulong)*(uint *)(lVar13 + 0x18) * 0x18;
            puVar17 = (ushort *)(*(long *)(lVar13 + 0x20) + 0x16);
            do {
              if ((*puVar17 >> 4 & 1) == 0) goto LAB_10017ea68;
              lVar14 = lVar14 + -0x18;
              puVar17 = puVar17 + 0xc;
            } while (lVar14 != 0);
          }
          local_140 = *(long *)(lVar13 + 8);
          if ((*(ushort *)(lVar13 + 0x16) & 0x1000) != 0) {
            local_140 = lVar13;
          }
          FUN_10017ceb4(&local_d0,0x12,lVar13 + 0x18);
          FUN_100184b98(&local_138,&local_140,&local_d0);
          if (pvStack_c8 != (void *)0x0) {
            local_c0 = pvStack_c8;
            operator_delete(pvStack_c8);
          }
        }
LAB_10017ea68:
        lVar13 = lVar13 + 0x30;
      } while (lVar13 != lVar16);
      if (local_128 == 0) goto LAB_10017eb54;
      *param_1 = (long)local_138;
      param_1[1] = lStack_130;
      param_1[2] = local_128;
      *(long **)(lStack_130 + 0x10) = param_1 + 1;
      lStack_130 = 0;
      local_128 = 0;
      *(undefined4 *)(param_1 + 4) = 0;
      local_138 = &lStack_130;
      goto LAB_10017eb84;
    }
    goto LAB_10017eb54;
  }
  goto LAB_10017eb3c;
LAB_10017e9f8:
  plVar7 = plVar7 + 6;
  lVar16 = lVar16 + -0x30;
  if (lVar16 == 0) goto LAB_10017eb3c;
  goto LAB_10017ea04;
LAB_10017eb3c:
  puVar8 = (undefined8 *)(**(code **)PTR_buffer_100d617b8)();
  *puVar8 = 0;
  puVar8[1] = 0;
  puVar8[2] = 0;
LAB_10017eb54:
  FUN_100171dc4(&local_d0,"Sound similarity feature file doesn\'t contain any usable feature values"
               );
  param_1[1] = (long)pvStack_c8;
  *param_1 = (long)local_d0;
  param_1[2] = (long)local_c0;
  *(undefined1 *)(param_1 + 3) = 1;
  *(undefined4 *)(param_1 + 4) = 1;
LAB_10017eb84:
  FUN_100184b28(&local_138,lStack_130);
  goto LAB_10017e8e4;
LAB_10017e6c4:
  do {
    piVar1 = (int *)((long)plStack_a8 + lVar13);
    iVar2 = *piVar1;
    if ((*(ushort *)((long)piVar1 + 0x16) & 0x1000) != 0) {
      iVar2 = 0x15 - *(char *)((long)piVar1 + 0x15);
    }
    if (iVar2 == 5) {
      piVar3 = *(int **)(piVar1 + 2);
      if ((*(ushort *)((long)piVar1 + 0x16) & 0x1000) != 0) {
        piVar3 = piVar1;
      }
      if ((piVar3 == (int *)"Files") || (*piVar3 == 0x656c6946 && (char)piVar3[1] == 's')) {
        if (lVar16 - lVar13 != 0) {
          pcVar11 = (char *)((long)plStack_a8 + lVar13 + 0x18);
          plVar7 = plStack_a8;
          goto LAB_10017e7dc;
        }
        break;
      }
    }
    lVar13 = lVar13 + 0x30;
  } while (lVar16 - lVar13 != 0);
  pcVar11 = (char *)(**(code **)PTR_buffer_100d617b8)();
  pcVar11[0] = '\0';
  pcVar11[1] = '\0';
  pcVar11[2] = '\0';
  pcVar11[3] = '\0';
  pcVar11[4] = '\0';
  pcVar11[5] = '\0';
  pcVar11[6] = '\0';
  pcVar11[7] = '\0';
  pcVar11[8] = '\0';
  pcVar11[9] = '\0';
  pcVar11[10] = '\0';
  pcVar11[0xb] = '\0';
  pcVar11[0xc] = '\0';
  pcVar11[0xd] = '\0';
  pcVar11[0xe] = '\0';
  pcVar11[0xf] = '\0';
  pcVar11[0x10] = '\0';
  pcVar11[0x11] = '\0';
  pcVar11[0x12] = '\0';
  pcVar11[0x13] = '\0';
  pcVar11[0x14] = '\0';
  pcVar11[0x15] = '\0';
  pcVar11[0x16] = '\0';
  pcVar11[0x17] = '\0';
  plVar7 = extraout_x8;
  lVar16 = extraout_x9;
  pcVar12 = (char *)extraout_x11;
  iVar18 = extraout_w10;
LAB_10017e7dc:
  plVar19 = plVar7;
  lVar13 = lVar16;
  if (*(short *)(pcVar11 + 0x16) == 3) {
    do {
      iVar2 = (int)*plVar19;
      if ((*(ushort *)((long)plVar19 + 0x16) & 0x1000) != 0) {
        iVar2 = 0x15 - *(char *)((long)plVar19 + 0x15);
      }
      if (iVar2 == 5) {
        plVar20 = (long *)plVar19[1];
        if ((*(ushort *)((long)plVar19 + 0x16) & 0x1000) != 0) {
          plVar20 = plVar19;
        }
        if ((plVar20 == (long *)pcVar12) ||
           (iVar18 == (int)*plVar20 && *(char *)((long)plVar20 + 4) == 's')) {
          if (lVar13 != 0) {
            plVar20 = plVar7;
            lVar13 = lVar16;
            if ((int)plVar19[3] == 0) goto LAB_10017e9b8;
            goto LAB_10017e928;
          }
          break;
        }
      }
      lVar13 = lVar13 + -0x30;
      plVar19 = plVar19 + 6;
    } while (lVar13 != 0);
    puVar8 = (undefined8 *)(**(code **)PTR_buffer_100d617b8)();
    *puVar8 = 0;
    puVar8[1] = 0;
    puVar8[2] = 0;
LAB_10017e9b8:
    pcVar12 = operator_new(0x28);
    uVar6 = s_Sound_similarity_feature_file_is_100c1e55e._16_8_;
    uVar5 = s_Sound_similarity_feature_file_is_100c1e55e._0_8_;
    uVar4 = CONCAT26(s_Sound_similarity_feature_file_is_100c1e55e._30_2_,
                     s_Sound_similarity_feature_file_is_100c1e55e._24_6_);
    *(undefined8 *)(pcVar12 + 8) = s_Sound_similarity_feature_file_is_100c1e55e._8_8_;
    *(undefined8 *)pcVar12 = uVar5;
    *(undefined8 *)(pcVar12 + 0x18) = uVar4;
    *(undefined8 *)(pcVar12 + 0x10) = uVar6;
    *(ulong *)(pcVar12 + 0x1e) =
         CONCAT62(s_Sound_similarity_feature_file_is_100c1e55e._32_6_,
                  s_Sound_similarity_feature_file_is_100c1e55e._30_2_);
    pcVar12[0x26] = '\0';
    *param_1 = (long)pcVar12;
    lVar13 = _DAT_100ba1730;
    lVar16 = _UNK_100ba1738;
    goto LAB_10017e9e8;
  }
LAB_10017e89c:
  pcVar12 = operator_new(0x40);
  uVar6 = s_Sound_similarity_feature_file_do_100c1e525._24_8_;
  uVar5 = s_Sound_similarity_feature_file_do_100c1e525._16_8_;
  uVar4 = s_Sound_similarity_feature_file_do_100c1e525._0_8_;
  *(undefined8 *)(pcVar12 + 8) = s_Sound_similarity_feature_file_do_100c1e525._8_8_;
  *(undefined8 *)pcVar12 = uVar4;
  *(undefined8 *)(pcVar12 + 0x18) = uVar6;
  *(undefined8 *)(pcVar12 + 0x10) = uVar5;
  uVar4 = s_Sound_similarity_feature_file_do_100c1e525._32_8_;
  *(undefined8 *)(pcVar12 + 0x28) = s_Sound_similarity_feature_file_do_100c1e525._40_8_;
  *(undefined8 *)(pcVar12 + 0x20) = uVar4;
  *(undefined8 *)(pcVar12 + 0x30) = s_Sound_similarity_feature_file_do_100c1e525._48_8_;
  pcVar12[0x38] = '\0';
  *param_1 = (long)pcVar12;
  lVar13 = _DAT_100ba1740;
  lVar16 = _UNK_100ba1748;
LAB_10017e8d4:
  param_1[2] = lVar16;
  param_1[1] = lVar13;
LAB_10017e8d8:
  *(undefined1 *)(param_1 + 3) = 1;
LAB_10017e8e0:
  *(undefined4 *)(param_1 + 4) = 1;
LAB_10017e8e4:
  FUN_10014d918(&local_b0);
  if (*(long *)PTR____stack_chk_guard_100d60390 != local_48) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}

