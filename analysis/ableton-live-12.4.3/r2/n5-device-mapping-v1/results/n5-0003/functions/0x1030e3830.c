
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1030e3830(long param_1)

{
  undefined *puVar1;
  int iVar2;
  int iVar3;
  undefined **ppuVar4;
  undefined8 *puVar5;
  long lVar6;
  long lVar7;
  undefined8 uVar8;
  long *plVar9;
  undefined8 uVar10;
  int *local_d0;
  int *local_c8;
  int *local_c0;
  int *local_b8;
  undefined8 *local_b0;
  int *local_a8;
  int *local_a0;
  int *local_98;
  undefined **local_90;
  undefined8 uStack_88;
  undefined1 auStack_80 [8];
  undefined ***local_78;
  undefined1 auStack_70 [8];
  undefined1 auStack_68 [8];
  undefined1 auStack_60 [8];
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_1064f8818;
  FUN_10319285c(*(undefined8 *)(param_1 + 0x490),"LFO On/Off",0,0);
  if (((DAT_107026fd0 & 1) == 0) && (iVar2 = ___cxa_guard_acquire(&DAT_107026fd0), iVar2 != 0)) {
    FUN_101427680(&local_90,"Sine");
    FUN_101427680(&uStack_88,"Square");
    FUN_101427680(auStack_80,"Triangle");
    FUN_101427680(&local_78,"SawUp");
    FUN_101427680(auStack_70,"SawDown");
    FUN_101427680(auStack_68,"Sample & Hold");
    FUN_101427680(auStack_60,"Random Ramp");
    FUN_1002c29cc(&DAT_107027278,&local_90,7);
    FUN_100234444(auStack_60);
    FUN_100234444(auStack_68);
    FUN_100234444(auStack_70);
    FUN_100234444(&local_78);
    FUN_100234444(auStack_80);
    FUN_100234444(&uStack_88);
    FUN_100234444(&local_90);
    ___cxa_atexit(FUN_1002343c8,&DAT_107027278,0x100000000);
    ___cxa_guard_release(&DAT_107026fd0);
  }
  if (((DAT_107026fd8 & 1) == 0) && (iVar2 = ___cxa_guard_acquire(&DAT_107026fd8), iVar2 != 0)) {
    FUN_101427680(&local_90,"ModulationSine");
    FUN_101427680(&uStack_88,"ModulationSquare");
    FUN_101427680(auStack_80,"ModulationTriangle");
    FUN_101427680(&local_78,"ModulationSawUp");
    FUN_101427680(auStack_70,"ModulationSawDown");
    FUN_101427680(auStack_68,"ModulationSHmono");
    FUN_101427680(auStack_60,"ModulationSHrounded");
    FUN_1002c29cc(&DAT_107027290,&local_90,7);
    FUN_100234444(auStack_60);
    FUN_100234444(auStack_68);
    FUN_100234444(auStack_70);
    FUN_100234444(&local_78);
    FUN_100234444(auStack_80);
    FUN_100234444(&uStack_88);
    FUN_100234444(&local_90);
    ___cxa_atexit(FUN_1002343c8,&DAT_107027290,0x100000000);
    ___cxa_guard_release(&DAT_107026fd8);
  }
  uVar8 = *(undefined8 *)(param_1 + 0x4a8);
  FUN_101427680(&local_98,"LFO Shape");
  FUN_1026ef060(uVar8,0,&DAT_107027290,&local_98,1);
  if (local_98 != (int *)0x0) {
    iVar2 = *local_98;
    *local_98 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar8 = *(undefined8 *)(param_1 + 0x4a8);
  ppuVar4 = (undefined **)FUN_1012d9850(0x20);
  FUN_10143bd04(ppuVar4,&DAT_107027278);
  if (ppuVar4 != (undefined **)0x0) {
    *(int *)(ppuVar4 + 1) = *(int *)(ppuVar4 + 1) + 1;
  }
  local_90 = ppuVar4;
  FUN_1026fc44c(uVar8,ppuVar4);
  if (ppuVar4 != (undefined **)0x0) {
    iVar2 = *(int *)(ppuVar4 + 1);
    *(int *)(ppuVar4 + 1) = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_10128eea0(ppuVar4);
    }
  }
  if (((DAT_107026fe0 & 1) == 0) && (iVar2 = ___cxa_guard_acquire(&DAT_107026fe0), iVar2 != 0)) {
    FUN_101427680(&local_90,"Free");
    FUN_101427680(&uStack_88,"Sync");
    FUN_1002c29cc(&DAT_1070272a8,&local_90,2);
    FUN_100234444(&uStack_88);
    FUN_100234444(&local_90);
    ___cxa_atexit(FUN_1002343c8,&DAT_1070272a8,0x100000000);
    ___cxa_guard_release(&DAT_107026fe0);
  }
  if (((DAT_107026fe8 & 1) == 0) && (iVar2 = ___cxa_guard_acquire(&DAT_107026fe8), iVar2 != 0)) {
    FUN_101427680(&local_90,"ModulationHertz");
    FUN_101427680(&uStack_88,"ModulationBeat");
    FUN_1002c29cc(&DAT_1070272c0,&local_90,2);
    FUN_100234444(&uStack_88);
    FUN_100234444(&local_90);
    ___cxa_atexit(FUN_1002343c8,&DAT_1070272c0,0x100000000);
    ___cxa_guard_release(&DAT_107026fe8);
  }
  uVar8 = *(undefined8 *)(param_1 + 0x4c0);
  FUN_101427680(&local_a0,"LFO Sync");
  FUN_1026ef060(uVar8,0,&DAT_1070272c0,&local_a0,1);
  if (local_a0 != (int *)0x0) {
    iVar2 = *local_a0;
    *local_a0 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar8 = *(undefined8 *)(param_1 + 0x4c0);
  ppuVar4 = (undefined **)FUN_1012d9850(0x20);
  FUN_10143bd04(ppuVar4,&DAT_1070272a8);
  if (ppuVar4 != (undefined **)0x0) {
    *(int *)(ppuVar4 + 1) = *(int *)(ppuVar4 + 1) + 1;
  }
  local_90 = ppuVar4;
  FUN_1026fc44c(uVar8,ppuVar4);
  if (ppuVar4 != (undefined **)0x0) {
    iVar2 = *(int *)(ppuVar4 + 1);
    *(int *)(ppuVar4 + 1) = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_10128eea0(ppuVar4);
    }
  }
  if (((DAT_107026ff0 & 1) == 0) && (iVar2 = ___cxa_guard_acquire(&DAT_107026ff0), iVar2 != 0)) {
    FUN_101427680(&local_90,"Phase");
    FUN_101427680(&uStack_88,"Spin");
    FUN_1002c29cc(&DAT_1070272d8,&local_90,2);
    FUN_100234444(&uStack_88);
    FUN_100234444(&local_90);
    ___cxa_atexit(FUN_1002343c8,&DAT_1070272d8,0x100000000);
    ___cxa_guard_release(&DAT_107026ff0);
  }
  if (((DAT_107026ff8 & 1) == 0) && (iVar2 = ___cxa_guard_acquire(&DAT_107026ff8), iVar2 != 0)) {
    FUN_101427680(&local_90,"Phi");
    FUN_101427680(&uStack_88,"Spin");
    FUN_1002c29cc(&DAT_1070272f0,&local_90,2);
    FUN_100234444(&uStack_88);
    FUN_100234444(&local_90);
    ___cxa_atexit(FUN_1002343c8,&DAT_1070272f0,0x100000000);
    ___cxa_guard_release(&DAT_107026ff8);
  }
  uVar8 = *(undefined8 *)(param_1 + 0x520);
  FUN_101427680(&local_a8,"LFO Stereo Mode");
  FUN_1026ef060(uVar8,0,&DAT_1070272f0,&local_a8,1);
  if (local_a8 != (int *)0x0) {
    iVar2 = *local_a8;
    *local_a8 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar8 = *(undefined8 *)(param_1 + 0x520);
  ppuVar4 = (undefined **)FUN_1012d9850(0x20);
  FUN_10143bd04(ppuVar4,&DAT_1070272d8);
  if (ppuVar4 != (undefined **)0x0) {
    *(int *)(ppuVar4 + 1) = *(int *)(ppuVar4 + 1) + 1;
  }
  local_90 = ppuVar4;
  FUN_1026fc44c(uVar8,ppuVar4);
  if (ppuVar4 != (undefined **)0x0) {
    iVar2 = *(int *)(ppuVar4 + 1);
    *(int *)(ppuVar4 + 1) = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_10128eea0(ppuVar4);
    }
  }
  FUN_1026faa9c(*(undefined8 *)(param_1 + 0x520),1);
  uVar8 = *(undefined8 *)(param_1 + 0x4d8);
  ppuVar4 = (undefined **)FUN_1012d9850(0x30);
  FUN_10128ed98();
  *ppuVar4 = (undefined *)&PTR_thunk_FUN_10128edf8_1068c5b48;
  *(undefined4 *)(ppuVar4 + 3) = 0x14;
  puVar1 = _DAT_10561dfd0;
  ppuVar4[5] = _UNK_10561dfd8;
  ppuVar4[4] = puVar1;
  *(int *)(ppuVar4 + 1) = *(int *)(ppuVar4 + 1) + 1;
  local_90 = ppuVar4;
  FUN_103192720(0x3f000000,param_1,uVar8,"LFO Rate",ppuVar4,0,0);
  iVar2 = *(int *)(ppuVar4 + 1);
  *(int *)(ppuVar4 + 1) = iVar2 + -1;
  if (iVar2 + -1 == 0) {
    FUN_10128eea0(ppuVar4);
  }
  local_90 = (undefined **)PTR__lambda___1__ARemoteable__TRemoteableUpdate__106551c78;
  uStack_88 = 0;
  FUN_10156934c(*(undefined8 *)(param_1 + 0x508),0xc0000000,&local_90);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x508),1);
  if (((DAT_107027008 & 1) == 0) && (iVar2 = ___cxa_guard_acquire(&DAT_107027008), iVar2 != 0)) {
    lVar6 = FUN_1012d9850(0x38);
    iVar2 = FUN_1020ef18c();
    FUN_101577e1c(0,(float)(iVar2 + -1),lVar6,1);
    DAT_107027000 = lVar6;
    if (lVar6 != 0) {
      *(int *)(lVar6 + 8) = *(int *)(lVar6 + 8) + 1;
    }
    ___cxa_atexit(FUN_1002483c0,&DAT_107027000,0x100000000);
    ___cxa_guard_release(&DAT_107027008);
  }
  uVar10 = *(undefined8 *)(param_1 + 0x4f0);
  iVar2 = FUN_1020ef18c();
  iVar3 = FUN_1020ee0f4();
  lVar6 = DAT_107027000;
  puVar5 = (undefined8 *)FUN_1012d9850(0x38);
  local_78 = &local_90;
  local_90 = &PTR_FUN_1068c5bc8;
  FUN_10128ed98();
  *puVar5 = &PTR_FUN_106845818;
  uVar8 = 0;
  if (local_78 == (undefined ***)0x0) {
LAB_1030e3c04:
    puVar5[6] = uVar8;
  }
  else {
    if (local_78 != &local_90) {
      uVar8 = (*(code *)(*local_78)[2])();
      goto LAB_1030e3c04;
    }
    puVar5[6] = puVar5 + 3;
    (*(code *)(*local_78)[3])();
  }
  *(int *)(puVar5 + 1) = *(int *)(puVar5 + 1) + 1;
  local_b0 = puVar5;
  if (local_78 == &local_90) {
    lVar7 = 0x20;
  }
  else {
    if (local_78 == (undefined ***)0x0) goto LAB_1030e3c58;
    lVar7 = 0x28;
  }
  (**(code **)((long)*local_78 + lVar7))();
