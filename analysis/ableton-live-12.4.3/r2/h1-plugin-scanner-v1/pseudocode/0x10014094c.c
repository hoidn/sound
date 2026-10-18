
/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_10014094c(char *param_1,undefined8 param_2,int param_3)

{
  undefined8 *******pppppppuVar1;
  undefined8 uVar2;
  undefined8 uVar3;
  char *pcVar4;
  undefined8 *puVar5;
  undefined8 uVar6;
  undefined8 *******local_58 [2];
  char local_41;
  void *local_40;
  char acStack_38 [8];
  undefined4 local_30;
  undefined1 local_2c;
  char local_29;
  
  if (param_3 < 4) {
    if (param_3 == 1) {
      pcVar4 = operator_new(0x28);
      *(char **)param_1 = pcVar4;
      uVar6 = _DAT_1009a8e20;
      *(undefined8 *)(param_1 + 0x10) = _UNK_1009a8e28;
      *(undefined8 *)(param_1 + 8) = uVar6;
      pcVar4[0x20] = 'n';
      uVar3 = s_Plugin_doesn_t_publish_a_functio_100a10a7c._24_8_;
      uVar2 = s_Plugin_doesn_t_publish_a_functio_100a10a7c._16_8_;
      uVar6 = s_Plugin_doesn_t_publish_a_functio_100a10a7c._0_8_;
      pcVar4[0x21] = '\0';
      *(undefined8 *)(pcVar4 + 8) = s_Plugin_doesn_t_publish_a_functio_100a10a7c._8_8_;
      *(undefined8 *)pcVar4 = uVar6;
      *(undefined8 *)(pcVar4 + 0x18) = uVar3;
      *(undefined8 *)(pcVar4 + 0x10) = uVar2;
      return;
    }
    if (param_3 == 2) {
      pcVar4 = operator_new(0x28);
      *(char **)param_1 = pcVar4;
      uVar6 = _DAT_1009a8e10;
      *(undefined8 *)(param_1 + 0x10) = _UNK_1009a8e18;
      *(undefined8 *)(param_1 + 8) = uVar6;
      pcVar4[0x1f] = 't';
      uVar3 = s_Plugin_doesn_t_have_a_main_funct_100a10a9e._24_8_;
      uVar2 = s_Plugin_doesn_t_have_a_main_funct_100a10a9e._16_8_;
      uVar6 = s_Plugin_doesn_t_have_a_main_funct_100a10a9e._0_8_;
      pcVar4[0x20] = 'i';
      pcVar4[0x21] = 'o';
      pcVar4[0x22] = 'n';
      *(undefined8 *)(pcVar4 + 8) = s_Plugin_doesn_t_have_a_main_funct_100a10a9e._8_8_;
      *(undefined8 *)pcVar4 = uVar6;
      *(undefined8 *)(pcVar4 + 0x18) = uVar3;
      *(undefined8 *)(pcVar4 + 0x10) = uVar2;
      pcVar4[0x23] = '\0';
      return;
    }
    if (param_3 == 3) {
      pcVar4 = operator_new(0x38);
      *(char **)param_1 = pcVar4;
      uVar6 = _DAT_1009a8e00;
      *(undefined8 *)(param_1 + 0x10) = _UNK_1009a8e08;
      *(undefined8 *)(param_1 + 8) = uVar6;
      pcVar4[0x30] = 't';
      uVar3 = s_the_plugin_main_function_didn_t_r_100a10ac2._24_8_;
      uVar2 = s_the_plugin_main_function_didn_t_r_100a10ac2._16_8_;
      uVar6 = s_the_plugin_main_function_didn_t_r_100a10ac2._0_8_;
      pcVar4[0x31] = '\0';
      *(undefined8 *)(pcVar4 + 8) = s_the_plugin_main_function_didn_t_r_100a10ac2._8_8_;
      *(undefined8 *)pcVar4 = uVar6;
      *(undefined8 *)(pcVar4 + 0x18) = uVar3;
      *(undefined8 *)(pcVar4 + 0x10) = uVar2;
      uVar6 = s_the_plugin_main_function_didn_t_r_100a10ac2._32_8_;
      *(undefined8 *)(pcVar4 + 0x28) = s_the_plugin_main_function_didn_t_r_100a10ac2._40_8_;
      *(undefined8 *)(pcVar4 + 0x20) = uVar6;
      return;
    }
  }
  else {
    if (param_3 == 4) {
      pcVar4 = operator_new(0x20);
      *(char **)param_1 = pcVar4;
      uVar6 = _DAT_1009a8df0;
      *(undefined8 *)(param_1 + 0x10) = _UNK_1009a8df8;
      *(undefined8 *)(param_1 + 8) = uVar6;
      uVar6 = s_plugin_has_an_invalid_signature_100a10af4._0_8_;
      *(ulong *)(pcVar4 + 8) =
           CONCAT17(s_plugin_has_an_invalid_signature_100a10af4[0xf],
                    s_plugin_has_an_invalid_signature_100a10af4._8_7_);
      *(undefined8 *)pcVar4 = uVar6;
      uVar6 = CONCAT71(s_plugin_has_an_invalid_signature_100a10af4._16_7_,
                       s_plugin_has_an_invalid_signature_100a10af4[0xf]);
      *(undefined8 *)(pcVar4 + 0x17) = s_plugin_has_an_invalid_signature_100a10af4._23_8_;
      *(undefined8 *)(pcVar4 + 0xf) = uVar6;
      pcVar4[0x1f] = '\0';
      return;
    }
    if (param_3 == 5) {
      param_1[0x17] = '\x14';
      param_1[0x10] = 'u';
      uVar6 = s_couldn_t_load_plugin_100a10b14._0_8_;
      param_1[0x11] = 'g';
      param_1[0x12] = 'i';
      param_1[0x13] = 'n';
      *(undefined8 *)(param_1 + 8) = s_couldn_t_load_plugin_100a10b14._8_8_;
      *(undefined8 *)param_1 = uVar6;
      param_1[0x14] = '\0';
      return;
    }
    if (param_3 == 6) {
      param_1[0x17] = '\x11';
      param_1[0x10] = 't';
      uVar6 = s_bad_bundle_layout_100a10b29._0_8_;
      param_1[0x11] = '\0';
      *(undefined8 *)(param_1 + 8) = s_bad_bundle_layout_100a10b29._8_8_;
      *(undefined8 *)param_1 = uVar6;
      return;
    }
  }
  local_29 = '\x14';
  local_30 = 0x203a6564;
  acStack_38 = (char  [8])s_Unknown_error_code__100a10b3b._8_8_;
  local_40 = (void *)s_Unknown_error_code__100a10b3b._0_8_;
  local_2c = 0;
  std::to_string(param_3);
  pppppppuVar1 = local_58[0];
  if (-1 < local_41) {
    pppppppuVar1 = local_58;
  }
  puVar5 = (undefined8 *)std::string::append((char *)&local_40,(ulong)pppppppuVar1);
  uVar6 = *puVar5;
  *(undefined8 *)(param_1 + 8) = puVar5[1];
  *(undefined8 *)param_1 = uVar6;
  *(undefined8 *)(param_1 + 0x10) = puVar5[2];
  puVar5[1] = 0;
  puVar5[2] = 0;
  *puVar5 = 0;
  if (local_41 < '\0') {
    operator_delete(local_58[0]);
  }
  if (-1 < local_29) {
    s_Unknown_error_code__100a10b3b[8] = (char)s_Unknown_error_code__100a10b3b._8_8_;
    s_Unknown_error_code__100a10b3b[9] = SUB81(s_Unknown_error_code__100a10b3b._8_8_,1);
    s_Unknown_error_code__100a10b3b[10] = SUB81(s_Unknown_error_code__100a10b3b._8_8_,2);
    s_Unknown_error_code__100a10b3b[0xb] = SUB81(s_Unknown_error_code__100a10b3b._8_8_,3);
    s_Unknown_error_code__100a10b3b[0xc] = SUB81(s_Unknown_error_code__100a10b3b._8_8_,4);
    s_Unknown_error_code__100a10b3b[0xd] = SUB81(s_Unknown_error_code__100a10b3b._8_8_,5);
    s_Unknown_error_code__100a10b3b[0xe] = SUB81(s_Unknown_error_code__100a10b3b._8_8_,6);
    s_Unknown_error_code__100a10b3b[0xf] = SUB81(s_Unknown_error_code__100a10b3b._8_8_,7);
    s_Unknown_error_code__100a10b3b[0] = (char)s_Unknown_error_code__100a10b3b._0_8_;
    s_Unknown_error_code__100a10b3b[1] = SUB81(s_Unknown_error_code__100a10b3b._0_8_,1);
    s_Unknown_error_code__100a10b3b[2] = SUB81(s_Unknown_error_code__100a10b3b._0_8_,2);
    s_Unknown_error_code__100a10b3b[3] = SUB81(s_Unknown_error_code__100a10b3b._0_8_,3);
    s_Unknown_error_code__100a10b3b[4] = SUB81(s_Unknown_error_code__100a10b3b._0_8_,4);
    s_Unknown_error_code__100a10b3b[5] = SUB81(s_Unknown_error_code__100a10b3b._0_8_,5);
    s_Unknown_error_code__100a10b3b[6] = SUB81(s_Unknown_error_code__100a10b3b._0_8_,6);
    s_Unknown_error_code__100a10b3b[7] = SUB81(s_Unknown_error_code__100a10b3b._0_8_,7);
    s_bad_bundle_layout_100a10b29[8] = (char)s_bad_bundle_layout_100a10b29._8_8_;
    s_bad_bundle_layout_100a10b29[9] = SUB81(s_bad_bundle_layout_100a10b29._8_8_,1);
    s_bad_bundle_layout_100a10b29[10] = SUB81(s_bad_bundle_layout_100a10b29._8_8_,2);
    s_bad_bundle_layout_100a10b29[0xb] = SUB81(s_bad_bundle_layout_100a10b29._8_8_,3);
    s_bad_bundle_layout_100a10b29[0xc] = SUB81(s_bad_bundle_layout_100a10b29._8_8_,4);
    s_bad_bundle_layout_100a10b29[0xd] = SUB81(s_bad_bundle_layout_100a10b29._8_8_,5);
    s_bad_bundle_layout_100a10b29[0xe] = SUB81(s_bad_bundle_layout_100a10b29._8_8_,6);
    s_bad_bundle_layout_100a10b29[0xf] = SUB81(s_bad_bundle_layout_100a10b29._8_8_,7);
    s_bad_bundle_layout_100a10b29[0] = (char)s_bad_bundle_layout_100a10b29._0_8_;
    s_bad_bundle_layout_100a10b29[1] = SUB81(s_bad_bundle_layout_100a10b29._0_8_,1);
    s_bad_bundle_layout_100a10b29[2] = SUB81(s_bad_bundle_layout_100a10b29._0_8_,2);
    s_bad_bundle_layout_100a10b29[3] = SUB81(s_bad_bundle_layout_100a10b29._0_8_,3);
    s_bad_bundle_layout_100a10b29[4] = SUB81(s_bad_bundle_layout_100a10b29._0_8_,4);
    s_bad_bundle_layout_100a10b29[5] = SUB81(s_bad_bundle_layout_100a10b29._0_8_,5);
    s_bad_bundle_layout_100a10b29[6] = SUB81(s_bad_bundle_layout_100a10b29._0_8_,6);
    s_bad_bundle_layout_100a10b29[7] = SUB81(s_bad_bundle_layout_100a10b29._0_8_,7);
    s_couldn_t_load_plugin_100a10b14[8] = (char)s_couldn_t_load_plugin_100a10b14._8_8_;
    s_couldn_t_load_plugin_100a10b14[9] = SUB81(s_couldn_t_load_plugin_100a10b14._8_8_,1);
    s_couldn_t_load_plugin_100a10b14[10] = SUB81(s_couldn_t_load_plugin_100a10b14._8_8_,2);
    s_couldn_t_load_plugin_100a10b14[0xb] = SUB81(s_couldn_t_load_plugin_100a10b14._8_8_,3);
    s_couldn_t_load_plugin_100a10b14[0xc] = SUB81(s_couldn_t_load_plugin_100a10b14._8_8_,4);
    s_couldn_t_load_plugin_100a10b14[0xd] = SUB81(s_couldn_t_load_plugin_100a10b14._8_8_,5);
    s_couldn_t_load_plugin_100a10b14[0xe] = SUB81(s_couldn_t_load_plugin_100a10b14._8_8_,6);
    s_couldn_t_load_plugin_100a10b14[0xf] = SUB81(s_couldn_t_load_plugin_100a10b14._8_8_,7);
    s_couldn_t_load_plugin_100a10b14[0] = (char)s_couldn_t_load_plugin_100a10b14._0_8_;
    s_couldn_t_load_plugin_100a10b14[1] = SUB81(s_couldn_t_load_plugin_100a10b14._0_8_,1);
    s_couldn_t_load_plugin_100a10b14[2] = SUB81(s_couldn_t_load_plugin_100a10b14._0_8_,2);
    s_couldn_t_load_plugin_100a10b14[3] = SUB81(s_couldn_t_load_plugin_100a10b14._0_8_,3);
    s_couldn_t_load_plugin_100a10b14[4] = SUB81(s_couldn_t_load_plugin_100a10b14._0_8_,4);
    s_couldn_t_load_plugin_100a10b14[5] = SUB81(s_couldn_t_load_plugin_100a10b14._0_8_,5);
    s_couldn_t_load_plugin_100a10b14[6] = SUB81(s_couldn_t_load_plugin_100a10b14._0_8_,6);
    s_couldn_t_load_plugin_100a10b14[7] = SUB81(s_couldn_t_load_plugin_100a10b14._0_8_,7);
    s_plugin_has_an_invalid_signature_100a10af4[0x17] =
         (char)s_plugin_has_an_invalid_signature_100a10af4._23_8_;
    s_plugin_has_an_invalid_signature_100a10af4[0x18] =
         SUB81(s_plugin_has_an_invalid_signature_100a10af4._23_8_,1);
    s_plugin_has_an_invalid_signature_100a10af4[0x19] =
         SUB81(s_plugin_has_an_invalid_signature_100a10af4._23_8_,2);
    s_plugin_has_an_invalid_signature_100a10af4[0x1a] =
         SUB81(s_plugin_has_an_invalid_signature_100a10af4._23_8_,3);
    s_plugin_has_an_invalid_signature_100a10af4[0x1b] =
         SUB81(s_plugin_has_an_invalid_signature_100a10af4._23_8_,4);
    s_plugin_has_an_invalid_signature_100a10af4[0x1c] =
         SUB81(s_plugin_has_an_invalid_signature_100a10af4._23_8_,5);
    s_plugin_has_an_invalid_signature_100a10af4[0x1d] =
         SUB81(s_plugin_has_an_invalid_signature_100a10af4._23_8_,6);
    s_plugin_has_an_invalid_signature_100a10af4[0x1e] =
         SUB81(s_plugin_has_an_invalid_signature_100a10af4._23_8_,7);
    s_plugin_has_an_invalid_signature_100a10af4[0x10] =
         (char)s_plugin_has_an_invalid_signature_100a10af4._16_7_;
    s_plugin_has_an_invalid_signature_100a10af4[0x11] =
         SUB71(s_plugin_has_an_invalid_signature_100a10af4._16_7_,1);
    s_plugin_has_an_invalid_signature_100a10af4[0x12] =
         SUB71(s_plugin_has_an_invalid_signature_100a10af4._16_7_,2);
    s_plugin_has_an_invalid_signature_100a10af4[0x13] =
         SUB71(s_plugin_has_an_invalid_signature_100a10af4._16_7_,3);
    s_plugin_has_an_invalid_signature_100a10af4[0x14] =
         SUB71(s_plugin_has_an_invalid_signature_100a10af4._16_7_,4);
    s_plugin_has_an_invalid_signature_100a10af4[0x15] =
         SUB71(s_plugin_has_an_invalid_signature_100a10af4._16_7_,5);
    s_plugin_has_an_invalid_signature_100a10af4[0x16] =
         SUB71(s_plugin_has_an_invalid_signature_100a10af4._16_7_,6);
    s_plugin_has_an_invalid_signature_100a10af4[8] =
         (char)s_plugin_has_an_invalid_signature_100a10af4._8_7_;
    s_plugin_has_an_invalid_signature_100a10af4[9] =
         SUB71(s_plugin_has_an_invalid_signature_100a10af4._8_7_,1);
    s_plugin_has_an_invalid_signature_100a10af4[10] =
         SUB71(s_plugin_has_an_invalid_signature_100a10af4._8_7_,2);
    s_plugin_has_an_invalid_signature_100a10af4[0xb] =
         SUB71(s_plugin_has_an_invalid_signature_100a10af4._8_7_,3);
    s_plugin_has_an_invalid_signature_100a10af4[0xc] =
         SUB71(s_plugin_has_an_invalid_signature_100a10af4._8_7_,4);
    s_plugin_has_an_invalid_signature_100a10af4[0xd] =
         SUB71(s_plugin_has_an_invalid_signature_100a10af4._8_7_,5);
    s_plugin_has_an_invalid_signature_100a10af4[0xe] =
         SUB71(s_plugin_has_an_invalid_signature_100a10af4._8_7_,6);
    s_plugin_has_an_invalid_signature_100a10af4[0] =
         (char)s_plugin_has_an_invalid_signature_100a10af4._0_8_;
    s_plugin_has_an_invalid_signature_100a10af4[1] =
         SUB81(s_plugin_has_an_invalid_signature_100a10af4._0_8_,1);
    s_plugin_has_an_invalid_signature_100a10af4[2] =
         SUB81(s_plugin_has_an_invalid_signature_100a10af4._0_8_,2);
    s_plugin_has_an_invalid_signature_100a10af4[3] =
         SUB81(s_plugin_has_an_invalid_signature_100a10af4._0_8_,3);
    s_plugin_has_an_invalid_signature_100a10af4[4] =
         SUB81(s_plugin_has_an_invalid_signature_100a10af4._0_8_,4);
    s_plugin_has_an_invalid_signature_100a10af4[5] =
         SUB81(s_plugin_has_an_invalid_signature_100a10af4._0_8_,5);
    s_plugin_has_an_invalid_signature_100a10af4[6] =
         SUB81(s_plugin_has_an_invalid_signature_100a10af4._0_8_,6);
    s_plugin_has_an_invalid_signature_100a10af4[7] =
         SUB81(s_plugin_has_an_invalid_signature_100a10af4._0_8_,7);
    s_the_plugin_main_function_didn_t_r_100a10ac2[0x28] =
         (char)s_the_plugin_main_function_didn_t_r_100a10ac2._40_8_;
    s_the_plugin_main_function_didn_t_r_100a10ac2[0x29] =
         SUB81(s_the_plugin_main_function_didn_t_r_100a10ac2._40_8_,1);
    s_the_plugin_main_function_didn_t_r_100a10ac2[0x2a] =
         SUB81(s_the_plugin_main_function_didn_t_r_100a10ac2._40_8_,2);
    s_the_plugin_main_function_didn_t_r_100a10ac2[0x2b] =
         SUB81(s_the_plugin_main_function_didn_t_r_100a10ac2._40_8_,3);
    s_the_plugin_main_function_didn_t_r_100a10ac2[0x2c] =
         SUB81(s_the_plugin_main_function_didn_t_r_100a10ac2._40_8_,4);
    s_the_plugin_main_function_didn_t_r_100a10ac2[0x2d] =
         SUB81(s_the_plugin_main_function_didn_t_r_100a10ac2._40_8_,5);
    s_the_plugin_main_function_didn_t_r_100a10ac2[0x2e] =
         SUB81(s_the_plugin_main_function_didn_t_r_100a10ac2._40_8_,6);
    s_the_plugin_main_function_didn_t_r_100a10ac2[0x2f] =
         SUB81(s_the_plugin_main_function_didn_t_r_100a10ac2._40_8_,7);
    s_the_plugin_main_function_didn_t_r_100a10ac2[0x20] =
         (char)s_the_plugin_main_function_didn_t_r_100a10ac2._32_8_;
    s_the_plugin_main_function_didn_t_r_100a10ac2[0x21] =
         SUB81(s_the_plugin_main_function_didn_t_r_100a10ac2._32_8_,1);
    s_the_plugin_main_function_didn_t_r_100a10ac2[0x22] =
         SUB81(s_the_plugin_main_function_didn_t_r_100a10ac2._32_8_,2);
    s_the_plugin_main_function_didn_t_r_100a10ac2[0x23] =
         SUB81(s_the_plugin_main_function_didn_t_r_100a10ac2._32_8_,3);
    s_the_plugin_main_function_didn_t_r_100a10ac2[0x24] =
         SUB81(s_the_plugin_main_function_didn_t_r_100a10ac2._32_8_,4);
    s_the_plugin_main_function_didn_t_r_100a10ac2[0x25] =
         SUB81(s_the_plugin_main_function_didn_t_r_100a10ac2._32_8_,5);
    s_the_plugin_main_function_didn_t_r_100a10ac2[0x26] =
         SUB81(s_the_plugin_main_function_didn_t_r_100a10ac2._32_8_,6);
    s_the_plugin_main_function_didn_t_r_100a10ac2[0x27] =
         SUB81(s_the_plugin_main_function_didn_t_r_100a10ac2._32_8_,7);
    s_the_plugin_main_function_didn_t_r_100a10ac2[0x18] =
         (char)s_the_plugin_main_function_didn_t_r_100a10ac2._24_8_;
    s_the_plugin_main_function_didn_t_r_100a10ac2[0x19] =
         SUB81(s_the_plugin_main_function_didn_t_r_100a10ac2._24_8_,1);
    s_the_plugin_main_function_didn_t_r_100a10ac2[0x1a] =
         SUB81(s_the_plugin_main_function_didn_t_r_100a10ac2._24_8_,2);
    s_the_plugin_main_function_didn_t_r_100a10ac2[0x1b] =
         SUB81(s_the_plugin_main_function_didn_t_r_100a10ac2._24_8_,3);
    s_the_plugin_main_function_didn_t_r_100a10ac2[0x1c] =
         SUB81(s_the_plugin_main_function_didn_t_r_100a10ac2._24_8_,4);
    s_the_plugin_main_function_didn_t_r_100a10ac2[0x1d] =
         SUB81(s_the_plugin_main_function_didn_t_r_100a10ac2._24_8_,5);
    s_the_plugin_main_function_didn_t_r_100a10ac2[0x1e] =
         SUB81(s_the_plugin_main_function_didn_t_r_100a10ac2._24_8_,6);
    s_the_plugin_main_function_didn_t_r_100a10ac2[0x1f] =
         SUB81(s_the_plugin_main_function_didn_t_r_100a10ac2._24_8_,7);
    s_the_plugin_main_function_didn_t_r_100a10ac2[0x10] =
         (char)s_the_plugin_main_function_didn_t_r_100a10ac2._16_8_;
    s_the_plugin_main_function_didn_t_r_100a10ac2[0x11] =
         SUB81(s_the_plugin_main_function_didn_t_r_100a10ac2._16_8_,1);
    s_the_plugin_main_function_didn_t_r_100a10ac2[0x12] =
         SUB81(s_the_plugin_main_function_didn_t_r_100a10ac2._16_8_,2);
    s_the_plugin_main_function_didn_t_r_100a10ac2[0x13] =
         SUB81(s_the_plugin_main_function_didn_t_r_100a10ac2._16_8_,3);
    s_the_plugin_main_function_didn_t_r_100a10ac2[0x14] =
         SUB81(s_the_plugin_main_function_didn_t_r_100a10ac2._16_8_,4);
    s_the_plugin_main_function_didn_t_r_100a10ac2[0x15] =
         SUB81(s_the_plugin_main_function_didn_t_r_100a10ac2._16_8_,5);
    s_the_plugin_main_function_didn_t_r_100a10ac2[0x16] =
         SUB81(s_the_plugin_main_function_didn_t_r_100a10ac2._16_8_,6);
    s_the_plugin_main_function_didn_t_r_100a10ac2[0x17] =
         SUB81(s_the_plugin_main_function_didn_t_r_100a10ac2._16_8_,7);
    s_the_plugin_main_function_didn_t_r_100a10ac2[8] =
         (char)s_the_plugin_main_function_didn_t_r_100a10ac2._8_8_;
    s_the_plugin_main_function_didn_t_r_100a10ac2[9] =
         SUB81(s_the_plugin_main_function_didn_t_r_100a10ac2._8_8_,1);
    s_the_plugin_main_function_didn_t_r_100a10ac2[10] =
         SUB81(s_the_plugin_main_function_didn_t_r_100a10ac2._8_8_,2);
    s_the_plugin_main_function_didn_t_r_100a10ac2[0xb] =
         SUB81(s_the_plugin_main_function_didn_t_r_100a10ac2._8_8_,3);
    s_the_plugin_main_function_didn_t_r_100a10ac2[0xc] =
         SUB81(s_the_plugin_main_function_didn_t_r_100a10ac2._8_8_,4);
    s_the_plugin_main_function_didn_t_r_100a10ac2[0xd] =
         SUB81(s_the_plugin_main_function_didn_t_r_100a10ac2._8_8_,5);
    s_the_plugin_main_function_didn_t_r_100a10ac2[0xe] =
         SUB81(s_the_plugin_main_function_didn_t_r_100a10ac2._8_8_,6);
    s_the_plugin_main_function_didn_t_r_100a10ac2[0xf] =
         SUB81(s_the_plugin_main_function_didn_t_r_100a10ac2._8_8_,7);
    s_the_plugin_main_function_didn_t_r_100a10ac2[0] =
         (char)s_the_plugin_main_function_didn_t_r_100a10ac2._0_8_;
    s_the_plugin_main_function_didn_t_r_100a10ac2[1] =
         SUB81(s_the_plugin_main_function_didn_t_r_100a10ac2._0_8_,1);
    s_the_plugin_main_function_didn_t_r_100a10ac2[2] =
         SUB81(s_the_plugin_main_function_didn_t_r_100a10ac2._0_8_,2);
    s_the_plugin_main_function_didn_t_r_100a10ac2[3] =
         SUB81(s_the_plugin_main_function_didn_t_r_100a10ac2._0_8_,3);
    s_the_plugin_main_function_didn_t_r_100a10ac2[4] =
         SUB81(s_the_plugin_main_function_didn_t_r_100a10ac2._0_8_,4);
    s_the_plugin_main_function_didn_t_r_100a10ac2[5] =
         SUB81(s_the_plugin_main_function_didn_t_r_100a10ac2._0_8_,5);
    s_the_plugin_main_function_didn_t_r_100a10ac2[6] =
         SUB81(s_the_plugin_main_function_didn_t_r_100a10ac2._0_8_,6);
    s_the_plugin_main_function_didn_t_r_100a10ac2[7] =
         SUB81(s_the_plugin_main_function_didn_t_r_100a10ac2._0_8_,7);
    s_Plugin_doesn_t_have_a_main_funct_100a10a9e[0x18] =
         (char)s_Plugin_doesn_t_have_a_main_funct_100a10a9e._24_8_;
    s_Plugin_doesn_t_have_a_main_funct_100a10a9e[0x19] =
         SUB81(s_Plugin_doesn_t_have_a_main_funct_100a10a9e._24_8_,1);
    s_Plugin_doesn_t_have_a_main_funct_100a10a9e[0x1a] =
         SUB81(s_Plugin_doesn_t_have_a_main_funct_100a10a9e._24_8_,2);
    s_Plugin_doesn_t_have_a_main_funct_100a10a9e[0x1b] =
         SUB81(s_Plugin_doesn_t_have_a_main_funct_100a10a9e._24_8_,3);
    s_Plugin_doesn_t_have_a_main_funct_100a10a9e[0x1c] =
         SUB81(s_Plugin_doesn_t_have_a_main_funct_100a10a9e._24_8_,4);
    s_Plugin_doesn_t_have_a_main_funct_100a10a9e[0x1d] =
         SUB81(s_Plugin_doesn_t_have_a_main_funct_100a10a9e._24_8_,5);
    s_Plugin_doesn_t_have_a_main_funct_100a10a9e[0x1e] =
         SUB81(s_Plugin_doesn_t_have_a_main_funct_100a10a9e._24_8_,6);
    s_Plugin_doesn_t_have_a_main_funct_100a10a9e[0x1f] =
         SUB81(s_Plugin_doesn_t_have_a_main_funct_100a10a9e._24_8_,7);
    s_Plugin_doesn_t_have_a_main_funct_100a10a9e[0x10] =
         (char)s_Plugin_doesn_t_have_a_main_funct_100a10a9e._16_8_;
    s_Plugin_doesn_t_have_a_main_funct_100a10a9e[0x11] =
         SUB81(s_Plugin_doesn_t_have_a_main_funct_100a10a9e._16_8_,1);
    s_Plugin_doesn_t_have_a_main_funct_100a10a9e[0x12] =
         SUB81(s_Plugin_doesn_t_have_a_main_funct_100a10a9e._16_8_,2);
    s_Plugin_doesn_t_have_a_main_funct_100a10a9e[0x13] =
         SUB81(s_Plugin_doesn_t_have_a_main_funct_100a10a9e._16_8_,3);
    s_Plugin_doesn_t_have_a_main_funct_100a10a9e[0x14] =
         SUB81(s_Plugin_doesn_t_have_a_main_funct_100a10a9e._16_8_,4);
    s_Plugin_doesn_t_have_a_main_funct_100a10a9e[0x15] =
         SUB81(s_Plugin_doesn_t_have_a_main_funct_100a10a9e._16_8_,5);
    s_Plugin_doesn_t_have_a_main_funct_100a10a9e[0x16] =
         SUB81(s_Plugin_doesn_t_have_a_main_funct_100a10a9e._16_8_,6);
    s_Plugin_doesn_t_have_a_main_funct_100a10a9e[0x17] =
         SUB81(s_Plugin_doesn_t_have_a_main_funct_100a10a9e._16_8_,7);
    s_Plugin_doesn_t_have_a_main_funct_100a10a9e[8] =
         (char)s_Plugin_doesn_t_have_a_main_funct_100a10a9e._8_8_;
    s_Plugin_doesn_t_have_a_main_funct_100a10a9e[9] =
         SUB81(s_Plugin_doesn_t_have_a_main_funct_100a10a9e._8_8_,1);
    s_Plugin_doesn_t_have_a_main_funct_100a10a9e[10] =
         SUB81(s_Plugin_doesn_t_have_a_main_funct_100a10a9e._8_8_,2);
    s_Plugin_doesn_t_have_a_main_funct_100a10a9e[0xb] =
         SUB81(s_Plugin_doesn_t_have_a_main_funct_100a10a9e._8_8_,3);
    s_Plugin_doesn_t_have_a_main_funct_100a10a9e[0xc] =
         SUB81(s_Plugin_doesn_t_have_a_main_funct_100a10a9e._8_8_,4);
    s_Plugin_doesn_t_have_a_main_funct_100a10a9e[0xd] =
         SUB81(s_Plugin_doesn_t_have_a_main_funct_100a10a9e._8_8_,5);
    s_Plugin_doesn_t_have_a_main_funct_100a10a9e[0xe] =
         SUB81(s_Plugin_doesn_t_have_a_main_funct_100a10a9e._8_8_,6);
    s_Plugin_doesn_t_have_a_main_funct_100a10a9e[0xf] =
         SUB81(s_Plugin_doesn_t_have_a_main_funct_100a10a9e._8_8_,7);
    s_Plugin_doesn_t_have_a_main_funct_100a10a9e[0] =
         (char)s_Plugin_doesn_t_have_a_main_funct_100a10a9e._0_8_;
    s_Plugin_doesn_t_have_a_main_funct_100a10a9e[1] =
         SUB81(s_Plugin_doesn_t_have_a_main_funct_100a10a9e._0_8_,1);
    s_Plugin_doesn_t_have_a_main_funct_100a10a9e[2] =
         SUB81(s_Plugin_doesn_t_have_a_main_funct_100a10a9e._0_8_,2);
    s_Plugin_doesn_t_have_a_main_funct_100a10a9e[3] =
         SUB81(s_Plugin_doesn_t_have_a_main_funct_100a10a9e._0_8_,3);
    s_Plugin_doesn_t_have_a_main_funct_100a10a9e[4] =
         SUB81(s_Plugin_doesn_t_have_a_main_funct_100a10a9e._0_8_,4);
    s_Plugin_doesn_t_have_a_main_funct_100a10a9e[5] =
         SUB81(s_Plugin_doesn_t_have_a_main_funct_100a10a9e._0_8_,5);
    s_Plugin_doesn_t_have_a_main_funct_100a10a9e[6] =
         SUB81(s_Plugin_doesn_t_have_a_main_funct_100a10a9e._0_8_,6);
    s_Plugin_doesn_t_have_a_main_funct_100a10a9e[7] =
         SUB81(s_Plugin_doesn_t_have_a_main_funct_100a10a9e._0_8_,7);
    s_Plugin_doesn_t_publish_a_functio_100a10a7c[0x18] =
         (char)s_Plugin_doesn_t_publish_a_functio_100a10a7c._24_8_;
    s_Plugin_doesn_t_publish_a_functio_100a10a7c[0x19] =
         SUB81(s_Plugin_doesn_t_publish_a_functio_100a10a7c._24_8_,1);
    s_Plugin_doesn_t_publish_a_functio_100a10a7c[0x1a] =
         SUB81(s_Plugin_doesn_t_publish_a_functio_100a10a7c._24_8_,2);
    s_Plugin_doesn_t_publish_a_functio_100a10a7c[0x1b] =
         SUB81(s_Plugin_doesn_t_publish_a_functio_100a10a7c._24_8_,3);
    s_Plugin_doesn_t_publish_a_functio_100a10a7c[0x1c] =
         SUB81(s_Plugin_doesn_t_publish_a_functio_100a10a7c._24_8_,4);
    s_Plugin_doesn_t_publish_a_functio_100a10a7c[0x1d] =
         SUB81(s_Plugin_doesn_t_publish_a_functio_100a10a7c._24_8_,5);
    s_Plugin_doesn_t_publish_a_functio_100a10a7c[0x1e] =
         SUB81(s_Plugin_doesn_t_publish_a_functio_100a10a7c._24_8_,6);
    s_Plugin_doesn_t_publish_a_functio_100a10a7c[0x1f] =
         SUB81(s_Plugin_doesn_t_publish_a_functio_100a10a7c._24_8_,7);
    s_Plugin_doesn_t_publish_a_functio_100a10a7c[0x10] =
         (char)s_Plugin_doesn_t_publish_a_functio_100a10a7c._16_8_;
    s_Plugin_doesn_t_publish_a_functio_100a10a7c[0x11] =
         SUB81(s_Plugin_doesn_t_publish_a_functio_100a10a7c._16_8_,1);
    s_Plugin_doesn_t_publish_a_functio_100a10a7c[0x12] =
         SUB81(s_Plugin_doesn_t_publish_a_functio_100a10a7c._16_8_,2);
    s_Plugin_doesn_t_publish_a_functio_100a10a7c[0x13] =
         SUB81(s_Plugin_doesn_t_publish_a_functio_100a10a7c._16_8_,3);
    s_Plugin_doesn_t_publish_a_functio_100a10a7c[0x14] =
         SUB81(s_Plugin_doesn_t_publish_a_functio_100a10a7c._16_8_,4);
    s_Plugin_doesn_t_publish_a_functio_100a10a7c[0x15] =
         SUB81(s_Plugin_doesn_t_publish_a_functio_100a10a7c._16_8_,5);
    s_Plugin_doesn_t_publish_a_functio_100a10a7c[0x16] =
         SUB81(s_Plugin_doesn_t_publish_a_functio_100a10a7c._16_8_,6);
    s_Plugin_doesn_t_publish_a_functio_100a10a7c[0x17] =
         SUB81(s_Plugin_doesn_t_publish_a_functio_100a10a7c._16_8_,7);
    s_Plugin_doesn_t_publish_a_functio_100a10a7c[8] =
         (char)s_Plugin_doesn_t_publish_a_functio_100a10a7c._8_8_;
    s_Plugin_doesn_t_publish_a_functio_100a10a7c[9] =
         SUB81(s_Plugin_doesn_t_publish_a_functio_100a10a7c._8_8_,1);
    s_Plugin_doesn_t_publish_a_functio_100a10a7c[10] =
         SUB81(s_Plugin_doesn_t_publish_a_functio_100a10a7c._8_8_,2);
    s_Plugin_doesn_t_publish_a_functio_100a10a7c[0xb] =
         SUB81(s_Plugin_doesn_t_publish_a_functio_100a10a7c._8_8_,3);
    s_Plugin_doesn_t_publish_a_functio_100a10a7c[0xc] =
         SUB81(s_Plugin_doesn_t_publish_a_functio_100a10a7c._8_8_,4);
    s_Plugin_doesn_t_publish_a_functio_100a10a7c[0xd] =
         SUB81(s_Plugin_doesn_t_publish_a_functio_100a10a7c._8_8_,5);
    s_Plugin_doesn_t_publish_a_functio_100a10a7c[0xe] =
         SUB81(s_Plugin_doesn_t_publish_a_functio_100a10a7c._8_8_,6);
    s_Plugin_doesn_t_publish_a_functio_100a10a7c[0xf] =
         SUB81(s_Plugin_doesn_t_publish_a_functio_100a10a7c._8_8_,7);
    s_Plugin_doesn_t_publish_a_functio_100a10a7c[0] =
         (char)s_Plugin_doesn_t_publish_a_functio_100a10a7c._0_8_;
    s_Plugin_doesn_t_publish_a_functio_100a10a7c[1] =
         SUB81(s_Plugin_doesn_t_publish_a_functio_100a10a7c._0_8_,1);
    s_Plugin_doesn_t_publish_a_functio_100a10a7c[2] =
         SUB81(s_Plugin_doesn_t_publish_a_functio_100a10a7c._0_8_,2);
    s_Plugin_doesn_t_publish_a_functio_100a10a7c[3] =
         SUB81(s_Plugin_doesn_t_publish_a_functio_100a10a7c._0_8_,3);
    s_Plugin_doesn_t_publish_a_functio_100a10a7c[4] =
         SUB81(s_Plugin_doesn_t_publish_a_functio_100a10a7c._0_8_,4);
    s_Plugin_doesn_t_publish_a_functio_100a10a7c[5] =
         SUB81(s_Plugin_doesn_t_publish_a_functio_100a10a7c._0_8_,5);
    s_Plugin_doesn_t_publish_a_functio_100a10a7c[6] =
         SUB81(s_Plugin_doesn_t_publish_a_functio_100a10a7c._0_8_,6);
    s_Plugin_doesn_t_publish_a_functio_100a10a7c[7] =
         SUB81(s_Plugin_doesn_t_publish_a_functio_100a10a7c._0_8_,7);
    return;
  }
  operator_delete(local_40);
  return;
}

