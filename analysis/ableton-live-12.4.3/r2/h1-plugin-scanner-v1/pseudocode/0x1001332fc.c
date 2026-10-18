
/* WARNING: Type propagation algorithm not settling */

void FUN_1001332fc(undefined8 *param_1,long param_2,char *param_3)

{
  undefined8 *puVar1;
  ulong uVar2;
  ulong uVar3;
  undefined8 *puVar4;
  long *plVar5;
  bool bVar6;
  void *pvVar7;
  int *******pppppppiVar8;
  byte bVar9;
  undefined7 uVar10;
  undefined1 uVar11;
  undefined7 uVar12;
  code *pcVar13;
  int iVar14;
  size_t sVar15;
  undefined8 *******pppppppuVar16;
  undefined *puVar17;
  undefined1 **ppuVar18;
  int *******pppppppiVar19;
  undefined8 uVar20;
  long lVar21;
  ulong uVar22;
  undefined1 **ppuVar23;
  long *plVar24;
  undefined1 *local_130;
  ulong local_128;
  undefined8 uStack_120;
  int *******local_118;
  undefined7 uStack_110;
  undefined1 uStack_109;
  undefined7 local_108;
  byte bStack_101;
  int *******local_100;
  undefined8 *******local_f8;
  ulong local_f0;
  undefined8 local_e8;
  ulong local_e0;
  undefined8 *local_d8;
  undefined8 *local_d0;
  undefined8 *******local_c0;
  ulong uStack_b8;
  ulong local_b0;
  int *******local_a0;
  undefined7 local_98;
  undefined1 uStack_91;
  undefined7 uStack_90;
  byte local_89;
  undefined7 local_88;
  undefined1 uStack_81;
  undefined7 uStack_80;
  long local_78;
  
  local_78 = *(long *)PTR____stack_chk_guard_100b1c378;
  *param_1 = 0;
  param_1[1] = 0;
  param_1[2] = 0;
  sVar15 = _strlen(param_3);
  if (0x7ffffffffffffff7 < sVar15) {
                    /* WARNING: Subroutine does not return */
    FUN_100134f2c(&local_f8);
  }
  if (sVar15 < 0x17) {
    local_e8 = (void *)CONCAT17((char)sVar15,(undefined7)local_e8);
    pppppppuVar16 = &local_f8;
    if (sVar15 != 0) goto LAB_1001333ac;
                    /* WARNING: Ignoring partial resolution of indirect */
    local_f8._0_1_ = 0;
    plVar24 = *(long **)(param_2 + 0x18);
    uVar22 = 0;
  }
  else {
    uVar22 = 0x19;
    if ((sVar15 | 7) != 0x17) {
      uVar22 = (sVar15 | 7) + 1;
    }
    pppppppuVar16 = operator_new(uVar22);
    local_e8 = (void *)(uVar22 | 0x8000000000000000);
    local_f8 = pppppppuVar16;
    local_f0 = sVar15;
LAB_1001333ac:
    _memcpy(pppppppuVar16,param_3,sVar15);
    *(undefined1 *)((long)pppppppuVar16 + sVar15) = 0;
    plVar24 = *(long **)(param_2 + 0x18);
    uVar22 = (ulong)local_e8 >> 0x38;
  }
  if (plVar24 != (long *)0x0) {
    pppppppuVar16 = local_f8;
    uVar3 = local_f0;
    if (-1 < (char)uVar22) {
      pppppppuVar16 = &local_f8;
      uVar3 = uVar22;
    }
    do {
      uVar2 = plVar24[5];
      plVar5 = (long *)plVar24[4];
      if (-1 < (char)*(byte *)((long)plVar24 + 0x37)) {
        uVar2 = (ulong)*(byte *)((long)plVar24 + 0x37);
        plVar5 = plVar24 + 4;
      }
      sVar15 = uVar2;
      if (uVar3 <= uVar2) {
        sVar15 = uVar3;
      }
      iVar14 = _memcmp(pppppppuVar16,plVar5,sVar15);
      if (iVar14 == 0) {
        if (uVar2 <= uVar3) goto LAB_100133448;
      }
      else if (-1 < iVar14) {
LAB_100133448:
        iVar14 = _memcmp(plVar5,pppppppuVar16,sVar15);
        if (iVar14 == 0) {
          if (uVar2 < uVar3) goto LAB_1001333f0;
        }
        else if (iVar14 < 0) {
LAB_1001333f0:
          plVar24 = plVar24 + 1;
          goto LAB_1001333f4;
        }
        bVar6 = false;
        goto joined_r0x000100133464;
      }
LAB_1001333f4:
      plVar24 = (long *)*plVar24;
    } while (plVar24 != (long *)0x0);
  }
  bVar6 = true;
joined_r0x000100133464:
  if ((uint)uVar22 >> 7 != 0) {
    operator_delete(local_f8);
  }
  if (bVar6) goto LAB_1001338c8;
  sVar15 = _strlen(param_3);
  if (0x7ffffffffffffff7 < sVar15) {
                    /* WARNING: Subroutine does not return */
    FUN_100134f2c(&local_f8);
  }
  if (sVar15 < 0x17) {
    local_e8 = (void *)CONCAT17((char)sVar15,(undefined7)local_e8);
    pppppppuVar16 = &local_f8;
    if (sVar15 != 0) goto LAB_1001334e0;
  }
  else {
    uVar22 = 0x19;
    if ((sVar15 | 7) != 0x17) {
      uVar22 = (sVar15 | 7) + 1;
    }
    pppppppuVar16 = operator_new(uVar22);
    local_e8 = (void *)(uVar22 | 0x8000000000000000);
    local_f8 = pppppppuVar16;
    local_f0 = sVar15;
LAB_1001334e0:
    _memcpy(pppppppuVar16,param_3,sVar15);
  }
  *(undefined1 *)((long)pppppppuVar16 + sVar15) = 0;
  plVar24 = (long *)FUN_10016bf7c(param_2,&local_f8);
  puVar17 = PTR_typeinfo_100b1c300;
  if ((long *)*plVar24 != (long *)0x0) {
    puVar17 = (undefined *)(**(code **)(*(long *)*plVar24 + 0x10))();
  }
  if (((char *)(*(ulong *)(puVar17 + 8) & 0x7fffffffffffffff) !=
       "NSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEE") &&
     (iVar14 = _strcmp((char *)(*(ulong *)(puVar17 + 8) & 0x7fffffffffffffff),
                       "NSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEE"),
     iVar14 != 0)) {
    local_118 = (int *******)0x0;
    std::bad_cast::bad_cast((bad_cast *)&local_118);
    local_118 = (int *******)&PTR__bad_cast_100b43d08;
    FUN_100138a40(&local_118);
                    /* WARNING: Does not return */
    pcVar13 = (code *)SoftwareBreakpoint(1,0x10013395c);
    (*pcVar13)();
  }
  lVar21 = *plVar24;
  if (*(char *)(lVar21 + 0x1f) < '\0') {
    FUN_100135b64(&local_c0,*(undefined8 *)(lVar21 + 8),*(undefined8 *)(lVar21 + 0x10));
  }
  else {
    uStack_b8 = *(ulong *)(lVar21 + 0x10);
    local_c0 = *(undefined8 ********)(lVar21 + 8);
    local_b0 = *(ulong *)(lVar21 + 0x18);
  }
  if ((long)local_e8 < 0) {
    operator_delete(local_f8);
  }
  uVar22 = uStack_b8;
  pppppppuVar16 = local_c0;
  if (-1 < (long)local_b0) {
    uVar22 = local_b0 >> 0x38;
    pppppppuVar16 = &local_c0;
  }
  FUN_10013797c(&local_d8,pppppppuVar16,uVar22,",");
  for (puVar1 = local_d8; puVar1 != local_d0; puVar1 = puVar1 + 2) {
    FUN_100137810(&local_f8,*puVar1,puVar1[1],"=");
    uVar22 = local_e0;
    pvVar7 = local_e8;
    if (local_e0 == 0) {
      FUN_10043cb54(&local_a0,&local_f8);
      pppppppiVar19 = local_a0;
      local_118 = (int *******)0x0;
      uStack_110 = 0;
      uStack_109 = 0;
      local_108 = 0;
      bStack_101 = 0;
      local_100 = local_a0;
      local_a0 = (int *******)0x0;
      puVar4 = (undefined8 *)param_1[1];
      if (puVar4 < (undefined8 *)param_1[2]) {
        puVar4[1] = 0;
        *puVar4 = 0;
        puVar4[3] = 0;
        puVar4[2] = 0;
        local_108 = 0;
        bStack_101 = 0;
        uStack_110 = 0;
        uStack_109 = 0;
        local_118 = (int *******)0x0;
        puVar4[3] = pppppppiVar19;
        local_100 = (int *******)0x0;
        param_1[1] = puVar4 + 4;
      }
      else {
        uVar20 = FUN_100137dac(param_1,&local_118);
        param_1[1] = uVar20;
        if ((local_100 != (int *******)0x0) &&
           (iVar14 = *(int *)local_100, *(int *)local_100 = iVar14 + -1, iVar14 + -1 == 0)) {
          FUN_100454b40();
        }
      }
      if ((char)bStack_101 < '\0') {
        operator_delete(local_118);
      }
      if ((local_a0 != (int *******)0x0) &&
         (iVar14 = *(int *)local_a0, *(int *)local_a0 = iVar14 + -1, iVar14 + -1 == 0)) {
        FUN_100454b40();
      }
    }
    else {
      if (0x7ffffffffffffff7 < local_e0) {
                    /* WARNING: Subroutine does not return */
        FUN_100134f2c(&local_130);
      }
      if (local_e0 < 0x17) {
        uStack_120 = CONCAT17((char)local_e0,(undefined7)uStack_120);
        ppuVar18 = &local_130;
      }
      else {
        uVar3 = 0x19;
        if ((local_e0 | 7) != 0x17) {
          uVar3 = (local_e0 | 7) + 1;
        }
        ppuVar18 = operator_new(uVar3);
        uStack_120 = uVar3 | 0x8000000000000000;
        local_128 = uVar22;
        local_130 = (undefined1 *)ppuVar18;
      }
      _memmove(ppuVar18,pvVar7,uVar22);
      *(undefined1 *)((long)ppuVar18 + uVar22) = 0;
      uVar22 = (ulong)uStack_120._7_1_;
      if ((long)uVar22 < 0) {
        if (0x7ffffffffffffff7 < local_128) {
                    /* WARNING: Subroutine does not return */
          FUN_100134f2c(&local_a0);
        }
        uVar22 = local_128;
        ppuVar18 = (undefined1 **)local_130;
        ppuVar23 = (undefined1 **)local_130;
        if (local_128 < 0x17) goto LAB_1001336cc;
LAB_1001336fc:
        uVar3 = 0x19;
        if ((uVar22 | 7) != 0x17) {
          uVar3 = (uVar22 | 7) + 1;
        }
        pppppppiVar19 = operator_new(uVar3);
        local_89 = (byte)(uVar3 >> 0x38) | 0x80;
        local_98 = (undefined7)uVar22;
        uStack_91 = (undefined1)(uVar22 >> 0x38);
        uStack_90 = (undefined7)uVar3;
        local_a0 = pppppppiVar19;
LAB_100133724:
        _memmove(pppppppiVar19,ppuVar18,uVar22);
      }
      else {
        ppuVar18 = &local_130;
        ppuVar23 = &local_130;
        if (0x16 < uVar22) goto LAB_1001336fc;
LAB_1001336cc:
        local_89 = (byte)uVar22;
        pppppppiVar19 = (int *******)&local_a0;
        ppuVar18 = ppuVar23;
        if (uVar22 != 0) goto LAB_100133724;
      }
      *(undefined1 *)((long)pppppppiVar19 + uVar22) = 0;
      bVar9 = local_89;
      pppppppiVar19 = local_a0;
      local_88 = local_98;
      uStack_81 = uStack_91;
      uStack_80 = uStack_90;
      FUN_10043cb54(&local_a0,&local_f8);
      uVar12 = uStack_80;
      uVar11 = uStack_81;
      uVar10 = local_88;
      pppppppiVar8 = local_a0;
      local_118 = pppppppiVar19;
      uStack_110 = local_88;
      uStack_109 = uStack_81;
      local_108 = uStack_80;
      bStack_101 = bVar9;
      local_88 = 0;
      uStack_81 = 0;
      uStack_80 = 0;
      local_100 = local_a0;
      local_a0 = (int *******)0x0;
      puVar4 = (undefined8 *)param_1[1];
      if (puVar4 < (undefined8 *)param_1[2]) {
        puVar4[2] = CONCAT17(bVar9,uVar12);
        puVar4[3] = 0;
        puVar4[1] = CONCAT17(uVar11,uVar10);
        *puVar4 = pppppppiVar19;
        local_118 = (int *******)0x0;
        uStack_110 = 0;
        uStack_109 = 0;
        puVar4[3] = pppppppiVar8;
        local_108 = 0;
        bStack_101 = 0;
        local_100 = (int *******)0x0;
        param_1[1] = puVar4 + 4;
      }
      else {
        uVar20 = FUN_100137dac(param_1,&local_118);
        param_1[1] = uVar20;
        if ((local_100 != (int *******)0x0) &&
           (iVar14 = *(int *)local_100, *(int *)local_100 = iVar14 + -1, iVar14 + -1 == 0)) {
          FUN_100454b40();
        }
      }
      if ((char)bStack_101 < '\0') {
        operator_delete(local_118);
      }
      if ((local_a0 != (int *******)0x0) &&
         (iVar14 = *(int *)local_a0, *(int *)local_a0 = iVar14 + -1, iVar14 + -1 == 0)) {
        FUN_100454b40();
      }
      if ((long)uStack_120 < 0) {
        operator_delete(local_130);
      }
    }
  }
  if (local_d8 != (undefined8 *)0x0) {
    operator_delete(local_d8);
  }
  if ((long)local_b0 < 0) {
    operator_delete(local_c0);
  }
LAB_1001338c8:
  if (*(long *)PTR____stack_chk_guard_100b1c378 != local_78) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}

