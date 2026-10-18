// 0x100132970 FUN_100132970 state=exported-with-warnings body_bytes=3664 warnings=4 chunk=chunk-00052.jsonl

/* WARNING: Removing unreachable block (ram,0x000100133100) */
/* WARNING: Removing unreachable block (ram,0x000100133454) */
/* WARNING: Removing unreachable block (ram,0x0001001334a4) */

undefined8 FUN_100132970(long param_1)

{
  char *pcVar1;
  ushort uVar2;
  byte bVar3;
  void *pvVar4;
  undefined8 *puVar5;
  undefined ***pppuVar6;
  int iVar7;
  undefined4 uVar8;
  uint uVar9;
  undefined8 uVar10;
  long *plVar11;
  undefined **ppuVar12;
  undefined **ppuVar13;
  ulong uVar14;
  long *plVar15;
  long lVar16;
  void *pvVar17;
  undefined ***pppuVar18;
  undefined4 in_wzr;
  undefined ***local_518;
  undefined ***local_510;
  undefined8 local_508;
  undefined8 uStack_500;
  int *local_4f8;
  int *local_4f0;
  undefined1 auStack_4e8 [8];
  void **local_4e0;
  void **local_4d8;
  undefined1 auStack_4c8 [16];
  long **local_4b8 [2];
  long **local_4a8 [2];
  long local_498;
  long *local_490;
  undefined8 local_488;
  undefined8 local_480;
  void *local_478;
  void *local_470;
  long **local_468;
  long *local_460;
  undefined **local_458;
  undefined **local_450;
  long *local_448;
  long *local_440;
  char local_431;
  long local_390;
  undefined8 uStack_388;
  long local_380;
  undefined8 uStack_378;
  void *local_370;
  undefined8 uStack_368;
  void *local_360;
  undefined8 uStack_358;
  undefined4 local_350;
  long local_348;
  long *local_340;
  undefined1 auStack_338 [8];
  long *local_330;
  byte local_321;
  long *local_320;
  long *local_318;
  long *local_310;
  long *local_308;
  byte local_2f9;
  undefined **local_2f8;
  undefined **local_2f0;
  undefined **ppuStack_2e8;
  undefined7 local_2e0;
  char cStack_2d9;
  undefined ***local_2d8;
  long local_270;
  long lStack_268;
  long lStack_260;
  long lStack_258;
  long local_250;
  long local_248;
  long local_240;
  long local_238;
  long local_230;
  byte local_220;
  int local_218;
  long local_1e8;
  byte local_1d0;
  long local_158;
  long alStack_98 [3];
  long *local_80;
  long local_78;
  
  local_78 = *(long *)PTR____stack_chk_guard_100d60390;
  FUN_10014dc18(param_1 + 0x58);
  cStack_2d9 = '\a';
  local_2f0 = (undefined **)&DAT_72656e6e616353;
  uVar10 = std::chrono::system_clock::now();
  FUN_10073cd34(&local_448,1,&local_2f0,uVar10);
  if (cStack_2d9 < '\0') {
    operator_delete(local_2f0);
  }
  iVar7 = FUN_1007396c0(&local_448);
  if (iVar7 != 0) {
    FUN_100736880(&local_448,"Entering controlled mode");
  }
  thunk_FUN_1007363ec(&local_448);
  FUN_10014ddfc(param_1);
  FUN_10014e198(param_1);
  cStack_2d9 = '\a';
  local_2f0 = (undefined **)&DAT_72656e6e616353;
  uVar10 = std::chrono::system_clock::now();
  FUN_10073cd34(&local_380,2,&local_2f0,uVar10);
  if (cStack_2d9 < '\0') {
    operator_delete(local_2f0);
  }
  iVar7 = FUN_1007396c0(&local_380);
  if (iVar7 != 0) {
    uVar10 = FUN_100736880(&local_380,"App resources: ");
    FUN_1001e5250(&local_448);
    (**(code **)(*local_440 + 0xc0))(&local_2f0);
    FUN_10013a004(uVar10,&local_2f0);
    if (cStack_2d9 < '\0') {
      operator_delete(local_2f0);
    }
    if ((local_448 != (long *)0x0) &&
       (iVar7 = (int)local_448[1] + -1, *(int *)(local_448 + 1) = iVar7, iVar7 == 0)) {
      FUN_1002abea8();
    }
  }
  thunk_FUN_1007363ec(&local_380);
  FUN_1001cfb20(&local_2f0);
  FUN_100211cc4(&local_2f0);
  FUN_100154a2c(&ppuStack_2e8,CONCAT17(cStack_2d9,local_2e0));
  plVar11 = (long *)FUN_10027aef0();
  (**(code **)(*plVar11 + 0x38))
            (plVar11,param_1,6,*(undefined4 *)(param_1 + 0x70),*(undefined4 *)(param_1 + 0x74));
  ppuVar12 = (undefined **)FUN_1002f80e4(0x98);
  ppuVar12[0x12] = (undefined *)0x0;
  ppuVar12[0xf] = (undefined *)0x0;
  ppuVar12[0xe] = (undefined *)0x0;
  ppuVar12[0x11] = (undefined *)0x0;
  ppuVar12[0x10] = (undefined *)0x0;
  ppuVar12[0xb] = (undefined *)0x0;
  ppuVar12[10] = (undefined *)0x0;
  ppuVar12[0xd] = (undefined *)0x0;
  ppuVar12[0xc] = (undefined *)0x0;
  ppuVar12[7] = (undefined *)0x0;
  ppuVar12[6] = (undefined *)0x0;
  ppuVar12[9] = (undefined *)0x0;
  ppuVar12[8] = (undefined *)0x0;
  ppuVar12[3] = (undefined *)0x0;
  ppuVar12[2] = (undefined *)0x0;
  ppuVar12[5] = (undefined *)0x0;
  ppuVar12[4] = (undefined *)0x0;
  ppuVar12[1] = (undefined *)0x0;
  *ppuVar12 = (undefined *)0x0;
  FUN_1002abda0();
  ppuVar12[3] = (undefined *)&PTR_FUN_100db9540;
  *ppuVar12 = (undefined *)&PTR_thunk_FUN_100695958_100db94d0;
  ppuVar12[6] = (undefined *)0x0;
  ppuVar12[7] = (undefined *)0x0;
  ppuVar12[5] = (undefined *)0x0;
  ppuVar12[4] = (undefined *)(ppuVar12 + 5);
  ppuVar12[8] = (undefined *)0x0;
  ppuVar12[9] = (undefined *)0x0;
  ppuVar12[0xc] = (undefined *)0x0;
  ppuVar12[0xb] = (undefined *)0x0;
  ppuVar12[10] = (undefined *)(ppuVar12 + 0xb);
  *(undefined1 *)(ppuVar12 + 0xd) = 0;
  ppuVar12[0xf] = (undefined *)0x0;
  ppuVar12[0xe] = (undefined *)0x0;
  ppuVar12[0x11] = (undefined *)0x0;
  ppuVar12[0x10] = (undefined *)0x0;
  ppuVar12[0x12] = (undefined *)0x0;
  *(int *)(ppuVar12 + 1) = *(int *)(ppuVar12 + 1) + 1;
  local_2f8 = ppuVar12;
  plVar11 = (long *)FUN_10027aef0();
  *(int *)(ppuVar12 + 1) = *(int *)(ppuVar12 + 1) + 1;
  local_2f0 = ppuVar12;
  ppuStack_2e8 = ppuVar12 + 3;
  (**(code **)(*plVar11 + 0x120))(plVar11,&local_2f0);
  if ((local_2f0 != (undefined **)0x0) &&
     (iVar7 = *(int *)(local_2f0 + 1), *(int *)(local_2f0 + 1) = iVar7 + -1, iVar7 + -1 == 0)) {
    FUN_1002abea8();
  }
  ppuVar13 = (undefined **)FUN_1002f80e4(0x38);
  thunk_FUN_1005284c4(ppuVar13,param_1 + 0x18,1);
  if (ppuVar13 != (undefined **)0x0) {
    *(int *)(ppuVar13 + 1) = *(int *)(ppuVar13 + 1) + 1;
  }
  local_2f0 = ppuVar13;
  FUN_100528d40(&local_2f0);
  if ((local_2f0 != (undefined **)0x0) &&
     (iVar7 = *(int *)(local_2f0 + 1), *(int *)(local_2f0 + 1) = iVar7 + -1, iVar7 + -1 == 0)) {
    FUN_1002abea8();
  }
  plVar11 = operator_new(0x58);
  FUN_1004516f4(&local_448,param_1 + 0x30);
  FUN_10014e584(&local_2f0,&local_448,0);
  *plVar11 = (long)&PTR_thunk_FUN_1001503c8_100d88508;
  plVar11[1] = (long)(plVar11 + 2);
  *(undefined8 *)((long)plVar11 + 0x14) = DAT_100b9c5a8;
  *(undefined4 *)((long)plVar11 + 0x1c) = 0xffffffff;
  if (cStack_2d9 < '\0') {
    FUN_100147c88(plVar11 + 4,local_2f0,ppuStack_2e8);
    *(undefined4 *)(plVar11 + 7) = 0;
    plVar11[9] = 0;
    plVar11[10] = 0;
    plVar11[8] = 0;
    if (cStack_2d9 < '\0') {
      operator_delete(local_2f0);
    }
  }
  else {
    plVar11[5] = (long)ppuStack_2e8;
    plVar11[4] = (long)local_2f0;
    plVar11[6] = CONCAT17(cStack_2d9,local_2e0);
    *(undefined4 *)(plVar11 + 7) = 0;
    plVar11[9] = 0;
    plVar11[10] = 0;
    plVar11[8] = 0;
  }
  if (local_431 < '\0') {
    operator_delete(local_448);
  }
  (**(code **)(*plVar11 + 0x38))(plVar11);
  uVar14 = (**(code **)(*plVar11 + 0x10))(plVar11);
  if ((uVar14 & 1) == 0) {
    cStack_2d9 = '\x03';
    local_2f0 = (undefined **)CONCAT44(local_2f0._4_4_,0x766564);
    uVar10 = std::chrono::system_clock::now();
    FUN_10073cd34(&local_448,4,&local_2f0,uVar10);
    if (cStack_2d9 < '\0') {
      operator_delete(local_2f0);
    }
    iVar7 = FUN_1007396c0(&local_448);
    if (iVar7 != 0) {
      uVar10 = FUN_100736880(&local_448,"Scanner: Failed to set up IPC channel. ");
      (**(code **)(*plVar11 + 0x48))(&local_2f0,plVar11);
      uVar10 = FUN_100737760(uVar10,&ppuStack_2e8);
      uVar10 = FUN_100736880(uVar10," ");
      iVar7 = FUN_10019fd6c();
      pcVar1 = " Process orphaned.";
      if (iVar7 == 0) {
        pcVar1 = "";
      }
      FUN_100736880(uVar10,pcVar1);
      if ((long)local_2d8 < 0) {
        operator_delete(ppuStack_2e8);
      }
    }
    thunk_FUN_1007363ec(&local_448);
    (**(code **)(*plVar11 + 8))(plVar11);
    uVar10 = 1;
  }
  else {
    local_2f9 = 0;
    local_308 = (long *)0x0;
    plVar15 = (long *)FUN_1002f80e4(0xe8);
    ppuStack_2e8 = (undefined **)&local_2f9;
    local_2f0 = &PTR_FUN_100d885a8;
    local_2d8 = &local_2f0;
    FUN_100611f78(plVar15,&local_2f0);
    if (plVar15 != (long *)0x0) {
      *(int *)(plVar15 + 1) = (int)plVar15[1] + 1;
    }
    local_448 = plVar15;
    if (local_2d8 == &local_2f0) {
      lVar16 = 0x20;
LAB_100132e88:
      (**(code **)((long)*local_2d8 + lVar16))();
    }
    else if (local_2d8 != (undefined ***)0x0) {
      lVar16 = 0x28;
      goto LAB_100132e88;
    }
    if ((local_308 != (long *)0x0) &&
       (iVar7 = *(int *)((long)local_308 + 8) + -1, *(int *)((long)local_308 + 8) = iVar7,
       iVar7 == 0)) {
      FUN_1002abea8();
    }
    local_80 = (long *)0x0;
    local_318 = plVar11;
    local_308 = plVar15;
    FUN_100612ec0(&local_310,plVar15,&local_318,alStack_98);
    if (local_80 == alStack_98) {
      lVar16 = 0x20;
LAB_100132ef0:
      (**(code **)(*local_80 + lVar16))();
    }
    else if (local_80 != (long *)0x0) {
      lVar16 = 0x28;
      goto LAB_100132ef0;
    }
    plVar11 = local_318;
    local_318 = (long *)0x0;
    if (plVar11 != (long *)0x0) {
      (**(code **)(*plVar11 + 8))();
    }
    plVar11 = local_310;
    local_310 = (long *)0x0;
    ppuVar12 = operator_new(0x10);
    *ppuVar12 = (undefined *)&PTR_FUN_100d88638;
    ppuVar12[1] = (undefined *)plVar11;
    plVar11 = (long *)FUN_1002f80e4(0xe0);
    local_2f0 = ppuVar12;
    thunk_FUN_1005db528(plVar11,&local_2f0,"index->live");
    ppuVar12 = local_2f0;
    if (plVar11 != (long *)0x0) {
      *(int *)(plVar11 + 1) = (int)plVar11[1] + 1;
    }
    local_2f0 = (undefined **)0x0;
    local_320 = plVar11;
    if (ppuVar12 != (undefined **)0x0) {
      (**(code **)(*ppuVar12 + 8))();
    }
    local_321 = 0;
    ppuStack_2e8 = (undefined **)&local_321;
    local_2f0 = &PTR_FUN_100d88698;
    local_2d8 = &local_2f0;
    FUN_1005dc12c(auStack_338,local_320,2,&local_2f0);
    if (local_330 != (long *)0x0) {
      LOAcquire();
      iVar7 = *(int *)((long)local_330 + 0xc);
      *(int *)((long)local_330 + 0xc) = iVar7 + -1;
      LORelease();
      if (iVar7 == 1) {
        (**(code **)(*local_330 + 0x18))();
      }
    }
    if (local_2d8 == &local_2f0) {
      lVar16 = 0x20;
LAB_100133004:
      (**(code **)((long)*local_2d8 + lVar16))();
    }
    else if (local_2d8 != (undefined ***)0x0) {
      lVar16 = 0x28;
      goto LAB_100133004;
    }
    FUN_10014e8fc(&local_348,param_1);
    plVar11 = (long *)FUN_10027aef0();
    (**(code **)(*plVar11 + 0xf0))(&local_390);
    uStack_378 = uStack_388;
    local_380 = local_390;
    local_390 = 0;
    uStack_388 = 0;
    uStack_368 = 0;
    local_370 = (void *)0x0;
    uStack_358 = 0;
    local_360 = (void *)0x0;
    local_350 = 0x3f800000;
    uVar10 = FUN_10027aef0();
    ppuVar12 = local_2f8;
    local_458 = local_2f8;
    if (local_2f8 != (undefined **)0x0) {
      *(int *)(local_2f8 + 1) = *(int *)(local_2f8 + 1) + 1;
    }
    local_450 = (undefined **)0x0;
    if (local_2f8 != (undefined **)0x0) {
      local_450 = local_2f8 + 3;
    }
    thunk_FUN_1006cea64(&local_448,uVar10,&local_458);
    if ((local_458 != (undefined **)0x0) &&
       (iVar7 = *(int *)(local_458 + 1), *(int *)(local_458 + 1) = iVar7 + -1, iVar7 + -1 == 0)) {
      FUN_1002abea8();
    }
    FUN_10014ebec(&local_478,param_1);
    FUN_100136b24(&local_2f0,ppuVar12,&local_348,&local_478,&local_380,&local_448,param_1);
    if (local_478 != (void *)0x0) {
      for (; local_470 != local_478; local_470 = (void *)((long)local_470 + -0x18)) {
      }
      local_470 = local_478;
      operator_delete(local_478);
    }
    local_478 = (void *)FUN_10027aef0();
    local_468 = &local_448;
    local_460 = &local_380;
    local_490 = (long *)FUN_10027aef0();
    local_488 = 0;
    local_480 = 0x3fffffff3fffffff;
    (**(code **)(*local_490 + 0xf0))(&local_518);
    uVar8 = (*(code *)(*local_510)[0x20])();
    local_480 = CONCAT44(local_480._4_4_,uVar8);
    if ((local_518 != (undefined ***)0x0) &&
       (iVar7 = *(int *)(local_518 + 1), *(int *)(local_518 + 1) = iVar7 + -1, iVar7 + -1 == 0)) {
      FUN_1002abea8();
    }
    local_518 = &local_2f0;
    local_4e0 = &local_478;
    local_4a8[0] = &local_490;
    local_4b8[0] = &local_448;
    FUN_10014edf8(&local_498,&local_320,&local_518,&local_4e0,local_4a8,local_4b8);
    FUN_1005dbf08(local_320);
    FUN_1005dbfd0(local_320);
    FUN_1001afda8(local_4a8);
    FUN_1001afda8(local_4b8);
    FUN_1001afda8(auStack_4c8);
    while ((local_321 & 1) == 0) {
      iVar7 = FUN_1001afebc(local_4a8);
      if ((iVar7 == 0) || (iVar7 = FUN_1001b00e4(local_4a8), 1999 < iVar7)) {
        uVar14 = FUN_10019fd6c();
        FUN_1001afdb8(local_4a8);
        if ((uVar14 & 1) != 0) break;
      }
      LOAcquire();
      LORelease();
      bVar3 = local_2f9 & 1;
      local_2f9 = (byte)in_wzr;
      if (bVar3 != 0) {
        FUN_100612ccc(local_308);
      }
      if ((local_340 != (long *)0x0) &&
         ((iVar7 = FUN_1001afebc(local_4b8), iVar7 == 0 ||
          (iVar7 = FUN_1001b00e4(local_4b8), 1999 < iVar7)))) {
        (**(code **)(*local_340 + 0x10))(&local_4e0);
        if (local_4d8 != local_4e0) {
          local_508._7_1_ = '\a';
          local_518 = (undefined ***)&DAT_72656e6e616353;
          uVar10 = std::chrono::system_clock::now();
          FUN_10073cd34(auStack_4e8,2,&local_518,uVar10);
          if (local_508._7_1_ < '\0') {
            operator_delete(local_518);
          }
          iVar7 = FUN_1007396c0(auStack_4e8);
          if (iVar7 != 0) {
            uVar10 = FUN_100736880(auStack_4e8,"Starting scan, Reason: OS Events, Folders: ");
            FUN_10014ef34(&local_518,&local_4e0,FUN_10014f04c);
            FUN_100446c84(&local_4f8,",");
            if (local_4f8 == (int *)0x0) {
              lVar16 = -1;
            }
            else {
              lVar16 = (long)(local_4f8[1] / 2 + -1);
            }
            FUN_100445ddc(&local_4f0,&local_518,local_4f8 + 4,lVar16);
            FUN_1004525f4(uVar10,&local_4f0);
            if ((local_4f0 != (int *)0x0) &&
               (iVar7 = *local_4f0, *local_4f0 = iVar7 + -1, iVar7 + -1 == 0)) {
              FUN_100469e84();
            }
            if ((local_4f8 != (int *)0x0) &&
               (iVar7 = *local_4f8, *local_4f8 = iVar7 + -1, iVar7 + -1 == 0)) {
              FUN_100469e84();
            }
            pppuVar6 = local_518;
            pppuVar18 = local_510;
            if (local_518 != (undefined ***)0x0) {
              while (pppuVar18 != pppuVar6) {
                pppuVar18 = pppuVar18 + -1;
                ppuVar12 = *pppuVar18;
                if ((ppuVar12 != (undefined **)0x0) &&
                   (iVar7 = *(int *)ppuVar12, *(int *)ppuVar12 = iVar7 + -1, iVar7 + -1 == 0)) {
                  FUN_100469e84();
                }
              }
              local_510 = pppuVar6;
              operator_delete(local_518);
            }
          }
          thunk_FUN_1007363ec(auStack_4e8);
          local_518 = (undefined ***)CONCAT35(local_518._5_3_,0x3fffffff);
          local_508 = (undefined ***)0x0;
          uStack_500 = 0;
          local_510 = (undefined ***)0x0;
          FUN_100154f84(&local_510,local_4e0,local_4d8,(long)local_4d8 - (long)local_4e0 >> 5);
          FUN_10013fda8(&local_2f0,&local_518);
          if (local_510 != (undefined ***)0x0) {
            for (; local_508 != local_510; local_508 = local_508 + -4) {
            }
            local_508 = local_510;
            operator_delete(local_510);
          }
        }
        FUN_1001afdb8(local_4b8);
        if (local_4e0 != (void **)0x0) {
          for (; local_4d8 != local_4e0; local_4d8 = local_4d8 + -4) {
          }
          local_4d8 = local_4e0;
          operator_delete(local_4e0);
        }
      }
      FUN_1006cf5c0(&local_448);
      uVar10 = FUN_1006cf56c(&local_448);
      FUN_10013ba4c(&local_2f0,uVar10,0);
      FUN_1006cf574(&local_448);
      uVar2 = NEON_umaxv(CONCAT17(~(byte)(-(ulong)(lStack_258 == 0) >> 8),
                                  CONCAT16(~(byte)-(ulong)(lStack_258 == 0),
                                           CONCAT15(~(byte)(-(ulong)(lStack_260 == 0) >> 8),
                                                    CONCAT14(~(byte)-(ulong)(lStack_260 == 0),
                                                             CONCAT13(~(byte)(-(ulong)(lStack_268 ==
                                                                                      0) >> 8),
                                                                      CONCAT12(~(byte)-(ulong)(
                                                  lStack_268 == 0),
                                                  CONCAT11(~(byte)(-(ulong)(local_270 == 0) >> 8),
                                                           ~(byte)-(ulong)(local_270 == 0)))))))),2)
      ;
      if (((((uVar2 & 1) == 0) && (local_250 == 0)) && (local_238 == local_230)) && (local_240 == 0)
         ) {
        if (local_248 == 0) {
          if (local_218 == 0) goto LAB_100133554;
          goto LAB_100133564;
        }
        uVar9 = FUN_1006cbcb8(local_248 + 0x18);
        if (local_218 != 0) {
          uVar9 = 1;
        }
        if ((uVar9 & 1) != 0) goto LAB_100133564;
LAB_100133554:
        if (((local_1e8 != 0) || ((local_220 & 1) != 0)) ||
           (((local_1d0 & 1) != 0 || (local_158 != 0)))) goto LAB_100133564;
        FUN_1001af47c(0x32);
      }
      else {
LAB_100133564:
        FUN_10013c0b8(&local_2f0);
      }
      iVar7 = FUN_1001afebc(auStack_4c8);
      if ((iVar7 == 0) || (iVar7 = FUN_1001b00e4(auStack_4c8), 9999 < iVar7)) {
        if (local_480._4_4_ != (int)local_480) {
          local_480 = CONCAT44((int)local_480,(int)local_480);
          FUN_100146860(local_488);
        }
        FUN_1001afdb8(auStack_4c8);
      }
      FUN_1001436bc(&local_2f0);
    }
    FUN_1006cf614(&local_448);
    if (local_340 != (long *)0x0) {
      (**(code **)*local_340)();
    }
    plVar11 = local_320;
    FUN_10044cb5c(&local_518,L"done",4);
    FUN_10044cb5c(&local_4e0,&DAT_100d23e54,2);
    (**(code **)(*plVar11 + 0x28))(plVar11,&local_518,&local_4e0);
    if ((local_4e0 != (void **)0x0) &&
       (iVar7 = *(int *)local_4e0, *(int *)local_4e0 = iVar7 + -1, iVar7 + -1 == 0)) {
      FUN_100469e84();
    }
    if ((local_518 != (undefined ***)0x0) &&
       (iVar7 = *(int *)local_518, *(int *)local_518 = iVar7 + -1, iVar7 + -1 == 0)) {
      FUN_100469e84();
    }
    if ((local_498 != 0) &&
       (iVar7 = *(int *)(local_498 + 8) + -1, *(int *)(local_498 + 8) = iVar7, iVar7 == 0)) {
      FUN_1002abea8();
    }
    FUN_100152fbc(&local_2f0);
    FUN_100153344(&local_448);
    pvVar4 = local_370;
    puVar5 = local_360;
    while (puVar5 != (void *)0x0) {
      pvVar17 = (void *)*puVar5;
      local_370 = pvVar4;
      operator_delete(puVar5);
      pvVar4 = local_370;
      puVar5 = pvVar17;
    }
    local_370 = (void *)0x0;
    if (pvVar4 != (void *)0x0) {
      operator_delete(pvVar4);
    }
    if ((local_380 != 0) &&
       (iVar7 = *(int *)(local_380 + 8) + -1, *(int *)(local_380 + 8) = iVar7, iVar7 == 0)) {
      FUN_1002abea8();
    }
    if ((local_348 != 0) &&
       (iVar7 = *(int *)(local_348 + 8) + -1, *(int *)(local_348 + 8) = iVar7, iVar7 == 0)) {
      FUN_1002abea8();
    }
    if ((local_320 != (long *)0x0) &&
       (iVar7 = (int)local_320[1] + -1, *(int *)(local_320 + 1) = iVar7, iVar7 == 0)) {
      FUN_1002abea8();
    }
    plVar11 = local_310;
    local_310 = (long *)0x0;
    if (plVar11 != (long *)0x0) {
      (**(code **)(*plVar11 + 8))();
    }
    if (((local_308 != (long *)0x0) &&
        ((**(code **)(*local_308 + 0x18))(), local_308 != (long *)0x0)) &&
       (iVar7 = (int)local_308[1] + -1, *(int *)(local_308 + 1) = iVar7, iVar7 == 0)) {
      FUN_1002abea8();
    }
    uVar10 = 0;
    ppuVar12 = local_2f8;
    if (local_2f8 == (undefined **)0x0) goto LAB_100133794;
  }
  iVar7 = *(int *)(ppuVar12 + 1);
  *(int *)(ppuVar12 + 1) = iVar7 + -1;
  if (iVar7 + -1 == 0) {
    FUN_1002abea8(ppuVar12);
  }
LAB_100133794:
  if (*(long *)PTR____stack_chk_guard_100d60390 != local_78) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return uVar10;
}

