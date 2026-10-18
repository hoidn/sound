// 0x100133f90 FUN_100133f90 state=exported-with-warnings body_bytes=4516 warnings=9 chunk=chunk-00052.jsonl

/* WARNING: Removing unreachable block (ram,0x000100134f6c) */
/* WARNING: Removing unreachable block (ram,0x000100134dec) */
/* WARNING: Removing unreachable block (ram,0x000100134930) */
/* WARNING: Removing unreachable block (ram,0x000100134294) */
/* WARNING: Removing unreachable block (ram,0x000100134714) */
/* WARNING: Removing unreachable block (ram,0x000100134c44) */
/* WARNING: Removing unreachable block (ram,0x000100134f24) */
/* WARNING: Removing unreachable block (ram,0x00010013504c) */

void FUN_100133f90(undefined8 param_1,long param_2)

{
  ushort uVar1;
  undefined8 *puVar2;
  undefined8 *puVar3;
  void *pvVar4;
  char cVar5;
  int iVar6;
  undefined4 uVar7;
  uint uVar8;
  ulong uVar9;
  undefined8 uVar10;
  long *plVar11;
  undefined8 *puVar12;
  undefined8 *puVar13;
  int *piVar14;
  undefined8 **ppuVar15;
  undefined8 *puVar16;
  void *pvVar17;
  undefined8 *local_5e0;
  undefined8 *local_5d8;
  undefined8 **local_5c8;
  undefined8 **local_5c0;
  undefined8 **local_5b8;
  undefined8 *local_5b0;
  undefined8 *local_5a8;
  undefined1 *local_598;
  long **local_590;
  long local_588;
  long *local_580;
  undefined8 uStack_578;
  undefined8 local_570;
  undefined8 local_568;
  undefined8 uStack_560;
  undefined1 *local_558;
  long *local_550;
  undefined8 *local_548;
  undefined8 *puStack_540;
  undefined1 local_538 [184];
  long local_480;
  undefined8 uStack_478;
  long local_470;
  undefined8 uStack_468;
  void *local_460;
  undefined8 uStack_458;
  void *local_450;
  undefined8 uStack_448;
  undefined4 local_440;
  undefined8 *local_438;
  undefined8 *local_430;
  undefined8 *puStack_428;
  undefined8 *local_418;
  undefined8 *puStack_410;
  long *local_400;
  long *plStack_3f8;
  undefined7 local_3f0;
  char cStack_3e9;
  int *local_3e8;
  undefined8 local_3e0;
  undefined4 local_3d8;
  undefined8 *local_3d0;
  undefined8 *local_3c8;
  long *local_3b8;
  long *plStack_3b0;
  undefined7 local_3a8;
  char cStack_3a1;
  int *local_3a0;
  undefined8 local_398;
  undefined4 local_390;
  undefined8 *local_388;
  undefined8 *local_380;
  undefined8 *local_370;
  undefined8 *local_368;
  undefined8 *local_358;
  undefined8 *local_350;
  long *local_340;
  long *plStack_338;
  undefined7 local_330;
  char cStack_329;
  int *local_328;
  undefined8 local_320;
  undefined4 local_318;
  long *local_310;
  long *plStack_308;
  undefined7 local_300;
  char cStack_2f9;
  int *local_2f8;
  undefined8 local_2f0;
  undefined4 local_2e8;
  long *local_2e0;
  long *plStack_2d8;
  undefined8 local_2d0;
  int *local_2c8;
  undefined8 local_2c0;
  undefined4 local_2b8;
  undefined8 *local_2b0;
  undefined8 *local_2a8;
  undefined7 local_2a0;
  char cStack_299;
  long local_230;
  long lStack_228;
  long lStack_220;
  long lStack_218;
  long local_210;
  long local_208;
  long local_200;
  long local_1f8;
  long local_1f0;
  byte local_1e0;
  uint local_1d8;
  long local_1a8;
  byte local_190;
  long local_118;
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_100d60390;
  FUN_1001534d8(&local_430);
  uVar9 = FUN_100153650(param_1,&local_430);
  if ((uVar9 & 1) != 0) {
    FUN_10014dc18(param_2 + 0x58);
    cStack_299 = '\a';
    local_2b0 = (undefined8 *)&DAT_72656e6e616353;
    uVar10 = std::chrono::system_clock::now();
    FUN_10073cd34(local_538,1,&local_2b0,uVar10);
    if (cStack_299 < '\0') {
      operator_delete(local_2b0);
    }
    iVar6 = FUN_1007396c0(local_538);
    if (iVar6 != 0) {
      FUN_100736880(local_538,"Entering command mode");
    }
    thunk_FUN_1007363ec(local_538);
    FUN_10014ddfc(param_2);
    FUN_10014e198(param_2);
    FUN_1001cfb20(&local_2b0);
    FUN_100211cc4(&local_2b0);
    FUN_100154a2c(&local_2a8,CONCAT17(cStack_299,local_2a0));
    plVar11 = (long *)FUN_10027aef0();
    (**(code **)(*plVar11 + 0x38))
              (plVar11,param_2,6,*(undefined4 *)(param_2 + 0x70),*(undefined4 *)(param_2 + 0x74));
    puVar12 = (undefined8 *)FUN_1002f80e4(0x98);
    puVar12[0x12] = 0;
    puVar12[0xf] = 0;
    puVar12[0xe] = 0;
    puVar12[0x11] = 0;
    puVar12[0x10] = 0;
    puVar12[0xb] = 0;
    puVar12[10] = 0;
    puVar12[0xd] = 0;
    puVar12[0xc] = 0;
    puVar12[7] = 0;
    puVar12[6] = 0;
    puVar12[9] = 0;
    puVar12[8] = 0;
    puVar12[3] = 0;
    puVar12[2] = 0;
    puVar12[5] = 0;
    puVar12[4] = 0;
    puVar12[1] = 0;
    *puVar12 = 0;
    FUN_1002abda0();
    puVar16 = puVar12 + 3;
    *puVar16 = &PTR_FUN_100db9540;
    *puVar12 = &PTR_thunk_FUN_100695958_100db94d0;
    puVar12[6] = 0;
    puVar12[7] = 0;
    puVar12[5] = 0;
    puVar12[4] = puVar12 + 5;
    puVar12[8] = 0;
    puVar12[9] = 0;
    puVar12[0xc] = 0;
    puVar12[0xb] = 0;
    puVar12[10] = puVar12 + 0xb;
    *(undefined1 *)(puVar12 + 0xd) = 0;
    puVar12[0xf] = 0;
    puVar12[0xe] = 0;
    puVar12[0x11] = 0;
    puVar12[0x10] = 0;
    puVar12[0x12] = 0;
    *(int *)(puVar12 + 1) = *(int *)(puVar12 + 1) + 1;
    local_438 = puVar12;
    plVar11 = (long *)FUN_10027aef0();
    *(int *)(puVar12 + 1) = *(int *)(puVar12 + 1) + 1;
    local_2b0 = puVar12;
    local_2a8 = puVar16;
    (**(code **)(*plVar11 + 0x120))(plVar11,&local_2b0);
    if ((local_2b0 != (undefined8 *)0x0) &&
       (iVar6 = *(int *)(local_2b0 + 1), *(int *)(local_2b0 + 1) = iVar6 + -1, iVar6 + -1 == 0)) {
      FUN_1002abea8();
    }
    puVar13 = (undefined8 *)FUN_1002f80e4(0x38);
    thunk_FUN_1005284c4(puVar13,param_2 + 0x18,1);
    if (puVar13 != (undefined8 *)0x0) {
      *(int *)(puVar13 + 1) = *(int *)(puVar13 + 1) + 1;
    }
    local_2b0 = puVar13;
    FUN_100528d40(&local_2b0);
    if ((local_2b0 != (undefined8 *)0x0) &&
       (iVar6 = *(int *)(local_2b0 + 1), *(int *)(local_2b0 + 1) = iVar6 + -1, iVar6 + -1 == 0)) {
      FUN_1002abea8();
    }
    plVar11 = (long *)FUN_10027aef0();
    (**(code **)(*plVar11 + 0xf0))(&local_480);
    uStack_468 = uStack_478;
    local_470 = local_480;
    local_480 = 0;
    uStack_478 = 0;
    uStack_458 = 0;
    local_460 = (void *)0x0;
    uStack_448 = 0;
    local_450 = (void *)0x0;
    local_440 = 0x3f800000;
    uVar10 = FUN_10027aef0();
    *(int *)(puVar12 + 1) = *(int *)(puVar12 + 1) + 1;
    local_548 = puVar12;
    puStack_540 = puVar16;
    thunk_FUN_1006cea64(local_538,uVar10,&local_548);
    if ((local_548 != (undefined8 *)0x0) &&
       (iVar6 = *(int *)(local_548 + 1), *(int *)(local_548 + 1) = iVar6 + -1, iVar6 + -1 == 0)) {
      FUN_1002abea8();
    }
    local_568 = 0;
    uStack_560 = 0;
    FUN_10014ebec(&local_2e0,param_2);
    FUN_100136b24(&local_2b0,puVar12,&local_568,&local_2e0,&local_470,local_538,param_2);
    if (local_2e0 != (long *)0x0) {
      for (; plStack_2d8 != local_2e0; plStack_2d8 = plStack_2d8 + -3) {
      }
      plStack_2d8 = local_2e0;
      operator_delete(local_2e0);
    }
    local_568 = FUN_10027aef0();
    local_558 = local_538;
    local_550 = &local_470;
    local_580 = (long *)FUN_10027aef0();
    uStack_578 = 0;
    local_570 = 0x3fffffff3fffffff;
    (**(code **)(*local_580 + 0xf0))(&local_2e0);
    uVar7 = (**(code **)(*plStack_2d8 + 0x100))();
    local_570 = CONCAT44(local_570._4_4_,uVar7);
    if ((local_2e0 != (long *)0x0) &&
       (iVar6 = (int)local_2e0[1] + -1, *(int *)(local_2e0 + 1) = iVar6, iVar6 == 0)) {
      FUN_1002abea8();
    }
    plVar11 = (long *)FUN_1002f80e4(0x20);
    plVar11[1] = 0;
    *plVar11 = 0;
    plVar11[3] = 0;
    plVar11[2] = 0;
    FUN_1002abda0();
    *plVar11 = (long)&PTR_thunk_FUN_1002abe00_100d887e0;
    plVar11[3] = (long)&PTR_FUN_100d88830;
    *(int *)(plVar11 + 1) = (int)plVar11[1] + 1;
    local_5c8 = &local_2b0;
    local_5e0 = &local_568;
    local_590 = &local_580;
    local_598 = local_538;
    local_2e0 = plVar11;
    FUN_100153ab8(&local_588,&local_2e0,&local_5c8,&local_5e0,&local_590,&local_598);
    if ((local_2e0 != (long *)0x0) &&
       (iVar6 = (int)local_2e0[1] + -1, *(int *)(local_2e0 + 1) = iVar6, iVar6 == 0)) {
      FUN_1002abea8();
    }
    FUN_100138184(&local_5b0,&local_2b0,&local_430,&local_418,&local_400,&local_3d0,&local_3b8,
                  &local_388,&local_370,&local_358,&local_340,&local_310);
    puVar12 = local_5b0;
    if (local_5b0 != (undefined8 *)0x0) {
      while (local_5a8 != puVar12) {
        local_5a8 = local_5a8 + -1;
        piVar14 = (int *)*local_5a8;
        if ((piVar14 != (int *)0x0) && (iVar6 = *piVar14, *piVar14 = iVar6 + -1, iVar6 + -1 == 0)) {
          FUN_100469e84();
        }
      }
      local_5a8 = puVar12;
      operator_delete(local_5b0);
    }
    local_5c8 = (undefined8 **)0x0;
    local_5c0 = (undefined8 **)0x0;
    local_5b8 = (undefined8 **)0x0;
    if (local_430 == puStack_428) {
      ppuVar15 = (undefined8 **)0x0;
      puVar12 = local_418;
    }
    else {
      ppuVar15 = (undefined8 **)0x0;
      puVar16 = local_430;
      do {
        cVar5 = *(char *)((long)puVar16 + 0x17);
        if (cVar5 < '\0') {
          if (puVar16[1] != 0) goto LAB_100134510;
        }
        else if (cVar5 != '\0') {
LAB_100134510:
          if (ppuVar15 < local_5b8) {
            if (cVar5 < '\0') {
              FUN_100147c88(ppuVar15,*puVar16,puVar16[1]);
              ppuVar15 = ppuVar15 + 3;
              local_5c0 = ppuVar15;
            }
            else {
              puVar13 = (undefined8 *)puVar16[1];
              puVar12 = (undefined8 *)*puVar16;
              ppuVar15[2] = (undefined8 *)puVar16[2];
              local_5c0 = ppuVar15 + 3;
              ppuVar15[1] = puVar13;
              *ppuVar15 = puVar12;
              ppuVar15 = local_5c0;
            }
          }
          else {
            ppuVar15 = (undefined8 **)FUN_100154134(&local_5c8,puVar16);
            local_5c0 = ppuVar15;
          }
        }
        puVar16 = puVar16 + 6;
        puVar12 = local_418;
      } while (puVar16 != puStack_428);
    }
    for (; puVar12 != puStack_410; puVar12 = puVar12 + 6) {
      cVar5 = *(char *)((long)puVar12 + 0x17);
      if (cVar5 < '\0') {
        if (puVar12[1] != 0) goto LAB_10013458c;
      }
      else if (cVar5 != '\0') {
LAB_10013458c:
        if (ppuVar15 < local_5b8) {
          if (cVar5 < '\0') {
            FUN_100147c88(ppuVar15,*puVar12,puVar12[1]);
            ppuVar15 = ppuVar15 + 3;
            local_5c0 = ppuVar15;
          }
          else {
            puVar13 = (undefined8 *)puVar12[1];
            puVar16 = (undefined8 *)*puVar12;
            ppuVar15[2] = (undefined8 *)puVar12[2];
            local_5c0 = ppuVar15 + 3;
            ppuVar15[1] = puVar13;
            *ppuVar15 = puVar16;
            ppuVar15 = local_5c0;
          }
        }
        else {
          ppuVar15 = (undefined8 **)FUN_100154134(&local_5c8,puVar12);
          local_5c0 = ppuVar15;
        }
      }
    }
    if (cStack_3e9 < '\0') {
      FUN_100147c88(&local_2e0,local_400,plStack_3f8);
    }
    else {
      plStack_2d8 = plStack_3f8;
      local_2e0 = local_400;
      local_2d0 = (long *)CONCAT17(cStack_3e9,local_3f0);
    }
    local_2c8 = local_3e8;
    if (local_3e8 != (int *)0x0) {
      *local_3e8 = *local_3e8 + 1;
    }
    local_2c0 = local_3e0;
    local_2b8 = local_3d8;
    FUN_100155880(&local_5e0,&local_2e0,1);
    puVar13 = local_5d8;
    puVar2 = local_5e0;
    puVar16 = local_5d8;
    ppuVar15 = local_5c0;
    for (puVar12 = local_5e0; local_5d8 = puVar2, local_5e0 = local_5d8, local_5c0 = ppuVar15,
        puVar12 != puVar13; puVar12 = puVar12 + 6) {
      cVar5 = *(char *)((long)puVar12 + 0x17);
      if (cVar5 < '\0') {
        if (puVar12[1] != 0) goto LAB_100134674;
      }
      else if (cVar5 != '\0') {
LAB_100134674:
        local_5d8 = puVar16;
        if (ppuVar15 < local_5b8) {
          if (cVar5 < '\0') {
            FUN_100147c88(ppuVar15,*puVar12,puVar12[1]);
            puVar16 = local_5d8;
            local_5c0 = ppuVar15 + 3;
          }
          else {
            puVar3 = (undefined8 *)puVar12[1];
            puVar2 = (undefined8 *)*puVar12;
            ppuVar15[2] = (undefined8 *)puVar12[2];
            ppuVar15[1] = puVar3;
            *ppuVar15 = puVar2;
            local_5c0 = ppuVar15 + 3;
          }
        }
        else {
          local_5c0 = (undefined8 **)FUN_100154134(&local_5c8,puVar12);
          puVar16 = local_5d8;
        }
      }
      local_5d8 = puVar16;
      puVar2 = local_5e0;
      puVar16 = local_5d8;
      ppuVar15 = local_5c0;
    }
    if (local_5d8 != (undefined8 *)0x0) {
      if (puVar16 == local_5d8) {
        operator_delete(local_5d8);
        puVar16 = local_5d8;
      }
      else {
        do {
          piVar14 = (int *)puVar16[-3];
          if ((piVar14 != (int *)0x0) && (iVar6 = *piVar14, *piVar14 = iVar6 + -1, iVar6 + -1 == 0))
          {
            FUN_100469e84();
          }
          puVar16 = puVar16 + -6;
        } while (puVar16 != local_5d8);
        operator_delete(local_5e0);
        puVar16 = local_5d8;
      }
    }
    local_5d8 = puVar16;
    if ((local_2c8 != (int *)0x0) && (iVar6 = *local_2c8, *local_2c8 = iVar6 + -1, iVar6 + -1 == 0))
    {
      FUN_100469e84();
    }
    puVar12 = local_3d0;
    if ((long)local_2d0 < 0) {
      operator_delete(local_2e0);
      puVar12 = local_3d0;
    }
    for (; ppuVar15 = local_5c0, puVar12 != local_3c8; puVar12 = puVar12 + 6) {
      cVar5 = *(char *)((long)puVar12 + 0x17);
      if (cVar5 < '\0') {
        if (puVar12[1] != 0) goto LAB_1001347a0;
      }
      else if (cVar5 != '\0') {
LAB_1001347a0:
        if (local_5c0 < local_5b8) {
          if (cVar5 < '\0') {
            FUN_100147c88(local_5c0,*puVar12,puVar12[1]);
            local_5c0 = ppuVar15 + 3;
          }
          else {
            puVar13 = (undefined8 *)puVar12[1];
            puVar16 = (undefined8 *)*puVar12;
            local_5c0[2] = (undefined8 *)puVar12[2];
            local_5c0[1] = puVar13;
            *local_5c0 = puVar16;
            local_5c0 = local_5c0 + 3;
          }
        }
        else {
          local_5c0 = (undefined8 **)FUN_100154134(&local_5c8,puVar12);
        }
      }
    }
    if (cStack_3a1 < '\0') {
      FUN_100147c88(&local_2e0,local_3b8,plStack_3b0);
    }
    else {
      plStack_2d8 = plStack_3b0;
      local_2e0 = local_3b8;
      local_2d0 = (long *)CONCAT17(cStack_3a1,local_3a8);
    }
    local_2c8 = local_3a0;
    if (local_3a0 != (int *)0x0) {
      *local_3a0 = *local_3a0 + 1;
    }
    local_2c0 = local_398;
    local_2b8 = local_390;
    FUN_100155880(&local_5e0,&local_2e0,1);
    puVar2 = local_5d8;
    puVar16 = local_5e0;
    puVar13 = local_5d8;
    ppuVar15 = local_5c0;
    for (puVar12 = local_5e0; local_5e0 = puVar16, local_5d8 = puVar13, local_5c0 = ppuVar15,
        puVar12 != puVar2; puVar12 = puVar12 + 6) {
      cVar5 = *(char *)((long)puVar12 + 0x17);
      if (cVar5 < '\0') {
        if (puVar12[1] != 0) goto LAB_100134890;
      }
      else if (cVar5 != '\0') {
LAB_100134890:
        if (ppuVar15 < local_5b8) {
          if (cVar5 < '\0') {
            FUN_100147c88(ppuVar15,*puVar12,puVar12[1]);
            local_5c0 = ppuVar15 + 3;
          }
          else {
            puVar13 = (undefined8 *)puVar12[1];
            puVar16 = (undefined8 *)*puVar12;
            ppuVar15[2] = (undefined8 *)puVar12[2];
            ppuVar15[1] = puVar13;
            *ppuVar15 = puVar16;
            local_5c0 = ppuVar15 + 3;
          }
        }
        else {
          local_5c0 = (undefined8 **)FUN_100154134(&local_5c8,puVar12);
        }
      }
      puVar16 = local_5e0;
      puVar13 = local_5d8;
      ppuVar15 = local_5c0;
    }
    if (puVar16 != (undefined8 *)0x0) {
      if (puVar13 == puVar16) {
        local_5d8 = puVar16;
        operator_delete(puVar16);
      }
      else {
        do {
          piVar14 = (int *)puVar13[-3];
          if ((piVar14 != (int *)0x0) && (iVar6 = *piVar14, *piVar14 = iVar6 + -1, iVar6 + -1 == 0))
          {
            FUN_100469e84();
          }
          puVar13 = puVar13 + -6;
        } while (puVar13 != puVar16);
        local_5d8 = puVar16;
        operator_delete(local_5e0);
      }
    }
    if ((local_2c8 != (int *)0x0) && (iVar6 = *local_2c8, *local_2c8 = iVar6 + -1, iVar6 + -1 == 0))
    {
      FUN_100469e84();
    }
    puVar12 = local_388;
    if ((long)local_2d0 < 0) {
      operator_delete(local_2e0);
      puVar12 = local_388;
    }
    for (; ppuVar15 = local_5c0, puVar16 = local_370, puVar12 != local_380; puVar12 = puVar12 + 6) {
      cVar5 = *(char *)((long)puVar12 + 0x17);
      if (cVar5 < '\0') {
        if (puVar12[1] != 0) goto LAB_1001349bc;
      }
      else if (cVar5 != '\0') {
LAB_1001349bc:
        if (local_5c0 < local_5b8) {
          if (cVar5 < '\0') {
            FUN_100147c88(local_5c0,*puVar12,puVar12[1]);
            local_5c0 = ppuVar15 + 3;
          }
          else {
            puVar13 = (undefined8 *)puVar12[1];
            puVar16 = (undefined8 *)*puVar12;
            local_5c0[2] = (undefined8 *)puVar12[2];
            local_5c0[1] = puVar13;
            *local_5c0 = puVar16;
            local_5c0 = local_5c0 + 3;
          }
        }
        else {
          local_5c0 = (undefined8 **)FUN_100154134(&local_5c8,puVar12);
        }
      }
    }
    for (; ppuVar15 = local_5c0, puVar12 = local_358, puVar16 != local_368; puVar16 = puVar16 + 6) {
      cVar5 = *(char *)((long)puVar16 + 0x17);
      if (cVar5 < '\0') {
        if (puVar16[1] != 0) goto LAB_100134a38;
      }
      else if (cVar5 != '\0') {
LAB_100134a38:
        if (local_5c0 < local_5b8) {
          if (cVar5 < '\0') {
            FUN_100147c88(local_5c0,*puVar16,puVar16[1]);
            local_5c0 = ppuVar15 + 3;
          }
          else {
            puVar13 = (undefined8 *)puVar16[1];
            puVar12 = (undefined8 *)*puVar16;
            local_5c0[2] = (undefined8 *)puVar16[2];
            local_5c0[1] = puVar13;
            *local_5c0 = puVar12;
            local_5c0 = local_5c0 + 3;
          }
        }
        else {
          local_5c0 = (undefined8 **)FUN_100154134(&local_5c8,puVar16);
        }
      }
    }
    for (; ppuVar15 = local_5c0, puVar12 != local_350; puVar12 = puVar12 + 6) {
      cVar5 = *(char *)((long)puVar12 + 0x17);
      if (cVar5 < '\0') {
        if (puVar12[1] != 0) goto LAB_100134ab4;
      }
      else if (cVar5 != '\0') {
LAB_100134ab4:
        if (local_5c0 < local_5b8) {
          if (cVar5 < '\0') {
            FUN_100147c88(local_5c0,*puVar12,puVar12[1]);
            local_5c0 = ppuVar15 + 3;
          }
          else {
            puVar13 = (undefined8 *)puVar12[1];
            puVar16 = (undefined8 *)*puVar12;
            local_5c0[2] = (undefined8 *)puVar12[2];
            local_5c0[1] = puVar13;
            *local_5c0 = puVar16;
            local_5c0 = local_5c0 + 3;
          }
        }
        else {
          local_5c0 = (undefined8 **)FUN_100154134(&local_5c8,puVar12);
        }
      }
    }
    if (cStack_329 < '\0') {
      FUN_100147c88(&local_2e0,local_340,plStack_338);
    }
    else {
      plStack_2d8 = plStack_338;
      local_2e0 = local_340;
      local_2d0 = (long *)CONCAT17(cStack_329,local_330);
    }
    local_2c8 = local_328;
    if (local_328 != (int *)0x0) {
      *local_328 = *local_328 + 1;
    }
    local_2c0 = local_320;
    local_2b8 = local_318;
    FUN_100155880(&local_5e0,&local_2e0,1);
    puVar2 = local_5d8;
    puVar16 = local_5e0;
    puVar13 = local_5d8;
    ppuVar15 = local_5c0;
    for (puVar12 = local_5e0; local_5e0 = puVar16, local_5d8 = puVar13, local_5c0 = ppuVar15,
        puVar12 != puVar2; puVar12 = puVar12 + 6) {
      cVar5 = *(char *)((long)puVar12 + 0x17);
      if (cVar5 < '\0') {
        if (puVar12[1] != 0) goto LAB_100134ba4;
      }
      else if (cVar5 != '\0') {
LAB_100134ba4:
        if (ppuVar15 < local_5b8) {
          if (cVar5 < '\0') {
            FUN_100147c88(ppuVar15,*puVar12,puVar12[1]);
            local_5c0 = ppuVar15 + 3;
          }
          else {
            puVar13 = (undefined8 *)puVar12[1];
            puVar16 = (undefined8 *)*puVar12;
            ppuVar15[2] = (undefined8 *)puVar12[2];
            ppuVar15[1] = puVar13;
            *ppuVar15 = puVar16;
            local_5c0 = ppuVar15 + 3;
          }
        }
        else {
          local_5c0 = (undefined8 **)FUN_100154134(&local_5c8,puVar12);
        }
      }
      puVar16 = local_5e0;
      puVar13 = local_5d8;
      ppuVar15 = local_5c0;
    }
    if (puVar16 != (undefined8 *)0x0) {
      if (puVar13 == puVar16) {
        local_5d8 = puVar16;
        operator_delete(puVar16);
      }
      else {
        do {
          piVar14 = (int *)puVar13[-3];
          if ((piVar14 != (int *)0x0) && (iVar6 = *piVar14, *piVar14 = iVar6 + -1, iVar6 + -1 == 0))
          {
            FUN_100469e84();
          }
          puVar13 = puVar13 + -6;
        } while (puVar13 != puVar16);
        local_5d8 = puVar16;
        operator_delete(local_5e0);
      }
    }
    if ((local_2c8 != (int *)0x0) && (iVar6 = *local_2c8, *local_2c8 = iVar6 + -1, iVar6 + -1 == 0))
    {
      FUN_100469e84();
    }
    if ((long)local_2d0 < 0) {
      operator_delete(local_2e0);
    }
    if (cStack_2f9 < '\0') {
      FUN_100147c88(&local_2e0,local_310,plStack_308);
    }
    else {
      local_2d0 = (long *)CONCAT17(cStack_2f9,local_300);
      local_2e0 = local_310;
      plStack_2d8 = plStack_308;
    }
    local_2c8 = local_2f8;
    if (local_2f8 != (int *)0x0) {
      *local_2f8 = *local_2f8 + 1;
    }
    local_2c0 = local_2f0;
    local_2b8 = local_2e8;
    FUN_100155880(&local_5e0,&local_2e0,1);
    puVar2 = local_5d8;
    puVar16 = local_5e0;
    puVar13 = local_5d8;
    ppuVar15 = local_5c0;
    for (puVar12 = local_5e0; local_5e0 = puVar16, local_5d8 = puVar13, local_5c0 = ppuVar15,
        puVar12 != puVar2; puVar12 = puVar12 + 6) {
      cVar5 = *(char *)((long)puVar12 + 0x17);
      if (cVar5 < '\0') {
        if (puVar12[1] != 0) goto LAB_100134d4c;
      }
      else if (cVar5 != '\0') {
LAB_100134d4c:
        if (ppuVar15 < local_5b8) {
          if (cVar5 < '\0') {
            FUN_100147c88(ppuVar15,*puVar12,puVar12[1]);
            local_5c0 = ppuVar15 + 3;
          }
          else {
            puVar13 = (undefined8 *)puVar12[1];
            puVar16 = (undefined8 *)*puVar12;
            ppuVar15[2] = (undefined8 *)puVar12[2];
            ppuVar15[1] = puVar13;
            *ppuVar15 = puVar16;
            local_5c0 = ppuVar15 + 3;
          }
        }
        else {
          local_5c0 = (undefined8 **)FUN_100154134(&local_5c8,puVar12);
        }
      }
      puVar16 = local_5e0;
      puVar13 = local_5d8;
      ppuVar15 = local_5c0;
    }
    if (puVar16 != (undefined8 *)0x0) {
      if (puVar13 == puVar16) {
        local_5d8 = puVar16;
        operator_delete(puVar16);
      }
      else {
        do {
          piVar14 = (int *)puVar13[-3];
          if ((piVar14 != (int *)0x0) && (iVar6 = *piVar14, *piVar14 = iVar6 + -1, iVar6 + -1 == 0))
          {
            FUN_100469e84();
          }
          puVar13 = puVar13 + -6;
        } while (puVar13 != puVar16);
        local_5d8 = puVar16;
        operator_delete(local_5e0);
      }
    }
    if ((local_2c8 != (int *)0x0) && (iVar6 = *local_2c8, *local_2c8 = iVar6 + -1, iVar6 + -1 == 0))
    {
      FUN_100469e84();
    }
    if ((long)local_2d0 < 0) {
      operator_delete(local_2e0);
    }
    local_2d0._7_1_ = '\a';
    local_2e0 = (long *)&DAT_72656e6e616353;
    uVar10 = std::chrono::system_clock::now();
    FUN_10073cd34(&local_5e0,2,&local_2e0,uVar10);
    if (local_2d0._7_1_ < '\0') {
      operator_delete(local_2e0);
    }
    iVar6 = FUN_1007396c0(&local_5e0);
    if (iVar6 != 0) {
      FUN_100736880(&local_5e0,"Starting scan, Reason: Explicit, All Folders?: true");
    }
    thunk_FUN_1007363ec(&local_5e0);
    FUN_10067b9d8(&local_5e0,&local_5c8);
    local_2e0 = (long *)CONCAT35(local_2e0._5_3_,0x10000002a);
    local_2c8 = (int *)0x0;
    plStack_2d8 = (long *)0x0;
    local_2d0 = (long *)0x0;
    FUN_100154f84(&plStack_2d8,local_5e0,local_5d8,(long)local_5d8 - (long)local_5e0 >> 5);
    FUN_10013fda8(&local_2b0,&local_2e0);
    if (plStack_2d8 != (long *)0x0) {
      for (; local_2d0 != plStack_2d8; local_2d0 = local_2d0 + -4) {
      }
      local_2d0 = plStack_2d8;
      operator_delete(plStack_2d8);
    }
    if (local_5e0 != (undefined8 *)0x0) {
      for (; local_5d8 != local_5e0; local_5d8 = local_5d8 + -4) {
      }
      local_5d8 = local_5e0;
      operator_delete(local_5e0);
    }
    do {
      uVar1 = NEON_umaxv(CONCAT17(~(byte)(-(ulong)(lStack_218 == 0) >> 8),
                                  CONCAT16(~(byte)-(ulong)(lStack_218 == 0),
                                           CONCAT15(~(byte)(-(ulong)(lStack_220 == 0) >> 8),
                                                    CONCAT14(~(byte)-(ulong)(lStack_220 == 0),
                                                             CONCAT13(~(byte)(-(ulong)(lStack_228 ==
                                                                                      0) >> 8),
                                                                      CONCAT12(~(byte)-(ulong)(
                                                  lStack_228 == 0),
                                                  CONCAT11(~(byte)(-(ulong)(local_230 == 0) >> 8),
                                                           ~(byte)-(ulong)(local_230 == 0)))))))),2)
      ;
      if ((((uVar1 & 1) == 0) && (local_210 == 0)) && (local_1f8 == local_1f0 && local_200 == 0)) {
        uVar8 = local_1d8;
        if (local_208 != 0) {
          uVar8 = FUN_1006cbcb8(local_208 + 0x18);
          if (local_1d8 != 0) {
            uVar8 = 1;
          }
          uVar8 = uVar8 & 1;
        }
        if (((uVar8 == 0) && (local_1a8 == 0)) &&
           (((local_1e0 & 1) == 0 && (((local_190 & 1) == 0 && (local_118 == 0))))))
        goto code_r0x00010013501c;
      }
      FUN_10013c0b8(&local_2b0);
    } while( true );
  }
  cVar5 = FUN_10014d60c(PTR_cerr_100d601f8,
                        "Error reading lib config file, or no lib config file specified.",0x3f);
  std::ios_base::getloc();
  plVar11 = (long *)std::locale::use_facet((id *)&local_2b0);
  (**(code **)(*plVar11 + 0x38))(plVar11,10);
  std::locale::~locale(&local_2b0);
  std::ostream::put(cVar5);
  std::ostream::flush();
  FUN_10014bec8(&local_430);
  uVar10 = 1;
LAB_1001350fc:
  if (*(long *)PTR____stack_chk_guard_100d60390 == local_58) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail(uVar10);
code_r0x00010013501c:
  if (local_5c8 != (undefined8 **)0x0) {
    for (; local_5c0 != local_5c8; local_5c0 = local_5c0 + -3) {
    }
    local_5c0 = local_5c8;
    operator_delete(local_5c8);
  }
  if ((local_588 != 0) &&
     (iVar6 = *(int *)(local_588 + 8) + -1, *(int *)(local_588 + 8) = iVar6, iVar6 == 0)) {
    FUN_1002abea8();
  }
  FUN_100152fbc(&local_2b0);
  FUN_100153344(local_538);
  pvVar4 = local_460;
  puVar12 = local_450;
  while (puVar12 != (void *)0x0) {
    pvVar17 = (void *)*puVar12;
    local_460 = pvVar4;
    operator_delete(puVar12);
    pvVar4 = local_460;
    puVar12 = pvVar17;
  }
  local_460 = (void *)0x0;
  if (pvVar4 != (void *)0x0) {
    operator_delete(pvVar4);
  }
  if ((local_470 != 0) &&
     (iVar6 = *(int *)(local_470 + 8) + -1, *(int *)(local_470 + 8) = iVar6, iVar6 == 0)) {
    FUN_1002abea8();
  }
  if ((local_438 != (undefined8 *)0x0) &&
     (iVar6 = *(int *)(local_438 + 1), *(int *)(local_438 + 1) = iVar6 + -1, iVar6 + -1 == 0)) {
    FUN_1002abea8();
  }
  FUN_10014bec8(&local_430);
  uVar10 = 0;
  goto LAB_1001350fc;
}

