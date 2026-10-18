
undefined8 FUN_1024b0650(short param_1)

{
  char cVar1;
  short sVar2;
  int iVar3;
  uint uVar4;
  long lVar5;
  long lVar6;
  long lVar7;
  undefined8 uVar8;
  size_t sVar9;
  char *pcVar10;
  undefined4 local_ce0;
  uint local_cdc;
  undefined1 local_cd8 [12];
  undefined4 local_ccc;
  undefined1 *local_cc8;
  char *local_cc0;
  undefined8 local_cb8;
  undefined4 *local_ca8;
  char *local_ca0;
  undefined8 local_c98;
  char local_c88 [1024];
  char local_888 [8];
  undefined1 auStack_880 [9];
  char acStack_877 [1007];
  int *local_488 [10];
  undefined1 local_438 [1024];
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_106a33b20;
  lVar5 = _CFBundleGetMainBundle();
  if ((lVar5 == 0) || (lVar5 = _CFBundleCopyResourceURL(lVar5,&cf_ReWire_Mach_O,0,0), lVar5 == 0)) {
    FUN_1024b8500();
LAB_1024b0b6b:
    uVar8 = 0;
  }
  else {
    cVar1 = _CFURLGetFileSystemRepresentation(lVar5,1,local_438,0x400);
    if ((cVar1 == '\0') || (lVar6 = _CFStringCreateWithCString(0,"ReWire.bundle",0x600), lVar6 == 0)
       ) goto LAB_1024b0b6b;
    _CFAutorelease(lVar6);
    lVar7 = _CFURLCreateCopyAppendingPathComponent(0,lVar5,lVar6,1);
    _CFRelease(lVar5);
    if (lVar7 == 0) goto LAB_1024b0b6b;
    lVar5 = _CFBundleCreate(0,lVar7);
    _CFRelease(lVar7);
    if (lVar5 == 0) {
      FUN_1024b8500();
      goto LAB_1024b0b6b;
    }
    local_cdc = _CFBundleGetVersionNumber(lVar5);
    _CFRelease(lVar5);
    sVar2 = _FSFindFolder((int)param_1,0x61737570,1,local_888);
    if ((sVar2 == 0) &&
       (sVar2 = _FSMakeFSRefUnicode(local_888,0x16,L"Propellerhead Software",0xffff,local_c88),
       sVar2 == 0)) {
      FUN_101421a50(local_488,"ReWire");
      uVar8 = FUN_101427810(local_488);
      sVar2 = _FSMakeFSRefUnicode(local_c88,6,uVar8,0xffff,local_c88);
      if ((local_488[0] != (int *)0x0) && (*local_488[0] = *local_488[0] + -1, *local_488[0] == 0))
      {
        FUN_101442b40();
      }
      if (sVar2 == 0) {
        FUN_101421a50(local_488,"ReWire.bundle");
        uVar8 = FUN_101427810(local_488);
        sVar2 = _FSMakeFSRefUnicode(local_c88,0xd,uVar8,0xffff,local_888);
        if ((local_488[0] != (int *)0x0) && (*local_488[0] = *local_488[0] + -1, *local_488[0] == 0)
           ) {
          FUN_101442b40();
        }
        if ((sVar2 == 0) && (lVar5 = _CFURLCreateFromFSRef(0,local_888), lVar5 != 0)) {
          lVar7 = _CFBundleCreate(0,lVar5);
          _CFRelease(lVar5);
          if (lVar7 != 0) {
            uVar4 = _CFBundleGetVersionNumber();
            _CFRelease(lVar7);
            if (local_cdc <= uVar4) {
              uVar8 = std::chrono::system_clock::now();
              FUN_10410fff0(local_888,2,uVar8);
              cVar1 = FUN_10410c530(local_888);
              if (cVar1 != '\0') {
                uVar8 = FUN_104108bf0(local_888,"InstallPropellerheadDlls: ");
                uVar8 = FUN_104108bf0(uVar8,"ReWire.bundle");
                uVar8 = FUN_104108bf0(uVar8," (");
                pcVar10 = "kUserDomain";
                if (param_1 == -0x7ffd) {
                  pcVar10 = "kLocalDomain";
                }
                uVar8 = FUN_104108bf0(uVar8,pcVar10);
                FUN_104108bf0(uVar8,") is already installed and up to date, no action required");
              }
              FUN_104108a10(local_888);
              if (*(long *)PTR____stack_chk_guard_106a33b20 == local_38) {
                return 1;
              }
              goto LAB_1024b0cad;
            }
          }
        }
      }
    }
    uVar8 = std::chrono::system_clock::now();
    FUN_10410fff0(local_888,2,uVar8);
    cVar1 = FUN_10410c530(local_888);
    if (cVar1 != '\0') {
      uVar8 = FUN_104108bf0(local_888,"InstallPropellerheadDlls: ");
      uVar8 = FUN_104108bf0(uVar8,"ReWire.bundle");
      uVar8 = FUN_104108bf0(uVar8," (");
      pcVar10 = "kUserDomain";
      if (param_1 == -0x7ffd) {
        pcVar10 = "kLocalDomain";
      }
      uVar8 = FUN_104108bf0(uVar8,pcVar10);
      FUN_104108bf0(uVar8,") is either missing or not up to date, will install");
    }
    FUN_104108a10(local_888);
    sVar2 = _FSFindFolder((int)param_1,0x61737570,1,local_488);
    if (sVar2 != 0) goto LAB_1024b0b6b;
    iVar3 = _CFStringGetLength(lVar6);
    iVar3 = _FSRefMakePath(local_488,local_888,0x3e0 - iVar3);
    if (iVar3 != 0) goto LAB_1024b0b6b;
    sVar9 = _strlen(local_888);
    *(undefined8 *)(local_888 + sVar9) = s__Propellerhead_Software__10612f211._0_8_;
    *(ulong *)(auStack_880 + sVar9) =
         CONCAT71(s__Propellerhead_Software__10612f211._9_7_,s__Propellerhead_Software__10612f211[8]
                 );
    *(ulong *)(auStack_880 + sVar9 + 1) =
         CONCAT17(s__Propellerhead_Software__10612f211[0x10],
                  s__Propellerhead_Software__10612f211._9_7_);
    *(undefined8 *)(acStack_877 + sVar9) = s__Propellerhead_Software__10612f211._17_8_;
    sVar9 = _strlen(local_888);
    builtin_strncpy(local_888 + sVar9,"ReWire",7);
    _snprintf(local_c88,0x400,"%s/%s",local_888,"ReWire.bundle");
    local_ce0 = 0x66722d;
    local_ca8 = &local_ce0;
    local_c98 = 0;
    local_ca0 = local_c88;
    local_ccc = FUN_101180aa0("/bin/rm",&local_ca8);
    uVar8 = std::chrono::system_clock::now();
    FUN_10410fff0(&local_cc8,2,uVar8);
    cVar1 = FUN_10410c530(&local_cc8);
    if (cVar1 != '\0') {
      uVar8 = FUN_104108bf0(&local_cc8,"InstallPropellerheadDlls: ran helper tool: \'/bin/rm\' ");
      uVar8 = FUN_104108bf0(uVar8,local_ca8);
      uVar8 = FUN_104108bf0(uVar8," ");
      uVar8 = FUN_104108bf0(uVar8,local_ca0);
      uVar8 = FUN_104108bf0(uVar8,"   status: ");
      FUN_1024b8680(uVar8,&local_ccc);
    }
    FUN_104108a10(&local_cc8);
    cVar1 = FUN_1024b89a0(local_ccc);
    if (cVar1 == '\0') goto LAB_1024b0b6b;
    local_cb8 = 0;
    local_cc8 = local_438;
    local_cc0 = local_888;
    local_ccc = FUN_101180aa0("/usr/bin/ditto",&local_cc8);
    uVar8 = std::chrono::system_clock::now();
    FUN_10410fff0(local_cd8,2,uVar8);
    cVar1 = FUN_10410c530(local_cd8);
    if (cVar1 != '\0') {
      uVar8 = FUN_104108bf0(local_cd8,
                            "InstallPropellerheadDlls: ran helper tool: \'/usr/bin/ditto\' ");
      uVar8 = FUN_104108bf0(uVar8,local_cc8);
      uVar8 = FUN_104108bf0(uVar8," ");
      uVar8 = FUN_104108bf0(uVar8,local_cc0);
      uVar8 = FUN_104108bf0(uVar8,"   status: ");
      FUN_1024b8680(uVar8,&local_ccc);
    }
    FUN_104108a10(local_cd8);
    uVar8 = FUN_1024b89a0(local_ccc);
  }
  if (*(long *)PTR____stack_chk_guard_106a33b20 == local_38) {
    return uVar8;
  }
LAB_1024b0cad:
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

