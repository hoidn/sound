// 0x100220ad0 FUN_100220ad0 state=exported role=MIDI forwarding thread loop
// source chunk chunk-00094.jsonl; code_sha256=e97bc6cac9662f275aa619e591be1b3228535a821df5c1d279615afda8e82234

void FUN_100220ad0(long param_1)

{
  byte bVar1;
  undefined1 auStack_58 [24];
  uint local_40;
  undefined8 local_38;
  char local_30;
  undefined1 uStack_21;
  
  bVar1 = *(byte *)(param_1 + 0x58);
  while ((bVar1 & 1) == 0) {
    (**(code **)(**(long **)(param_1 + 0x30) + 0x20))(auStack_58);
    if ((local_30 == '\x01') && ((*(byte *)(param_1 + 0x58) & 1) == 0)) {
      FUN_10022cb04(param_1,auStack_58,local_38);
    }
    if ((local_30 == '\x01') && (local_40 != 0xffffffff)) {
      (*(code *)(&PTR_FUN_101bd4128)[local_40])(&uStack_21,auStack_58);
    }
    bVar1 = *(byte *)(param_1 + 0x58);
  }
  return;
}

