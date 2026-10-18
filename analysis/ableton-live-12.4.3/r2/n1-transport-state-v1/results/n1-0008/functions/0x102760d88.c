
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

code * FUN_102760d88(code *param_1)

{
  code *pcVar1;
  code *pcVar2;
  code *pcVar3;
  code *pcVar4;
  undefined *puVar5;
  undefined *puVar6;
  code *pcVar7;
  int iVar8;
  undefined8 *puVar9;
  long lVar10;
  undefined8 uVar11;
  long lVar12;
  code *pcVar13;
  int *piVar14;
  long *plVar15;
  undefined8 *puVar16;
  undefined8 *puVar17;
  long *plVar18;
  long lVar19;
  undefined8 uVar20;
  code *pcVar21;
  double dVar22;
  float fVar23;
  undefined1 auVar24 [16];
  undefined4 local_100;
  undefined4 local_fc;
  undefined4 local_f8;
  undefined4 uStack_f4;
  int *local_f0;
  int *local_e8;
  int *local_e0;
  int *local_d8;
  code **local_d0;
  ulong local_c8;
  code *local_c0;
  code *pcStack_b8;
  code *local_b0;
  long local_a8;
  undefined *local_a0;
  code *pcStack_98;
  undefined1 auStack_90 [8];
  int *local_88;
  long local_80;
  
  local_80 = *(long *)PTR____stack_chk_guard_1064f8818;
  puVar9 = (undefined8 *)FUN_1014826c4();
  *puVar9 = &PTR_thunk_FUN_102766edc_1068031d8;
  FUN_101563fa0(&local_c0);
  FUN_10150b1cc(puVar9 + 5,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x28) = &PTR_thunk_FUN_10150b2b4_106592670;
  *(undefined4 *)(param_1 + 0x40) = 2;
  *(undefined8 *)(param_1 + 0x48) = 0;
  *(undefined1 **)(param_1 + 0x50) = &DAT_7fefffffffffffff;
  FUN_1015643d8(&local_c0);
  FUN_10150b1cc(param_1 + 0x58,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x58) = &PTR_thunk_FUN_10150b2b4_10658fdd8;
  *(undefined1 **)(param_1 + 0x78) = &DAT_7fefffffffffffff;
  *(undefined1 **)(param_1 + 0x70) = &DAT_7fefffffffffffff;
  *(undefined1 **)(param_1 + 0x80) = &DAT_7fefffffffffffff;
  *(undefined2 *)(param_1 + 0x88) = 0;
  FUN_1015643d8(&local_c0);
  FUN_10150b1cc(param_1 + 0x90,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x90) = &PTR_thunk_FUN_10150b2b4_10658fdd8;
  FUN_1015643d8(&local_c0);
  FUN_10150b1cc(param_1 + 0xa8,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0xa8) = &PTR_thunk_FUN_10150b2b4_10658fdd8;
  FUN_1015643d8(&local_c0);
  FUN_10150b1cc(param_1 + 0xc0,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0xc0) = &PTR_thunk_FUN_10150b2b4_10658fdd8;
  FUN_10156915c(&local_c0);
  FUN_10150b1cc(param_1 + 0xd8,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  pcVar13 = param_1 + 0xf0;
  *(long *)pcVar13 = 0;
  *(undefined ***)(param_1 + 0xd8) = &PTR_thunk_FUN_10150b2b4_10658fd48;
  FUN_1015643d8(&local_c0);
  lVar10 = *(long *)pcVar13;
  if ((lVar10 != 0) && (iVar8 = *(int *)(lVar10 + 8) + -1, *(int *)(lVar10 + 8) = iVar8, iVar8 == 0)
     ) {
    FUN_10128eea0();
  }
  *(code **)(param_1 + 0xf0) = local_c0;
  FUN_1015686ac(&local_c0);
  FUN_10150b1cc(param_1 + 0xf8,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0xf8) = &PTR_thunk_FUN_10150b2b4_1065a39c8;
  puVar6 = PTR__lambda___1___106551f08;
  *(undefined **)(param_1 + 0x110) = PTR__lambda___1___106551f08;
  *(undefined8 *)(param_1 + 0x118) = 0;
  FUN_1015643d8(&local_c0);
  FUN_10150b1cc(param_1 + 0x120,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x120) = &PTR_thunk_FUN_10150b2b4_10658fdd8;
  FUN_1015643d8(&local_c0);
  FUN_10150b1cc(param_1 + 0x138,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x138) = &PTR_thunk_FUN_10150b2b4_10658fdd8;
  *(undefined8 *)(param_1 + 0x160) = 0;
  *(undefined8 *)(param_1 + 0x168) = 0;
  *(undefined **)(param_1 + 0x150) = &DAT_106598220;
  *(undefined8 *)(param_1 + 0x158) = 0;
  FUN_101563fa0(&local_c0);
  FUN_10150b1cc(param_1 + 0x170,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x170) = &PTR_thunk_FUN_10150b2b4_106592670;
  *(undefined8 *)(param_1 + 0x198) = 0;
  *(undefined8 *)(param_1 + 0x1a0) = 0;
  *(undefined **)(param_1 + 0x188) = &DAT_106598220;
  *(undefined8 *)(param_1 + 400) = 0;
  FUN_1015643d8(&local_c0);
  FUN_10150b1cc(param_1 + 0x1a8,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x1a8) = &PTR_thunk_FUN_10150b2b4_10658fdd8;
  FUN_10276df68(&local_c0);
  FUN_10150b1cc(param_1 + 0x1c0,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x1c0) = &PTR_thunk_FUN_10150b2b4_106804810;
  FUN_10276e290(&local_c0);
  FUN_10150b1cc(param_1 + 0x1d8,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x1d8) = &PTR_thunk_FUN_10150b2b4_1068048a0;
  FUN_101565098(&local_c0);
  FUN_10150b1cc(param_1 + 0x1f0,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x1f0) = &PTR_thunk_FUN_10150b2b4_10673f310;
  FUN_101565098(&local_c0);
  FUN_10150b1cc(param_1 + 0x208,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x208) = &PTR_thunk_FUN_10150b2b4_10673f310;
  FUN_1027730b4(param_1 + 0x220);
  FUN_10276d678(&local_c0);
  FUN_10150b1cc(param_1 + 0x238,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x238) = &PTR_thunk_FUN_10150b2b4_1068049c0;
  FUN_101563fa0(&local_c0);
  FUN_10150b1cc(param_1 + 0x250,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x250) = &PTR_thunk_FUN_10150b2b4_106592670;
  FUN_10276d678(&local_c0);
  FUN_10150b1cc(param_1 + 0x268,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x268) = &PTR_thunk_FUN_10150b2b4_1068049c0;
  pcVar21 = param_1 + 0x280;
  *(undefined8 *)(param_1 + 0x280) = 0;
  FUN_1015643d8(&local_c0);
  lVar10 = *(long *)pcVar21;
  if ((lVar10 != 0) && (iVar8 = *(int *)(lVar10 + 8) + -1, *(int *)(lVar10 + 8) = iVar8, iVar8 == 0)
     ) {
    FUN_10128eea0();
  }
  *(code **)(param_1 + 0x280) = local_c0;
  FUN_101563fa0(&local_c0);
  FUN_10150b1cc(param_1 + 0x288,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x288) = &PTR_thunk_FUN_10150b2b4_106592670;
  FUN_1015740f0(&local_c0);
  FUN_10150b1cc(param_1 + 0x2a0,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x2a0) = &PTR_thunk_FUN_10150b2b4_106590220;
  FUN_1015643d8(&local_c0);
  FUN_10150b1cc(param_1 + 0x2b8,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x2b8) = &PTR_thunk_FUN_10150b2b4_10658fdd8;
  FUN_1015643d8(&local_c0);
  FUN_10150b1cc(param_1 + 0x2d0,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x2d0) = &PTR_thunk_FUN_10150b2b4_10658fdd8;
  FUN_10260a70c(&local_c0);
  FUN_10150b1cc(param_1 + 0x2e8,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x2e8) = &PTR_thunk_FUN_10150b2b4_1067bd7a8;
  FUN_10260a70c(&local_c0);
  FUN_10150b1cc(param_1 + 0x300,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x300) = &PTR_thunk_FUN_10150b2b4_1067bd7a8;
  FUN_10260a70c(&local_c0);
  FUN_10150b1cc(param_1 + 0x318,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x318) = &PTR_thunk_FUN_10150b2b4_1067bd7a8;
  FUN_10260a70c(&local_c0);
  FUN_10150b1cc(param_1 + 0x330,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x330) = &PTR_thunk_FUN_10150b2b4_1067bd7a8;
  FUN_10260a70c(&local_c0);
  FUN_10150b1cc(param_1 + 0x348,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x348) = &PTR_thunk_FUN_10150b2b4_1067bd7a8;
  FUN_10260a70c(&local_c0);
  FUN_10150b1cc(param_1 + 0x360,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x360) = &PTR_thunk_FUN_10150b2b4_1067bd7a8;
  FUN_10260a70c(&local_c0);
  FUN_10150b1cc(param_1 + 0x378,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x378) = &PTR_thunk_FUN_10150b2b4_1067bd7a8;
  FUN_10260a70c(&local_c0);
  FUN_10150b1cc(param_1 + 0x390,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x390) = &PTR_thunk_FUN_10150b2b4_1067bd7a8;
  FUN_10260a70c(&local_c0);
  FUN_10150b1cc(param_1 + 0x3a8,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x3a8) = &PTR_thunk_FUN_10150b2b4_1067bd7a8;
  FUN_10260a70c(&local_c0);
  FUN_10150b1cc(param_1 + 0x3c0,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x3c0) = &PTR_thunk_FUN_10150b2b4_1067bd7a8;
  FUN_10260a70c(&local_c0);
  FUN_10150b1cc(param_1 + 0x3d8,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x3d8) = &PTR_thunk_FUN_10150b2b4_1067bd7a8;
  FUN_10260a70c(&local_c0);
  FUN_10150b1cc(param_1 + 0x3f0,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x3f0) = &PTR_thunk_FUN_10150b2b4_1067bd7a8;
  FUN_10260a70c(&local_c0);
  FUN_10150b1cc(param_1 + 0x408,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x408) = &PTR_thunk_FUN_10150b2b4_1067bd7a8;
  FUN_10260a70c(&local_c0);
  FUN_10150b1cc(param_1 + 0x420,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x420) = &PTR_thunk_FUN_10150b2b4_1067bd7a8;
  FUN_10260a70c(&local_c0);
  FUN_10150b1cc(param_1 + 0x438,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x438) = &PTR_thunk_FUN_10150b2b4_1067bd7a8;
  FUN_10260a70c(&local_c0);
  FUN_10150b1cc(param_1 + 0x450,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x450) = &PTR_thunk_FUN_10150b2b4_1067bd7a8;
  FUN_10260a70c(&local_c0);
  FUN_10150b1cc(param_1 + 0x468,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x468) = &PTR_thunk_FUN_10150b2b4_1067bd7a8;
  FUN_10260a70c(&local_c0);
  FUN_10150b1cc(param_1 + 0x480,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x480) = &PTR_thunk_FUN_10150b2b4_1067bd7a8;
  FUN_10260a70c(&local_c0);
  FUN_10150b1cc(param_1 + 0x498,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x498) = &PTR_thunk_FUN_10150b2b4_1067bd7a8;
  FUN_10260a70c(&local_c0);
  FUN_10150b1cc(param_1 + 0x4b0,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x4b0) = &PTR_thunk_FUN_10150b2b4_1067bd7a8;
  FUN_10260a70c(&local_c0);
  FUN_10150b1cc(param_1 + 0x4c8,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x4c8) = &PTR_thunk_FUN_10150b2b4_1067bd7a8;
  FUN_10260a70c(&local_c0);
  FUN_10150b1cc(param_1 + 0x4e0,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x4e0) = &PTR_thunk_FUN_10150b2b4_1067bd7a8;
  FUN_10260a70c(&local_c0);
  FUN_10150b1cc(param_1 + 0x4f8,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x4f8) = &PTR_thunk_FUN_10150b2b4_1067bd7a8;
  FUN_1027731bc(param_1 + 0x510);
  FUN_1015740f0(&local_c0);
  FUN_10150b1cc(param_1 + 0x528,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x528) = &PTR_thunk_FUN_10150b2b4_106590220;
  FUN_1015740f0(&local_c0);
  FUN_10150b1cc(param_1 + 0x540,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x540) = &PTR_thunk_FUN_10150b2b4_106590220;
  FUN_1015740f0(&local_c0);
  FUN_10150b1cc(param_1 + 0x558,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x558) = &PTR_thunk_FUN_10150b2b4_106590220;
  FUN_1015643d8(&local_c0);
  FUN_10150b1cc(param_1 + 0x570,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x570) = &PTR_thunk_FUN_10150b2b4_10658fdd8;
  FUN_101563fa0(&local_c0);
  FUN_10150b1cc(param_1 + 0x588,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x588) = &PTR_thunk_FUN_10150b2b4_106592670;
  FUN_1015643d8(&local_c0);
  FUN_10150b1cc(param_1 + 0x5a0,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x5a0) = &PTR_thunk_FUN_10150b2b4_10658fdd8;
  FUN_1015643d8(&local_c0);
  FUN_10150b1cc(param_1 + 0x5b8,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x5b8) = &PTR_thunk_FUN_10150b2b4_10658fdd8;
  FUN_1015643d8(&local_c0);
  FUN_10150b1cc(param_1 + 0x5d0,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x5d0) = &PTR_thunk_FUN_10150b2b4_10658fdd8;
  FUN_101563fa0(&local_c0);
  FUN_10150b1cc(param_1 + 0x5e8,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x5e8) = &PTR_thunk_FUN_10150b2b4_106592670;
  FUN_1015643d8(&local_c0);
  FUN_10150b1cc(param_1 + 0x600,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x600) = &PTR_thunk_FUN_10150b2b4_10658fdd8;
  FUN_1015643d8(&local_c0);
  FUN_10150b1cc(param_1 + 0x618,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x618) = &PTR_thunk_FUN_10150b2b4_10658fdd8;
  FUN_1015643d8(&local_c0);
  FUN_10150b1cc(param_1 + 0x630,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x630) = &PTR_thunk_FUN_10150b2b4_10658fdd8;
  FUN_101565f54(&local_c0);
  FUN_10150b1cc(param_1 + 0x648,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x648) = &PTR_thunk_FUN_10150b2b4_1065925e0;
  FUN_1015643d8(&local_c0);
  FUN_10150b1cc(param_1 + 0x660,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x660) = &PTR_thunk_FUN_10150b2b4_10658fdd8;
  FUN_1015643d8(&local_c0);
  FUN_10150b1cc(param_1 + 0x678,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x678) = &PTR_thunk_FUN_10150b2b4_10658fdd8;
  FUN_101563fa0(&local_c0);
  FUN_10150b1cc(param_1 + 0x690,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x690) = &PTR_thunk_FUN_10150b2b4_106592670;
  FUN_1027732b0(param_1 + 0x6a8);
  FUN_1015643d8(&local_c0);
  FUN_10150b1cc(param_1 + 0x6c0,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x6c0) = &PTR_thunk_FUN_10150b2b4_10658fdd8;
  pcVar1 = param_1 + 0x6d8;
  *(undefined8 *)(param_1 + 0x6d8) = 0;
  FUN_1015643d8(&local_c0);
  lVar10 = *(long *)pcVar1;
  if ((lVar10 != 0) && (iVar8 = *(int *)(lVar10 + 8) + -1, *(int *)(lVar10 + 8) = iVar8, iVar8 == 0)
     ) {
    FUN_10128eea0();
  }
  *(code **)(param_1 + 0x6d8) = local_c0;
  FUN_1015643d8(&local_c0);
  FUN_10150b1cc(param_1 + 0x6e0,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x6e0) = &PTR_thunk_FUN_10150b2b4_10658fdd8;
  FUN_101565f54(&local_c0);
  FUN_10150b1cc(param_1 + 0x6f8,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x6f8) = &PTR_thunk_FUN_10150b2b4_1065925e0;
  FUN_1015686ac(&local_c0);
  FUN_10150b1cc(param_1 + 0x710,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x710) = &PTR_thunk_FUN_10150b2b4_1065a39c8;
  FUN_101563fa0(&local_c0);
  FUN_10150b1cc(param_1 + 0x728,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x728) = &PTR_thunk_FUN_10150b2b4_106592670;
  FUN_1015643d8(&local_c0);
  FUN_10150b1cc(param_1 + 0x740,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x740) = &PTR_thunk_FUN_10150b2b4_10658fdd8;
  FUN_1015686ac(&local_c0);
  FUN_10150b1cc(param_1 + 0x758,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x758) = &PTR_thunk_FUN_10150b2b4_1065a39c8;
  FUN_1015686ac(&local_c0);
  FUN_10150b1cc(param_1 + 0x770,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x770) = &PTR_thunk_FUN_10150b2b4_1065a39c8;
  pcVar2 = param_1 + 0x788;
  *(undefined8 *)(param_1 + 0x788) = 0;
  FUN_1015643d8(&local_c0);
  lVar10 = *(long *)pcVar2;
  if ((lVar10 != 0) && (iVar8 = *(int *)(lVar10 + 8) + -1, *(int *)(lVar10 + 8) = iVar8, iVar8 == 0)
     ) {
    FUN_10128eea0();
  }
  *(code **)(param_1 + 0x788) = local_c0;
  pcVar3 = param_1 + 0x790;
  *(undefined8 *)(param_1 + 0x790) = 0;
  FUN_1015643d8(&local_c0);
  lVar10 = *(long *)pcVar3;
  if ((lVar10 != 0) && (iVar8 = *(int *)(lVar10 + 8) + -1, *(int *)(lVar10 + 8) = iVar8, iVar8 == 0)
     ) {
    FUN_10128eea0();
  }
  *(code **)(param_1 + 0x790) = local_c0;
  pcVar4 = param_1 + 0x798;
  *(undefined8 *)(param_1 + 0x798) = 0;
  FUN_1015643d8(&local_c0);
  lVar10 = *(long *)pcVar4;
  if ((lVar10 != 0) && (iVar8 = *(int *)(lVar10 + 8) + -1, *(int *)(lVar10 + 8) = iVar8, iVar8 == 0)
     ) {
    FUN_10128eea0();
  }
  *(code **)(param_1 + 0x798) = local_c0;
  *(undefined8 *)(param_1 + 0x7a0) = 0;
  FUN_1015643d8(&local_c0);
  FUN_10150b1cc(param_1 + 0x7a8,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x7a8) = &PTR_thunk_FUN_10150b2b4_10658fdd8;
  FUN_1015643d8(&local_c0);
  FUN_10150b1cc(param_1 + 0x7c0,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x7c0) = &PTR_thunk_FUN_10150b2b4_10658fdd8;
  FUN_1015643d8(&local_c0);
  FUN_10150b1cc(param_1 + 0x7d8,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x7d8) = &PTR_thunk_FUN_10150b2b4_10658fdd8;
  FUN_1015643d8(&local_c0);
  FUN_10150b1cc(param_1 + 0x7f0,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x7f0) = &PTR_thunk_FUN_10150b2b4_10658fdd8;
  FUN_1015643d8(&local_c0);
  FUN_10150b1cc(param_1 + 0x808,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x808) = &PTR_thunk_FUN_10150b2b4_10658fdd8;
  FUN_1015643d8(&local_c0);
  FUN_10150b1cc(param_1 + 0x820,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x820) = &PTR_thunk_FUN_10150b2b4_10658fdd8;
  FUN_1015643d8(&local_c0);
  FUN_10150b1cc(param_1 + 0x838,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x838) = &PTR_thunk_FUN_10150b2b4_10658fdd8;
  FUN_102502be4(&local_c0);
  FUN_10150b1cc(param_1 + 0x850,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x850) = &PTR_thunk_FUN_10150b2b4_106804b70;
  FUN_1015643d8(&local_c0);
  FUN_10150b1cc(param_1 + 0x868,local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)(local_c0 + 8), *(int *)(local_c0 + 8) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined ***)(param_1 + 0x868) = &PTR_thunk_FUN_10150b2b4_10658fdd8;
  *(undefined8 *)(param_1 + 0x880) = 0;
  FUN_101563fa0(&local_c0);
  lVar10 = *(long *)(param_1 + 0x880);
  if ((lVar10 != 0) && (iVar8 = *(int *)(lVar10 + 8) + -1, *(int *)(lVar10 + 8) = iVar8, iVar8 == 0)
     ) {
    FUN_10128eea0();
  }
  *(code **)(param_1 + 0x880) = local_c0;
  *(undefined8 *)(param_1 + 0x888) = 0;
  FUN_1015643d8(&local_c0);
  lVar10 = *(long *)(param_1 + 0x888);
  if ((lVar10 != 0) && (iVar8 = *(int *)(lVar10 + 8) + -1, *(int *)(lVar10 + 8) = iVar8, iVar8 == 0)
     ) {
    FUN_10128eea0();
  }
  *(code **)(param_1 + 0x888) = local_c0;
  *(undefined8 *)(param_1 + 0x890) = 0;
  FUN_1015643d8(&local_c0);
  lVar10 = *(long *)(param_1 + 0x890);
  if ((lVar10 != 0) && (iVar8 = *(int *)(lVar10 + 8) + -1, *(int *)(lVar10 + 8) = iVar8, iVar8 == 0)
     ) {
    FUN_10128eea0();
  }
  *(code **)(param_1 + 0x890) = local_c0;
  *(undefined8 *)(param_1 + 0x898) = 0;
  FUN_10156915c(&local_c0);
  lVar10 = *(long *)(param_1 + 0x898);
  if ((lVar10 != 0) && (iVar8 = *(int *)(lVar10 + 8) + -1, *(int *)(lVar10 + 8) = iVar8, iVar8 == 0)
     ) {
    FUN_10128eea0();
  }
  *(code **)(param_1 + 0x898) = local_c0;
  *(undefined4 *)(param_1 + 0x8a0) = 0;
  *(undefined8 *)(param_1 + 0x8a8) = 0;
  FUN_1015643d8(&local_c0);
  lVar10 = *(long *)(param_1 + 0x8a8);
  if ((lVar10 != 0) && (iVar8 = *(int *)(lVar10 + 8) + -1, *(int *)(lVar10 + 8) = iVar8, iVar8 == 0)
     ) {
    FUN_10128eea0();
  }
  *(code **)(param_1 + 0x8a8) = local_c0;
  *(undefined2 *)(param_1 + 0x8b0) = 0x101;
  *(undefined8 *)(param_1 + 0x8d8) = 0;
  *(undefined8 *)(param_1 + 0x8e8) = 0;
  *(undefined8 *)(param_1 + 0x8e0) = 0;
  *(undefined8 *)(param_1 + 0x8b8) = 0;
  *(undefined8 *)(param_1 + 0x8c8) = 0;
  *(undefined8 *)(param_1 + 0x8c0) = 0;
  *(undefined **)(param_1 + 0x8d0) = &DAT_1066a7220;
  *(undefined **)(param_1 + 0x8f0) = puVar6;
  *(undefined8 *)(param_1 + 0x908) = 0;
  *(undefined8 *)(param_1 + 0x8f8) = 0;
  *(undefined4 *)(param_1 + 0x8ff) = 0;
  FUN_101565f54(&local_c0);
  lVar10 = *(long *)(param_1 + 0x908);
  if ((lVar10 != 0) && (iVar8 = *(int *)(lVar10 + 8) + -1, *(int *)(lVar10 + 8) = iVar8, iVar8 == 0)
     ) {
    FUN_10128eea0();
  }
  *(code **)(param_1 + 0x908) = local_c0;
  *(undefined ***)(param_1 + 0x910) = &PTR_FUN_1066026a8;
  *(undefined8 *)(param_1 + 0x918) = 0;
  *(undefined8 *)(param_1 + 0x928) = 0;
  *(undefined8 *)(param_1 + 0x920) = 0;
  *(undefined ***)(param_1 + 0x930) = &PTR_FUN_1066cb768;
  *(undefined8 *)(param_1 + 0x940) = 0;
  *(undefined8 *)(param_1 + 0x938) = 0;
  *(undefined8 *)(param_1 + 0x950) = 0;
  *(undefined8 *)(param_1 + 0x948) = 0;
  *(undefined8 *)(param_1 + 0x958) = 0;
  *(undefined1 **)(param_1 + 0x968) = &DAT_7fefffffffffffff;
  *(undefined1 **)(param_1 + 0x960) = &DAT_7fefffffffffffff;
  *(undefined8 *)(param_1 + 0x978) = 0;
  *(undefined8 *)(param_1 + 0x970) = 0;
  *(undefined1 **)(param_1 + 0x980) = &DAT_7fefffffffffffff;
  *(undefined8 *)(param_1 + 0x988) = 0;
  FUN_101563fa0(&local_c0);
  lVar10 = *(long *)(param_1 + 0x988);
  if ((lVar10 != 0) && (iVar8 = *(int *)(lVar10 + 8) + -1, *(int *)(lVar10 + 8) = iVar8, iVar8 == 0)
     ) {
    FUN_10128eea0();
  }
  *(code **)(param_1 + 0x988) = local_c0;
  *(undefined8 *)(param_1 + 0x990) = 0;
  *(undefined4 *)(param_1 + 0x998) = 0x80000000;
  *(undefined1 **)(param_1 + 0x9a8) = &DAT_7fefffffffffffff;
  *(undefined1 **)(param_1 + 0x9a0) = &DAT_7fefffffffffffff;
  *(undefined ***)(param_1 + 0x9b0) = &PTR_FUN_1066026a8;
  param_1[0x9f4] = (code)0x0;
  *(undefined8 *)(param_1 + 0x9c0) = 0;
  *(undefined8 *)(param_1 + 0x9b8) = 0;
  *(undefined8 *)(param_1 + 0x9d0) = 0;
  *(undefined8 *)(param_1 + 0x9c8) = 0;
  *(undefined8 *)(param_1 + 0x9e0) = 0;
  *(undefined8 *)(param_1 + 0x9d8) = 0;
  *(undefined8 *)(param_1 + 0x9e9) = 0;
  *(undefined8 *)(param_1 + 0x9e1) = 0;
  *(undefined8 *)(param_1 + 0xa00) = 0;
  *(undefined8 *)(param_1 + 0x9f8) = 0;
  *(undefined8 *)(param_1 + 0xa10) = 0;
  *(undefined8 *)(param_1 + 0xa08) = 0;
  *(undefined8 *)(param_1 + 0xa18) = 0;
  *(undefined4 *)(param_1 + 0xa20) = 0x3f800000;
  *(undefined8 *)(param_1 + 0xa28) = 0;
  param_1[0xa30] = (code)0x0;
  *(undefined ***)(param_1 + 0xa38) = &PTR_FUN_1066026a8;
  *(undefined8 *)(param_1 + 0xa78) = 0;
  *(undefined8 *)(param_1 + 0xa40) = 0;
  *(undefined8 *)(param_1 + 0xa50) = 0;
  *(undefined8 *)(param_1 + 0xa48) = 0;
  param_1[0xa58] = (code)0x0;
  FUN_101486414(param_1);
  local_c0 = (code *)PTR_CallMemberFunc<&ATransport::OnTapTempo>_10652a208;
  pcStack_b8 = param_1;
  FUN_10155e028(*(undefined8 *)(param_1 + 0x290),&local_c0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x290),1);
  plVar18 = *(long **)(param_1 + 0x290);
  FUN_101427680(&local_c0,"Tap tempo");
  (**(code **)(*plVar18 + 0x1c8))(plVar18,&local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)local_c0, *(int *)local_c0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  plVar18 = *(long **)(param_1 + 0x2a8);
  FUN_101427680(&local_c0,"Phase nudge tempo");
  (**(code **)(*plVar18 + 0x1c8))(plVar18,&local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)local_c0, *(int *)local_c0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x2a8),1);
  if (((DAT_10700d010 & 1) == 0) && (iVar8 = ___cxa_guard_acquire(&DAT_10700d010), iVar8 != 0)) {
    pcStack_b8 = _UNK_10588f6d4;
    local_c0 = _DAT_10588f6cc;
    local_a8 = _UNK_10588f6e4;
    local_b0 = _DAT_10588f6dc;
    auVar24 = FUN_1011aeb80(&local_c0);
    _DAT_10700d078 = auVar24._8_8_;
    DAT_10700d070 = auVar24._0_8_;
    ___cxa_guard_release(&DAT_10700d010);
  }
  fVar23 = 10.0;
  if (DAT_10700d078 == '\x01') {
    dVar22 = (double)FUN_1011ac0a0(0,&DAT_10700d070,1);
    fVar23 = (float)dVar22;
  }
  uVar20 = *(undefined8 *)(param_1 + 0x2a8);
  uVar11 = FUN_1012d9850(0x38);
  FUN_101575868(0,0x4479c000,0x3f800000,0x3dcccccd);
  puVar6 = PTR__lambda___1__ARemoteable__TRemoteableUpdate__106551c78;
  local_c0 = (code *)PTR__lambda___1__ARemoteable__TRemoteableUpdate__106551c78;
  pcStack_b8 = (code *)0x0;
  FUN_1015743b0(0,0x4479c000,fVar23,uVar20,uVar11,&local_c0);
  plVar18 = *(long **)(param_1 + 0x2c0);
  FUN_101427680(&local_c0,"Phase nudge up");
  (**(code **)(*plVar18 + 0x1c8))(plVar18,&local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)local_c0, *(int *)local_c0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x2c0),1);
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_101564728(*(undefined8 *)(param_1 + 0x2c0),0,&local_c0);
  plVar18 = *(long **)(param_1 + 0x2d8);
  FUN_101427680(&local_c0,"Phase nudge down");
  (**(code **)(*plVar18 + 0x1c8))(plVar18,&local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)local_c0, *(int *)local_c0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x2d8),1);
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_101564728(*(undefined8 *)(param_1 + 0x2d8),0,&local_c0);
  uVar20 = *(undefined8 *)(param_1 + 0x518);
  uVar11 = FUN_1012d9850(0x38);
  FUN_101575868(0x41a00000,0x4479c000,0x3f800000,0x3dcccccd);
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_1015743b0(0x41a00000,0x4479c000,0x42f00000,uVar20,uVar11,&local_c0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x518),1);
  uVar20 = *(undefined8 *)(param_1 + 0x530);
  uVar11 = FUN_1012d9850(0x38);
  FUN_101575868(0x41a00000,0x4479c000,0x3f800000,0x3dcccccd);
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_1015743b0(0x41a00000,0x4479c000,0x42f00000,uVar20,uVar11,&local_c0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x530),1);
  uVar20 = *(undefined8 *)(param_1 + 0x548);
  uVar11 = FUN_1012d9850(0x38);
  FUN_101575868(0x3dcccccd,0x41200000,0x3d4ccccd,0x3c23d70a);
  local_c0 = FUN_102770944;
  pcStack_b8 = (code *)0x0;
  FUN_1015743b0(0x3dcccccd,0x41200000,0x3f800000,uVar20,uVar11,&local_c0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x548),1);
  uVar20 = *(undefined8 *)(param_1 + 0x560);
  uVar11 = FUN_1012d9850(0x38);
  FUN_101575868(0,0x461c4000,0x3f800000,0x3dcccccd);
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_1015743b0(0,0x461c4000,0x42f00000,uVar20,uVar11,&local_c0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x560),1);
  local_c0 = (code *)PTR_CallMemberFunc<&ATransport::OnCurrentTimeChanged>_10652a230;
  pcStack_b8 = param_1;
  FUN_1015655f4(0,*(undefined8 *)(param_1 + 0x240),&local_c0);
  lVar10 = *(long *)(param_1 + 0x240);
  *(code **)(lVar10 + 0x78) = param_1;
  FUN_10155baa4(lVar10,1);
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_1015655f4(0,*(undefined8 *)(param_1 + 0x270),&local_c0);
  lVar10 = *(long *)(param_1 + 0x270);
  *(code **)(lVar10 + 0x78) = param_1;
  FUN_10155baa4(lVar10,1);
  FUN_10155baa4(*(long *)pcVar21,1);
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_101564728(*(long *)pcVar21,0,&local_c0);
  local_c0 = (code *)PTR_CallMemberFunc<&ATransport::OnIsCountingInChanged>_10652a240;
  pcStack_b8 = param_1;
  FUN_10155c8c0(*(undefined8 *)(param_1 + 0x280),param_1,&local_c0);
  lVar10 = FUN_102676cf0();
  local_c0 = (code *)PTR_CallMemberFunc<&ATransport::OnCountInDurationChanged>_10652a250;
  pcStack_b8 = param_1;
  FUN_10155c8c0(*(undefined8 *)(lVar10 + 0x4b0),param_1,&local_c0);
  FUN_10155baa4(*(long *)(param_1 + 0x988),1);
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_1015655f4(0x4069000000000000,*(undefined8 *)(param_1 + 0x210),&local_c0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x210),1);
  local_c0 = (code *)
             PTR___ZN7ableton7utility6detail13CallbackTypesI10ATransportvJP11ARemoteable17TRemoteableUpdateEE14CallMemberFuncIXadL_ZNS3_7OnStartES5_S6_EEEEvPvS5_S6__10652a2b0
  ;
  pcStack_b8 = param_1;
  FUN_101564728(*(undefined8 *)(param_1 + 0x5a8),0,&local_c0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x5a8),1);
  plVar18 = *(long **)(param_1 + 0x5a8);
  FUN_101427680(&local_c0,"Play");
  (**(code **)(*plVar18 + 0x1c8))(plVar18,&local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)local_c0, *(int *)local_c0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  local_c0 = (code *)
             PTR___ZN7ableton7utility6detail13CallbackTypesI10ATransportvJP11ARemoteable17TRemoteableUpdateEE14CallMemberFuncIXadL_ZNS3_6OnStopES5_S6_EEEEvPvS5_S6__10652a2a8
  ;
  pcStack_b8 = param_1;
  FUN_10155e028(*(undefined8 *)(param_1 + 0x698),&local_c0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x698),1);
  plVar18 = *(long **)(param_1 + 0x698);
  FUN_101427680(&local_c0,"Stop");
  (**(code **)(*plVar18 + 0x1c8))(plVar18,&local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)local_c0, *(int *)local_c0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_101564728(*(undefined8 *)(param_1 + 0x5c0),0,&local_c0);
  local_c0 = (code *)
             PTR___ZN7ableton7utility6detail13CallbackTypesI10ATransportvJP15ARemoteableBoolbEE14CallMemberFuncIXadL_ZNS3_22GlobalRecordControllerES5_bEEEEvPvS5_b_10652a2d0
  ;
  pcStack_b8 = param_1;
  FUN_101564768(*(undefined8 *)(param_1 + 0x5c0),&local_c0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x5c0),1);
  plVar18 = *(long **)(param_1 + 0x5c0);
  FUN_101427680(&local_c0,"Record");
  (**(code **)(*plVar18 + 0x1c8))(plVar18,&local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)local_c0, *(int *)local_c0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_101564728(*(undefined8 *)(param_1 + 0x5d8),0,&local_c0);
  local_c0 = (code *)
             PTR___ZN7ableton7utility6detail13CallbackTypesI10ATransportvJP15ARemoteableBoolbEE14CallMemberFuncIXadL_ZNS3_23SessionRecordControllerES5_bEEEEvPvS5_b_10652a2e0
  ;
  pcStack_b8 = param_1;
  FUN_101564768(*(undefined8 *)(param_1 + 0x5d8),&local_c0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x5d8),1);
  plVar18 = *(long **)(param_1 + 0x5d8);
  FUN_101427680(&local_c0,"Session Record");
  (**(code **)(*plVar18 + 0x1c8))(plVar18,&local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)local_c0, *(int *)local_c0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  local_c0 = (code *)PTR_CallMemberFunc<&ATransport::OnTriggerPrepareSceneForNewRecording>_10652a290
  ;
  pcStack_b8 = param_1;
  FUN_10155c8c0(*(undefined8 *)(param_1 + 0x5f0),param_1,&local_c0);
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_101564728(*(undefined8 *)(param_1 + 0x608),0,&local_c0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x608),1);
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_101564728(*(undefined8 *)(param_1 + 0x748),0,&local_c0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x748),1);
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_101568960(0xbf800000,*(undefined8 *)(param_1 + 0x760),&local_c0);
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_101568960(0xbf800000,*(undefined8 *)(param_1 + 0x778),&local_c0);
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_101564728(*(undefined8 *)(param_1 + 0x620),0,&local_c0);
  local_c0 = (code *)PTR_CallMemberFunc<&ATransport::ArrangementOverdubController>_10652a2e8;
  pcStack_b8 = param_1;
  FUN_101564768(*(undefined8 *)(param_1 + 0x620),&local_c0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x620),1);
  plVar18 = *(long **)(param_1 + 0x620);
  FUN_101427680(&local_c0,"Arrangement Overdub");
  (**(code **)(*plVar18 + 0x1c8))(plVar18,&local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)local_c0, *(int *)local_c0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  uVar20 = *(undefined8 *)(param_1 + 0x638);
  FUN_102676cf0();
  FUN_1026ab304();
  uVar11 = FUN_1015645a0();
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_101564728(uVar20,uVar11,&local_c0);
  local_c0 = (code *)
             PTR___ZN7ableton7utility6detail13CallbackTypesI10ATransportvJP15ARemoteableBoolbEE14CallMemberFuncIXadL_ZNS3_23AutomationArmControllerES5_bEEEEvPvS5_b_10652a2d8
  ;
  pcStack_b8 = param_1;
  FUN_101564768(*(undefined8 *)(param_1 + 0x638),&local_c0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x638),1);
  plVar18 = *(long **)(param_1 + 0x638);
  FUN_101427680(&local_c0,"Automation Arm");
  (**(code **)(*plVar18 + 0x1c8))(plVar18,&local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)local_c0, *(int *)local_c0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  uVar20 = *(undefined8 *)(param_1 + 0x840);
  FUN_102676cf0();
  FUN_1026ab30c();
  uVar11 = FUN_1015645a0();
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_101564728(uVar20,uVar11,&local_c0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x840),1);
  local_c0 = (code *)
             PTR_CallMemberFunc<&ATransport::SessionAutomationRecordingInArmedTracksOnlyController>_10652a2f8
  ;
  pcStack_b8 = param_1;
  FUN_101564768(*(undefined8 *)(param_1 + 0x840),&local_c0);
  uVar11 = *(undefined8 *)(param_1 + 0x650);
  FUN_101427680(&local_88,"Off");
  local_c0 = (code *)0x0;
  pcStack_b8 = (code *)0x0;
  local_b0 = (code *)0x0;
  local_d0 = &local_c0;
  local_c8 = local_c8 & 0xffffffffffffff00;
  local_c0 = operator_new(8);
  pcStack_b8 = local_c0 + 8;
  *(int **)local_c0 = local_88;
  if (local_88 != (int *)0x0) {
    *local_88 = *local_88 + 1;
  }
  local_d0 = (code **)puVar6;
  local_c8 = 0;
  local_b0 = pcStack_b8;
  FUN_101567ad8(uVar11,0,&local_c0,&local_d0);
  pcVar7 = local_c0;
  pcVar21 = pcStack_b8;
  if (local_c0 != (code *)0x0) {
    while (pcVar21 != pcVar7) {
      pcVar21 = pcVar21 + -8;
      piVar14 = *(int **)pcVar21;
      if ((piVar14 != (int *)0x0) && (iVar8 = *piVar14, *piVar14 = iVar8 + -1, iVar8 + -1 == 0)) {
        FUN_101449efc();
      }
    }
    pcStack_b8 = pcVar7;
    operator_delete(local_c0);
  }
  if ((local_88 != (int *)0x0) && (iVar8 = *local_88, *local_88 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  uVar11 = *(undefined8 *)(param_1 + 0x650);
  FUN_101427680(&local_d8,"On");
  FUN_1011cb734(&local_e0);
  FUN_101567120(uVar11,&local_d8,1,&local_e0);
  if ((local_e0 != (int *)0x0) && (iVar8 = *local_e0, *local_e0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  if ((local_d8 != (int *)0x0) && (iVar8 = *local_d8, *local_d8 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  uVar11 = *(undefined8 *)(param_1 + 0x650);
  FUN_101427680(&local_e8,"Transition");
  FUN_1011cb734(&local_f0);
  FUN_101567120(uVar11,&local_e8,2,&local_f0);
  if ((local_f0 != (int *)0x0) && (iVar8 = *local_f0, *local_f0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  if ((local_e8 != (int *)0x0) && (iVar8 = *local_e8, *local_e8 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x650),1);
  local_c0 = (code *)PTR_CallMemberFunc<&ATransport::OnBackToArrangement>_10652a220;
  pcStack_b8 = param_1;
  FUN_101564728(*(undefined8 *)(param_1 + 0x6b0),0,&local_c0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x6b0),1);
  plVar18 = *(long **)(param_1 + 0x6b0);
  FUN_101427680(&local_c0,"Back to arrangement");
  (**(code **)(*plVar18 + 0x1c8))(plVar18,&local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)local_c0, *(int *)local_c0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_101564728(*(undefined8 *)(param_1 + 0x6c8),0,&local_c0);
  local_c0 = (code *)PTR_CallMemberFunc<&ATransport::ReEnableAutomationController>_10652a2f0;
  pcStack_b8 = param_1;
  FUN_101564768(*(undefined8 *)(param_1 + 0x6c8),&local_c0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x6c8),1);
  plVar18 = *(long **)(param_1 + 0x6c8);
  FUN_101427680(&local_c0,"Re-Enable Automation");
  (**(code **)(*plVar18 + 0x1c8))(plVar18,&local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)local_c0, *(int *)local_c0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_101564728(*(long *)pcVar2,0,&local_c0);
  FUN_10155baa4(*(long *)pcVar2,1);
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_101564728(*(undefined8 *)(param_1 + 0x228),0,&local_c0);
  plVar18 = *(long **)(param_1 + 0x228);
  FUN_101427680(&local_c0,"Toggle loop");
  (**(code **)(*plVar18 + 0x1c8))(plVar18,&local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)local_c0, *(int *)local_c0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_1015655f4(0x4020000000000000,*(undefined8 *)(param_1 + 0x1c8),&local_c0);
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_1015655f4(0x4030000000000000,*(undefined8 *)(param_1 + 0x1e0),&local_c0);
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_1015655f4(0x4038000000000000,*(undefined8 *)(param_1 + 0x1f8),&local_c0);
  local_c0 = (code *)PTR_CallMemberFunc<&ATransport::LoopStartController>_10652a300;
  pcStack_b8 = param_1;
  FUN_1015656bc(*(undefined8 *)(param_1 + 0x1c8),&local_c0);
  local_c0 = (code *)PTR_CallMemberFunc<&ATransport::LoopLengthController>_10652a308;
  pcStack_b8 = param_1;
  FUN_1015656bc(*(undefined8 *)(param_1 + 0x1e0),&local_c0);
  local_c0 = (code *)PTR_CallMemberFunc<&ATransport::EmptyLoopEndController>_10652a310;
  pcStack_b8 = param_1;
  FUN_1015656bc(*(undefined8 *)(param_1 + 0x1f8),&local_c0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x228),1);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x1c8),1);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x1e0),1);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x1f8),1);
  local_c0 = (code *)PTR_CallMemberFunc<&ATransport::OnLoopIsSongStart>_10652a210;
  pcStack_b8 = param_1;
  FUN_101564728(*(undefined8 *)(param_1 + 0x60),0,&local_c0);
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_101564728(*(undefined8 *)(param_1 + 0x668),0,&local_c0);
  puVar5 = PTR_CallMemberFunc<&ATransport::PunchInOutController>_10652a2c8;
  local_c0 = (code *)PTR_CallMemberFunc<&ATransport::PunchInOutController>_10652a2c8;
  pcStack_b8 = param_1;
  FUN_101564768(*(undefined8 *)(param_1 + 0x668),&local_c0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x668),1);
  plVar18 = *(long **)(param_1 + 0x668);
  FUN_101427680(&local_c0,"Punch In");
  (**(code **)(*plVar18 + 0x1c8))(plVar18,&local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)local_c0, *(int *)local_c0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_101564728(*(undefined8 *)(param_1 + 0x680),0,&local_c0);
  local_c0 = (code *)puVar5;
  pcStack_b8 = param_1;
  FUN_101564768(*(undefined8 *)(param_1 + 0x680),&local_c0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x680),1);
  plVar18 = *(long **)(param_1 + 0x680);
  FUN_101427680(&local_c0,"Punch Out");
  (**(code **)(*plVar18 + 0x1c8))(plVar18,&local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)local_c0, *(int *)local_c0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  local_c0 = (code *)PTR_CallMemberFunc<&ATransport::OnMidiMode>_10652a200;
  pcStack_b8 = param_1;
  FUN_101564728(*(undefined8 *)(param_1 + 0x128),0,&local_c0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x128),1);
  local_c0 = (code *)PTR_CallMemberFunc<&ATransport::OnKeyMode>_10652a2b8;
  pcStack_b8 = param_1;
  FUN_101564728(*(undefined8 *)(param_1 + 0x140),0,&local_c0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x140),1);
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_101564728(*(undefined8 *)(param_1 + 0x578),0,&local_c0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x578),1);
  local_c0 = (code *)PTR_CallMemberFunc<&ATransport::OnExternSyncOnChanged>_10652a238;
  pcStack_b8 = param_1;
  FUN_10155c8c0(*(undefined8 *)(param_1 + 0x578),param_1,&local_c0);
  local_c0 = (code *)PTR_CallMemberFunc<&ATransport::OnResyncExternalHardware>_10652a258;
  pcStack_b8 = param_1;
  FUN_10155e028(*(undefined8 *)(param_1 + 0x590),&local_c0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x590),1);
  plVar18 = *(long **)(param_1 + 0x590);
  FUN_101427680(&local_c0,"Resync External Hardware");
  (**(code **)(*plVar18 + 0x1c8))(plVar18,&local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)local_c0, *(int *)local_c0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_101564728(*(undefined8 *)(param_1 + 0xb0),0,&local_c0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0xb0),1);
  local_c0 = (code *)PTR_CallMemberFunc<&ATransport::OnIsTempoFollowerInControlChanged>_10652a278;
  pcStack_b8 = param_1;
  FUN_10155c8c0(*(undefined8 *)(param_1 + 0xb0),param_1,&local_c0);
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_101564728(*(undefined8 *)(param_1 + 200),0,&local_c0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 200),1);
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_101564728(*(undefined8 *)(param_1 + 0x98),0,&local_c0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x98),1);
  local_c0 = (code *)PTR_CallMemberFunc<&ATransport::OnIsAbletonLinkEnabledChanged>_10652a260;
  pcStack_b8 = param_1;
  FUN_10155c8c0(*(undefined8 *)(param_1 + 0x98),param_1,&local_c0);
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_10156934c(*(undefined8 *)(param_1 + 0xe0),0,&local_c0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0xe0),1);
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_101564728(*(long *)pcVar13,0,&local_c0);
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_101568960(0,*(undefined8 *)(param_1 + 0x100),&local_c0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x100),1);
  *(undefined **)(param_1 + 0x110) =
       PTR_CallMemberFunc<&ATransport::OnAbletonLinkAudioChannelsChanged>_10652a1e8;
  *(code **)(param_1 + 0x118) = param_1;
  FUN_1003c2c04(param_1 + 0xa38);
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_101564728(*(undefined8 *)(param_1 + 0x1b0),0,&local_c0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x1b0),1);
  plVar18 = *(long **)(param_1 + 0x1b0);
  FUN_101427680(&local_c0,"Automation Draw Mode");
  (**(code **)(*plVar18 + 0x1c8))(plVar18,&local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)local_c0, *(int *)local_c0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  puVar9 = (undefined8 *)FUN_1012d97bc(0x438);
  uVar20 = _UNK_10588f5a8;
  uVar11 = _DAT_10588f5a0;
  puVar9[1] = _UNK_10588f5a8;
  *puVar9 = uVar11;
  _bzero(puVar9 + 2,0x428);
  *(undefined8 **)(param_1 + 0x8b8) = puVar9 + 2;
  puVar9 = (undefined8 *)FUN_1012d97bc(0x438);
  puVar9[1] = uVar20;
  *puVar9 = uVar11;
  _bzero(puVar9 + 2,0x428);
  lVar10 = 0;
  *(undefined8 **)(param_1 + 0x8c0) = puVar9 + 2;
  do {
    FUN_1015686ac(&local_d0);
    local_c0 = (code *)puVar6;
    pcStack_b8 = (code *)0x0;
    FUN_101568960(0,local_d0,&local_c0);
    FUN_10155baa4(local_d0,1);
    FUN_1015686ac(&local_88);
    local_c0 = (code *)puVar6;
    pcStack_b8 = (code *)0x0;
    FUN_101568960(0,local_88,&local_c0);
    FUN_10155baa4(local_88,1);
    lVar19 = *(long *)(param_1 + 0x8b8);
    if (local_d0 != (code **)0x0) {
      *(int *)(local_d0 + 1) = *(int *)(local_d0 + 1) + 1;
    }
    lVar12 = *(long *)(lVar19 + lVar10);
    if ((lVar12 == 0) ||
       (iVar8 = *(int *)(lVar12 + 8) + -1, *(int *)(lVar12 + 8) = iVar8, iVar8 != 0)) {
      *(code ***)(lVar19 + lVar10) = local_d0;
      lVar19 = *(long *)(param_1 + 0x8c0);
    }
    else {
      FUN_10128eea0();
      *(code ***)(lVar19 + lVar10) = local_d0;
      lVar19 = *(long *)(param_1 + 0x8c0);
    }
    if (local_88 != (int *)0x0) {
      local_88[2] = local_88[2] + 1;
    }
    lVar12 = *(long *)(lVar19 + lVar10);
    if ((lVar12 == 0) ||
       (iVar8 = *(int *)(lVar12 + 8) + -1, *(int *)(lVar12 + 8) = iVar8, iVar8 != 0)) {
      *(int **)(lVar19 + lVar10) = local_88;
    }
    else {
      FUN_10128eea0();
      *(int **)(lVar19 + lVar10) = local_88;
    }
    if ((local_88 != (int *)0x0) && (iVar8 = local_88[2], local_88[2] = iVar8 + -1, iVar8 + -1 == 0)
       ) {
      FUN_10128eea0();
    }
    if ((local_d0 != (code **)0x0) &&
       (iVar8 = *(int *)(local_d0 + 1), *(int *)(local_d0 + 1) = iVar8 + -1, iVar8 + -1 == 0)) {
      FUN_10128eea0();
    }
    lVar10 = lVar10 + 8;
  } while (lVar10 != 0x428);
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_101564728(*(long *)pcVar3,0,&local_c0);
  FUN_10155baa4(*(long *)pcVar3,1);
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_101564728(*(long *)pcVar4,0,&local_c0);
  FUN_10155baa4(*(long *)pcVar4,1);
  pcVar13 = (code *)FUN_1012d9850(0x38);
  FUN_1027733b8(pcVar13,20000);
  if (pcVar13 != (code *)0x0) {
    *(int *)(pcVar13 + 8) = *(int *)(pcVar13 + 8) + 1;
  }
  lVar10 = *(long *)(param_1 + 0x7a0);
  if ((lVar10 != 0) && (iVar8 = *(int *)(lVar10 + 8) + -1, *(int *)(lVar10 + 8) = iVar8, iVar8 == 0)
     ) {
    local_c0 = pcVar13;
    FUN_10128eea0();
    pcVar13 = local_c0;
  }
  *(code **)(param_1 + 0x7a0) = pcVar13;
  puVar5 = PTR_CallMemberFunc<&TRemoteableBoolPositiveEdgeDetector::OnObservedChanged>_106534818;
  lVar10 = *(long *)pcVar3;
  if (*(long *)(pcVar13 + 0x30) != 0) {
    local_c0 = (code *)
               PTR_CallMemberFunc<&TRemoteableBoolPositiveEdgeDetector::OnObservedChanged>_106534818
    ;
    pcStack_b8 = pcVar13;
    FUN_10155cbd8(*(long *)(pcVar13 + 0x30),pcVar13,&local_c0);
  }
  *(long *)(pcVar13 + 0x30) = lVar10;
  if (lVar10 != 0) {
    local_c0 = (code *)puVar5;
    pcStack_b8 = pcVar13;
    FUN_10155c8c0(lVar10,pcVar13,&local_c0);
  }
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_101564728(*(undefined8 *)(param_1 + 0x7b0),0,&local_c0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x7b0),1);
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_101564728(*(undefined8 *)(param_1 + 0x7c8),0,&local_c0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x7c8),1);
  local_c0 = (code *)PTR_CallMemberFunc<&ATransport::OnUpdateMidiInFlash>_10652a228;
  pcStack_b8 = param_1;
  FUN_10155c8c0(*(undefined8 *)(param_1 + 0x7b0),param_1,&local_c0);
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_101564728(*(undefined8 *)(param_1 + 0x7e0),0,&local_c0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x7e0),1);
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_101564728(*(undefined8 *)(param_1 + 0x7f8),0,&local_c0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x7f8),1);
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_101564728(*(undefined8 *)(param_1 + 0x810),0,&local_c0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x810),1);
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_101564728(*(undefined8 *)(param_1 + 0x828),0,&local_c0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x828),1);
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_101564728(*(long *)(param_1 + 0x888),0,&local_c0);
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_101564728(*(long *)(param_1 + 0x890),0,&local_c0);
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_10156934c(*(long *)(param_1 + 0x898),0,&local_c0);
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_101564728(*(long *)(param_1 + 0x8a8),0,&local_c0);
  FUN_1024ad478(&local_c0);
  lVar10 = *(long *)(param_1 + 0xa28);
  if ((lVar10 != 0) && (iVar8 = *(int *)(lVar10 + 8) + -1, *(int *)(lVar10 + 8) = iVar8, iVar8 == 0)
     ) {
    FUN_10128eea0();
  }
  *(code **)(param_1 + 0xa28) = local_c0;
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_101564728(*(undefined8 *)(param_1 + 0x6e8),0,&local_c0);
  plVar18 = *(long **)(param_1 + 0x6e8);
  FUN_101427680(&local_c0,"Metronome");
  (**(code **)(*plVar18 + 0x1c8))(plVar18,&local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)local_c0, *(int *)local_c0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x6e8),1);
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_101564728(*(long *)pcVar1,0,&local_c0);
  plVar18 = *(long **)pcVar1;
  FUN_101427680(&local_c0,"Metronome audible");
  (**(code **)(*plVar18 + 0x1c8))(plVar18,&local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)local_c0, *(int *)local_c0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  FUN_10155baa4(*(long *)pcVar1,1);
  local_c0 = (code *)0x0;
  pcStack_b8 = (code *)0x0;
  local_b0 = (code *)0x0;
  local_d0 = (code **)puVar6;
  local_c8 = 0;
  FUN_101567ad8(*(undefined8 *)(param_1 + 0x700),0,&local_c0,&local_d0);
  pcVar21 = local_c0;
  pcVar13 = pcStack_b8;
  if (local_c0 != (code *)0x0) {
    while (pcVar13 != pcVar21) {
      pcVar13 = pcVar13 + -8;
      piVar14 = *(int **)pcVar13;
      if ((piVar14 != (int *)0x0) && (iVar8 = *piVar14, *piVar14 = iVar8 + -1, iVar8 + -1 == 0)) {
        FUN_101449efc();
      }
    }
    pcStack_b8 = pcVar21;
    operator_delete(local_c0);
  }
  plVar18 = *(long **)(param_1 + 0x700);
  FUN_101427680(&local_c0,"Metronome presets");
  (**(code **)(*plVar18 + 0x1c8))(plVar18,&local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)local_c0, *(int *)local_c0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x700),1);
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_101568960(0,*(undefined8 *)(param_1 + 0x718),&local_c0);
  plVar18 = *(long **)(param_1 + 0x718);
  FUN_101427680(&local_c0,"Metronome tick duration");
  (**(code **)(*plVar18 + 0x1c8))(plVar18,&local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)local_c0, *(int *)local_c0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  puVar5 = PTR_CallMemberFunc<&ATransport::OnUpdateMetronomeState>_10652a248;
  local_c0 = (code *)PTR_CallMemberFunc<&ATransport::OnUpdateMetronomeState>_10652a248;
  pcStack_b8 = param_1;
  FUN_10155c8c0(*(undefined8 *)(param_1 + 0x6e8),param_1,&local_c0);
  lVar10 = FUN_102676cf0();
  local_c0 = (code *)puVar5;
  pcStack_b8 = param_1;
  FUN_10155c8c0(*(undefined8 *)(lVar10 + 0x3c0),param_1,&local_c0);
  local_c0 = (code *)puVar5;
  pcStack_b8 = param_1;
  FUN_10155c8c0(*(undefined8 *)(param_1 + 0x5c0),param_1,&local_c0);
  local_c0 = (code *)puVar5;
  pcStack_b8 = param_1;
  FUN_10155c8c0(*(undefined8 *)(param_1 + 0x5d8),param_1,&local_c0);
  uVar11 = *(undefined8 *)(param_1 + 0x2f0);
  FUN_101427680(&local_d0,"Transport");
  FUN_101427680(&local_88,"Phase nudge up");
  local_f8 = 0;
  uStack_f4 = 0x2711;
  local_fc = 0;
  plVar18 = *(long **)(param_1 + 0x9d8);
  if (plVar18 < *(long **)(param_1 + 0x9e0)) {
    *plVar18 = 0;
    FUN_10248c0b4(&local_c0,&local_d0,&local_88,&uStack_f4,&local_f8,&local_fc);
    lVar10 = *plVar18;
    if ((lVar10 != 0) &&
       (iVar8 = *(int *)(lVar10 + 8) + -1, *(int *)(lVar10 + 8) = iVar8, iVar8 == 0)) {
      FUN_10128eea0();
    }
    plVar15 = plVar18 + 1;
    *plVar18 = (long)local_c0;
    *(long **)(param_1 + 0x9d8) = plVar15;
  }
  else {
    plVar15 = (long *)FUN_10248becc(param_1 + 0x9d0,&local_d0,&local_88,&uStack_f4,&local_f8,
                                    &local_fc);
  }
  *(long **)(param_1 + 0x9d8) = plVar15;
  lVar10 = 0;
  if (plVar15[-1] != 0) {
    lVar10 = plVar15[-1] + 0x18;
  }
  FUN_10260aa38(uVar11,lVar10,0);
  if ((local_88 != (int *)0x0) && (iVar8 = *local_88, *local_88 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  if ((local_d0 != (code **)0x0) &&
     (iVar8 = *(int *)local_d0, *(int *)local_d0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  uVar11 = *(undefined8 *)(param_1 + 0x308);
  FUN_101427680(&local_d0,"Transport");
  FUN_101427680(&local_88,"Phase nudge down");
  local_f8 = 0;
  uStack_f4 = 0x2711;
  local_fc = 1;
  plVar18 = *(long **)(param_1 + 0x9d8);
  if (plVar18 < *(long **)(param_1 + 0x9e0)) {
    *plVar18 = 0;
    FUN_10248c0b4(&local_c0,&local_d0,&local_88,&uStack_f4,&local_f8,&local_fc);
    lVar10 = *plVar18;
    if ((lVar10 != 0) &&
       (iVar8 = *(int *)(lVar10 + 8) + -1, *(int *)(lVar10 + 8) = iVar8, iVar8 == 0)) {
      FUN_10128eea0();
    }
    plVar15 = plVar18 + 1;
    *plVar18 = (long)local_c0;
    *(long **)(param_1 + 0x9d8) = plVar15;
  }
  else {
    plVar15 = (long *)FUN_10248becc(param_1 + 0x9d0,&local_d0,&local_88,&uStack_f4,&local_f8,
                                    &local_fc);
  }
  *(long **)(param_1 + 0x9d8) = plVar15;
  lVar10 = 0;
  if (plVar15[-1] != 0) {
    lVar10 = plVar15[-1] + 0x18;
  }
  FUN_10260aa38(uVar11,lVar10,0);
  if ((local_88 != (int *)0x0) && (iVar8 = *local_88, *local_88 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  if ((local_d0 != (code **)0x0) &&
     (iVar8 = *(int *)local_d0, *(int *)local_d0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  uVar11 = *(undefined8 *)(param_1 + 800);
  FUN_101427680(&local_d0,"Transport");
  FUN_101427680(&local_88,"Tap Tempo");
  local_f8 = 0;
  uStack_f4 = 0x2711;
  local_fc = 2;
  plVar18 = *(long **)(param_1 + 0x9d8);
  if (plVar18 < *(long **)(param_1 + 0x9e0)) {
    *plVar18 = 0;
    FUN_10248c0b4(&local_c0,&local_d0,&local_88,&uStack_f4,&local_f8,&local_fc);
    lVar10 = *plVar18;
    if ((lVar10 != 0) &&
       (iVar8 = *(int *)(lVar10 + 8) + -1, *(int *)(lVar10 + 8) = iVar8, iVar8 == 0)) {
      FUN_10128eea0();
    }
    plVar15 = plVar18 + 1;
    *plVar18 = (long)local_c0;
    *(long **)(param_1 + 0x9d8) = plVar15;
  }
  else {
    plVar15 = (long *)FUN_10248becc(param_1 + 0x9d0,&local_d0,&local_88,&uStack_f4,&local_f8,
                                    &local_fc);
  }
  *(long **)(param_1 + 0x9d8) = plVar15;
  lVar10 = 0;
  if (plVar15[-1] != 0) {
    lVar10 = plVar15[-1] + 0x18;
  }
  FUN_10260aa38(uVar11,lVar10,0);
  if ((local_88 != (int *)0x0) && (iVar8 = *local_88, *local_88 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  if ((local_d0 != (code **)0x0) &&
     (iVar8 = *(int *)local_d0, *(int *)local_d0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  uVar11 = *(undefined8 *)(param_1 + 0x338);
  FUN_101427680(&local_d0,"Transport");
  FUN_101427680(&local_88,"Start");
  local_f8 = 0;
  uStack_f4 = 0x2711;
  local_100 = 8;
  local_fc = 3;
  plVar18 = *(long **)(param_1 + 0x9d8);
  if (plVar18 < *(long **)(param_1 + 0x9e0)) {
    *plVar18 = 0;
    FUN_10248c3b4(&local_c0,&local_d0,&local_88,&uStack_f4,&local_f8,&local_fc,&local_100);
    lVar10 = *plVar18;
    if ((lVar10 != 0) &&
       (iVar8 = *(int *)(lVar10 + 8) + -1, *(int *)(lVar10 + 8) = iVar8, iVar8 == 0)) {
      FUN_10128eea0();
    }
    plVar15 = plVar18 + 1;
    *plVar18 = (long)local_c0;
    *(long **)(param_1 + 0x9d8) = plVar15;
  }
  else {
    plVar15 = (long *)FUN_10248c1bc(param_1 + 0x9d0,&local_d0,&local_88,&uStack_f4,&local_f8,
                                    &local_fc,&local_100);
  }
  *(long **)(param_1 + 0x9d8) = plVar15;
  lVar10 = 0;
  if (plVar15[-1] != 0) {
    lVar10 = plVar15[-1] + 0x18;
  }
  FUN_10260aa38(uVar11,lVar10,0);
  if ((local_88 != (int *)0x0) && (iVar8 = *local_88, *local_88 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  if ((local_d0 != (code **)0x0) &&
     (iVar8 = *(int *)local_d0, *(int *)local_d0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  uVar11 = *(undefined8 *)(param_1 + 0x350);
  FUN_101427680(&local_d0,"Transport");
  FUN_101427680(&local_88,"Stop");
  local_f8 = 0;
  uStack_f4 = 0x2711;
  local_100 = 8;
  local_fc = 4;
  plVar18 = *(long **)(param_1 + 0x9d8);
  if (plVar18 < *(long **)(param_1 + 0x9e0)) {
    *plVar18 = 0;
    FUN_10248c3b4(&local_c0,&local_d0,&local_88,&uStack_f4,&local_f8,&local_fc,&local_100);
    lVar10 = *plVar18;
    if ((lVar10 != 0) &&
       (iVar8 = *(int *)(lVar10 + 8) + -1, *(int *)(lVar10 + 8) = iVar8, iVar8 == 0)) {
      FUN_10128eea0();
    }
    plVar15 = plVar18 + 1;
    *plVar18 = (long)local_c0;
    *(long **)(param_1 + 0x9d8) = plVar15;
  }
  else {
    plVar15 = (long *)FUN_10248c1bc(param_1 + 0x9d0,&local_d0,&local_88,&uStack_f4,&local_f8,
                                    &local_fc,&local_100);
  }
  *(long **)(param_1 + 0x9d8) = plVar15;
  lVar10 = 0;
  if (plVar15[-1] != 0) {
    lVar10 = plVar15[-1] + 0x18;
  }
  FUN_10260aa38(uVar11,lVar10,0);
  if ((local_88 != (int *)0x0) && (iVar8 = *local_88, *local_88 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  if ((local_d0 != (code **)0x0) &&
     (iVar8 = *(int *)local_d0, *(int *)local_d0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  uVar11 = *(undefined8 *)(param_1 + 0x368);
  FUN_101427680(&local_d0,"Transport");
  FUN_101427680(&local_88,"Global Record");
  local_f8 = 0;
  uStack_f4 = 0x2711;
  local_fc = 5;
  plVar18 = *(long **)(param_1 + 0x9d8);
  if (plVar18 < *(long **)(param_1 + 0x9e0)) {
    *plVar18 = 0;
    FUN_10248c0b4(&local_c0,&local_d0,&local_88,&uStack_f4,&local_f8,&local_fc);
    lVar10 = *plVar18;
    if ((lVar10 != 0) &&
       (iVar8 = *(int *)(lVar10 + 8) + -1, *(int *)(lVar10 + 8) = iVar8, iVar8 == 0)) {
      FUN_10128eea0();
    }
    plVar15 = plVar18 + 1;
    *plVar18 = (long)local_c0;
    *(long **)(param_1 + 0x9d8) = plVar15;
  }
  else {
    plVar15 = (long *)FUN_10248becc(param_1 + 0x9d0,&local_d0,&local_88,&uStack_f4,&local_f8,
                                    &local_fc);
  }
  *(long **)(param_1 + 0x9d8) = plVar15;
  lVar10 = 0;
  if (plVar15[-1] != 0) {
    lVar10 = plVar15[-1] + 0x18;
  }
  FUN_10260aa38(uVar11,lVar10,0);
  if ((local_88 != (int *)0x0) && (iVar8 = *local_88, *local_88 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  if ((local_d0 != (code **)0x0) &&
     (iVar8 = *(int *)local_d0, *(int *)local_d0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  uVar11 = *(undefined8 *)(param_1 + 0x380);
  FUN_101427680(&local_d0,"Transport");
  FUN_101427680(&local_88,"Session Record");
  local_f8 = 0;
  uStack_f4 = 0x2711;
  local_fc = 6;
  plVar18 = *(long **)(param_1 + 0x9d8);
  if (plVar18 < *(long **)(param_1 + 0x9e0)) {
    *plVar18 = 0;
    FUN_10248c0b4(&local_c0,&local_d0,&local_88,&uStack_f4,&local_f8,&local_fc);
    lVar10 = *plVar18;
    if ((lVar10 != 0) &&
       (iVar8 = *(int *)(lVar10 + 8) + -1, *(int *)(lVar10 + 8) = iVar8, iVar8 == 0)) {
      FUN_10128eea0();
    }
    plVar15 = plVar18 + 1;
    *plVar18 = (long)local_c0;
    *(long **)(param_1 + 0x9d8) = plVar15;
  }
  else {
    plVar15 = (long *)FUN_10248becc(param_1 + 0x9d0,&local_d0,&local_88,&uStack_f4,&local_f8,
                                    &local_fc);
  }
  *(long **)(param_1 + 0x9d8) = plVar15;
  lVar10 = 0;
  if (plVar15[-1] != 0) {
    lVar10 = plVar15[-1] + 0x18;
  }
  FUN_10260aa38(uVar11,lVar10,0);
  if ((local_88 != (int *)0x0) && (iVar8 = *local_88, *local_88 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  if ((local_d0 != (code **)0x0) &&
     (iVar8 = *(int *)local_d0, *(int *)local_d0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  uVar11 = *(undefined8 *)(param_1 + 0x398);
  FUN_101427680(&local_d0,"Transport");
  FUN_101427680(&local_88,"Prepare Scene For New Recording");
  local_f8 = 0;
  uStack_f4 = 0x2711;
  local_fc = 7;
  plVar18 = *(long **)(param_1 + 0x9d8);
  if (plVar18 < *(long **)(param_1 + 0x9e0)) {
    *plVar18 = 0;
    FUN_10248c0b4(&local_c0,&local_d0,&local_88,&uStack_f4,&local_f8,&local_fc);
    lVar10 = *plVar18;
    if ((lVar10 != 0) &&
       (iVar8 = *(int *)(lVar10 + 8) + -1, *(int *)(lVar10 + 8) = iVar8, iVar8 == 0)) {
      FUN_10128eea0();
    }
    plVar15 = plVar18 + 1;
    *plVar18 = (long)local_c0;
    *(long **)(param_1 + 0x9d8) = plVar15;
  }
  else {
    plVar15 = (long *)FUN_10248becc(param_1 + 0x9d0,&local_d0,&local_88,&uStack_f4,&local_f8,
                                    &local_fc);
  }
  *(long **)(param_1 + 0x9d8) = plVar15;
  lVar10 = 0;
  if (plVar15[-1] != 0) {
    lVar10 = plVar15[-1] + 0x18;
  }
  FUN_10260aa38(uVar11,lVar10,0);
  if ((local_88 != (int *)0x0) && (iVar8 = *local_88, *local_88 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  if ((local_d0 != (code **)0x0) &&
     (iVar8 = *(int *)local_d0, *(int *)local_d0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  uVar11 = *(undefined8 *)(param_1 + 0x3b0);
  FUN_101427680(&local_d0,"Transport");
  FUN_101427680(&local_88,"Arrangement Overdub");
  local_f8 = 0;
  uStack_f4 = 0x2711;
  local_fc = 8;
  plVar18 = *(long **)(param_1 + 0x9d8);
  if (plVar18 < *(long **)(param_1 + 0x9e0)) {
    *plVar18 = 0;
    FUN_10248c0b4(&local_c0,&local_d0,&local_88,&uStack_f4,&local_f8,&local_fc);
    lVar10 = *plVar18;
    if ((lVar10 != 0) &&
       (iVar8 = *(int *)(lVar10 + 8) + -1, *(int *)(lVar10 + 8) = iVar8, iVar8 == 0)) {
      FUN_10128eea0();
    }
    plVar15 = plVar18 + 1;
    *plVar18 = (long)local_c0;
    *(long **)(param_1 + 0x9d8) = plVar15;
  }
  else {
    plVar15 = (long *)FUN_10248becc(param_1 + 0x9d0,&local_d0,&local_88,&uStack_f4,&local_f8,
                                    &local_fc);
  }
  *(long **)(param_1 + 0x9d8) = plVar15;
  lVar10 = 0;
  if (plVar15[-1] != 0) {
    lVar10 = plVar15[-1] + 0x18;
  }
  FUN_10260aa38(uVar11,lVar10,0);
  if ((local_88 != (int *)0x0) && (iVar8 = *local_88, *local_88 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  if ((local_d0 != (code **)0x0) &&
     (iVar8 = *(int *)local_d0, *(int *)local_d0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  uVar11 = *(undefined8 *)(param_1 + 0x3c8);
  FUN_101427680(&local_d0,"Transport");
  FUN_101427680(&local_88,"Automation Arm");
  local_f8 = 0;
  uStack_f4 = 0x2711;
  local_fc = 9;
  plVar18 = *(long **)(param_1 + 0x9d8);
  if (plVar18 < *(long **)(param_1 + 0x9e0)) {
    *plVar18 = 0;
    FUN_10248c0b4(&local_c0,&local_d0,&local_88,&uStack_f4,&local_f8,&local_fc);
    lVar10 = *plVar18;
    if ((lVar10 != 0) &&
       (iVar8 = *(int *)(lVar10 + 8) + -1, *(int *)(lVar10 + 8) = iVar8, iVar8 == 0)) {
      FUN_10128eea0();
    }
    plVar15 = plVar18 + 1;
    *plVar18 = (long)local_c0;
    *(long **)(param_1 + 0x9d8) = plVar15;
  }
  else {
    plVar15 = (long *)FUN_10248becc(param_1 + 0x9d0,&local_d0,&local_88,&uStack_f4,&local_f8,
                                    &local_fc);
  }
  *(long **)(param_1 + 0x9d8) = plVar15;
  lVar10 = 0;
  if (plVar15[-1] != 0) {
    lVar10 = plVar15[-1] + 0x18;
  }
  FUN_10260aa38(uVar11,lVar10,0);
  if ((local_88 != (int *)0x0) && (iVar8 = *local_88, *local_88 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  if ((local_d0 != (code **)0x0) &&
     (iVar8 = *(int *)local_d0, *(int *)local_d0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  uVar11 = *(undefined8 *)(param_1 + 0x3e0);
  FUN_101427680(&local_d0,"Transport");
  FUN_101427680(&local_88,"Back to Arrangement");
  local_f8 = 0;
  uStack_f4 = 0x2711;
  local_fc = 10;
  plVar18 = *(long **)(param_1 + 0x9d8);
  if (plVar18 < *(long **)(param_1 + 0x9e0)) {
    *plVar18 = 0;
    FUN_10248c0b4(&local_c0,&local_d0,&local_88,&uStack_f4,&local_f8,&local_fc);
    lVar10 = *plVar18;
    if ((lVar10 != 0) &&
       (iVar8 = *(int *)(lVar10 + 8) + -1, *(int *)(lVar10 + 8) = iVar8, iVar8 == 0)) {
      FUN_10128eea0();
    }
    plVar15 = plVar18 + 1;
    *plVar18 = (long)local_c0;
    *(long **)(param_1 + 0x9d8) = plVar15;
  }
  else {
    plVar15 = (long *)FUN_10248becc(param_1 + 0x9d0,&local_d0,&local_88,&uStack_f4,&local_f8,
                                    &local_fc);
  }
  *(long **)(param_1 + 0x9d8) = plVar15;
  lVar10 = 0;
  if (plVar15[-1] != 0) {
    lVar10 = plVar15[-1] + 0x18;
  }
  FUN_10260aa38(uVar11,lVar10,0);
  if ((local_88 != (int *)0x0) && (iVar8 = *local_88, *local_88 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  if ((local_d0 != (code **)0x0) &&
     (iVar8 = *(int *)local_d0, *(int *)local_d0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  uVar11 = *(undefined8 *)(param_1 + 0x3f8);
  FUN_101427680(&local_d0,"Transport");
  FUN_101427680(&local_88,"Re-Enable Automation");
  local_f8 = 0;
  uStack_f4 = 0x2711;
  local_fc = 0xb;
  plVar18 = *(long **)(param_1 + 0x9d8);
  if (plVar18 < *(long **)(param_1 + 0x9e0)) {
    *plVar18 = 0;
    FUN_10248c0b4(&local_c0,&local_d0,&local_88,&uStack_f4,&local_f8,&local_fc);
    lVar10 = *plVar18;
    if ((lVar10 != 0) &&
       (iVar8 = *(int *)(lVar10 + 8) + -1, *(int *)(lVar10 + 8) = iVar8, iVar8 == 0)) {
      FUN_10128eea0();
    }
    plVar15 = plVar18 + 1;
    *plVar18 = (long)local_c0;
    *(long **)(param_1 + 0x9d8) = plVar15;
  }
  else {
    plVar15 = (long *)FUN_10248becc(param_1 + 0x9d0,&local_d0,&local_88,&uStack_f4,&local_f8,
                                    &local_fc);
  }
  *(long **)(param_1 + 0x9d8) = plVar15;
  lVar10 = 0;
  if (plVar15[-1] != 0) {
    lVar10 = plVar15[-1] + 0x18;
  }
  FUN_10260aa38(uVar11,lVar10,0);
  if ((local_88 != (int *)0x0) && (iVar8 = *local_88, *local_88 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  if ((local_d0 != (code **)0x0) &&
     (iVar8 = *(int *)local_d0, *(int *)local_d0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  uVar11 = *(undefined8 *)(param_1 + 0x410);
  FUN_101427680(&local_d0,"Transport");
  FUN_101427680(&local_88,"Loop On/Off");
  local_f8 = 0;
  uStack_f4 = 0x2711;
  local_fc = 0xc;
  plVar18 = *(long **)(param_1 + 0x9d8);
  if (plVar18 < *(long **)(param_1 + 0x9e0)) {
    *plVar18 = 0;
    FUN_10248c0b4(&local_c0,&local_d0,&local_88,&uStack_f4,&local_f8,&local_fc);
    lVar10 = *plVar18;
    if ((lVar10 != 0) &&
       (iVar8 = *(int *)(lVar10 + 8) + -1, *(int *)(lVar10 + 8) = iVar8, iVar8 == 0)) {
      FUN_10128eea0();
    }
    plVar15 = plVar18 + 1;
    *plVar18 = (long)local_c0;
    *(long **)(param_1 + 0x9d8) = plVar15;
  }
  else {
    plVar15 = (long *)FUN_10248becc(param_1 + 0x9d0,&local_d0,&local_88,&uStack_f4,&local_f8,
                                    &local_fc);
  }
  *(long **)(param_1 + 0x9d8) = plVar15;
  lVar10 = 0;
  if (plVar15[-1] != 0) {
    lVar10 = plVar15[-1] + 0x18;
  }
  FUN_10260aa38(uVar11,lVar10,0);
  if ((local_88 != (int *)0x0) && (iVar8 = *local_88, *local_88 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  if ((local_d0 != (code **)0x0) &&
     (iVar8 = *(int *)local_d0, *(int *)local_d0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  uVar11 = *(undefined8 *)(param_1 + 0x428);
  FUN_101427680(&local_d0,"Transport");
  FUN_101427680(&local_88,"Punch In");
  local_f8 = 0;
  uStack_f4 = 0x2711;
  local_fc = 0xd;
  plVar18 = *(long **)(param_1 + 0x9d8);
  if (plVar18 < *(long **)(param_1 + 0x9e0)) {
    *plVar18 = 0;
    FUN_10248c0b4(&local_c0,&local_d0,&local_88,&uStack_f4,&local_f8,&local_fc);
    lVar10 = *plVar18;
    if ((lVar10 != 0) &&
       (iVar8 = *(int *)(lVar10 + 8) + -1, *(int *)(lVar10 + 8) = iVar8, iVar8 == 0)) {
      FUN_10128eea0();
    }
    plVar15 = plVar18 + 1;
    *plVar18 = (long)local_c0;
    *(long **)(param_1 + 0x9d8) = plVar15;
  }
  else {
    plVar15 = (long *)FUN_10248becc(param_1 + 0x9d0,&local_d0,&local_88,&uStack_f4,&local_f8,
                                    &local_fc);
  }
  *(long **)(param_1 + 0x9d8) = plVar15;
  lVar10 = 0;
  if (plVar15[-1] != 0) {
    lVar10 = plVar15[-1] + 0x18;
  }
  FUN_10260aa38(uVar11,lVar10,0);
  if ((local_88 != (int *)0x0) && (iVar8 = *local_88, *local_88 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  if ((local_d0 != (code **)0x0) &&
     (iVar8 = *(int *)local_d0, *(int *)local_d0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  uVar11 = *(undefined8 *)(param_1 + 0x440);
  FUN_101427680(&local_d0,"Transport");
  FUN_101427680(&local_88,"Punch Out");
  local_f8 = 0;
  uStack_f4 = 0x2711;
  local_fc = 0xe;
  plVar18 = *(long **)(param_1 + 0x9d8);
  if (plVar18 < *(long **)(param_1 + 0x9e0)) {
    *plVar18 = 0;
    FUN_10248c0b4(&local_c0,&local_d0,&local_88,&uStack_f4,&local_f8,&local_fc);
    lVar10 = *plVar18;
    if ((lVar10 != 0) &&
       (iVar8 = *(int *)(lVar10 + 8) + -1, *(int *)(lVar10 + 8) = iVar8, iVar8 == 0)) {
      FUN_10128eea0();
    }
    plVar15 = plVar18 + 1;
    *plVar18 = (long)local_c0;
    *(long **)(param_1 + 0x9d8) = plVar15;
  }
  else {
    plVar15 = (long *)FUN_10248becc(param_1 + 0x9d0,&local_d0,&local_88,&uStack_f4,&local_f8,
                                    &local_fc);
  }
  *(long **)(param_1 + 0x9d8) = plVar15;
  lVar10 = 0;
  if (plVar15[-1] != 0) {
    lVar10 = plVar15[-1] + 0x18;
  }
  FUN_10260aa38(uVar11,lVar10,0);
  if ((local_88 != (int *)0x0) && (iVar8 = *local_88, *local_88 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  if ((local_d0 != (code **)0x0) &&
     (iVar8 = *(int *)local_d0, *(int *)local_d0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  uVar11 = *(undefined8 *)(param_1 + 0x458);
  FUN_101427680(&local_d0,"Transport");
  FUN_101427680(&local_88,"Draw Mode");
  local_f8 = 0;
  uStack_f4 = 0x2711;
  local_fc = 0xf;
  plVar18 = *(long **)(param_1 + 0x9d8);
  if (plVar18 < *(long **)(param_1 + 0x9e0)) {
    *plVar18 = 0;
    FUN_10248c0b4(&local_c0,&local_d0,&local_88,&uStack_f4,&local_f8,&local_fc);
    lVar10 = *plVar18;
    if ((lVar10 != 0) &&
       (iVar8 = *(int *)(lVar10 + 8) + -1, *(int *)(lVar10 + 8) = iVar8, iVar8 == 0)) {
      FUN_10128eea0();
    }
    plVar15 = plVar18 + 1;
    *plVar18 = (long)local_c0;
    *(long **)(param_1 + 0x9d8) = plVar15;
  }
  else {
    plVar15 = (long *)FUN_10248becc(param_1 + 0x9d0,&local_d0,&local_88,&uStack_f4,&local_f8,
                                    &local_fc);
  }
  *(long **)(param_1 + 0x9d8) = plVar15;
  lVar10 = 0;
  if (plVar15[-1] != 0) {
    lVar10 = plVar15[-1] + 0x18;
  }
  FUN_10260aa38(uVar11,lVar10,0);
  if ((local_88 != (int *)0x0) && (iVar8 = *local_88, *local_88 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  if ((local_d0 != (code **)0x0) &&
     (iVar8 = *(int *)local_d0, *(int *)local_d0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  uVar11 = *(undefined8 *)(param_1 + 0x470);
  FUN_101427680(&local_d0,"Transport");
  FUN_101427680(&local_88,"Follow");
  local_f8 = 0;
  uStack_f4 = 0x2711;
  local_fc = 0x10;
  plVar18 = *(long **)(param_1 + 0x9d8);
  if (plVar18 < *(long **)(param_1 + 0x9e0)) {
    *plVar18 = 0;
    FUN_10248c0b4(&local_c0,&local_d0,&local_88,&uStack_f4,&local_f8,&local_fc);
    lVar10 = *plVar18;
    if ((lVar10 != 0) &&
       (iVar8 = *(int *)(lVar10 + 8) + -1, *(int *)(lVar10 + 8) = iVar8, iVar8 == 0)) {
      FUN_10128eea0();
    }
    plVar15 = plVar18 + 1;
    *plVar18 = (long)local_c0;
    *(long **)(param_1 + 0x9d8) = plVar15;
  }
  else {
    plVar15 = (long *)FUN_10248becc(param_1 + 0x9d0,&local_d0,&local_88,&uStack_f4,&local_f8,
                                    &local_fc);
  }
  *(long **)(param_1 + 0x9d8) = plVar15;
  lVar10 = 0;
  if (plVar15[-1] != 0) {
    lVar10 = plVar15[-1] + 0x18;
  }
  FUN_10260aa38(uVar11,lVar10,0);
  if ((local_88 != (int *)0x0) && (iVar8 = *local_88, *local_88 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  if ((local_d0 != (code **)0x0) &&
     (iVar8 = *(int *)local_d0, *(int *)local_d0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  uVar11 = *(undefined8 *)(param_1 + 0x488);
  FUN_101427680(&local_d0,"Transport");
  FUN_101427680(&local_88,"Metronome On/Off");
  local_f8 = 0;
  uStack_f4 = 0x2711;
  local_fc = 0x11;
  plVar18 = *(long **)(param_1 + 0x9d8);
  if (plVar18 < *(long **)(param_1 + 0x9e0)) {
    *plVar18 = 0;
    FUN_10248c0b4(&local_c0,&local_d0,&local_88,&uStack_f4,&local_f8,&local_fc);
    lVar10 = *plVar18;
    if ((lVar10 != 0) &&
       (iVar8 = *(int *)(lVar10 + 8) + -1, *(int *)(lVar10 + 8) = iVar8, iVar8 == 0)) {
      FUN_10128eea0();
    }
    plVar15 = plVar18 + 1;
    *plVar18 = (long)local_c0;
    *(long **)(param_1 + 0x9d8) = plVar15;
  }
  else {
    plVar15 = (long *)FUN_10248becc(param_1 + 0x9d0,&local_d0,&local_88,&uStack_f4,&local_f8,
                                    &local_fc);
  }
  *(long **)(param_1 + 0x9d8) = plVar15;
  lVar10 = 0;
  if (plVar15[-1] != 0) {
    lVar10 = plVar15[-1] + 0x18;
  }
  FUN_10260aa38(uVar11,lVar10,0);
  if ((local_88 != (int *)0x0) && (iVar8 = *local_88, *local_88 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  if ((local_d0 != (code **)0x0) &&
     (iVar8 = *(int *)local_d0, *(int *)local_d0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  uVar11 = *(undefined8 *)(param_1 + 0x4b8);
  FUN_101427680(&local_d0,"Transport");
  FUN_101427680(&local_88,"Trigger Capture");
  local_f8 = 0;
  uStack_f4 = 0x2711;
  local_fc = 0x12;
  plVar18 = *(long **)(param_1 + 0x9d8);
  if (plVar18 < *(long **)(param_1 + 0x9e0)) {
    *plVar18 = 0;
    FUN_10248c0b4(&local_c0,&local_d0,&local_88,&uStack_f4,&local_f8,&local_fc);
    lVar10 = *plVar18;
    if ((lVar10 != 0) &&
       (iVar8 = *(int *)(lVar10 + 8) + -1, *(int *)(lVar10 + 8) = iVar8, iVar8 == 0)) {
      FUN_10128eea0();
    }
    plVar15 = plVar18 + 1;
    *plVar18 = (long)local_c0;
    *(long **)(param_1 + 0x9d8) = plVar15;
  }
  else {
    plVar15 = (long *)FUN_10248becc(param_1 + 0x9d0,&local_d0,&local_88,&uStack_f4,&local_f8,
                                    &local_fc);
  }
  *(long **)(param_1 + 0x9d8) = plVar15;
  lVar10 = 0;
  if (plVar15[-1] != 0) {
    lVar10 = plVar15[-1] + 0x18;
  }
  FUN_10260aa38(uVar11,lVar10,0);
  if ((local_88 != (int *)0x0) && (iVar8 = *local_88, *local_88 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  if ((local_d0 != (code **)0x0) &&
     (iVar8 = *(int *)local_d0, *(int *)local_d0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  uVar11 = *(undefined8 *)(param_1 + 0x4d0);
  FUN_101427680(&local_d0,"Transport");
  FUN_101427680(&local_88,"Enable/Disable Follow Actions");
  local_f8 = 0;
  uStack_f4 = 0x2711;
  local_fc = 0x13;
  plVar18 = *(long **)(param_1 + 0x9d8);
  if (plVar18 < *(long **)(param_1 + 0x9e0)) {
    *plVar18 = 0;
    FUN_10248c0b4(&local_c0,&local_d0,&local_88,&uStack_f4,&local_f8,&local_fc);
    lVar10 = *plVar18;
    if ((lVar10 != 0) &&
       (iVar8 = *(int *)(lVar10 + 8) + -1, *(int *)(lVar10 + 8) = iVar8, iVar8 == 0)) {
      FUN_10128eea0();
    }
    plVar15 = plVar18 + 1;
    *plVar18 = (long)local_c0;
    *(long **)(param_1 + 0x9d8) = plVar15;
  }
  else {
    plVar15 = (long *)FUN_10248becc(param_1 + 0x9d0,&local_d0,&local_88,&uStack_f4,&local_f8,
                                    &local_fc);
  }
  *(long **)(param_1 + 0x9d8) = plVar15;
  lVar10 = 0;
  if (plVar15[-1] != 0) {
    lVar10 = plVar15[-1] + 0x18;
  }
  FUN_10260aa38(uVar11,lVar10,0);
  if ((local_88 != (int *)0x0) && (iVar8 = *local_88, *local_88 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  if ((local_d0 != (code **)0x0) &&
     (iVar8 = *(int *)local_d0, *(int *)local_d0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  uVar11 = *(undefined8 *)(param_1 + 0x4e8);
  FUN_101427680(&local_d0,"Transport");
  FUN_101427680(&local_88,"Enable/Disable Tempo Follower");
  local_f8 = 0;
  uStack_f4 = 0x2711;
  local_fc = 0x14;
  plVar18 = *(long **)(param_1 + 0x9d8);
  if (plVar18 < *(long **)(param_1 + 0x9e0)) {
    *plVar18 = 0;
    FUN_10248c0b4(&local_c0,&local_d0,&local_88,&uStack_f4,&local_f8,&local_fc);
    lVar10 = *plVar18;
    if ((lVar10 != 0) &&
       (iVar8 = *(int *)(lVar10 + 8) + -1, *(int *)(lVar10 + 8) = iVar8, iVar8 == 0)) {
      FUN_10128eea0();
    }
    plVar15 = plVar18 + 1;
    *plVar18 = (long)local_c0;
    *(long **)(param_1 + 0x9d8) = plVar15;
  }
  else {
    plVar15 = (long *)FUN_10248becc(param_1 + 0x9d0,&local_d0,&local_88,&uStack_f4,&local_f8,
                                    &local_fc);
  }
  *(long **)(param_1 + 0x9d8) = plVar15;
  lVar10 = 0;
  if (plVar15[-1] != 0) {
    lVar10 = plVar15[-1] + 0x18;
  }
  FUN_10260aa38(uVar11,lVar10,0);
  if ((local_88 != (int *)0x0) && (iVar8 = *local_88, *local_88 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  if ((local_d0 != (code **)0x0) &&
     (iVar8 = *(int *)local_d0, *(int *)local_d0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  uVar11 = *(undefined8 *)(param_1 + 0x500);
  FUN_101427680(&local_d0,"Transport");
  FUN_101427680(&local_88,"Resync External Hardware");
  local_f8 = 0;
  uStack_f4 = 0x2711;
  local_fc = 0x15;
  plVar18 = *(long **)(param_1 + 0x9d8);
  if (plVar18 < *(long **)(param_1 + 0x9e0)) {
    *plVar18 = 0;
    FUN_10248c0b4(&local_c0,&local_d0,&local_88,&uStack_f4,&local_f8,&local_fc);
    lVar10 = *plVar18;
    if ((lVar10 != 0) &&
       (iVar8 = *(int *)(lVar10 + 8) + -1, *(int *)(lVar10 + 8) = iVar8, iVar8 == 0)) {
      FUN_10128eea0();
    }
    plVar15 = plVar18 + 1;
    *plVar18 = (long)local_c0;
    *(long **)(param_1 + 0x9d8) = plVar15;
  }
  else {
    plVar15 = (long *)FUN_10248becc(param_1 + 0x9d0,&local_d0,&local_88,&uStack_f4,&local_f8,
                                    &local_fc);
  }
  *(long **)(param_1 + 0x9d8) = plVar15;
  lVar10 = 0;
  if (plVar15[-1] != 0) {
    lVar10 = plVar15[-1] + 0x18;
  }
  FUN_10260aa38(uVar11,lVar10,0);
  if ((local_88 != (int *)0x0) && (iVar8 = *local_88, *local_88 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  if ((local_d0 != (code **)0x0) &&
     (iVar8 = *(int *)local_d0, *(int *)local_d0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  uVar11 = *(undefined8 *)(param_1 + 0x4a0);
  FUN_101427680(&local_d0,"Clip");
  FUN_101427680(&local_88,"MIDI Prelisten");
  local_f8 = 0;
  uStack_f4 = 0x2713;
  local_fc = 1000;
  plVar18 = *(long **)(param_1 + 0x9d8);
  if (plVar18 < *(long **)(param_1 + 0x9e0)) {
    *plVar18 = 0;
    FUN_102671e38(&local_c0,&local_d0,&local_88,&uStack_f4,&local_f8,&local_fc);
    lVar10 = *plVar18;
    if ((lVar10 != 0) &&
       (iVar8 = *(int *)(lVar10 + 8) + -1, *(int *)(lVar10 + 8) = iVar8, iVar8 == 0)) {
      FUN_10128eea0();
    }
    plVar15 = plVar18 + 1;
    *plVar18 = (long)local_c0;
    *(long **)(param_1 + 0x9d8) = plVar15;
  }
  else {
    plVar15 = (long *)FUN_102770fdc(param_1 + 0x9d0,&local_d0,&local_88,&uStack_f4,&local_f8,
                                    &local_fc);
  }
  *(long **)(param_1 + 0x9d8) = plVar15;
  lVar10 = 0;
  if (plVar15[-1] != 0) {
    lVar10 = plVar15[-1] + 0x18;
  }
  FUN_10260aa38(uVar11,lVar10,0);
  if ((local_88 != (int *)0x0) && (iVar8 = *local_88, *local_88 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  if ((local_d0 != (code **)0x0) &&
     (iVar8 = *(int *)local_d0, *(int *)local_d0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  if (((DAT_10700d018 & 1) == 0) && (iVar8 = ___cxa_guard_acquire(&DAT_10700d018), iVar8 != 0)) {
    FUN_101427680(&local_c0,"Invalid");
    pcStack_b8 = DAT_10700d008;
    if (DAT_10700d008 != (code *)0x0) {
      *(int *)DAT_10700d008 = *(int *)DAT_10700d008 + 1;
    }
    FUN_101427680("ReWireDevice");
    FUN_101427680("MidiTimeCode");
    FUN_101427680("MidiClock");
    FUN_101427680(&pcStack_98,"MidiReady");
    FUN_101427680(auStack_90,"SongTempoFollowsClipTempo");
    FUN_1002c29cc(&DAT_10700d0e8,&local_c0,7);
    FUN_100234444(auStack_90);
    FUN_100234444(&pcStack_98);
    FUN_100234444(&local_a0);
    FUN_100234444(&local_a8);
    FUN_100234444(&local_b0);
    FUN_100234444(&pcStack_b8);
    FUN_100234444(&local_c0);
    ___cxa_atexit(FUN_1002343c8,&DAT_10700d0e8,0x100000000);
    ___cxa_guard_release(&DAT_10700d018);
  }
  local_c0 = (code *)PTR_CallMemberFunc<&ATransport::OnTempoModeChanged>_10652a218;
  pcStack_b8 = param_1;
  FUN_101567bfc(*(undefined8 *)(param_1 + 0x908),0,&DAT_10700d0e8,0,&local_c0);
  lVar10 = FUN_10226efb4();
  if (lVar10 != 0) {
    plVar18 = (long *)FUN_10226efb4();
    (**(code **)(*plVar18 + 0x1a0))(plVar18,FUN_102766dfc,param_1,0);
  }
  lVar10 = FUN_1022a9658();
  if (lVar10 != 0) {
    FUN_1023a6d30();
    uVar11 = FUN_1023b0250();
    local_c0 = (code *)
               PTR_CallMemberFunc<&ATransport::OnIsAbletonLinkToggleVisibleChanged>_10652a288;
    pcStack_b8 = param_1;
    FUN_10155c8c0(uVar11,param_1,&local_c0);
    FUN_1023a6d30();
    uVar11 = FUN_1023a6d68();
    local_c0 = (code *)
               PTR_CallMemberFunc<&ATransport::OnIsAbletonLinkStartStopSyncEnabledChanged>_10652a298
    ;
    pcStack_b8 = param_1;
    FUN_10155c8c0(uVar11,param_1,&local_c0);
    FUN_1023a6d30();
    uVar11 = FUN_1023a6d70();
    local_c0 = (code *)PTR_CallMemberFunc<&ATransport::OnIsAbletonLinkAudioEnabledChanged>_10652a280
    ;
    pcStack_b8 = param_1;
    FUN_10155c8c0(uVar11,param_1,&local_c0);
    FUN_1023a6d30();
    uVar11 = FUN_1023b0258();
    local_c0 = (code *)PTR_CallMemberFunc<&ATransport::OnAbletonLinkAudioPeerNameChanged>_10652a270;
    pcStack_b8 = param_1;
    FUN_10155c8c0(uVar11,param_1,&local_c0);
    FUN_1023a6d30();
    uVar11 = FUN_1023b0260();
    local_c0 = (code *)PTR_CallMemberFunc<&ATransport::OnAbletonLinkAudioLatencyChanged>_10652a268;
    pcStack_b8 = param_1;
    FUN_10155c8c0(uVar11,param_1,&local_c0);
    FUN_1023a6d30();
    uVar11 = FUN_1023b0268();
    local_c0 = (code *)
               PTR_CallMemberFunc<&ATransport::OnAbletonLinkAudioSyncToIncomingAudioChanged>_10652a2a0
    ;
    pcStack_b8 = param_1;
    FUN_10155c8c0(uVar11,param_1,&local_c0);
    lVar10 = FUN_1022bbab0(lVar10);
    FUN_101458fc8(&local_c0,param_1);
    puVar5 = PTR_CallMemberFunc<&ATransport::OnMidiDevicesChanged>_10652a318;
    local_c0 = (code *)&DAT_106592510;
    local_a0 = PTR_CallMemberFunc<&ATransport::OnMidiDevicesChanged>_10652a318;
    puVar9 = *(undefined8 **)(lVar10 + 0x10);
    pcStack_98 = param_1;
    if (puVar9 < *(undefined8 **)(lVar10 + 0x18)) {
      puVar16 = puVar9 + 2;
      *puVar16 = 0;
      puVar9[1] = 0;
      puVar9[3] = local_a8;
      if (local_a8 != 0) {
        lVar19 = *(long *)(local_a8 + 0x10);
        puVar17 = puVar9;
        if (lVar19 != 0) {
          puVar16 = (undefined8 *)(lVar19 + 8);
          puVar17 = (undefined8 *)*puVar16;
          puVar9[2] = lVar19;
          puVar17[2] = puVar9;
        }
        puVar9[1] = puVar17;
        *puVar16 = puVar9;
        *(undefined8 **)(local_a8 + 0x10) = puVar9;
      }
      *puVar9 = &DAT_106592510;
      puVar9[5] = param_1;
      puVar9[4] = puVar5;
      puVar9 = puVar9 + 6;
    }
    else {
      puVar9 = (undefined8 *)FUN_1022c4760(lVar10 + 8,&local_c0);
    }
    *(undefined8 **)(lVar10 + 0x10) = puVar9;
    FUN_101459068(&local_c0);
  }
  uVar11 = *(undefined8 *)(param_1 + 0x858);
  lVar10 = FUN_102676cf0();
  FUN_102502fdc(uVar11,*(undefined8 *)(lVar10 + 0x2b8),*(long *)pcVar2);
  local_c0 = (code *)puVar6;
  pcStack_b8 = (code *)0x0;
  FUN_101564728(*(undefined8 *)(param_1 + 0x870),1,&local_c0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x870),1);
  plVar18 = *(long **)(param_1 + 0x870);
  FUN_101427680(&local_c0,"Enable Follow Actions");
  (**(code **)(*plVar18 + 0x1c8))(plVar18,&local_c0);
  if ((local_c0 != (code *)0x0) &&
     (iVar8 = *(int *)local_c0, *(int *)local_c0 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  if (*(long *)PTR____stack_chk_guard_1064f8818 == local_80) {
    return param_1;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

