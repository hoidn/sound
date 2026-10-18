// 0x100668c58 FUN_100668c58 state=exported role=Watchdog state names
// source chunk chunk-00230.jsonl; code_sha256=c47bca4656bcef7e59358bb394bb25e848c78b5ea10f79108570cbc05fbc610d

undefined8 FUN_100668c58(undefined8 param_1,int *param_2)

{
  int iVar1;
  char *pcVar2;
  undefined8 uVar3;
  
  iVar1 = *param_2;
  if (iVar1 < 4) {
    if (iVar1 < 2) {
      if (iVar1 != 0) {
        if (iVar1 != 1) {
          return param_1;
        }
        pcVar2 = "kWaitForUsb";
        uVar3 = 0xb;
        goto LAB_100668d60;
      }
      pcVar2 = "kLaunched";
LAB_100668d58:
      uVar3 = 9;
      goto LAB_100668d60;
    }
    if (iVar1 == 2) {
      pcVar2 = "kWaitForReceiverThread";
      uVar3 = 0x16;
      goto LAB_100668d60;
    }
    if (iVar1 != 3) {
      return param_1;
    }
    pcVar2 = "kSendFirstSync";
  }
  else {
    if (5 < iVar1) {
      if (iVar1 == 6) {
        pcVar2 = "kRunning";
      }
      else {
        if (iVar1 == 7) {
          pcVar2 = "kShutdown";
          goto LAB_100668d58;
        }
        if (iVar1 != 8) {
          return param_1;
        }
        pcVar2 = "kDefunct";
      }
      uVar3 = 8;
      goto LAB_100668d60;
    }
    if (iVar1 == 4) {
      pcVar2 = "kSendSecondSync";
      uVar3 = 0xf;
      goto LAB_100668d60;
    }
    if (iVar1 != 5) {
      return param_1;
    }
    pcVar2 = "kSendThirdSync";
  }
  uVar3 = 0xe;
LAB_100668d60:
  FUN_100181e9c(param_1,pcVar2,uVar3);
  return param_1;
}

