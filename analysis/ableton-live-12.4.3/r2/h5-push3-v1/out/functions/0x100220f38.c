// 0x100220f38 FUN_100220f38 state=exported-with-warnings role=live-to-push-midi-ipc-channel (server)
// source chunk chunk-00094.jsonl; code_sha256=51d253d345a60693325752ff4e4fb21bb77a11fb2c6ddf21ac9e1387baa6d111

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 * FUN_100220f38(undefined8 *param_1)

{
  undefined8 uVar1;
  undefined8 *puVar2;
  char *local_60;
  undefined8 local_58;
  long lStack_50;
  void *local_48;
  undefined8 uStack_40;
  undefined7 local_38;
  char cStack_31;
  
  local_60 = operator_new(0x20);
  uVar1 = s_live_to_push_midi_ipc_channel_10183b4e7._0_8_;
  lStack_50 = _UNK_1015771d8;
  local_58 = _DAT_1015771d0;
  *(ulong *)(local_60 + 8) =
       CONCAT35(s_live_to_push_midi_ipc_channel_10183b4e7._13_3_,
                s_live_to_push_midi_ipc_channel_10183b4e7._8_5_);
  *(undefined8 *)local_60 = uVar1;
  uVar1 = CONCAT53(s_live_to_push_midi_ipc_channel_10183b4e7._16_5_,
                   s_live_to_push_midi_ipc_channel_10183b4e7._13_3_);
  *(undefined8 *)(local_60 + 0x15) = s_live_to_push_midi_ipc_channel_10183b4e7._21_8_;
  *(undefined8 *)(local_60 + 0xd) = uVar1;
  local_60[0x1d] = '\0';
  FUN_100180a80(&local_48,&local_60,0);
  puVar2 = operator_new(0x58);
  *puVar2 = &PTR_thunk_FUN_100221558_101bd4098;
  puVar2[1] = puVar2 + 2;
  *(undefined8 *)((long)puVar2 + 0x14) = DAT_101570410;
  *(undefined4 *)((long)puVar2 + 0x1c) = 0xffffffff;
  if (cStack_31 < '\0') {
    FUN_10018127c(puVar2 + 4,local_48,uStack_40);
    *(undefined4 *)(puVar2 + 7) = 0;
    puVar2[9] = 0;
    puVar2[10] = 0;
    puVar2[8] = 0;
    *param_1 = puVar2;
    if (cStack_31 < '\0') {
      operator_delete(local_48);
    }
  }
  else {
    puVar2[5] = uStack_40;
    puVar2[4] = local_48;
    puVar2[6] = CONCAT17(cStack_31,local_38);
    *(undefined4 *)(puVar2 + 7) = 0;
    puVar2[9] = 0;
    puVar2[10] = 0;
    puVar2[8] = 0;
    *param_1 = puVar2;
  }
  if (lStack_50 < 0) {
    operator_delete(local_60);
  }
  (**(code **)(*(long *)*param_1 + 0x38))();
  return param_1;
}

