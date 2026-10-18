// 0x100668448 FUN_100668448 state=exported role=Watchdog shutdown reasons
// source chunk chunk-00229.jsonl; code_sha256=a39567d88a55f6b47cbf53f9010dc398abe968a550f11e046ee16a6f6d4c2f6d

void FUN_100668448(long param_1,int param_2,int param_3)

{
  int iVar1;
  undefined8 uVar2;
  undefined1 auStack_28 [8];
  
  if (param_3 - 3U < 3) {
    FUN_1002947e8(*(undefined8 *)(param_1 + 0x90));
    return;
  }
  if (param_3 != 7) {
    if (param_3 != 8) {
      return;
    }
    FUN_1002947e8(*(undefined8 *)(param_1 + 0xa8));
    return;
  }
  uVar2 = std::chrono::system_clock::now();
  FUN_1003324b0(auStack_28,1,uVar2);
  iVar1 = FUN_10032ece8(auStack_28);
  if (iVar1 != 0) {
    FUN_10032bea8(auStack_28,"bark bark: shutdown!");
  }
  thunk_FUN_10032ba14(auStack_28);
  if (param_2 < 2) {
    if (param_2 == 0) {
      uVar2 = std::chrono::system_clock::now();
      FUN_1003324b0(auStack_28,3,uVar2);
      iVar1 = FUN_10032ece8(auStack_28);
      if (iVar1 != 0) {
        FUN_10032bea8(auStack_28,
                      "Shutting down because neither background thread started nor USB device connected"
                     );
      }
    }
    else {
      if (param_2 != 1) goto LAB_1006685e0;
      uVar2 = std::chrono::system_clock::now();
      FUN_1003324b0(auStack_28,3,uVar2);
      iVar1 = FUN_10032ece8(auStack_28);
      if (iVar1 != 0) {
        FUN_10032bea8(auStack_28,"Shutting down because USB device wasn\'t connected in time");
      }
    }
  }
  else if (param_2 == 2) {
    uVar2 = std::chrono::system_clock::now();
    FUN_1003324b0(auStack_28,3,uVar2);
    iVar1 = FUN_10032ece8(auStack_28);
    if (iVar1 != 0) {
      FUN_10032bea8(auStack_28,"Shutting down because background thread not started in time");
    }
  }
  else {
    if (param_2 != 5) goto LAB_1006685e0;
    uVar2 = std::chrono::system_clock::now();
    FUN_1003324b0(auStack_28,3,uVar2);
    iVar1 = FUN_10032ece8(auStack_28);
    if (iVar1 != 0) {
      FUN_10032bea8(auStack_28,"Shutting down because live didn\'t ack in time");
    }
  }
  thunk_FUN_10032ba14(auStack_28);
LAB_1006685e0:
  FUN_1002947e8(*(undefined8 *)(param_1 + 0x78));
  return;
}

