
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1030d6708(long param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4)

{
  int iVar1;
  undefined8 *puVar2;
  undefined8 uVar3;
  int *piVar4;
  long lVar5;
  long *plVar6;
  undefined8 uVar7;
  undefined8 uVar8;
  undefined8 uVar9;
  int *local_248;
  int *local_240;
  int *local_238;
  int *local_230;
  int *local_228;
  int *local_220;
  int *local_218;
  int *local_210;
  int *local_208;
  int *local_200;
  int *local_1f8;
  int *local_1f0;
  int *local_1e8;
  int *local_1e0;
  int *local_1d8;
  int *local_1d0;
  int *local_1c8;
  int *local_1c0;
  int *local_1b8;
  int *local_1b0;
  int *local_1a8;
  int *local_1a0;
  int *local_198;
  int *local_190;
  int *local_188;
  int *local_180;
  int *local_178;
  int *local_170;
  int *local_168;
  int *local_160;
  int *local_158;
  int *local_150;
  int *local_148;
  int *local_140;
  int *local_138;
  int *local_130;
  int *local_128;
  int *local_120;
  int *local_118;
  int *local_110;
  int *local_108;
  int *local_100;
  int *local_f8;
  int *local_f0;
  int *local_e8;
  int *local_e0;
  int *local_d8;
  int *local_d0;
  int *local_c8;
  int *local_c0;
  int *local_b8;
  undefined4 local_b0;
  undefined4 uStack_ac;
  int *local_a8;
  int *local_a0;
  undefined8 uStack_98;
  undefined1 auStack_90 [8];
  undefined1 auStack_88 [8];
  undefined1 auStack_80 [8];
  undefined1 auStack_78 [8];
  undefined1 auStack_70 [8];
  long local_68;
  
  local_68 = *(long *)PTR____stack_chk_guard_1064f8818;
  *(undefined8 *)(param_1 + 0x3a0) = param_4;
  FUN_101427680(&local_b0,"Res ");
  FUN_101430a10(&local_a0,param_3);
  puVar2 = (undefined8 *)FUN_10142da5c(&local_b0,&local_a0);
  if (local_a0 != (int *)0x0) {
    iVar1 = *local_a0;
    *local_a0 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  local_a8 = (int *)*puVar2;
  if (local_a8 != (int *)0x0) {
    *local_a8 = *local_a8 + 1;
  }
  piVar4 = (int *)CONCAT44(uStack_ac,local_b0);
  if ((piVar4 != (int *)0x0) && (iVar1 = *piVar4, *piVar4 = iVar1 + -1, iVar1 + -1 == 0)) {
    FUN_101449efc();
  }
  uVar3 = *(undefined8 *)(param_1 + 0x48);
  if (local_a8 != (int *)0x0) {
    *local_a8 = *local_a8 + 1;
  }
  local_b8 = local_a8;
  FUN_10156fa68(uVar3,&local_b8);
  if (local_b8 != (int *)0x0) {
    iVar1 = *local_b8;
    *local_b8 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  piVar4 = (int *)PTR__lambda___1__ARemoteable__TRemoteableUpdate__106551c78;
  local_a0 = (int *)PTR__lambda___1__ARemoteable__TRemoteableUpdate__106551c78;
  uStack_98 = 0;
  FUN_10156934c(*(undefined8 *)(param_1 + 0x30),param_3,&local_a0);
  uVar3 = *(undefined8 *)(param_1 + 0x60);
  FUN_10142dd4c(&local_c0,&local_a8," On/Off");
  FUN_1011cb734(&local_c8);
  FUN_1031980a4(uVar3,&local_c0,0,&local_c8);
  if (local_c8 != (int *)0x0) {
    iVar1 = *local_c8;
    *local_c8 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_c0 != (int *)0x0) {
    iVar1 = *local_c0;
    *local_c0 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (((DAT_107026ee8 & 1) == 0) && (iVar1 = ___cxa_guard_acquire(&DAT_107026ee8), iVar1 != 0)) {
    FUN_101427680(&local_a0,"Beam");
    FUN_101427680(&uStack_98,"Marimba");
    FUN_101427680(auStack_90,"String");
    FUN_101427680(auStack_88,"Membrane");
    FUN_101427680(auStack_80,"Plate");
    FUN_101427680(auStack_78,"Pipe");
    FUN_101427680(auStack_70,"Tube");
    FUN_1002c29cc(&DAT_1070271d0,&local_a0,7);
    FUN_100234444(auStack_70);
    FUN_100234444(auStack_78);
    FUN_100234444(auStack_80);
    FUN_100234444(auStack_88);
    FUN_100234444(auStack_90);
    FUN_100234444(&uStack_98);
    FUN_100234444(&local_a0);
    ___cxa_atexit(FUN_1002343c8,&DAT_1070271d0,0x100000000);
    ___cxa_guard_release(&DAT_107026ee8);
    piVar4 = (int *)PTR__lambda___1__ARemoteable__TRemoteableUpdate__106551c78;
  }
  uVar3 = *(undefined8 *)(param_1 + 0x78);
  FUN_10142dd4c(&local_d0,&local_a8," Type");
  FUN_1026ef060(uVar3,0,&DAT_1070271d0,&local_d0,1);
  if (local_d0 != (int *)0x0) {
    iVar1 = *local_d0;
    *local_d0 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (((DAT_107026ef0 & 1) == 0) && (iVar1 = ___cxa_guard_acquire(&DAT_107026ef0), iVar1 != 0)) {
    FUN_101427680(&local_a0,"Eco");
    FUN_101427680(&uStack_98,"Low");
    FUN_101427680(auStack_90,"Med");
    FUN_101427680(auStack_88,"High");
    FUN_1002c29cc(&DAT_1070271e8,&local_a0,4);
    FUN_100234444(auStack_88);
    FUN_100234444(auStack_90);
    FUN_100234444(&uStack_98);
    FUN_100234444(&local_a0);
    ___cxa_atexit(FUN_1002343c8,&DAT_1070271e8,0x100000000);
    ___cxa_guard_release(&DAT_107026ef0);
  }
  uVar3 = *(undefined8 *)(param_1 + 0x90);
  FUN_10142dd4c(&local_d8,&local_a8," Quality");
  FUN_1026ef060(uVar3,2,&DAT_1070271e8,&local_d8,1);
  if (local_d8 != (int *)0x0) {
    iVar1 = *local_d8;
    *local_d8 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uStack_98 = 0;
  local_a0 = piVar4;
  FUN_10156934c(*(undefined8 *)(param_1 + 0xc0),0xc0000000,&local_a0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0xc0),1);
  if (((DAT_107026f00 & 1) == 0) && (iVar1 = ___cxa_guard_acquire(&DAT_107026f00), iVar1 != 0)) {
    lVar5 = FUN_1012d9850(0x38);
    FUN_101577e1c(0xc2400000,0x42400000,lVar5,0xc);
    DAT_107026ef8 = lVar5;
    if (lVar5 != 0) {
      *(int *)(lVar5 + 8) = *(int *)(lVar5 + 8) + 1;
    }
    ___cxa_atexit(FUN_1002483c0,&DAT_107026ef8,0x100000000);
    ___cxa_guard_release(&DAT_107026f00);
  }
  lVar5 = DAT_107026ef8;
  uVar7 = *(undefined8 *)(param_1 + 0xa8);
  uVar3 = FUN_10143c034();
  FUN_10142dd4c(&local_e0,&local_a8," Tune");
  FUN_1026f0b58(0xc2400000,0x42400000,0,uVar7,param_2,lVar5,uVar3,&local_e0,2);
  if (local_e0 != (int *)0x0) {
    iVar1 = *local_e0;
    *local_e0 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar3 = (**(code **)(**(long **)(param_1 + 0xa8) + 0x2b0))();
  FUN_1024dd614(uVar3,2);
  uVar3 = (**(code **)(**(long **)(param_1 + 0xa8) + 0x2b0))();
  FUN_1024dd624(uVar3,*(undefined8 *)(param_1 + 0xc0));
  uVar3 = FUN_1026f96b0(*(undefined8 *)(param_1 + 0xa8));
  FUN_1024dd614(uVar3,2);
  FUN_1026f96b0(*(undefined8 *)(param_1 + 0xa8));
  FUN_1025ba00c(0xc2400000,0x42400000);
  uVar3 = FUN_1026f96b0(*(undefined8 *)(param_1 + 0xa8));
  FUN_1024dd624(uVar3,*(undefined8 *)(param_1 + 0xc0));
  FUN_1026f1850(*(undefined8 *)(param_1 + 0xa8),0);
  if (((DAT_107026f10 & 1) == 0) && (iVar1 = ___cxa_guard_acquire(&DAT_107026f10), iVar1 != 0)) {
    lVar5 = FUN_1012d9850(0x38);
    FUN_101577e1c(0xc2480000,0x42480000,lVar5,1);
    DAT_107026f08 = lVar5;
    if (lVar5 != 0) {
      *(int *)(lVar5 + 8) = *(int *)(lVar5 + 8) + 1;
    }
    ___cxa_atexit(FUN_1002483c0,&DAT_107026f08,0x100000000);
    ___cxa_guard_release(&DAT_107026f10);
  }
  if (((DAT_107026f20 & 1) == 0) && (iVar1 = ___cxa_guard_acquire(&DAT_107026f20), iVar1 != 0)) {
    FUN_101427680(&local_a0," ct");
    FUN_102d7bdc0(&DAT_107026f18,&local_a0);
    FUN_100234444(&local_a0);
    ___cxa_atexit(FUN_1027a8b40,&DAT_107026f18,0x100000000);
    ___cxa_guard_release(&DAT_107026f20);
  }
  uVar3 = DAT_107026f18;
  lVar5 = DAT_107026f08;
  uVar7 = *(undefined8 *)(param_1 + 0xd8);
  FUN_10142dd4c(&local_e8,&local_a8," Fine Tune");
  FUN_1026f0b58(0xc2480000,0x42480000,0,uVar7,param_2,lVar5,uVar3,&local_e8,2);
  if (local_e8 != (int *)0x0) {
    iVar1 = *local_e8;
    *local_e8 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar3 = *(undefined8 *)(param_1 + 0xf0);
  FUN_10142dd4c(&local_f0,&local_a8," Tune < Key");
  FUN_1030cdf18(0x3f800000,param_2,uVar3,&local_f0);
  if (local_f0 != (int *)0x0) {
    iVar1 = *local_f0;
    *local_f0 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar3 = *(undefined8 *)(param_1 + 0x108);
  FUN_10142dd4c(&local_f8,&local_a8," Pitch Env.");
  FUN_1011cb734(&local_100);
  FUN_103197e1c(0,param_2,uVar3,&local_f8,0,&local_100,0);
  if (local_100 != (int *)0x0) {
    iVar1 = *local_100;
    *local_100 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_f8 != (int *)0x0) {
    iVar1 = *local_f8;
    *local_f8 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar3 = *(undefined8 *)(param_1 + 0x120);
  FUN_10142dd4c(&local_108,&local_a8," Pitch Env. < Vel");
  FUN_1030cb214(0,param_2,uVar3,&local_108);
  if (local_108 != (int *)0x0) {
    iVar1 = *local_108;
    *local_108 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar8 = *(undefined8 *)(param_1 + 0x138);
  FUN_10142dd4c(&local_110,&local_a8," Pitch Env. Time");
  piVar4 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  *(undefined ***)piVar4 = &PTR_thunk_FUN_10128edf8_1068c5778;
  piVar4[6] = 0x21;
  uVar7 = _UNK_10561dfd8;
  uVar3 = _DAT_10561dfd0;
  *(undefined8 *)(piVar4 + 10) = _UNK_10561dfd8;
  *(undefined8 *)(piVar4 + 8) = uVar3;
  piVar4[2] = piVar4[2] + 1;
  local_a0 = piVar4;
  FUN_1011cb734(&local_118);
  FUN_103197830(0x3f000000,param_2,uVar8,&local_110,piVar4,&local_118,0,0);
  if (local_118 != (int *)0x0) {
    iVar1 = *local_118;
    *local_118 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  iVar1 = piVar4[2];
  piVar4[2] = iVar1 + -1;
  if (iVar1 + -1 == 0) {
    FUN_10128eea0(piVar4);
  }
  if (local_110 != (int *)0x0) {
    iVar1 = *local_110;
    *local_110 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar8 = *(undefined8 *)(param_1 + 0x150);
  FUN_10142dd4c(&local_120,&local_a8," Decay");
  piVar4 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  *(undefined ***)piVar4 = &PTR_thunk_FUN_10128edf8_1068c5778;
  piVar4[6] = 0x22;
  *(undefined8 *)(piVar4 + 10) = uVar7;
  *(undefined8 *)(piVar4 + 8) = uVar3;
  piVar4[2] = piVar4[2] + 1;
  local_a0 = piVar4;
  FUN_1011cb734(&local_128);
  FUN_103197830(0x3f000000,param_2,uVar8,&local_120,piVar4,&local_128,0,0);
  if (local_128 != (int *)0x0) {
    iVar1 = *local_128;
    *local_128 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  iVar1 = piVar4[2];
  piVar4[2] = iVar1 + -1;
  if (iVar1 + -1 == 0) {
    FUN_10128eea0(piVar4);
  }
  if (local_120 != (int *)0x0) {
    iVar1 = *local_120;
    *local_120 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar8 = *(undefined8 *)(param_1 + 0x168);
  FUN_10142dd4c(&local_130,&local_a8," Decay < Vel");
  FUN_1030cb214(0,param_2,uVar8,&local_130);
  if (local_130 != (int *)0x0) {
    iVar1 = *local_130;
    *local_130 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar8 = *(undefined8 *)(param_1 + 0x180);
  FUN_10142dd4c(&local_138,&local_a8," Decay < Key");
  FUN_1030cdf18(0,param_2,uVar8,&local_138);
  if (local_138 != (int *)0x0) {
    iVar1 = *local_138;
    *local_138 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar8 = *(undefined8 *)(param_1 + 0x198);
  FUN_10142dd4c(&local_140,&local_a8," Off Decay");
  FUN_1011cb734(&local_148);
  FUN_103197830(0,param_2,uVar8,&local_140,0,&local_148,0,0);
  if (local_148 != (int *)0x0) {
    iVar1 = *local_148;
    *local_148 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_140 != (int *)0x0) {
    iVar1 = *local_140;
    *local_140 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar9 = *(undefined8 *)(param_1 + 0x1b0);
  FUN_10142dd4c(&local_150,&local_a8," Material");
  piVar4 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  *(undefined ***)piVar4 = &PTR_thunk_FUN_10128edf8_1068c5778;
  piVar4[6] = 0x26;
  uVar8 = _DAT_1058c6a80;
  *(undefined8 *)(piVar4 + 10) = _UNK_1058c6a88;
  *(undefined8 *)(piVar4 + 8) = uVar8;
  piVar4[2] = piVar4[2] + 1;
  local_a0 = piVar4;
  FUN_1011cb734(&local_158);
  FUN_103197e1c(0,param_2,uVar9,&local_150,piVar4,&local_158,2);
  if (local_158 != (int *)0x0) {
    iVar1 = *local_158;
    *local_158 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  iVar1 = piVar4[2];
  piVar4[2] = iVar1 + -1;
  if (iVar1 + -1 == 0) {
    FUN_10128eea0(piVar4);
  }
  if (local_150 != (int *)0x0) {
    iVar1 = *local_150;
    *local_150 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar8 = *(undefined8 *)(param_1 + 0x1c8);
  FUN_10142dd4c(&local_160,&local_a8," Material < Vel");
  FUN_1030cb214(0,param_2,uVar8,&local_160);
  if (local_160 != (int *)0x0) {
    iVar1 = *local_160;
    *local_160 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar8 = *(undefined8 *)(param_1 + 0x1e0);
  FUN_10142dd4c(&local_168,&local_a8," Material < Key");
  FUN_1030cdf18(0,param_2,uVar8,&local_168);
  if (local_168 != (int *)0x0) {
    iVar1 = *local_168;
    *local_168 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar8 = *(undefined8 *)(param_1 + 0x1f8);
  FUN_10142dd4c(&local_170,&local_a8," Radius");
  FUN_1011cb734(&local_178);
  FUN_103197830(0x3f000000,param_2,uVar8,&local_170,0,&local_178,0,0);
  if (local_178 != (int *)0x0) {
    iVar1 = *local_178;
    *local_178 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_170 != (int *)0x0) {
    iVar1 = *local_170;
    *local_170 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar8 = *(undefined8 *)(param_1 + 0x210);
  FUN_10142dd4c(&local_180,&local_a8," Radius < Vel");
  FUN_1030cb214(0,param_2,uVar8,&local_180);
  if (local_180 != (int *)0x0) {
    iVar1 = *local_180;
    *local_180 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar8 = *(undefined8 *)(param_1 + 0x228);
  FUN_10142dd4c(&local_188,&local_a8," Radius < Key");
  FUN_1030cdf18(0,param_2,uVar8,&local_188);
  if (local_188 != (int *)0x0) {
    iVar1 = *local_188;
    *local_188 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar8 = *(undefined8 *)(param_1 + 0x2d0);
  FUN_10142dd4c(&local_190,&local_a8," Ratio");
  FUN_1011cb734(&local_198);
  FUN_103197830(0,param_2,uVar8,&local_190,0,&local_198,0,0);
  if (local_198 != (int *)0x0) {
    iVar1 = *local_198;
    *local_198 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_190 != (int *)0x0) {
    iVar1 = *local_190;
    *local_190 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar8 = *(undefined8 *)(param_1 + 0x240);
  FUN_10142dd4c(&local_1a0,&local_a8," Brightness");
  FUN_1011cb734(&local_1a8);
  FUN_103197e1c(0,param_2,uVar8,&local_1a0,0,&local_1a8,2);
  if (local_1a8 != (int *)0x0) {
    iVar1 = *local_1a8;
    *local_1a8 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_1a0 != (int *)0x0) {
    iVar1 = *local_1a0;
    *local_1a0 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar8 = *(undefined8 *)(param_1 + 600);
  FUN_10142dd4c(&local_1b0,&local_a8," Bleed");
  FUN_1011cb734(&local_1b8);
  FUN_103197830(0,param_2,uVar8,&local_1b0,0,&local_1b8,0,0);
  if (local_1b8 != (int *)0x0) {
    iVar1 = *local_1b8;
    *local_1b8 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_1b0 != (int *)0x0) {
    iVar1 = *local_1b0;
    *local_1b0 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar8 = *(undefined8 *)(param_1 + 0x270);
  FUN_10142dd4c(&local_1c0,&local_a8," Inharmonics");
  FUN_1011cb734(&local_1c8);
  FUN_103197e1c(0,param_2,uVar8,&local_1c0,0,&local_1c8,2);
  if (local_1c8 != (int *)0x0) {
    iVar1 = *local_1c8;
    *local_1c8 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_1c0 != (int *)0x0) {
    iVar1 = *local_1c0;
    *local_1c0 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar8 = *(undefined8 *)(param_1 + 0x288);
  FUN_10142dd4c(&local_1d0,&local_a8," Inharmonics < Vel");
  FUN_1030cb214(0,param_2,uVar8,&local_1d0);
  if (local_1d0 != (int *)0x0) {
    iVar1 = *local_1d0;
    *local_1d0 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar8 = *(undefined8 *)(param_1 + 0x2a0);
  FUN_10142dd4c(&local_1d8,&local_a8," Opening");
  FUN_1011cb734(&local_1e0);
  FUN_103197830(0x3f800000,param_2,uVar8,&local_1d8,0,&local_1e0,0,0);
  if (local_1e0 != (int *)0x0) {
    iVar1 = *local_1e0;
    *local_1e0 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_1d8 != (int *)0x0) {
    iVar1 = *local_1d8;
    *local_1d8 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar8 = *(undefined8 *)(param_1 + 0x2b8);
  FUN_10142dd4c(&local_1e8,&local_a8," Opening < Vel");
  FUN_1030cb214(0,param_2,uVar8,&local_1e8);
  if (local_1e8 != (int *)0x0) {
    iVar1 = *local_1e8;
    *local_1e8 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar8 = *(undefined8 *)(param_1 + 0x2e8);
  FUN_10142dd4c(&local_1f0,&local_a8," Hit");
  FUN_1011cb734(&local_1f8);
  FUN_103197830(0x3f000000,param_2,uVar8,&local_1f0,0,&local_1f8,0,0);
  if (local_1f8 != (int *)0x0) {
    iVar1 = *local_1f8;
    *local_1f8 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_1f0 != (int *)0x0) {
    iVar1 = *local_1f0;
    *local_1f0 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar8 = *(undefined8 *)(param_1 + 0x300);
  FUN_10142dd4c(&local_200,&local_a8," Hit < Random");
  FUN_1011cb734(&local_208);
  FUN_103197830(0,param_2,uVar8,&local_200,0,&local_208,0,0);
  if (local_208 != (int *)0x0) {
    iVar1 = *local_208;
    *local_208 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_200 != (int *)0x0) {
    iVar1 = *local_200;
    *local_200 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar8 = *(undefined8 *)(param_1 + 0x318);
  FUN_10142dd4c(&local_210,&local_a8," Listening L");
  FUN_1011cb734(&local_218);
  FUN_103197830(0x3dcccccd,param_2,uVar8,&local_210,0,&local_218,0,0);
  if (local_218 != (int *)0x0) {
    iVar1 = *local_218;
    *local_218 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_210 != (int *)0x0) {
    iVar1 = *local_210;
    *local_210 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar8 = *(undefined8 *)(param_1 + 0x330);
  FUN_10142dd4c(&local_220,&local_a8," Listening R");
  FUN_1011cb734(&local_228);
  FUN_103197830(0x3f666666,param_2,uVar8,&local_220,0,&local_228,0,0);
  if (local_228 != (int *)0x0) {
    iVar1 = *local_228;
    *local_228 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_220 != (int *)0x0) {
    iVar1 = *local_220;
    *local_220 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (((DAT_107026f30 & 1) == 0) && (iVar1 = ___cxa_guard_acquire(&DAT_107026f30), iVar1 != 0)) {
    lVar5 = FUN_1012d9850(0x38);
    FUN_101575868(0xbf800000,0x3f800000,0x3dcccccd,0x3ca3d70a);
    DAT_107026f28 = lVar5;
    if (lVar5 != 0) {
      *(int *)(lVar5 + 8) = *(int *)(lVar5 + 8) + 1;
    }
    ___cxa_atexit(FUN_1002483c0,&DAT_107026f28,0x100000000);
    ___cxa_guard_release(&DAT_107026f30);
  }
  lVar5 = DAT_107026f28;
  uVar9 = *(undefined8 *)(param_1 + 0x348);
  uVar8 = FUN_101439ec4();
  FUN_10142dd4c(&local_230,&local_a8," Panorama");
  FUN_1026f0b58(0xbf800000,0x3f800000,0,uVar9,param_2,lVar5,uVar8,&local_230,2);
  if (local_230 != (int *)0x0) {
    iVar1 = *local_230;
    *local_230 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  plVar6 = *(long **)(param_1 + 0x348);
  FUN_10142dd4c(&local_a0,&local_a8," Pan");
  (**(code **)(*plVar6 + 0x298))(plVar6,&local_a0);
  if (local_a0 != (int *)0x0) {
    iVar1 = *local_a0;
    *local_a0 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar8 = *(undefined8 *)(param_1 + 0x360);
  FUN_10142dd4c(&local_238,&local_a8," Panorama < Key");
  if (((DAT_107027110 & 1) == 0) && (iVar1 = ___cxa_guard_acquire(&DAT_107027110), iVar1 != 0)) {
    lVar5 = FUN_1012d9850(0x38);
    FUN_101575868(0xbf800000,0x3f800000,0x3b03126f,0x3951b718);
    DAT_107027108 = lVar5;
    if (lVar5 != 0) {
      *(int *)(lVar5 + 8) = *(int *)(lVar5 + 8) + 1;
    }
    ___cxa_atexit(FUN_1019a2da0,&DAT_107027108,0x100000000);
    ___cxa_guard_release(&DAT_107027110);
  }
  if (((DAT_107027120 & 1) == 0) && (iVar1 = ___cxa_guard_acquire(&DAT_107027120), iVar1 != 0)) {
    local_b0 = 0x40a00000;
    FUN_1030ee7c4(&local_a0,&local_b0);
    DAT_107027118 = local_a0;
    local_a0 = (int *)0x0;
    FUN_1030ee830(&local_a0);
    ___cxa_atexit(FUN_101437c58,&DAT_107027118,0x100000000);
    ___cxa_guard_release(&DAT_107027120);
  }
  piVar4 = DAT_107027118;
  lVar5 = DAT_107027108;
  local_a0 = local_238;
  if (local_238 != (int *)0x0) {
    *local_238 = *local_238 + 1;
  }
  FUN_1026f0b58(0xbf800000,0x3f800000,0,uVar8,param_2,lVar5,piVar4,&local_a0,2);
  if (local_a0 != (int *)0x0) {
    iVar1 = *local_a0;
    *local_a0 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_238 != (int *)0x0) {
    iVar1 = *local_238;
    *local_238 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  plVar6 = *(long **)(param_1 + 0x360);
  FUN_10142dd4c(&local_a0,&local_a8," Pan < Key");
  (**(code **)(*plVar6 + 0x298))(plVar6,&local_a0);
  if (local_a0 != (int *)0x0) {
    iVar1 = *local_a0;
    *local_a0 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar8 = *(undefined8 *)(param_1 + 0x378);
  FUN_10142dd4c(&local_240,&local_a8," Volume");
  piVar4 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  *(undefined ***)piVar4 = &PTR_thunk_FUN_10128edf8_1068c5778;
  piVar4[6] = 0x39;
  *(undefined8 *)(piVar4 + 10) = uVar7;
  *(undefined8 *)(piVar4 + 8) = uVar3;
  piVar4[2] = piVar4[2] + 1;
  local_a0 = piVar4;
  FUN_1011cb734(&local_248);
  FUN_103197830(0x3f000000,param_2,uVar8,&local_240,piVar4,&local_248,0,0);
  if (local_248 != (int *)0x0) {
    iVar1 = *local_248;
    *local_248 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  iVar1 = piVar4[2];
  piVar4[2] = iVar1 + -1;
  if (iVar1 + -1 == 0) {
    FUN_10128eea0(piVar4);
  }
  if (local_240 != (int *)0x0) {
    iVar1 = *local_240;
    *local_240 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_a8 != (int *)0x0) {
    iVar1 = *local_a8;
    *local_a8 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (*(long *)PTR____stack_chk_guard_1064f8818 == local_68) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

