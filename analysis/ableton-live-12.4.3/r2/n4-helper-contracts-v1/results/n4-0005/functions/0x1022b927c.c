
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

long FUN_1022b927c(long param_1)

{
  int iVar1;
  undefined8 uVar2;
  undefined8 *puVar3;
  void *pvVar4;
  long lVar5;
  char *local_60;
  undefined8 local_58;
  long lStack_50;
  int *local_48;
  undefined8 uStack_40;
  undefined7 local_38;
  char cStack_31;
  
  puVar3 = (undefined8 *)FUN_1022b7a24();
  *puVar3 = &PTR_FUN_106786a38;
  local_60 = operator_new(0x20);
  uVar2 = s_live_to_push_midi_ipc_channel_105bc24ba._0_8_;
  lStack_50 = _UNK_1055ce038;
  local_58 = _DAT_1055ce030;
  *(ulong *)(local_60 + 8) =
       CONCAT35(s_live_to_push_midi_ipc_channel_105bc24ba._13_3_,
                s_live_to_push_midi_ipc_channel_105bc24ba._8_5_);
  *(undefined8 *)local_60 = uVar2;
  uVar2 = CONCAT53(s_live_to_push_midi_ipc_channel_105bc24ba._16_5_,
                   s_live_to_push_midi_ipc_channel_105bc24ba._13_3_);
  *(undefined8 *)(local_60 + 0x15) = s_live_to_push_midi_ipc_channel_105bc24ba._21_8_;
  *(undefined8 *)(local_60 + 0xd) = uVar2;
  local_60[0x1d] = '\0';
  FUN_1002725dc(&local_48,&local_60,0);
  puVar3 = operator_new(0x58);
  *puVar3 = &PTR_thunk_FUN_1022c424c_106787a18;
  puVar3[1] = puVar3 + 2;
  *(undefined8 *)((long)puVar3 + 0x14) = DAT_1055d3960;
  *(undefined4 *)((long)puVar3 + 0x1c) = 0xffffffff;
  if (cStack_31 < '\0') {
    FUN_10023448c(puVar3 + 4,local_48,uStack_40);
    *(undefined4 *)(puVar3 + 7) = 0;
    puVar3[9] = 0;
    puVar3[10] = 0;
    puVar3[8] = 0;
    *(undefined8 **)(param_1 + 0xb8) = puVar3;
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
    *(undefined8 **)(param_1 + 0xb8) = puVar3;
  }
  if (lStack_50 < 0) {
    operator_delete(local_60);
  }
  *(undefined8 *)(param_1 + 0xc0) = DAT_1058781e8;
  pvVar4 = operator_new(0x500000);
  *(void **)(param_1 + 200) = pvVar4;
  *(undefined8 *)(param_1 + 0xd8) = 0;
  *(undefined8 *)(param_1 + 0xd0) = 0;
  *(undefined8 *)(param_1 + 0xe8) = 0;
  *(undefined8 *)(param_1 + 0xe0) = 0;
  *(undefined8 *)(param_1 + 0xf8) = 0;
  *(undefined8 *)(param_1 + 0xf0) = 0;
  *(undefined8 *)(param_1 + 0x108) = 0;
  *(undefined8 *)(param_1 + 0x100) = 0;
  *(undefined8 *)(param_1 + 0x118) = 0;
  *(undefined8 *)(param_1 + 0x110) = 0;
  *(undefined8 *)(param_1 + 0x128) = 0;
  *(undefined8 *)(param_1 + 0x120) = 0;
  *(undefined8 *)(param_1 + 0x138) = 0;
  *(undefined8 *)(param_1 + 0x130) = 0;
  *(undefined8 *)(param_1 + 0x148) = 0;
  *(undefined8 *)(param_1 + 0x140) = 0;
  *(undefined4 *)(param_1 + 0x150) = 0;
  *(undefined1 *)(param_1 + 0x158) = 0;
  *(undefined1 *)(param_1 + 0x188) = 0;
  FUN_101486414(param_1);
  (**(code **)(**(long **)(param_1 + 0xb8) + 0x38))();
  FUN_1012d9734(0x160);
  local_48 = (int *)FUN_1022bf694();
  if (local_48 != (int *)0x0) {
    local_48[2] = local_48[2] + 1;
  }
  FUN_101482718();
  lVar5 = *(long *)(param_1 + 0x30);
  if ((lVar5 != 0) && (iVar1 = *(int *)(lVar5 + 8) + -1, *(int *)(lVar5 + 8) = iVar1, iVar1 == 0)) {
    FUN_10128eea0();
  }
  *(int **)(param_1 + 0x30) = local_48;
  *(long *)(local_48 + 0x3e) = param_1;
  (**(code **)(**(long **)(local_48 + 0x34) + 0x248))(*(long **)(local_48 + 0x34),1);
  *(undefined1 *)(param_1 + 0x25) = 1;
  FUN_101427680(&local_48,"ToPush");
  FUN_1022a8f54(param_1,&local_48);
  if ((local_48 != (int *)0x0) && (iVar1 = *local_48, *local_48 = iVar1 + -1, iVar1 + -1 == 0)) {
    FUN_101449efc();
  }
  FUN_101427680(&local_48,"ToPush");
  FUN_1022b5194(param_1,&local_48);
  if ((local_48 != (int *)0x0) && (iVar1 = *local_48, *local_48 = iVar1 + -1, iVar1 + -1 == 0)) {
    FUN_101449efc();
  }
  return param_1;
}

