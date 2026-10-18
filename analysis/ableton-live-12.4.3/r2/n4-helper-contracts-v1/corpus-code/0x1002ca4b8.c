// 0x1002ca4b8 FUN_1002ca4b8 exported-with-warnings  sig: undefined FUN_1002ca4b8()

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1002ca4b8(long *param_1,undefined8 *param_2)

{
  undefined8 uVar1;
  long lVar2;
  undefined8 uVar3;
  char *local_60;
  undefined8 local_58;
  long lStack_50;
  void *local_48 [2];
  char local_31;
  
  lVar2 = FUN_1012d9850(0x198);
  uVar3 = *param_2;
  local_60 = operator_new(0x20);
  uVar1 = s_push_flip_api_ipc_channel_105ab0498._0_8_;
  lStack_50 = _UNK_1055cdf98;
  local_58 = _DAT_1055cdf90;
  *(ulong *)(local_60 + 8) =
       CONCAT71(s_push_flip_api_ipc_channel_105ab0498._9_7_,s_push_flip_api_ipc_channel_105ab0498[8]
               );
  *(undefined8 *)local_60 = uVar1;
  uVar1 = CONCAT17(s_push_flip_api_ipc_channel_105ab0498[0x10],
                   s_push_flip_api_ipc_channel_105ab0498._9_7_);
  *(undefined8 *)(local_60 + 0x11) = s_push_flip_api_ipc_channel_105ab0498._17_8_;
  *(undefined8 *)(local_60 + 9) = uVar1;
  local_60[0x19] = '\0';
  FUN_1002725dc(local_48,&local_60,0);
  thunk_FUN_10390c024(lVar2,uVar3,local_48);
  *param_1 = lVar2;
  if (lVar2 != 0) {
    *(int *)(lVar2 + 8) = *(int *)(lVar2 + 8) + 1;
  }
  if (local_31 < '\0') {
    operator_delete(local_48[0]);
  }
  if (lStack_50 < 0) {
    operator_delete(local_60);
    return;
  }
  s_push_flip_api_ipc_channel_105ab0498[0] = (char)s_push_flip_api_ipc_channel_105ab0498._0_8_;
  s_push_flip_api_ipc_channel_105ab0498[1] = SUB81(s_push_flip_api_ipc_channel_105ab0498._0_8_,1);
  s_push_flip_api_ipc_channel_105ab0498[2] = SUB81(s_push_flip_api_ipc_channel_105ab0498._0_8_,2);
  s_push_flip_api_ipc_channel_105ab0498[3] = SUB81(s_push_flip_api_ipc_channel_105ab0498._0_8_,3);
  s_push_flip_api_ipc_channel_105ab0498[4] = SUB81(s_push_flip_api_ipc_channel_105ab0498._0_8_,4);
  s_push_flip_api_ipc_channel_105ab0498[5] = SUB81(s_push_flip_api_ipc_channel_105ab0498._0_8_,5);
  s_push_flip_api_ipc_channel_105ab0498[6] = SUB81(s_push_flip_api_ipc_channel_105ab0498._0_8_,6);
  s_push_flip_api_ipc_channel_105ab0498[7] = SUB81(s_push_flip_api_ipc_channel_105ab0498._0_8_,7);
  s_push_flip_api_ipc_channel_105ab0498[9] = (char)s_push_flip_api_ipc_channel_105ab0498._9_7_;
  s_push_flip_api_ipc_channel_105ab0498[10] = SUB71(s_push_flip_api_ipc_channel_105ab0498._9_7_,1);
  s_push_flip_api_ipc_channel_105ab0498[0xb] = SUB71(s_push_flip_api_ipc_channel_105ab0498._9_7_,2);
  s_push_flip_api_ipc_channel_105ab0498[0xc] = SUB71(s_push_flip_api_ipc_channel_105ab0498._9_7_,3);
  s_push_flip_api_ipc_channel_105ab0498[0xd] = SUB71(s_push_flip_api_ipc_channel_105ab0498._9_7_,4);
  s_push_flip_api_ipc_channel_105ab0498[0xe] = SUB71(s_push_flip_api_ipc_channel_105ab0498._9_7_,5);
  s_push_flip_api_ipc_channel_105ab0498[0xf] = SUB71(s_push_flip_api_ipc_channel_105ab0498._9_7_,6);
  s_push_flip_api_ipc_channel_105ab0498[0x11] = (char)s_push_flip_api_ipc_channel_105ab0498._17_8_;
  s_push_flip_api_ipc_channel_105ab0498[0x12] =
       SUB81(s_push_flip_api_ipc_channel_105ab0498._17_8_,1);
  s_push_flip_api_ipc_channel_105ab0498[0x13] =
       SUB81(s_push_flip_api_ipc_channel_105ab0498._17_8_,2);
  s_push_flip_api_ipc_channel_105ab0498[0x14] =
       SUB81(s_push_flip_api_ipc_channel_105ab0498._17_8_,3);
  s_push_flip_api_ipc_channel_105ab0498[0x15] =
       SUB81(s_push_flip_api_ipc_channel_105ab0498._17_8_,4);
  s_push_flip_api_ipc_channel_105ab0498[0x16] =
       SUB81(s_push_flip_api_ipc_channel_105ab0498._17_8_,5);
  s_push_flip_api_ipc_channel_105ab0498[0x17] =
       SUB81(s_push_flip_api_ipc_channel_105ab0498._17_8_,6);
  s_push_flip_api_ipc_channel_105ab0498[0x18] =
       SUB81(s_push_flip_api_ipc_channel_105ab0498._17_8_,7);
  return;
}


