// 0x10016b3e8 FUN_10016b3e8 state=exported-with-warnings body_bytes=852 warnings=1 chunk=chunk-00062.jsonl

/* WARNING: Type propagation algorithm not settling */

undefined8 FUN_10016b3e8(undefined8 param_1,uint *param_2)

{
  uint uVar1;
  char *pcVar2;
  undefined8 uVar3;
  
  uVar1 = *param_2;
  if ((int)uVar1 < 0x39f4) {
    if ((int)uVar1 < 0x38c0) {
      if (uVar1 == 0) {
        pcVar2 = "none";
        uVar3 = 4;
        goto LAB_10016b52c;
      }
      if (uVar1 == 0x300) {
        pcVar2 = "all-folders";
        uVar3 = 0xb;
        goto LAB_10016b52c;
      }
    }
    else {
      if (uVar1 == 0x38c0) {
        pcVar2 = "restricted-others";
        uVar3 = 0x11;
        goto LAB_10016b52c;
      }
      if (uVar1 == 0x38c4) {
        pcVar2 = "audio";
        uVar3 = 5;
        goto LAB_10016b52c;
      }
    }
  }
  else {
    if (0x7ffe < (int)uVar1) {
      if (uVar1 == 0x7fff) {
        pcVar2 = "browser-default-and-folders";
      }
      else {
        if (uVar1 != 0xfdff) {
          if (uVar1 == 0xffff) {
            pcVar2 = "all";
            uVar3 = 3;
            goto LAB_10016b52c;
          }
          goto LAB_10016b540;
        }
        pcVar2 = "browser-all-without-folders";
      }
      uVar3 = 0x1b;
      goto LAB_10016b52c;
    }
    if (uVar1 == 0x39f4) {
      pcVar2 = "midi-track-devices";
      uVar3 = 0x12;
      goto LAB_10016b52c;
    }
    if (uVar1 == 31999) {
      pcVar2 = "browser-default";
      uVar3 = 0xf;
      goto LAB_10016b52c;
    }
  }
LAB_10016b540:
  if ((uVar1 & 1) != 0) {
    FUN_10014d60c(param_1,"others",6);
    uVar1 = *param_2;
  }
  if ((uVar1 >> 1 & 1) != 0) {
    FUN_10014d60c(param_1,"clips",5);
    uVar1 = *param_2;
  }
  if ((uVar1 >> 2 & 1) != 0) {
    FUN_10014d60c(param_1,"other-audio",0xb);
    uVar1 = *param_2;
  }
  if ((uVar1 >> 3 & 1) != 0) {
    FUN_10014d60c(param_1,"groove",6);
    uVar1 = *param_2;
  }
  if ((uVar1 >> 4 & 1) != 0) {
    FUN_10014d60c(param_1,"max-patches",0xb);
    uVar1 = *param_2;
  }
  if ((uVar1 >> 5 & 1) != 0) {
    FUN_10014d60c(param_1,"live-presets",0xc);
    uVar1 = *param_2;
  }
  if ((uVar1 >> 6 & 1) != 0) {
    FUN_10014d60c(param_1,"video",5);
    uVar1 = *param_2;
  }
  if ((uVar1 >> 7 & 1) != 0) {
    FUN_10014d60c(param_1,"rex-files",9);
    uVar1 = *param_2;
  }
  if ((uVar1 >> 8 & 1) != 0) {
    FUN_10014d60c(param_1,"device-folders",0xe);
    uVar1 = *param_2;
  }
  if ((uVar1 >> 9 & 1) != 0) {
    FUN_10014d60c(param_1,"other-folders",0xd);
    uVar1 = *param_2;
  }
  if ((uVar1 >> 10 & 1) != 0) {
    FUN_10014d60c(param_1,"images",6);
    uVar1 = *param_2;
  }
  if ((uVar1 >> 0xb & 1) != 0) {
    FUN_10014d60c(param_1,"restricted-encoded-audio",0x18);
    uVar1 = *param_2;
  }
  if ((uVar1 >> 0xc & 1) != 0) {
    FUN_10014d60c(param_1,"restricted-direct-show-audio",0x1c);
    uVar1 = *param_2;
  }
  if ((uVar1 >> 0xd & 1) != 0) {
    FUN_10014d60c(param_1,"restricted-direct-show-m4a-audio",0x20);
    uVar1 = *param_2;
  }
  if ((uVar1 >> 0xe & 1) != 0) {
    FUN_10014d60c(param_1,"plugin-presets",0xe);
    uVar1 = *param_2;
  }
  if ((uVar1 >> 0xf & 1) == 0) {
    return param_1;
  }
  pcVar2 = "plugins";
  uVar3 = 7;
LAB_10016b52c:
  FUN_10014d60c(param_1,pcVar2,uVar3);
  return param_1;
}

