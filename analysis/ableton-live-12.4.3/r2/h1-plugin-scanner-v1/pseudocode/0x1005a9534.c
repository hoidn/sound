
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1005a9534(long *param_1,undefined8 *param_2,undefined8 param_3)

{
  undefined4 *puVar1;
  undefined4 *puVar2;
  undefined4 uVar3;
  undefined8 uVar4;
  undefined8 uVar5;
  long lVar6;
  undefined8 uVar7;
  long lVar8;
  undefined8 uVar9;
  long lVar10;
  undefined8 uVar11;
  undefined8 uVar12;
  int iVar13;
  long lVar14;
  undefined1 auVar15 [16];
  char *local_108;
  undefined1 auStack_100 [16];
  uint local_f0;
  char *local_e8;
  undefined8 local_e0;
  long lStack_d8;
  uint local_d0;
  char *local_c8;
  undefined8 local_c0;
  long lStack_b8;
  undefined1 auStack_b0 [24];
  char local_98;
  undefined1 auStack_90 [16];
  undefined4 local_80 [2];
  undefined8 local_78;
  undefined1 auStack_69 [9];
  
  iVar13 = (**(code **)(*param_1 + 0x10))();
  if (iVar13 != 0) {
    local_80[0] = 0;
    local_78 = std::system_category();
    FUN_100783784(auStack_90,param_1[1],1,local_80);
    FUN_1005a4e00(local_80);
    lVar10 = _UNK_1009d2858;
    uVar9 = _DAT_1009d2850;
    lVar8 = _UNK_1009d2788;
    uVar7 = _DAT_1009d2780;
    lVar6 = _UNK_1009cc488;
    uVar5 = _DAT_1009cc480;
    puVar2 = (undefined4 *)param_2[1];
    for (puVar1 = (undefined4 *)*param_2; puVar1 != puVar2; puVar1 = puVar1 + 1) {
      uVar3 = *puVar1;
      lVar14 = param_1[1];
      local_c8 = operator_new(0x50);
      uVar12 = s_DELETE_FROM_plugin_domains_WHERE_100a4922c._48_8_;
      uVar11 = s_DELETE_FROM_plugin_domains_WHERE_100a4922c._32_8_;
      lStack_b8 = lVar6;
      local_c0 = uVar5;
      uVar4 = CONCAT17(s_DELETE_FROM_plugin_domains_WHERE_100a4922c[0x3f],
                       s_DELETE_FROM_plugin_domains_WHERE_100a4922c._56_7_);
      *(undefined8 *)(local_c8 + 0x28) = s_DELETE_FROM_plugin_domains_WHERE_100a4922c._40_8_;
      *(undefined8 *)(local_c8 + 0x20) = uVar11;
      *(undefined8 *)(local_c8 + 0x38) = uVar4;
      *(undefined8 *)(local_c8 + 0x30) = uVar12;
      uVar4 = CONCAT71(s_DELETE_FROM_plugin_domains_WHERE_100a4922c._64_7_,
                       s_DELETE_FROM_plugin_domains_WHERE_100a4922c[0x3f]);
      *(undefined8 *)(local_c8 + 0x47) = s_DELETE_FROM_plugin_domains_WHERE_100a4922c._71_8_;
      *(undefined8 *)(local_c8 + 0x3f) = uVar4;
      uVar12 = s_DELETE_FROM_plugin_domains_WHERE_100a4922c._24_8_;
      uVar11 = s_DELETE_FROM_plugin_domains_WHERE_100a4922c._16_8_;
      uVar4 = s_DELETE_FROM_plugin_domains_WHERE_100a4922c._0_8_;
      *(undefined8 *)(local_c8 + 8) = s_DELETE_FROM_plugin_domains_WHERE_100a4922c._8_8_;
      *(undefined8 *)local_c8 = uVar4;
      *(undefined8 *)(local_c8 + 0x18) = uVar12;
      *(undefined8 *)(local_c8 + 0x10) = uVar11;
      local_c8[0x4f] = '\0';
      local_e8 = ":module_id";
      local_e0 = CONCAT44(local_e0._4_4_,uVar3);
      local_d0 = 2;
      auVar15 = FUN_100437d68(param_3);
      local_108 = ":domain_id";
      local_f0 = 6;
      auStack_100 = auVar15;
      FUN_1005a6424(auStack_b0,lVar14,&local_c8,local_80,&local_e8,&local_108);
      if (local_f0 != 0xffffffff) {
        (*(code *)(&PTR_FUN_100b6daf0)[local_f0])(auStack_69,auStack_100);
      }
      if (local_d0 != 0xffffffff) {
        (*(code *)(&PTR_FUN_100b6daf0)[local_d0])(&local_108,&local_e0);
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
      lVar14 = param_1[1];
      local_e8 = operator_new(0xe0);
      uVar12 = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._184_8_;
      uVar11 = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._176_8_;
      uVar4 = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._160_8_;
      lStack_d8 = lVar8;
      local_e0 = uVar7;
      *(undefined8 *)(local_e8 + 0xa8) = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._168_8_;
      *(undefined8 *)(local_e8 + 0xa0) = uVar4;
      *(undefined8 *)(local_e8 + 0xb8) = uVar12;
      *(undefined8 *)(local_e8 + 0xb0) = uVar11;
      uVar4 = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._192_8_;
      *(ulong *)(local_e8 + 200) =
           CONCAT53(s_DELETE_FROM_plugin_modules_WHERE_100a4927c._203_5_,
                    s_DELETE_FROM_plugin_modules_WHERE_100a4927c._200_3_);
      *(undefined8 *)(local_e8 + 0xc0) = uVar4;
      uVar4 = CONCAT35(s_DELETE_FROM_plugin_modules_WHERE_100a4927c._208_3_,
                       s_DELETE_FROM_plugin_modules_WHERE_100a4927c._203_5_);
      *(undefined8 *)(local_e8 + 0xd3) = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._211_8_;
      *(undefined8 *)(local_e8 + 0xcb) = uVar4;
      uVar12 = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._120_8_;
      uVar11 = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._112_8_;
      uVar4 = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._96_8_;
      *(undefined8 *)(local_e8 + 0x68) = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._104_8_;
      *(undefined8 *)(local_e8 + 0x60) = uVar4;
      *(undefined8 *)(local_e8 + 0x78) = uVar12;
      *(undefined8 *)(local_e8 + 0x70) = uVar11;
      uVar12 = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._152_8_;
      uVar11 = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._144_8_;
      uVar4 = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._128_8_;
      *(undefined8 *)(local_e8 + 0x88) = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._136_8_;
      *(undefined8 *)(local_e8 + 0x80) = uVar4;
      *(undefined8 *)(local_e8 + 0x98) = uVar12;
      *(undefined8 *)(local_e8 + 0x90) = uVar11;
      uVar12 = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._56_8_;
      uVar11 = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._48_8_;
      uVar4 = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._32_8_;
      *(undefined8 *)(local_e8 + 0x28) = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._40_8_;
      *(undefined8 *)(local_e8 + 0x20) = uVar4;
      *(undefined8 *)(local_e8 + 0x38) = uVar12;
      *(undefined8 *)(local_e8 + 0x30) = uVar11;
      uVar12 = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._88_8_;
      uVar11 = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._80_8_;
      uVar4 = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._64_8_;
      *(undefined8 *)(local_e8 + 0x48) = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._72_8_;
      *(undefined8 *)(local_e8 + 0x40) = uVar4;
      *(undefined8 *)(local_e8 + 0x58) = uVar12;
      *(undefined8 *)(local_e8 + 0x50) = uVar11;
      uVar12 = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._24_8_;
      uVar11 = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._16_8_;
      uVar4 = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._0_8_;
      *(undefined8 *)(local_e8 + 8) = s_DELETE_FROM_plugin_modules_WHERE_100a4927c._8_8_;
      *(undefined8 *)local_e8 = uVar4;
      *(undefined8 *)(local_e8 + 0x18) = uVar12;
      *(undefined8 *)(local_e8 + 0x10) = uVar11;
      local_e8[0xdb] = '\0';
      FUN_1005a7f64(auStack_b0,lVar14,&local_e8,local_80);
      if (lStack_d8 < 0) {
        operator_delete(local_e8);
      }
      FUN_1005a4e00(local_80);
      FUN_100787c3c(auStack_b0,local_80);
      FUN_1005a4e00(local_80);
      if (local_98 == '\x01') {
        FUN_1007879a4(auStack_b0);
      }
      lVar14 = param_1[1];
      local_e8 = operator_new(0xd8);
      lStack_d8 = lVar10;
      local_e0 = uVar9;
      local_e8[0xd0] = ')';
      uVar12 = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._184_8_;
      uVar11 = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._176_8_;
      uVar4 = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._160_8_;
      *(undefined8 *)(local_e8 + 0xa8) = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._168_8_;
      *(undefined8 *)(local_e8 + 0xa0) = uVar4;
      *(undefined8 *)(local_e8 + 0xb8) = uVar12;
      *(undefined8 *)(local_e8 + 0xb0) = uVar11;
      uVar4 = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._192_8_;
      *(undefined8 *)(local_e8 + 200) = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._200_8_;
      *(undefined8 *)(local_e8 + 0xc0) = uVar4;
      uVar12 = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._120_8_;
      uVar11 = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._112_8_;
      uVar4 = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._96_8_;
      *(undefined8 *)(local_e8 + 0x68) = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._104_8_;
      *(undefined8 *)(local_e8 + 0x60) = uVar4;
      *(undefined8 *)(local_e8 + 0x78) = uVar12;
      *(undefined8 *)(local_e8 + 0x70) = uVar11;
      uVar12 = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._152_8_;
      uVar11 = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._144_8_;
      uVar4 = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._128_8_;
      *(undefined8 *)(local_e8 + 0x88) = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._136_8_;
      *(undefined8 *)(local_e8 + 0x80) = uVar4;
      *(undefined8 *)(local_e8 + 0x98) = uVar12;
      *(undefined8 *)(local_e8 + 0x90) = uVar11;
      uVar12 = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._56_8_;
      uVar11 = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._48_8_;
      uVar4 = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._32_8_;
      *(undefined8 *)(local_e8 + 0x28) = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._40_8_;
      *(undefined8 *)(local_e8 + 0x20) = uVar4;
      *(undefined8 *)(local_e8 + 0x38) = uVar12;
      *(undefined8 *)(local_e8 + 0x30) = uVar11;
      uVar12 = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._88_8_;
      uVar11 = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._80_8_;
      uVar4 = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._64_8_;
      *(undefined8 *)(local_e8 + 0x48) = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._72_8_;
      *(undefined8 *)(local_e8 + 0x40) = uVar4;
      *(undefined8 *)(local_e8 + 0x58) = uVar12;
      *(undefined8 *)(local_e8 + 0x50) = uVar11;
      uVar12 = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._24_8_;
      uVar11 = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._16_8_;
      uVar4 = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._0_8_;
      *(undefined8 *)(local_e8 + 8) = s_DELETE_FROM_plugins_WHERE_plugin_100a49358._8_8_;
      *(undefined8 *)local_e8 = uVar4;
      *(undefined8 *)(local_e8 + 0x18) = uVar12;
      *(undefined8 *)(local_e8 + 0x10) = uVar11;
      local_e8[0xd1] = '\0';
      FUN_1005a7f64(auStack_b0,lVar14,&local_e8,local_80);
      if (lStack_d8 < 0) {
        operator_delete(local_e8);
      }
      FUN_1005a4e00(local_80);
      FUN_100787c3c(auStack_b0,local_80);
      FUN_1005a4e00(local_80);
      if (local_98 == '\x01') {
        FUN_1007879a4(auStack_b0);
      }
    }
    FUN_1007839d4(auStack_90,local_80);
    FUN_1005a4e00(local_80);
    thunk_FUN_100785fdc(auStack_90);
  }
  return;
}

