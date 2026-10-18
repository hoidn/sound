
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1030e277c(long param_1)

{
  undefined8 *puVar1;
  undefined *puVar2;
  int iVar3;
  int *piVar4;
  long lVar5;
  undefined8 uVar6;
  long *plVar7;
  undefined8 uVar8;
  undefined8 uVar9;
  int *local_d0;
  int *local_c8;
  int *local_c0;
  int *local_b8;
  int *local_b0;
  int *local_a8;
  int *local_a0;
  int *local_98;
  int *local_90;
  undefined8 uStack_88;
  undefined1 auStack_80 [8];
  undefined1 auStack_78 [8];
  undefined1 auStack_70 [8];
  undefined1 auStack_68 [8];
  undefined1 auStack_60 [8];
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_1064f8818;
  if (((DAT_107026f78 & 1) == 0) && (iVar3 = ___cxa_guard_acquire(&DAT_107026f78), iVar3 != 0)) {
    FUN_101427680(&local_90,"Beam");
    FUN_101427680(&uStack_88,"Marimba");
    FUN_101427680(auStack_80,"String");
    FUN_101427680(auStack_78,"Membrane");
    FUN_101427680(auStack_70,"Plate");
    FUN_101427680(auStack_68,"Pipe");
    FUN_101427680(auStack_60,"Tube");
    FUN_1002c29cc(&DAT_107027230,&local_90,7);
    FUN_100234444(auStack_60);
    FUN_100234444(auStack_68);
    FUN_100234444(auStack_70);
    FUN_100234444(auStack_78);
    FUN_100234444(auStack_80);
    FUN_100234444(&uStack_88);
    FUN_100234444(&local_90);
    ___cxa_atexit(FUN_1002343c8,&DAT_107027230,0x100000000);
    ___cxa_guard_release(&DAT_107026f78);
  }
  uVar6 = *(undefined8 *)(param_1 + 0x268);
  FUN_101427680(&local_98,"Resonance Type");
  FUN_1026ef060(uVar6,0,&DAT_107027230,&local_98,1);
  if (local_98 != (int *)0x0) {
    iVar3 = *local_98;
    *local_98 = iVar3 + -1;
    if (iVar3 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar8 = *(undefined8 *)(param_1 + 0x280);
  piVar4 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  *(undefined ***)piVar4 = &PTR_thunk_FUN_10128edf8_1068c5b48;
  piVar4[6] = 1;
  uVar9 = _UNK_10561dfd8;
  uVar6 = _DAT_10561dfd0;
  *(undefined8 *)(piVar4 + 10) = _UNK_10561dfd8;
  *(undefined8 *)(piVar4 + 8) = uVar6;
  piVar4[2] = piVar4[2] + 1;
  local_90 = piVar4;
  FUN_103192720(0x3f000000,param_1,uVar8,"Decay",piVar4,0,0);
  iVar3 = piVar4[2];
  piVar4[2] = iVar3 + -1;
  if (iVar3 + -1 == 0) {
    FUN_10128eea0(piVar4);
  }
  FUN_103192720(0,param_1,*(undefined8 *)(param_1 + 0x430),"Note Off Decay",0,"Off Decay",0);
  FUN_103192974(0,param_1,*(undefined8 *)(param_1 + 0x298),"Material",0,0,2);
  FUN_103192974(0,param_1,*(undefined8 *)(param_1 + 0x2b0),"Inharmonics",0,0,2);
  FUN_103192720(0x3f800000,param_1,*(undefined8 *)(param_1 + 0x2f8),"Opening",0,0,0);
  FUN_103192720(0x3f000000,param_1,*(undefined8 *)(param_1 + 0x2c8),"Ratio",0,0,0);
  FUN_103192720(0x3f000000,param_1,*(undefined8 *)(param_1 + 0x2e0),"Radius",0,0,0);
  uVar8 = *(undefined8 *)(param_1 + 0x310);
  FUN_101427680(&local_a0,"Tune");
  piVar4 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  *(undefined ***)piVar4 = &PTR_thunk_FUN_10128edf8_1068c5b48;
  piVar4[6] = 6;
  *(undefined8 *)(piVar4 + 10) = uVar9;
  *(undefined8 *)(piVar4 + 8) = uVar6;
  piVar4[2] = piVar4[2] + 1;
  local_90 = piVar4;
  FUN_1011cb734(&local_a8);
  uVar6 = FUN_1012d9850(0x38);
  FUN_101575868(0,0x3f800000,0x3c2aaaab,0x38da740e);
  FUN_103197830(0x3f000000,param_1,uVar8,&local_a0,piVar4,&local_a8,0,uVar6);
  if (local_a8 != (int *)0x0) {
    iVar3 = *local_a8;
    *local_a8 = iVar3 + -1;
    if (iVar3 + -1 == 0) {
      FUN_101449efc();
    }
  }
  iVar3 = piVar4[2];
  piVar4[2] = iVar3 + -1;
  if (iVar3 + -1 == 0) {
    FUN_10128eea0(piVar4);
  }
  if (local_a0 != (int *)0x0) {
    iVar3 = *local_a0;
    *local_a0 = iVar3 + -1;
    if (iVar3 + -1 == 0) {
      FUN_101449efc();
    }
  }
  puVar2 = PTR__lambda___1__ARemoteable__TRemoteableUpdate__106551c78;
  local_90 = (int *)PTR__lambda___1__ARemoteable__TRemoteableUpdate__106551c78;
  uStack_88 = 0;
  FUN_10156934c(*(undefined8 *)(param_1 + 0x340),0xc0000000,&local_90);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x340),1);
  if (((DAT_107026f88 & 1) == 0) && (iVar3 = ___cxa_guard_acquire(&DAT_107026f88), iVar3 != 0)) {
    lVar5 = FUN_1012d9850(0x38);
    FUN_101577e1c(0xc2400000,0x42400000,lVar5,1);
    DAT_107026f80 = lVar5;
    if (lVar5 != 0) {
      *(int *)(lVar5 + 8) = *(int *)(lVar5 + 8) + 1;
    }
    ___cxa_atexit(FUN_1002483c0,&DAT_107026f80,0x100000000);
    ___cxa_guard_release(&DAT_107026f88);
  }
  lVar5 = DAT_107026f80;
  uVar9 = *(undefined8 *)(param_1 + 0x328);
  uVar6 = FUN_10143c034();
  FUN_101427680(&local_b0,"Transpose");
  FUN_1026f0b58(0xc2400000,0x42400000,0,uVar9,param_1,lVar5,uVar6,&local_b0,2);
  if (local_b0 != (int *)0x0) {
    iVar3 = *local_b0;
    *local_b0 = iVar3 + -1;
    if (iVar3 + -1 == 0) {
      FUN_101449efc();
    }
  }
  plVar7 = *(long **)(param_1 + 0x328);
  FUN_101427680(&local_90,"Transpose");
  (**(code **)(*plVar7 + 0x298))(plVar7,&local_90);
  if (local_90 != (int *)0x0) {
    iVar3 = *local_90;
    *local_90 = iVar3 + -1;
    if (iVar3 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar6 = (**(code **)(**(long **)(param_1 + 0x328) + 0x2b0))();
  FUN_1024dd614(uVar6,2);
  puVar1 = (undefined8 *)(param_1 + 0x328);
  uVar6 = (**(code **)(*(long *)*puVar1 + 0x2b0))();
  FUN_1024dd624(uVar6,*(undefined8 *)(param_1 + 0x340));
  uVar6 = FUN_1026f96b0(*puVar1);
  FUN_1024dd614(uVar6,2);
  FUN_1026f96b0(*puVar1);
  FUN_1025ba00c(0xc2400000,0x42400000);
  uVar6 = FUN_1026f96b0(*puVar1);
  FUN_1024dd624(uVar6,*(undefined8 *)(param_1 + 0x340));
  FUN_1026f1850(*puVar1,0);
  if (((DAT_107026f98 & 1) == 0) && (iVar3 = ___cxa_guard_acquire(&DAT_107026f98), iVar3 != 0)) {
    lVar5 = FUN_1012d9850(0x38);
    FUN_101577e1c(0xc2480000,0x42480000,lVar5,1);
    DAT_107026f90 = lVar5;
    if (lVar5 != 0) {
      *(int *)(lVar5 + 8) = *(int *)(lVar5 + 8) + 1;
    }
    ___cxa_atexit(FUN_1002483c0,&DAT_107026f90,0x100000000);
    ___cxa_guard_release(&DAT_107026f98);
  }
  if (((DAT_107026fa8 & 1) == 0) && (iVar3 = ___cxa_guard_acquire(&DAT_107026fa8), iVar3 != 0)) {
    FUN_101427680(&local_90," ct");
    FUN_102d7bdc0(&DAT_107026fa0,&local_90);
    FUN_100234444(&local_90);
    ___cxa_atexit(FUN_1027a8b40,&DAT_107026fa0,0x100000000);
    ___cxa_guard_release(&DAT_107026fa8);
  }
  uVar6 = DAT_107026fa0;
  lVar5 = DAT_107026f90;
  uVar9 = *(undefined8 *)(param_1 + 0x358);
  FUN_101427680(&local_b8,"Fine Transpose");
  FUN_1026f0b58(0xc2480000,0x42480000,0,uVar9,param_1,lVar5,uVar6,&local_b8,2);
  if (local_b8 != (int *)0x0) {
    iVar3 = *local_b8;
    *local_b8 = iVar3 + -1;
    if (iVar3 + -1 == 0) {
      FUN_101449efc();
    }
  }
  plVar7 = *(long **)(param_1 + 0x358);
  FUN_101427680(&local_90,"Fine");
  (**(code **)(*plVar7 + 0x298))(plVar7,&local_90);
  if (local_90 != (int *)0x0) {
    iVar3 = *local_90;
    *local_90 = iVar3 + -1;
    if (iVar3 + -1 == 0) {
      FUN_101449efc();
    }
  }
  FUN_103192974(0,param_1,*(undefined8 *)(param_1 + 0x370),"Spread",0,0,2);
  FUN_103192974(0,param_1,*(undefined8 *)(param_1 + 0x3b8),"Brightness",0,0,2);
  FUN_103192720(0,param_1,*(undefined8 *)(param_1 + 0x3d0),"Bleed",0,0,0);
  local_90 = (int *)puVar2;
  uStack_88 = 0;
  FUN_10156934c(*(undefined8 *)(param_1 + 0x3a0),0xc0000000,&local_90);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x3a0),1);
  if (((DAT_107026fb8 & 1) == 0) && (iVar3 = ___cxa_guard_acquire(&DAT_107026fb8), iVar3 != 0)) {
    lVar5 = FUN_1012d9850(0x38);
    FUN_101577e1c(0,0x41c00000,lVar5,1);
    DAT_107026fb0 = lVar5;
    if (lVar5 != 0) {
      *(int *)(lVar5 + 8) = *(int *)(lVar5 + 8) + 1;
    }
    ___cxa_atexit(FUN_1002483c0,&DAT_107026fb0,0x100000000);
    ___cxa_guard_release(&DAT_107026fb8);
  }
  lVar5 = DAT_107026fb0;
  uVar9 = *(undefined8 *)(param_1 + 0x388);
  uVar6 = FUN_10143c034();
  FUN_101427680(&local_c0,"PitchBend Range");
  FUN_1026f0b58(0,0x41c00000,0x40a00000,uVar9,param_1,lVar5,uVar6,&local_c0,2);
  if (local_c0 != (int *)0x0) {
    iVar3 = *local_c0;
    *local_c0 = iVar3 + -1;
    if (iVar3 + -1 == 0) {
      FUN_101449efc();
    }
  }
  plVar7 = *(long **)(param_1 + 0x388);
  FUN_101427680(&local_90,"PB Range");
  (**(code **)(*plVar7 + 0x298))(plVar7,&local_90);
  if (local_90 != (int *)0x0) {
    iVar3 = *local_90;
    *local_90 = iVar3 + -1;
    if (iVar3 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar6 = (**(code **)(**(long **)(param_1 + 0x388) + 0x2b0))();
  FUN_1024dd614(uVar6,2);
  puVar1 = (undefined8 *)(param_1 + 0x388);
  uVar6 = (**(code **)(*(long *)*puVar1 + 0x2b0))();
  FUN_1024dd624(uVar6,*(undefined8 *)(param_1 + 0x3a0));
  uVar6 = FUN_1026f96b0(*puVar1);
  FUN_1024dd614(uVar6,2);
  FUN_1026f96b0(*puVar1);
  FUN_1025ba00c(0,0x41c00000);
  uVar6 = FUN_1026f96b0(*puVar1);
  FUN_1024dd624(uVar6,*(undefined8 *)(param_1 + 0x3a0));
  FUN_1026f1850(*puVar1,0);
  FUN_103192720(0x3f000000,param_1,*(undefined8 *)(param_1 + 0x448),"Hit",0,0,0);
  FUN_103192720(0x3dcccccd,param_1,*(undefined8 *)(param_1 + 0x460),"Listening L",0,0,0);
  FUN_103192720(0x3f666666,param_1,*(undefined8 *)(param_1 + 0x478),"Listening R",0,0,0);
  FUN_10319285c(*(undefined8 *)(param_1 + 1000),"MIDI Frequency",0,0);
  if (((DAT_107026fc0 & 1) == 0) && (iVar3 = ___cxa_guard_acquire(&DAT_107026fc0), iVar3 != 0)) {
    FUN_101427680(&local_90,"Last");
    FUN_101427680(&uStack_88,"Low");
    FUN_1002c29cc(&DAT_107027248,&local_90,2);
    FUN_100234444(&uStack_88);
    FUN_100234444(&local_90);
    ___cxa_atexit(FUN_1002343c8,&DAT_107027248,0x100000000);
    ___cxa_guard_release(&DAT_107026fc0);
  }
  uVar6 = *(undefined8 *)(param_1 + 0x400);
  FUN_101427680(&local_c8,"MIDI Mode");
  FUN_1026ef060(uVar6,0,&DAT_107027248,&local_c8,1);
  if (local_c8 != (int *)0x0) {
    iVar3 = *local_c8;
    *local_c8 = iVar3 + -1;
    if (iVar3 + -1 == 0) {
      FUN_101449efc();
    }
  }
  FUN_10319285c(*(undefined8 *)(param_1 + 0x418),"Note Off",0,0);
  if (((DAT_107026fc8 & 1) == 0) && (iVar3 = ___cxa_guard_acquire(&DAT_107026fc8), iVar3 != 0)) {
    FUN_101427680(&local_90,"Eco");
    FUN_101427680(&uStack_88,"Low");
    FUN_101427680(auStack_80,"Med");
    FUN_101427680(auStack_78,"High");
    FUN_1002c29cc(&DAT_107027260,&local_90,4);
    FUN_100234444(auStack_78);
    FUN_100234444(auStack_80);
    FUN_100234444(&uStack_88);
    FUN_100234444(&local_90);
    ___cxa_atexit(FUN_1002343c8,&DAT_107027260,0x100000000);
    ___cxa_guard_release(&DAT_107026fc8);
  }
  uVar6 = *(undefined8 *)(param_1 + 0x628);
  FUN_101427680(&local_d0,"Resonator Quality");
  FUN_1026ef060(uVar6,2,&DAT_107027260,&local_d0,1);
  if (local_d0 != (int *)0x0) {
    iVar3 = *local_d0;
    *local_d0 = iVar3 + -1;
    if (iVar3 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (*(long *)PTR____stack_chk_guard_1064f8818 == local_58) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

