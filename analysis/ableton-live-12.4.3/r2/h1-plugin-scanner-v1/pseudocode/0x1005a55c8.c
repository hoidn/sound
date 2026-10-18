
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1005a55c8(undefined8 *param_1,long *param_2,undefined4 param_3,undefined8 *param_4,
                  int param_5)

{
  undefined8 uVar1;
  undefined8 uVar2;
  undefined8 uVar3;
  int iVar4;
  char *pcVar5;
  long lVar6;
  char *local_f0;
  undefined8 *local_e8;
  ulong uStack_e0;
  uint local_d8;
  char *local_d0;
  undefined8 local_c8;
  long lStack_c0;
  char *local_b8;
  undefined4 local_b0;
  undefined4 uStack_ac;
  undefined8 uStack_a8;
  uint local_a0;
  undefined1 auStack_98 [24];
  char local_80;
  undefined1 auStack_78 [16];
  undefined4 local_68 [2];
  undefined8 local_60;
  undefined1 uStack_51;
  
  iVar4 = (**(code **)(*param_2 + 0x10))();
  param_1[1] = 0;
  param_1[2] = 0;
  *param_1 = 0;
  if (iVar4 != 0) {
    local_68[0] = 0;
    local_60 = std::system_category();
    FUN_100783784(auStack_78,param_2[1],1,local_68);
    local_b0 = param_3;
    if (param_5 == 0) {
      lVar6 = param_2[1];
      pcVar5 = operator_new(0x180);
      uStack_e0 = _UNK_1009d2768;
      local_e8 = _DAT_1009d2760;
      local_f0 = pcVar5;
      _memcpy(pcVar5,
              "SELECT p.plugin_id, p.module_id, pm.path, pd.relpath, p.name, p.vendor, p.scanstate,        p.version, p.sdk_version, p.dev_identifier, p.enabled, pd.id, p.flags,        pm.processor, p.subcategories   FROM plugins AS p        JOIN plugin_modules AS pm ON (p.module_id = pm.module_id)        JOIN plugin_domains AS pd ON (p.module_id = pd.module_id)  WHERE pm.module_id = :module_id "
              ,0x17f);
      pcVar5[0x17f] = '\0';
      local_b8 = ":module_id";
      local_a0 = 2;
      FUN_1005a5a48(auStack_98,lVar6,&local_f0,local_68,&local_b8);
      if (local_a0 != 0xffffffff) {
        (*(code *)(&PTR_FUN_100b6daf0)[local_a0])(&local_d0,&local_b0);
      }
      if ((long)uStack_e0 < 0) {
        operator_delete(local_f0);
      }
      FUN_1005a4e00(local_68);
      FUN_1005a5bc0(&local_b8,auStack_98);
      pcVar5 = (char *)CONCAT44(uStack_ac,local_b0);
      param_1[2] = uStack_a8;
      param_1[1] = pcVar5;
      *param_1 = local_b8;
      lVar6 = 0;
      if (pcVar5 != local_b8) {
        lVar6 = LZCOUNT(((long)pcVar5 - (long)local_b8 >> 3) * -0xf0f0f0f0f0f0f0f) * -2 + 0x7e;
      }
      FUN_1005cfc70(local_b8,pcVar5,lVar6,1);
    }
    else {
      lVar6 = param_2[1];
      local_f0 = operator_new(0x38);
      uStack_e0 = _UNK_1009a8e08;
      local_e8 = _DAT_1009a8e00;
      local_f0[0x30] = 'd';
      uVar3 = s_DELETE_FROM_plugins_WHERE_module_100a49503._24_8_;
      uVar2 = s_DELETE_FROM_plugins_WHERE_module_100a49503._16_8_;
      uVar1 = s_DELETE_FROM_plugins_WHERE_module_100a49503._0_8_;
      local_f0[0x31] = '\0';
      *(undefined8 *)(local_f0 + 8) = s_DELETE_FROM_plugins_WHERE_module_100a49503._8_8_;
      *(undefined8 *)local_f0 = uVar1;
      *(undefined8 *)(local_f0 + 0x18) = uVar3;
      *(undefined8 *)(local_f0 + 0x10) = uVar2;
      uVar1 = s_DELETE_FROM_plugins_WHERE_module_100a49503._32_8_;
      *(undefined8 *)(local_f0 + 0x28) = s_DELETE_FROM_plugins_WHERE_module_100a49503._40_8_;
      *(undefined8 *)(local_f0 + 0x20) = uVar1;
      local_b8 = ":module_id";
      local_a0 = 2;
      FUN_1005a5a48(auStack_98,lVar6,&local_f0,local_68,&local_b8);
      if (local_a0 != 0xffffffff) {
        (*(code *)(&PTR_FUN_100b6daf0)[local_a0])(&local_d0,&local_b0);
      }
      if ((long)uStack_e0 < 0) {
        operator_delete(local_f0);
      }
      FUN_1005a4e00(local_68);
      FUN_100787c3c(auStack_98,local_68);
      FUN_1005a4e00(local_68);
    }
    if (local_80 == '\x01') {
      FUN_1007879a4(auStack_98);
    }
    lVar6 = param_2[1];
    local_d0 = operator_new(0x70);
    uVar3 = s_UPDATE_plugin_modules_SET_finger_100a49f49._80_8_;
    uVar2 = s_UPDATE_plugin_modules_SET_finger_100a49f49._64_8_;
    lStack_c0 = _UNK_1009d27e8;
    local_c8 = _DAT_1009d27e0;
    uVar1 = CONCAT53(s_UPDATE_plugin_modules_SET_finger_100a49f49._91_5_,
                     s_UPDATE_plugin_modules_SET_finger_100a49f49._88_3_);
    *(undefined8 *)(local_d0 + 0x48) = s_UPDATE_plugin_modules_SET_finger_100a49f49._72_8_;
    *(undefined8 *)(local_d0 + 0x40) = uVar2;
    *(undefined8 *)(local_d0 + 0x58) = uVar1;
    *(undefined8 *)(local_d0 + 0x50) = uVar3;
    uVar1 = CONCAT35(s_UPDATE_plugin_modules_SET_finger_100a49f49._96_3_,
                     s_UPDATE_plugin_modules_SET_finger_100a49f49._91_5_);
    *(undefined8 *)(local_d0 + 99) = s_UPDATE_plugin_modules_SET_finger_100a49f49._99_8_;
    *(undefined8 *)(local_d0 + 0x5b) = uVar1;
    uVar3 = s_UPDATE_plugin_modules_SET_finger_100a49f49._24_8_;
    uVar2 = s_UPDATE_plugin_modules_SET_finger_100a49f49._16_8_;
    uVar1 = s_UPDATE_plugin_modules_SET_finger_100a49f49._0_8_;
    *(undefined8 *)(local_d0 + 8) = s_UPDATE_plugin_modules_SET_finger_100a49f49._8_8_;
    *(undefined8 *)local_d0 = uVar1;
    *(undefined8 *)(local_d0 + 0x18) = uVar3;
    *(undefined8 *)(local_d0 + 0x10) = uVar2;
    uVar3 = s_UPDATE_plugin_modules_SET_finger_100a49f49._56_8_;
    uVar2 = s_UPDATE_plugin_modules_SET_finger_100a49f49._48_8_;
    uVar1 = s_UPDATE_plugin_modules_SET_finger_100a49f49._32_8_;
    *(undefined8 *)(local_d0 + 0x28) = s_UPDATE_plugin_modules_SET_finger_100a49f49._40_8_;
    *(undefined8 *)(local_d0 + 0x20) = uVar1;
    *(undefined8 *)(local_d0 + 0x38) = uVar3;
    *(undefined8 *)(local_d0 + 0x30) = uVar2;
    local_d0[0x6b] = '\0';
    local_b8 = ":module_id";
    local_a0 = 2;
    uStack_e0 = param_4[1];
    local_e8 = (undefined8 *)*param_4;
    if (-1 < (char)*(byte *)((long)param_4 + 0x17)) {
      uStack_e0 = (ulong)*(byte *)((long)param_4 + 0x17);
      local_e8 = param_4;
    }
    local_f0 = ":fingerprint";
    local_d8 = 5;
    local_b0 = param_3;
    FUN_1005a6424(auStack_98,lVar6,&local_d0,local_68,&local_b8,&local_f0);
    if (local_d8 != 0xffffffff) {
      (*(code *)(&PTR_FUN_100b6daf0)[local_d8])(&uStack_51,&local_e8);
    }
    if (local_a0 != 0xffffffff) {
      (*(code *)(&PTR_FUN_100b6daf0)[local_a0])(&local_f0,&local_b0);
    }
    if (lStack_c0 < 0) {
      operator_delete(local_d0);
    }
    FUN_1005a4e00(local_68);
    FUN_100787c3c(auStack_98,local_68);
    FUN_1005a4e00(local_68);
    if (local_80 == '\x01') {
      FUN_1007879a4(auStack_98);
    }
    FUN_1007839d4(auStack_78,local_68);
    FUN_1005a4e00(local_68);
    thunk_FUN_100785fdc(auStack_78);
  }
  return;
}

