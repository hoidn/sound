
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1030d1d80(long param_1,undefined8 param_2)

{
  undefined *puVar1;
  int iVar2;
  int *piVar3;
  long lVar4;
  undefined8 uVar5;
  undefined8 uVar6;
  undefined8 uVar7;
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
  int *local_b0;
  int *local_a8;
  int *local_a0;
  int *local_98;
  int *local_90;
  int *local_88;
  undefined4 local_7c;
  int *local_78;
  long lStack_70;
  undefined1 auStack_68 [8];
  undefined1 auStack_60 [8];
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_1064f8818;
  FUN_101427680(&local_88,"Noise");
  uVar6 = *(undefined8 *)(param_1 + 0x70);
  FUN_10142dd4c(&local_90,&local_88," On/Off");
  FUN_1011cb734(&local_98);
  FUN_1031980a4(uVar6,&local_90,0,&local_98);
  if (local_98 != (int *)0x0) {
    iVar2 = *local_98;
    *local_98 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_90 != (int *)0x0) {
    iVar2 = *local_90;
    *local_90 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar7 = *(undefined8 *)(param_1 + 0x88);
  FUN_10142dd4c(&local_a0,&local_88," Volume");
  piVar3 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  *(undefined ***)piVar3 = &PTR_thunk_FUN_10128edf8_1068c5778;
  piVar3[6] = 0xc;
  uVar5 = _UNK_10561dfd8;
  uVar6 = _DAT_10561dfd0;
  *(undefined8 *)(piVar3 + 10) = _UNK_10561dfd8;
  *(undefined8 *)(piVar3 + 8) = uVar6;
  piVar3[2] = piVar3[2] + 1;
  local_78 = piVar3;
  FUN_1011cb734(&local_a8);
  FUN_103197830(0x3f000000,param_2,uVar7,&local_a0,piVar3,&local_a8,0,0);
  if (local_a8 != (int *)0x0) {
    iVar2 = *local_a8;
    *local_a8 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  iVar2 = piVar3[2];
  piVar3[2] = iVar2 + -1;
  if (iVar2 + -1 == 0) {
    FUN_10128eea0(piVar3);
  }
  if (local_a0 != (int *)0x0) {
    iVar2 = *local_a0;
    *local_a0 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar7 = *(undefined8 *)(param_1 + 0xa0);
  FUN_10142dd4c(&local_b0,&local_88," Volume < Vel");
  FUN_1030cb214(0,param_2,uVar7,&local_b0);
  if (local_b0 != (int *)0x0) {
    iVar2 = *local_b0;
    *local_b0 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar7 = *(undefined8 *)(param_1 + 0xb8);
  FUN_10142dd4c(&local_b8,&local_88," Volume < Key");
  FUN_1030cdf18(0,param_2,uVar7,&local_b8);
  if (local_b8 != (int *)0x0) {
    iVar2 = *local_b8;
    *local_b8 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (((DAT_107026ee0 & 1) == 0) && (iVar2 = ___cxa_guard_acquire(&DAT_107026ee0), iVar2 != 0)) {
    FUN_101427680(&local_78,"LP");
    FUN_101427680(&lStack_70,"HP");
    FUN_101427680(auStack_68,"BP");
    FUN_101427680(auStack_60,"LP+HP");
    FUN_1002c29cc(&DAT_1070271b8,&local_78,4);
    FUN_100234444(auStack_60);
    FUN_100234444(auStack_68);
    FUN_100234444(&lStack_70);
    FUN_100234444(&local_78);
    ___cxa_atexit(FUN_1002343c8,&DAT_1070271b8,0x100000000);
    ___cxa_guard_release(&DAT_107026ee0);
  }
  uVar7 = *(undefined8 *)(param_1 + 0xd0);
  FUN_10142dd4c(&local_c0,&local_88," Filter Type");
  FUN_1026ef060(uVar7,0,&DAT_1070271b8,&local_c0,1);
  if (local_c0 != (int *)0x0) {
    iVar2 = *local_c0;
    *local_c0 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar7 = *(undefined8 *)(param_1 + 0xe8);
  FUN_10142dd4c(&local_c8,&local_88," Filter Freq");
  piVar3 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  *(undefined ***)piVar3 = &PTR_thunk_FUN_10128edf8_1068c5778;
  piVar3[6] = 0x10;
  *(undefined8 *)(piVar3 + 10) = uVar5;
  *(undefined8 *)(piVar3 + 8) = uVar6;
  piVar3[2] = piVar3[2] + 1;
  local_78 = piVar3;
  FUN_1011cb734(&local_d0);
  FUN_103197830(0x3f000000,param_2,uVar7,&local_c8,piVar3,&local_d0,0,0);
  if (local_d0 != (int *)0x0) {
    iVar2 = *local_d0;
    *local_d0 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  iVar2 = piVar3[2];
  piVar3[2] = iVar2 + -1;
  if (iVar2 + -1 == 0) {
    FUN_10128eea0(piVar3);
  }
  if (local_c8 != (int *)0x0) {
    iVar2 = *local_c8;
    *local_c8 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar7 = *(undefined8 *)(param_1 + 0x100);
  FUN_10142dd4c(&local_d8,&local_88," Freq < Vel");
  if (((DAT_1070270f0 & 1) == 0) && (iVar2 = ___cxa_guard_acquire(&DAT_1070270f0), iVar2 != 0)) {
    lVar4 = FUN_1012d9850(0x38);
    FUN_101575868(0xc1000000,0x41000000,0x3da3d70a,0x3c03126f);
    DAT_1070270e8 = lVar4;
    if (lVar4 != 0) {
      *(int *)(lVar4 + 8) = *(int *)(lVar4 + 8) + 1;
    }
    ___cxa_atexit(FUN_1019a2da0,&DAT_1070270e8,0x100000000);
    ___cxa_guard_release(&DAT_1070270f0);
  }
  if (((DAT_107027100 & 1) == 0) && (iVar2 = ___cxa_guard_acquire(&DAT_107027100), iVar2 != 0)) {
    local_7c = 0x3e000000;
    FUN_1030ee7c4(&local_78,&local_7c);
    DAT_1070270f8 = local_78;
    local_78 = (int *)0x0;
    FUN_1030ee830(&local_78);
    ___cxa_atexit(FUN_101437c58,&DAT_1070270f8,0x100000000);
    ___cxa_guard_release(&DAT_107027100);
  }
  piVar3 = DAT_1070270f8;
  lVar4 = DAT_1070270e8;
  local_78 = local_d8;
  if (local_d8 != (int *)0x0) {
    *local_d8 = *local_d8 + 1;
  }
  FUN_1026f0b58(0xc1000000,0x41000000,0,uVar7,param_2,lVar4,piVar3,&local_78,2);
  if (local_78 != (int *)0x0) {
    iVar2 = *local_78;
    *local_78 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_d8 != (int *)0x0) {
    iVar2 = *local_d8;
    *local_d8 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar7 = *(undefined8 *)(param_1 + 0x118);
  FUN_10142dd4c(&local_e0,&local_88," Freq < Key");
  FUN_1030cdf18(0,param_2,uVar7,&local_e0);
  if (local_e0 != (int *)0x0) {
    iVar2 = *local_e0;
    *local_e0 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar7 = *(undefined8 *)(param_1 + 0x130);
  FUN_10142dd4c(&local_e8,&local_88," Freq < Env");
  FUN_1030cb214(0,param_2,uVar7,&local_e8);
  if (local_e8 != (int *)0x0) {
    iVar2 = *local_e8;
    *local_e8 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar7 = *(undefined8 *)(param_1 + 0x148);
  FUN_10142dd4c(&local_f0,&local_88," Filter Q");
  piVar3 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  *(undefined ***)piVar3 = &PTR_thunk_FUN_10128edf8_1068c5778;
  piVar3[6] = 0x14;
  *(undefined8 *)(piVar3 + 10) = uVar5;
  *(undefined8 *)(piVar3 + 8) = uVar6;
  piVar3[2] = piVar3[2] + 1;
  local_78 = piVar3;
  FUN_1011cb734(&local_f8);
  FUN_103197830(0,param_2,uVar7,&local_f0,piVar3,&local_f8,0,0);
  if (local_f8 != (int *)0x0) {
    iVar2 = *local_f8;
    *local_f8 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  iVar2 = piVar3[2];
  piVar3[2] = iVar2 + -1;
  if (iVar2 + -1 == 0) {
    FUN_10128eea0(piVar3);
  }
  if (local_f0 != (int *)0x0) {
    iVar2 = *local_f0;
    *local_f0 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar7 = *(undefined8 *)(param_1 + 0x160);
  FUN_10142dd4c(&local_100,&local_88," Attack");
  piVar3 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  *(undefined ***)piVar3 = &PTR_thunk_FUN_10128edf8_1068c5778;
  piVar3[6] = 0x15;
  *(undefined8 *)(piVar3 + 10) = uVar5;
  *(undefined8 *)(piVar3 + 8) = uVar6;
  piVar3[2] = piVar3[2] + 1;
  local_78 = piVar3;
  FUN_1011cb734(&local_108);
  FUN_103197830(0,param_2,uVar7,&local_100,piVar3,&local_108,0,0);
  if (local_108 != (int *)0x0) {
    iVar2 = *local_108;
    *local_108 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  iVar2 = piVar3[2];
  piVar3[2] = iVar2 + -1;
  if (iVar2 + -1 == 0) {
    FUN_10128eea0(piVar3);
  }
  if (local_100 != (int *)0x0) {
    iVar2 = *local_100;
    *local_100 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar7 = *(undefined8 *)(param_1 + 0x178);
  FUN_10142dd4c(&local_110,&local_88," Decay");
  piVar3 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  *(undefined ***)piVar3 = &PTR_thunk_FUN_10128edf8_1068c5778;
  piVar3[6] = 0x16;
  *(undefined8 *)(piVar3 + 10) = uVar5;
  *(undefined8 *)(piVar3 + 8) = uVar6;
  piVar3[2] = piVar3[2] + 1;
  local_78 = piVar3;
  FUN_1011cb734(&local_118);
  FUN_103197830(0x3e4ccccd,param_2,uVar7,&local_110,piVar3,&local_118,0,0);
  if (local_118 != (int *)0x0) {
    iVar2 = *local_118;
    *local_118 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  iVar2 = piVar3[2];
  piVar3[2] = iVar2 + -1;
  if (iVar2 + -1 == 0) {
    FUN_10128eea0(piVar3);
  }
  if (local_110 != (int *)0x0) {
    iVar2 = *local_110;
    *local_110 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar7 = *(undefined8 *)(param_1 + 400);
  FUN_10142dd4c(&local_120,&local_88," Sustain");
  piVar3 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  *(undefined ***)piVar3 = &PTR_thunk_FUN_10128edf8_1068c5778;
  piVar3[6] = 0x17;
  *(undefined8 *)(piVar3 + 10) = uVar5;
  *(undefined8 *)(piVar3 + 8) = uVar6;
  piVar3[2] = piVar3[2] + 1;
  local_78 = piVar3;
  FUN_1011cb734(&local_128);
  FUN_103197830(0,param_2,uVar7,&local_120,piVar3,&local_128,0,0);
  if (local_128 != (int *)0x0) {
    iVar2 = *local_128;
    *local_128 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  iVar2 = piVar3[2];
  piVar3[2] = iVar2 + -1;
  if (iVar2 + -1 == 0) {
    FUN_10128eea0(piVar3);
  }
  if (local_120 != (int *)0x0) {
    iVar2 = *local_120;
    *local_120 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar7 = *(undefined8 *)(param_1 + 0x1a8);
  FUN_10142dd4c(&local_130,&local_88," Release");
  piVar3 = (int *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  *(undefined ***)piVar3 = &PTR_thunk_FUN_10128edf8_1068c5778;
  piVar3[6] = 0x18;
  *(undefined8 *)(piVar3 + 10) = uVar5;
  *(undefined8 *)(piVar3 + 8) = uVar6;
  piVar3[2] = piVar3[2] + 1;
  local_78 = piVar3;
  FUN_1011cb734(&local_138);
  FUN_103197830(0x3e4ccccd,param_2,uVar7,&local_130,piVar3,&local_138,0,0);
  if (local_138 != (int *)0x0) {
    iVar2 = *local_138;
    *local_138 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  iVar2 = piVar3[2];
  piVar3[2] = iVar2 + -1;
  if (iVar2 + -1 == 0) {
    FUN_10128eea0(piVar3);
  }
  if (local_130 != (int *)0x0) {
    iVar2 = *local_130;
    *local_130 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  puVar1 = PTR_CallMemberFunc<&ACollisionNoise::FilterParameter>_10652cb60;
  local_78 = (int *)PTR_CallMemberFunc<&ACollisionNoise::FilterParameter>_10652cb60;
  lStack_70 = param_1;
  FUN_102953a9c(*(undefined8 *)(param_1 + 0x50),0,&local_78);
  local_78 = (int *)puVar1;
  lStack_70 = param_1;
  FUN_102953a9c(*(undefined8 *)(param_1 + 0x58),1,&local_78);
  local_78 = (int *)PTR_CallMemberFunc<&ACollisionNoise::FilterCascades>_10652cb68;
  lStack_70 = param_1;
  FUN_102953514(*(undefined8 *)(param_1 + 0x60),&local_78);
  FUN_102953520(*(undefined8 *)(param_1 + 0x60),*(undefined8 *)(param_1 + 0x50));
  FUN_102953520(*(undefined8 *)(param_1 + 0x60),*(undefined8 *)(param_1 + 0x58));
  uVar5 = *(undefined8 *)(param_1 + 0x60);
  uVar6 = (**(code **)(**(long **)(param_1 + 0xe8) + 0x278))();
  FUN_102953070(uVar5,uVar6);
  uVar5 = *(undefined8 *)(param_1 + 0x60);
  uVar6 = (**(code **)(**(long **)(param_1 + 0x148) + 0x278))();
  FUN_102953070(uVar5,uVar6);
  uVar5 = *(undefined8 *)(param_1 + 0x60);
  uVar6 = (**(code **)(**(long **)(param_1 + 0xd0) + 0x278))();
  FUN_102953070(uVar5,uVar6);
  if (local_88 != (int *)0x0) {
    iVar2 = *local_88;
    *local_88 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (*(long *)PTR____stack_chk_guard_1064f8818 == local_58) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

