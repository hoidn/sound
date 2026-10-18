
ulong FUN_1024b0300(void)

{
  int *piVar1;
  char cVar2;
  undefined8 uVar3;
  int *piVar4;
  undefined8 unaff_RBX;
  ulong uVar5;
  int *local_48;
  int *local_40;
  int *local_38;
  int *local_30;
  int *local_28;
  char local_19;
  
  DAT_10749b880 = '\0';
  cVar2 = FUN_1024b0650(0xffff8003);
  if (cVar2 == '\0') {
LAB_1024b03d7:
    if (DAT_10749b880 == '\0') {
      FUN_1011a7c70(&local_30);
      FUN_1011a7c70(&local_28);
      FUN_1011a7c70(&local_48);
      FUN_1011a7c70(&local_40);
      FUN_1011a7c70(&local_38);
      FUN_101222a20(&DAT_10749b7f0,&local_30,&local_28,&local_48,&local_40,&local_38);
      if ((local_38 != (int *)0x0) && (*local_38 = *local_38 + -1, *local_38 == 0)) {
        FUN_101442b40();
      }
      if ((local_40 != (int *)0x0) && (*local_40 = *local_40 + -1, *local_40 == 0)) {
        FUN_101442b40();
      }
      if ((local_48 != (int *)0x0) && (*local_48 = *local_48 + -1, *local_48 == 0)) {
        FUN_101442b40();
      }
      if ((local_28 != (int *)0x0) && (*local_28 = *local_28 + -1, *local_28 == 0)) {
        FUN_101442b40();
      }
      if ((local_30 != (int *)0x0) && (*local_30 = *local_30 + -1, *local_30 == 0)) {
        FUN_101442b40();
      }
    }
  }
  else {
    cVar2 = FUN_1024b0650(0xffff8005);
    if (cVar2 == '\0') goto LAB_1024b03d7;
    local_19 = '\0';
    cVar2 = FUN_1024b0d30(0xffff8003,&local_19);
    if (cVar2 != '\0') {
      cVar2 = FUN_1024b0d30(0xffff8005,&local_19);
      if (cVar2 != '\0') {
        uVar5 = CONCAT71((int7)((ulong)unaff_RBX >> 8),1);
        if (local_19 == '\x01') {
          uVar3 = FUN_101863860();
          piVar4 = (int *)FUN_10186fa90(uVar3);
          if (piVar4 != (int *)0x0) {
            piVar4[2] = piVar4[2] + 1;
            local_30 = piVar4;
            FUN_101440510(&local_28,&DAT_10749b838);
            FUN_10196d620(piVar4,&local_28);
            if ((local_28 != (int *)0x0) && (*local_28 = *local_28 + -1, *local_28 == 0)) {
              FUN_101442b40();
            }
            piVar1 = piVar4 + 2;
            *piVar1 = *piVar1 + -1;
            if (*piVar1 == 0) {
              FUN_1012716c0(piVar4);
            }
          }
        }
        goto LAB_1024b054e;
      }
    }
    if (DAT_10749b880 == '\0') {
      FUN_1011a7c70(&local_30);
      FUN_1011a7c70(&local_28);
      FUN_1011a7c70(&local_48);
      FUN_1011a7c70(&local_40);
      FUN_1011a7c70(&local_38);
      FUN_101222a20(&DAT_10749b820,&local_30,&local_28,&local_48,&local_40,&local_38);
      if ((local_38 != (int *)0x0) && (*local_38 = *local_38 + -1, *local_38 == 0)) {
        FUN_101442b40();
      }
      if ((local_40 != (int *)0x0) && (*local_40 = *local_40 + -1, *local_40 == 0)) {
        FUN_101442b40();
      }
      if ((local_48 != (int *)0x0) && (*local_48 = *local_48 + -1, *local_48 == 0)) {
        FUN_101442b40();
      }
      if ((local_28 != (int *)0x0) && (*local_28 = *local_28 + -1, *local_28 == 0)) {
        FUN_101442b40();
      }
      if ((local_30 != (int *)0x0) && (*local_30 = *local_30 + -1, *local_30 == 0)) {
        FUN_101442b40();
      }
    }
  }
  uVar5 = 0;
LAB_1024b054e:
  return uVar5 & 0xffffffff;
}

