
/* WARNING: Removing unreachable block (ram,0x000100131878) */
/* WARNING: Removing unreachable block (ram,0x00010013238c) */
/* WARNING: Removing unreachable block (ram,0x000100131d24) */
/* WARNING: Removing unreachable block (ram,0x000100131cdc) */
/* WARNING: Removing unreachable block (ram,0x00010013170c) */
/* WARNING: Removing unreachable block (ram,0x0001001312b4) */
/* WARNING: Removing unreachable block (ram,0x000100131288) */
/* WARNING: Removing unreachable block (ram,0x000100130ff0) */
/* WARNING: Removing unreachable block (ram,0x000100130f98) */
/* WARNING: Removing unreachable block (ram,0x000100130ef8) */
/* WARNING: Removing unreachable block (ram,0x000100130ea0) */
/* WARNING: Removing unreachable block (ram,0x000100130dc0) */
/* WARNING: Removing unreachable block (ram,0x000100130d2c) */
/* WARNING: Removing unreachable block (ram,0x000100130d60) */
/* WARNING: Removing unreachable block (ram,0x000100130df8) */
/* WARNING: Removing unreachable block (ram,0x000100130ec0) */
/* WARNING: Removing unreachable block (ram,0x000100130fb8) */
/* WARNING: Removing unreachable block (ram,0x000100131298) */
/* WARNING: Removing unreachable block (ram,0x0001001312a4) */
/* WARNING: Removing unreachable block (ram,0x000100131904) */
/* WARNING: Removing unreachable block (ram,0x0001001319dc) */
/* WARNING: Removing unreachable block (ram,0x000100131b84) */
/* WARNING: Removing unreachable block (ram,0x000100131e90) */
/* WARNING: Removing unreachable block (ram,0x000100132400) */
/* WARNING: Removing unreachable block (ram,0x0001001318b8) */
/* WARNING: Removing unreachable block (ram,0x000100131e08) */
/* WARNING: Removing unreachable block (ram,0x000100131a34) */
/* WARNING: Removing unreachable block (ram,0x000100131dc0) */
/* WARNING: Removing unreachable block (ram,0x000100131254) */
/* WARNING: Type propagation algorithm not settling */

undefined8 entry(undefined8 param_1,undefined8 param_2)

