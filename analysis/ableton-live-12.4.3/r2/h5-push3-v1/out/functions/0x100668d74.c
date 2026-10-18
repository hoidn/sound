// 0x100668d74 FUN_100668d74 state=exported role=Watchdog event names
// source chunk chunk-00230.jsonl; code_sha256=67917f82613d3bbde7c555f6325dd11325b5e2018f68c4f62438d865953209a6

undefined8 FUN_100668d74(undefined8 param_1,int *param_2)

{
  int iVar1;
  char *pcVar2;
  undefined8 uVar3;
  
  iVar1 = *param_2;
  if (iVar1 < 2) {
    if (iVar1 == 0) {
      pcVar2 = "kReceiverThreadStarted";
      uVar3 = 0x16;
    }
    else {
      if (iVar1 != 1) {
        return param_1;
      }
      pcVar2 = "kLiveStillRunning";
      uVar3 = 0x11;
    }
  }
  else if (iVar1 == 2) {
    pcVar2 = "kAckReceived";
    uVar3 = 0xc;
  }
  else if (iVar1 == 3) {
    pcVar2 = "kUsbDeviceOpen";
    uVar3 = 0xe;
  }
  else {
    if (iVar1 != 4) {
      return param_1;
    }
    pcVar2 = "kProcessDefunct";
    uVar3 = 0xf;
  }
  FUN_100181e9c(param_1,pcVar2,uVar3);
  return param_1;
}

