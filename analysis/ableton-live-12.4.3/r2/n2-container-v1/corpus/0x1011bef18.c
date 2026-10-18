
void FUN_1011bef18(long param_1)

{
  undefined8 *puVar1;
  long lVar2;
  long lVar3;
  long lVar4;
  byte bVar5;
  code *pcVar6;
  void *pvVar7;
  uint uVar8;
  long lVar9;
  undefined8 *puVar10;
  ulong uVar11;
  long lVar12;
  byte *pbVar13;
  ulong uVar14;
  ulong uVar15;
  long *plVar16;
  int iVar17;
  byte *pbVar18;
  void *pvVar19;
  size_t sVar20;
  void *pvVar21;
  ulong uVar22;
  size_t sVar23;
  undefined8 *puVar24;
  int iVar25;
  ulong uVar26;
  void *local_498;
  undefined8 *local_488;
  long lStack_480;
  undefined8 local_478;
  undefined1 auStack_458 [60];
  undefined2 local_41c;
  long local_70;
  
  local_70 = *(long *)PTR____stack_chk_guard_1064f8818;
  if ((DAT_106f4de68 & 1) == 0) {
    FUN_105410224();
  }
  lVar12 = param_1 * 0x40;
  plVar16 = (long *)(&DAT_106f4ce68 + lVar12);
  pvVar19 = (void *)*plVar16;
  if (pvVar19 == *(void **)(&DAT_106f4ce70 + lVar12)) {
    if ((ulong)(*(long *)(&DAT_106f4ce78 + lVar12) - (long)pvVar19) < 800) {
      pvVar7 = operator_new(800);
      *plVar16 = (long)pvVar7;
      *(void **)(&DAT_106f4ce70 + lVar12) = pvVar7;
      *(long *)(&DAT_106f4ce78 + lVar12) = (long)pvVar7 + 800;
      if (pvVar19 != (void *)0x0) {
        operator_delete(pvVar19);
      }
    }
    iVar25 = 0;
    iVar17 = (int)param_1;
    if (iVar17 != 0) {
      iVar25 = 0x1000 / iVar17;
    }
    if (0xfe < iVar25) {
      iVar25 = 0xff;
    }
    *(int *)(&DAT_106f4ce84 + lVar12) = iVar25;
    *(int *)(&DAT_106f4ce88 + lVar12) = iVar25 * iVar17;
    *(undefined8 *)(&DAT_106f4ce98 + lVar12) = 0xffffffffffffffff;
    *(long *)(&DAT_106f4cea0 + lVar12) = param_1;
    pbVar18 = *(byte **)(&DAT_106f4ce90 + lVar12);
  }
  else {
    pbVar18 = *(byte **)(&DAT_106f4ce90 + lVar12);
  }
  if (pbVar18 != (byte *)0x0) {
    bVar5 = pbVar18[1];
    if (bVar5 == 0) {
      FUN_1011a612c(L"Memory corrupt: ",&local_478,0x20);
      FUN_1011a612c(L"Heap corrupt on allocation (1)",auStack_458,0x3c);
      local_41c = 0;
      if ((short)local_478 == 0) {
        lStack_480 = 0;
      }
      else {
        lVar12 = 0;
        do {
          lStack_480 = lVar12 + 1;
          lVar9 = lVar12 * 2;
          lVar12 = lStack_480;
        } while (*(short *)((long)&local_478 + lVar9 + 2) != 0);
      }
      local_488 = &local_478;
      FUN_1011b5254(&local_488);
LAB_1011bf560:
                    /* WARNING: Does not return */
      pcVar6 = (code *)SoftwareBreakpoint(1,0x1011bf564);
      (*pcVar6)();
    }
    iVar25 = *(int *)(pbVar18 + 0x18);
    *(int *)(&DAT_106f4ce98 + lVar12) = iVar25;
    if (*(byte **)(*plVar16 + (long)iVar25 * 8) != pbVar18) {
      FUN_1011a612c(L"Memory corrupt: ",&local_478,0x20);
      FUN_1011a612c(L"Heap corrupt on allocation (2)",auStack_458,0x3c);
      local_41c = 0;
      if ((short)local_478 == 0) {
        lStack_480 = 0;
      }
      else {
        lVar12 = 0;
        do {
          lStack_480 = lVar12 + 1;
          lVar9 = lVar12 * 2;
          lVar12 = lStack_480;
        } while (*(short *)((long)&local_478 + lVar9 + 2) != 0);
      }
      local_488 = &local_478;
      FUN_1011b5254(&local_488);
      goto LAB_1011bf560;
    }
    if (*(uint *)(&DAT_106f4ce84 + lVar12) == (uint)bVar5) {
      *(int *)(&DAT_106f4ce80 + lVar12) = *(int *)(&DAT_106f4ce80 + lVar12) + -1;
    }
    else if (bVar5 == 1) {
      if (*(byte **)(pbVar18 + 8) == pbVar18) {
        *(undefined8 *)(&DAT_106f4ce90 + lVar12) = 0;
      }
      else {
        lVar9 = *(long *)(pbVar18 + 0x10);
        *(byte **)(lVar9 + 8) = *(byte **)(pbVar18 + 8);
        *(long *)(*(long *)(pbVar18 + 8) + 0x10) = lVar9;
        *(long *)(&DAT_106f4ce90 + lVar12) = lVar9;
      }
    }
    goto LAB_1011bf3d8;
  }
  if (*(long *)(&DAT_106f4ce70 + lVar12) == *(long *)(&DAT_106f4ce78 + lVar12)) {
    pvVar19 = (void *)*plVar16;
    sVar20 = *(long *)(&DAT_106f4ce70 + lVar12) - (long)pvVar19;
    uVar22 = (long)sVar20 >> 3;
    uVar11 = uVar22 + (uVar22 >> 1);
    uVar26 = uVar22 + 100;
    if (uVar22 + 100 <= uVar11) {
      uVar26 = uVar11;
    }
    if (uVar26 <= uVar22) goto LAB_1011bf08c;
    if (uVar26 >> 0x3d == 0) {
      pvVar7 = operator_new(uVar26 * 8);
      pvVar21 = (void *)((long)pvVar7 + sVar20 + uVar22 * -8);
      _memcpy(pvVar21,pvVar19,sVar20);
      *plVar16 = (long)pvVar21;
      *(size_t *)(&DAT_106f4ce70 + lVar12) = (long)pvVar7 + sVar20;
      *(void **)(&DAT_106f4ce78 + lVar12) = (void *)((long)pvVar7 + uVar26 * 8);
      if (pvVar19 != (void *)0x0) {
        operator_delete(pvVar19);
      }
      goto LAB_1011bf08c;
    }
  }
  else {
LAB_1011bf08c:
    pbVar18 = _malloc((long)*(int *)(&DAT_106f4ce88 + lVar12) + 0x20);
    if (pbVar18 == (byte *)0x0) {
                    /* WARNING: Subroutine does not return */
      FUN_1011b50a8();
    }
    bVar5 = (&DAT_106f4ce84)[lVar12];
    *pbVar18 = 0;
    pbVar18[1] = bVar5;
    if (bVar5 != 0) {
      uVar8 = 0;
      pbVar13 = pbVar18 + 0x20;
      do {
        uVar8 = uVar8 + 1;
        *pbVar13 = (byte)uVar8;
        pbVar13 = pbVar13 + param_1;
      } while (uVar8 != bVar5);
    }
    local_478 = pbVar18;
    lVar9 = *plVar16;
    puVar24 = *(undefined8 **)(&DAT_106f4ce70 + lVar12);
    uVar11 = (long)puVar24 - lVar9 >> 3;
    if ((long)puVar24 - lVar9 == 0) {
      uVar26 = 0;
    }
    else {
      uVar26 = 0;
      uVar22 = uVar11;
      do {
        uVar14 = uVar22 >> 1;
        uVar15 = uVar22 + ~uVar14;
        uVar22 = uVar14;
        if (*(byte **)(lVar9 + (uVar14 + uVar26) * 8) < pbVar18) {
          uVar26 = uVar14 + uVar26 + 1;
          uVar22 = uVar15;
        }
      } while (uVar22 != 0);
    }
    iVar25 = (int)uVar26;
    *(int *)(pbVar18 + 0x18) = iVar25;
    uVar22 = (ulong)iVar25;
    uVar26 = -(uVar26 >> 0x1f & 1) & 0xfffffff800000000 | (uVar26 & 0xffffffff) << 3;
    puVar1 = (undefined8 *)(lVar9 + uVar26);
    if (puVar24 < *(undefined8 **)(&DAT_106f4ce78 + lVar12)) {
      if (puVar1 == puVar24) {
        *puVar24 = pbVar18;
        *(undefined8 **)(&DAT_106f4ce70 + lVar12) = puVar24 + 1;
        lVar9 = *plVar16;
        uVar11 = *(long *)(&DAT_106f4ce70 + lVar12) - lVar9 >> 3;
        if (uVar22 + 1 < uVar11) goto LAB_1011bf318;
      }
      else {
        if (puVar24 + -1 < puVar24) {
          puVar10 = puVar24 + 1;
          *puVar24 = puVar24[-1];
          *(undefined8 **)(&DAT_106f4ce70 + lVar12) = puVar10;
        }
        else {
          *(undefined8 **)(&DAT_106f4ce70 + lVar12) = puVar24;
          puVar10 = puVar24;
        }
        if (puVar24 != puVar1 + 1) {
          sVar20 = (long)puVar24 - (long)(puVar1 + 1);
          _memmove((void *)((long)puVar24 - sVar20),puVar1,sVar20);
          puVar10 = *(undefined8 **)(&DAT_106f4ce70 + lVar12);
        }
        lVar9 = 8;
        if (puVar10 <= &local_478 || &local_478 < puVar1) {
          lVar9 = 0;
        }
        *puVar1 = *(undefined8 *)((long)&local_478 + lVar9);
        lVar9 = *plVar16;
        uVar11 = *(long *)(&DAT_106f4ce70 + lVar12) - lVar9 >> 3;
        if (uVar22 + 1 < uVar11) {
LAB_1011bf318:
          uVar26 = uVar22 + 1;
          uVar15 = uVar11 + ~uVar22;
          if (3 < uVar15) {
            uVar14 = uVar15 & 0xfffffffffffffffc;
            uVar26 = uVar26 + uVar14;
            plVar16 = (long *)(lVar9 + uVar22 * 8 + 0x10);
            uVar22 = uVar14;
            iVar17 = iVar25;
            do {
              lVar3 = *plVar16;
              lVar2 = plVar16[1];
              lVar4 = plVar16[2];
              *(int *)(plVar16[-1] + 0x18) = iVar17 + 1;
              *(int *)(lVar3 + 0x18) = iVar17 + 2;
              *(int *)(lVar2 + 0x18) = iVar17 + 3;
              *(int *)(lVar4 + 0x18) = iVar17 + 4;
              plVar16 = plVar16 + 4;
              uVar22 = uVar22 - 4;
              iVar17 = iVar17 + 4;
            } while (uVar22 != 0);
            if (uVar15 == uVar14) goto LAB_1011bf390;
          }
          do {
            *(int *)(*(long *)(lVar9 + uVar26 * 8) + 0x18) = (int)uVar26;
            uVar26 = uVar26 + 1;
          } while (uVar11 != uVar26);
        }
      }
LAB_1011bf390:
      *(int *)(&DAT_106f4ce98 + lVar12) = iVar25;
      if (iVar25 <= *(int *)(&DAT_106f4ce9c + lVar12)) {
        *(int *)(&DAT_106f4ce9c + lVar12) = *(int *)(&DAT_106f4ce9c + lVar12) + 1;
      }
      lVar9 = *(long *)(&DAT_106f4ce90 + lVar12);
      if (lVar9 == 0) {
        *(byte **)(pbVar18 + 8) = pbVar18;
        *(byte **)(pbVar18 + 0x10) = pbVar18;
        *(byte **)(&DAT_106f4ce90 + lVar12) = pbVar18;
      }
      else {
        *(long *)(pbVar18 + 0x10) = lVar9;
        lVar12 = *(long *)(lVar9 + 8);
        *(long *)(pbVar18 + 8) = lVar12;
        *(byte **)(lVar12 + 0x10) = pbVar18;
        *(byte **)(lVar9 + 8) = pbVar18;
      }
LAB_1011bf3d8:
      *pbVar18 = pbVar18[(ulong)*pbVar18 * param_1 + 0x20];
      pbVar18[1] = pbVar18[1] - 1;
      if (*(long *)PTR____stack_chk_guard_1064f8818 == local_70) {
        return;
      }
                    /* WARNING: Subroutine does not return */
      ___stack_chk_fail();
    }
    uVar11 = uVar11 + 1;
    if (uVar11 >> 0x3d == 0) {
      uVar14 = (long)*(undefined8 **)(&DAT_106f4ce78 + lVar12) - lVar9;
      uVar15 = (long)uVar14 >> 2;
      if (uVar15 <= uVar11) {
        uVar15 = uVar11;
      }
      if (0x7ffffffffffffff7 < uVar14) {
        uVar15 = 0x1fffffffffffffff;
      }
      if (uVar15 == 0) {
        pvVar19 = (void *)0x0;
        puVar10 = (undefined8 *)(uVar22 << 3);
        local_498 = (void *)0x0;
        if (uVar22 == 0) {
LAB_1011bf1e8:
          if (iVar25 < 1) {
            uVar11 = uVar22 << 1;
            if (iVar25 == 0) {
              uVar11 = 1;
            }
            local_498 = operator_new(uVar11 << 3);
            puVar10 = (undefined8 *)((long)local_498 + (uVar11 >> 2) * 8);
            local_498 = (void *)((long)local_498 + uVar11 * 8);
            if (pvVar19 != (void *)0x0) {
              operator_delete(pvVar19);
              puVar24 = *(undefined8 **)(&DAT_106f4ce70 + lVar12);
            }
          }
          else {
            puVar10 = (undefined8 *)((long)puVar10 - (uVar22 * 4 + 4 & 0xfffffffffffffff8));
          }
        }
      }
      else {
        if (uVar15 >> 0x3d != 0) goto LAB_1011bf500;
        pvVar19 = operator_new(uVar15 << 3);
        puVar10 = (undefined8 *)((long)pvVar19 + uVar22 * 8);
        local_498 = (void *)((long)pvVar19 + uVar15 * 8);
        if (uVar15 == uVar22) goto LAB_1011bf1e8;
      }
      *puVar10 = pbVar18;
      lVar9 = uVar26 + lVar9;
      sVar23 = (long)puVar24 - lVar9;
      _memcpy(puVar10 + 1,puVar1,sVar23);
      *(undefined8 **)(&DAT_106f4ce70 + lVar12) = puVar1;
      sVar20 = lVar9 - *plVar16;
      pvVar7 = (void *)((long)puVar10 - sVar20);
      _memcpy(pvVar7,(void *)*plVar16,sVar20);
      pvVar19 = (void *)*plVar16;
      *plVar16 = (long)pvVar7;
      *(size_t *)(&DAT_106f4ce70 + lVar12) = (long)(puVar10 + 1) + sVar23;
      *(void **)(&DAT_106f4ce78 + lVar12) = local_498;
      if (pvVar19 != (void *)0x0) {
        operator_delete(pvVar19);
      }
      lVar9 = *plVar16;
      uVar11 = *(long *)(&DAT_106f4ce70 + lVar12) - lVar9 >> 3;
      if (uVar22 + 1 < uVar11) goto LAB_1011bf318;
      goto LAB_1011bf390;
    }
  }
  FUN_1011bfcc4();
LAB_1011bf500:
                    /* WARNING: Subroutine does not return */
  FUN_10024a858();
}

