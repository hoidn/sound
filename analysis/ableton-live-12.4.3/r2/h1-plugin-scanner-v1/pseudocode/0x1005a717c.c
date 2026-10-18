
/* WARNING: Removing unreachable block (ram,0x0001005a7bf0) */
/* WARNING: Removing unreachable block (ram,0x0001005a797c) */
/* WARNING: Removing unreachable block (ram,0x0001005a7b88) */
/* WARNING: Removing unreachable block (ram,0x0001005a7650) */
/* WARNING: Removing unreachable block (ram,0x0001005a7538) */
/* WARNING: Removing unreachable block (ram,0x0001005a7b60) */
/* WARNING: Removing unreachable block (ram,0x0001005a73d4) */
/* WARNING: Removing unreachable block (ram,0x0001005a72c8) */
/* WARNING: Removing unreachable block (ram,0x0001005a7b44) */
/* WARNING: Removing unreachable block (ram,0x0001005a7b34) */
/* WARNING: Removing unreachable block (ram,0x0001005a7b54) */
/* WARNING: Removing unreachable block (ram,0x0001005a7414) */
/* WARNING: Removing unreachable block (ram,0x0001005a7b70) */
/* WARNING: Removing unreachable block (ram,0x0001005a7b84) */
/* WARNING: Removing unreachable block (ram,0x0001005a7690) */
/* WARNING: Removing unreachable block (ram,0x0001005a7b98) */
/* WARNING: Removing unreachable block (ram,0x0001005a7bac) */
/* WARNING: Removing unreachable block (ram,0x0001005a77c0) */
/* WARNING: Removing unreachable block (ram,0x0001005a793c) */
/* WARNING: Removing unreachable block (ram,0x0001005a7c00) */
/* WARNING: Removing unreachable block (ram,0x0001005a7c14) */
/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1005a717c(long *param_1)

