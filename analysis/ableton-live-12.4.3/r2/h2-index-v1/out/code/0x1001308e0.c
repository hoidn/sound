// 0x1001308e0 entry state=exported-with-warnings body_bytes=3220 warnings=8 chunk=chunk-00052.jsonl

/* WARNING: Removing unreachable block (ram,0x000100131170) */
/* WARNING: Removing unreachable block (ram,0x000100130b90) */
/* WARNING: Removing unreachable block (ram,0x000100130a2c) */
/* WARNING: Removing unreachable block (ram,0x000100130a9c) */
/* WARNING: Removing unreachable block (ram,0x0001001311a4) */

undefined8 entry(undefined8 param_1,undefined8 param_2)

{
  size_t sVar1;
  undefined8 *puVar2;
  byte bVar3;
  undefined4 uVar4;
  code *pcVar5;
  char cVar6;
  int iVar7;
  int iVar8;
  undefined8 uVar9;
  long *plVar10;
  undefined *puVar11;
  long lVar12;
  undefined ***pppuVar13;
  ulong uVar14;
  char *pcVar15;
  undefined **ppuVar16;
  undefined8 *puVar17;
  undefined ***pppuVar18;
  undefined8 *puVar19;
  undefined **local_490;
  undefined8 uStack_488;
  undefined8 local_480;
  undefined8 uStack_478;
  undefined8 uStack_470;
  undefined8 uStack_468;
  long local_460;
  undefined8 uStack_458;
  undefined8 uStack_450;
  undefined8 uStack_448;
  undefined8 local_440;
  undefined8 uStack_438;
  undefined8 uStack_430;
  undefined8 uStack_428;
  undefined8 local_420;
  undefined8 uStack_418;
  undefined8 uStack_410;
  undefined8 uStack_408;
  undefined8 local_400;
  undefined7 local_3f0;
  undefined4 uStack_3e9;
  undefined1 local_3e5;
  char local_3d9;
  undefined **local_3d8;
  undefined4 local_3d0;
  undefined1 local_3cc;
  char local_3c1;
  undefined **local_3c0;
  undefined **ppuStack_3b8;
  undefined8 local_3b0;
  undefined **local_3a8 [2];
  undefined1 auStack_398 [8];
  long local_390;
  undefined1 auStack_380 [8];
  undefined8 local_378;
  undefined1 auStack_368 [8];
  undefined8 local_360;
  void *local_350;
  void *local_348;
  undefined1 auStack_338 [360];
  undefined1 auStack_1d0 [360];
  undefined1 auStack_68 [8];
  
  FUN_1001a3704(auStack_68);
  uVar4 = DAT_100ba4908;
  thunk_FUN_1001c0d6c(auStack_1d0,"Ableton","Index","12.4.3","1.0",1,DAT_100ba4908);
  FUN_1001c1b9c(auStack_1d0);
  thunk_FUN_1001c0d6c(auStack_338,"Ableton","Live","12.4.3","12.0",1,uVar4);
  FUN_1001e5190(auStack_338);
  FUN_1001b1f08(&local_3c0,param_1,param_2);
  FUN_100131790(&local_490);
  uVar9 = s_options_file_100c1c873._0_8_;
  local_3c1 = '\f';
  local_3d0 = 0x656c6966;
  local_3d8 = (undefined **)s_options_file_100c1c873._0_8_;
  local_3cc = 0;
  FUN_1001b2b18(local_3a8,&local_3c0,&local_490,0,&local_3d8);
  if (local_3c1 < '\0') {
    operator_delete(local_3d8);
  }
  FUN_10014b72c(&local_490);
  if (local_3c0 != (undefined **)0x0) {
    for (; ppuStack_3b8 != local_3c0; ppuStack_3b8 = ppuStack_3b8 + -3) {
    }
    ppuStack_3b8 = local_3c0;
    operator_delete(local_3c0);
  }
  FUN_1001bef10();
  FUN_1001a8224(&local_350);
  local_490 = (undefined **)0x0;
  uStack_488 = (undefined **)0x0;
  local_480 = 0;
  FUN_1001af998(local_3a8,0,&local_490);
  if (local_490 != (undefined **)0x0) {
    for (; uStack_488 != local_490; uStack_488 = uStack_488 + -3) {
    }
    uStack_488 = local_490;
    operator_delete(local_490);
  }
  FUN_1001a917c();
  FUN_100228758(&local_490,param_1,param_2);
  FUN_1001e5198(&local_3d8);
  local_3d9 = '\v';
  local_3f0 = (undefined7)s_Indexer_txt_100c1c880._0_8_;
  uStack_3e9._0_1_ = SUB81(s_Indexer_txt_100c1c880._0_8_,7);
  uStack_3e9 = CONCAT31(0x747874,(char)uStack_3e9);
  local_3e5 = 0;
  FUN_1001ba8f4(&local_3c0,&local_3d8,&local_3f0);
  FUN_1001ba79c(&local_490,&local_3c0);
  if ((long)local_3b0 < 0) {
    operator_delete(local_3c0);
  }
  if (local_3d9 < '\0') {
    operator_delete((void *)CONCAT17((char)uStack_3e9,local_3f0));
  }
  if (local_3c1 < '\0') {
    operator_delete(local_3d8);
  }
  if (local_490 != (undefined **)0x0) {
    for (; uStack_488 != local_490; uStack_488 = uStack_488 + -3) {
    }
    uStack_488 = local_490;
    operator_delete(local_490);
  }
  FUN_100229730(local_3a8,0);
  FUN_10025cb8c(FUN_10022897c);
  FUN_1004c4a78(0);
  FUN_10057aa1c(0);
  FUN_1005b6964(0);
  FUN_100690580();
  thunk_FUN_10066e8a8();
  iVar7 = FUN_1001afd54();
  if (iVar7 != 0) {
    uVar9 = FUN_10014d60c(PTR_cerr_100d601f8,"Usage:\n",7);
    FUN_100131790(&local_490);
    FUN_1001918f0(uVar9,&local_490);
    FUN_10014b72c(&local_490);
    uVar9 = 0;
    goto LAB_100131130;
  }
  local_480 = CONCAT17(0x11,(undefined7)local_480);
  local_480 = CONCAT62(local_480._2_6_,0x73);
  uStack_488 = (undefined **)s_dump_config_files_100c1c88c._8_8_;
  local_490 = (undefined **)s_dump_config_files_100c1c88c._0_8_;
  plVar10 = (long *)FUN_10019e650(local_3a8,&local_490);
  puVar11 = PTR_typeinfo_100d60300;
  if ((long *)*plVar10 != (long *)0x0) {
    puVar11 = (undefined *)(**(code **)(*(long *)*plVar10 + 0x10))();
  }
  pcVar15 = (char *)(*(ulong *)(PTR_typeinfo_100d602e0 + 8) & 0x7fffffffffffffff);
  if (((char *)(*(ulong *)(puVar11 + 8) & 0x7fffffffffffffff) != pcVar15) &&
     (iVar7 = _strcmp((char *)(*(ulong *)(puVar11 + 8) & 0x7fffffffffffffff),pcVar15), iVar7 != 0))
  {
    local_3c0 = (undefined **)0x0;
    std::bad_cast::bad_cast((bad_cast *)&local_3c0);
    local_3c0 = &PTR__bad_cast_100d880e8;
    FUN_1001499a0(&local_3c0);
    goto LAB_100131578;
  }
  cVar6 = *(char *)(*plVar10 + 8);
  if ((long)local_480 < 0) {
    operator_delete(local_490);
  }
  if (cVar6 != '\0') {
    local_400 = 0;
    uStack_418 = 0;
    local_420 = 0;
    uStack_408 = 0;
    uStack_410 = 0;
    uStack_438 = 0;
    local_440 = 0;
    uStack_428 = 0;
    uStack_430 = 0;
    uStack_458 = 0;
    local_460 = 0;
    uStack_448 = 0;
    uStack_450 = 0;
    uStack_478 = 0;
    local_480 = 0;
    uStack_468 = 0;
    uStack_470 = 0;
    uStack_488 = (undefined **)0x0;
    local_490 = (undefined **)0x0;
    FUN_10014d9d0(&local_490);
    FUN_100131a44(&local_490);
    FUN_10014dac4(&local_490);
                    /* WARNING: Subroutine does not return */
    _exit(0);
  }
  local_480 = CONCAT17(5,(undefined7)local_480);
  local_490 = (undefined **)CONCAT26(local_490._6_2_,0x6576616c73);
  plVar10 = (long *)FUN_10019e650(local_3a8,&local_490);
  if ((long *)*plVar10 == (long *)0x0) {
    uVar14 = *(ulong *)(PTR_typeinfo_100d60300 + 8);
  }
  else {
    lVar12 = (**(code **)(*(long *)*plVar10 + 0x10))();
    uVar14 = *(ulong *)(lVar12 + 8);
  }
  if (((char *)(uVar14 & 0x7fffffffffffffff) != pcVar15) &&
     (iVar7 = _strcmp((char *)(uVar14 & 0x7fffffffffffffff),pcVar15), iVar7 != 0)) {
    local_3d8 = (undefined **)0x0;
    std::bad_cast::bad_cast((bad_cast *)&local_3d8);
    local_3d8 = &PTR__bad_cast_100d880e8;
    FUN_1001499a0(&local_3d8);
    goto LAB_100131578;
  }
  bVar3 = *(byte *)(*plVar10 + 8);
  if ((long)local_480 < 0) {
    operator_delete(local_490);
    if ((bVar3 & 1) == 0) goto LAB_100130d5c;
LAB_100130ea4:
    iVar7 = 0;
  }
  else {
    if ((bVar3 & 1) != 0) goto LAB_100130ea4;
LAB_100130d5c:
    local_480 = CONCAT17(10,(undefined7)local_480);
    local_490 = (undefined **)s_standalone_100c1d314._0_8_;
    uStack_488 = (undefined **)CONCAT53(uStack_488._3_5_,0x656e);
    plVar10 = (long *)FUN_10019e650(local_3a8,&local_490);
    if ((long *)*plVar10 == (long *)0x0) {
      uVar14 = *(ulong *)(PTR_typeinfo_100d60300 + 8);
    }
    else {
      lVar12 = (**(code **)(*(long *)*plVar10 + 0x10))();
      uVar14 = *(ulong *)(lVar12 + 8);
    }
    if (((char *)(uVar14 & 0x7fffffffffffffff) != pcVar15) &&
       (iVar7 = _strcmp((char *)(uVar14 & 0x7fffffffffffffff),pcVar15), iVar7 != 0)) {
      local_3d8 = (undefined **)0x0;
      std::bad_cast::bad_cast((bad_cast *)&local_3d8);
      local_3d8 = &PTR__bad_cast_100d880e8;
      FUN_1001499a0(&local_3d8);
      goto LAB_100131578;
    }
    bVar3 = *(byte *)(*plVar10 + 8);
    if ((long)local_480 < 0) {
      operator_delete(local_490);
      if ((bVar3 & 1) != 0) goto LAB_100130df0;
LAB_100130e04:
      local_480 = CONCAT17(0x10,(undefined7)local_480);
      uStack_488 = (undefined **)s_os_notifications_100c1d31f._8_8_;
      local_490 = (undefined **)s_os_notifications_100c1d31f._0_8_;
      local_480 = local_480 & 0xffffffffffffff00;
      plVar10 = (long *)FUN_10019e650(local_3a8,&local_490);
      if ((long *)*plVar10 == (long *)0x0) {
        uVar14 = *(ulong *)(PTR_typeinfo_100d60300 + 8);
      }
      else {
        lVar12 = (**(code **)(*(long *)*plVar10 + 0x10))();
        uVar14 = *(ulong *)(lVar12 + 8);
      }
      if (((char *)(uVar14 & 0x7fffffffffffffff) != pcVar15) &&
         (iVar7 = _strcmp((char *)(uVar14 & 0x7fffffffffffffff),pcVar15), iVar7 != 0)) {
        local_3d8 = (undefined **)0x0;
        std::bad_cast::bad_cast((bad_cast *)&local_3d8);
        local_3d8 = &PTR__bad_cast_100d880e8;
        FUN_1001499a0(&local_3d8);
LAB_100131578:
                    /* WARNING: Does not return */
        pcVar5 = (code *)SoftwareBreakpoint(1,0x10013157c);
        (*pcVar5)();
      }
      bVar3 = *(byte *)(*plVar10 + 8);
      if ((long)local_480 < 0) {
        operator_delete(local_490);
      }
      if ((bVar3 & 1) == 0) goto LAB_100130ea4;
      uStack_488._4_4_ = (undefined4)((ulong)uStack_488 >> 0x20);
      iVar7 = 2;
    }
    else {
      if ((bVar3 & 1) == 0) goto LAB_100130e04;
LAB_100130df0:
      iVar7 = 1;
    }
  }
  local_480 = CONCAT17(0xc,(undefined7)local_480);
  uStack_488 = (undefined **)CONCAT35(uStack_488._5_3_,0x656c6966);
  local_490 = (undefined **)uVar9;
  for (plVar10 = (long *)local_390; plVar10 != (long *)0x0; plVar10 = (long *)*plVar10) {
    uVar14 = plVar10[5];
    puVar19 = (void *)plVar10[4];
    if (-1 < (char)*(byte *)((long)plVar10 + 0x37)) {
      uVar14 = (ulong)*(byte *)((long)plVar10 + 0x37);
      puVar19 = plVar10 + 4;
    }
    sVar1 = uVar14;
    if (0xb < uVar14) {
      sVar1 = 0xc;
    }
    iVar8 = _memcmp(&local_490,puVar19,sVar1);
    if (iVar8 == 0) {
      if (uVar14 < 0xd) goto LAB_100130f34;
    }
    else if (-1 < iVar8) {
LAB_100130f34:
      iVar8 = _memcmp(puVar19,&local_490,sVar1);
      if (iVar8 == 0) {
        if (uVar14 < 0xc) goto LAB_100130edc;
      }
      else if (iVar8 < 0) {
LAB_100130edc:
        plVar10 = plVar10 + 1;
        goto LAB_100130ee0;
      }
      local_480 = CONCAT17(0xc,(undefined7)local_480);
      local_490 = (undefined **)uVar9;
      uStack_488 = (undefined **)CONCAT35(uStack_488._5_3_,0x656c6966);
      plVar10 = (long *)FUN_10019e650(local_3a8,&local_490);
      puVar11 = PTR_typeinfo_100d60300;
      if ((long *)*plVar10 != (long *)0x0) {
        puVar11 = (undefined *)(**(code **)(*(long *)*plVar10 + 0x10))();
      }
      if (((char *)(*(ulong *)(puVar11 + 8) & 0x7fffffffffffffff) !=
           "NSt3__16vectorINS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEENS4_IS6_EEEE")
         && (iVar8 = _strcmp((char *)(*(ulong *)(puVar11 + 8) & 0x7fffffffffffffff),
                             "NSt3__16vectorINS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEENS4_IS6_EEEE"
                            ), iVar8 != 0)) {
        local_3d8 = (undefined **)0x0;
        std::bad_cast::bad_cast((bad_cast *)&local_3d8);
        local_3d8 = &PTR__bad_cast_100d880e8;
        FUN_1001499a0(&local_3d8);
        goto LAB_100131578;
      }
      lVar12 = *plVar10;
      if ((long)local_480 < 0) {
        operator_delete(local_490);
      }
      puVar19 = *(undefined8 **)(lVar12 + 8);
      puVar2 = *(undefined8 **)(lVar12 + 0x10);
      if (puVar19 != puVar2) goto LAB_100130ffc;
      break;
    }
LAB_100130ee0:
  }
  goto LAB_1001310a4;
  while( true ) {
    if (iVar8 < 0) {
      operator_delete(local_3c0);
    }
    puVar19 = puVar19 + 3;
    if (puVar19 == puVar2) break;
LAB_100130ffc:
    ppuVar16 = (undefined **)(long)*(char *)((long)puVar19 + 0x17);
    if ((long)ppuVar16 < 0) {
      ppuVar16 = (undefined **)puVar19[1];
      if ((undefined **)0x7ffffffffffffff7 < ppuVar16) {
                    /* WARNING: Subroutine does not return */
        FUN_100147bd8(&local_490);
      }
      puVar17 = (undefined8 *)*puVar19;
      if (ppuVar16 < (undefined **)0x17) goto LAB_100131010;
LAB_100131038:
      uVar14 = 0x19;
      if (((ulong)ppuVar16 | 7) != 0x17) {
        uVar14 = ((ulong)ppuVar16 | 7) + 1;
      }
      pppuVar13 = operator_new(uVar14);
      local_480 = uVar14 | 0x8000000000000000;
      local_490 = (undefined **)pppuVar13;
      uStack_488 = ppuVar16;
LAB_10013105c:
      _memmove(pppuVar13,puVar17,(size_t)ppuVar16);
      pppuVar18 = pppuVar13;
    }
    else {
      puVar17 = puVar19;
      if ((undefined **)0x16 < ppuVar16) goto LAB_100131038;
LAB_100131010:
      local_480 = CONCAT17((char)ppuVar16,(undefined7)local_480);
      pppuVar13 = &local_490;
      pppuVar18 = &local_490;
      if (ppuVar16 != (undefined **)0x0) goto LAB_10013105c;
    }
    *(undefined1 *)((long)pppuVar18 + (long)ppuVar16) = 0;
    ppuStack_3b8 = uStack_488;
    local_3c0 = local_490;
    local_3b0 = local_480;
    uVar14 = FUN_100716cfc(&local_3c0);
    iVar8 = (int)local_3b0._7_1_;
    if ((uVar14 & 1) != 0) {
      ppuVar16 = ppuStack_3b8;
      if (-1 < iVar8) {
        ppuVar16 = (undefined **)(long)iVar8;
      }
      if (ppuVar16 == (undefined **)0x0) goto LAB_1001310ac;
      FUN_10014d9d0(&local_490);
      iVar8 = FUN_100673f10(&local_490,&local_3c0);
      if (iVar8 == 0) {
        cVar6 = FUN_10014d60c(PTR_cerr_100d601f8,"ERROR: Reading option file",0x1a);
        std::ios_base::getloc();
        plVar10 = (long *)std::locale::use_facet((id *)&local_3d8);
        (**(code **)(*plVar10 + 0x38))(plVar10,10);
        std::locale::~locale(&local_3d8);
        std::ostream::put(cVar6);
LAB_1001313ac:
        std::ostream::flush();
LAB_1001313b4:
        uVar9 = 0;
      }
      else {
        DAT_100e33568 = FUN_1001f22cc();
        FUN_1006c13e0(uStack_418 & 0xff);
        FUN_1006c1480(uStack_418._1_1_);
        ppuVar16 = uStack_488;
        if (-1 < (long)local_480) {
          ppuVar16 = (undefined **)(local_480 >> 0x38);
        }
        if (ppuVar16 == (undefined **)0x0) {
          cVar6 = FUN_10014d60c(PTR_cerr_100d601f8,"ERROR: No valid database path defined",0x25);
          std::ios_base::getloc();
          plVar10 = (long *)std::locale::use_facet((id *)&local_3d8);
          (**(code **)(*plVar10 + 0x38))(plVar10,10);
          std::locale::~locale(&local_3d8);
          std::ostream::put(cVar6);
          goto LAB_1001313ac;
        }
        if (iVar7 == 0) {
          if ((local_460 == 0) || ((*(uint *)(local_460 + 4) & 0xfffffffe) != 2)) {
            uVar9 = FUN_100132970(&local_490);
            FUN_100446c84(&local_3d8,"end");
            FUN_10047286c(&local_3d8);
            goto LAB_10013145c;
          }
          FUN_10014d60c(PTR_cerr_100d601f8,"ERROR: No valid IPC channel defined",0x23);
          FUN_100133f00();
          goto LAB_1001313b4;
        }
        if (iVar7 == 1) {
          FUN_100674a60(&local_490);
          uVar9 = FUN_100133f90(local_3a8,&local_490);
          FUN_100446c84(&local_3d8,"end");
          FUN_10047286c(&local_3d8);
LAB_10013145c:
          FUN_100133ec0(&local_3d8);
        }
        else {
          FUN_100135614(local_3a8,&local_490);
          FUN_100446c84(&local_3d8,"end");
          FUN_10047286c(&local_3d8);
          FUN_100133ec0(&local_3d8);
          uVar9 = 1;
        }
      }
      FUN_10014dac4(&local_490);
      goto joined_r0x0001001313c4;
    }
  }
LAB_1001310a4:
  local_3c0 = (undefined **)0x0;
  ppuStack_3b8 = (undefined **)0x0;
  local_3b0 = 0;
LAB_1001310ac:
  cVar6 = FUN_10014d60c(PTR_cerr_100d601f8,"ERROR: Invalid option file",0x1a);
  std::ios_base::getloc();
  plVar10 = (long *)std::locale::use_facet((id *)&local_490);
  (**(code **)(*plVar10 + 0x38))(plVar10,10);
  std::locale::~locale(&local_490);
  std::ostream::put(cVar6);
  std::ostream::flush();
  uVar9 = 0;
joined_r0x0001001313c4:
  if ((long)local_3b0 < 0) {
    operator_delete(local_3c0);
  }
LAB_100131130:
  FUN_10061f3bc();
  FUN_1006906a4();
  FUN_1005b6b10();
  FUN_10057acfc();
  FUN_1004c4bd8();
  FUN_10022ac48();
  FUN_1001856f8(&DAT_100e33568);
  if (local_350 != (void *)0x0) {
    for (; local_348 != local_350; local_348 = (void *)((long)local_348 + -0x30)) {
    }
    local_348 = local_350;
    operator_delete(local_350);
  }
  local_3a8[0] = &PTR_FUN_100d8be48;
  FUN_10014add0(auStack_368,local_360);
  FUN_1001542e8(auStack_380,local_378);
  FUN_100154348(auStack_398,local_390);
  FUN_100154418(auStack_338);
  FUN_100154418(auStack_1d0);
  FUN_1001a3758(auStack_68);
  return uVar9;
}

