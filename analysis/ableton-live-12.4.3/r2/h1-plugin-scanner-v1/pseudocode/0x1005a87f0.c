
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1005a87f0(long *param_1,int param_2,undefined4 param_3,long *param_4)

{
  long lVar1;
  long lVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  undefined8 uVar5;
  undefined8 uVar6;
  undefined4 uVar7;
  undefined4 uVar8;
  int iVar9;
  int iVar10;
  long lVar11;
  long lVar12;
  undefined1 auVar13 [16];
  char *local_130;
  undefined4 local_128 [4];
  uint local_118;
  char *local_110;
  undefined1 auStack_108 [16];
  uint local_f8;
  char *local_f0;
  int iStack_e8;
  undefined4 uStack_e4;
  undefined4 uStack_e0;
  undefined4 uStack_dc;
  uint local_d8;
  char *local_c8;
  undefined8 local_c0;
  long lStack_b8;
  undefined1 auStack_b0 [24];
  char local_98;
  undefined1 auStack_90 [16];
  undefined4 local_80 [2];
  undefined8 local_78;
  undefined1 auStack_69 [9];
  
  iVar10 = (**(code **)(*param_1 + 0x10))();
  if (iVar10 != 0) {
    local_80[0] = 0;
    local_78 = std::system_category();
    FUN_100783784(auStack_90,param_1[1],1,local_80);
    FUN_1005a4e00(local_80);
    lVar11 = _UNK_1009d2798;
    uVar3 = _DAT_1009d2790;
    if (param_2 == 0) {
      lVar11 = param_1[1];
      local_f0 = operator_new(0x20);
      uVar3 = s_DELETE_FROM_plugin_domains_100a1ff5a._0_8_;
      uStack_e0 = (undefined4)_UNK_1009ad718;
      uVar8 = uStack_e0;
      uStack_dc = (int)((ulong)_UNK_1009ad718 >> 0x20);
      iVar9 = uStack_dc;
      iStack_e8 = (int)_DAT_1009ad710;
      iVar10 = iStack_e8;
      uStack_e4 = (undefined4)((ulong)_DAT_1009ad710 >> 0x20);
      uVar7 = uStack_e4;
      *(ulong *)(local_f0 + 8) =
           CONCAT62(s_DELETE_FROM_plugin_domains_100a1ff5a._10_6_,
                    s_DELETE_FROM_plugin_domains_100a1ff5a._8_2_);
      *(undefined8 *)local_f0 = uVar3;
      uVar3 = CONCAT26(s_DELETE_FROM_plugin_domains_100a1ff5a._16_2_,
                       s_DELETE_FROM_plugin_domains_100a1ff5a._10_6_);
      *(undefined8 *)(local_f0 + 0x12) = s_DELETE_FROM_plugin_domains_100a1ff5a._18_8_;
      *(undefined8 *)(local_f0 + 10) = uVar3;
      local_f0[0x1a] = '\0';
      FUN_1005a7f64(auStack_b0,lVar11,&local_f0,local_80);
      if (uStack_dc < 0) {
        operator_delete(local_f0);
      }
      FUN_1005a4e00(local_80);
      FUN_100787c3c(auStack_b0,local_80);
      FUN_1005a4e00(local_80);
      if (local_98 == '\x01') {
        FUN_1007879a4(auStack_b0);
      }
      uStack_dc._3_1_ = '\x13';
      iStack_e8 = (int)s_DELETE_FROM_plugins_100a49218._8_8_;
      uStack_e4 = SUB84(s_DELETE_FROM_plugins_100a49218._8_8_,4);
      local_f0 = (char *)s_DELETE_FROM_plugins_100a49218._0_8_;
      uStack_e0 = 0x736e69;
      FUN_1005a7f64(auStack_b0,param_1[1],&local_f0,local_80);
      if (uStack_dc._3_1_ < '\0') {
        operator_delete(local_f0);
      }
      FUN_1005a4e00(local_80);
      FUN_100787c3c(auStack_b0,local_80);
      FUN_1005a4e00(local_80);
      if (local_98 == '\x01') {
        FUN_1007879a4(auStack_b0);
      }
      lVar11 = param_1[1];
      local_f0 = operator_new(0x20);
      uVar3 = s_DELETE_FROM_plugin_modules_100a4a7c2._0_8_;
      *(ulong *)(local_f0 + 8) =
           CONCAT62(s_DELETE_FROM_plugin_modules_100a4a7c2._10_6_,
                    s_DELETE_FROM_plugin_modules_100a4a7c2._8_2_);
      *(undefined8 *)local_f0 = uVar3;
      uVar3 = CONCAT26(s_DELETE_FROM_plugin_modules_100a4a7c2._16_2_,
                       s_DELETE_FROM_plugin_modules_100a4a7c2._10_6_);
      *(undefined8 *)(local_f0 + 0x12) = s_DELETE_FROM_plugin_modules_100a4a7c2._18_8_;
      *(undefined8 *)(local_f0 + 10) = uVar3;
      local_f0[0x1a] = '\0';
      iStack_e8 = iVar10;
      uStack_e4 = uVar7;
      uStack_e0 = uVar8;
      uStack_dc = iVar9;
      FUN_1005a7f64(auStack_b0,lVar11,&local_f0,local_80);
      if (uStack_dc < 0) {
        operator_delete(local_f0);
      }
      FUN_1005a4e00(local_80);
      FUN_100787c3c(auStack_b0,local_80);
      FUN_1005a4e00(local_80);
    }
    else {
      lVar2 = param_4[1];
      for (lVar1 = *param_4; lVar1 != lVar2; lVar1 = lVar1 + 8) {
        lVar12 = param_1[1];
        local_c8 = operator_new(0xe0);
        uVar6 = s_DELETE_FROM_plugin_domains_WHERE_100a4942a._184_8_;
        uVar5 = s_DELETE_FROM_plugin_domains_WHERE_100a4942a._176_8_;
        uVar4 = s_DELETE_FROM_plugin_domains_WHERE_100a4942a._160_8_;
        lStack_b8 = lVar11;
        local_c0 = uVar3;
        *(undefined8 *)(local_c8 + 0xa8) = s_DELETE_FROM_plugin_domains_WHERE_100a4942a._168_8_;
        *(undefined8 *)(local_c8 + 0xa0) = uVar4;
        *(undefined8 *)(local_c8 + 0xb8) = uVar6;
        *(undefined8 *)(local_c8 + 0xb0) = uVar5;
        uVar4 = s_DELETE_FROM_plugin_domains_WHERE_100a4942a._192_8_;
        *(undefined8 *)(local_c8 + 200) = s_DELETE_FROM_plugin_domains_WHERE_100a4942a._200_8_;
        *(undefined8 *)(local_c8 + 0xc0) = uVar4;
        *(undefined8 *)(local_c8 + 0xd0) = s_DELETE_FROM_plugin_domains_WHERE_100a4942a._208_8_;
        uVar6 = s_DELETE_FROM_plugin_domains_WHERE_100a4942a._120_8_;
        uVar5 = s_DELETE_FROM_plugin_domains_WHERE_100a4942a._112_8_;
        uVar4 = s_DELETE_FROM_plugin_domains_WHERE_100a4942a._96_8_;
        *(undefined8 *)(local_c8 + 0x68) = s_DELETE_FROM_plugin_domains_WHERE_100a4942a._104_8_;
        *(undefined8 *)(local_c8 + 0x60) = uVar4;
        *(undefined8 *)(local_c8 + 0x78) = uVar6;
        *(undefined8 *)(local_c8 + 0x70) = uVar5;
        uVar6 = s_DELETE_FROM_plugin_domains_WHERE_100a4942a._152_8_;
        uVar5 = s_DELETE_FROM_plugin_domains_WHERE_100a4942a._144_8_;
        uVar4 = s_DELETE_FROM_plugin_domains_WHERE_100a4942a._128_8_;
        *(undefined8 *)(local_c8 + 0x88) = s_DELETE_FROM_plugin_domains_WHERE_100a4942a._136_8_;
        *(undefined8 *)(local_c8 + 0x80) = uVar4;
        *(undefined8 *)(local_c8 + 0x98) = uVar6;
        *(undefined8 *)(local_c8 + 0x90) = uVar5;
        uVar6 = s_DELETE_FROM_plugin_domains_WHERE_100a4942a._56_8_;
        uVar5 = s_DELETE_FROM_plugin_domains_WHERE_100a4942a._48_8_;
        uVar4 = s_DELETE_FROM_plugin_domains_WHERE_100a4942a._32_8_;
        *(undefined8 *)(local_c8 + 0x28) = s_DELETE_FROM_plugin_domains_WHERE_100a4942a._40_8_;
        *(undefined8 *)(local_c8 + 0x20) = uVar4;
        *(undefined8 *)(local_c8 + 0x38) = uVar6;
        *(undefined8 *)(local_c8 + 0x30) = uVar5;
        uVar6 = s_DELETE_FROM_plugin_domains_WHERE_100a4942a._88_8_;
        uVar5 = s_DELETE_FROM_plugin_domains_WHERE_100a4942a._80_8_;
        uVar4 = s_DELETE_FROM_plugin_domains_WHERE_100a4942a._64_8_;
        *(undefined8 *)(local_c8 + 0x48) = s_DELETE_FROM_plugin_domains_WHERE_100a4942a._72_8_;
        *(undefined8 *)(local_c8 + 0x40) = uVar4;
        *(undefined8 *)(local_c8 + 0x58) = uVar6;
        *(undefined8 *)(local_c8 + 0x50) = uVar5;
        uVar6 = s_DELETE_FROM_plugin_domains_WHERE_100a4942a._24_8_;
        uVar5 = s_DELETE_FROM_plugin_domains_WHERE_100a4942a._16_8_;
        uVar4 = s_DELETE_FROM_plugin_domains_WHERE_100a4942a._0_8_;
        *(undefined8 *)(local_c8 + 8) = s_DELETE_FROM_plugin_domains_WHERE_100a4942a._8_8_;
        *(undefined8 *)local_c8 = uVar4;
        *(undefined8 *)(local_c8 + 0x18) = uVar6;
        *(undefined8 *)(local_c8 + 0x10) = uVar5;
        local_c8[0xd8] = '\0';
        local_f0 = s__arch_100a4a7dd;
        local_d8 = 2;
        iStack_e8 = param_2;
        auVar13 = FUN_100437d68(lVar1);
        local_110 = ":domain_id";
        local_f8 = 6;
        local_130 = ":processor_mask";
        local_118 = 2;
        local_128[0] = param_3;
        auStack_108 = auVar13;
        FUN_1005a6818(auStack_b0,lVar12,&local_c8,local_80,&local_f0,&local_110,&local_130);
        if (local_118 != 0xffffffff) {
          (*(code *)(&PTR_FUN_100b6daf0)[local_118])(auStack_69,local_128);
        }
        if (local_f8 != 0xffffffff) {
          (*(code *)(&PTR_FUN_100b6daf0)[local_f8])(&local_130,auStack_108);
        }
        if (local_d8 != 0xffffffff) {
          (*(code *)(&PTR_FUN_100b6daf0)[local_d8])(&local_110,&iStack_e8);
        }
        if (lStack_b8 < 0) {
          operator_delete(local_c8);
        }
        FUN_1005a4e00(local_80);
        FUN_100787c3c(auStack_b0,local_80);
        FUN_1005a4e00(local_80);
        if (local_98 == '\x01') {
          FUN_1007879a4(auStack_b0);
        }
      }
      lVar11 = param_1[1];
      local_f0 = operator_new(0xe0);
      uVar5 = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._184_8_;
      uVar4 = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._176_8_;
      uVar3 = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._160_8_;
      uStack_e0 = (undefined4)_UNK_1009d2788;
      uStack_dc = (int)((ulong)_UNK_1009d2788 >> 0x20);
      iStack_e8 = (int)_DAT_1009d2780;
      uStack_e4 = (undefined4)((ulong)_DAT_1009d2780 >> 0x20);
      *(undefined8 *)(local_f0 + 0xa8) = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._168_8_;
      *(undefined8 *)(local_f0 + 0xa0) = uVar3;
      *(undefined8 *)(local_f0 + 0xb8) = uVar5;
      *(undefined8 *)(local_f0 + 0xb0) = uVar4;
      uVar3 = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._192_8_;
      *(ulong *)(local_f0 + 200) =
           CONCAT53(s_DELETE_FROM_plugin_modules_WHERE_100a4927c._203_5_,
                    s_DELETE_FROM_plugin_modules_WHERE_100a4927c._200_3_);
      *(undefined8 *)(local_f0 + 0xc0) = uVar3;
      uVar3 = CONCAT35(s_DELETE_FROM_plugin_modules_WHERE_100a4927c._208_3_,
                       s_DELETE_FROM_plugin_modules_WHERE_100a4927c._203_5_);
      *(undefined8 *)(local_f0 + 0xd3) = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._211_8_;
      *(undefined8 *)(local_f0 + 0xcb) = uVar3;
      uVar5 = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._120_8_;
      uVar4 = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._112_8_;
      uVar3 = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._96_8_;
      *(undefined8 *)(local_f0 + 0x68) = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._104_8_;
      *(undefined8 *)(local_f0 + 0x60) = uVar3;
      *(undefined8 *)(local_f0 + 0x78) = uVar5;
      *(undefined8 *)(local_f0 + 0x70) = uVar4;
      uVar5 = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._152_8_;
      uVar4 = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._144_8_;
      uVar3 = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._128_8_;
      *(undefined8 *)(local_f0 + 0x88) = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._136_8_;
      *(undefined8 *)(local_f0 + 0x80) = uVar3;
      *(undefined8 *)(local_f0 + 0x98) = uVar5;
      *(undefined8 *)(local_f0 + 0x90) = uVar4;
      uVar5 = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._56_8_;
      uVar4 = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._48_8_;
      uVar3 = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._32_8_;
      *(undefined8 *)(local_f0 + 0x28) = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._40_8_;
      *(undefined8 *)(local_f0 + 0x20) = uVar3;
      *(undefined8 *)(local_f0 + 0x38) = uVar5;
      *(undefined8 *)(local_f0 + 0x30) = uVar4;
      uVar5 = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._88_8_;
      uVar4 = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._80_8_;
      uVar3 = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._64_8_;
      *(undefined8 *)(local_f0 + 0x48) = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._72_8_;
      *(undefined8 *)(local_f0 + 0x40) = uVar3;
      *(undefined8 *)(local_f0 + 0x58) = uVar5;
      *(undefined8 *)(local_f0 + 0x50) = uVar4;
      uVar5 = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._24_8_;
      uVar4 = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._16_8_;
      uVar3 = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._0_8_;
      *(undefined8 *)(local_f0 + 8) = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._8_8_;
      *(undefined8 *)local_f0 = uVar3;
      *(undefined8 *)(local_f0 + 0x18) = uVar5;
      *(undefined8 *)(local_f0 + 0x10) = uVar4;
      local_f0[0xdb] = '\0';
      FUN_1005a7f64(auStack_b0,lVar11,&local_f0,local_80);
      if (uStack_dc < 0) {
        operator_delete(local_f0);
      }
      FUN_1005a4e00(local_80);
      FUN_100787c3c(auStack_b0,local_80);
      FUN_1005a4e00(local_80);
      if (local_98 == '\x01') {
        FUN_1007879a4(auStack_b0);
      }
      lVar11 = param_1[1];
      local_f0 = operator_new(0xd8);
      uStack_e0 = (undefined4)_UNK_1009d2858;
      uStack_dc = (int)((ulong)_UNK_1009d2858 >> 0x20);
      iStack_e8 = (int)_DAT_1009d2850;
      uStack_e4 = (undefined4)((ulong)_DAT_1009d2850 >> 0x20);
      local_f0[0xd0] = ')';
      uVar5 = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._184_8_;
      uVar4 = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._176_8_;
      uVar3 = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._160_8_;
      *(undefined8 *)(local_f0 + 0xa8) = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._168_8_;
      *(undefined8 *)(local_f0 + 0xa0) = uVar3;
      *(undefined8 *)(local_f0 + 0xb8) = uVar5;
      *(undefined8 *)(local_f0 + 0xb0) = uVar4;
      uVar3 = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._192_8_;
      *(undefined8 *)(local_f0 + 200) = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._200_8_;
      *(undefined8 *)(local_f0 + 0xc0) = uVar3;
      uVar5 = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._120_8_;
      uVar4 = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._112_8_;
      uVar3 = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._96_8_;
      *(undefined8 *)(local_f0 + 0x68) = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._104_8_;
      *(undefined8 *)(local_f0 + 0x60) = uVar3;
      *(undefined8 *)(local_f0 + 0x78) = uVar5;
      *(undefined8 *)(local_f0 + 0x70) = uVar4;
      uVar5 = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._152_8_;
      uVar4 = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._144_8_;
      uVar3 = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._128_8_;
      *(undefined8 *)(local_f0 + 0x88) = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._136_8_;
      *(undefined8 *)(local_f0 + 0x80) = uVar3;
      *(undefined8 *)(local_f0 + 0x98) = uVar5;
      *(undefined8 *)(local_f0 + 0x90) = uVar4;
      uVar5 = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._56_8_;
      uVar4 = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._48_8_;
      uVar3 = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._32_8_;
      *(undefined8 *)(local_f0 + 0x28) = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._40_8_;
      *(undefined8 *)(local_f0 + 0x20) = uVar3;
      *(undefined8 *)(local_f0 + 0x38) = uVar5;
      *(undefined8 *)(local_f0 + 0x30) = uVar4;
      uVar5 = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._88_8_;
      uVar4 = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._80_8_;
      uVar3 = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._64_8_;
      *(undefined8 *)(local_f0 + 0x48) = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._72_8_;
      *(undefined8 *)(local_f0 + 0x40) = uVar3;
      *(undefined8 *)(local_f0 + 0x58) = uVar5;
      *(undefined8 *)(local_f0 + 0x50) = uVar4;
      uVar5 = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._24_8_;
      uVar4 = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._16_8_;
      uVar3 = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._0_8_;
      *(undefined8 *)(local_f0 + 8) = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._8_8_;
      *(undefined8 *)local_f0 = uVar3;
      *(undefined8 *)(local_f0 + 0x18) = uVar5;
      *(undefined8 *)(local_f0 + 0x10) = uVar4;
      local_f0[0xd1] = '\0';
      FUN_1005a7f64(auStack_b0,lVar11,&local_f0,local_80);
      if (uStack_dc < 0) {
        operator_delete(local_f0);
      }
      FUN_1005a4e00(local_80);
      FUN_100787c3c(auStack_b0,local_80);
      FUN_1005a4e00(local_80);
    }
    if (local_98 == '\x01') {
      FUN_1007879a4(auStack_b0);
    }
    FUN_1007839d4(auStack_90,local_80);
    FUN_1005a4e00(local_80);
    thunk_FUN_100785fdc(auStack_90);
  }
  return;
}