{
  char *******pppppppcVar1;
  undefined8 *******pppppppuVar2;
  undefined8 *puVar3;
  char *****pppppcVar4;
  uint7 uVar5;
  undefined8 uVar6;
  undefined8 uVar7;
  byte bVar8;
  int iVar9;
  ulong uVar10;
  long *plVar11;
  undefined8 uVar12;
  long lVar13;
  uint local_180;
  undefined4 uStack_17c;
  ulong uStack_178;
  ulong local_170;
  undefined4 local_164;
  undefined8 *******local_160;
  ulong uStack_158;
  ulong local_150;
  undefined1 local_148 [4];
  undefined1 auStack_144 [4];
  undefined8 local_140;
  ulong uStack_138;
  ulong local_130;
  undefined8 *******local_120;
  ulong uStack_118;
  ulong local_110;
  undefined1 local_108 [4];
  undefined1 auStack_104 [4];
  char *******local_100;
  ulong uStack_f8;
  ulong local_f0;
  undefined1 local_e0 [24];
  char local_c8;
  int local_c0 [2];
  undefined8 local_b8;
  char *******local_b0;
  ulong uStack_a8;
  undefined8 local_a0;
  char *******local_90;
  ulong uStack_88;
  ulong uStack_80;
  long *local_78;
  
  uVar10 = (**(code **)(*param_1 + 0x10))();
  if ((uVar10 & 1) == 0) {
    uVar12 = std::chrono::system_clock::now();
    FUN_1006a290c(local_e0,3,uVar12);
    iVar9 = FUN_10069f1d8(local_e0);
    if (iVar9 != 0) {
      FUN_10069c398(local_e0,"Logging plugins information failed because !IsOpen");
    }
    thunk_FUN_10069bf04(local_e0);
  }
  else {
    FUN_1001c5f40(&local_90);
    uStack_a8._0_1_ = s_PluginScanDb_txt_100a4a4b8[8];
    uStack_a8._1_1_ = s_PluginScanDb_txt_100a4a4b8[9];
    uStack_a8._2_1_ = s_PluginScanDb_txt_100a4a4b8[10];
    uStack_a8._3_1_ = s_PluginScanDb_txt_100a4a4b8[0xb];
    uStack_a8._4_1_ = s_PluginScanDb_txt_100a4a4b8[0xc];
    uStack_a8._5_1_ = s_PluginScanDb_txt_100a4a4b8[0xd];
    uStack_a8._6_1_ = s_PluginScanDb_txt_100a4a4b8[0xe];
    uStack_a8._7_1_ = s_PluginScanDb_txt_100a4a4b8[0xf];
    local_b0 = (char *******)s_PluginScanDb_txt_100a4a4b8._0_8_;
    uVar5 = (uint7)local_a0;
    local_a0 = CONCAT17(0x10,uVar5 & 0xffffffffffff00);
    FUN_10018ef44(local_e0,&local_90,&local_b0);
    plVar11 = (long *)FUN_1002e29c4(0x40);
    thunk_FUN_1002a3f74(plVar11,local_e0,0,1);
    if (plVar11 != (long *)0x0) {
      *(int *)(plVar11 + 1) = (int)plVar11[1] + 1;
    }
    local_78 = plVar11;
    FUN_1002a2f54(plVar11,"",
                  "Logging plugins information about plugin domains start ------------------");
    FUN_1002a2f54(plVar11,"","Id,ModuleId,RelPath,IsEnabled");
    local_c0[0] = 0;
    local_b8 = std::system_category();
    lVar13 = param_1[1];
    local_90 = operator_new(0x40);
    uVar7 = s_SELECT_id__module_id__relpath__e_100a48e58._24_8_;
    uVar6 = s_SELECT_id__module_id__relpath__e_100a48e58._16_8_;
    uVar12 = s_SELECT_id__module_id__relpath__e_100a48e58._0_8_;
    uStack_80 = _UNK_1009d2738;
    uStack_88 = _DAT_1009d2730;
    local_90[1] = (char ******)s_SELECT_id__module_id__relpath__e_100a48e58._8_8_;
    *local_90 = (char ******)uVar12;
    local_90[3] = (char ******)uVar7;
    local_90[2] = (char ******)uVar6;
    uVar12 = s_SELECT_id__module_id__relpath__e_100a48e58._32_8_;
    local_90[5] = (char ******)
                  CONCAT53(s_SELECT_id__module_id__relpath__e_100a48e58._43_5_,
                           s_SELECT_id__module_id__relpath__e_100a48e58._40_3_);
    local_90[4] = (char ******)uVar12;
    uVar12 = CONCAT35(s_SELECT_id__module_id__relpath__e_100a48e58._48_3_,
                      s_SELECT_id__module_id__relpath__e_100a48e58._43_5_);
    *(undefined8 *)((long)local_90 + 0x33) = s_SELECT_id__module_id__relpath__e_100a48e58._51_8_;
    *(undefined8 *)((long)local_90 + 0x2b) = uVar12;
    *(char *)((long)local_90 + 0x3b) = '\0';
    FUN_1005a7f64(local_e0,lVar13,&local_90,local_c0);
    FUN_1005a4e00(local_c0);
    local_90 = (char *******)0x0;
    uStack_88 = 0;
    uStack_80 = 0;
    local_b0 = (char *******)0x0;
    uStack_a8 = 0;
    local_a0 = 0;
    local_140 = (undefined8 *)((ulong)local_140._4_4_ << 0x20);
    while (bVar8 = FUN_1007879e8(local_e0,local_c0), (local_c0[0] == 0 & bVar8) == 1) {
      FUN_1007881cc(local_e0,&local_90);
      FUN_100787e94(local_e0,&local_120);
      FUN_1007881cc(local_e0,&local_b0);
      FUN_100787e94(local_e0,&local_140);
      uVar10 = uStack_88;
      pppppppcVar1 = local_90;
      if (-1 < (long)uStack_80) {
        uVar10 = uStack_80 >> 0x38;
        pppppppcVar1 = (char *******)&local_90;
      }
      FUN_10059b4c4(&local_100,pppppppcVar1,uVar10);
      uStack_88 = uStack_f8;
      local_90 = local_100;
      uStack_80 = local_f0;
      uVar10 = uStack_a8;
      pppppppcVar1 = local_b0;
      if (-1 < (long)local_a0) {
        uVar10 = local_a0 >> 0x38;
        pppppppcVar1 = (char *******)&local_b0;
      }
      FUN_10059b4c4(&local_100,pppppppcVar1,uVar10);
      uStack_a8 = uStack_f8;
      local_b0 = local_100;
      local_a0 = local_f0;
      FUN_1002a335c(plVar11,"","%s,%d,%s,%d");
    }
    FUN_1005a4e00(local_c0);
    if (local_c8 == '\x01') {
      FUN_1007879a4(local_e0);
    }
    FUN_1002a2f54(plVar11,"",
                  "Logging plugins information about plugin domains end --------------------");
    FUN_1002a2f54(plVar11,"",
                  "Logging plugins information about plugin modules start ------------------");
    FUN_1002a2f54(plVar11,"","ModuleId,Path,Arch,Processor,ScanState,Fingerprint");
    lVar13 = param_1[1];
    local_90 = operator_new(0x58);
    uStack_80 = _UNK_1009d2748;
    uStack_88 = _DAT_1009d2740;
    *(undefined4 *)(local_90 + 10) = 0x73656c75;
    uVar7 = s_SELECT_module_id__path__arch__pr_100a48e94._56_8_;
    uVar6 = s_SELECT_module_id__path__arch__pr_100a48e94._48_8_;
    uVar12 = s_SELECT_module_id__path__arch__pr_100a48e94._32_8_;
    local_90[5] = (char ******)s_SELECT_module_id__path__arch__pr_100a48e94._40_8_;
    local_90[4] = (char ******)uVar12;
    local_90[7] = (char ******)uVar7;
    local_90[6] = (char ******)uVar6;
    uVar12 = s_SELECT_module_id__path__arch__pr_100a48e94._64_8_;
    local_90[9] = (char ******)s_SELECT_module_id__path__arch__pr_100a48e94._72_8_;
    local_90[8] = (char ******)uVar12;
    uVar7 = s_SELECT_module_id__path__arch__pr_100a48e94._24_8_;
    uVar6 = s_SELECT_module_id__path__arch__pr_100a48e94._16_8_;
    uVar12 = s_SELECT_module_id__path__arch__pr_100a48e94._0_8_;
    local_90[1] = (char ******)s_SELECT_module_id__path__arch__pr_100a48e94._8_8_;
    *local_90 = (char ******)uVar12;
    local_90[3] = (char ******)uVar7;
    local_90[2] = (char ******)uVar6;
    *(char *)((long)local_90 + 0x54) = '\0';
    FUN_1005a7f64(local_e0,lVar13,&local_90,local_c0);
    FUN_1005a4e00(local_c0);
    local_90 = (char *******)0x0;
    uStack_88 = 0;
    uStack_80 = 0;
    local_b0 = (char *******)0x0;
    uStack_a8 = 0;
    local_a0 = 0;
    while (bVar8 = FUN_1007879e8(local_e0,local_c0), (local_c0[0] == 0 & bVar8) == 1) {
      FUN_100787e94(local_e0,&local_120);
      FUN_1007881cc(local_e0,&local_90);
      FUN_100787e94(local_e0,&local_140);
      FUN_100787e94(local_e0,&local_160);
      FUN_100787e94(local_e0,&local_180);
      FUN_1007881cc(local_e0,&local_b0);
      uVar10 = uStack_88;
      pppppppcVar1 = local_90;
      if (-1 < (long)uStack_80) {
        uVar10 = uStack_80 >> 0x38;
        pppppppcVar1 = (char *******)&local_90;
      }
      FUN_10059b4c4(&local_100,pppppppcVar1,uVar10);
      uStack_88 = uStack_f8;
      local_90 = local_100;
      uStack_80 = local_f0;
      uVar10 = uStack_a8;
      pppppppcVar1 = local_b0;
      if (-1 < (long)local_a0) {
        uVar10 = local_a0 >> 0x38;
        pppppppcVar1 = (char *******)&local_b0;
      }
      FUN_10059b4c4(&local_100,pppppppcVar1,uVar10);
      uStack_a8 = uStack_f8;
      local_b0 = local_100;
      local_a0 = local_f0;
      FUN_1002a335c(plVar11,"","%d,%s,%d,%d,%s,%s");
    }
    FUN_1005a4e00(local_c0);
    if (local_c8 == '\x01') {
      FUN_1007879a4(local_e0);
    }
    FUN_1002a2f54(plVar11,"",
                  "Logging plugins information about plugin modules end --------------------");
    plVar11 = local_78;
    FUN_1002a2f54(local_78,"",
                  "Logging plugins information about all plugins start----------------------");
    FUN_1002a2f54(plVar11,"",
                  "PluginId,ModuleId,DevIdentifier,Name,Vendor,Version,SdkVersion,Flags,ScanState,SubCategories,IsEnabled"
                 );
    lVar13 = param_1[1];
    local_90 = operator_new(0x90);
    uVar6 = s_SELECT_plugin_id__module_id__dev_100a48ee9._112_8_;
    uVar12 = s_SELECT_plugin_id__module_id__dev_100a48ee9._96_8_;
    uStack_80 = _UNK_1009d2758;
    uStack_88 = _DAT_1009d2750;
    pppppcVar4 = (char *****)
                 CONCAT17(s_SELECT_plugin_id__module_id__dev_100a48ee9[0x7f],
                          s_SELECT_plugin_id__module_id__dev_100a48ee9._120_7_);
    local_90[0xd] = (char ******)s_SELECT_plugin_id__module_id__dev_100a48ee9._104_8_;
    local_90[0xc] = (char ******)uVar12;
    local_90[0xf] = (char ******)pppppcVar4;
    local_90[0xe] = (char ******)uVar6;
    uVar12 = CONCAT71(s_SELECT_plugin_id__module_id__dev_100a48ee9._128_7_,
                      s_SELECT_plugin_id__module_id__dev_100a48ee9[0x7f]);
    *(undefined8 *)((long)local_90 + 0x87) = s_SELECT_plugin_id__module_id__dev_100a48ee9._135_8_;
    *(undefined8 *)((long)local_90 + 0x7f) = uVar12;
    uVar7 = s_SELECT_plugin_id__module_id__dev_100a48ee9._56_8_;
    uVar6 = s_SELECT_plugin_id__module_id__dev_100a48ee9._48_8_;
    uVar12 = s_SELECT_plugin_id__module_id__dev_100a48ee9._32_8_;
    local_90[5] = (char ******)s_SELECT_plugin_id__module_id__dev_100a48ee9._40_8_;
    local_90[4] = (char ******)uVar12;
    local_90[7] = (char ******)uVar7;
    local_90[6] = (char ******)uVar6;
    uVar7 = s_SELECT_plugin_id__module_id__dev_100a48ee9._88_8_;
    uVar6 = s_SELECT_plugin_id__module_id__dev_100a48ee9._80_8_;
    uVar12 = s_SELECT_plugin_id__module_id__dev_100a48ee9._64_8_;
    local_90[9] = (char ******)s_SELECT_plugin_id__module_id__dev_100a48ee9._72_8_;
    local_90[8] = (char ******)uVar12;
    local_90[0xb] = (char ******)uVar7;
    local_90[10] = (char ******)uVar6;
    uVar7 = s_SELECT_plugin_id__module_id__dev_100a48ee9._24_8_;
    uVar6 = s_SELECT_plugin_id__module_id__dev_100a48ee9._16_8_;
    uVar12 = s_SELECT_plugin_id__module_id__dev_100a48ee9._0_8_;
    local_90[1] = (char ******)s_SELECT_plugin_id__module_id__dev_100a48ee9._8_8_;
    *local_90 = (char ******)uVar12;
    local_90[3] = (char ******)uVar7;
    local_90[2] = (char ******)uVar6;
    *(char *)((long)local_90 + 0x8f) = '\0';
    FUN_1005a7f64(local_e0,lVar13,&local_90,local_c0);
    FUN_1005a4e00(local_c0);
    local_90 = (char *******)0x0;
    uStack_88 = 0;
    uStack_80 = 0;
    local_b0 = (char *******)0x0;
    uStack_a8 = 0;
    local_a0 = 0;
    local_100 = (char *******)0x0;
    uStack_f8 = 0;
    local_f0 = 0;
    local_120 = (undefined8 *******)0x0;
    uStack_118 = 0;
    local_110 = 0;
    local_140 = (undefined8 *)0x0;
    uStack_138 = 0;
    local_130 = 0;
    local_160 = (undefined8 *******)0x0;
    uStack_158 = 0;
    local_150 = 0;
    local_164 = 0;
    while (iVar9 = FUN_1005a8058(local_e0,local_c0,auStack_104,local_108,&local_90,&local_b0,
                                 &local_100,&local_120,&local_140,auStack_144,local_148,&local_160,
                                 &local_164), iVar9 != 0) {
      uVar10 = uStack_88;
      pppppppcVar1 = local_90;
      if (-1 < (long)uStack_80) {
        uVar10 = uStack_80 >> 0x38;
        pppppppcVar1 = (char *******)&local_90;
      }
      FUN_10059b4c4(&local_180,pppppppcVar1,uVar10);
      local_90 = (char *******)CONCAT44(uStack_17c,local_180);
      uStack_88 = uStack_178;
      uStack_80 = local_170;
      uVar10 = uStack_a8;
      pppppppcVar1 = local_b0;
      if (-1 < (long)local_a0) {
        uVar10 = local_a0 >> 0x38;
        pppppppcVar1 = (char *******)&local_b0;
      }
      FUN_10059b4c4(&local_180,pppppppcVar1,uVar10);
      local_b0 = (char *******)CONCAT44(uStack_17c,local_180);
      uStack_a8 = uStack_178;
      local_a0 = local_170;
      uVar10 = uStack_f8;
      pppppppcVar1 = local_100;
      if (-1 < (long)local_f0) {
        uVar10 = local_f0 >> 0x38;
        pppppppcVar1 = (char *******)&local_100;
      }
      FUN_10059b4c4(&local_180,pppppppcVar1,uVar10);
      if ((long)local_f0 < 0) {
        operator_delete(local_100);
      }
      local_100 = (char *******)CONCAT44(uStack_17c,local_180);
      uStack_f8 = uStack_178;
      local_f0 = local_170;
      uVar10 = uStack_118;
      pppppppuVar2 = local_120;
      if (-1 < (long)local_110) {
        uVar10 = local_110 >> 0x38;
        pppppppuVar2 = &local_120;
      }
      FUN_10059b4c4(&local_180,pppppppuVar2,uVar10);
      if ((long)local_110 < 0) {
        operator_delete(local_120);
      }
      local_120 = (undefined8 *******)CONCAT44(uStack_17c,local_180);
      uStack_118 = uStack_178;
      local_110 = local_170;
      uVar10 = uStack_138;
      puVar3 = local_140;
      if (-1 < (long)local_130) {
        uVar10 = local_130 >> 0x38;
        puVar3 = &local_140;
      }
      FUN_10059b4c4(&local_180,puVar3,uVar10);
      if ((long)local_130 < 0) {
        operator_delete(local_140);
      }
      local_140 = (undefined8 *)CONCAT44(uStack_17c,local_180);
      uStack_138 = uStack_178;
      local_130 = local_170;
      uVar10 = uStack_158;
      pppppppuVar2 = local_160;
      if (-1 < (long)local_150) {
        uVar10 = local_150 >> 0x38;
        pppppppuVar2 = &local_160;
      }
      FUN_10059b4c4(&local_180,pppppppuVar2,uVar10);
      if ((long)local_150 < 0) {
        operator_delete(local_160);
      }
      local_160 = (undefined8 *******)CONCAT44(uStack_17c,local_180);
      uStack_158 = uStack_178;
      local_150 = local_170;
      FUN_1002a335c(plVar11,"","%d,%d,%s,%s,%s,%s,%s,%d,%d,%s,%d");
    }
    FUN_1005a4e00(local_c0);
    if ((long)local_150 < 0) {
      operator_delete(local_160);
    }
    if ((long)local_130 < 0) {
      operator_delete(local_140);
    }
    if ((long)local_110 < 0) {
      operator_delete(local_120);
    }
    if ((long)local_f0 < 0) {
      operator_delete(local_100);
    }
    if (local_c8 == '\x01') {
      FUN_1007879a4(local_e0);
    }
    FUN_1002a2f54(plVar11,"",
                  "Logging plugins information about all plugins end -----------------------");
    (**(code **)(*plVar11 + 0x28))(plVar11);
    iVar9 = (int)plVar11[1] + -1;
    *(int *)(plVar11 + 1) = iVar9;
    if (iVar9 == 0) {
      FUN_100292f88(plVar11);
    }
  }
  return;
}

