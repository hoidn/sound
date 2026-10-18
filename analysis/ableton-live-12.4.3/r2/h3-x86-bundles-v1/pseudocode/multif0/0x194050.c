// 0x194050 _mf0p_GetMultiF0Result | undefined _mf0p_GetMultiF0Result() | state=exported-with-warnings | chunk-00006.jsonl

undefined8 * _mf0p_GetMultiF0Result(long param_1)

{
  char *pcVar1;
  undefined4 *puVar2;
  undefined1 (*pauVar3) [16];
  float fVar4;
  undefined4 uVar5;
  int iVar6;
  undefined8 uVar7;
  undefined4 *puVar8;
  undefined1 (*pauVar9) [16];
  undefined4 *puVar10;
  undefined1 auVar11 [16];
  undefined1 auVar12 [16];
  undefined1 auVar13 [16];
  undefined1 auVar14 [16];
  undefined *puVar15;
  char cVar16;
  uint uVar17;
  uint uVar18;
  int iVar19;
  ulong uVar20;
  undefined8 *puVar21;
  long lVar22;
  void *pvVar23;
  undefined4 *puVar24;
  long lVar25;
  int iVar26;
  int iVar27;
  ulong uVar28;
  undefined8 *puVar29;
  undefined1 (*pauVar30) [16];
  undefined1 (*pauVar31) [16];
  undefined8 *puVar32;
  long lVar33;
  undefined8 uVar34;
  long lVar35;
  long lVar36;
  long lVar37;
  undefined8 uVar38;
  undefined8 *puVar39;
  ulong *puVar40;
  char *pcVar41;
  undefined8 *puVar42;
  int iVar43;
  bool bVar44;
  float fVar45;
  undefined1 auVar46 [16];
  undefined1 auVar47 [16];
  undefined1 auVar49 [16];
  undefined1 auVar50 [16];
  float fVar52;
  long local_d0;
  float local_a4;
  undefined8 *local_a0;
  ulong local_90;
  undefined8 *local_88;
  long local_80;
  undefined8 *local_78;
  long local_70;
  undefined8 *local_68;
  undefined8 *local_58;
  undefined8 *local_50;
  undefined8 *local_48;
  undefined1 auVar48 [16];
  undefined1 auVar51 [16];
  
  lVar36 = *(long *)(*(long *)(param_1 + 0x18) + 0xc0);
  fVar4 = *(float *)(lVar36 + 0x14);
  local_58 = (undefined8 *)0x0;
  local_50 = (undefined8 *)0x0;
  local_48 = (undefined8 *)0x0;
  if (0 < *(int *)(lVar36 + 0x90)) {
    iVar43 = 0;
    do {
      puVar42 = (undefined8 *)((long)iVar43 * 8 + *(long *)(lVar36 + 0x88));
      if (local_50 == local_48) {
        uVar20 = (long)local_50 - (long)local_58 >> 3;
        if (uVar20 == 0x1fffffffffffffff) {
                    /* WARNING: Subroutine does not return */
          std::__throw_length_error("vector::_M_insert_aux");
        }
        uVar28 = 1;
        if (uVar20 == 0) {
LAB_001941c4:
          if (0x1fffffffffffffff < uVar28) {
                    /* WARNING: Subroutine does not return */
            std::__throw_bad_alloc();
          }
          local_90 = uVar28 << 3;
        }
        else {
          uVar28 = uVar20 * 2;
          local_90 = 0xfffffffffffffff8;
          if (uVar20 <= uVar28) goto LAB_001941c4;
        }
        puVar21 = operator_new(local_90);
        _memmove(puVar21,local_58,(long)local_50 - (long)local_58);
        puVar29 = (undefined8 *)((long)puVar21 + ((long)local_50 - (long)local_58));
        if (puVar29 != (undefined8 *)0x0) {
          *puVar29 = *puVar42;
        }
        _memmove(puVar29 + 1,local_50,0);
        if (local_58 != (undefined8 *)0x0) {
          operator_delete(local_58);
        }
        local_48 = (undefined8 *)((long)puVar21 + local_90);
        local_58 = puVar21;
        local_50 = puVar29 + 1;
      }
      else {
        if (local_50 != (undefined8 *)0x0) {
          *local_50 = *puVar42;
        }
        local_50 = local_50 + 1;
      }
      iVar43 = iVar43 + 1;
    } while (iVar43 < *(int *)(lVar36 + 0x90));
  }
  if (local_50 != local_58) {
    lVar25 = (long)local_50 - (long)local_58 >> 3;
    if (lVar25 != 1) {
      local_d0 = 0;
      lVar22 = lVar25;
      do {
        local_d0 = local_d0 + 1;
        lVar22 = lVar22 >> 1;
      } while (lVar22 != 1);
      if (0x10 < lVar25) {
        local_d0 = local_d0 * 2;
        local_a0 = local_50;
        puVar42 = local_58 + 1;
LAB_0019425c:
        local_d0 = local_d0 + -1;
        uVar38 = local_58[((long)local_a0 - (long)local_58 >> 3) -
                          ((long)local_a0 - (long)local_58 >> 0x3f) >> 1];
        uVar34 = *local_58;
        cVar16 = FUN_00149b90(uVar34,uVar38);
        puVar21 = local_a0;
        puVar29 = puVar42;
        if (cVar16 == '\0') {
          uVar7 = local_a0[-1];
          cVar16 = FUN_00149b90(uVar34,uVar7);
          if (cVar16 == '\0') {
            cVar16 = FUN_00149b90(uVar38,uVar7);
            if (cVar16 != '\0') {
              uVar38 = uVar7;
            }
            goto LAB_001942d0;
          }
        }
        else {
          uVar7 = local_a0[-1];
          cVar16 = FUN_00149b90(uVar38,uVar7);
          if ((cVar16 != '\0') ||
             (cVar16 = FUN_00149b90(uVar34,uVar7), uVar38 = uVar7, cVar16 != '\0'))
          goto LAB_001942d0;
        }
        uVar38 = uVar34;
LAB_001942d0:
        do {
          puVar32 = puVar29 + -1;
          cVar16 = FUN_00149b90(uVar34,uVar38);
          if (cVar16 == '\0') {
            do {
              puVar21 = puVar21 + -1;
              uVar34 = *puVar21;
              cVar16 = FUN_00149b90(uVar38,uVar34);
            } while (cVar16 != '\0');
            if (puVar21 <= puVar32) goto LAB_00194320;
            uVar7 = *puVar32;
            *puVar32 = uVar34;
            *puVar21 = uVar7;
          }
          uVar34 = *puVar29;
          puVar29 = puVar29 + 1;
        } while( true );
      }
    }
    if (local_58 + 1 != local_50) {
      puVar42 = local_58 + 1;
      local_68 = local_58 + 2;
      do {
        uVar38 = *puVar42;
        cVar16 = FUN_00149b90(uVar38,*local_58);
        if (cVar16 == '\0') {
          puVar42 = local_68 + -2;
          puVar21 = local_68 + -1;
          while( true ) {
            puVar29 = puVar42;
            uVar34 = *puVar29;
            cVar16 = FUN_00149b90(uVar38,uVar34);
            if (cVar16 == '\0') break;
            *puVar21 = uVar34;
            puVar42 = puVar29 + -1;
            puVar21 = puVar29;
          }
          *puVar21 = uVar38;
        }
        else {
          uVar20 = (long)(local_68 + -1) - (long)local_58 & 0xfffffffffffffff8;
          _memmove((void *)((long)local_68 - uVar20),local_58,uVar20);
          *local_58 = uVar38;
        }
        bVar44 = local_68 != local_50;
        puVar42 = local_68;
        local_68 = local_68 + 1;
      } while (bVar44);
    }
  }
  goto LAB_001945b3;
LAB_00194320:
  FUN_00149d50(puVar32,local_a0,local_d0,FUN_00149b90);
  lVar25 = (long)puVar32 - (long)local_58 >> 3;
  if (lVar25 < 0x11) goto LAB_00194e89;
  local_a0 = puVar32;
  if (local_d0 == 0) goto code_r0x0019436a;
  goto LAB_0019425c;
code_r0x0019436a:
  if (1 < lVar25) {
    lVar22 = (lVar25 + -2) / 2;
    local_78 = local_58 + lVar22;
    local_70 = lVar22 * 2 + 2;
    do {
      uVar38 = *local_78;
      lVar35 = lVar22;
      puVar21 = local_78;
      for (lVar37 = local_70; lVar37 < lVar25; lVar37 = lVar37 * 2 + 2) {
        puVar21 = local_58 + lVar37;
        uVar34 = *puVar21;
        cVar16 = FUN_00149b90(uVar34,local_58[lVar37 + -1]);
        if (cVar16 != '\0') {
          lVar37 = lVar37 + -1;
          puVar21 = local_58 + lVar37;
          uVar34 = *puVar21;
        }
        local_58[lVar35] = uVar34;
        lVar35 = lVar37;
      }
      puVar39 = puVar21;
      if (lVar25 == lVar37) {
        lVar35 = lVar37 + -1;
        puVar39 = local_58 + lVar35;
        *puVar21 = *puVar39;
      }
      if (lVar22 < lVar35) {
        lVar37 = (lVar35 + -1) - (lVar35 + -1 >> 0x3f);
        while( true ) {
          lVar33 = lVar37 >> 1;
          puVar39 = local_58 + lVar33;
          uVar34 = *puVar39;
          cVar16 = FUN_00149b90(uVar34);
          if (cVar16 == '\0') break;
          local_58[lVar35] = uVar34;
          if (lVar33 <= lVar22) goto LAB_001944cf;
          lVar37 = (lVar33 + -1) - (lVar33 + -1 >> 0x3f);
          lVar35 = lVar33;
        }
        puVar39 = local_58 + lVar35;
      }
LAB_001944cf:
      *puVar39 = uVar38;
      local_78 = local_78 + -1;
      local_70 = local_70 + -2;
      if (lVar22 == 0) break;
      lVar22 = lVar22 + -1;
    } while( true );
  }
  if (1 < (long)puVar32 - (long)local_58 >> 3) {
    local_80 = (long)puVar29 + (-0x10 - (long)local_58);
    do {
      uVar38 = puVar32[-1];
      puVar32[-1] = *local_58;
      lVar25 = (long)(puVar32 + -1) - (long)local_58 >> 3;
      if (lVar25 < 3) {
        lVar22 = 2;
        lVar37 = 0;
        puVar21 = local_58;
      }
      else {
        lVar22 = 2;
        lVar35 = 0;
        do {
          puVar21 = local_58 + lVar22;
          uVar34 = *puVar21;
          cVar16 = FUN_00149b90(uVar34,local_58[lVar22 + -1]);
          lVar37 = lVar22;
          if (cVar16 != '\0') {
            lVar37 = lVar22 + -1;
            puVar21 = local_58 + lVar37;
            uVar34 = *puVar21;
          }
          local_58[lVar35] = uVar34;
          lVar22 = lVar37 * 2 + 2;
          lVar35 = lVar37;
        } while (lVar22 < lVar25);
      }
      puVar29 = puVar21;
      if (lVar25 == lVar22) {
        lVar37 = lVar22 + -1;
        puVar29 = local_58 + lVar37;
        *puVar21 = *puVar29;
      }
      if (0 < lVar37) {
        lVar25 = (lVar37 + -1) - (lVar37 + -1 >> 0x3f);
        while( true ) {
          lVar22 = lVar25 >> 1;
          puVar29 = local_58 + lVar22;
          uVar34 = *puVar29;
          cVar16 = FUN_00149b90(uVar34);
          if (cVar16 == '\0') break;
          local_58[lVar37] = uVar34;
          if (lVar22 == 0) goto LAB_00194e62;
          lVar25 = (lVar22 + -1) - (lVar22 + -1 >> 0x3f);
          lVar37 = lVar22;
        }
        puVar29 = local_58 + lVar37;
      }
LAB_00194e62:
      *puVar29 = uVar38;
      lVar25 = local_80 >> 3;
      local_80 = local_80 + -8;
      puVar32 = puVar32 + -1;
    } while (1 < lVar25);
  }
LAB_00194e89:
  puVar21 = local_58 + 0x10;
  if (puVar42 != puVar21) {
    local_88 = local_58 + 2;
    do {
      uVar38 = *puVar42;
      cVar16 = FUN_00149b90(uVar38,*local_58);
      if (cVar16 == '\0') {
        puVar42 = local_88 + -2;
        puVar29 = local_88 + -1;
        while( true ) {
          puVar32 = puVar42;
          uVar34 = *puVar32;
          cVar16 = FUN_00149b90(uVar38,uVar34);
          if (cVar16 == '\0') break;
          *puVar29 = uVar34;
          puVar42 = puVar32 + -1;
          puVar29 = puVar32;
        }
        *puVar29 = uVar38;
      }
      else {
        uVar20 = (long)(local_88 + -1) - (long)local_58 & 0xfffffffffffffff8;
        _memmove((void *)((long)local_88 - uVar20),local_58,uVar20);
        *local_58 = uVar38;
      }
      bVar44 = local_88 != puVar21;
      puVar42 = local_88;
      local_88 = local_88 + 1;
    } while (bVar44);
  }
  for (; local_50 != puVar21; puVar21 = puVar21 + 1) {
    uVar38 = *puVar21;
    puVar42 = puVar21;
    while( true ) {
      uVar34 = puVar42[-1];
      cVar16 = FUN_00149b90(uVar38,uVar34);
      if (cVar16 == '\0') break;
      *puVar42 = uVar34;
      puVar42 = puVar42 + -1;
    }
    *puVar42 = uVar38;
  }
LAB_001945b3:
  pvVar23 = _malloc((long)*(int *)(lVar36 + 0x90) << 5);
  if (local_58 < local_50) {
    local_a4 = DAT_0042b1f4;
    iVar43 = 0;
    puVar42 = local_58;
    do {
      puVar8 = (undefined4 *)*puVar42;
      if (*(char *)(puVar8 + 0xc) != '\0') {
        puVar2 = (undefined4 *)((long)iVar43 * 0x20 + (long)pvVar23);
        *puVar2 = *puVar8;
        puVar2[1] = puVar8[1];
        puVar2[2] = puVar8[3];
        puVar2[7] = (float)puVar8[5] / fVar4;
        pauVar9 = *(undefined1 (**) [16])(puVar8 + 0x2a);
        uVar18 = puVar8[0x2c];
        if (uVar18 == 0) {
          puVar42 = (undefined8 *)___cxa_allocate_exception(0x18);
          *puVar42 = &DAT_0046e970;
          puVar15 = PTR__S_empty_rep_storage_0046ead0;
          puVar42[1] = PTR__S_empty_rep_storage_0046ead0;
          puVar42[2] = puVar15;
          pcVar1 = (char *)(puVar42 + 1);
          std::string::assign(pcVar1,0x4239e0);
          cVar16 = s_min_max_elem_called_for_empty_ve_004239b8[0];
          lVar36 = puVar42[1];
          lVar25 = *(long *)(lVar36 + -0x18);
          uVar20 = lVar25 + 1;
          if ((*(ulong *)(lVar36 + -0x10) < uVar20) || (0 < *(int *)(lVar36 + -8))) {
            std::string::reserve((ulong)pcVar1);
          }
          *(char *)(puVar42[1] + *(long *)(puVar42[1] + -0x18)) = cVar16;
          puVar40 = (ulong *)(puVar42[1] + -0x18);
          *(undefined4 *)(puVar42[1] + -8) = 0;
          *puVar40 = uVar20;
          *(undefined1 *)(lVar25 + 0x19 + (long)puVar40) = 0;
          cVar16 = s_min_max_elem_called_for_empty_ve_004239b8[1];
          lVar36 = puVar42[1];
          lVar25 = *(long *)(lVar36 + -0x18);
          uVar20 = lVar25 + 1;
          if ((*(ulong *)(lVar36 + -0x10) < uVar20) || (0 < *(int *)(lVar36 + -8))) {
            std::string::reserve((ulong)pcVar1);
          }
          *(char *)(puVar42[1] + *(long *)(puVar42[1] + -0x18)) = cVar16;
          puVar40 = (ulong *)(puVar42[1] + -0x18);
          *(undefined4 *)(puVar42[1] + -8) = 0;
          *puVar40 = uVar20;
          *(undefined1 *)(lVar25 + 0x19 + (long)puVar40) = 0;
          pcVar41 = "/max_elem called for empty vector \n";
          do {
            cVar16 = pcVar41[-1];
            lVar36 = puVar42[1];
            lVar25 = *(long *)(lVar36 + -0x18);
            uVar20 = lVar25 + 1;
            if ((*(ulong *)(lVar36 + -0x10) < uVar20) || (0 < *(int *)(lVar36 + -8))) {
              std::string::reserve((ulong)pcVar1);
            }
            *(char *)(puVar42[1] + *(long *)(puVar42[1] + -0x18)) = cVar16;
            puVar40 = (ulong *)(puVar42[1] + -0x18);
            *(undefined4 *)(puVar42[1] + -8) = 0;
            *puVar40 = uVar20;
            *(undefined1 *)(lVar25 + 0x19 + (long)puVar40) = 0;
            cVar16 = *pcVar41;
            lVar36 = puVar42[1];
            lVar25 = *(long *)(lVar36 + -0x18);
            uVar20 = lVar25 + 1;
            if ((*(ulong *)(lVar36 + -0x10) < uVar20) || (0 < *(int *)(lVar36 + -8))) {
              std::string::reserve((ulong)pcVar1);
            }
            *(char *)(puVar42[1] + *(long *)(puVar42[1] + -0x18)) = cVar16;
            puVar40 = (ulong *)(puVar42[1] + -0x18);
            *(undefined4 *)(puVar42[1] + -8) = 0;
            *puVar40 = uVar20;
            *(undefined1 *)(lVar25 + 0x19 + (long)puVar40) = 0;
            cVar16 = pcVar41[1];
            lVar36 = puVar42[1];
            lVar25 = *(long *)(lVar36 + -0x18);
            uVar20 = lVar25 + 1;
            if ((*(ulong *)(lVar36 + -0x10) < uVar20) || (0 < *(int *)(lVar36 + -8))) {
              std::string::reserve((ulong)pcVar1);
            }
            *(char *)(puVar42[1] + *(long *)(puVar42[1] + -0x18)) = cVar16;
            puVar40 = (ulong *)(puVar42[1] + -0x18);
            *(undefined4 *)(puVar42[1] + -8) = 0;
            *puVar40 = uVar20;
            *(undefined1 *)(lVar25 + 0x19 + (long)puVar40) = 0;
            cVar16 = pcVar41[2];
            lVar36 = puVar42[1];
            lVar25 = *(long *)(lVar36 + -0x18);
            uVar20 = lVar25 + 1;
            if ((*(ulong *)(lVar36 + -0x10) < uVar20) || (0 < *(int *)(lVar36 + -8))) {
              std::string::reserve((ulong)pcVar1);
            }
            *(char *)(puVar42[1] + *(long *)(puVar42[1] + -0x18)) = cVar16;
            puVar40 = (ulong *)(puVar42[1] + -0x18);
            *(undefined4 *)(puVar42[1] + -8) = 0;
            *puVar40 = uVar20;
            *(undefined1 *)(lVar25 + 0x19 + (long)puVar40) = 0;
            pcVar41 = pcVar41 + 4;
          } while (pcVar41 != "");
                    /* WARNING: Subroutine does not return */
          ___cxa_throw(puVar42,&PTR_vtable_0046e940,FUN_000172a0);
        }
        pauVar3 = (undefined1 (*) [16])(*pauVar9 + (long)(int)(uVar18 & 0xfffffffc) * 4);
        uVar5 = *(undefined4 *)*pauVar9;
        auVar46._4_4_ = uVar5;
        auVar46._0_4_ = uVar5;
        auVar46._8_4_ = uVar5;
        auVar46._12_4_ = uVar5;
        if (pauVar9 != pauVar3) {
          uVar20 = (ulong)((long)pauVar3 + (-0x10 - (long)pauVar9)) >> 4;
          uVar17 = (uint)uVar20 & 7;
          auVar46 = maxps(auVar46,*pauVar9);
          pauVar31 = pauVar9 + 1;
          if (pauVar3 != pauVar31) {
            if ((uVar20 & 7) != 0) {
              if (uVar17 != 1) {
                if (uVar17 != 2) {
                  if (uVar17 != 3) {
                    if (uVar17 != 4) {
                      if (uVar17 != 5) {
                        if (uVar17 != 6) {
                          auVar46 = maxps(auVar46,pauVar9[1]);
                          pauVar31 = pauVar9 + 2;
                        }
                        auVar46 = maxps(auVar46,*pauVar31);
                        pauVar31 = pauVar31 + 1;
                      }
                      auVar46 = maxps(auVar46,*pauVar31);
                      pauVar31 = pauVar31 + 1;
                    }
                    auVar46 = maxps(auVar46,*pauVar31);
                    pauVar31 = pauVar31 + 1;
                  }
                  auVar46 = maxps(auVar46,*pauVar31);
                  pauVar31 = pauVar31 + 1;
                }
                auVar46 = maxps(auVar46,*pauVar31);
                pauVar31 = pauVar31 + 1;
              }
              auVar46 = maxps(auVar46,*pauVar31);
              pauVar31 = pauVar31 + 1;
              if (pauVar3 == pauVar31) goto LAB_0019471e;
            }
            do {
              auVar46 = maxps(auVar46,*pauVar31);
              auVar46 = maxps(auVar46,pauVar31[1]);
              auVar46 = maxps(auVar46,pauVar31[2]);
              auVar46 = maxps(auVar46,pauVar31[3]);
              auVar46 = maxps(auVar46,pauVar31[4]);
              auVar46 = maxps(auVar46,pauVar31[5]);
              auVar46 = maxps(auVar46,pauVar31[6]);
              auVar46 = maxps(auVar46,pauVar31[7]);
              pauVar31 = pauVar31 + 8;
            } while (pauVar3 != pauVar31);
          }
        }
LAB_0019471e:
        auVar48._0_8_ = auVar46._0_8_;
        auVar48._8_4_ = auVar46._4_4_;
        auVar48._12_4_ = auVar46._4_4_;
        auVar47._0_4_ = auVar46._0_4_;
        auVar47._8_8_ = auVar48._8_8_;
        auVar47._4_4_ = auVar47._0_4_;
        auVar12._4_4_ = auVar46._8_4_;
        auVar12._0_4_ = auVar46._8_4_;
        auVar12._8_4_ = auVar46._12_4_;
        auVar12._12_4_ = auVar46._12_4_;
        auVar46 = maxps(auVar47,auVar12);
        auVar11._4_4_ = auVar46._8_4_;
        auVar11._0_4_ = auVar46._8_4_;
        auVar11._8_4_ = auVar46._12_4_;
        auVar11._12_4_ = auVar46._12_4_;
        auVar46 = maxps(auVar46,auVar11);
        fVar45 = auVar46._0_4_;
        pauVar31 = (undefined1 (*) [16])(*pauVar3 + (ulong)(uVar18 & 3) * 4);
        if (pauVar3 != pauVar31) {
          uVar20 = (ulong)((long)pauVar31 + (-4 - (long)pauVar3)) >> 2;
          uVar17 = (uint)uVar20 & 7;
          fVar52 = *(float *)*pauVar3;
          if (*(float *)*pauVar3 <= fVar45) {
            fVar52 = fVar45;
          }
          fVar45 = fVar52;
          pauVar30 = (undefined1 (*) [16])(*pauVar3 + 4);
          if (pauVar31 != pauVar30) {
            if ((uVar20 & 7) != 0) {
              if (uVar17 != 1) {
                if (uVar17 != 2) {
                  if (uVar17 != 3) {
                    if (uVar17 != 4) {
                      if (uVar17 != 5) {
                        if (uVar17 != 6) {
                          fVar52 = *(float *)(*pauVar3 + 4);
                          if (*(float *)(*pauVar3 + 4) <= fVar45) {
                            fVar52 = fVar45;
                          }
                          fVar45 = fVar52;
                          pauVar30 = (undefined1 (*) [16])(*pauVar3 + 8);
                        }
                        fVar52 = *(float *)*pauVar30;
                        if (*(float *)*pauVar30 <= fVar45) {
                          fVar52 = fVar45;
                        }
                        fVar45 = fVar52;
                        pauVar30 = (undefined1 (*) [16])(*pauVar30 + 4);
                      }
                      fVar52 = *(float *)*pauVar30;
                      if (*(float *)*pauVar30 <= fVar45) {
                        fVar52 = fVar45;
                      }
                      fVar45 = fVar52;
                      pauVar30 = (undefined1 (*) [16])(*pauVar30 + 4);
                    }
                    fVar52 = *(float *)*pauVar30;
                    if (*(float *)*pauVar30 <= fVar45) {
                      fVar52 = fVar45;
                    }
                    fVar45 = fVar52;
                    pauVar30 = (undefined1 (*) [16])(*pauVar30 + 4);
                  }
                  fVar52 = *(float *)*pauVar30;
                  if (*(float *)*pauVar30 <= fVar45) {
                    fVar52 = fVar45;
                  }
                  fVar45 = fVar52;
                  pauVar30 = (undefined1 (*) [16])(*pauVar30 + 4);
                }
                fVar52 = *(float *)*pauVar30;
                if (*(float *)*pauVar30 <= fVar45) {
                  fVar52 = fVar45;
                }
                fVar45 = fVar52;
                pauVar30 = (undefined1 (*) [16])(*pauVar30 + 4);
              }
              fVar52 = *(float *)*pauVar30;
              if (*(float *)*pauVar30 <= fVar45) {
                fVar52 = fVar45;
              }
              fVar45 = fVar52;
              pauVar30 = (undefined1 (*) [16])(*pauVar30 + 4);
              if (pauVar31 == pauVar30) goto LAB_00194879;
            }
            do {
              fVar52 = *(float *)*pauVar30;
              if (*(float *)*pauVar30 <= fVar45) {
                fVar52 = fVar45;
              }
              fVar45 = *(float *)(*pauVar30 + 4);
              if (*(float *)(*pauVar30 + 4) <= fVar52) {
                fVar45 = fVar52;
              }
              fVar52 = *(float *)(*pauVar30 + 8);
              if (*(float *)(*pauVar30 + 8) <= fVar45) {
                fVar52 = fVar45;
              }
              fVar45 = *(float *)(*pauVar30 + 0xc);
              if (*(float *)(*pauVar30 + 0xc) <= fVar52) {
                fVar45 = fVar52;
              }
              fVar52 = *(float *)pauVar30[1];
              if (*(float *)pauVar30[1] <= fVar45) {
                fVar52 = fVar45;
              }
              fVar45 = *(float *)(pauVar30[1] + 4);
              if (*(float *)(pauVar30[1] + 4) <= fVar52) {
                fVar45 = fVar52;
              }
              fVar52 = *(float *)(pauVar30[1] + 8);
              if (*(float *)(pauVar30[1] + 8) <= fVar45) {
                fVar52 = fVar45;
              }
              fVar45 = *(float *)(pauVar30[1] + 0xc);
              if (*(float *)(pauVar30[1] + 0xc) <= fVar52) {
                fVar45 = fVar52;
              }
              pauVar30 = pauVar30 + 2;
            } while (pauVar31 != pauVar30);
          }
        }
LAB_00194879:
        if (local_a4 < fVar45) {
          if (uVar18 == 0) {
            puVar42 = (undefined8 *)___cxa_allocate_exception(0x18);
            *puVar42 = &DAT_0046e970;
            puVar15 = PTR__S_empty_rep_storage_0046ead0;
            puVar42[1] = PTR__S_empty_rep_storage_0046ead0;
            puVar42[2] = puVar15;
            pcVar1 = (char *)(puVar42 + 1);
            std::string::assign(pcVar1,0x4239e0);
            cVar16 = s_min_max_elem_called_for_empty_ve_004239b8[0];
            lVar36 = puVar42[1];
            lVar25 = *(long *)(lVar36 + -0x18);
            uVar20 = lVar25 + 1;
            if ((*(ulong *)(lVar36 + -0x10) < uVar20) || (0 < *(int *)(lVar36 + -8))) {
              std::string::reserve((ulong)pcVar1);
            }
            *(char *)(puVar42[1] + *(long *)(puVar42[1] + -0x18)) = cVar16;
            puVar40 = (ulong *)(puVar42[1] + -0x18);
            *(undefined4 *)(puVar42[1] + -8) = 0;
            *puVar40 = uVar20;
            *(undefined1 *)(lVar25 + 0x19 + (long)puVar40) = 0;
            cVar16 = s_min_max_elem_called_for_empty_ve_004239b8[1];
            lVar36 = puVar42[1];
            lVar25 = *(long *)(lVar36 + -0x18);
            uVar20 = lVar25 + 1;
            if ((*(ulong *)(lVar36 + -0x10) < uVar20) || (0 < *(int *)(lVar36 + -8))) {
              std::string::reserve((ulong)pcVar1);
            }
            *(char *)(puVar42[1] + *(long *)(puVar42[1] + -0x18)) = cVar16;
            puVar40 = (ulong *)(puVar42[1] + -0x18);
            *(undefined4 *)(puVar42[1] + -8) = 0;
            *puVar40 = uVar20;
            *(undefined1 *)(lVar25 + 0x19 + (long)puVar40) = 0;
            pcVar41 = "/max_elem called for empty vector \n";
            do {
              cVar16 = pcVar41[-1];
              lVar36 = puVar42[1];
              lVar25 = *(long *)(lVar36 + -0x18);
              uVar20 = lVar25 + 1;
              if ((*(ulong *)(lVar36 + -0x10) < uVar20) || (0 < *(int *)(lVar36 + -8))) {
                std::string::reserve((ulong)pcVar1);
              }
              *(char *)(puVar42[1] + *(long *)(puVar42[1] + -0x18)) = cVar16;
              puVar40 = (ulong *)(puVar42[1] + -0x18);
              *(undefined4 *)(puVar42[1] + -8) = 0;
              *puVar40 = uVar20;
              *(undefined1 *)(lVar25 + 0x19 + (long)puVar40) = 0;
              cVar16 = *pcVar41;
              lVar36 = puVar42[1];
              lVar25 = *(long *)(lVar36 + -0x18);
              uVar20 = lVar25 + 1;
              if ((*(ulong *)(lVar36 + -0x10) < uVar20) || (0 < *(int *)(lVar36 + -8))) {
                std::string::reserve((ulong)pcVar1);
              }
              *(char *)(puVar42[1] + *(long *)(puVar42[1] + -0x18)) = cVar16;
              puVar40 = (ulong *)(puVar42[1] + -0x18);
              *(undefined4 *)(puVar42[1] + -8) = 0;
              *puVar40 = uVar20;
              *(undefined1 *)(lVar25 + 0x19 + (long)puVar40) = 0;
              cVar16 = pcVar41[1];
              lVar36 = puVar42[1];
              lVar25 = *(long *)(lVar36 + -0x18);
              uVar20 = lVar25 + 1;
              if ((*(ulong *)(lVar36 + -0x10) < uVar20) || (0 < *(int *)(lVar36 + -8))) {
                std::string::reserve((ulong)pcVar1);
              }
              *(char *)(puVar42[1] + *(long *)(puVar42[1] + -0x18)) = cVar16;
              puVar40 = (ulong *)(puVar42[1] + -0x18);
              *(undefined4 *)(puVar42[1] + -8) = 0;
              *puVar40 = uVar20;
              *(undefined1 *)(lVar25 + 0x19 + (long)puVar40) = 0;
              cVar16 = pcVar41[2];
              lVar36 = puVar42[1];
              lVar25 = *(long *)(lVar36 + -0x18);
              uVar20 = lVar25 + 1;
              if ((*(ulong *)(lVar36 + -0x10) < uVar20) || (0 < *(int *)(lVar36 + -8))) {
                std::string::reserve((ulong)pcVar1);
              }
              *(char *)(puVar42[1] + *(long *)(puVar42[1] + -0x18)) = cVar16;
              puVar40 = (ulong *)(puVar42[1] + -0x18);
              *(undefined4 *)(puVar42[1] + -8) = 0;
              *puVar40 = uVar20;
              *(undefined1 *)(lVar25 + 0x19 + (long)puVar40) = 0;
              pcVar41 = pcVar41 + 4;
            } while (pcVar41 != "");
                    /* WARNING: Subroutine does not return */
            ___cxa_throw(puVar42,&PTR_vtable_0046e940,FUN_000172a0);
          }
          pauVar3 = (undefined1 (*) [16])(*pauVar9 + (long)(int)(uVar18 & 0xfffffffc) * 4);
          uVar5 = *(undefined4 *)*pauVar9;
          auVar49._4_4_ = uVar5;
          auVar49._0_4_ = uVar5;
          auVar49._8_4_ = uVar5;
          auVar49._12_4_ = uVar5;
          if (pauVar9 != pauVar3) {
            uVar20 = (ulong)((long)pauVar3 + (-0x10 - (long)pauVar9)) >> 4;
            uVar17 = (uint)uVar20 & 7;
            auVar49 = maxps(auVar49,*pauVar9);
            pauVar31 = pauVar9 + 1;
            if (pauVar3 != pauVar31) {
              if ((uVar20 & 7) != 0) {
                if (uVar17 != 1) {
                  if (uVar17 != 2) {
                    if (uVar17 != 3) {
                      if (uVar17 != 4) {
                        if (uVar17 != 5) {
                          if (uVar17 != 6) {
                            auVar49 = maxps(auVar49,pauVar9[1]);
                            pauVar31 = pauVar9 + 2;
                          }
                          auVar49 = maxps(auVar49,*pauVar31);
                          pauVar31 = pauVar31 + 1;
                        }
                        auVar49 = maxps(auVar49,*pauVar31);
                        pauVar31 = pauVar31 + 1;
                      }
                      auVar49 = maxps(auVar49,*pauVar31);
                      pauVar31 = pauVar31 + 1;
                    }
                    auVar49 = maxps(auVar49,*pauVar31);
                    pauVar31 = pauVar31 + 1;
                  }
                  auVar49 = maxps(auVar49,*pauVar31);
                  pauVar31 = pauVar31 + 1;
                }
                auVar49 = maxps(auVar49,*pauVar31);
                pauVar31 = pauVar31 + 1;
                if (pauVar3 == pauVar31) goto LAB_00194955;
              }
              do {
                auVar46 = maxps(auVar49,*pauVar31);
                auVar46 = maxps(auVar46,pauVar31[1]);
                auVar46 = maxps(auVar46,pauVar31[2]);
                auVar46 = maxps(auVar46,pauVar31[3]);
                auVar46 = maxps(auVar46,pauVar31[4]);
                auVar46 = maxps(auVar46,pauVar31[5]);
                auVar46 = maxps(auVar46,pauVar31[6]);
                auVar49 = maxps(auVar46,pauVar31[7]);
                pauVar31 = pauVar31 + 8;
              } while (pauVar3 != pauVar31);
            }
          }
LAB_00194955:
          auVar51._0_8_ = auVar49._0_8_;
          auVar51._8_4_ = auVar49._4_4_;
          auVar51._12_4_ = auVar49._4_4_;
          auVar50._0_4_ = auVar49._0_4_;
          auVar50._8_8_ = auVar51._8_8_;
          auVar50._4_4_ = auVar50._0_4_;
          auVar14._4_4_ = auVar49._8_4_;
          auVar14._0_4_ = auVar49._8_4_;
          auVar14._8_4_ = auVar49._12_4_;
          auVar14._12_4_ = auVar49._12_4_;
          auVar46 = maxps(auVar50,auVar14);
          auVar13._4_4_ = auVar46._8_4_;
          auVar13._0_4_ = auVar46._8_4_;
          auVar13._8_4_ = auVar46._12_4_;
          auVar13._12_4_ = auVar46._12_4_;
          auVar46 = maxps(auVar46,auVar13);
          fVar45 = auVar46._0_4_;
          pauVar9 = (undefined1 (*) [16])(*pauVar3 + (ulong)(uVar18 & 3) * 4);
          local_a4 = fVar45;
          if (pauVar3 != pauVar9) {
            uVar20 = (ulong)((long)pauVar9 + (-4 - (long)pauVar3)) >> 2;
            uVar18 = (uint)uVar20 & 7;
            local_a4 = *(float *)*pauVar3;
            if (*(float *)*pauVar3 <= fVar45) {
              local_a4 = fVar45;
            }
            pauVar31 = (undefined1 (*) [16])(*pauVar3 + 4);
            if (pauVar9 != pauVar31) {
              if ((uVar20 & 7) != 0) {
                if (uVar18 != 1) {
                  if (uVar18 != 2) {
                    if (uVar18 != 3) {
                      if (uVar18 != 4) {
                        if (uVar18 != 5) {
                          if (uVar18 != 6) {
                            fVar45 = *(float *)(*pauVar3 + 4);
                            if (*(float *)(*pauVar3 + 4) <= local_a4) {
                              fVar45 = local_a4;
                            }
                            local_a4 = fVar45;
                            pauVar31 = (undefined1 (*) [16])(*pauVar3 + 8);
                          }
                          fVar45 = *(float *)*pauVar31;
                          if (*(float *)*pauVar31 <= local_a4) {
                            fVar45 = local_a4;
                          }
                          local_a4 = fVar45;
                          pauVar31 = (undefined1 (*) [16])(*pauVar31 + 4);
                        }
                        fVar45 = *(float *)*pauVar31;
                        if (*(float *)*pauVar31 <= local_a4) {
                          fVar45 = local_a4;
                        }
                        local_a4 = fVar45;
                        pauVar31 = (undefined1 (*) [16])(*pauVar31 + 4);
                      }
                      fVar45 = *(float *)*pauVar31;
                      if (*(float *)*pauVar31 <= local_a4) {
                        fVar45 = local_a4;
                      }
                      local_a4 = fVar45;
                      pauVar31 = (undefined1 (*) [16])(*pauVar31 + 4);
                    }
                    fVar45 = *(float *)*pauVar31;
                    if (*(float *)*pauVar31 <= local_a4) {
                      fVar45 = local_a4;
                    }
                    local_a4 = fVar45;
                    pauVar31 = (undefined1 (*) [16])(*pauVar31 + 4);
                  }
                  fVar45 = *(float *)*pauVar31;
                  if (*(float *)*pauVar31 <= local_a4) {
                    fVar45 = local_a4;
                  }
                  local_a4 = fVar45;
                  pauVar31 = (undefined1 (*) [16])(*pauVar31 + 4);
                }
                fVar45 = *(float *)*pauVar31;
                if (*(float *)*pauVar31 <= local_a4) {
                  fVar45 = local_a4;
                }
                local_a4 = fVar45;
                pauVar31 = (undefined1 (*) [16])(*pauVar31 + 4);
                if (pauVar9 == pauVar31) goto LAB_00194aba;
              }
              do {
                fVar45 = *(float *)*pauVar31;
                if (*(float *)*pauVar31 <= local_a4) {
                  fVar45 = local_a4;
                }
                fVar52 = *(float *)(*pauVar31 + 4);
                if (*(float *)(*pauVar31 + 4) <= fVar45) {
                  fVar52 = fVar45;
                }
                fVar45 = *(float *)(*pauVar31 + 8);
                if (*(float *)(*pauVar31 + 8) <= fVar52) {
                  fVar45 = fVar52;
                }
                fVar52 = *(float *)(*pauVar31 + 0xc);
                if (*(float *)(*pauVar31 + 0xc) <= fVar45) {
                  fVar52 = fVar45;
                }
                fVar45 = *(float *)pauVar31[1];
                if (*(float *)pauVar31[1] <= fVar52) {
                  fVar45 = fVar52;
                }
                fVar52 = *(float *)(pauVar31[1] + 4);
                if (*(float *)(pauVar31[1] + 4) <= fVar45) {
                  fVar52 = fVar45;
                }
                fVar45 = *(float *)(pauVar31[1] + 8);
                if (*(float *)(pauVar31[1] + 8) <= fVar52) {
                  fVar45 = fVar52;
                }
                local_a4 = *(float *)(pauVar31[1] + 0xc);
                if (*(float *)(pauVar31[1] + 0xc) <= fVar45) {
                  local_a4 = fVar45;
                }
                pauVar31 = pauVar31 + 2;
              } while (pauVar9 != pauVar31);
            }
          }
        }
LAB_00194aba:
        iVar6 = puVar8[0x1e];
        puVar24 = _malloc((long)iVar6 << 3);
        if (0 < iVar6) {
          iVar27 = 0;
          lVar36 = 0;
          puVar10 = *(undefined4 **)(puVar8 + 0x1c);
          puVar8 = *(undefined4 **)(puVar8 + 0xe);
          uVar18 = iVar6 - 1U & 7;
          if (uVar18 != 0) {
            puVar24[1] = *puVar10;
            *puVar24 = *puVar8;
            iVar19 = 1;
            lVar36 = 4;
            iVar27 = 1;
            iVar26 = 1;
            if (uVar18 != 1) {
              if (uVar18 != 2) {
                if (uVar18 != 3) {
                  if (uVar18 != 4) {
                    if (uVar18 != 5) {
                      if (uVar18 != 6) {
                        puVar24[3] = puVar10[1];
                        puVar24[2] = puVar8[1];
                        iVar19 = 2;
                        lVar36 = 8;
                        iVar26 = 2;
                      }
                      puVar24[(long)iVar19 * 2 + 1] = puVar10[iVar19];
                      *(undefined4 *)((long)puVar24 + lVar36 * 2) =
                           *(undefined4 *)(lVar36 + (long)puVar8);
                      iVar26 = iVar26 + 1;
                      lVar36 = lVar36 + 4;
                    }
                    puVar24[(long)iVar26 * 2 + 1] = puVar10[iVar26];
                    *(undefined4 *)((long)puVar24 + lVar36 * 2) =
                         *(undefined4 *)(lVar36 + (long)puVar8);
                    iVar26 = iVar26 + 1;
                    lVar36 = lVar36 + 4;
                  }
                  puVar24[(long)iVar26 * 2 + 1] = puVar10[iVar26];
                  *(undefined4 *)((long)puVar24 + lVar36 * 2) =
                       *(undefined4 *)(lVar36 + (long)puVar8);
                  iVar26 = iVar26 + 1;
                  lVar36 = lVar36 + 4;
                }
                puVar24[(long)iVar26 * 2 + 1] = puVar10[iVar26];
                *(undefined4 *)((long)puVar24 + lVar36 * 2) = *(undefined4 *)(lVar36 + (long)puVar8)
                ;
                iVar26 = iVar26 + 1;
                lVar36 = lVar36 + 4;
              }
              puVar24[(long)iVar26 * 2 + 1] = puVar10[iVar26];
              *(undefined4 *)((long)puVar24 + lVar36 * 2) = *(undefined4 *)(lVar36 + (long)puVar8);
              iVar27 = iVar26 + 1;
              lVar36 = lVar36 + 4;
            }
          }
          while( true ) {
            puVar24[(long)iVar27 * 2 + 1] = puVar10[iVar27];
            *(undefined4 *)((long)puVar24 + lVar36 * 2) = *(undefined4 *)(lVar36 + (long)puVar8);
            iVar19 = iVar27 + 1;
            if (iVar19 == iVar6) break;
            puVar24[(long)iVar19 * 2 + 1] = puVar10[iVar19];
            *(undefined4 *)((long)puVar24 + (lVar36 + 4) * 2) =
                 *(undefined4 *)(lVar36 + 4 + (long)puVar8);
            puVar24[(long)(iVar27 + 2) * 2 + 1] = puVar10[iVar27 + 2];
            *(undefined4 *)((long)puVar24 + lVar36 * 2 + 0x10) =
                 *(undefined4 *)(lVar36 + 8 + (long)puVar8);
            puVar24[(long)(iVar27 + 3) * 2 + 1] = puVar10[iVar27 + 3];
            *(undefined4 *)((long)puVar24 + lVar36 * 2 + 0x18) =
                 *(undefined4 *)(lVar36 + 0xc + (long)puVar8);
            puVar24[(long)(iVar27 + 4) * 2 + 1] = puVar10[iVar27 + 4];
            *(undefined4 *)((long)puVar24 + lVar36 * 2 + 0x20) =
                 *(undefined4 *)(lVar36 + 0x10 + (long)puVar8);
            puVar24[(long)(iVar27 + 5) * 2 + 1] = puVar10[iVar27 + 5];
            *(undefined4 *)((long)puVar24 + lVar36 * 2 + 0x28) =
                 *(undefined4 *)(lVar36 + 0x14 + (long)puVar8);
            puVar24[(long)(iVar27 + 6) * 2 + 1] = puVar10[iVar27 + 6];
            *(undefined4 *)((long)puVar24 + lVar36 * 2 + 0x30) =
                 *(undefined4 *)(lVar36 + 0x18 + (long)puVar8);
            puVar24[(long)(iVar27 + 7) * 2 + 1] = puVar10[iVar27 + 7];
            *(undefined4 *)((long)puVar24 + lVar36 * 2 + 0x38) =
                 *(undefined4 *)(lVar36 + 0x1c + (long)puVar8);
            iVar27 = iVar27 + 8;
            lVar36 = lVar36 + 0x20;
          }
        }
        puVar2[6] = iVar6;
        *(undefined4 **)(puVar2 + 4) = puVar24;
        iVar43 = iVar43 + 1;
      }
      puVar42 = puVar42 + 1;
    } while (puVar42 < local_50);
  }
  else {
    iVar43 = 0;
  }
  puVar42 = _malloc(0x10);
  *puVar42 = pvVar23;
  *(int *)(puVar42 + 1) = iVar43;
  if (local_58 != (undefined8 *)0x0) {
    operator_delete(local_58);
  }
  return puVar42;
}

