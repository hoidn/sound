
ulong FUN_100140cb8(undefined8 param_1,int param_2,undefined8 param_3,undefined8 param_4,
                   char *param_5)

{
  int iVar1;
  ulong uVar2;
  undefined8 *local_20;
  ulong uStack_18;
  
  if (param_2 < 0x21) {
    if (param_2 == 1) {
      return 0x960;
    }
    if (param_2 == 2) {
      return DAT_100b94e78;
    }
    if (param_2 == 0x20) {
      builtin_strncpy(param_5,"Ableton",8);
      return 1;
    }
  }
  else if (param_2 < 0x25) {
    if (param_2 == 0x21) {
      builtin_strncpy(param_5,"Live",5);
      return 1;
    }
    if (param_2 == 0x22) {
      return (long)(DAT_100b94e70 / 10);
    }
  }
  else if (param_2 == 0x25) {
    iVar1 = _strcmp(param_5,"shellCategory");
    if (iVar1 == 0) {
      return 10;
    }
  }
  else if (param_2 == 0x26) {
    if ((DAT_100b94e80 & 1) == 0) {
      FUN_100964d48();
    }
    local_20 = DAT_100b94e88;
    uStack_18 = DAT_100b94e90;
    if (-1 < (char)DAT_100b94e9f) {
      local_20 = &DAT_100b94e88;
      uStack_18 = (ulong)DAT_100b94e9f;
    }
    uVar2 = FUN_100140c0c(&local_20);
    return uVar2 & 0xffffffff;
  }
  return 0;
}

