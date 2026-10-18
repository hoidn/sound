
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1002cc484(long *param_1)

{
  int iVar1;
  int iVar2;
  code *pcVar3;
  code *pcVar4;
  long lVar5;
  ulong extraout_x1;
  ulong extraout_x1_00;
  ulong extraout_x1_01;
  ulong extraout_x1_02;
  ulong extraout_x1_03;
  ulong extraout_x1_04;
  ulong extraout_x1_05;
  long local_78;
  code *local_70;
  undefined8 uStack_68;
  undefined8 uStack_60;
  undefined8 uStack_58;
  code *local_50;
  long *plStack_48;
  undefined8 uStack_40;
  undefined8 uStack_38;
  
  iVar2 = FUN_1011b59ec();
  if ((iVar2 != 2) && (iVar2 = FUN_1011b59ec(), iVar2 != 1)) {
    plStack_48 = (long *)_UNK_1055d8138;
    local_50 = _DAT_1055d8130;
    uStack_38 = _UNK_1055d8148;
    uStack_40 = _DAT_1055d8140;
    FUN_1011aeb80(&local_50);
    if ((extraout_x1 & 1) == 0) {
      uStack_68 = _UNK_1055d7db4;
      local_70 = _DAT_1055d7dac;
      uStack_58 = _UNK_1055d7dc4;
      uStack_60 = _DAT_1055d7dbc;
      FUN_1011aeb80(&local_70);
      if ((extraout_x1_00 & 1) == 0) {
        local_50 = (code *)PTR_CallMemberFunc<&ALiveApp::StartAppAddOns>_106535390;
        plStack_48 = param_1;
        pcVar3 = (code *)FUN_1012d9850(0x60);
        FUN_1017de0e0(pcVar3,&local_50,"AddOns");
        if (pcVar3 != (code *)0x0) {
          *(int *)(pcVar3 + 8) = *(int *)(pcVar3 + 8) + 1;
        }
        local_78 = 0;
        local_70 = pcVar3;
        FUN_1018558c8(param_1,&local_70);
        if (local_70 != (code *)0x0) {
          iVar2 = *(int *)(local_70 + 8);
          *(int *)(local_70 + 8) = iVar2 + -1;
          if (iVar2 + -1 == 0) {
            FUN_10128eea0();
          }
        }
      }
    }
  }
  local_50 = FUN_1002fcc0c;
  plStack_48 = (long *)0x0;
  pcVar3 = (code *)FUN_1012d9850(0x60);
  FUN_1017de0e0(pcVar3,&local_50,"CloseSplashScreen");
  if (pcVar3 != (code *)0x0) {
    *(int *)(pcVar3 + 8) = *(int *)(pcVar3 + 8) + 1;
  }
  local_78 = 0;
  local_70 = pcVar3;
  FUN_1018558c8(param_1,&local_70);
  if (local_70 != (code *)0x0) {
    iVar2 = *(int *)(local_70 + 8);
    *(int *)(local_70 + 8) = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  local_50 = (code *)PTR_CallMemberFunc<&ALiveApp::OpenSecondWindowOnStartupHook>_1065353c0;
  plStack_48 = param_1;
  pcVar3 = (code *)FUN_1012d9850(0x60);
  FUN_1017de0e0(pcVar3,&local_50,"OpenSecondWindowOnStartup");
  if (pcVar3 != (code *)0x0) {
    *(int *)(pcVar3 + 8) = *(int *)(pcVar3 + 8) + 1;
  }
  local_78 = 0;
  local_70 = pcVar3;
  FUN_1018558c8(param_1,&local_70);
  if (local_70 != (code *)0x0) {
    iVar2 = *(int *)(local_70 + 8);
    *(int *)(local_70 + 8) = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  iVar2 = FUN_101505540();
  if (iVar2 == 2) {
    plStack_48 = (long *)_UNK_1055d7db4;
    local_50 = _DAT_1055d7dac;
    uStack_38 = _UNK_1055d7dc4;
    uStack_40 = _DAT_1055d7dbc;
    FUN_1011aeb80(&local_50);
    if ((extraout_x1_01 & 1) == 0) goto LAB_1002cc7c8;
  }
  plStack_48 = (long *)_UNK_1055d8158;
  local_50 = _DAT_1055d8150;
  uStack_38 = _UNK_1055d8168;
  uStack_40 = _DAT_1055d8160;
  FUN_1011aeb80(&local_50);
  if ((extraout_x1_02 & 1) == 0) {
    plStack_48 = (long *)_UNK_1055d8178;
    local_50 = _DAT_1055d8170;
    uStack_38 = _UNK_1055d8188;
    uStack_40 = _DAT_1055d8180;
    FUN_1011aeb80(&local_50);
    if ((extraout_x1_03 & 1) == 0) {
      plStack_48 = (long *)_UNK_1055d8138;
      local_50 = _DAT_1055d8130;
      uStack_38 = _UNK_1055d8148;
      uStack_40 = _DAT_1055d8140;
      FUN_1011aeb80(&local_50);
      if ((extraout_x1_04 & 1) != 0) {
        local_50 = (code *)PTR_CallStaticFunc<&APackingTool::SDeferredRun>_106536820;
        plStack_48 = (long *)0x0;
        pcVar3 = (code *)FUN_1012d9850(0x60);
        FUN_1017de0e0(pcVar3,&local_50,"PackingTool");
        if (pcVar3 != (code *)0x0) {
          *(int *)(pcVar3 + 8) = *(int *)(pcVar3 + 8) + 1;
        }
        local_78 = 0;
        local_70 = pcVar3;
        FUN_1018558c8(param_1,&local_70);
        if (local_70 != (code *)0x0) {
          iVar2 = *(int *)(local_70 + 8);
          *(int *)(local_70 + 8) = iVar2 + -1;
          if (iVar2 + -1 == 0) {
            FUN_10128eea0();
          }
        }
      }
    }
    else {
      local_50 = (code *)PTR_CallStaticFunc<&APackingTool::SConvertToMidiTracks>_106536828;
      plStack_48 = (long *)0x0;
      pcVar3 = (code *)FUN_1012d9850(0x60);
      FUN_1017de0e0(pcVar3,&local_50,"PackingToolConvertToMidiTracks");
      if (pcVar3 != (code *)0x0) {
        *(int *)(pcVar3 + 8) = *(int *)(pcVar3 + 8) + 1;
      }
      local_78 = 0;
      local_70 = pcVar3;
      FUN_1018558c8(param_1,&local_70);
      if (local_70 != (code *)0x0) {
        iVar2 = *(int *)(local_70 + 8);
        *(int *)(local_70 + 8) = iVar2 + -1;
        if (iVar2 + -1 == 0) {
          FUN_10128eea0();
        }
      }
    }
  }
  else {
    local_50 = (code *)PTR_CallStaticFunc<&APackingTool::SFreeze>_106536830;
    plStack_48 = (long *)0x0;
    pcVar3 = (code *)FUN_1012d9850(0x60);
    FUN_1017de0e0(pcVar3,&local_50,"PackingToolFreeze");
    if (pcVar3 != (code *)0x0) {
      *(int *)(pcVar3 + 8) = *(int *)(pcVar3 + 8) + 1;
    }
    local_78 = 0;
    local_70 = pcVar3;
    FUN_1018558c8(param_1,&local_70);
    if (local_70 != (code *)0x0) {
      iVar2 = *(int *)(local_70 + 8);
      *(int *)(local_70 + 8) = iVar2 + -1;
      if (iVar2 + -1 == 0) {
        FUN_10128eea0();
      }
    }
  }
LAB_1002cc7c8:
  local_50 = (code *)PTR_CallMemberFunc<&ALiveApp::StartWebConnector>_106535398;
  plStack_48 = param_1;
  pcVar3 = (code *)FUN_1012d9850(0x60);
  FUN_1017de0e0(pcVar3,&local_50,"StartWebConnector");
  if (pcVar3 != (code *)0x0) {
    *(int *)(pcVar3 + 8) = *(int *)(pcVar3 + 8) + 1;
  }
  local_78 = 0;
  local_70 = pcVar3;
  FUN_1018558c8(param_1,&local_70);
  if (local_70 != (code *)0x0) {
    iVar2 = *(int *)(local_70 + 8);
    *(int *)(local_70 + 8) = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  local_50 = thunk_FUN_101780940;
  plStack_48 = (long *)0x0;
  pcVar3 = (code *)FUN_1012d9850(0x60);
  FUN_1017de0e0(pcVar3,&local_50,"WriteUsageData");
  if (pcVar3 != (code *)0x0) {
    *(int *)(pcVar3 + 8) = *(int *)(pcVar3 + 8) + 1;
  }
  local_78 = 0;
  local_70 = pcVar3;
  FUN_1018558c8(param_1,&local_70);
  if (local_70 != (code *)0x0) {
    iVar2 = *(int *)(local_70 + 8);
    *(int *)(local_70 + 8) = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  iVar2 = FUN_1011b59ec();
  if (iVar2 != 2) {
    local_50 = (code *)PTR_CallMemberFunc<&ALiveApp::StartAppIndex>_106535388;
    plStack_48 = param_1;
    pcVar3 = (code *)FUN_1012d9850(0x60);
    FUN_1017de0e0(pcVar3,&local_50,"StartIndex");
    if (pcVar3 != (code *)0x0) {
      *(int *)(pcVar3 + 8) = *(int *)(pcVar3 + 8) + 1;
    }
    local_78 = 0;
    local_70 = pcVar3;
    FUN_1018558c8(param_1,&local_70);
    if (local_70 != (code *)0x0) {
      iVar2 = *(int *)(local_70 + 8);
      *(int *)(local_70 + 8) = iVar2 + -1;
      if (iVar2 + -1 == 0) {
        FUN_10128eea0();
      }
    }
  }
  pcVar3 = (code *)FUN_1012d9850(0x58);
  thunk_FUN_100320ba0();
  if (pcVar3 != (code *)0x0) {
    *(int *)(pcVar3 + 8) = *(int *)(pcVar3 + 8) + 1;
  }
  local_70 = (code *)0x0;
  local_50 = pcVar3;
  FUN_1018558c8(param_1,&local_50);
  if (local_50 != (code *)0x0) {
    iVar2 = *(int *)(local_50 + 8);
    *(int *)(local_50 + 8) = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  local_50 = (code *)PTR_CallStaticFunc<&ALiveApp::SFileSystemEndUpdate>_106536840;
  plStack_48 = (long *)0x0;
  pcVar3 = (code *)FUN_1012d9850(0x60);
  FUN_1017de0e0(pcVar3,&local_50,"FileSystemEndUpdate");
  if (pcVar3 != (code *)0x0) {
    *(int *)(pcVar3 + 8) = *(int *)(pcVar3 + 8) + 1;
  }
  local_78 = 0;
  local_70 = pcVar3;
  FUN_1018558c8(param_1,&local_70);
  if (local_70 != (code *)0x0) {
    iVar2 = *(int *)(local_70 + 8);
    *(int *)(local_70 + 8) = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  FUN_1002cd978(&local_70,param_1);
  pcVar3 = (code *)FUN_1012d9850(0x48);
  *(undefined8 *)(pcVar3 + 0x40) = 0;
  *(undefined8 *)(pcVar3 + 0x28) = 0;
  *(undefined8 *)(pcVar3 + 0x20) = 0;
  *(undefined8 *)(pcVar3 + 0x38) = 0;
  *(undefined8 *)(pcVar3 + 0x30) = 0;
  *(undefined8 *)(pcVar3 + 8) = 0;
  *(undefined8 *)pcVar3 = 0;
  *(undefined8 *)(pcVar3 + 0x18) = 0;
  *(undefined8 *)(pcVar3 + 0x10) = 0;
  FUN_1017ddee0();
  *(undefined ***)pcVar3 = &PTR_thunk_FUN_10128edf8_1065a0c58;
  *(int *)(pcVar3 + 8) = *(int *)(pcVar3 + 8) + 1;
  local_78 = 0;
  local_50 = pcVar3;
  FUN_1018558c8(param_1,&local_50);
  if (local_50 != (code *)0x0) {
    iVar2 = *(int *)(local_50 + 8);
    *(int *)(local_50 + 8) = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  pcVar4 = (code *)FUN_1012d9850(0x50);
  pcVar3 = local_70;
  FUN_100322068(pcVar4,local_70);
  if (pcVar4 != (code *)0x0) {
    *(int *)(pcVar4 + 8) = *(int *)(pcVar4 + 8) + 1;
  }
  local_78 = 0;
  local_50 = pcVar4;
  FUN_1018558c8(param_1,&local_50);
  if (local_50 != (code *)0x0) {
    iVar2 = *(int *)(local_50 + 8);
    *(int *)(local_50 + 8) = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  FUN_1011db938(&local_50);
  iVar2 = (**(code **)(*plStack_48 + 0x20))();
  if (local_50 != (code *)0x0) {
    iVar1 = *(int *)(local_50 + 8);
    *(int *)(local_50 + 8) = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  if (iVar2 != 0) {
    local_50 = (code *)PTR_CallMemberFunc<&ALiveApp::ShowFirstTimeContent>_1065353a0;
    plStack_48 = param_1;
    lVar5 = FUN_1012d9850(0x60);
    FUN_1017de0e0(lVar5,&local_50,"ShowFirstTimeContent");
    if (lVar5 != 0) {
      *(int *)(lVar5 + 8) = *(int *)(lVar5 + 8) + 1;
    }
    local_78 = lVar5;
    FUN_1018558c8(param_1,&local_78);
    if (local_78 != 0) {
      iVar2 = *(int *)(local_78 + 8) + -1;
      *(int *)(local_78 + 8) = iVar2;
      if (iVar2 == 0) {
        FUN_10128eea0();
      }
    }
  }
  pcVar4 = (code *)FUN_1012d9850(0x50);
  FUN_1017ddee0();
  *(undefined ***)pcVar4 = &PTR_FUN_1065a0bd8;
  *(code **)(pcVar4 + 0x48) = pcVar3;
  if (pcVar3 != (code *)0x0) {
    *(int *)(pcVar3 + 8) = *(int *)(pcVar3 + 8) + 1;
  }
  *(int *)(pcVar4 + 8) = *(int *)(pcVar4 + 8) + 1;
  local_78 = 0;
  local_50 = pcVar4;
  FUN_1018558c8(param_1,&local_50);
  if (local_50 != (code *)0x0) {
    iVar2 = *(int *)(local_50 + 8);
    *(int *)(local_50 + 8) = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  local_50 = (code *)PTR_CallMemberFunc<&ALiveApp::InitializeContentLibraryHook>_1065353b8;
  plStack_48 = param_1;
  lVar5 = FUN_1012d9850(0x60);
  FUN_1017de0e0(lVar5,&local_50,"InitializeContentLibrary");
  if (lVar5 != 0) {
    *(int *)(lVar5 + 8) = *(int *)(lVar5 + 8) + 1;
  }
  local_78 = lVar5;
  FUN_1018558c8(param_1,&local_78);
  if (local_78 != 0) {
    iVar2 = *(int *)(local_78 + 8) + -1;
    *(int *)(local_78 + 8) = iVar2;
    if (iVar2 == 0) {
      FUN_10128eea0();
    }
  }
  local_50 = (code *)PTR_CallMemberFunc<&ALiveApp::StartLibraryRescanHook>_1065353a8;
  plStack_48 = param_1;
  lVar5 = FUN_1012d9850(0x60);
  FUN_1017de0e0(lVar5,&local_50,"StartLibraryRescan");
  if (lVar5 != 0) {
    *(int *)(lVar5 + 8) = *(int *)(lVar5 + 8) + 1;
  }
  local_78 = lVar5;
  FUN_1018558c8(param_1,&local_78);
  if (local_78 != 0) {
    iVar2 = *(int *)(local_78 + 8) + -1;
    *(int *)(local_78 + 8) = iVar2;
    if (iVar2 == 0) {
      FUN_10128eea0();
    }
  }
  local_50 = (code *)
             PTR_CallStaticFunc<&NDownloadablePacks::SInitializeDownloadablePackListHook>_106536838;
  plStack_48 = (long *)0x0;
  lVar5 = FUN_1012d9850(0x60);
  FUN_1017de0e0(lVar5,&local_50,"FetchDownloadablePackListFromWeb");
  if (lVar5 != 0) {
    *(int *)(lVar5 + 8) = *(int *)(lVar5 + 8) + 1;
  }
  local_78 = lVar5;
  FUN_1018558c8(param_1,&local_78);
  if (local_78 != 0) {
    iVar2 = *(int *)(local_78 + 8) + -1;
    *(int *)(local_78 + 8) = iVar2;
    if (iVar2 == 0) {
      FUN_10128eea0();
    }
  }
  local_50 = thunk_FUN_1011a7760;
  plStack_48 = (long *)0x0;
  lVar5 = FUN_1012d9850(0x60);
  FUN_1017de0e0(lVar5,&local_50,"EndAuthorizationSession");
  if (lVar5 != 0) {
    *(int *)(lVar5 + 8) = *(int *)(lVar5 + 8) + 1;
  }
  local_78 = lVar5;
  FUN_1018558c8(param_1,&local_78);
  if (local_78 != 0) {
    iVar2 = *(int *)(local_78 + 8) + -1;
    *(int *)(local_78 + 8) = iVar2;
    if (iVar2 == 0) {
      FUN_10128eea0();
    }
  }
  plStack_48 = (long *)_UNK_1055d7dd4;
  local_50 = _DAT_1055d7dcc;
  uStack_38 = _UNK_1055d7de4;
  uStack_40 = _DAT_1055d7ddc;
  FUN_1011aeb80(&local_50);
  if ((extraout_x1_05 & 1) != 0) {
    local_50 = FUN_1002fcd18;
    plStack_48 = (long *)0x0;
    lVar5 = FUN_1012d9850(0x60);
    FUN_1017de0e0(lVar5,&local_50,"Log hotkeys");
    if (lVar5 != 0) {
      *(int *)(lVar5 + 8) = *(int *)(lVar5 + 8) + 1;
    }
    local_78 = lVar5;
    FUN_1018558c8(param_1,&local_78);
    if (local_78 != 0) {
      iVar2 = *(int *)(local_78 + 8) + -1;
      *(int *)(local_78 + 8) = iVar2;
      if (iVar2 == 0) {
        FUN_10128eea0();
      }
    }
  }
  iVar2 = FUN_1011b59ec();
  if (iVar2 == 2) {
    local_50 = FUN_1002fd394;
    plStack_48 = (long *)0x0;
    lVar5 = FUN_1012d9850(0x60);
    FUN_1017de0e0(lVar5,&local_50,"Install acceptance test runner");
    if (lVar5 != 0) {
      *(int *)(lVar5 + 8) = *(int *)(lVar5 + 8) + 1;
    }
    local_78 = lVar5;
    FUN_1018558c8(param_1,&local_78);
    if (local_78 != 0) {
      iVar2 = *(int *)(local_78 + 8) + -1;
      *(int *)(local_78 + 8) = iVar2;
      if (iVar2 == 0) {
        FUN_10128eea0();
      }
    }
  }
  if (pcVar3 != (code *)0x0) {
    iVar2 = *(int *)(pcVar3 + 8);
    *(int *)(pcVar3 + 8) = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_10128eea0(pcVar3);
    }
  }
  return;
}

