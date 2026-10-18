
void FUN_1027c81e0(undefined8 *param_1)

{
  long *plVar1;
  int *piVar2;
  long *plVar3;
  long lVar4;
  long *plVar5;
  char cVar6;
  undefined4 uVar7;
  int iVar8;
  char *pcVar9;
  undefined8 uVar10;
  undefined8 uVar11;
  long *plVar12;
  long *plVar13;
  int iVar14;
  char *local_40;
  undefined8 *local_38;
  
  FUN_10154d810();
  *param_1 = &PTR_FUN_106d38258;
  FUN_10147d5c0(param_1);
  *param_1 = &PTR_FUN_106d38738;
  plVar1 = param_1 + 0xb;
  param_1[0xb] = 0;
  pcVar9 = (char *)FUN_1012bd9b0(0xc0);
  FUN_1027c3900(pcVar9);
  if (pcVar9 != (char *)0x0) {
    *(int *)(pcVar9 + 8) = *(int *)(pcVar9 + 8) + 1;
  }
  local_40 = pcVar9;
  FUN_101479bf0(pcVar9);
  if (*plVar1 != 0) {
    piVar2 = (int *)(*plVar1 + 8);
    *piVar2 = *piVar2 + -1;
    if (*piVar2 == 0) {
      FUN_1012716c0();
      pcVar9 = local_40;
    }
  }
  param_1[0xb] = pcVar9;
  param_1[0xf] = 0;
  param_1[0x10] = 0;
  FUN_102397600(&local_40);
  FUN_1014fa480(param_1 + 0x11,local_40);
  if (local_40 != (char *)0x0) {
    piVar2 = (int *)(local_40 + 8);
    *piVar2 = *piVar2 + -1;
    if (*piVar2 == 0) {
      FUN_1012716c0();
    }
  }
  param_1[0x11] = &PTR_FUN_106d3afa0;
  FUN_1023bdc10(&local_40);
  FUN_1014fa480(param_1 + 0x14,local_40);
  if (local_40 != (char *)0x0) {
    piVar2 = (int *)(local_40 + 8);
    *piVar2 = *piVar2 + -1;
    if (*piVar2 == 0) {
      FUN_1012716c0();
    }
  }
  param_1[0x14] = &PTR_FUN_106d3b030;
  param_1[0x17] = 0;
  pcVar9 = (char *)FUN_1012bdaa0(0xa0);
  FUN_1025e6250(pcVar9);
  if (pcVar9 != (char *)0x0) {
    *(int *)(pcVar9 + 8) = *(int *)(pcVar9 + 8) + 1;
  }
  lVar4 = param_1[0x17];
  local_40 = pcVar9;
  if (lVar4 != 0) {
    piVar2 = (int *)(lVar4 + 8);
    *piVar2 = *piVar2 + -1;
    if (*piVar2 == 0) {
      FUN_1012716c0();
    }
  }
  param_1[0x17] = pcVar9;
  param_1[0x18] = 0;
  plVar13 = param_1 + 0x1a;
  param_1[0x1a] = 0;
  FUN_1024136a0(&local_40);
  if (*plVar13 != 0) {
    piVar2 = (int *)(*plVar13 + 8);
    *piVar2 = *piVar2 + -1;
    if (*piVar2 == 0) {
      FUN_1012716c0();
    }
  }
  param_1[0x1a] = local_40;
  plVar12 = param_1 + 0x1b;
  param_1[0x1b] = 0;
  FUN_102412a20(&local_40);
  if (*plVar12 != 0) {
    piVar2 = (int *)(*plVar12 + 8);
    *piVar2 = *piVar2 + -1;
    if (*piVar2 == 0) {
      FUN_1012716c0();
    }
  }
  param_1[0x1b] = local_40;
  param_1[0x1c] = 0;
  pcVar9 = (char *)FUN_1012bdaa0(0x78);
  FUN_1024c23c0(pcVar9);
  if (pcVar9 != (char *)0x0) {
    *(int *)(pcVar9 + 8) = *(int *)(pcVar9 + 8) + 1;
  }
  local_40 = pcVar9;
  if (param_1[0x1c] != 0) {
    piVar2 = (int *)(param_1[0x1c] + 8);
    *piVar2 = *piVar2 + -1;
    if (*piVar2 == 0) {
      FUN_1012716c0();
    }
  }
  param_1[0x1c] = pcVar9;
  plVar3 = param_1 + 0x1d;
  param_1[0x1d] = 0;
  FUN_1024b6190(&local_40);
  if (*plVar3 != 0) {
    piVar2 = (int *)(*plVar3 + 8);
    *piVar2 = *piVar2 + -1;
    if (*piVar2 == 0) {
      FUN_1012716c0();
    }
  }
  *plVar3 = (long)local_40;
  FUN_1026c2d90(&local_40);
  if (param_1[0x18] != 0) {
    piVar2 = (int *)(param_1[0x18] + 8);
    *piVar2 = *piVar2 + -1;
    if (*piVar2 == 0) {
      FUN_1012716c0();
    }
  }
  param_1[0x18] = local_40;
  (**(code **)(*(long *)param_1[0x12] + 0x1c8))();
  param_1[0x19] = 0;
  param_1[0xc] = 0;
  param_1[0xd] = 0;
  param_1[0xe] = 0;
  FUN_10147d5c0(param_1);
  uVar10 = std::chrono::system_clock::now();
  FUN_10410fff0(&local_40,2,uVar10);
  cVar6 = FUN_10410c530(&local_40);
  if (cVar6 != '\0') {
    uVar10 = FUN_104108bf0(&local_40,"LSongAgent");
    FUN_104108bf0(uVar10,": Begin Constructing");
  }
  FUN_104108a10(&local_40);
  local_40 = "(All)";
  local_38 = (undefined8 *)((ulong)local_38 & 0xffffffffffffff00);
  (**(code **)(*(long *)*plVar1 + 0x280))((long *)*plVar1,&local_40);
  FUN_10244a3d0(*plVar1,*plVar13,*plVar12);
  *(undefined8 **)(param_1[0xb] + 0x90) = param_1;
  local_40 = "Audio In";
  local_38 = (undefined8 *)((ulong)local_38 & 0xffffffffffffff00);
  FUN_10245da30(param_1[0x1a],&local_40,0,1);
  local_40 = "Audio Out";
  local_38 = (undefined8 *)((ulong)local_38 & 0xffffffffffffff00);
  FUN_10245da30(*plVar12,&local_40,0,1);
  plVar5 = (long *)*plVar3;
  uVar10 = FUN_10244a5b0(*plVar1);
  uVar11 = FUN_10244a5b0(*plVar1);
  uVar7 = FUN_101a6a980(uVar11);
  (**(code **)(*plVar5 + 400))(plVar5,uVar10,uVar7);
  FUN_10245ddc0(*plVar1,*plVar13);
  FUN_10245ddc0(*plVar1,*plVar12);
  iVar14 = 0;
  while( true ) {
    iVar8 = (**(code **)(*(long *)*plVar3 + 0x1a8))();
    plVar13 = (long *)*plVar1;
    if (iVar8 <= iVar14) break;
    plVar12 = (long *)(**(code **)(*(long *)*plVar3 + 0x1b0))((long *)*plVar3,iVar14);
    uVar10 = (**(code **)(*plVar12 + 0x1c8))(plVar12);
    FUN_10245ddc0(plVar13,uVar10);
    lVar4 = *plVar1;
    plVar13 = (long *)(**(code **)(*(long *)*plVar3 + 0x1b0))((long *)*plVar3,iVar14);
    uVar10 = (**(code **)(*plVar13 + 0x1d0))(plVar13);
    FUN_10245ddc0(lVar4,uVar10);
    iVar14 = iVar14 + 1;
  }
  (**(code **)(*plVar13 + 0x290))(plVar13);
  cVar6 = FUN_101a69490();
  if (cVar6 == '\0') {
    FUN_1027c8a90(param_1 + 0x10);
    lVar4 = param_1[0x10];
    uVar10 = FUN_10244a5b0(*plVar1);
    *(undefined8 **)(lVar4 + 0x30) = param_1;
    FUN_102418310(lVar4,uVar10);
    (**(code **)(*(long *)param_1[0x12] + 0x1d8))((long *)param_1[0x12],param_1[0x10]);
  }
  else {
    uVar10 = std::chrono::system_clock::now();
    FUN_10410fff0(&local_40,2,uVar10);
    cVar6 = FUN_10410c530(&local_40);
    if (cVar6 != '\0') {
      uVar10 = FUN_104108bf0(&local_40,"LSongAgent");
      FUN_104108bf0(uVar10,": Constructing: ReWire Device");
    }
    FUN_104108a10(&local_40);
  }
  FUN_102449180(*plVar1);
  uVar10 = FUN_101ac77d0(0x70);
  FUN_101baca30(uVar10);
  param_1[0xe] = uVar10;
  local_40 = PTR_CallMemberFunc<&LSongAgent::ShowLostMidiSyncBoxAndDisableSync>_106a65810;
  local_38 = param_1;
  FUN_101bacd10(uVar10,&local_40);
  uVar10 = FUN_101ac77d0(0x38);
  FUN_101ba0930(uVar10);
  param_1[0xc] = uVar10;
  uVar10 = FUN_101ac77d0(0x38);
  FUN_101baa510(uVar10);
  param_1[0xd] = uVar10;
  uVar10 = FUN_101ac77d0(0x20);
  FUN_101babb80(uVar10);
  param_1[0x19] = uVar10;
  uVar10 = FUN_1023bdd30();
  FUN_1023d0f40(uVar10,param_1[0xc]);
  uVar10 = FUN_1023bdd30();
  FUN_1023d0f80(uVar10,param_1[0xd]);
  FUN_101baa940(param_1[0xd],FUN_1027dca70,FUN_1027dcaa0,FUN_1027dcad0);
  FUN_1025e6260(param_1[0x17],*plVar1);
  *(undefined1 *)(param_1 + 10) = 0;
  DAT_10752f900 = param_1;
  uVar10 = std::chrono::system_clock::now();
  FUN_10410fff0(&local_40,2,uVar10);
  cVar6 = FUN_10410c530(&local_40);
  if (cVar6 != '\0') {
    uVar10 = FUN_104108bf0(&local_40,"LSongAgent");
    FUN_104108bf0(uVar10,": End Constructing");
  }
  FUN_104108a10(&local_40);
  return;
}

