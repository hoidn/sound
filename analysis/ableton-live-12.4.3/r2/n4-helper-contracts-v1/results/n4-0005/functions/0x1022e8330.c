
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4 * FUN_1022e8330(undefined4 *param_1,undefined4 param_2,undefined8 param_3)

{
  undefined8 uVar1;
  undefined *puVar2;
  undefined8 *puVar3;
  undefined4 *puVar4;
  char *local_60;
  undefined8 local_58;
  long lStack_50;
  undefined *local_48;
  undefined8 uStack_40;
  undefined7 local_38;
  char cStack_31;
  
  *param_1 = param_2;
  *(undefined8 *)(param_1 + 2) = param_3;
  *(undefined2 *)(param_1 + 4) = 0;
  local_60 = operator_new(0x20);
  uVar1 = s_push_to_live_midi_ipc_channel_105bc33fc._0_8_;
  lStack_50 = _UNK_1055ce038;
  local_58 = _DAT_1055ce030;
  *(ulong *)(local_60 + 8) =
       CONCAT35(s_push_to_live_midi_ipc_channel_105bc33fc._13_3_,
                s_push_to_live_midi_ipc_channel_105bc33fc._8_5_);
  *(undefined8 *)local_60 = uVar1;
  uVar1 = CONCAT53(s_push_to_live_midi_ipc_channel_105bc33fc._16_5_,
                   s_push_to_live_midi_ipc_channel_105bc33fc._13_3_);
  *(undefined8 *)(local_60 + 0x15) = s_push_to_live_midi_ipc_channel_105bc33fc._21_8_;
  *(undefined8 *)(local_60 + 0xd) = uVar1;
  local_60[0x1d] = '\0';
  FUN_1002725dc(&local_48,&local_60,0);
  puVar3 = operator_new(0x58);
  *puVar3 = &PTR_thunk_FUN_10027a25c_1065928b0;
  puVar3[1] = puVar3 + 2;
  *(undefined8 *)((long)puVar3 + 0x14) = DAT_1055d3960;
  *(undefined4 *)((long)puVar3 + 0x1c) = 0xffffffff;
  if (cStack_31 < '\0') {
    FUN_10023448c(puVar3 + 4,local_48,uStack_40);
    *(undefined4 *)(puVar3 + 7) = 0;
    puVar3[9] = 0;
    puVar3[10] = 0;
    puVar3[8] = 0;
    *(undefined8 **)(param_1 + 6) = puVar3;
    if (cStack_31 < '\0') {
      operator_delete(local_48);
    }
  }
  else {
    puVar3[5] = uStack_40;
    puVar3[4] = local_48;
    puVar3[6] = CONCAT17(cStack_31,local_38);
    *(undefined4 *)(puVar3 + 7) = 0;
    puVar3[9] = 0;
    puVar3[10] = 0;
    puVar3[8] = 0;
    *(undefined8 **)(param_1 + 6) = puVar3;
  }
  if (lStack_50 < 0) {
    operator_delete(local_60);
  }
  puVar4 = param_1 + 8;
  *puVar4 = 0;
  puVar2 = PTR__lambda___1__TUserData__106551c20;
  *(undefined8 *)(param_1 + 10) = 0;
  *(undefined **)(param_1 + 0xc) = puVar2;
  *(undefined8 *)(param_1 + 0xe) = 0;
  *(undefined8 *)(param_1 + 0x12) = 0;
  (**(code **)(**(long **)(param_1 + 6) + 0x38))();
  local_48 = PTR_CallStaticFunc<&TPushMidiForwarder::SProcess>_1065366c8;
  uStack_40 = 0;
  FUN_1011c0b58(puVar4,0,param_1,&local_48,"PushMidiForwarder");
  FUN_1011c0b88(puVar4);
  return param_1;
}