LAB_1030e3c58:
  FUN_101427680(&local_b8,"LFO Synced Rate");
  FUN_1026f0b58(0,(float)(iVar2 + -1),(float)iVar3,uVar10,param_1,lVar6,puVar5,&local_b8,2);
  if (local_b8 != (int *)0x0) {
    iVar2 = *local_b8;
    *local_b8 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  iVar2 = *(int *)(puVar5 + 1);
  *(int *)(puVar5 + 1) = iVar2 + -1;
  if (iVar2 + -1 == 0) {
    FUN_10128eea0(puVar5);
  }
  plVar9 = *(long **)(param_1 + 0x4f0);
  FUN_101427680(&local_90,"LFO Sync Rate");
  (**(code **)(*plVar9 + 0x298))(plVar9,&local_90);
  if (local_90 != (undefined **)0x0) {
    iVar2 = *(int *)local_90;
    *(int *)local_90 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar8 = (**(code **)(**(long **)(param_1 + 0x4f0) + 0x2b0))();
  FUN_1024dd614(uVar8,2);
  puVar5 = (undefined8 *)(param_1 + 0x4f0);
  uVar8 = (**(code **)(*(long *)*puVar5 + 0x2b0))();
  FUN_1024dd624(uVar8,*(undefined8 *)(param_1 + 0x508));
  uVar8 = FUN_1026f96b0(*puVar5);
  FUN_1024dd614(uVar8,2);
  uVar8 = FUN_1026f96b0(*puVar5);
  iVar2 = FUN_1020ef18c();
  FUN_1025ba00c(0,(float)(iVar2 + -1),uVar8);
  uVar8 = FUN_1026f96b0(*puVar5);
  FUN_1024dd624(uVar8,*(undefined8 *)(param_1 + 0x508));
  FUN_1026f1850(*puVar5,0);
  if (((DAT_107027018 & 1) == 0) && (iVar2 = ___cxa_guard_acquire(&DAT_107027018), iVar2 != 0)) {
    lVar6 = FUN_1012d9850(0x38);
    FUN_101575868(0,0x3f000000,0x3c23d70a,0x3c23d70a);
    DAT_107027010 = lVar6;
    if (lVar6 != 0) {
      *(int *)(lVar6 + 8) = *(int *)(lVar6 + 8) + 1;
    }
    ___cxa_atexit(FUN_1002483c0,&DAT_107027010,0x100000000);
    ___cxa_guard_release(&DAT_107027018);
  }
  lVar6 = DAT_107027010;
  uVar8 = *(undefined8 *)(param_1 + 0x538);
  ppuVar4 = (undefined **)FUN_1012d9850(0x28);
  FUN_101437d10(ppuVar4,0,1);
  if (ppuVar4 != (undefined **)0x0) {
    *(int *)(ppuVar4 + 1) = *(int *)(ppuVar4 + 1) + 1;
  }
  local_90 = ppuVar4;
  FUN_101427680(&local_c0,"LFO Spin");
  FUN_1026f0b58(0,0x3f000000,0,uVar8,param_1,lVar6,ppuVar4,&local_c0,2);
  if (local_c0 != (int *)0x0) {
    iVar2 = *local_c0;
    *local_c0 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (ppuVar4 != (undefined **)0x0) {
    iVar2 = *(int *)(ppuVar4 + 1);
    *(int *)(ppuVar4 + 1) = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_10128eea0(ppuVar4);
    }
  }
  plVar9 = *(long **)(param_1 + 0x538);
  FUN_101427680(&local_90,"Spin");
  (**(code **)(*plVar9 + 0x298))(plVar9,&local_90);
  if (local_90 != (undefined **)0x0) {
    iVar2 = *(int *)local_90;
    *(int *)local_90 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (((DAT_107027028 & 1) == 0) && (iVar2 = ___cxa_guard_acquire(&DAT_107027028), iVar2 != 0)) {
    lVar6 = FUN_1012d9850(0x38);
    FUN_101575868(0,0x43b40000,0x3f800000,0x3dcccccd);
    DAT_107027020 = lVar6;
    if (lVar6 != 0) {
      *(int *)(lVar6 + 8) = *(int *)(lVar6 + 8) + 1;
    }
    ___cxa_atexit(FUN_1002483c0,&DAT_107027020,0x100000000);
    ___cxa_guard_release(&DAT_107027028);
  }
  lVar6 = DAT_107027020;
  uVar8 = *(undefined8 *)(param_1 + 0x550);
  ppuVar4 = (undefined **)FUN_1012d9850(0x20);
  FUN_10143a894(ppuVar4,0);
  if (ppuVar4 != (undefined **)0x0) {
    *(int *)(ppuVar4 + 1) = *(int *)(ppuVar4 + 1) + 1;
  }
  local_90 = ppuVar4;
  FUN_101427680(&local_c8,"LFO Phase");
  FUN_1026f0b58(0,0x43b40000,0x43340000,uVar8,param_1,lVar6,ppuVar4,&local_c8,2);
  if (local_c8 != (int *)0x0) {
    iVar2 = *local_c8;
    *local_c8 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (ppuVar4 != (undefined **)0x0) {
    iVar2 = *(int *)(ppuVar4 + 1);
    *(int *)(ppuVar4 + 1) = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_10128eea0(ppuVar4);
    }
  }
  plVar9 = *(long **)(param_1 + 0x550);
  FUN_101427680(&local_90,"Phase");
  (**(code **)(*plVar9 + 0x298))(plVar9,&local_90);
  if (local_90 != (undefined **)0x0) {
    iVar2 = *(int *)local_90;
    *(int *)local_90 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  lVar6 = DAT_107027020;
  uVar8 = *(undefined8 *)(param_1 + 0x568);
  ppuVar4 = (undefined **)FUN_1012d9850(0x20);
  FUN_10143a894(ppuVar4,0);
  if (ppuVar4 != (undefined **)0x0) {
    *(int *)(ppuVar4 + 1) = *(int *)(ppuVar4 + 1) + 1;
  }
  local_90 = ppuVar4;
  FUN_101427680(&local_d0,"LFO Offset");
  FUN_1026f0b58(0,0x43b40000,0,uVar8,param_1,lVar6,ppuVar4,&local_d0,2);
  if (local_d0 != (int *)0x0) {
    iVar2 = *local_d0;
    *local_d0 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (ppuVar4 != (undefined **)0x0) {
    iVar2 = *(int *)(ppuVar4 + 1);
    *(int *)(ppuVar4 + 1) = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_10128eea0(ppuVar4);
    }
  }
  plVar9 = *(long **)(param_1 + 0x568);
  FUN_101427680(&local_90,"Offset");
  (**(code **)(*plVar9 + 0x298))(plVar9,&local_90);
  if (local_90 != (undefined **)0x0) {
    iVar2 = *(int *)local_90;
    *(int *)local_90 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  FUN_103192720(0,param_1,*(undefined8 *)(param_1 + 0x580),"LFO Amount",0,0,0);
  if (*(long *)PTR____stack_chk_guard_1064f8818 == local_58) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

