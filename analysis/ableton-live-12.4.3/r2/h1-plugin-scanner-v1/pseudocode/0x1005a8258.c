
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1005a8258(long *param_1,undefined4 param_2)

{
  undefined8 uVar1;
  undefined8 uVar2;
  undefined8 uVar3;
  int iVar4;
  char *pcVar5;
  long lVar6;
  char *local_c0;
  undefined4 local_b8 [4];
  uint local_a8;
  char *local_a0;
  undefined8 local_98;
  long lStack_90;
  undefined1 auStack_88 [24];
  char local_70;
  undefined1 auStack_68 [16];
  undefined4 local_58 [2];
  undefined8 local_50;
  undefined1 uStack_41;
  
  iVar4 = (**(code **)(*param_1 + 0x10))();
  if (iVar4 != 0) {
    local_58[0] = 0;
    local_50 = std::system_category();
    FUN_100783784(auStack_68,param_1[1],1,local_58);
    FUN_1005a4e00(local_58);
    lVar6 = param_1[1];
    local_a0 = operator_new(200);
    uVar3 = s_UPDATE_plugins_SET_scanstate___2_100a4a351._176_8_;
    uVar2 = s_UPDATE_plugins_SET_scanstate___2_100a4a351._160_8_;
    lStack_90 = _UNK_1009d2828;
    local_98 = _DAT_1009d2820;
    uVar1 = CONCAT17(s_UPDATE_plugins_SET_scanstate___2_100a4a351[0xbf],
                     s_UPDATE_plugins_SET_scanstate___2_100a4a351._184_7_);
    *(undefined8 *)(local_a0 + 0xa8) = s_UPDATE_plugins_SET_scanstate___2_100a4a351._168_8_;
    *(undefined8 *)(local_a0 + 0xa0) = uVar2;
    *(undefined8 *)(local_a0 + 0xb8) = uVar1;
    *(undefined8 *)(local_a0 + 0xb0) = uVar3;
    *(ulong *)(local_a0 + 0xbf) =
         CONCAT71(s_UPDATE_plugins_SET_scanstate___2_100a4a351._192_7_,
                  s_UPDATE_plugins_SET_scanstate___2_100a4a351[0xbf]);
    uVar3 = s_UPDATE_plugins_SET_scanstate___2_100a4a351._120_8_;
    uVar2 = s_UPDATE_plugins_SET_scanstate___2_100a4a351._112_8_;
    uVar1 = s_UPDATE_plugins_SET_scanstate___2_100a4a351._96_8_;
    *(undefined8 *)(local_a0 + 0x68) = s_UPDATE_plugins_SET_scanstate___2_100a4a351._104_8_;
    *(undefined8 *)(local_a0 + 0x60) = uVar1;
    *(undefined8 *)(local_a0 + 0x78) = uVar3;
    *(undefined8 *)(local_a0 + 0x70) = uVar2;
    uVar3 = s_UPDATE_plugins_SET_scanstate___2_100a4a351._152_8_;
    uVar2 = s_UPDATE_plugins_SET_scanstate___2_100a4a351._144_8_;
    uVar1 = s_UPDATE_plugins_SET_scanstate___2_100a4a351._128_8_;
    *(undefined8 *)(local_a0 + 0x88) = s_UPDATE_plugins_SET_scanstate___2_100a4a351._136_8_;
    *(undefined8 *)(local_a0 + 0x80) = uVar1;
    *(undefined8 *)(local_a0 + 0x98) = uVar3;
    *(undefined8 *)(local_a0 + 0x90) = uVar2;
    uVar3 = s_UPDATE_plugins_SET_scanstate___2_100a4a351._56_8_;
    uVar2 = s_UPDATE_plugins_SET_scanstate___2_100a4a351._48_8_;
    uVar1 = s_UPDATE_plugins_SET_scanstate___2_100a4a351._32_8_;
    *(undefined8 *)(local_a0 + 0x28) = s_UPDATE_plugins_SET_scanstate___2_100a4a351._40_8_;
    *(undefined8 *)(local_a0 + 0x20) = uVar1;
    *(undefined8 *)(local_a0 + 0x38) = uVar3;
    *(undefined8 *)(local_a0 + 0x30) = uVar2;
    uVar3 = s_UPDATE_plugins_SET_scanstate___2_100a4a351._88_8_;
    uVar2 = s_UPDATE_plugins_SET_scanstate___2_100a4a351._80_8_;
    uVar1 = s_UPDATE_plugins_SET_scanstate___2_100a4a351._64_8_;
    *(undefined8 *)(local_a0 + 0x48) = s_UPDATE_plugins_SET_scanstate___2_100a4a351._72_8_;
    *(undefined8 *)(local_a0 + 0x40) = uVar1;
    *(undefined8 *)(local_a0 + 0x58) = uVar3;
    *(undefined8 *)(local_a0 + 0x50) = uVar2;
    uVar3 = s_UPDATE_plugins_SET_scanstate___2_100a4a351._24_8_;
    uVar2 = s_UPDATE_plugins_SET_scanstate___2_100a4a351._16_8_;
    uVar1 = s_UPDATE_plugins_SET_scanstate___2_100a4a351._0_8_;
    *(undefined8 *)(local_a0 + 8) = s_UPDATE_plugins_SET_scanstate___2_100a4a351._8_8_;
    *(undefined8 *)local_a0 = uVar1;
    *(undefined8 *)(local_a0 + 0x18) = uVar3;
    *(undefined8 *)(local_a0 + 0x10) = uVar2;
    local_a0[199] = '\0';
    local_c0 = ":processor_mask";
    local_a8 = 2;
    local_b8[0] = param_2;
    FUN_1005a5a48(auStack_88,lVar6,&local_a0,local_58,&local_c0);
    if (local_a8 != 0xffffffff) {
      (*(code *)(&PTR_FUN_100b6daf0)[local_a8])(&uStack_41,local_b8);
    }
    if (lStack_90 < 0) {
      operator_delete(local_a0);
    }
    FUN_1005a4e00(local_58);
    FUN_100787c3c(auStack_88,local_58);
    FUN_1005a4e00(local_58);
    if (local_70 == '\x01') {
      FUN_1007879a4(auStack_88);
    }
    lVar6 = param_1[1];
    pcVar5 = operator_new(0x188);
    lStack_90 = _UNK_1009d2838;
    local_98 = _DAT_1009d2830;
    local_a0 = pcVar5;
    _memcpy(pcVar5,
            "UPDATE plugins    SET scanstate = 4  WHERE plugin_id IN (SELECT plugin_id                        FROM plugins                       WHERE scanstate = 0                         AND module_id IN (SELECT module_id                                             FROM plugin_modules                                            WHERE processor & :processor_mask <> 0)                       LIMIT 1)"
            ,0x184);
    pcVar5[0x184] = '\0';
    local_c0 = ":processor_mask";
    local_a8 = 2;
    local_b8[0] = param_2;
    FUN_1005a5a48(auStack_88,lVar6,&local_a0,local_58,&local_c0);
    if (local_a8 != 0xffffffff) {
      (*(code *)(&PTR_FUN_100b6daf0)[local_a8])(&uStack_41,local_b8);
    }
    if (lStack_90 < 0) {
      operator_delete(local_a0);
    }
    FUN_1005a4e00(local_58);
    FUN_100787c3c(auStack_88,local_58);
    FUN_1005a4e00(local_58);
    if (local_70 == '\x01') {
      FUN_1007879a4(auStack_88);
    }
    lVar6 = param_1[1];
    local_a0 = operator_new(0xa0);
    uVar3 = s_UPDATE_plugin_modules_SET_scanst_100a4a2b1._120_8_;
    uVar2 = s_UPDATE_plugin_modules_SET_scanst_100a4a2b1._112_8_;
    uVar1 = s_UPDATE_plugin_modules_SET_scanst_100a4a2b1._96_8_;
    lStack_90 = _UNK_1009d2808;
    local_98 = _DAT_1009d2800;
    *(undefined8 *)(local_a0 + 0x68) = s_UPDATE_plugin_modules_SET_scanst_100a4a2b1._104_8_;
    *(undefined8 *)(local_a0 + 0x60) = uVar1;
    *(undefined8 *)(local_a0 + 0x78) = uVar3;
    *(undefined8 *)(local_a0 + 0x70) = uVar2;
    uVar1 = s_UPDATE_plugin_modules_SET_scanst_100a4a2b1._128_8_;
    *(ulong *)(local_a0 + 0x88) =
         CONCAT17(s_UPDATE_plugin_modules_SET_scanst_100a4a2b1[0x8f],
                  s_UPDATE_plugin_modules_SET_scanst_100a4a2b1._136_7_);
    *(undefined8 *)(local_a0 + 0x80) = uVar1;
    uVar1 = CONCAT71(s_UPDATE_plugin_modules_SET_scanst_100a4a2b1._144_7_,
                     s_UPDATE_plugin_modules_SET_scanst_100a4a2b1[0x8f]);
    *(undefined8 *)(local_a0 + 0x97) = s_UPDATE_plugin_modules_SET_scanst_100a4a2b1._151_8_;
    *(undefined8 *)(local_a0 + 0x8f) = uVar1;
    uVar3 = s_UPDATE_plugin_modules_SET_scanst_100a4a2b1._56_8_;
    uVar2 = s_UPDATE_plugin_modules_SET_scanst_100a4a2b1._48_8_;
    uVar1 = s_UPDATE_plugin_modules_SET_scanst_100a4a2b1._32_8_;
    *(undefined8 *)(local_a0 + 0x28) = s_UPDATE_plugin_modules_SET_scanst_100a4a2b1._40_8_;
    *(undefined8 *)(local_a0 + 0x20) = uVar1;
    *(undefined8 *)(local_a0 + 0x38) = uVar3;
    *(undefined8 *)(local_a0 + 0x30) = uVar2;
    uVar3 = s_UPDATE_plugin_modules_SET_scanst_100a4a2b1._88_8_;
    uVar2 = s_UPDATE_plugin_modules_SET_scanst_100a4a2b1._80_8_;
    uVar1 = s_UPDATE_plugin_modules_SET_scanst_100a4a2b1._64_8_;
    *(undefined8 *)(local_a0 + 0x48) = s_UPDATE_plugin_modules_SET_scanst_100a4a2b1._72_8_;
    *(undefined8 *)(local_a0 + 0x40) = uVar1;
    *(undefined8 *)(local_a0 + 0x58) = uVar3;
    *(undefined8 *)(local_a0 + 0x50) = uVar2;
    uVar3 = s_UPDATE_plugin_modules_SET_scanst_100a4a2b1._24_8_;
    uVar2 = s_UPDATE_plugin_modules_SET_scanst_100a4a2b1._16_8_;
    uVar1 = s_UPDATE_plugin_modules_SET_scanst_100a4a2b1._0_8_;
    *(undefined8 *)(local_a0 + 8) = s_UPDATE_plugin_modules_SET_scanst_100a4a2b1._8_8_;
    *(undefined8 *)local_a0 = uVar1;
    *(undefined8 *)(local_a0 + 0x18) = uVar3;
    *(undefined8 *)(local_a0 + 0x10) = uVar2;
    local_a0[0x9f] = '\0';
    local_c0 = ":processor_mask";
    local_a8 = 2;
    local_b8[0] = param_2;
    FUN_1005a5a48(auStack_88,lVar6,&local_a0,local_58,&local_c0);
    if (local_a8 != 0xffffffff) {
      (*(code *)(&PTR_FUN_100b6daf0)[local_a8])(&uStack_41,local_b8);
    }
    if (lStack_90 < 0) {
      operator_delete(local_a0);
    }
    FUN_1005a4e00(local_58);
    FUN_100787c3c(auStack_88,local_58);
    FUN_1005a4e00(local_58);
    if (local_70 == '\x01') {
      FUN_1007879a4(auStack_88);
    }
    lVar6 = param_1[1];
    pcVar5 = operator_new(0x128);
    lStack_90 = _UNK_1009d27f8;
    local_98 = _DAT_1009d27f0;
    local_a0 = pcVar5;
    _memcpy(pcVar5,
            "UPDATE plugin_modules    SET scanstate = 4  WHERE module_id IN (SELECT module_id                        FROM plugin_modules                       WHERE scanstate = 0                       LIMIT 1)    AND module_id NOT IN (SELECT module_id FROM plugins)    AND processor & :processor_mask <> 0"
            ,0x124);
    pcVar5[0x124] = '\0';
    local_c0 = ":processor_mask";
    local_a8 = 2;
    local_b8[0] = param_2;
    FUN_1005a5a48(auStack_88,lVar6,&local_a0,local_58,&local_c0);
    if (local_a8 != 0xffffffff) {
      (*(code *)(&PTR_FUN_100b6daf0)[local_a8])(&uStack_41,local_b8);
    }
    if (lStack_90 < 0) {
      operator_delete(local_a0);
    }
    FUN_1005a4e00(local_58);
    FUN_100787c3c(auStack_88,local_58);
    FUN_1005a4e00(local_58);
    if (local_70 == '\x01') {
      FUN_1007879a4(auStack_88);
    }
    lVar6 = param_1[1];
    pcVar5 = operator_new(0x180);
    lStack_90 = _UNK_1009d2848;
    local_98 = _DAT_1009d2840;
    local_a0 = pcVar5;
    _memcpy(pcVar5,
            "UPDATE plugin_modules    SET scanstate = 2  WHERE scanstate IN (0, 4)    AND module_ID IN (SELECT module_id                        FROM plugins                       WHERE scanstate IN (2, 3)                      EXCEPT                      SELECT module_id                        FROM plugins                       WHERE scanstate IN (1, 0))    AND processor & :processor_mask <> 0"
            ,0x17e);
    pcVar5[0x17e] = '\0';
    local_c0 = ":processor_mask";
    local_a8 = 2;
    local_b8[0] = param_2;
    FUN_1005a5a48(auStack_88,lVar6,&local_a0,local_58,&local_c0);
    if (local_a8 != 0xffffffff) {
      (*(code *)(&PTR_FUN_100b6daf0)[local_a8])(&uStack_41,local_b8);
    }
    if (lStack_90 < 0) {
      operator_delete(local_a0);
    }
    FUN_1005a4e00(local_58);
    FUN_100787c3c(auStack_88,local_58);
    FUN_1005a4e00(local_58);
    if (local_70 == '\x01') {
      FUN_1007879a4(auStack_88);
    }
    FUN_1007839d4(auStack_68,local_58);
    FUN_1005a4e00(local_58);
    thunk_FUN_100785fdc(auStack_68);
  }
  return;
}

