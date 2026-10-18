// 0x100220998 FUN_100220998 state=exported-with-warnings role=push-to-live-midi-ipc-channel (client)
// source chunk chunk-00094.jsonl; code_sha256=7d61352e6f22a08e06ff02f97f3607f45c521bc3648c07e713f312da616b5a08

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

long FUN_100220998(long param_1)

{
  undefined8 uVar1;
  long local_40;
  code *local_38;
  undefined8 local_30;
  long lStack_28;
  
  local_38 = operator_new(0x20);
  uVar1 = s_push_to_live_midi_ipc_channel_10183b4c9._0_8_;
  lStack_28 = _UNK_1015771d8;
  local_30 = _DAT_1015771d0;
  *(ulong *)(local_38 + 8) =
       CONCAT35(s_push_to_live_midi_ipc_channel_10183b4c9._13_3_,
                s_push_to_live_midi_ipc_channel_10183b4c9._8_5_);
  *(undefined8 *)local_38 = uVar1;
  uVar1 = CONCAT53(s_push_to_live_midi_ipc_channel_10183b4c9._16_5_,
                   s_push_to_live_midi_ipc_channel_10183b4c9._13_3_);
  *(undefined8 *)(local_38 + 0x15) = s_push_to_live_midi_ipc_channel_10183b4c9._21_8_;
  *(undefined8 *)(local_38 + 0xd) = uVar1;
  local_38[0x1d] = (code)0x0;
  thunk_FUN_10022c9d0(param_1,&local_38);
  if (lStack_28 < 0) {
    operator_delete(local_38);
  }
  FUN_100220f38(param_1 + 8);
  FUN_100221bcc(param_1 + 0x10);
  local_38 = FUN_100220ad0;
  local_30 = 0;
  local_40 = param_1;
  FUN_100223d20(param_1 + 0x50,&local_38,&local_40);
  *(undefined1 *)(param_1 + 0x58) = 0;
  FUN_10022cc8c(param_1,500);
  return param_1;
}

