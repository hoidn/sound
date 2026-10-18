// 0x10017f084 FUN_10017f084 state=exported-with-warnings role=push-flip-api-ipc-channel socket
// source chunk chunk-00065.jsonl; code_sha256=02c3c6700b58379dec561348aecd4299bccc4afd1a4714c33cfc06e8b1d4ac99

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_10017f084(undefined8 *param_1)

{
  undefined8 uVar1;
  undefined8 *puVar2;
  char *local_50;
  undefined8 local_48;
  long lStack_40;
  void *local_38;
  undefined8 uStack_30;
  undefined7 local_28;
  char cStack_21;
  
  local_50 = operator_new(0x20);
  uVar1 = s_push_flip_api_ipc_channel_101837655._0_8_;
  lStack_40 = _UNK_1015703d8;
  local_48 = _DAT_1015703d0;
  *(ulong *)(local_50 + 8) =
       CONCAT71(s_push_flip_api_ipc_channel_101837655._9_7_,s_push_flip_api_ipc_channel_101837655[8]
               );
  *(undefined8 *)local_50 = uVar1;
  uVar1 = CONCAT17(s_push_flip_api_ipc_channel_101837655[0x10],
                   s_push_flip_api_ipc_channel_101837655._9_7_);
  *(undefined8 *)(local_50 + 0x11) = s_push_flip_api_ipc_channel_101837655._17_8_;
  *(undefined8 *)(local_50 + 9) = uVar1;
  local_50[0x19] = '\0';
  FUN_100180a80(&local_38,&local_50,0);
  puVar2 = operator_new(0x58);
  *puVar2 = &PTR_thunk_FUN_10018131c_101bcf110;
  puVar2[1] = puVar2 + 2;
  *(undefined8 *)((long)puVar2 + 0x14) = DAT_101570410;
  *(undefined4 *)((long)puVar2 + 0x1c) = 0xffffffff;
  if (cStack_21 < '\0') {
    FUN_10018127c(puVar2 + 4,local_38,uStack_30);
    *(undefined4 *)(puVar2 + 7) = 0;
    puVar2[9] = 0;
    puVar2[10] = 0;
    puVar2[8] = 0;
    *param_1 = puVar2;
    if (cStack_21 < '\0') {
      operator_delete(local_38);
    }
  }
  else {
    puVar2[5] = uStack_30;
    puVar2[4] = local_38;
    puVar2[6] = CONCAT17(cStack_21,local_28);
    *(undefined4 *)(puVar2 + 7) = 0;
    puVar2[9] = 0;
    puVar2[10] = 0;
    puVar2[8] = 0;
    *param_1 = puVar2;
  }
  if (-1 < lStack_40) {
    s_push_flip_api_ipc_channel_101837655[0] = (char)s_push_flip_api_ipc_channel_101837655._0_8_;
    s_push_flip_api_ipc_channel_101837655[1] = SUB81(s_push_flip_api_ipc_channel_101837655._0_8_,1);
    s_push_flip_api_ipc_channel_101837655[2] = SUB81(s_push_flip_api_ipc_channel_101837655._0_8_,2);
    s_push_flip_api_ipc_channel_101837655[3] = SUB81(s_push_flip_api_ipc_channel_101837655._0_8_,3);
    s_push_flip_api_ipc_channel_101837655[4] = SUB81(s_push_flip_api_ipc_channel_101837655._0_8_,4);
    s_push_flip_api_ipc_channel_101837655[5] = SUB81(s_push_flip_api_ipc_channel_101837655._0_8_,5);
    s_push_flip_api_ipc_channel_101837655[6] = SUB81(s_push_flip_api_ipc_channel_101837655._0_8_,6);
    s_push_flip_api_ipc_channel_101837655[7] = SUB81(s_push_flip_api_ipc_channel_101837655._0_8_,7);
    s_push_flip_api_ipc_channel_101837655[9] = (char)s_push_flip_api_ipc_channel_101837655._9_7_;
    s_push_flip_api_ipc_channel_101837655[10] = SUB71(s_push_flip_api_ipc_channel_101837655._9_7_,1)
    ;
    s_push_flip_api_ipc_channel_101837655[0xb] =
         SUB71(s_push_flip_api_ipc_channel_101837655._9_7_,2);
    s_push_flip_api_ipc_channel_101837655[0xc] =
         SUB71(s_push_flip_api_ipc_channel_101837655._9_7_,3);
    s_push_flip_api_ipc_channel_101837655[0xd] =
         SUB71(s_push_flip_api_ipc_channel_101837655._9_7_,4);
    s_push_flip_api_ipc_channel_101837655[0xe] =
         SUB71(s_push_flip_api_ipc_channel_101837655._9_7_,5);
    s_push_flip_api_ipc_channel_101837655[0xf] =
         SUB71(s_push_flip_api_ipc_channel_101837655._9_7_,6);
    s_push_flip_api_ipc_channel_101837655[0x11] = (char)s_push_flip_api_ipc_channel_101837655._17_8_
    ;
    s_push_flip_api_ipc_channel_101837655[0x12] =
         SUB81(s_push_flip_api_ipc_channel_101837655._17_8_,1);
    s_push_flip_api_ipc_channel_101837655[0x13] =
         SUB81(s_push_flip_api_ipc_channel_101837655._17_8_,2);
    s_push_flip_api_ipc_channel_101837655[0x14] =
         SUB81(s_push_flip_api_ipc_channel_101837655._17_8_,3);
    s_push_flip_api_ipc_channel_101837655[0x15] =
         SUB81(s_push_flip_api_ipc_channel_101837655._17_8_,4);
    s_push_flip_api_ipc_channel_101837655[0x16] =
         SUB81(s_push_flip_api_ipc_channel_101837655._17_8_,5);
    s_push_flip_api_ipc_channel_101837655[0x17] =
         SUB81(s_push_flip_api_ipc_channel_101837655._17_8_,6);
    s_push_flip_api_ipc_channel_101837655[0x18] =
         SUB81(s_push_flip_api_ipc_channel_101837655._17_8_,7);
    return;
  }
  operator_delete(local_50);
  return;
}

