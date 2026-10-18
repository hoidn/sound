
void FUN_100149888(long param_1,int param_2,int param_3)

{
  int iVar1;
  undefined8 uVar2;
  undefined1 auStack_28 [8];
  
  if (param_3 - 3U < 3) {
    FUN_10015241c(*(undefined8 *)(param_1 + 0x90));
    return;
  }
  if (param_3 != 7) {
    if (param_3 != 8) {
      return;
    }
    FUN_10015241c(*(undefined8 *)(param_1 + 0xa8));
    return;
  }
  uVar2 = std::chrono::system_clock::now();
  FUN_1006a290c(auStack_28,1,uVar2);
  iVar1 = FUN_10069f1d8(auStack_28);
  if (iVar1 != 0) {
    FUN_10069c398(auStack_28,"bark bark: shutdown!");
  }
  thunk_FUN_10069bf04(auStack_28);
  if (param_2 < 2) {
    if (param_2 == 0) {
      uVar2 = std::chrono::system_clock::now();
      FUN_1006a290c(auStack_28,3,uVar2);
      iVar1 = FUN_10069f1d8(auStack_28);
      if (iVar1 != 0) {
        FUN_10069c398(auStack_28,
                      "Shutting down because neither background thread started nor USB device connected"
                     );
      }
    }
    else {
      if (param_2 != 1) goto LAB_100149a20;
      uVar2 = std::chrono::system_clock::now();
      FUN_1006a290c(auStack_28,3,uVar2);
      iVar1 = FUN_10069f1d8(auStack_28);
      if (iVar1 != 0) {
        FUN_10069c398(auStack_28,"Shutting down because USB device wasn\'t connected in time");
      }
    }
  }
  else if (param_2 == 2) {
    uVar2 = std::chrono::system_clock::now();
    FUN_1006a290c(auStack_28,3,uVar2);
    iVar1 = FUN_10069f1d8(auStack_28);
    if (iVar1 != 0) {
      FUN_10069c398(auStack_28,"Shutting down because background thread not started in time");
    }
  }
  else {
    if (param_2 != 5) goto LAB_100149a20;
    uVar2 = std::chrono::system_clock::now();
    FUN_1006a290c(auStack_28,3,uVar2);
    iVar1 = FUN_10069f1d8(auStack_28);
    if (iVar1 != 0) {
      FUN_10069c398(auStack_28,"Shutting down because live didn\'t ack in time");
    }
  }
  thunk_FUN_10069bf04(auStack_28);
LAB_100149a20:
  FUN_10015241c(*(undefined8 *)(param_1 + 0x78));
  return;
}