{
  size_t sVar1;
  ulong uVar2;
  long *plVar3;
  undefined **ppuVar4;
  undefined **ppuVar5;
  code *pcVar6;
  int iVar7;
  uint uVar8;
  uint uVar9;
  undefined8 uVar10;
  undefined8 *puVar11;
  undefined8 uVar12;
  undefined1 *puVar13;
  undefined *puVar14;
  undefined ********ppppppppuVar15;
  int *piVar16;
  undefined ******ppppppuVar17;
  long lVar18;
  char cVar19;
  undefined4 uVar20;
  undefined *******pppppppuVar21;
  long *plVar22;
  void *pvVar23;
  long *plVar24;
  void *local_5a0 [2];
  char local_589;
  void *local_588 [2];
  char local_571;
  undefined1 auStack_570 [8];
  long *local_568;
  undefined8 local_560;
  char acStack_558 [8];
  undefined2 local_550;
  char local_549;
  undefined1 auStack_548 [8];
  undefined5 local_540;
  undefined3 uStack_53b;
  char acStack_538 [5];
  char cStack_533;
  undefined2 uStack_532;
  char acStack_530 [5];
  undefined1 local_52b;
  char local_529;
  long *local_528;
  undefined1 local_4d0 [24];
  char local_4b8;
  undefined1 auStack_4b0 [104];
  undefined1 auStack_448 [104];
  undefined1 auStack_3e0 [360];
  undefined1 auStack_278 [360];
  undefined **local_110;
  undefined **local_108;
  undefined8 local_100;
  undefined ********local_f0;
  undefined *******pppppppuStack_e8;
  undefined8 local_e0;
  undefined8 local_d8;
  undefined1 auStack_c8 [8];
  undefined8 local_c0;
  undefined1 auStack_b0 [8];
  undefined8 local_a8;
  void *local_98;
  void *local_90;
  undefined8 local_80;
  undefined *******pppppppuStack_78;
  undefined8 local_70;
  long local_68;
  
  uVar20 = DAT_1009ad578;
  local_68 = *(long *)PTR____stack_chk_guard_100b1c378;
  thunk_FUN_1001a0e00(auStack_278,"Ableton","PluginScanner","12.4.3","1.0",1,DAT_1009ad578);
  FUN_1001a1c30(auStack_278);
  thunk_FUN_1001a0e00(auStack_3e0,"Ableton","Live","12.4.3","12.0",1,uVar20);
  FUN_1001c5f38(auStack_3e0);
  uVar9 = DAT_1009aa3f0;
  local_529 = '\x15';
  acStack_538[0] = s_PluginScanner_options_100a1067b[8];
  acStack_538[1] = s_PluginScanner_options_100a1067b[9];
  acStack_538[2] = s_PluginScanner_options_100a1067b[10];
  acStack_538[3] = s_PluginScanner_options_100a1067b[0xb];
  acStack_538[4] = s_PluginScanner_options_100a1067b[0xc];
  local_540 = (undefined5)s_PluginScanner_options_100a1067b._0_8_;
  uStack_53b = SUB83(s_PluginScanner_options_100a1067b._0_8_,5);
  cStack_533 = (char)s_PluginScanner_options_100a1067b._13_3_;
  uStack_532 = SUB32(s_PluginScanner_options_100a1067b._13_3_,1);
  acStack_530[0] = s_PluginScanner_options_100a1067b[0x10];
  acStack_530[1] = s_PluginScanner_options_100a1067b[0x11];
  acStack_530[2] = s_PluginScanner_options_100a1067b[0x12];
  acStack_530[3] = s_PluginScanner_options_100a1067b[0x13];
  acStack_530[4] = s_PluginScanner_options_100a1067b[0x14];
  local_52b = 0;
  uVar8 = DAT_1009aa3f0 >> 1;
  FUN_10015f6fc(auStack_448,&local_540,DAT_1009aa3f0,uVar8);
  if (local_529 < '\0') {
    operator_delete((void *)CONCAT35(uStack_53b,local_540));
  }
  uVar10 = FUN_10015fa30(auStack_448);
  local_540 = (undefined5)uVar10;
  uStack_53b = (undefined3)((ulong)uVar10 >> 0x28);
  uVar10 = FUN_10015efb8(&local_540,"help,h","this help");
  puVar11 = operator_new(0x98);
  *puVar11 = &PTR_FUN_100b43d50;
  puVar11[1] = &PTR_FUN_100b43dc0;
  puVar11[0xf] = 0;
  puVar11[3] = 0;
  puVar11[2] = 0;
  puVar11[5] = 0;
  puVar11[4] = 0;
  puVar11[7] = 0;
  puVar11[6] = 0;
  puVar11[9] = 0;
  puVar11[8] = 0;
  puVar11[0xb] = 0;
  puVar11[10] = 0;
  puVar11[0xd] = 0;
  puVar11[0xc] = 0;
  *(undefined8 *)((long)puVar11 + 0x6d) = 0;
  uVar10 = FUN_10015f490(uVar10,"cid",puVar11,"communication channel id");
  puVar11 = operator_new(0x98);
  *puVar11 = &PTR_FUN_100b43d50;
  puVar11[1] = &PTR_FUN_100b43dc0;
  puVar11[0xf] = 0;
  puVar11[3] = 0;
  puVar11[2] = 0;
  puVar11[5] = 0;
  puVar11[4] = 0;
  puVar11[7] = 0;
  puVar11[6] = 0;
  puVar11[9] = 0;
  puVar11[8] = 0;
  puVar11[0xb] = 0;
  puVar11[10] = 0;
  puVar11[0xd] = 0;
  puVar11[0xc] = 0;
  *(undefined8 *)((long)puVar11 + 0x6d) = 0;
  uVar10 = FUN_10015f490(uVar10,"db,d",puVar11,"path to database");
  puVar11 = operator_new(0x98);
  *puVar11 = &PTR_FUN_100b43d50;
  puVar11[1] = &PTR_FUN_100b43dc0;
  puVar11[0xf] = 0;
  puVar11[3] = 0;
  puVar11[2] = 0;
  puVar11[5] = 0;
  puVar11[4] = 0;
  puVar11[7] = 0;
  puVar11[6] = 0;
  puVar11[9] = 0;
  puVar11[8] = 0;
  puVar11[0xb] = 0;
  puVar11[10] = 0;
  puVar11[0xd] = 0;
  puVar11[0xc] = 0;
  *(undefined8 *)((long)puVar11 + 0x6d) = 0;
  uVar10 = FUN_10015f490(uVar10,"vst3",puVar11,"paths to scan for vst3 plugins");
  puVar11 = operator_new(0x98);
  *puVar11 = &PTR_FUN_100b43d50;
  puVar11[1] = &PTR_FUN_100b43dc0;
  puVar11[0xf] = 0;
  puVar11[3] = 0;
  puVar11[2] = 0;
  puVar11[5] = 0;
  puVar11[4] = 0;
  puVar11[7] = 0;
  puVar11[6] = 0;
  puVar11[9] = 0;
  puVar11[8] = 0;
  puVar11[0xb] = 0;
  puVar11[10] = 0;
  puVar11[0xd] = 0;
  puVar11[0xc] = 0;
  *(undefined8 *)((long)puVar11 + 0x6d) = 0;
  uVar10 = FUN_10015f490(uVar10,"vst2",puVar11,"paths to scan for vst2 plugins");
  puVar11 = operator_new(0x98);
  *puVar11 = &PTR_FUN_100b43d50;
  puVar11[1] = &PTR_FUN_100b43dc0;
  puVar11[0xf] = 0;
  puVar11[3] = 0;
  puVar11[2] = 0;
  puVar11[5] = 0;
  puVar11[4] = 0;
  puVar11[7] = 0;
  puVar11[6] = 0;
  puVar11[9] = 0;
  puVar11[8] = 0;
  puVar11[0xb] = 0;
  puVar11[10] = 0;
  puVar11[0xd] = 0;
  puVar11[0xc] = 0;
  *(undefined8 *)((long)puVar11 + 0x6d) = 0;
  uVar10 = FUN_10015f490(uVar10,"reset",puVar11,
                         "reset plugin data before scanning. Possible values: \'all\', \'vst2\', \'vst3\'"
                        );
  puVar11 = operator_new(0x98);
  *puVar11 = &PTR_FUN_100b43d50;
  puVar11[1] = &PTR_FUN_100b43dc0;
  puVar11[0xf] = 0;
  puVar11[3] = 0;
  puVar11[2] = 0;
  puVar11[5] = 0;
  puVar11[4] = 0;
  puVar11[7] = 0;
  puVar11[6] = 0;
  puVar11[9] = 0;
  puVar11[8] = 0;
  puVar11[0xb] = 0;
  puVar11[10] = 0;
  puVar11[0xd] = 0;
  puVar11[0xc] = 0;
  *(undefined8 *)((long)puVar11 + 0x6d) = 0;
  uVar10 = FUN_10015f490(uVar10,"lang,l",puVar11,"language to use; defaults to \'EN\'");
  puVar11 = operator_new(0x98);
  *puVar11 = &PTR_FUN_100b43e30;
  puVar11[1] = &PTR_FUN_100b43ea0;
  puVar11[0xf] = 0;
  puVar11[3] = 0;
  puVar11[2] = 0;
  puVar11[5] = 0;
  puVar11[4] = 0;
  puVar11[7] = 0;
  puVar11[6] = 0;
  puVar11[9] = 0;
  puVar11[8] = 0;
  puVar11[0xb] = 0;
  puVar11[10] = 0;
  puVar11[0xd] = 0;
  puVar11[0xc] = 0;
  *(undefined8 *)((long)puVar11 + 0x6d) = 0;
  uVar10 = FUN_10015f490(uVar10,"limit,N",puVar11,"limit to check N candidates in one session");
  uVar12 = FUN_100165308();
  FUN_10015f490(uVar10,"verbose,v",uVar12,"verbose output");
  local_529 = '\r';
  local_540._0_1_ = s_Valid_options_100a107dd[0];
  local_540._1_1_ = s_Valid_options_100a107dd[1];
  local_540._2_1_ = s_Valid_options_100a107dd[2];
  local_540._3_1_ = s_Valid_options_100a107dd[3];
  local_540._4_1_ = s_Valid_options_100a107dd[4];
  uStack_53b._0_1_ = s_Valid_options_100a107dd[5];
  uStack_53b._1_1_ = s_Valid_options_100a107dd[6];
  uStack_53b._2_1_ = s_Valid_options_100a107dd[7];
  acStack_538[0] = s_Valid_options_100a107dd[8];
  acStack_538[1] = s_Valid_options_100a107dd[9];
  acStack_538[2] = s_Valid_options_100a107dd[10];
  acStack_538[3] = s_Valid_options_100a107dd[0xb];
  acStack_538[4] = s_Valid_options_100a107dd[0xc];
  cStack_533 = 0;
  FUN_10015f6fc(auStack_4b0,&local_540,uVar9,uVar8);
  if (local_529 < '\0') {
    operator_delete((void *)CONCAT35(uStack_53b,local_540));
  }
  FUN_10015f768(auStack_4b0,auStack_448);
  FUN_1001903a4(&local_540,0);
  FUN_10015f768(auStack_4b0,&local_540);
  FUN_100134fdc(&local_540);
  FUN_100192a58(&local_110,param_1,param_2);
  local_80 = (undefined **)0x0;
  pppppppuStack_78 = (undefined *******)0x0;
  local_70 = 0;
  FUN_100192a88(&local_f0,&local_110,auStack_4b0,0,&local_80);
  FUN_1001352c0(&local_540,&local_f0);
  local_4d0[0] = 0;
  local_4b8 = '\0';
  if (local_98 != (void *)0x0) {
    for (; local_90 != local_98; local_90 = (void *)((long)local_90 + -0x30)) {
    }
    local_90 = local_98;
    operator_delete(local_98);
  }
  local_f0 = (undefined ********)&PTR_FUN_100b46480;
  FUN_1001369c4(auStack_b0,local_a8);
  FUN_10013637c(auStack_c8,local_c0);
  FUN_100135da4(&local_e0,local_d8);
  if (local_110 != (undefined **)0x0) {
    for (; local_108 != local_110; local_108 = local_108 + -3) {
    }
    local_108 = local_110;
    operator_delete(local_110);
  }
  FUN_10019efa4();
  FUN_100188cac();
  FUN_100184120(auStack_548);
  FUN_10020b0ec(&local_f0,param_1,param_2);
  local_70 = CONCAT17(0x10,(undefined7)local_70);
  pppppppuStack_78 = (undefined *******)s_AppPluginScanner_100a107eb._8_8_;
  local_80._0_1_ = s_AppPluginScanner_100a107eb[0];
  local_80._1_1_ = s_AppPluginScanner_100a107eb[1];
  local_80._2_1_ = s_AppPluginScanner_100a107eb[2];
  local_80._3_1_ = s_AppPluginScanner_100a107eb[3];
  local_80._4_1_ = s_AppPluginScanner_100a107eb[4];
  local_80._5_1_ = s_AppPluginScanner_100a107eb[5];
  local_80._6_1_ = s_AppPluginScanner_100a107eb[6];
  local_80._7_1_ = s_AppPluginScanner_100a107eb[7];
  local_70 = local_70 & 0xffffffffffffff00;
  FUN_100136c80(&local_110,&local_80,1);
  FUN_100190720(&local_f0,1,0,&local_110);
  if (local_110 != (undefined **)0x0) {
    for (; local_108 != local_110; local_108 = local_108 + -3) {
    }
    local_108 = local_110;
    operator_delete(local_110);
  }
  if (local_f0 != (undefined ********)0x0) {
    for (; (undefined ********)pppppppuStack_e8 != local_f0;
        pppppppuStack_e8 = pppppppuStack_e8 + -3) {
    }
    pppppppuStack_e8 = (undefined *******)local_f0;
    operator_delete(local_f0);
  }
  FUN_100189b98();
  FUN_10023fda0(FUN_10020b310);
  FUN_10020b0ec(&local_f0,param_1,param_2);
  FUN_1001c5f40(&local_80);
  local_549 = '\x11';
  local_550 = 0x74;
  acStack_558[0] = s_PluginScanner_txt_100a107fc[8];
  acStack_558[1] = s_PluginScanner_txt_100a107fc[9];
  acStack_558[2] = s_PluginScanner_txt_100a107fc[10];
  acStack_558[3] = s_PluginScanner_txt_100a107fc[0xb];
  acStack_558[4] = s_PluginScanner_txt_100a107fc[0xc];
  acStack_558[5] = s_PluginScanner_txt_100a107fc[0xd];
  acStack_558[6] = s_PluginScanner_txt_100a107fc[0xe];
  acStack_558[7] = s_PluginScanner_txt_100a107fc[0xf];
  local_560 = (undefined **)s_PluginScanner_txt_100a107fc._0_8_;
  FUN_10019ab30(&local_110,&local_80,&local_560);
  FUN_10019a9d8(&local_f0,&local_110);
  if (local_549 < '\0') {
    operator_delete(local_560);
  }
  if (local_f0 != (undefined ********)0x0) {
    for (; (undefined ********)pppppppuStack_e8 != local_f0;
        pppppppuStack_e8 = pppppppuStack_e8 + -3) {
    }
    pppppppuStack_e8 = (undefined *******)local_f0;
    operator_delete(local_f0);
  }
  local_e0 = CONCAT17(4,(undefined7)local_e0);
  local_f0 = (undefined ********)CONCAT35(local_f0._5_3_,0x72726563);
  local_560 = (undefined **)CONCAT44(local_560._4_4_,7);
  local_70 = CONCAT17(6,(undefined7)local_70);
  local_80 = (undefined **)CONCAT17(local_80._7_1_,0x7625203a6c25);
  local_108 = (undefined **)0x0;
  local_100 = (undefined **)0x0;
  local_110 = (undefined **)0x0;
  local_110 = operator_new(0x78);
  local_100 = local_110 + 0xf;
  *(undefined4 *)local_110 = 2;
  *(undefined1 *)(local_110 + 1) = 1;
  *(undefined4 *)(local_110 + 4) = 0;
  local_108 = local_110 + 5;
  FUN_10013cd58(&local_110,4,2,&local_560,&local_80);
  FUN_1006a0ff4(&local_f0,&local_110);
  ppuVar5 = local_110;
  ppuVar4 = local_108;
  if (local_110 != (undefined **)0x0) {
    for (; ppuVar4 != ppuVar5; ppuVar4 = ppuVar4 + -5) {
      if (*(uint *)(ppuVar4 + -1) != 0xffffffff) {
        (*(code *)(&PTR_FUN_100b437e8)[*(uint *)(ppuVar4 + -1)])(local_588,ppuVar4 + -4);
      }
      *(undefined4 *)(ppuVar4 + -1) = 0xffffffff;
    }
    local_108 = ppuVar5;
    operator_delete(local_110);
  }
  local_e0 = CONCAT17(4,(undefined7)local_e0);
  local_f0 = (undefined ********)CONCAT35(local_f0._5_3_,0x74756f63);
  local_560 = (undefined **)CONCAT44(local_560._4_4_,7);
  local_70 = CONCAT17(2,(undefined7)local_70);
  local_80 = (undefined **)CONCAT53(local_80._3_5_,0x7625);
  local_108 = (undefined **)0x0;
  local_100 = (undefined **)0x0;
  local_110 = (undefined **)0x0;
  local_110 = operator_new(0x78);
  local_100 = local_110 + 0xf;
  *(undefined4 *)local_110 = 1;
  *(undefined1 *)(local_110 + 1) = 1;
  *(undefined4 *)(local_110 + 4) = 0;
  local_108 = local_110 + 5;
  FUN_10013cd58(&local_110,4,2,&local_560,&local_80);
  FUN_1006a0ff4(&local_f0,&local_110);
  ppuVar5 = local_110;
  ppuVar4 = local_108;
  if (local_110 != (undefined **)0x0) {
    for (; ppuVar4 != ppuVar5; ppuVar4 = ppuVar4 + -5) {
      if (*(uint *)(ppuVar4 + -1) != 0xffffffff) {
        (*(code *)(&PTR_FUN_100b437e8)[*(uint *)(ppuVar4 + -1)])(local_588,ppuVar4 + -4);
      }
      *(undefined4 *)(ppuVar4 + -1) = 0xffffffff;
    }
    local_108 = ppuVar5;
    operator_delete(local_110);
  }
  plVar22 = local_528;
  if (local_4b8 == '\x01') {
    local_e0 = CONCAT17(4,(undefined7)local_e0);
    local_f0 = (undefined ********)CONCAT35(local_f0._5_3_,0x72726563);
    uVar10 = std::chrono::system_clock::now();
    FUN_1006a284c(&local_110,4,&local_f0,uVar10);
    iVar7 = FUN_10069f1d8(&local_110);
    if (iVar7 != 0) {
      FUN_10069d278(&local_110,local_4d0);
    }
    thunk_FUN_10069bf04(&local_110);
    puVar13 = auStack_448;
  }
  else {
    local_e0 = CONCAT17(4,(undefined7)local_e0);
    local_f0 = (undefined ********)CONCAT35(local_f0._5_3_,0x706c6568);
    plVar24 = local_528;
    if (local_528 != (long *)0x0) {
      do {
        uVar2 = plVar24[5];
        plVar3 = (long *)plVar24[4];
        if (-1 < (char)*(byte *)((long)plVar24 + 0x37)) {
          uVar2 = (ulong)*(byte *)((long)plVar24 + 0x37);
          plVar3 = plVar24 + 4;
        }
        sVar1 = uVar2;
        if (3 < uVar2) {
          sVar1 = 4;
        }
        iVar7 = _memcmp(&local_f0,plVar3,sVar1);
        if (iVar7 == 0) {
          if (uVar2 < 5) goto LAB_10013135c;
        }
        else if (-1 < iVar7) {
LAB_10013135c:
          iVar7 = _memcmp(plVar3,&local_f0,sVar1);
          if (iVar7 == 0) {
            if (3 < uVar2) goto LAB_1001314ec;
          }
          else if (-1 < iVar7) goto LAB_1001314ec;
          plVar24 = plVar24 + 1;
        }
        plVar24 = (long *)*plVar24;
      } while (plVar24 != (long *)0x0);
      local_e0 = CONCAT17(4,(undefined7)local_e0);
      local_f0 = (undefined ********)CONCAT35(local_f0._5_3_,0x33747376);
      plVar24 = plVar22;
      if (plVar22 != (long *)0x0) {
        do {
          uVar2 = plVar24[5];
          plVar3 = (long *)plVar24[4];
          if (-1 < (char)*(byte *)((long)plVar24 + 0x37)) {
            uVar2 = (ulong)*(byte *)((long)plVar24 + 0x37);
            plVar3 = plVar24 + 4;
          }
          sVar1 = uVar2;
          if (3 < uVar2) {
            sVar1 = 4;
          }
          iVar7 = _memcmp(&local_f0,plVar3,sVar1);
          if (iVar7 == 0) {
            if (uVar2 < 5) goto LAB_100131400;
          }
          else if (-1 < iVar7) {
LAB_100131400:
            iVar7 = _memcmp(plVar3,&local_f0,sVar1);
            if (iVar7 == 0) {
              if (3 < uVar2) goto LAB_1001314bc;
            }
            else if (-1 < iVar7) goto LAB_1001314bc;
            plVar24 = plVar24 + 1;
          }
          plVar24 = (long *)*plVar24;
        } while (plVar24 != (long *)0x0);
        local_100 = (undefined **)CONCAT17(4,(undefined7)local_100);
        local_110 = (undefined **)CONCAT35(local_110._5_3_,0x32747376);
        for (plVar24 = plVar22; plVar24 != (long *)0x0; plVar24 = (long *)*plVar24) {
          uVar2 = plVar24[5];
          puVar11 = (void *)plVar24[4];
          if (-1 < (char)*(byte *)((long)plVar24 + 0x37)) {
            uVar2 = (ulong)*(byte *)((long)plVar24 + 0x37);
            puVar11 = plVar24 + 4;
          }
          sVar1 = uVar2;
          if (3 < uVar2) {
            sVar1 = 4;
          }
          iVar7 = _memcmp(&local_110,puVar11,sVar1);
          if (iVar7 == 0) {
            if (uVar2 < 5) goto LAB_1001314a4;
          }
          else if (-1 < iVar7) {
LAB_1001314a4:
            iVar7 = _memcmp(puVar11,&local_110,sVar1);
            if (iVar7 == 0) {
              if (3 < uVar2) goto LAB_1001314bc;
            }
            else if (-1 < iVar7) goto LAB_1001314bc;
            plVar24 = plVar24 + 1;
          }
        }
      }
    }
LAB_1001314ec:
    puVar13 = auStack_4b0;
  }
  FUN_100132bd4(puVar13);
  uVar10 = 1;
  goto LAB_1001314f8;
LAB_1001314bc:
  local_e0 = CONCAT17(7,(undefined7)local_e0);
  local_f0 = (undefined ********)0x65736f62726576;
  for (; plVar22 != (long *)0x0; plVar22 = (long *)*plVar22) {
    uVar2 = plVar22[5];
    puVar11 = (void *)plVar22[4];
    if (-1 < (char)*(byte *)((long)plVar22 + 0x37)) {
      uVar2 = (ulong)*(byte *)((long)plVar22 + 0x37);
      puVar11 = plVar22 + 4;
    }
    sVar1 = uVar2;
    if (6 < uVar2) {
      sVar1 = 7;
    }
    iVar7 = _memcmp(&local_f0,puVar11,sVar1);
    if (iVar7 == 0) {
      if (uVar2 < 8) goto LAB_1001315c4;
    }
    else if (-1 < iVar7) {
LAB_1001315c4:
      iVar7 = _memcmp(puVar11,&local_f0,sVar1);
      if (iVar7 == 0) {
        if (uVar2 < 7) goto LAB_10013156c;
      }
      else if (iVar7 < 0) {
LAB_10013156c:
        plVar22 = plVar22 + 1;
        goto LAB_100131570;
      }
      local_100 = (undefined **)CONCAT17(7,(undefined7)local_100);
      local_110 = (undefined **)0x65736f62726576;
      plVar22 = (long *)FUN_10016bf7c(&local_540,&local_110);
      puVar14 = PTR_typeinfo_100b1c300;
      if ((long *)*plVar22 != (long *)0x0) {
        puVar14 = (undefined *)(**(code **)(*(long *)*plVar22 + 0x10))();
      }
      if (((char *)(*(ulong *)(puVar14 + 8) & 0x7fffffffffffffff) !=
           (char *)(*(ulong *)(PTR_typeinfo_100b1c2e0 + 8) & 0x7fffffffffffffff)) &&
         (iVar7 = _strcmp((char *)(*(ulong *)(puVar14 + 8) & 0x7fffffffffffffff),
                          (char *)(*(ulong *)(PTR_typeinfo_100b1c2e0 + 8) & 0x7fffffffffffffff)),
         iVar7 != 0)) {
        local_80 = (undefined **)0x0;
        std::bad_cast::bad_cast((bad_cast *)&local_80);
        local_80 = &PTR__bad_cast_100b43d08;
        FUN_100138a40();
        goto LAB_100131f3c;
      }
      cVar19 = *(char *)(*plVar22 + 8);
      goto LAB_10013162c;
    }
LAB_100131570:
  }
  local_560._4_4_ = (undefined4)((ulong)local_560 >> 0x20);
  local_80._4_4_ = (undefined4)((ulong)local_80 >> 0x20);
  cVar19 = '\0';
LAB_10013162c:
  local_e0 = CONCAT17(8,(undefined7)local_e0);
  local_f0 = (undefined ********)&DAT_6e61637367756c70;
  pppppppuStack_e8 = (undefined *******)((ulong)pppppppuStack_e8 & 0xffffffffffffff00);
  local_80 = (undefined **)CONCAT44(local_80._4_4_,4);
  local_560 = (undefined **)CONCAT44(local_560._4_4_,2);
  local_108 = (undefined **)0x0;
  local_100 = (undefined **)0x0;
  local_110 = (undefined **)0x0;
  local_110 = operator_new(0x50);
  local_100 = local_110 + 10;
  local_108 = local_110;
  FUN_10013d0f0(&local_110,1,cVar19,&local_80,&local_560);
  FUN_1006a0ff4(&local_f0,&local_110);
  ppuVar5 = local_110;
  ppuVar4 = local_108;
  if (local_110 != (undefined **)0x0) {
    for (; ppuVar4 != ppuVar5; ppuVar4 = ppuVar4 + -5) {
      if (*(uint *)(ppuVar4 + -1) != 0xffffffff) {
        (*(code *)(&PTR_FUN_100b437e8)[*(uint *)(ppuVar4 + -1)])(local_588,ppuVar4 + -4);
      }
      *(undefined4 *)(ppuVar4 + -1) = 0xffffffff;
    }
    local_108 = ppuVar5;
    operator_delete(local_110);
  }
  uVar10 = FUN_10016c040(&local_f0);
  FUN_10020c0c4(uVar10,0);
  local_f0 = (undefined ********)&PTR_FUN_100b46480;
  FUN_1001369c4(auStack_b0,local_a8);
  FUN_10013637c(auStack_c8,local_c0);
  FUN_100135da4(&local_e0,local_d8);
  FUN_1004af53c(0);
  thunk_FUN_1005eade0();
  local_e0 = CONCAT17(2,(undefined7)local_e0);
  local_f0 = (undefined ********)CONCAT53(local_f0._3_5_,0x6264);
  for (plVar22 = local_528; plVar22 != (long *)0x0; plVar22 = (long *)*plVar22) {
    uVar2 = plVar22[5];
    puVar11 = (void *)plVar22[4];
    if (-1 < (char)*(byte *)((long)plVar22 + 0x37)) {
      uVar2 = (ulong)*(byte *)((long)plVar22 + 0x37);
      puVar11 = plVar22 + 4;
    }
    sVar1 = uVar2;
    if (1 < uVar2) {
      sVar1 = 2;
    }
    iVar7 = _memcmp(&local_f0,puVar11,sVar1);
    if (iVar7 == 0) {
      if (uVar2 < 3) goto LAB_1001317ec;
    }
    else if (-1 < iVar7) {
LAB_1001317ec:
      iVar7 = _memcmp(puVar11,&local_f0,sVar1);
      if (iVar7 == 0) {
        if (uVar2 < 2) goto LAB_100131794;
      }
      else if (iVar7 < 0) {
LAB_100131794:
        plVar22 = plVar22 + 1;
        goto LAB_100131798;
      }
      local_100 = (undefined **)CONCAT17(2,(undefined7)local_100);
      local_110 = (undefined **)CONCAT53(local_110._3_5_,0x6264);
      plVar22 = (long *)FUN_10016bf7c(&local_540,&local_110);
      puVar14 = PTR_typeinfo_100b1c300;
      if ((long *)*plVar22 != (long *)0x0) {
        puVar14 = (undefined *)(**(code **)(*(long *)*plVar22 + 0x10))();
      }
      if (((char *)(*(ulong *)(puVar14 + 8) & 0x7fffffffffffffff) !=
           "NSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEE") &&
         (iVar7 = _strcmp((char *)(*(ulong *)(puVar14 + 8) & 0x7fffffffffffffff),
                          "NSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEE"),
         iVar7 != 0)) {
        local_f0 = (undefined ********)0x0;
        std::bad_cast::bad_cast((bad_cast *)&local_f0);
        local_f0 = (undefined ********)&PTR__bad_cast_100b43d08;
        FUN_100138a40();
        goto LAB_100131f3c;
      }
      lVar18 = *plVar22;
      pppppppuVar21 = (undefined *******)(long)*(char *)(lVar18 + 0x1f);
      if ((long)pppppppuVar21 < 0) {
        pppppppuVar21 = *(undefined ********)(lVar18 + 0x10);
        if ((undefined *******)0x7ffffffffffffff7 < pppppppuVar21) {
                    /* WARNING: Subroutine does not return */
          FUN_100134f2c(&local_f0);
        }
        pvVar23 = *(void **)(lVar18 + 8);
      }
      else {
        pvVar23 = (void *)(lVar18 + 8);
      }
      if (pppppppuVar21 < (undefined *******)0x17) {
        local_e0 = CONCAT17((char)pppppppuVar21,(undefined7)local_e0);
        ppppppppuVar15 = (undefined ********)&local_f0;
        if (pppppppuVar21 != (undefined *******)0x0) goto LAB_1001319b0;
      }
      else {
        uVar2 = 0x19;
        if (((ulong)pppppppuVar21 | 7) != 0x17) {
          uVar2 = ((ulong)pppppppuVar21 | 7) + 1;
        }
        ppppppppuVar15 = operator_new(uVar2);
        local_e0 = uVar2 | 0x8000000000000000;
        local_f0 = ppppppppuVar15;
        pppppppuStack_e8 = pppppppuVar21;
LAB_1001319b0:
        _memmove(ppppppppuVar15,pvVar23,(size_t)pppppppuVar21);
      }
      *(undefined1 *)((long)ppppppppuVar15 + (long)pppppppuVar21) = 0;
      pppppppuStack_78 = pppppppuStack_e8;
      local_80 = (undefined **)local_f0;
      local_70 = local_e0;
      pppppppuVar21 = pppppppuStack_e8;
      if (-1 < (long)local_e0) {
        pppppppuVar21 = (undefined *******)(local_e0 >> 0x38);
      }
      if (pppppppuVar21 == (undefined *******)0x0) goto LAB_100131848;
      if (cVar19 != '\0') {
        local_e0 = CONCAT17(8,(undefined7)local_e0);
        local_f0 = (undefined ********)&DAT_6e61637367756c70;
        pppppppuStack_e8 = (undefined *******)((ulong)pppppppuStack_e8 & 0xffffffffffffff00);
        uVar10 = std::chrono::system_clock::now();
        FUN_1006a284c(&local_110,2,&local_f0,uVar10);
        iVar7 = FUN_10069f1d8(&local_110);
        if (iVar7 != 0) {
          uVar10 = FUN_10069c398(&local_110,"Database: ");
          FUN_10013300c(uVar10,&local_80);
        }
        thunk_FUN_10069bf04(&local_110);
      }
      local_e0 = CONCAT17(5,(undefined7)local_e0);
      local_f0 = (undefined ********)CONCAT26(local_f0._6_2_,0x74696d696c);
      plVar22 = local_528;
      goto joined_r0x000100131a88;
    }
LAB_100131798:
  }
  pppppppuStack_78 = (undefined *******)0x0;
  local_70 = 0;
  local_80 = (undefined **)0x0;
LAB_100131848:
  local_e0 = CONCAT17(4,(undefined7)local_e0);
  local_f0 = (undefined ********)CONCAT35(local_f0._5_3_,0x72726563);
  uVar10 = std::chrono::system_clock::now();
  FUN_1006a284c(&local_110,4,&local_f0,uVar10);
  iVar7 = FUN_10069f1d8(&local_110);
  if (iVar7 != 0) {
    FUN_10069c398(&local_110,"No database path");
  }
  thunk_FUN_10069bf04(&local_110);
  FUN_100132bd4(auStack_448);
  uVar10 = 1;
  goto LAB_1001314f8;
joined_r0x000100131a88:
  if (plVar22 == (long *)0x0) goto LAB_100131b50;
  uVar2 = plVar22[5];
  puVar11 = (void *)plVar22[4];
  if (-1 < (char)*(byte *)((long)plVar22 + 0x37)) {
    uVar2 = (ulong)*(byte *)((long)plVar22 + 0x37);
    puVar11 = plVar22 + 4;
  }
  sVar1 = uVar2;
  if (4 < uVar2) {
    sVar1 = 5;
  }
  iVar7 = _memcmp(&local_f0,puVar11,sVar1);
  if (iVar7 == 0) {
    if (uVar2 < 6) goto LAB_100131af4;
  }
  else if (-1 < iVar7) {
LAB_100131af4:
    iVar7 = _memcmp(puVar11,&local_f0,sVar1);
    if (iVar7 == 0) {
      if (uVar2 < 5) goto LAB_100131a9c;
    }
    else if (iVar7 < 0) {
LAB_100131a9c:
      plVar22 = plVar22 + 1;
      goto LAB_100131aa0;
    }
    local_100 = (undefined **)CONCAT17(5,(undefined7)local_100);
    local_110 = (undefined **)CONCAT26(local_110._6_2_,0x74696d696c);
    plVar22 = (long *)FUN_10016bf7c(&local_540,&local_110);
    puVar14 = PTR_typeinfo_100b1c300;
    if ((long *)*plVar22 != (long *)0x0) {
      puVar14 = (undefined *)(**(code **)(*(long *)*plVar22 + 0x10))();
    }
    if (((char *)(*(ulong *)(puVar14 + 8) & 0x7fffffffffffffff) !=
         (char *)(*(ulong *)(PTR_typeinfo_100b1c2f8 + 8) & 0x7fffffffffffffff)) &&
       (iVar7 = _strcmp((char *)(*(ulong *)(puVar14 + 8) & 0x7fffffffffffffff),
                        (char *)(*(ulong *)(PTR_typeinfo_100b1c2f8 + 8) & 0x7fffffffffffffff)),
       iVar7 != 0)) {
      local_560 = (undefined **)0x0;
      std::bad_cast::bad_cast((bad_cast *)&local_560);
      local_560 = &PTR__bad_cast_100b43d08;
      FUN_100138a40(&local_560);
      goto LAB_100131f3c;
    }
    uVar20 = *(undefined4 *)(*plVar22 + 8);
    goto LAB_100131b54;
  }
LAB_100131aa0:
  plVar22 = (long *)*plVar22;
  goto joined_r0x000100131a88;
LAB_100131b50:
  uVar20 = 0x32;
LAB_100131b54:
  local_e0 = CONCAT17(8,(undefined7)local_e0);
  local_f0 = (undefined ********)&DAT_6e61637367756c70;
  pppppppuStack_e8 = (undefined *******)((ulong)pppppppuStack_e8 & 0xffffffffffffff00);
  uVar10 = std::chrono::system_clock::now();
  FUN_1006a284c(&local_110,2,&local_f0,uVar10);
  iVar7 = FUN_10069f1d8(&local_110);
  if (iVar7 != 0) {
    uVar10 = FUN_10069c398(&local_110,"Init: check for ");
    uVar10 = FUN_10069e0d0(uVar10,uVar20);
    FUN_10069c398(uVar10," plugin modules per architecture maximum");
  }
  thunk_FUN_10069bf04(&local_110);
  local_e0 = CONCAT17(3,(undefined7)local_e0);
  local_f0 = (undefined ********)CONCAT44(local_f0._4_4_,0x646963);
  for (plVar22 = local_528; plVar22 != (long *)0x0; plVar22 = (long *)*plVar22) {
    uVar2 = plVar22[5];
    puVar11 = (void *)plVar22[4];
    if (-1 < (char)*(byte *)((long)plVar22 + 0x37)) {
      uVar2 = (ulong)*(byte *)((long)plVar22 + 0x37);
      puVar11 = plVar22 + 4;
    }
    sVar1 = uVar2;
    if (2 < uVar2) {
      sVar1 = 3;
    }
    iVar7 = _memcmp(&local_f0,puVar11,sVar1);
    if (iVar7 == 0) {
      if (uVar2 < 4) goto LAB_100131c48;
    }
    else if (-1 < iVar7) {
LAB_100131c48:
      iVar7 = _memcmp(puVar11,&local_f0,sVar1);
      if (iVar7 == 0) {
        if (uVar2 < 3) goto LAB_100131bf0;
      }
      else if (iVar7 < 0) {
LAB_100131bf0:
        plVar22 = plVar22 + 1;
        goto LAB_100131bf4;
      }
      local_e0 = CONCAT17(3,(undefined7)local_e0);
      local_f0 = (undefined ********)CONCAT44(local_f0._4_4_,0x646963);
      plVar22 = (long *)FUN_10016bf7c(&local_540,&local_f0);
      puVar14 = PTR_typeinfo_100b1c300;
      if ((long *)*plVar22 != (long *)0x0) {
        puVar14 = (undefined *)(**(code **)(*(long *)*plVar22 + 0x10))();
      }
      if (((char *)(*(ulong *)(puVar14 + 8) & 0x7fffffffffffffff) !=
           "NSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEE") &&
         (iVar7 = _strcmp((char *)(*(ulong *)(puVar14 + 8) & 0x7fffffffffffffff),
                          "NSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEE"),
         iVar7 != 0)) {
        local_110 = (undefined **)0x0;
        std::bad_cast::bad_cast((bad_cast *)&local_110);
        local_110 = &PTR__bad_cast_100b43d08;
        FUN_100138a40();
LAB_100131f3c:
                    /* WARNING: Does not return */
        pcVar6 = (code *)SoftwareBreakpoint(1,0x100131f40);
        (*pcVar6)();
      }
      FUN_100134348(&local_568,*plVar22 + 8);
      plVar22 = local_568;
      if (local_568 != (long *)0x0) {
        (**(code **)(*local_568 + 0x20))(local_568);
        goto LAB_100131d64;
      }
      break;
    }
LAB_100131bf4:
  }
  plVar22 = operator_new(8);
  *plVar22 = (long)&PTR_FUN_100b44748;
  local_568 = plVar22;
LAB_100131d64:
  local_110 = (undefined **)((ulong)local_110 & 0xffffffff00000000);
  local_108 = (undefined **)std::system_category();
  plVar24 = operator_new(0x18);
  thunk_FUN_1005a30f8(plVar24,&local_80,&local_110);
  if ((int)local_110 == 0) {
    FUN_1001332fc(&local_f0,&local_540,"vst3");
    if (local_f0 == (undefined ********)pppppppuStack_e8) {
      uVar8 = 1;
    }
    else {
      FUN_100132a18(&local_110,"vst3");
      uVar10 = FUN_100133b9c(&local_540,&local_110);
      uVar8 = FUN_100133aa0(plVar22,plVar24,uVar10,&local_f0,uVar20);
    }
    FUN_1001332fc(&local_110,&local_540,"vst2");
    plVar22 = local_568;
    if (local_110 == local_108) {
joined_r0x0001001322ec:
      if ((uVar8 & 1) == 0) goto LAB_1001322f0;
LAB_100132144:
      FUN_100431940(&local_560,"scan");
      FUN_100431940(local_588,"done");
      (**(code **)(*plVar22 + 0x28))(plVar22,&local_560,local_588);
    }
    else {
      FUN_100132a18(&local_560,"vst2");
      uVar10 = FUN_100133b9c(&local_540,&local_560);
      FUN_100132a18(local_588,"lang");
      lVar18 = FUN_100132edc(acStack_530,local_588);
      if (lVar18 == 0) {
        FUN_100437728(auStack_570,&DAT_100ae84c0);
      }
      else {
        FUN_100132a18(local_5a0,"lang");
        FUN_10016bf7c(&local_540,local_5a0);
        FUN_100134164();
        FUN_10043ce2c(auStack_570);
      }
      uVar9 = FUN_100134018(plVar22,plVar24,uVar10,auStack_570,&local_110,uVar20);
      FUN_100133fc8(auStack_570);
      if ((lVar18 != 0) && (local_589 < '\0')) {
        operator_delete(local_5a0[0]);
      }
      if (local_571 < '\0') {
        operator_delete(local_588[0]);
      }
      if (local_549 < '\0') {
        uVar8 = uVar8 & uVar9;
        operator_delete(local_560);
        goto joined_r0x0001001322ec;
      }
      if ((uVar8 & uVar9 & 1) != 0) goto LAB_100132144;
LAB_1001322f0:
      FUN_100431940(&local_560,"scan");
      FUN_100431940(local_588,"interrupted");
      (**(code **)(*plVar22 + 0x28))(plVar22,&local_560,local_588);
    }
    FUN_100133fc8(local_588);
    FUN_100133fc8(&local_560);
    ppuVar5 = local_110;
    ppuVar4 = local_108;
    if (local_110 != (undefined **)0x0) {
      for (; ppuVar4 != ppuVar5; ppuVar4 = ppuVar4 + -4) {
        piVar16 = (int *)ppuVar4[-1];
        if ((piVar16 != (int *)0x0) && (iVar7 = *piVar16, *piVar16 = iVar7 + -1, iVar7 + -1 == 0)) {
          FUN_100454b40();
        }
      }
      local_108 = ppuVar5;
      operator_delete(local_110);
    }
    ppppppppuVar15 = local_f0;
    pppppppuVar21 = pppppppuStack_e8;
    if (local_f0 != (undefined ********)0x0) {
      for (; (undefined ********)pppppppuVar21 != ppppppppuVar15; pppppppuVar21 = pppppppuVar21 + -4
          ) {
        ppppppuVar17 = pppppppuVar21[-1];
        if ((ppppppuVar17 != (undefined ******)0x0) &&
           (iVar7 = *(int *)ppppppuVar17, *(int *)ppppppuVar17 = iVar7 + -1, iVar7 + -1 == 0)) {
          FUN_100454b40();
        }
      }
      pppppppuStack_e8 = (undefined *******)ppppppppuVar15;
      operator_delete(local_f0);
    }
    (**(code **)(*plVar24 + 8))(plVar24);
    uVar10 = 0;
  }
  else {
    local_e0 = CONCAT17(4,(undefined7)local_e0);
    local_f0 = (undefined ********)CONCAT35(local_f0._5_3_,0x72726563);
    uVar10 = std::chrono::system_clock::now();
    FUN_1006a284c(&local_560,4,&local_f0,uVar10);
    iVar7 = FUN_10069f1d8(&local_560);
    if (iVar7 != 0) {
      uVar10 = FUN_10069c398(&local_560,"Error opening plugin scan database: ");
      std::error_code::message();
      FUN_10069d278(uVar10,&local_f0);
    }
    thunk_FUN_10069bf04(&local_560);
    (**(code **)(*plVar24 + 8))(plVar24);
    uVar10 = 1;
  }
  FUN_10059b4c0();
  FUN_1004af69c();
  FUN_10020d5dc();
  if (local_568 != (long *)0x0) {
    (**(code **)(*local_568 + 8))();
  }
LAB_1001314f8:
  FUN_100184174(auStack_548);
  FUN_1001380b4(&local_540);
  FUN_100134fdc(auStack_4b0);
  FUN_100134fdc(auStack_448);
  FUN_100138198(auStack_3e0);
  FUN_100138198(auStack_278);
  if (*(long *)PTR____stack_chk_guard_100b1c378 != local_68) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return uVar10;
}

