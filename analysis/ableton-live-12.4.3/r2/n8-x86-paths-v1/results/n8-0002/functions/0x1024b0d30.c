
undefined8 FUN_1024b0d30(short param_1,undefined1 *param_2)

{
  ulong uVar1;
  char cVar2;
  short sVar3;
  int iVar4;
  long lVar5;
  long lVar6;
  size_t sVar7;
  undefined8 uVar8;
  undefined1 local_1908 [12];
  undefined4 local_18fc;
  char local_18f8 [8];
  undefined8 uStack_18f0;
  char acStack_18e5 [4];
  char acStack_18e1 [4];
  char acStack_18dd [997];
  char local_14f8 [1024];
  undefined1 local_10f8 [80];
  undefined1 local_10a8 [80];
  undefined8 ****local_1058;
  char *local_1050;
  char *local_1048;
  undefined8 local_1040;
  char local_1038 [4];
  char acStack_1034 [4];
  char acStack_1030 [4];
  char acStack_102c [4];
  undefined7 uStack_1028;
  char local_c38 [1024];
  undefined8 ****local_838;
  char *local_830;
  undefined8 local_828;
  char local_438 [1032];
  long local_30;
  
  local_30 = 0x1024b0d45;
  lVar5 = ____chkstk_darwin();
  lVar5 = -lVar5;
  local_30 = *(long *)PTR____stack_chk_guard_106a33b20;
  *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b0d61;
  lVar6 = _CFBundleGetMainBundle();
  if (lVar6 == 0) {
LAB_1024b1225:
    *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b122a;
    FUN_1024b8500();
    *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b122f;
    uVar8 = std::chrono::system_clock::now();
    *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b1243;
    FUN_10410fff0(local_438,4,uVar8);
    *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b124f;
    cVar2 = FUN_10410c530(local_438);
    if (cVar2 != '\0') {
      *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b1266;
      FUN_104108bf0(local_438,"InstallPropellerheadDlls: \'Ableton Live Engine.bundle\' not found");
    }
LAB_1024b1266:
    *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b1272;
    FUN_104108a10(local_438);
LAB_1024b1272:
    uVar8 = 0;
  }
  else {
    *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b0d7d;
    lVar6 = _CFBundleCopyResourceURL(lVar6,&cf_AbletonLiveEngine_bundle,0,0);
    if (lVar6 == 0) goto LAB_1024b1225;
    *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b0d98;
    cVar2 = _CFURLGetFSRef(lVar6,local_10a8);
    *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b0da6;
    _CFRelease(lVar6);
    if (cVar2 == '\0') goto LAB_1024b1225;
    *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b0dc9;
    sVar3 = _FSFindFolder((int)param_1,0x61737570,1,local_10f8);
    if (sVar3 != 0) goto LAB_1024b1272;
    *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b0dea;
    iVar4 = _FSRefMakePath(local_10f8,local_14f8,0x3c5);
    if (iVar4 != 0) goto LAB_1024b1272;
    *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b0e0b;
    _strcpy(local_18f8,local_14f8);
    *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b0e13;
    sVar7 = _strlen(local_18f8);
    *(undefined8 *)(local_18f8 + sVar7) = s__Propellerhead_Software_ReWire_10612f323._0_8_;
    *(ulong *)((long)&uStack_18f0 + sVar7) =
         CONCAT17(s__Propellerhead_Software_ReWire_10612f323[0xf],
                  s__Propellerhead_Software_ReWire_10612f323._8_7_);
    *(undefined4 *)((long)&uStack_18f0 + sVar7 + 7) =
         s__Propellerhead_Software_ReWire_10612f323._15_4_;
    *(undefined4 *)(acStack_18e5 + sVar7) = s__Propellerhead_Software_ReWire_10612f323._19_4_;
    *(undefined4 *)(acStack_18e1 + sVar7) = s__Propellerhead_Software_ReWire_10612f323._23_4_;
    *(undefined4 *)(acStack_18dd + sVar7) = s__Propellerhead_Software_ReWire_10612f323._27_4_;
    uVar1 = (ulong)local_1058 >> 0x10;
    local_1058 = (undefined8 ****)CONCAT62((uint6)uVar1 & 0xffffffffff00,0x662d);
    *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b0e68;
    _snprintf(local_438,0x400,"%s/%s",local_14f8,"Ableton Live Engine");
    local_838 = &local_1058;
    local_828 = 0;
    *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b0e9b;
    local_830 = local_438;
    local_1038 = (char  [4])FUN_101180aa0("/bin/rm",&local_838);
    *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b0ea6;
    uVar8 = std::chrono::system_clock::now();
    *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b0eba;
    FUN_10410fff0(local_c38,2,uVar8);
    *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b0ec6;
    cVar2 = FUN_10410c530(local_c38);
    if (cVar2 != '\0') {
      *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b0edd;
      uVar8 = FUN_104108bf0(local_c38,"SDeleteAlias: ran helper tool: \'/bin/rm\' ");
      *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b0eec;
      uVar8 = FUN_104108bf0(uVar8,local_838);
      *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b0efb;
      uVar8 = FUN_104108bf0(uVar8," ");
      *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b0f0a;
      uVar8 = FUN_104108bf0(uVar8,local_830);
      *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b0f19;
      uVar8 = FUN_104108bf0(uVar8,"   status: ");
      *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b0f28;
      FUN_1024b8680(uVar8,local_1038);
    }
    *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b0f34;
    FUN_104108a10(local_c38);
    *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b0f5f;
    _snprintf(local_438,0x400,"%s/%s",local_18f8,"Ableton Live Engine_64");
    *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b0f78;
    iVar4 = _FSPathMakeRef(local_438,&local_838,local_c38);
    if ((iVar4 == 0) && (local_c38[0] == '\0')) {
      *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b0fa4;
      sVar3 = _FSResolveAliasFile(&local_838,1,local_1038,&local_1058);
      if ((sVar3 == 0) && ((char)local_1058 != '\0')) {
        *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b0fc5;
        sVar3 = _FSCompareFSRefs(&local_838,local_10a8);
        if (sVar3 == 0) {
          *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b12e0;
          uVar8 = std::chrono::system_clock::now();
          *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b12f4;
          FUN_10410fff0(local_438,2,uVar8);
          *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b1300;
          cVar2 = FUN_10410c530(local_438);
          if (cVar2 != '\0') {
            *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b1317;
            uVar8 = FUN_104108bf0(local_438,"InstallPropellerheadDlls: ");
            *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b1326;
            uVar8 = FUN_104108bf0(uVar8,local_18f8);
            *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b1335;
            uVar8 = FUN_104108bf0(uVar8,"/");
            *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b1344;
            uVar8 = FUN_104108bf0(uVar8,"Ableton Live Engine_64");
            *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b1353;
            FUN_104108bf0(uVar8," is already installed and up to date, no action required");
          }
          *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b135f;
          FUN_104108a10(local_438);
          if (*(long *)PTR____stack_chk_guard_106a33b20 == local_30) {
            return 1;
          }
          goto LAB_1024b1375;
        }
      }
    }
    *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b0fd3;
    uVar8 = std::chrono::system_clock::now();
    *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b0fe7;
    FUN_10410fff0(local_438,2,uVar8);
    *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b0ff3;
    cVar2 = FUN_10410c530(local_438);
    if (cVar2 != '\0') {
      *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b100a;
      uVar8 = FUN_104108bf0(local_438,"InstallPropellerheadDlls: ");
      *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b1019;
      uVar8 = FUN_104108bf0(uVar8,local_18f8);
      *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b1028;
      uVar8 = FUN_104108bf0(uVar8,"/");
      *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b1037;
      uVar8 = FUN_104108bf0(uVar8,"Ableton Live Engine_64");
      *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b1046;
      FUN_104108bf0(uVar8," is either missing or not up to date, will install");
    }
    *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b1052;
    FUN_104108a10(local_438);
    if (param_2 != (undefined1 *)0x0) {
      *param_2 = 1;
    }
    *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b105f;
    lVar6 = _CFBundleGetMainBundle();
    if (lVar6 == 0) {
LAB_1024b1298:
      *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b129d;
      FUN_1024b8500();
      *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b12a2;
      uVar8 = std::chrono::system_clock::now();
      *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b12b6;
      FUN_10410fff0(local_438,4,uVar8);
      *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b12c2;
      cVar2 = FUN_10410c530(local_438);
      if (cVar2 != '\0') {
        *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b12d9;
        FUN_104108bf0(local_438,"InstallPropellerheadDlls: \'MakeAlias\' not found");
      }
      goto LAB_1024b1266;
    }
    *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b107b;
    lVar6 = _CFBundleCopyResourceURL(lVar6,&cf_MakeAlias,0,0);
    if (lVar6 == 0) goto LAB_1024b1298;
    *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b10a0;
    cVar2 = _CFURLGetFileSystemRepresentation(lVar6,1,local_438,0x400);
    *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b10ab;
    _CFRelease(lVar6);
    if (cVar2 == '\0') goto LAB_1024b1272;
    *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b10cf;
    iVar4 = _FSRefMakePath(local_10a8,&local_838,0x400);
    if (iVar4 != 0) goto LAB_1024b1272;
    *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b10e6;
    _strcpy(local_c38,local_18f8);
    uStack_1028 = 0x34365f656e69;
    local_1038[0] = s_Ableton_Live_Engine_64_10612f356[0];
    local_1038[1] = s_Ableton_Live_Engine_64_10612f356[1];
    local_1038[2] = s_Ableton_Live_Engine_64_10612f356[2];
    local_1038[3] = s_Ableton_Live_Engine_64_10612f356[3];
    acStack_1034[0] = s_Ableton_Live_Engine_64_10612f356[4];
    acStack_1034[1] = s_Ableton_Live_Engine_64_10612f356[5];
    acStack_1034[2] = s_Ableton_Live_Engine_64_10612f356[6];
    acStack_1034[3] = s_Ableton_Live_Engine_64_10612f356[7];
    acStack_1030[0] = s_Ableton_Live_Engine_64_10612f356[8];
    acStack_1030[1] = s_Ableton_Live_Engine_64_10612f356[9];
    acStack_1030[2] = s_Ableton_Live_Engine_64_10612f356[10];
    acStack_1030[3] = s_Ableton_Live_Engine_64_10612f356[0xb];
    acStack_102c[0] = s_Ableton_Live_Engine_64_10612f356[0xc];
    acStack_102c[1] = s_Ableton_Live_Engine_64_10612f356[0xd];
    acStack_102c[2] = s_Ableton_Live_Engine_64_10612f356[0xe];
    acStack_102c[3] = s_Ableton_Live_Engine_64_10612f356[0xf];
    local_1048 = local_1038;
    local_1040 = 0;
    *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b113f;
    local_1058 = &local_838;
    local_1050 = local_c38;
    local_18fc = FUN_101180aa0(local_438,&local_1058);
    *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b114a;
    uVar8 = std::chrono::system_clock::now();
    *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b115e;
    FUN_10410fff0(local_1908,2,uVar8);
    *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b116a;
    cVar2 = FUN_10410c530(local_1908);
    if (cVar2 != '\0') {
      *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b1185;
      uVar8 = FUN_104108bf0(local_1908,"InstallPropellerheadDlls: ran helper tool: \'");
      *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b1194;
      uVar8 = FUN_104108bf0(uVar8,local_438);
      *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b11a3;
      uVar8 = FUN_104108bf0(uVar8,"\' ");
      *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b11b2;
      uVar8 = FUN_104108bf0(uVar8,local_1058);
      *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b11c1;
      uVar8 = FUN_104108bf0(uVar8," ");
      *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b11d0;
      uVar8 = FUN_104108bf0(uVar8,local_1050);
      *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b11df;
      uVar8 = FUN_104108bf0(uVar8," ");
      *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b11ee;
      uVar8 = FUN_104108bf0(uVar8,local_1048);
      *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b11fd;
      uVar8 = FUN_104108bf0(uVar8,"   status: ");
      *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b120c;
      FUN_1024b8680(uVar8,&local_18fc);
    }
    *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b1218;
    FUN_104108a10(local_1908);
    *(undefined8 *)((long)&local_30 + lVar5) = 0x1024b1223;
    uVar8 = FUN_1024b89a0(local_18fc);
  }
  if (*(long *)PTR____stack_chk_guard_106a33b20 == local_30) {
    return uVar8;
  }
LAB_1024b1375:
                    /* WARNING: Subroutine does not return */
  *(undefined **)((long)&local_30 + lVar5) = &UNK_1024b137a;
  ___stack_chk_fail();
}

