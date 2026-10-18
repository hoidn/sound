
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1031a7d8c(long *param_1,undefined8 param_2,undefined8 param_3,int *param_4)

{
  undefined8 uVar1;
  undefined8 uVar2;
  undefined8 uVar3;
  int iVar4;
  int *piVar5;
  undefined8 uVar6;
  char *pcVar7;
  int iVar8;
  long lVar9;
  long *plVar10;
  long lVar11;
  char *pcVar12;
  long lVar13;
  int *local_190;
  int *local_188;
  int *local_180;
  int *local_178;
  int *local_170;
  int *local_168;
  int *local_160;
  int *local_158;
  long local_150;
  int *local_148;
  int *local_140;
  int *local_138;
  int *local_130;
  undefined8 uStack_128;
  undefined1 auStack_120 [8];
  undefined1 auStack_118 [8];
  undefined1 auStack_110 [8];
  undefined1 auStack_108 [8];
  undefined1 auStack_100 [8];
  undefined1 auStack_f8 [8];
  undefined1 auStack_f0 [8];
  undefined1 auStack_e8 [8];
  undefined1 auStack_e0 [8];
  undefined1 auStack_d8 [8];
  undefined1 auStack_d0 [8];
  undefined1 auStack_c8 [8];
  undefined1 auStack_c0 [8];
  undefined1 auStack_b8 [8];
  undefined1 auStack_b0 [8];
  undefined1 auStack_a8 [8];
  undefined1 auStack_a0 [8];
  undefined1 auStack_98 [8];
  undefined1 auStack_90 [8];
  undefined1 auStack_88 [8];
  undefined1 auStack_80 [8];
  undefined1 auStack_78 [8];
  long local_70;
  
  local_70 = *(long *)PTR____stack_chk_guard_1064f8818;
  lVar9 = param_1[0x95];
  iVar8 = (int)param_2;
  pcVar7 = "LFO1";
  if (iVar8 != 0) {
    pcVar7 = "LFO2";
  }
  FUN_101427680(&local_138,pcVar7);
  FUN_10156fa68(lVar9,&local_138);
  if (iVar8 == 0) {
    if (local_138 != (int *)0x0) {
      iVar4 = *local_138;
      *local_138 = iVar4 + -1;
      if (iVar4 + -1 == 0) {
        FUN_101449efc();
      }
    }
    pcVar7 = "OSC1 On/Off";
  }
  else {
    if (local_138 != (int *)0x0) {
      iVar4 = *local_138;
      *local_138 = iVar4 + -1;
      if (iVar4 + -1 == 0) {
        FUN_101449efc();
      }
    }
    pcVar7 = "OSC2 On/Off";
  }
  local_130 = (int *)PTR__lambda___1__ARemoteable__TRemoteableUpdate__106551c78;
  uStack_128 = 0;
  FUN_101564728(param_1[0x98],iVar8 == 1,&local_130);
  FUN_10319285c(param_1[0xb],pcVar7,iVar8 == 0,0);
  if (((DAT_107028010 & 1) == 0) && (iVar4 = ___cxa_guard_acquire(&DAT_107028010), iVar4 != 0)) {
    FUN_101427680(&local_130,"Sine");
    FUN_101427680(&uStack_128,"Saw");
    FUN_101427680(auStack_120,"Rect");
    FUN_101427680(auStack_118,"Noise");
    FUN_1002c29cc(&DAT_1070281f0,&local_130,4);
    FUN_100234444(auStack_118);
    FUN_100234444(auStack_120);
    FUN_100234444(&uStack_128);
    FUN_100234444(&local_130);
    ___cxa_atexit(FUN_1002343c8,&DAT_1070281f0,0x100000000);
    ___cxa_guard_release(&DAT_107028010);
  }
  if (((DAT_107028018 & 1) == 0) && (iVar4 = ___cxa_guard_acquire(&DAT_107028018), iVar4 != 0)) {
    FUN_1030b33e4(0);
    FUN_101427680(&local_130);
    FUN_1030b33e4(3);
    FUN_101427680(&uStack_128);
    FUN_1030b33e4(1);
    FUN_101427680(auStack_120);
    FUN_1030b33e4(4);
    FUN_101427680(auStack_118);
    FUN_1002c29cc(&DAT_107028208,&local_130,4);
    FUN_100234444(auStack_118);
    FUN_100234444(auStack_120);
    FUN_100234444(&uStack_128);
    FUN_100234444(&local_130);
    ___cxa_atexit(FUN_1002343c8,&DAT_107028208,0x100000000);
    ___cxa_guard_release(&DAT_107028018);
  }
  lVar9 = param_1[0xe];
  pcVar7 = "OSC1 Shape";
  if (iVar8 != 0) {
    pcVar7 = "OSC2 Shape";
  }
  FUN_101427680(&local_140,pcVar7);
  FUN_1026ef060(lVar9,1,&DAT_107028208,&local_140,1);
  if (iVar8 == 0) {
    if (local_140 != (int *)0x0) {
      iVar4 = *local_140;
      *local_140 = iVar4 + -1;
      if (iVar4 + -1 == 0) {
        FUN_101449efc();
      }
    }
  }
  else if (local_140 != (int *)0x0) {
    iVar4 = *local_140;
    *local_140 = iVar4 + -1;
    if (iVar4 + -1 == 0) {
      FUN_101449efc();
    }
  }
  lVar9 = param_1[0xe];
  piVar5 = (int *)FUN_1012d9850(0x20);
  FUN_10143bd04(piVar5,&DAT_1070281f0);
  if (piVar5 != (int *)0x0) {
    piVar5[2] = piVar5[2] + 1;
  }
  local_130 = piVar5;
  FUN_1026fc44c(lVar9,piVar5);
  if (piVar5 != (int *)0x0) {
    iVar4 = piVar5[2];
    piVar5[2] = iVar4 + -1;
    if (iVar4 + -1 == 0) {
      FUN_10128eea0(piVar5);
    }
  }
  if (((DAT_107028028 & 1) == 0) && (iVar4 = ___cxa_guard_acquire(&DAT_107028028), iVar4 != 0)) {
    lVar9 = FUN_1012d9850(0x38);
    FUN_101577e1c(0xc0400000,0x40400000,lVar9,1);
    DAT_107028020 = lVar9;
    if (lVar9 != 0) {
      *(int *)(lVar9 + 8) = *(int *)(lVar9 + 8) + 1;
    }
    ___cxa_atexit(FUN_1002483c0,&DAT_107028020,0x100000000);
    ___cxa_guard_release(&DAT_107028028);
  }
  lVar9 = DAT_107028020;
  lVar11 = param_1[0x11];
  uVar6 = FUN_101439478();
  pcVar7 = "OSC1 Octave";
  if (iVar8 != 0) {
    pcVar7 = "OSC2 Octave";
  }
  FUN_101427680(&local_148,pcVar7);
  FUN_1026f0b58(0xc0400000,0x40400000,0,lVar11,param_3,lVar9,uVar6,&local_148,2);
  if (iVar8 == 0) {
    if (local_148 != (int *)0x0) {
      iVar4 = *local_148;
      *local_148 = iVar4 + -1;
      if (iVar4 + -1 == 0) {
        FUN_101449efc();
      }
    }
  }
  else if (local_148 != (int *)0x0) {
    iVar4 = *local_148;
    *local_148 = iVar4 + -1;
    if (iVar4 + -1 == 0) {
      FUN_101449efc();
    }
  }
  plVar10 = param_1 + 0x11;
  uVar6 = (**(code **)(*(long *)*plVar10 + 0x2b0))();
  FUN_1024dd614(uVar6,2);
  uVar6 = (**(code **)(*(long *)*plVar10 + 0x2b0))();
  FUN_1024dd624(uVar6,param_1[0x14]);
  uVar6 = FUN_1026f96b0(*plVar10);
  FUN_1024dd614(uVar6,2);
  uVar6 = FUN_1026f96b0(*plVar10);
  FUN_1024dd624(uVar6,param_1[0x14]);
  FUN_1026f96b0(*plVar10);
  FUN_1025ba00c(0xc0400000,0x40400000);
  FUN_1026f1850(*plVar10,0);
  if (((DAT_107028038 & 1) == 0) && (iVar4 = ___cxa_guard_acquire(&DAT_107028038), iVar4 != 0)) {
    lVar9 = FUN_1012d9850(0x38);
    FUN_101577e1c(0xc1400000,0x41400000,lVar9,1);
    DAT_107028030 = lVar9;
    if (lVar9 != 0) {
      *(int *)(lVar9 + 8) = *(int *)(lVar9 + 8) + 1;
    }
    ___cxa_atexit(FUN_1002483c0,&DAT_107028030,0x100000000);
    ___cxa_guard_release(&DAT_107028038);
  }
  lVar9 = DAT_107028030;
  lVar13 = param_1[0x17];
  FUN_101427680(&local_158," st");
  lVar11 = FUN_1012d9850(0x20);
  local_130 = local_158;
  local_158 = (int *)0x0;
  FUN_101436450(lVar11,&local_130);
  if (lVar11 != 0) {
    *(int *)(lVar11 + 8) = *(int *)(lVar11 + 8) + 1;
  }
  local_150 = lVar11;
  if (local_130 != (int *)0x0) {
    iVar4 = *local_130;
    *local_130 = iVar4 + -1;
    if (iVar4 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (iVar8 == 0) {
    FUN_101427680(&local_160,"OSC1 Semi");
  }
  else {
    FUN_101427680(&local_160,"OSC2 Semi");
  }
  FUN_1026f0b58(0xc1400000,0x41400000,0,lVar13,param_3,lVar9,lVar11,&local_160,2);
  if (iVar8 == 0) {
    if (local_160 != (int *)0x0) {
      iVar4 = *local_160;
      *local_160 = iVar4 + -1;
      if (iVar4 + -1 == 0) {
        FUN_101449efc();
      }
    }
  }
  else if (local_160 != (int *)0x0) {
    iVar4 = *local_160;
    *local_160 = iVar4 + -1;
    if (iVar4 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (lVar11 != 0) {
    iVar4 = *(int *)(lVar11 + 8) + -1;
    *(int *)(lVar11 + 8) = iVar4;
    if (iVar4 == 0) {
      FUN_10128eea0(lVar11);
    }
  }
  if (local_158 != (int *)0x0) {
    iVar4 = *local_158;
    *local_158 = iVar4 + -1;
    if (iVar4 + -1 == 0) {
      FUN_101449efc();
    }
  }
  plVar10 = param_1 + 0x17;
  uVar6 = (**(code **)(*(long *)*plVar10 + 0x2b0))();
  FUN_1024dd614(uVar6,2);
  uVar6 = (**(code **)(*(long *)*plVar10 + 0x2b0))();
  FUN_1024dd624(uVar6,param_1[0x1a]);
  uVar6 = FUN_1026f96b0(*plVar10);
  FUN_1024dd614(uVar6,2);
  uVar6 = FUN_1026f96b0(*plVar10);
  FUN_1024dd624(uVar6,param_1[0x1a]);
  FUN_1026f96b0(*plVar10);
  FUN_1025ba00c(0xc1400000,0x41400000);
  FUN_1026f1850(*plVar10,0);
  if (((DAT_107028040 & 1) == 0) && (iVar4 = ___cxa_guard_acquire(&DAT_107028040), iVar4 != 0)) {
    FUN_101427680(&local_130,"Sub");
    FUN_101427680(&uStack_128,"Sync");
    FUN_1002c29cc(&DAT_107028220,&local_130,2);
    FUN_100234444(&uStack_128);
    FUN_100234444(&local_130);
    ___cxa_atexit(FUN_1002343c8,&DAT_107028220,0x100000000);
    ___cxa_guard_release(&DAT_107028040);
  }
  lVar9 = param_1[0x1d];
  pcVar7 = "OSC1 Mode";
  if (iVar8 != 0) {
    pcVar7 = "OSC2 Mode";
  }
  FUN_101427680(&local_168,pcVar7);
  FUN_1026ef060(lVar9,0,&DAT_107028220,&local_168,1);
  if (iVar8 == 0) {
    if (local_168 != (int *)0x0) {
      iVar4 = *local_168;
      *local_168 = iVar4 + -1;
      if (iVar4 + -1 == 0) {
        FUN_101449efc();
      }
    }
    pcVar7 = "OSC1 Env Time";
    pcVar12 = "PEG1 Time";
  }
  else {
    if (local_168 != (int *)0x0) {
      iVar4 = *local_168;
      *local_168 = iVar4 + -1;
      if (iVar4 + -1 == 0) {
        FUN_101449efc();
      }
    }
    pcVar7 = "OSC2 Env Time";
    pcVar12 = "PEG2 Time";
  }
  iVar4 = *param_4;
  lVar9 = param_1[0x20];
  *param_4 = iVar4 + 6;
  piVar5 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  *(undefined ***)piVar5 = &PTR_thunk_FUN_10128edf8_1068ddff8;
  piVar5[6] = iVar4 + 5;
  uVar1 = _UNK_10561dfd8;
  uVar6 = _DAT_10561dfd0;
  *(undefined8 *)(piVar5 + 10) = _UNK_10561dfd8;
  *(undefined8 *)(piVar5 + 8) = uVar6;
  piVar5[2] = piVar5[2] + 1;
  local_130 = piVar5;
  FUN_103192720(0x3f000000,param_3,lVar9,pcVar7,piVar5,pcVar12,0);
  iVar4 = piVar5[2];
  piVar5[2] = iVar4 + -1;
  if (iVar4 + -1 == 0) {
    FUN_10128eea0(piVar5);
  }
  lVar9 = param_1[0x23];
  iVar4 = *param_4;
  *param_4 = iVar4 + 1;
  piVar5 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  pcVar7 = "OSC1 Detune";
  if (iVar8 != 0) {
    pcVar7 = "OSC2 Detune";
  }
  *(undefined ***)piVar5 = &PTR_thunk_FUN_10128edf8_1068ddff8;
  piVar5[6] = iVar4;
  *(undefined8 *)(piVar5 + 10) = uVar1;
  *(undefined8 *)(piVar5 + 8) = uVar6;
  piVar5[2] = piVar5[2] + 1;
  local_130 = piVar5;
  FUN_103192720(0x3f000000,param_3,lVar9,pcVar7,piVar5,0,2);
  iVar4 = piVar5[2];
  piVar5[2] = iVar4 + -1;
  if (iVar4 + -1 == 0) {
    FUN_10128eea0(piVar5);
  }
  lVar9 = param_1[0x26];
  iVar4 = *param_4;
  *param_4 = iVar4 + 1;
  piVar5 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  pcVar7 = "OSC1 Keytrack";
  if (iVar8 != 0) {
    pcVar7 = "OSC2 Keytrack";
  }
  *(undefined ***)piVar5 = &PTR_thunk_FUN_10128edf8_1068ddff8;
  piVar5[6] = iVar4;
  *(undefined8 *)(piVar5 + 10) = uVar1;
  *(undefined8 *)(piVar5 + 8) = uVar6;
  piVar5[2] = piVar5[2] + 1;
  pcVar12 = "O1 Keytrack";
  if (iVar8 != 0) {
    pcVar12 = "O2 Keytrack";
  }
  local_130 = piVar5;
  FUN_103192720(0x3f000000,param_3,lVar9,pcVar7,piVar5,pcVar12,0);
  iVar4 = piVar5[2];
  piVar5[2] = iVar4 + -1;
  if (iVar4 + -1 == 0) {
    FUN_10128eea0(piVar5);
  }
  lVar9 = param_1[0x29];
  iVar4 = *param_4;
  *param_4 = iVar4 + 1;
  piVar5 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  pcVar7 = "OSC1 Pulse Width";
  if (iVar8 != 0) {
    pcVar7 = "OSC2 Pulse Width";
  }
  *(undefined ***)piVar5 = &PTR_thunk_FUN_10128edf8_1068ddff8;
  piVar5[6] = iVar4;
  *(undefined8 *)(piVar5 + 10) = uVar1;
  *(undefined8 *)(piVar5 + 8) = uVar6;
  piVar5[2] = piVar5[2] + 1;
  pcVar12 = "OSC1 PW";
  if (iVar8 != 0) {
    pcVar12 = "OSC2 PW";
  }
  local_130 = piVar5;
  FUN_103192720(0x3f000000,param_3,lVar9,pcVar7,piVar5,pcVar12,2);
  iVar4 = piVar5[2];
  piVar5[2] = iVar4 + -1;
  if (iVar4 + -1 == 0) {
    FUN_10128eea0(piVar5);
  }
  lVar9 = param_1[0x2c];
  iVar4 = *param_4;
  *param_4 = iVar4 + 1;
  piVar5 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  pcVar7 = "OSC1 Sub/Sync Amount";
  if (iVar8 != 0) {
    pcVar7 = "OSC2 Sub/Sync Amount";
  }
  *(undefined ***)piVar5 = &PTR_thunk_FUN_10128edf8_1068ddff8;
  piVar5[6] = iVar4;
  *(undefined8 *)(piVar5 + 10) = uVar1;
  *(undefined8 *)(piVar5 + 8) = uVar6;
  piVar5[2] = piVar5[2] + 1;
  pcVar12 = "O1 Sub/Sync";
  if (iVar8 != 0) {
    pcVar12 = "O2 Sub/Sync";
  }
  local_130 = piVar5;
  FUN_103192720(0,param_3,lVar9,pcVar7,piVar5,pcVar12,0);
  iVar4 = piVar5[2];
  piVar5[2] = iVar4 + -1;
  if (iVar4 + -1 == 0) {
    FUN_10128eea0(piVar5);
  }
  lVar9 = param_1[0x2f];
  iVar4 = *param_4;
  *param_4 = iVar4 + 1;
  piVar5 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  pcVar7 = "OSC1 Balance";
  if (iVar8 != 0) {
    pcVar7 = "OSC2 Balance";
  }
  *(undefined ***)piVar5 = &PTR_thunk_FUN_10128edf8_1068ddff8;
  piVar5[6] = iVar4;
  *(undefined8 *)(piVar5 + 10) = uVar1;
  *(undefined8 *)(piVar5 + 8) = uVar6;
  piVar5[2] = piVar5[2] + 1;
  local_130 = piVar5;
  FUN_103192720(0x3f000000,param_3,lVar9,pcVar7,piVar5,0,0);
  iVar4 = piVar5[2];
  piVar5[2] = iVar4 + -1;
  if (iVar4 + -1 == 0) {
    FUN_10128eea0(piVar5);
  }
  lVar9 = param_1[0x32];
  iVar4 = *param_4;
  *param_4 = iVar4 + 1;
  piVar5 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  pcVar7 = "OSC1 Env Initial";
  if (iVar8 != 0) {
    pcVar7 = "OSC2 Env Initial";
  }
  *(undefined ***)piVar5 = &PTR_thunk_FUN_10128edf8_1068ddff8;
  piVar5[6] = iVar4;
  uVar3 = _UNK_1058c6a88;
  uVar2 = _DAT_1058c6a80;
  *(undefined8 *)(piVar5 + 10) = _UNK_1058c6a88;
  *(undefined8 *)(piVar5 + 8) = uVar2;
  piVar5[2] = piVar5[2] + 1;
  pcVar12 = "PEG1 Amount";
  if (iVar8 != 0) {
    pcVar12 = "PEG2 Amount";
  }
  local_130 = piVar5;
  FUN_103192974(0,param_3,lVar9,pcVar7,piVar5,pcVar12,0);
  iVar4 = piVar5[2];
  piVar5[2] = iVar4 + -1;
  if (iVar4 + -1 == 0) {
    FUN_10128eea0(piVar5);
  }
  iVar4 = *param_4;
  lVar9 = param_1[0x35];
  *param_4 = iVar4 + 2;
  piVar5 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  pcVar7 = "OSC1 Pitch < LFO";
  if (iVar8 != 0) {
    pcVar7 = "OSC2 Pitch < LFO";
  }
  *(undefined ***)piVar5 = &PTR_thunk_FUN_10128edf8_1068ddff8;
  piVar5[6] = iVar4 + 1;
  *(undefined8 *)(piVar5 + 10) = uVar3;
  *(undefined8 *)(piVar5 + 8) = uVar2;
  piVar5[2] = piVar5[2] + 1;
  pcVar12 = "OSC1 < LFO";
  if (iVar8 != 0) {
    pcVar12 = "OSC2 < LFO";
  }
  local_130 = piVar5;
  FUN_103192974(0,param_3,lVar9,pcVar7,piVar5,pcVar12,0);
  iVar4 = piVar5[2];
  piVar5[2] = iVar4 + -1;
  if (iVar4 + -1 == 0) {
    FUN_10128eea0(piVar5);
  }
  iVar4 = *param_4;
  lVar9 = param_1[0x38];
  *param_4 = iVar4 + 2;
  piVar5 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  pcVar7 = "OSC1 PW < LFO";
  if (iVar8 != 0) {
    pcVar7 = "OSC2 PW < LFO";
  }
  *(undefined ***)piVar5 = &PTR_thunk_FUN_10128edf8_1068ddff8;
  piVar5[6] = iVar4 + 1;
  *(undefined8 *)(piVar5 + 10) = uVar3;
  *(undefined8 *)(piVar5 + 8) = uVar2;
  piVar5[2] = piVar5[2] + 1;
  pcVar12 = "O1 PW < LFO";
  if (iVar8 != 0) {
    pcVar12 = "O2 PW < LFO";
  }
  local_130 = piVar5;
  FUN_103192974(0,param_3,lVar9,pcVar7,piVar5,pcVar12,0);
  iVar4 = piVar5[2];
  piVar5[2] = iVar4 + -1;
  if (iVar4 + -1 == 0) {
    FUN_10128eea0(piVar5);
  }
  iVar4 = *param_4;
  lVar9 = param_1[0x3b];
  *param_4 = iVar4 + 2;
  piVar5 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  pcVar7 = "OSC1 Level";
  if (iVar8 != 0) {
    pcVar7 = "OSC2 Level";
  }
  *(undefined ***)piVar5 = &PTR_thunk_FUN_10128edf8_1068ddff8;
  piVar5[6] = iVar4 + 1;
  *(undefined8 *)(piVar5 + 10) = uVar1;
  *(undefined8 *)(piVar5 + 8) = uVar6;
  piVar5[2] = piVar5[2] + 1;
  local_130 = piVar5;
  FUN_103192720(0x3f4e6320,param_3,lVar9,pcVar7,piVar5,0,0);
  iVar4 = piVar5[2];
  piVar5[2] = iVar4 + -1;
  if (iVar4 + -1 == 0) {
    FUN_10128eea0(piVar5);
  }
  pcVar7 = "F1 On/Off";
  if (iVar8 != 0) {
    pcVar7 = "F2 On/Off";
  }
  FUN_10319285c(param_1[0x3e],pcVar7,0,0);
  if (((DAT_107028048 & 1) == 0) && (iVar4 = ___cxa_guard_acquire(&DAT_107028048), iVar4 != 0)) {
    FUN_101427680(&local_130,"LP12");
    FUN_101427680("LP24");
    FUN_101427680("BP6");
    FUN_101427680("BP12");
    FUN_101427680("N2P");
    FUN_101427680("N4P");
    FUN_101427680(auStack_100,"HP12");
    FUN_101427680(auStack_f8,"HP24");
    FUN_101427680(auStack_f0,"F6");
    FUN_101427680(auStack_e8,"F12");
    FUN_1002c29cc(&DAT_107028238,&local_130,10);
    FUN_100234444(auStack_e8);
    FUN_100234444(auStack_f0);
    FUN_100234444(auStack_f8);
    FUN_100234444(auStack_100);
    FUN_100234444(auStack_108);
    FUN_100234444(auStack_110);
    FUN_100234444(auStack_118);
    FUN_100234444(auStack_120);
    FUN_100234444(&uStack_128);
    FUN_100234444(&local_130);
    ___cxa_atexit(FUN_1002343c8,&DAT_107028238,0x100000000);
    ___cxa_guard_release(&DAT_107028048);
  }
  if (((DAT_107028050 & 1) == 0) && (iVar4 = ___cxa_guard_acquire(&DAT_107028050), iVar4 != 0)) {
    FUN_101427680(&local_130,"Low-pass 12dB/oct");
    FUN_101427680("Low-pass 24dB/oct");
    FUN_101427680("Band-pass 6dB/oct");
    FUN_101427680("Band-pass 12dB/oct");
    FUN_101427680("Notch 2-pole");
    FUN_101427680("Notch 4-pole");
    FUN_101427680(auStack_100,"High-pass 12dB/oct");
    FUN_101427680(auStack_f8,"High-pass 24dB/oct");
    FUN_101427680(auStack_f0,"Formant 6dB/oct");
    FUN_101427680(auStack_e8,"Formant 12dB/oct");
    FUN_1002c29cc(&DAT_107028250,&local_130,10);
    FUN_100234444(auStack_e8);
    FUN_100234444(auStack_f0);
    FUN_100234444(auStack_f8);
    FUN_100234444(auStack_100);
    FUN_100234444(auStack_108);
    FUN_100234444(auStack_110);
    FUN_100234444(auStack_118);
    FUN_100234444(auStack_120);
    FUN_100234444(&uStack_128);
    FUN_100234444(&local_130);
    ___cxa_atexit(FUN_1002343c8,&DAT_107028250,0x100000000);
    ___cxa_guard_release(&DAT_107028050);
  }
  lVar9 = param_1[0x41];
  pcVar7 = "F1 Type";
  if (iVar8 != 0) {
    pcVar7 = "F2 Type";
  }
  FUN_101427680(&local_170,pcVar7);
  FUN_1026ef0dc(lVar9,0,&DAT_107028250,&DAT_107028238,&local_170,1);
  if (iVar8 == 0) {
    if (local_170 != (int *)0x0) {
      iVar4 = *local_170;
      *local_170 = iVar4 + -1;
      if (iVar4 + -1 == 0) {
        FUN_101449efc();
      }
    }
  }
  else if (local_170 != (int *)0x0) {
    iVar4 = *local_170;
    *local_170 = iVar4 + -1;
    if (iVar4 + -1 == 0) {
      FUN_101449efc();
    }
  }
  lVar9 = param_1[0x41];
  piVar5 = (int *)FUN_1012d9850(0x20);
  FUN_10143bd04(piVar5,&DAT_107028238);
  if (piVar5 != (int *)0x0) {
    piVar5[2] = piVar5[2] + 1;
  }
  local_130 = piVar5;
  FUN_1026efa48(lVar9,piVar5);
  if (piVar5 != (int *)0x0) {
    iVar4 = piVar5[2];
    piVar5[2] = iVar4 + -1;
    if (iVar4 + -1 == 0) {
      FUN_10128eea0(piVar5);
    }
  }
  if (((DAT_107028058 & 1) == 0) && (iVar4 = ___cxa_guard_acquire(&DAT_107028058), iVar4 != 0)) {
    FUN_101427680(&local_130,"Off");
    FUN_101427680("Sym1");
    FUN_101427680(auStack_120,"Sym2");
    FUN_101427680(auStack_118,"Sym3");
    FUN_101427680(auStack_110,"Asym1");
    FUN_101427680(auStack_108,"Asym2");
    FUN_101427680(auStack_100,"Asym3");
    FUN_1002c29cc(&DAT_107028268,&local_130,7);
    FUN_100234444(auStack_100);
    FUN_100234444(auStack_108);
    FUN_100234444(auStack_110);
    FUN_100234444(auStack_118);
    FUN_100234444(auStack_120);
    FUN_100234444(&uStack_128);
    FUN_100234444(&local_130);
    ___cxa_atexit(FUN_1002343c8,&DAT_107028268,0x100000000);
    ___cxa_guard_release(&DAT_107028058);
  }
  lVar9 = param_1[0x44];
  pcVar7 = "F1 Drive";
  if (iVar8 != 0) {
    pcVar7 = "F2 Drive";
  }
  FUN_101427680(&local_178,pcVar7);
  FUN_1026ef060(lVar9,0,&DAT_107028268,&local_178,1);
  if (iVar8 == 0) {
    if (local_178 != (int *)0x0) {
      iVar4 = *local_178;
      *local_178 = iVar4 + -1;
      if (iVar4 + -1 == 0) {
        FUN_101449efc();
      }
    }
    pcVar7 = "F1 Freq < Key";
  }
  else {
    if (local_178 != (int *)0x0) {
      iVar4 = *local_178;
      *local_178 = iVar4 + -1;
      if (iVar4 + -1 == 0) {
        FUN_101449efc();
      }
    }
    pcVar7 = "F2 Freq < Key";
  }
  iVar4 = *param_4;
  lVar9 = param_1[0x47];
  *param_4 = iVar4 + 5;
  piVar5 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  *(undefined ***)piVar5 = &PTR_thunk_FUN_10128edf8_1068ddff8;
  piVar5[6] = iVar4 + 4;
  *(undefined8 *)(piVar5 + 10) = uVar3;
  *(undefined8 *)(piVar5 + 8) = uVar2;
  piVar5[2] = piVar5[2] + 1;
  local_130 = piVar5;
  FUN_103192974(0,param_3,lVar9,pcVar7,piVar5,0,0);
  iVar4 = piVar5[2];
  piVar5[2] = iVar4 + -1;
  if (iVar4 + -1 == 0) {
    FUN_10128eea0(piVar5);
  }
  iVar4 = *param_4;
  lVar9 = param_1[0x4a];
  *param_4 = iVar4 + 2;
  piVar5 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  pcVar7 = "F1 Freq";
  if (iVar8 != 0) {
    pcVar7 = "F2 Freq";
  }
  *(undefined ***)piVar5 = &PTR_thunk_FUN_10128edf8_1068ddff8;
  piVar5[6] = iVar4 + 1;
  *(undefined8 *)(piVar5 + 10) = uVar1;
  *(undefined8 *)(piVar5 + 8) = uVar6;
  piVar5[2] = piVar5[2] + 1;
  local_130 = piVar5;
  FUN_103192720(0x3f800000,param_3,lVar9,pcVar7,piVar5,0,2);
  iVar4 = piVar5[2];
  piVar5[2] = iVar4 + -1;
  if (iVar4 + -1 == 0) {
    FUN_10128eea0(piVar5);
  }
  lVar9 = param_1[0x4d];
  iVar4 = *param_4;
  *param_4 = iVar4 + 1;
  piVar5 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  pcVar7 = "F1 Reso < Key";
  if (iVar8 != 0) {
    pcVar7 = "F2 Reso < Key";
  }
  *(undefined ***)piVar5 = &PTR_thunk_FUN_10128edf8_1068ddff8;
  piVar5[6] = iVar4;
  *(undefined8 *)(piVar5 + 10) = uVar3;
  *(undefined8 *)(piVar5 + 8) = uVar2;
  piVar5[2] = piVar5[2] + 1;
  local_130 = piVar5;
  FUN_103192974(0,param_3,lVar9,pcVar7,piVar5,0,0);
  iVar4 = piVar5[2];
  piVar5[2] = iVar4 + -1;
  if (iVar4 + -1 == 0) {
    FUN_10128eea0(piVar5);
  }
  iVar4 = *param_4;
  lVar9 = param_1[0x50];
  *param_4 = iVar4 + 2;
  piVar5 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  pcVar7 = "F1 Resonance";
  if (iVar8 != 0) {
    pcVar7 = "F2 Resonance";
  }
  *(undefined ***)piVar5 = &PTR_thunk_FUN_10128edf8_1068ddff8;
  piVar5[6] = iVar4 + 1;
  *(undefined8 *)(piVar5 + 10) = uVar1;
  *(undefined8 *)(piVar5 + 8) = uVar6;
  piVar5[2] = piVar5[2] + 1;
  local_130 = piVar5;
  FUN_103192720(0,param_3,lVar9,pcVar7,piVar5,0,0);
  iVar4 = piVar5[2];
  piVar5[2] = iVar4 + -1;
  if (iVar4 + -1 == 0) {
    FUN_10128eea0(piVar5);
  }
  *param_4 = *param_4 + 1;
  (**(code **)(*param_1 + 0x1f0))(param_1,param_3);
  lVar9 = param_1[0x53];
  iVar4 = *param_4;
  *param_4 = iVar4 + 1;
  piVar5 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  pcVar7 = "F1 Freq < LFO";
  if (iVar8 != 0) {
    pcVar7 = "F2 Freq < LFO";
  }
  *(undefined ***)piVar5 = &PTR_thunk_FUN_10128edf8_1068ddff8;
  piVar5[6] = iVar4;
  *(undefined8 *)(piVar5 + 10) = uVar3;
  *(undefined8 *)(piVar5 + 8) = uVar2;
  piVar5[2] = piVar5[2] + 1;
  local_130 = piVar5;
  FUN_103192974(0,param_3,lVar9,pcVar7,piVar5,0,0);
  iVar4 = piVar5[2];
  piVar5[2] = iVar4 + -1;
  if (iVar4 + -1 == 0) {
    FUN_10128eea0(piVar5);
  }
  iVar4 = *param_4;
  lVar9 = param_1[0x56];
  *param_4 = iVar4 + 2;
  piVar5 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  pcVar7 = "F1 Freq < Env";
  if (iVar8 != 0) {
    pcVar7 = "F2 Freq < Env";
  }
  *(undefined ***)piVar5 = &PTR_thunk_FUN_10128edf8_1068ddff8;
  piVar5[6] = iVar4 + 1;
  *(undefined8 *)(piVar5 + 10) = uVar3;
  *(undefined8 *)(piVar5 + 8) = uVar2;
  piVar5[2] = piVar5[2] + 1;
  local_130 = piVar5;
  FUN_103192974(0,param_3,lVar9,pcVar7,piVar5,0,0);
  iVar4 = piVar5[2];
  piVar5[2] = iVar4 + -1;
  if (iVar4 + -1 == 0) {
    FUN_10128eea0(piVar5);
  }
  iVar4 = *param_4;
  lVar9 = param_1[0x59];
  *param_4 = iVar4 + 2;
  piVar5 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  pcVar7 = "F1 Reso < LFO";
  if (iVar8 != 0) {
    pcVar7 = "F2 Reso < LFO";
  }
  *(undefined ***)piVar5 = &PTR_thunk_FUN_10128edf8_1068ddff8;
  piVar5[6] = iVar4 + 1;
  *(undefined8 *)(piVar5 + 10) = uVar3;
  *(undefined8 *)(piVar5 + 8) = uVar2;
  piVar5[2] = piVar5[2] + 1;
  pcVar12 = "F1 Res < LFO";
  if (iVar8 != 0) {
    pcVar12 = "F2 Res < LFO";
  }
  local_130 = piVar5;
  FUN_103192974(0,param_3,lVar9,pcVar7,piVar5,pcVar12,0);
  iVar4 = piVar5[2];
  piVar5[2] = iVar4 + -1;
  if (iVar4 + -1 == 0) {
    FUN_10128eea0(piVar5);
  }
  iVar4 = *param_4;
  lVar9 = param_1[0x5c];
  *param_4 = iVar4 + 2;
  piVar5 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  pcVar7 = "F1 Reso < Env";
  if (iVar8 != 0) {
    pcVar7 = "F2 Reso < Env";
  }
  *(undefined ***)piVar5 = &PTR_thunk_FUN_10128edf8_1068ddff8;
  piVar5[6] = iVar4 + 1;
  *(undefined8 *)(piVar5 + 10) = uVar3;
  *(undefined8 *)(piVar5 + 8) = uVar2;
  piVar5[2] = piVar5[2] + 1;
  pcVar12 = "F1 Res < Env";
  if (iVar8 != 0) {
    pcVar12 = "F2 Res < Env";
  }
  local_130 = piVar5;
  FUN_103192974(0,param_3,lVar9,pcVar7,piVar5,pcVar12,0);
  iVar4 = piVar5[2];
  piVar5[2] = iVar4 + -1;
  if (iVar4 + -1 == 0) {
    FUN_10128eea0(piVar5);
  }
  *param_4 = *param_4 + 1;
  pcVar7 = "AMP1 On/Off";
  if (iVar8 != 0) {
    pcVar7 = "AMP2 On/Off";
  }
  FUN_10319285c(param_1[0x5f],pcVar7,iVar8 == 0,0);
  iVar4 = *param_4;
  lVar9 = param_1[0x62];
  *param_4 = iVar4 + 2;
  piVar5 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  pcVar7 = "AMP1 < Key";
  if (iVar8 != 0) {
    pcVar7 = "AMP2 < Key";
  }
  *(undefined ***)piVar5 = &PTR_thunk_FUN_10128edf8_1068ddff8;
  piVar5[6] = iVar4 + 1;
  *(undefined8 *)(piVar5 + 10) = uVar3;
  *(undefined8 *)(piVar5 + 8) = uVar2;
  piVar5[2] = piVar5[2] + 1;
  local_130 = piVar5;
  FUN_103192974(0,param_3,lVar9,pcVar7,piVar5,0,0);
  iVar4 = piVar5[2];
  piVar5[2] = iVar4 + -1;
  if (iVar4 + -1 == 0) {
    FUN_10128eea0(piVar5);
  }
  iVar4 = *param_4;
  lVar9 = param_1[0x65];
  *param_4 = iVar4 + 2;
  piVar5 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  pcVar7 = "AMP1 Level";
  if (iVar8 != 0) {
    pcVar7 = "AMP2 Level";
  }
  *(undefined ***)piVar5 = &PTR_thunk_FUN_10128edf8_1068ddff8;
  piVar5[6] = iVar4 + 1;
  *(undefined8 *)(piVar5 + 10) = uVar1;
  *(undefined8 *)(piVar5 + 8) = uVar6;
  piVar5[2] = piVar5[2] + 1;
  local_130 = piVar5;
  FUN_103192720(0x3f5e76c9,param_3,lVar9,pcVar7,piVar5,0,0);
  iVar4 = piVar5[2];
  piVar5[2] = iVar4 + -1;
  if (iVar4 + -1 == 0) {
    FUN_10128eea0(piVar5);
  }
  lVar9 = param_1[0x68];
  iVar4 = *param_4;
  *param_4 = iVar4 + 1;
  piVar5 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  pcVar7 = "AMP1 Pan < Key";
  if (iVar8 != 0) {
    pcVar7 = "AMP2 Pan < Key";
  }
  *(undefined ***)piVar5 = &PTR_thunk_FUN_10128edf8_1068ddff8;
  piVar5[6] = iVar4;
  *(undefined8 *)(piVar5 + 10) = uVar3;
  *(undefined8 *)(piVar5 + 8) = uVar2;
  piVar5[2] = piVar5[2] + 1;
  pcVar12 = "A1 Pan < Key";
  if (iVar8 != 0) {
    pcVar12 = "A2 Pan < Key";
  }
  local_130 = piVar5;
  FUN_103192974(0,param_3,lVar9,pcVar7,piVar5,pcVar12,0);
  iVar4 = piVar5[2];
  piVar5[2] = iVar4 + -1;
  if (iVar4 + -1 == 0) {
    FUN_10128eea0(piVar5);
  }
  iVar4 = *param_4;
  lVar9 = param_1[0x6b];
  *param_4 = iVar4 + 2;
  piVar5 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  pcVar7 = "AMP1 Pan";
  if (iVar8 != 0) {
    pcVar7 = "AMP2 Pan";
  }
  *(undefined ***)piVar5 = &PTR_thunk_FUN_10128edf8_1068ddff8;
  piVar5[6] = iVar4 + 1;
  *(undefined8 *)(piVar5 + 10) = uVar1;
  *(undefined8 *)(piVar5 + 8) = uVar6;
  piVar5[2] = piVar5[2] + 1;
  local_130 = piVar5;
  FUN_103192720(0x3f000000,param_3,lVar9,pcVar7,piVar5,0,2);
  iVar4 = piVar5[2];
  piVar5[2] = iVar4 + -1;
  if (iVar4 + -1 == 0) {
    FUN_10128eea0(piVar5);
  }
  lVar9 = param_1[0x6e];
  iVar4 = *param_4;
  *param_4 = iVar4 + 1;
  piVar5 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  pcVar7 = "AMP1 < LFO";
  if (iVar8 != 0) {
    pcVar7 = "AMP2 < LFO";
  }
  *(undefined ***)piVar5 = &PTR_thunk_FUN_10128edf8_1068ddff8;
  piVar5[6] = iVar4;
  *(undefined8 *)(piVar5 + 10) = uVar3;
  *(undefined8 *)(piVar5 + 8) = uVar2;
  piVar5[2] = piVar5[2] + 1;
  local_130 = piVar5;
  FUN_103192974(0,param_3,lVar9,pcVar7,piVar5,0,0);
  iVar4 = piVar5[2];
  piVar5[2] = iVar4 + -1;
  if (iVar4 + -1 == 0) {
    FUN_10128eea0(piVar5);
  }
  iVar4 = *param_4;
  lVar9 = param_1[0x71];
  *param_4 = iVar4 + 2;
  piVar5 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  pcVar7 = "AMP1 Pan < LFO";
  if (iVar8 != 0) {
    pcVar7 = "AMP2 Pan < LFO";
  }
  *(undefined ***)piVar5 = &PTR_thunk_FUN_10128edf8_1068ddff8;
  piVar5[6] = iVar4 + 1;
  *(undefined8 *)(piVar5 + 10) = uVar3;
  *(undefined8 *)(piVar5 + 8) = uVar2;
  piVar5[2] = piVar5[2] + 1;
  pcVar12 = "A1 Pan < LFO";
  if (iVar8 != 0) {
    pcVar12 = "A2 Pan < LFO";
  }
  local_130 = piVar5;
  FUN_103192974(0,param_3,lVar9,pcVar7,piVar5,pcVar12,0);
  iVar4 = piVar5[2];
  piVar5[2] = iVar4 + -1;
  if (iVar4 + -1 == 0) {
    FUN_10128eea0(piVar5);
  }
  iVar4 = *param_4;
  lVar9 = param_1[0x74];
  *param_4 = iVar4 + 2;
  piVar5 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  pcVar7 = "AMP1 Pan < Env";
  if (iVar8 != 0) {
    pcVar7 = "AMP2 Pan < Env";
  }
  *(undefined ***)piVar5 = &PTR_thunk_FUN_10128edf8_1068ddff8;
  piVar5[6] = iVar4 + 1;
  *(undefined8 *)(piVar5 + 10) = uVar3;
  *(undefined8 *)(piVar5 + 8) = uVar2;
  piVar5[2] = piVar5[2] + 1;
  pcVar12 = "A1 Pan < Env";
  if (iVar8 != 0) {
    pcVar12 = "A2 Pan < Env";
  }
  local_130 = piVar5;
  FUN_103192974(0,param_3,lVar9,pcVar7,piVar5,pcVar12,0);
  iVar4 = piVar5[2];
  piVar5[2] = iVar4 + -1;
  if (iVar4 + -1 == 0) {
    FUN_10128eea0(piVar5);
  }
  *param_4 = *param_4 + 1;
  pcVar7 = "LFO1 On/Off";
  if (iVar8 != 0) {
    pcVar7 = "LFO2 On/Off";
  }
  FUN_10319285c(param_1[0x77],pcVar7,0,0);
  if (((DAT_107028060 & 1) == 0) && (iVar4 = ___cxa_guard_acquire(&DAT_107028060), iVar4 != 0)) {
    FUN_101427680(&local_130,"Sine");
    FUN_101427680(&uStack_128,"Tri");
    FUN_101427680(auStack_120,"Rect");
    FUN_101427680(auStack_118,"Noise1");
    FUN_101427680(auStack_110,"Noise2");
    FUN_1002c29cc(&DAT_107028280,&local_130,5);
    FUN_100234444(auStack_110);
    FUN_100234444(auStack_118);
    FUN_100234444(auStack_120);
    FUN_100234444(&uStack_128);
    FUN_100234444(&local_130);
    ___cxa_atexit(FUN_1002343c8,&DAT_107028280,0x100000000);
    ___cxa_guard_release(&DAT_107028060);
  }
  if (((DAT_107028068 & 1) == 0) && (iVar4 = ___cxa_guard_acquire(&DAT_107028068), iVar4 != 0)) {
    FUN_1030b33e4(0);
    FUN_101427680(&local_130);
    FUN_1030b33e4(2);
    FUN_101427680(&uStack_128);
    FUN_1030b33e4(1);
    FUN_101427680(auStack_120);
    FUN_1030b33e4(4);
    FUN_101427680(auStack_118);
    FUN_1030b33e4(5);
    FUN_101427680(auStack_110);
    FUN_1002c29cc(&DAT_107028298,&local_130,5);
    FUN_100234444(auStack_110);
    FUN_100234444(auStack_118);
    FUN_100234444(auStack_120);
    FUN_100234444(&uStack_128);
    FUN_100234444(&local_130);
    ___cxa_atexit(FUN_1002343c8,&DAT_107028298,0x100000000);
    ___cxa_guard_release(&DAT_107028068);
  }
  lVar9 = param_1[0x7a];
  pcVar7 = "LFO1 Wave Shape";
  if (iVar8 != 0) {
    pcVar7 = "LFO2 Wave Shape";
  }
  FUN_101427680(&local_180,pcVar7);
  FUN_1026ef060(lVar9,0,&DAT_107028280,&local_180,1);
  if (iVar8 == 0) {
    if (local_180 != (int *)0x0) {
      iVar4 = *local_180;
      *local_180 = iVar4 + -1;
      if (iVar4 + -1 == 0) {
        FUN_101449efc();
      }
    }
    plVar10 = (long *)param_1[0x7a];
    pcVar7 = "LFO1 Shape";
  }
  else {
    if (local_180 != (int *)0x0) {
      iVar4 = *local_180;
      *local_180 = iVar4 + -1;
      if (iVar4 + -1 == 0) {
        FUN_101449efc();
      }
    }
    plVar10 = (long *)param_1[0x7a];
    pcVar7 = "LFO2 Shape";
  }
  FUN_101427680(&local_130,pcVar7);
  (**(code **)(*plVar10 + 0x298))(plVar10,&local_130);
  if (local_130 != (int *)0x0) {
    iVar4 = *local_130;
    *local_130 = iVar4 + -1;
    if (iVar4 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (((DAT_107028070 & 1) == 0) && (iVar4 = ___cxa_guard_acquire(&DAT_107028070), iVar4 != 0)) {
    FUN_101427680(&local_130,"4d");
    FUN_101427680("4");
    FUN_101427680("4t");
    FUN_101427680("2d");
    FUN_101427680("2");
    FUN_101427680("2t");
    FUN_101427680("1d");
    FUN_101427680("1");
    FUN_101427680("1t");
    FUN_101427680("1/2d");
    FUN_101427680("1/2");
    FUN_101427680("1/2t");
    FUN_101427680("1/4d");
    FUN_101427680("1/4");
    FUN_101427680("1/4t");
    FUN_101427680("1/8d");
    FUN_101427680("1/8");
    FUN_101427680("1/8t");
    FUN_101427680("1/16d");
    FUN_101427680("1/16");
    FUN_101427680(auStack_90,"1/16t");
    FUN_101427680(auStack_88,"1/32d");
    FUN_101427680(auStack_80,"1/32");
    FUN_101427680(auStack_78,"1/32t");
    FUN_1002c29cc(&DAT_1070282b0,&local_130,0x18);
    FUN_100234444(auStack_78);
    FUN_100234444(auStack_80);
    FUN_100234444(auStack_88);
    FUN_100234444(auStack_90);
    FUN_100234444(auStack_98);
    FUN_100234444(auStack_a0);
    FUN_100234444(auStack_a8);
    FUN_100234444(auStack_b0);
    FUN_100234444(auStack_b8);
    FUN_100234444(auStack_c0);
    FUN_100234444(auStack_c8);
    FUN_100234444(auStack_d0);
    FUN_100234444(auStack_d8);
    FUN_100234444(auStack_e0);
    FUN_100234444(auStack_e8);
    FUN_100234444(auStack_f0);
    FUN_100234444(auStack_f8);
    FUN_100234444(auStack_100);
    FUN_100234444(auStack_108);
    FUN_100234444(auStack_110);
    FUN_100234444(auStack_118);
    FUN_100234444(auStack_120);
    FUN_100234444(&uStack_128);
    FUN_100234444(&local_130);
    ___cxa_atexit(FUN_1002343c8,&DAT_1070282b0,0x100000000);
    ___cxa_guard_release(&DAT_107028070);
  }
  if (((DAT_107028080 & 1) == 0) && (iVar4 = ___cxa_guard_acquire(&DAT_107028080), iVar4 != 0)) {
    lVar9 = FUN_1012d9850(0x38);
    FUN_101577e1c(0,0x41b80000,lVar9,1);
    DAT_107028078 = lVar9;
    if (lVar9 != 0) {
      *(int *)(lVar9 + 8) = *(int *)(lVar9 + 8) + 1;
    }
    ___cxa_atexit(FUN_1002483c0,&DAT_107028078,0x100000000);
    ___cxa_guard_release(&DAT_107028080);
  }
  lVar9 = DAT_107028078;
  lVar11 = param_1[0x7d];
  piVar5 = (int *)FUN_1012d9850(0x20);
  FUN_10143bd04(piVar5,&DAT_1070282b0);
  if (piVar5 != (int *)0x0) {
    piVar5[2] = piVar5[2] + 1;
  }
  local_130 = piVar5;
  if (iVar8 == 0) {
    FUN_101427680(&local_188,"LFO1 Sync Rate");
  }
  else {
    FUN_101427680(&local_188,"LFO2 Sync Rate");
  }
  FUN_1026f0b58(0,0x41b80000,0x41500000,lVar11,param_3,lVar9,piVar5,&local_188,2);
  if (iVar8 == 0) {
    if (local_188 != (int *)0x0) {
      iVar4 = *local_188;
      *local_188 = iVar4 + -1;
      if (iVar4 + -1 == 0) {
        FUN_101449efc();
      }
    }
  }
  else if (local_188 != (int *)0x0) {
    iVar4 = *local_188;
    *local_188 = iVar4 + -1;
    if (iVar4 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (piVar5 != (int *)0x0) {
    iVar4 = piVar5[2];
    piVar5[2] = iVar4 + -1;
    if (iVar4 + -1 == 0) {
      FUN_10128eea0(piVar5);
    }
  }
  plVar10 = (long *)param_1[0x7d];
  pcVar7 = "LFO1 SncRate";
  if (iVar8 != 0) {
    pcVar7 = "LFO2 SncRate";
  }
  FUN_101427680(&local_130,pcVar7);
  (**(code **)(*plVar10 + 0x298))(plVar10,&local_130);
  if (local_130 != (int *)0x0) {
    iVar4 = *local_130;
    *local_130 = iVar4 + -1;
    if (iVar4 + -1 == 0) {
      FUN_101449efc();
    }
  }
  pcVar7 = "LFO1 Retrigger";
  if (iVar8 != 0) {
    pcVar7 = "LFO2 Retrigger";
  }
  pcVar12 = "LFO1 Retrig";
  if (iVar8 != 0) {
    pcVar12 = "LFO2 Retrig";
  }
  FUN_10319285c(param_1[0x83],pcVar7,0,pcVar12);
  if (((DAT_107028088 & 1) == 0) && (iVar4 = ___cxa_guard_acquire(&DAT_107028088), iVar4 != 0)) {
    FUN_101427680(&local_130,"Hertz");
    FUN_101427680(&uStack_128,"Beat");
    FUN_1002c29cc(&DAT_1070282c8,&local_130,2);
    FUN_100234444(&uStack_128);
    FUN_100234444(&local_130);
    ___cxa_atexit(FUN_1002343c8,&DAT_1070282c8,0x100000000);
    ___cxa_guard_release(&DAT_107028088);
  }
  if (((DAT_107028090 & 1) == 0) && (iVar4 = ___cxa_guard_acquire(&DAT_107028090), iVar4 != 0)) {
    FUN_1030b33e4(6);
    FUN_101427680(&local_130);
    FUN_1030b33e4(7);
    FUN_101427680(&uStack_128);
    FUN_1002c29cc(&DAT_1070282e0,&local_130,2);
    FUN_100234444(&uStack_128);
    FUN_100234444(&local_130);
    ___cxa_atexit(FUN_1002343c8,&DAT_1070282e0,0x100000000);
    ___cxa_guard_release(&DAT_107028090);
  }
  lVar9 = param_1[0x80];
  pcVar7 = "LFO1 Sync On/Off";
  if (iVar8 != 0) {
    pcVar7 = "LFO2 Sync On/Off";
  }
  FUN_101427680(&local_190,pcVar7);
  FUN_1026ef060(lVar9,0,&DAT_1070282e0,&local_190,1);
  if (iVar8 == 0) {
    if (local_190 != (int *)0x0) {
      iVar4 = *local_190;
      *local_190 = iVar4 + -1;
      if (iVar4 + -1 == 0) {
        FUN_101449efc();
      }
    }
  }
  else if (local_190 != (int *)0x0) {
    iVar4 = *local_190;
    *local_190 = iVar4 + -1;
    if (iVar4 + -1 == 0) {
      FUN_101449efc();
    }
  }
  lVar9 = param_1[0x80];
  piVar5 = (int *)FUN_1012d9850(0x20);
  FUN_10143bd04(piVar5,&DAT_1070282c8);
  if (piVar5 != (int *)0x0) {
    piVar5[2] = piVar5[2] + 1;
  }
  local_130 = piVar5;
  FUN_1026fc44c(lVar9,piVar5);
  if (piVar5 != (int *)0x0) {
    iVar4 = piVar5[2];
    piVar5[2] = iVar4 + -1;
    if (iVar4 + -1 == 0) {
      FUN_10128eea0(piVar5);
    }
  }
  plVar10 = (long *)param_1[0x80];
  pcVar7 = "LFO1 Sync";
  if (iVar8 != 0) {
    pcVar7 = "LFO2 Sync";
  }
  FUN_101427680(&local_130,pcVar7);
  (**(code **)(*plVar10 + 0x298))(plVar10,&local_130);
  if (local_130 != (int *)0x0) {
    iVar4 = *local_130;
    *local_130 = iVar4 + -1;
    if (iVar4 + -1 == 0) {
      FUN_101449efc();
    }
  }
  iVar4 = *param_4;
  lVar9 = param_1[0x86];
  *param_4 = iVar4 + 5;
  piVar5 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  pcVar7 = "LFO1 Pulse Width";
  if (iVar8 != 0) {
    pcVar7 = "LFO2 Pulse Width";
  }
  *(undefined ***)piVar5 = &PTR_thunk_FUN_10128edf8_1068ddff8;
  piVar5[6] = iVar4 + 4;
  *(undefined8 *)(piVar5 + 10) = uVar1;
  *(undefined8 *)(piVar5 + 8) = uVar6;
  piVar5[2] = piVar5[2] + 1;
  pcVar12 = "LFO1 PW";
  if (iVar8 != 0) {
    pcVar12 = "LFO2 PW";
  }
  local_130 = piVar5;
  FUN_103192720(0x3f000000,param_3,lVar9,pcVar7,piVar5,pcVar12,2);
  iVar4 = piVar5[2];
  piVar5[2] = iVar4 + -1;
  if (iVar4 + -1 == 0) {
    FUN_10128eea0(piVar5);
  }
  lVar9 = param_1[0x89];
  iVar4 = *param_4;
  *param_4 = iVar4 + 1;
  piVar5 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  pcVar7 = "LFO1 Speed";
  if (iVar8 != 0) {
    pcVar7 = "LFO2 Speed";
  }
  *(undefined ***)piVar5 = &PTR_thunk_FUN_10128edf8_1068ddff8;
  piVar5[6] = iVar4;
  *(undefined8 *)(piVar5 + 10) = uVar1;
  *(undefined8 *)(piVar5 + 8) = uVar6;
  piVar5[2] = piVar5[2] + 1;
  local_130 = piVar5;
  FUN_103192720(0x3f000000,param_3,lVar9,pcVar7,piVar5,0,0);
  iVar4 = piVar5[2];
  piVar5[2] = iVar4 + -1;
  if (iVar4 + -1 == 0) {
    FUN_10128eea0(piVar5);
  }
  lVar9 = param_1[0x8c];
  iVar4 = *param_4;
  *param_4 = iVar4 + 1;
  piVar5 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  pcVar7 = "LFO1 Phase";
  if (iVar8 != 0) {
    pcVar7 = "LFO2 Phase";
  }
  *(undefined ***)piVar5 = &PTR_thunk_FUN_10128edf8_1068ddff8;
  piVar5[6] = iVar4;
  *(undefined8 *)(piVar5 + 10) = uVar1;
  *(undefined8 *)(piVar5 + 8) = uVar6;
  piVar5[2] = piVar5[2] + 1;
  local_130 = piVar5;
  FUN_103192720(0,param_3,lVar9,pcVar7,piVar5,0,0);
  iVar4 = piVar5[2];
  piVar5[2] = iVar4 + -1;
  if (iVar4 + -1 == 0) {
    FUN_10128eea0(piVar5);
  }
  lVar9 = param_1[0x8f];
  iVar4 = *param_4;
  *param_4 = iVar4 + 1;
  piVar5 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  pcVar7 = "LFO1 Delay";
  if (iVar8 != 0) {
    pcVar7 = "LFO2 Delay";
  }
  *(undefined ***)piVar5 = &PTR_thunk_FUN_10128edf8_1068ddff8;
  piVar5[6] = iVar4;
  *(undefined8 *)(piVar5 + 10) = uVar1;
  *(undefined8 *)(piVar5 + 8) = uVar6;
  piVar5[2] = piVar5[2] + 1;
  local_130 = piVar5;
  FUN_103192720(0,param_3,lVar9,pcVar7,piVar5,0,0);
  iVar4 = piVar5[2];
  piVar5[2] = iVar4 + -1;
  if (iVar4 + -1 == 0) {
    FUN_10128eea0(piVar5);
  }
  lVar9 = param_1[0x92];
  iVar4 = *param_4;
  *param_4 = iVar4 + 1;
  piVar5 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  pcVar7 = "LFO1 Fade In";
  if (iVar8 != 0) {
    pcVar7 = "LFO2 Fade In";
  }
  *(undefined ***)piVar5 = &PTR_thunk_FUN_10128edf8_1068ddff8;
  piVar5[6] = iVar4;
  *(undefined8 *)(piVar5 + 10) = uVar1;
  *(undefined8 *)(piVar5 + 8) = uVar6;
  piVar5[2] = piVar5[2] + 1;
  local_130 = piVar5;
  FUN_103192720(0,param_3,lVar9,pcVar7,piVar5,0,0);
  iVar8 = piVar5[2];
  piVar5[2] = iVar8 + -1;
  if (iVar8 + -1 == 0) {
    FUN_10128eea0(piVar5);
  }
  FUN_1031b4554(param_1[0x9b],param_2,0,param_3,param_4);
  FUN_1031b4554(param_1[0x9e],param_2,1,param_3,param_4);
  if (*(long *)PTR____stack_chk_guard_1064f8818 == local_70) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

