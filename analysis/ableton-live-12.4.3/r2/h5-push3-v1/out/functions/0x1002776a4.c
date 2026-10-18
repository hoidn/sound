// 0x1002776a4 FUN_1002776a4 state=exported-with-warnings role=UsbDisplay::getNextFrameBuffer
// source chunk chunk-00108.jsonl; code_sha256=e472331cde6c90af567b37bd2433fe607256735f2266930f7da5754ac92b1dfa

long FUN_1002776a4(void *param_1)

{
  ulong uVar1;
  ulong uVar2;
  uint uVar3;
  void **ppvVar4;
  uint uVar5;
  ulong uVar6;
  int iVar7;
  long lVar8;
  long lVar9;
  void *pvVar10;
  ulong uVar11;
  ulong uVar12;
  ulong uVar13;
  void *pvVar14;
  undefined8 uVar15;
  long lVar16;
  long lVar17;
  double dVar18;
  double dVar19;
  void **local_b0;
  uint local_a8;
  undefined8 *local_a0;
  long *local_98;
  long local_90;
  undefined8 local_88;
  void *local_80;
  void *local_78;
  void *local_68;
  
  FUN_10066461c("UsbDisplay","getNextFrameBuffer");
  if ((*PTR_sLog_101b8cac8 & 1) == 0) {
    FUN_1014a8838();
  }
  uVar15 = *(undefined8 *)PTR_sLog_101ba0f90;
  local_88 = uVar15;
  lVar8 = _os_signpost_id_generate(uVar15);
  local_90 = lVar8;
  if ((lVar8 - 1U < 0xfffffffffffffffe) && (iVar7 = _os_signpost_enabled(uVar15), iVar7 != 0)) {
    local_80 = (void *)((ulong)local_80 & 0xffffffffffff0000);
    __os_signpost_emit_with_name_impl
              (0x100000000,uVar15,1,lVar8,"getNextFrameBuffer","",&local_80,2);
  }
  local_a0 = &local_88;
  local_98 = &local_90;
  lVar9 = std::chrono::steady_clock::now();
  lVar8 = lVar9 - *(long *)((long)param_1 + 0x160);
  if (lVar8 == 0) {
    uVar12 = 0xffffffff;
    lVar8 = 0;
  }
  else {
    dVar18 = 1.0;
    if ((double)lVar8 / 1000000000.0 <= 1.0) {
      dVar18 = (double)lVar8 / 1000000000.0;
    }
    dVar18 = *(double *)((long)param_1 + 0x168) + *(double *)((long)param_1 + 0x168) * -0.2 +
             dVar18 * 0.2;
    *(long *)((long)param_1 + 0x160) = lVar9;
    dVar19 = *(double *)((long)param_1 + 0x170) + *(double *)((long)param_1 + 0x170) * -0.1 +
             dVar18 * 0.1;
    *(double *)((long)param_1 + 0x168) = dVar18;
    *(double *)((long)param_1 + 0x170) = dVar19;
    lVar8 = lVar8 / 1000000;
    uVar12 = (ulong)(uint)(int)(1.0 / dVar19);
  }
  uVar3 = *(uint *)((long)param_1 + 0x230);
  *(ulong *)((long)param_1 + (ulong)uVar3 * 0x10 + 0x238) = uVar12;
  *(long *)((long)param_1 + (ulong)uVar3 * 0x10 + 0x240) = lVar8;
  LOAcquire();
  uVar5 = *(uint *)((long)param_1 + 0x228U);
  *(uint *)((long)param_1 + 0x228U) = uVar3 << 0x10 | 1;
  LORelease();
  *(uint *)((long)param_1 + 0x230) = uVar5 >> 0x10;
  uVar2 = *(ulong *)((long)param_1 + 0xe8);
  lVar8 = *(long *)((long)param_1 + 0xf0);
  uVar6 = *(ulong *)((long)param_1 + 0xa0);
  uVar11 = *(ulong *)((long)param_1 + 0xe0);
  uVar12 = uVar2;
  if (uVar11 <= uVar6) {
    uVar12 = 0;
  }
  lVar9 = uVar12 + (uVar6 - uVar11);
  if (lVar9 != 0) {
    uVar1 = uVar12 + uVar6;
    uVar13 = uVar1 - uVar2;
    if (uVar1 < uVar2 || uVar13 == 0) {
      lVar8 = lVar8 + uVar11 * 0x30;
      lVar9 = uVar11 * -0x30 + uVar1 * 0x30;
      do {
        if (*(uint *)(lVar8 + 0x28) == 0xffffffff) goto LAB_100277c3c;
        local_b0 = &local_80;
        local_80 = param_1;
        local_78 = param_1;
        (*(code *)(&PTR_FUN_101bd6588)[*(uint *)(lVar8 + 0x28)])(&local_b0,lVar8);
        if (*(uint *)(lVar8 + 0x28) != 0xffffffff) {
          (*(code *)(&PTR_FUN_101bd61d8)[*(uint *)(lVar8 + 0x28)])(&local_80,lVar8);
        }
        *(undefined4 *)(lVar8 + 0x28) = 0xffffffff;
        lVar8 = lVar8 + 0x30;
        lVar9 = lVar9 + -0x30;
      } while (lVar9 != 0);
      uVar13 = 0;
      if (uVar1 != uVar2) {
        uVar13 = uVar1;
      }
    }
    else {
      if (uVar11 - uVar2 != 0) {
        lVar16 = lVar8 + uVar11 * 0x30;
        lVar17 = uVar11 * -0x30 + uVar2 * 0x30;
        do {
          if (*(uint *)(lVar16 + 0x28) == 0xffffffff) goto LAB_100277c3c;
          local_b0 = &local_80;
          local_80 = param_1;
          local_78 = param_1;
          (*(code *)(&PTR_FUN_101bd6588)[*(uint *)(lVar16 + 0x28)])(&local_b0,lVar16);
          if (*(uint *)(lVar16 + 0x28) != 0xffffffff) {
            (*(code *)(&PTR_FUN_101bd61d8)[*(uint *)(lVar16 + 0x28)])(&local_80,lVar16);
          }
          *(undefined4 *)(lVar16 + 0x28) = 0xffffffff;
          lVar16 = lVar16 + 0x30;
          lVar17 = lVar17 + -0x30;
        } while (lVar17 != 0);
      }
      if (lVar8 + (uVar11 - uVar2) * 0x30 + lVar9 * 0x30 != lVar8) {
        lVar9 = (uVar12 + uVar6) * 0x30 + uVar2 * -0x30;
        do {
          if (*(uint *)(lVar8 + 0x28) == 0xffffffff) {
LAB_100277c3c:
            local_80 = param_1;
            local_78 = param_1;
                    /* WARNING: Subroutine does not return */
            FUN_100180824();
          }
          local_b0 = &local_80;
          local_80 = param_1;
          local_78 = param_1;
          (*(code *)(&PTR_FUN_101bd6588)[*(uint *)(lVar8 + 0x28)])(&local_b0,lVar8);
          if (*(uint *)(lVar8 + 0x28) != 0xffffffff) {
            (*(code *)(&PTR_FUN_101bd61d8)[*(uint *)(lVar8 + 0x28)])(&local_80,lVar8);
          }
          *(undefined4 *)(lVar8 + 0x28) = 0xffffffff;
          lVar8 = lVar8 + 0x30;
          lVar9 = lVar9 + -0x30;
        } while (lVar9 != 0);
      }
    }
    *(ulong *)((long)param_1 + 0xe0) = uVar13;
  }
  if ((*(byte *)((long)param_1 + 0x17d) & 1) == 0) {
    (**(code **)(**(long **)((long)param_1 + 0x40) + 0x28))
              (&local_80,*(long **)((long)param_1 + 0x40),1800000000);
    pvVar10 = local_80;
    if ((char)local_78 != '\x01') goto LAB_100277b20;
    if (local_80 == (void *)0x0) {
LAB_100277bec:
      lVar9 = 0;
      lVar8 = *local_98;
      goto joined_r0x000100277b68;
    }
    pvVar14 = *(void **)((long)param_1 + 0x158);
    if (pvVar14 == (void *)0x0) {
      local_80 = (void *)0x0;
      *(void **)((long)param_1 + 0x158) = pvVar10;
    }
    else {
      *(undefined8 *)((long)param_1 + 0x158) = 0;
      local_68 = pvVar14;
      (**(code **)(**(long **)((long)param_1 + 0x60) + 0x20))
                (&local_b0,*(long **)((long)param_1 + 0x60),&local_68);
      pvVar10 = local_68;
      local_68 = (void *)0x0;
      if (pvVar10 != (void *)0x0) {
        operator_delete(pvVar10);
      }
      pvVar10 = local_80;
      ppvVar4 = local_b0;
      if (local_a8 != 0) {
        if (local_a8 != 1) {
                    /* WARNING: Subroutine does not return */
          FUN_100180824();
        }
        local_b0 = (void **)0x0;
        pvVar10 = *(void **)((long)param_1 + 0x158);
        *(void ***)((long)param_1 + 0x158) = ppvVar4;
        if (pvVar10 == (void *)0x0) {
          local_a8 = 1;
LAB_100277bbc:
          (*(code *)(&PTR_FUN_101bd61c8)[local_a8])(&local_68,&local_b0);
        }
        else {
          operator_delete(pvVar10);
          if (local_a8 != 0xffffffff) goto LAB_100277bbc;
        }
        pvVar10 = local_80;
        if ((((ulong)local_78 & 1) != 0) && (local_80 = (void *)0x0, pvVar10 != (void *)0x0)) {
          operator_delete(pvVar10);
        }
        goto LAB_100277bec;
      }
      pvVar14 = *(void **)((long)param_1 + 0x158);
      local_80 = (void *)0x0;
      *(void **)((long)param_1 + 0x158) = pvVar10;
      if (pvVar14 != (void *)0x0) {
        operator_delete(pvVar14);
      }
    }
LAB_100277b20:
    pvVar10 = local_80;
    if (((char)local_78 == '\x01') && (local_80 = (void *)0x0, pvVar10 != (void *)0x0)) {
      operator_delete(pvVar10);
    }
    (**(code **)(**(long **)((long)param_1 + 0xf8) + 0x18))();
    lVar9 = *(long *)((long)param_1 + 0x158);
    if (lVar9 == 0) goto LAB_100277b54;
  }
  else {
LAB_100277b54:
    lVar9 = *(long *)((long)param_1 + 0x138);
  }
  lVar8 = *local_98;
joined_r0x000100277b68:
  if (lVar8 - 1U < 0xfffffffffffffffe) {
    uVar15 = *local_a0;
    iVar7 = _os_signpost_enabled(uVar15);
    if (iVar7 != 0) {
      local_80 = (void *)((ulong)local_80 & 0xffffffffffff0000);
      __os_signpost_emit_with_name_impl
                (0x100000000,uVar15,2,lVar8,"getNextFrameBuffer","",&local_80,2);
    }
  }
  FUN_100664a3c("UsbDisplay","getNextFrameBuffer");
  return lVar9;
}

