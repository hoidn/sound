
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1031b4554(long param_1,int param_2,int param_3,undefined8 param_4,int *param_5)

{
  char *pcVar1;
  char *pcVar2;
  char *pcVar3;
  char *pcVar4;
  undefined8 uVar5;
  undefined8 uVar6;
  bool bVar7;
  int iVar8;
  int *piVar9;
  undefined8 uVar10;
  long *plVar11;
  int *local_90;
  int *local_88;
  undefined8 uStack_80;
  undefined1 auStack_78 [8];
  undefined1 auStack_70 [8];
  long local_68;
  
  local_68 = *(long *)PTR____stack_chk_guard_1064f8818;
  local_88 = (int *)PTR__lambda___1__ARemoteable__TRemoteableUpdate__106551c78;
  uStack_80 = 0;
  FUN_101564728(*(undefined8 *)(param_1 + 0x58),1,&local_88);
  bVar7 = param_2 != 0;
  pcVar3 = "AMP1 Env Exponential";
  if (bVar7) {
    pcVar3 = "AMP2 Env Exponential";
  }
  pcVar1 = "F1 Env Exponential";
  if (bVar7) {
    pcVar1 = "F2 Env Exponential";
  }
  pcVar2 = "AEG1 Exp";
  if (bVar7) {
    pcVar2 = "AEG2 Exp";
  }
  pcVar4 = "FEG1 Exp";
  if (bVar7) {
    pcVar4 = "FEG2 Exp";
  }
  if (param_3 != 0) {
    pcVar4 = pcVar2;
    pcVar1 = pcVar3;
  }
  FUN_10319285c(*(undefined8 *)(param_1 + 0x70),pcVar1,1,pcVar4);
  if (((DAT_107028098 & 1) == 0) && (iVar8 = ___cxa_guard_acquire(&DAT_107028098), iVar8 != 0)) {
    FUN_101427680(&local_88,"Off");
    FUN_101427680(&uStack_80,"AD-R");
    FUN_101427680(auStack_78,"ADR-R");
    FUN_101427680(auStack_70,"ADS-AR");
    FUN_1002c29cc(&DAT_1070282f8,&local_88,4);
    FUN_100234444(auStack_70);
    FUN_100234444(auStack_78);
    FUN_100234444(&uStack_80);
    FUN_100234444(&local_88);
    ___cxa_atexit(FUN_1002343c8,&DAT_1070282f8,0x100000000);
    ___cxa_guard_release(&DAT_107028098);
  }
  uVar10 = *(undefined8 *)(param_1 + 0x88);
  pcVar3 = "AMP1 Env Loop";
  if (param_2 != 0) {
    pcVar3 = "AMP2 Env Loop";
  }
  pcVar1 = "F1 Env Loop";
  if (param_2 != 0) {
    pcVar1 = "F2 Env Loop";
  }
  if (param_3 != 0) {
    pcVar1 = pcVar3;
  }
  FUN_101427680(&local_90,pcVar1);
  FUN_1026ef060(uVar10,0,&DAT_1070282f8,&local_90,1);
  if ((local_90 != (int *)0x0) && (iVar8 = *local_90, *local_90 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  plVar11 = *(long **)(param_1 + 0x88);
  pcVar3 = "AEG1 Loop";
  if (param_2 != 0) {
    pcVar3 = "AEG2 Loop";
  }
  pcVar1 = "FEG1 Loop";
  if (param_2 != 0) {
    pcVar1 = "FEG2 Loop";
  }
  if (param_3 != 0) {
    pcVar1 = pcVar3;
  }
  FUN_101427680(&local_88,pcVar1);
  (**(code **)(*plVar11 + 0x298))(plVar11,&local_88);
  if ((local_88 != (int *)0x0) && (iVar8 = *local_88, *local_88 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  bVar7 = param_2 != 0;
  pcVar3 = "AMP1 Env Free Run";
  if (bVar7) {
    pcVar3 = "AMP2 Env Free Run";
  }
  pcVar1 = "AEG1 Free";
  pcVar2 = "F1 Env Free Run";
  if (bVar7) {
    pcVar1 = "AEG2 Free";
    pcVar2 = "F2 Env Free Run";
  }
  pcVar4 = "FEG1 Free";
  if (bVar7) {
    pcVar4 = "FEG2 Free";
  }
  if (param_3 != 0) {
    pcVar4 = pcVar1;
    pcVar2 = pcVar3;
  }
  FUN_10319285c(*(undefined8 *)(param_1 + 0xa0),pcVar2,0,pcVar4);
  pcVar3 = "AMP1 Env Legato";
  if (bVar7) {
    pcVar3 = "AMP2 Env Legato";
  }
  pcVar1 = "F1 Env Legato";
  if (bVar7) {
    pcVar1 = "F2 Env Legato";
  }
  pcVar2 = "AEG1 Legato";
  if (bVar7) {
    pcVar2 = "AEG2 Legato";
  }
  pcVar4 = "FEG1 Legato";
  if (bVar7) {
    pcVar4 = "FEG2 Legato";
  }
  if (param_3 != 0) {
    pcVar4 = pcVar2;
    pcVar1 = pcVar3;
  }
  FUN_10319285c(*(undefined8 *)(param_1 + 0xb8),pcVar1,0,pcVar4);
  iVar8 = *param_5;
  uVar10 = *(undefined8 *)(param_1 + 0xd0);
  *param_5 = iVar8 + 6;
  piVar9 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  bVar7 = param_2 != 0;
  pcVar3 = "F1 Env Attack < Vel";
  if (bVar7) {
    pcVar3 = "F2 Env Attack < Vel";
  }
  pcVar1 = "AMP1 Env Attack < Vel";
  if (bVar7) {
    pcVar1 = "AMP2 Env Attack < Vel";
  }
  pcVar2 = "AEG1 A < Vel";
  if (bVar7) {
    pcVar2 = "AEG2 A < Vel";
  }
  pcVar4 = "FEG1 A < Vel";
  if (bVar7) {
    pcVar4 = "FEG2 A < Vel";
  }
  if (param_3 != 0) {
    pcVar3 = pcVar1;
  }
  *(undefined ***)piVar9 = &PTR_thunk_FUN_10128edf8_1068ddff8;
  piVar9[6] = iVar8 + 5;
  uVar6 = _UNK_10561dfd8;
  uVar5 = _DAT_10561dfd0;
  *(undefined8 *)(piVar9 + 10) = _UNK_10561dfd8;
  *(undefined8 *)(piVar9 + 8) = uVar5;
  piVar9[2] = piVar9[2] + 1;
  if (param_3 != 0) {
    pcVar4 = pcVar2;
  }
  local_88 = piVar9;
  FUN_103192720(0,param_4,uVar10,pcVar3,piVar9,pcVar4,0);
  iVar8 = piVar9[2];
  piVar9[2] = iVar8 + -1;
  if (iVar8 + -1 == 0) {
    FUN_10128eea0(piVar9);
  }
  uVar10 = *(undefined8 *)(param_1 + 0xe8);
  iVar8 = *param_5;
  *param_5 = iVar8 + 1;
  piVar9 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  bVar7 = param_2 != 0;
  pcVar3 = "F1 Env Attack";
  if (bVar7) {
    pcVar3 = "F2 Env Attack";
  }
  pcVar1 = "AMP1 Env Attack";
  if (bVar7) {
    pcVar1 = "AMP2 Env Attack";
  }
  *(undefined ***)piVar9 = &PTR_thunk_FUN_10128edf8_1068ddff8;
  pcVar2 = "AEG1 Attack";
  if (bVar7) {
    pcVar2 = "AEG2 Attack";
  }
  piVar9[6] = iVar8;
  pcVar4 = "FEG1 Attack";
  if (bVar7) {
    pcVar4 = "FEG2 Attack";
  }
  if (param_3 != 0) {
    pcVar3 = pcVar1;
  }
  *(undefined8 *)(piVar9 + 10) = uVar6;
  *(undefined8 *)(piVar9 + 8) = uVar5;
  piVar9[2] = piVar9[2] + 1;
  if (param_3 != 0) {
    pcVar4 = pcVar2;
  }
  local_88 = piVar9;
  FUN_103192720(0,param_4,uVar10,pcVar3,piVar9,pcVar4,0);
  iVar8 = piVar9[2];
  piVar9[2] = iVar8 + -1;
  if (iVar8 + -1 == 0) {
    FUN_10128eea0(piVar9);
  }
  uVar10 = *(undefined8 *)(param_1 + 0x100);
  iVar8 = *param_5;
  *param_5 = iVar8 + 1;
  piVar9 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  bVar7 = param_2 != 0;
  pcVar3 = "F1 Env Decay";
  if (bVar7) {
    pcVar3 = "F2 Env Decay";
  }
  pcVar1 = "AMP1 Env Decay";
  if (bVar7) {
    pcVar1 = "AMP2 Env Decay";
  }
  *(undefined ***)piVar9 = &PTR_thunk_FUN_10128edf8_1068ddff8;
  pcVar2 = "AEG1 Decay";
  if (bVar7) {
    pcVar2 = "AEG2 Decay";
  }
  piVar9[6] = iVar8;
  pcVar4 = "FEG1 Decay";
  if (bVar7) {
    pcVar4 = "FEG2 Decay";
  }
  if (param_3 != 0) {
    pcVar3 = pcVar1;
  }
  *(undefined8 *)(piVar9 + 10) = uVar6;
  *(undefined8 *)(piVar9 + 8) = uVar5;
  piVar9[2] = piVar9[2] + 1;
  if (param_3 != 0) {
    pcVar4 = pcVar2;
  }
  local_88 = piVar9;
  FUN_103192720(0x3f19999a,param_4,uVar10,pcVar3,piVar9,pcVar4,0);
  iVar8 = piVar9[2];
  piVar9[2] = iVar8 + -1;
  if (iVar8 + -1 == 0) {
    FUN_10128eea0(piVar9);
  }
  uVar10 = *(undefined8 *)(param_1 + 0x118);
  iVar8 = *param_5;
  *param_5 = iVar8 + 1;
  piVar9 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  bVar7 = param_2 != 0;
  pcVar3 = "F1 Env < Vel";
  if (bVar7) {
    pcVar3 = "F2 Env < Vel";
  }
  pcVar1 = "AMP1 Env < Vel";
  if (bVar7) {
    pcVar1 = "AMP2 Env < Vel";
  }
  *(undefined ***)piVar9 = &PTR_thunk_FUN_10128edf8_1068ddff8;
  pcVar2 = "AEG1 < Vel";
  if (bVar7) {
    pcVar2 = "AEG2 < Vel";
  }
  piVar9[6] = iVar8;
  pcVar4 = "FEG1 < Vel";
  if (bVar7) {
    pcVar4 = "FEG2 < Vel";
  }
  if (param_3 != 0) {
    pcVar3 = pcVar1;
  }
  *(undefined8 *)(piVar9 + 10) = uVar6;
  *(undefined8 *)(piVar9 + 8) = uVar5;
  piVar9[2] = piVar9[2] + 1;
  if (param_3 != 0) {
    pcVar4 = pcVar2;
  }
  local_88 = piVar9;
  FUN_103192720(0,param_4,uVar10,pcVar3,piVar9,pcVar4,0);
  iVar8 = piVar9[2];
  piVar9[2] = iVar8 + -1;
  if (iVar8 + -1 == 0) {
    FUN_10128eea0(piVar9);
  }
  uVar10 = *(undefined8 *)(param_1 + 0x130);
  iVar8 = *param_5;
  *param_5 = iVar8 + 1;
  piVar9 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  bVar7 = param_2 != 0;
  pcVar3 = "F1 Env Sustain";
  if (bVar7) {
    pcVar3 = "F2 Env Sustain";
  }
  pcVar1 = "AMP1 Env Sustain";
  if (bVar7) {
    pcVar1 = "AMP2 Env Sustain";
  }
  *(undefined ***)piVar9 = &PTR_thunk_FUN_10128edf8_1068ddff8;
  pcVar2 = "AEG1 Sustain";
  if (bVar7) {
    pcVar2 = "AEG2 Sustain";
  }
  piVar9[6] = iVar8;
  pcVar4 = "FEG1 Sustain";
  if (bVar7) {
    pcVar4 = "FEG2 Sustain";
  }
  if (param_3 != 0) {
    pcVar3 = pcVar1;
  }
  *(undefined8 *)(piVar9 + 10) = uVar6;
  *(undefined8 *)(piVar9 + 8) = uVar5;
  piVar9[2] = piVar9[2] + 1;
  if (param_3 != 0) {
    pcVar4 = pcVar2;
  }
  local_88 = piVar9;
  FUN_103192720(0,param_4,uVar10,pcVar3,piVar9,pcVar4,0);
  iVar8 = piVar9[2];
  piVar9[2] = iVar8 + -1;
  if (iVar8 + -1 == 0) {
    FUN_10128eea0(piVar9);
  }
  uVar10 = *(undefined8 *)(param_1 + 0x148);
  iVar8 = *param_5;
  *param_5 = iVar8 + 1;
  piVar9 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  bVar7 = param_2 != 0;
  pcVar3 = "F1 Env Sustain Time";
  if (bVar7) {
    pcVar3 = "F2 Env Sustain Time";
  }
  pcVar1 = "AMP1 Env Sustain Time";
  if (bVar7) {
    pcVar1 = "AMP2 Env Sustain Time";
  }
  *(undefined ***)piVar9 = &PTR_thunk_FUN_10128edf8_1068ddff8;
  pcVar2 = "AEG1 S Time";
  if (bVar7) {
    pcVar2 = "AEG2 S Time";
  }
  piVar9[6] = iVar8;
  pcVar4 = "FEG1 S Time";
  if (bVar7) {
    pcVar4 = "FEG2 S Time";
  }
  if (param_3 != 0) {
    pcVar3 = pcVar1;
  }
  *(undefined8 *)(piVar9 + 10) = uVar6;
  *(undefined8 *)(piVar9 + 8) = uVar5;
  piVar9[2] = piVar9[2] + 1;
  if (param_3 != 0) {
    pcVar4 = pcVar2;
  }
  local_88 = piVar9;
  FUN_103192720(0x3f800000,param_4,uVar10,pcVar3,piVar9,pcVar4,0);
  iVar8 = piVar9[2];
  piVar9[2] = iVar8 + -1;
  if (iVar8 + -1 == 0) {
    FUN_10128eea0(piVar9);
  }
  uVar10 = *(undefined8 *)(param_1 + 0x160);
  iVar8 = *param_5;
  *param_5 = iVar8 + 1;
  piVar9 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  bVar7 = param_2 != 0;
  pcVar3 = "F1 Env Release";
  if (bVar7) {
    pcVar3 = "F2 Env Release";
  }
  pcVar1 = "AMP1 Env Release";
  if (bVar7) {
    pcVar1 = "AMP2 Env Release";
  }
  *(undefined ***)piVar9 = &PTR_thunk_FUN_10128edf8_1068ddff8;
  pcVar2 = "AEG1 Rel";
  if (bVar7) {
    pcVar2 = "AEG2 Rel";
  }
  piVar9[6] = iVar8;
  pcVar4 = "FEG1 Rel";
  if (bVar7) {
    pcVar4 = "FEG2 Rel";
  }
  if (param_3 != 0) {
    pcVar3 = pcVar1;
  }
  *(undefined8 *)(piVar9 + 10) = uVar6;
  *(undefined8 *)(piVar9 + 8) = uVar5;
  piVar9[2] = piVar9[2] + 1;
  if (param_3 != 0) {
    pcVar4 = pcVar2;
  }
  local_88 = piVar9;
  FUN_103192720(0x3f19999a,param_4,uVar10,pcVar3,piVar9,pcVar4,0);
  iVar8 = piVar9[2];
  piVar9[2] = iVar8 + -1;
  if (iVar8 + -1 == 0) {
    FUN_10128eea0(piVar9);
  }
  if (*(long *)PTR____stack_chk_guard_1064f8818 != local_68) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}

