
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1030ccacc(long param_1,undefined8 param_2,undefined8 *param_3,undefined8 param_4)

{
  undefined *puVar1;
  int iVar2;
  int iVar3;
  undefined8 uVar4;
  undefined **ppuVar5;
  undefined8 *puVar6;
  long lVar7;
  long lVar8;
  long *plVar9;
  undefined8 uVar10;
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
  undefined8 *local_f8;
  int *local_f0;
  int *local_e8;
  int *local_e0;
  int *local_d8;
  int *local_d0;
  int *local_c8;
  int *local_c0;
  int *local_b8;
  int *local_b0;
  undefined **local_a8;
  undefined8 uStack_a0;
  undefined1 auStack_98 [8];
  undefined ***local_90;
  undefined1 auStack_88 [8];
  undefined1 auStack_80 [8];
  undefined1 auStack_78 [8];
  long local_70;
  
  local_70 = *(long *)PTR____stack_chk_guard_1064f8818;
  uVar4 = *(undefined8 *)(param_1 + 0x58);
  local_b0 = (int *)*param_3;
  if (local_b0 != (int *)0x0) {
    *local_b0 = *local_b0 + 1;
  }
  FUN_10156fa68(uVar4,&local_b0);
  if (local_b0 != (int *)0x0) {
    iVar2 = *local_b0;
    *local_b0 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar4 = *(undefined8 *)(param_1 + 0x70);
  FUN_10142dd4c(&local_b8,param_3," On/Off");
  FUN_1011cb734(&local_c0);
  FUN_1031980a4(uVar4,&local_b8,0,&local_c0);
  if (local_c0 != (int *)0x0) {
    iVar2 = *local_c0;
    *local_c0 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_b8 != (int *)0x0) {
    iVar2 = *local_b8;
    *local_b8 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (((DAT_107026ea0 & 1) == 0) && (iVar2 = ___cxa_guard_acquire(&DAT_107026ea0), iVar2 != 0)) {
    FUN_101427680(&local_a8,"Sine");
    FUN_101427680(&uStack_a0,"Square");
    FUN_101427680(auStack_98,"Triangle");
    FUN_101427680(&local_90,"SawUp");
    FUN_101427680(auStack_88,"SawDown");
    FUN_101427680(auStack_80,"Sample & Hold");
    FUN_101427680(auStack_78,"Random Ramp");
    FUN_1002c29cc(&DAT_107027158,&local_a8,7);
    FUN_100234444(auStack_78);
    FUN_100234444(auStack_80);
    FUN_100234444(auStack_88);
    FUN_100234444(&local_90);
    FUN_100234444(auStack_98);
    FUN_100234444(&uStack_a0);
    FUN_100234444(&local_a8);
    ___cxa_atexit(FUN_1002343c8,&DAT_107027158,0x100000000);
    ___cxa_guard_release(&DAT_107026ea0);
  }
  if (((DAT_107026ea8 & 1) == 0) && (iVar2 = ___cxa_guard_acquire(&DAT_107026ea8), iVar2 != 0)) {
    FUN_101427680(&local_a8,"ModulationSine");
    FUN_101427680(&uStack_a0,"ModulationSquare");
    FUN_101427680(auStack_98,"ModulationTriangle");
    FUN_101427680(&local_90,"ModulationSawUp");
    FUN_101427680(auStack_88,"ModulationSawDown");
    FUN_101427680(auStack_80,"ModulationSHmono");
    FUN_101427680(auStack_78,"ModulationSHrounded");
    FUN_1002c29cc(&DAT_107027170,&local_a8,7);
    FUN_100234444(auStack_78);
    FUN_100234444(auStack_80);
    FUN_100234444(auStack_88);
    FUN_100234444(&local_90);
    FUN_100234444(auStack_98);
    FUN_100234444(&uStack_a0);
    FUN_100234444(&local_a8);
    ___cxa_atexit(FUN_1002343c8,&DAT_107027170,0x100000000);
    ___cxa_guard_release(&DAT_107026ea8);
  }
  uVar4 = *(undefined8 *)(param_1 + 0x88);
  FUN_10142dd4c(&local_c8,param_3," Shape");
  FUN_1026ef060(uVar4,0,&DAT_107027170,&local_c8,1);
  if (local_c8 != (int *)0x0) {
    iVar2 = *local_c8;
    *local_c8 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar4 = *(undefined8 *)(param_1 + 0x88);
  ppuVar5 = (undefined **)FUN_1012d9850(0x20);
  FUN_10143bd04(ppuVar5,&DAT_107027158);
  if (ppuVar5 != (undefined **)0x0) {
    *(int *)(ppuVar5 + 1) = *(int *)(ppuVar5 + 1) + 1;
  }
  local_a8 = ppuVar5;
  FUN_1026fc44c(uVar4,ppuVar5);
  if (ppuVar5 != (undefined **)0x0) {
    iVar2 = *(int *)(ppuVar5 + 1);
    *(int *)(ppuVar5 + 1) = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_10128eea0(ppuVar5);
    }
  }
  uVar4 = *(undefined8 *)(param_1 + 0xa0);
  FUN_10142dd4c(&local_d0,param_3," Retrigger");
  FUN_1011cb734(&local_d8);
  FUN_1031980a4(uVar4,&local_d0,1,&local_d8);
  if (local_d8 != (int *)0x0) {
    iVar2 = *local_d8;
    *local_d8 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_d0 != (int *)0x0) {
    iVar2 = *local_d0;
    *local_d0 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (((DAT_107026eb0 & 1) == 0) && (iVar2 = ___cxa_guard_acquire(&DAT_107026eb0), iVar2 != 0)) {
    FUN_101427680(&local_a8,"Free");
    FUN_101427680(&uStack_a0,"Sync");
    FUN_1002c29cc(&DAT_107027188,&local_a8,2);
    FUN_100234444(&uStack_a0);
    FUN_100234444(&local_a8);
    ___cxa_atexit(FUN_1002343c8,&DAT_107027188,0x100000000);
    ___cxa_guard_release(&DAT_107026eb0);
  }
  if (((DAT_107026eb8 & 1) == 0) && (iVar2 = ___cxa_guard_acquire(&DAT_107026eb8), iVar2 != 0)) {
    FUN_101427680(&local_a8,"ModulationHertz");
    FUN_101427680(&uStack_a0,"ModulationBeat");
    FUN_1002c29cc(&DAT_1070271a0,&local_a8,2);
    FUN_100234444(&uStack_a0);
    FUN_100234444(&local_a8);
    ___cxa_atexit(FUN_1002343c8,&DAT_1070271a0,0x100000000);
    ___cxa_guard_release(&DAT_107026eb8);
  }
  uVar4 = *(undefined8 *)(param_1 + 0xb8);
  FUN_10142dd4c(&local_e0,param_3," Sync");
  FUN_1026ef060(uVar4,0,&DAT_1070271a0,&local_e0,1);
  if (local_e0 != (int *)0x0) {
    iVar2 = *local_e0;
    *local_e0 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar4 = *(undefined8 *)(param_1 + 0xb8);
  ppuVar5 = (undefined **)FUN_1012d9850(0x20);
  FUN_10143bd04(ppuVar5,&DAT_107027188);
  if (ppuVar5 != (undefined **)0x0) {
    *(int *)(ppuVar5 + 1) = *(int *)(ppuVar5 + 1) + 1;
  }
  local_a8 = ppuVar5;
  FUN_1026fc44c(uVar4,ppuVar5);
  if (ppuVar5 != (undefined **)0x0) {
    iVar2 = *(int *)(ppuVar5 + 1);
    *(int *)(ppuVar5 + 1) = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_10128eea0(ppuVar5);
    }
  }
  uVar4 = *(undefined8 *)(param_1 + 0xd0);
  FUN_10142dd4c(&local_e8,param_3," Rate");
  ppuVar5 = (undefined **)FUN_1012d9850(0x30);
  FUN_10128ed98();
  *ppuVar5 = (undefined *)&PTR_thunk_FUN_10128edf8_1068c5778;
  *(undefined4 *)(ppuVar5 + 3) = 0x60;
  puVar1 = _DAT_10561dfd0;
  ppuVar5[5] = _UNK_10561dfd8;
  ppuVar5[4] = puVar1;
  *(int *)(ppuVar5 + 1) = *(int *)(ppuVar5 + 1) + 1;
  local_a8 = ppuVar5;
  FUN_1011cb734(&local_f0);
  FUN_103197830(0x3f000000,param_2,uVar4,&local_e8,ppuVar5,&local_f0,0,0);
  if (local_f0 != (int *)0x0) {
    iVar2 = *local_f0;
    *local_f0 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  iVar2 = *(int *)(ppuVar5 + 1);
  *(int *)(ppuVar5 + 1) = iVar2 + -1;
  if (iVar2 + -1 == 0) {
    FUN_10128eea0(ppuVar5);
  }
  if (local_e8 != (int *)0x0) {
    iVar2 = *local_e8;
    *local_e8 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  local_a8 = (undefined **)PTR__lambda___1__ARemoteable__TRemoteableUpdate__106551c78;
  uStack_a0 = 0;
  FUN_10156934c(*(undefined8 *)(param_1 + 0x100),0xc0000000,&local_a8);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x100),1);
  if (((DAT_107026ec8 & 1) == 0) && (iVar2 = ___cxa_guard_acquire(&DAT_107026ec8), iVar2 != 0)) {
    lVar7 = FUN_1012d9850(0x38);
    iVar2 = FUN_1020ef18c();
    FUN_101577e1c(0,(float)(iVar2 + -1),lVar7,1);
    DAT_107026ec0 = lVar7;
    if (lVar7 != 0) {
      *(int *)(lVar7 + 8) = *(int *)(lVar7 + 8) + 1;
    }
    ___cxa_atexit(FUN_1002483c0,&DAT_107026ec0,0x100000000);
    ___cxa_guard_release(&DAT_107026ec8);
  }
  uVar10 = *(undefined8 *)(param_1 + 0xe8);
  iVar2 = FUN_1020ef18c();
  iVar3 = FUN_1020ee0f4();
  lVar7 = DAT_107026ec0;
  puVar6 = (undefined8 *)FUN_1012d9850(0x38);
  local_90 = &local_a8;
  local_a8 = &PTR_FUN_1068c57f8;
  FUN_10128ed98();
  *puVar6 = &PTR_FUN_106845818;
  uVar4 = 0;
  if (local_90 == (undefined ***)0x0) {
LAB_1030ccf38:
    puVar6[6] = uVar4;
  }
  else {
    if (local_90 != &local_a8) {
      uVar4 = (*(code *)(*local_90)[2])();
      goto LAB_1030ccf38;
    }
    puVar6[6] = puVar6 + 3;
    (*(code *)(*local_90)[3])();
  }
  *(int *)(puVar6 + 1) = *(int *)(puVar6 + 1) + 1;
  local_f8 = puVar6;
  if (local_90 == &local_a8) {
    lVar8 = 0x20;
  }
  else {
    if (local_90 == (undefined ***)0x0) goto LAB_1030ccf8c;
    lVar8 = 0x28;
  }
  (**(code **)((long)*local_90 + lVar8))();
LAB_1030ccf8c:
  FUN_10142dd4c(&local_100,param_3," Synced Rate");
  FUN_1026f0b58(0,(float)(iVar2 + -1),(float)iVar3,uVar10,param_2,lVar7,puVar6,&local_100,2);
  if (local_100 != (int *)0x0) {
    iVar2 = *local_100;
    *local_100 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  iVar2 = *(int *)(puVar6 + 1);
  *(int *)(puVar6 + 1) = iVar2 + -1;
  if (iVar2 + -1 == 0) {
    FUN_10128eea0(puVar6);
  }
  plVar9 = *(long **)(param_1 + 0xe8);
  FUN_10142dd4c(&local_a8,param_3," Sync Rate");
  (**(code **)(*plVar9 + 0x298))(plVar9,&local_a8);
  if (local_a8 != (undefined **)0x0) {
    iVar2 = *(int *)local_a8;
    *(int *)local_a8 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  puVar6 = (undefined8 *)(param_1 + 0xe8);
  uVar4 = (**(code **)(*(long *)*puVar6 + 0x2b0))();
  FUN_1024dd614(uVar4,2);
  uVar4 = (**(code **)(*(long *)*puVar6 + 0x2b0))();
  FUN_1024dd624(uVar4,*(undefined8 *)(param_1 + 0x100));
  uVar4 = FUN_1026f96b0(*puVar6);
  FUN_1024dd614(uVar4,2);
  uVar4 = FUN_1026f96b0(*puVar6);
  iVar2 = FUN_1020ef18c();
  FUN_1025ba00c(0,(float)(iVar2 + -1),uVar4);
  uVar4 = FUN_1026f96b0(*puVar6);
  FUN_1024dd624(uVar4,*(undefined8 *)(param_1 + 0x100));
  FUN_1026f1850(*puVar6,0);
  uVar4 = *(undefined8 *)(param_1 + 0x118);
  FUN_10142dd4c(&local_108,param_3," Rate < Key");
  FUN_1030cdf18(0,param_2,uVar4,&local_108);
  if (local_108 != (int *)0x0) {
    iVar2 = *local_108;
    *local_108 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (((DAT_107026ed8 & 1) == 0) && (iVar2 = ___cxa_guard_acquire(&DAT_107026ed8), iVar2 != 0)) {
    lVar7 = FUN_1012d9850(0x38);
    FUN_101575868(0,0x43b40000,0x3f800000,0x3dcccccd);
    DAT_107026ed0 = lVar7;
    if (lVar7 != 0) {
      *(int *)(lVar7 + 8) = *(int *)(lVar7 + 8) + 1;
    }
    ___cxa_atexit(FUN_1002483c0,&DAT_107026ed0,0x100000000);
    ___cxa_guard_release(&DAT_107026ed8);
  }
  lVar7 = DAT_107026ed0;
  uVar4 = *(undefined8 *)(param_1 + 0x130);
  ppuVar5 = (undefined **)FUN_1012d9850(0x20);
  FUN_10143a894(ppuVar5,0);
  if (ppuVar5 != (undefined **)0x0) {
    *(int *)(ppuVar5 + 1) = *(int *)(ppuVar5 + 1) + 1;
  }
  local_a8 = ppuVar5;
  FUN_10142dd4c(&local_110,param_3," Offset");
  FUN_1026f0b58(0,0x43b40000,0,uVar4,param_2,lVar7,ppuVar5,&local_110,2);
  if (local_110 != (int *)0x0) {
    iVar2 = *local_110;
    *local_110 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (ppuVar5 != (undefined **)0x0) {
    iVar2 = *(int *)(ppuVar5 + 1);
    *(int *)(ppuVar5 + 1) = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_10128eea0(ppuVar5);
    }
  }
  uVar4 = *(undefined8 *)(param_1 + 0x148);
  FUN_10142dd4c(&local_118,param_3," Depth");
  FUN_1011cb734(&local_120);
  FUN_103197830(0x3f000000,param_2,uVar4,&local_118,0,&local_120,0,0);
  if (local_120 != (int *)0x0) {
    iVar2 = *local_120;
    *local_120 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_118 != (int *)0x0) {
    iVar2 = *local_118;
    *local_118 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar4 = *(undefined8 *)(param_1 + 0x160);
  FUN_10142dd4c(&local_128,param_3," Depth < Vel");
  FUN_1030cb214(0,param_2,uVar4,&local_128);
  if (local_128 != (int *)0x0) {
    iVar2 = *local_128;
    *local_128 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar4 = *(undefined8 *)(param_1 + 0x178);
  FUN_10142dd4c(&local_130,param_3," Destination A");
  FUN_10142dd4c(&local_138,param_3," Dest A");
  FUN_10142dd4c(&local_140,param_3," Amount A");
  FUN_10142dd4c(&local_148,param_3," Amt A");
  FUN_1030cac68(uVar4,param_2,&local_130,&local_138,&local_140,&local_148,param_4);
  if (local_148 != (int *)0x0) {
    iVar2 = *local_148;
    *local_148 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_140 != (int *)0x0) {
    iVar2 = *local_140;
    *local_140 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_138 != (int *)0x0) {
    iVar2 = *local_138;
    *local_138 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_130 != (int *)0x0) {
    iVar2 = *local_130;
    *local_130 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar4 = *(undefined8 *)(param_1 + 400);
  FUN_10142dd4c(&local_150,param_3," Destination B");
  FUN_10142dd4c(&local_158,param_3," Dest B");
  FUN_10142dd4c(&local_160,param_3," Amount B");
  FUN_10142dd4c(&local_168,param_3," Amt B");
  FUN_1030cac68(uVar4,param_2,&local_150,&local_158,&local_160,&local_168,param_4);
  if (local_168 != (int *)0x0) {
    iVar2 = *local_168;
    *local_168 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_160 != (int *)0x0) {
    iVar2 = *local_160;
    *local_160 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_158 != (int *)0x0) {
    iVar2 = *local_158;
    *local_158 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_150 != (int *)0x0) {
    iVar2 = *local_150;
    *local_150 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (*(long *)PTR____stack_chk_guard_1064f8818 == local_70) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

