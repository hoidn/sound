// 0x1002867e0 FUN_1002867e0 state=exported-with-warnings role=CoreMIDI port search by kMIDIPropertyModel
// source chunk chunk-00111.jsonl; code_sha256=8bbc8b3dd426c2a7417e7ce24781d1ece5bec8a2af6ce453c47f23f165157e72

/* WARNING: Removing unreachable block (ram,0x00010028728c) */
/* WARNING: Removing unreachable block (ram,0x000100287250) */
/* WARNING: Removing unreachable block (ram,0x00010028721c) */
/* WARNING: Removing unreachable block (ram,0x0001002872c0) */
/* WARNING: Type propagation algorithm not settling */

undefined1  [16] FUN_1002867e0(void)

{
  long *plVar1;
  long *******ppppppplVar2;
  long *******ppppppplVar3;
  uint uVar4;
  bool bVar5;
  bool bVar6;
  bool bVar7;
  byte bVar8;
  uint uVar9;
  code *pcVar10;
  int iVar11;
  undefined8 uVar12;
  ulong uVar13;
  undefined8 uVar14;
  void *pvVar15;
  long lVar16;
  long *plVar17;
  long *plVar18;
  ulong uVar19;
  undefined8 uVar20;
  ulong uVar21;
  size_t sVar22;
  uint uVar23;
  undefined1 auVar24 [16];
  uint local_184;
  uint local_180;
  uint local_17c;
  uint local_178;
  uint local_174;
  uint local_170;
  uint local_164;
  long *******local_158;
  long *******ppppppplStack_150;
  undefined7 local_148;
  char cStack_141;
  undefined8 local_140;
  long *******ppppppplStack_138;
  long *******local_130;
  long *******local_128;
  long *******ppppppplStack_120;
  long ******local_118;
  long *******local_108;
  long *******ppppppplStack_100;
  undefined7 local_f8;
  byte bStack_f1;
  long *******local_f0;
  long *******ppppppplStack_e8;
  undefined8 local_e0;
  long *local_d8;
  long *local_d0;
  long *local_c8;
  undefined4 local_bc;
  undefined **local_b8;
  undefined4 local_b0;
  undefined ***local_a0;
  undefined **local_98;
  undefined4 local_90;
  undefined ***local_80;
  byte local_78;
  long local_70;
  
  local_70 = *(long *)PTR____stack_chk_guard_101b8c408;
  uVar12 = _CFStringCreateWithCString(0,"Push 3 port search",0x600);
  _MIDIClientCreate(uVar12,0,0,&local_bc);
  bVar6 = false;
  local_178 = 0;
  uVar9 = 0;
  bVar8 = 0;
  uVar23 = 0;
  local_b8 = &PTR_FUN_101bd69b8;
  local_b0 = local_bc;
  local_a0 = &local_b8;
  local_98 = &PTR_FUN_101bd69b8;
  local_80 = &local_98;
  local_90 = local_bc;
  local_78 = 1;
  local_d8 = (long *)0x0;
  local_d0 = (long *)0x0;
  local_c8 = (long *)0x0;
  uVar12 = *(undefined8 *)PTR__kMIDIPropertyModel_101b8c0e0;
  uVar20 = *(undefined8 *)PTR__kMIDIPropertyDisplayName_101b8c0d8;
  while( true ) {
    uVar13 = _MIDIGetNumberOfSources();
    if (uVar13 <= uVar23) break;
    uVar14 = _MIDIGetSource();
    if ((int)uVar14 != 0) {
      FUN_1002875a4(&local_f0,uVar14,uVar12);
      FUN_1002875a4(&local_108,uVar14,uVar20);
      if ((long)local_e0 < 0) {
        FUN_10018127c(&local_140,local_f0,ppppppplStack_e8);
      }
      else {
        ppppppplStack_138 = ppppppplStack_e8;
        local_140 = local_f0;
        local_130 = local_e0;
      }
      if ((char)bStack_f1 < '\0') {
        FUN_10018127c(&local_128,local_108,ppppppplStack_100);
      }
      else {
        ppppppplStack_120 = ppppppplStack_100;
        local_128 = local_108;
        local_118 = (long ******)CONCAT17(bStack_f1,local_f8);
      }
      plVar18 = local_d8;
      if (local_d0 < local_c8) {
        local_d0[2] = (long)local_130;
        local_d0[1] = (long)ppppppplStack_138;
        *local_d0 = (long)local_140;
        ppppppplStack_138 = (long *******)0x0;
        local_130 = (long *******)0x0;
        local_140 = (long *******)0x0;
        local_d0[4] = (long)ppppppplStack_120;
        local_d0[3] = (long)local_128;
        local_d0[5] = (long)local_118;
        ppppppplStack_120 = (long *******)0x0;
        local_118 = (long ******)0x0;
        local_128 = (long *******)0x0;
        local_d0 = local_d0 + 6;
      }
      else {
        sVar22 = (long)local_d0 - (long)local_d8;
        uVar13 = ((long)sVar22 >> 4) * -0x5555555555555555 + 1;
        if (0x555555555555555 < uVar13) {
          FUN_1001bc450(&local_d8);
          goto LAB_1002873b8;
        }
        lVar16 = (long)local_c8 - (long)local_d8 >> 4;
        uVar19 = lVar16 * 0x5555555555555556;
        if (uVar19 < uVar13 || uVar19 - uVar13 == 0) {
          uVar19 = uVar13;
        }
        if (0x2aaaaaaaaaaaaa9 < (ulong)(lVar16 * -0x5555555555555555)) {
          uVar19 = 0x555555555555555;
        }
        if (uVar19 == 0) {
          pvVar15 = (void *)0x0;
        }
        else {
          if (0x555555555555555 < uVar19) {
                    /* WARNING: Subroutine does not return */
            FUN_10017f504();
          }
          pvVar15 = operator_new(uVar19 * 0x30);
        }
        plVar17 = (long *)((long)pvVar15 + ((long)sVar22 >> 4) * 0x10);
        plVar17[2] = (long)local_130;
        plVar17[1] = (long)ppppppplStack_138;
        *plVar17 = (long)local_140;
        ppppppplStack_138 = (long *******)0x0;
        local_130 = (long *******)0x0;
        local_140 = (long *******)0x0;
        plVar17[4] = (long)ppppppplStack_120;
        plVar17[3] = (long)local_128;
        plVar17[5] = (long)local_118;
        local_128 = (long *******)0x0;
        ppppppplStack_120 = (long *******)0x0;
        plVar1 = plVar17 + 6;
        local_118 = (long ******)0x0;
        _memcpy((long *)((long)plVar17 - sVar22),plVar18,sVar22);
        local_d8 = (long *)((long)plVar17 - sVar22);
        local_c8 = (long *)((long)pvVar15 + uVar19 * 0x30);
        local_d0 = plVar1;
        if (plVar18 == (long *)0x0) {
        }
        else {
          operator_delete(plVar18);
          local_d0 = plVar1;
          if ((long)local_118 < 0) {
            operator_delete(local_128);
          }
        }
        if ((long)local_130 < 0) {
          operator_delete(local_140);
        }
      }
      uVar4 = (uint)(char)local_e0._7_1_;
      ppppppplVar3 = ppppppplStack_e8;
      if (-1 < (int)uVar4) {
        ppppppplVar3 = (long *******)(ulong)local_e0._7_1_;
      }
      if (ppppppplVar3 == (long *******)0xe) {
        ppppppplVar3 = local_f0;
        if (-1 < (int)uVar4) {
          ppppppplVar3 = (long *******)&local_f0;
        }
        if ((*ppppppplVar3 == (long ******)0x206e6f74656c6241 &&
            *(long *)((long)ppppppplVar3 + 6) == 0x322068737550206e) && bVar8 == 0) {
          local_170 = uVar23 >> 8;
          bVar8 = 1;
          uVar9 = uVar23;
          goto joined_r0x000100286b60;
        }
        if (*ppppppplVar3 != (long ******)0x206e6f74656c6241 ||
            *(long *)((long)ppppppplVar3 + 6) != 0x332068737550206e) goto joined_r0x000100286b60;
        if (!bVar6) {
          local_180 = uVar23 >> 8;
          bVar6 = true;
          local_178 = uVar23;
          goto joined_r0x000100286b60;
        }
        bVar6 = true;
        if (-1 < (char)bStack_f1) goto LAB_100286b64;
LAB_1002868c4:
        operator_delete(local_108);
        if (-1 < (long)local_e0) goto LAB_1002868d4;
      }
      else {
joined_r0x000100286b60:
        if ((char)bStack_f1 < '\0') goto LAB_1002868c4;
LAB_100286b64:
        if ((uVar4 >> 7 & 1) == 0) goto LAB_1002868d4;
      }
      operator_delete(local_f0);
    }
LAB_1002868d4:
    uVar23 = uVar23 + 1;
  }
  bVar7 = false;
  local_17c = 0;
  bVar5 = false;
  local_164 = 0;
  local_f0 = (long *******)0x0;
  ppppppplStack_e8 = (long *******)0x0;
  local_e0 = (long *******)0x0;
  for (uVar23 = 0; uVar13 = _MIDIGetNumberOfDestinations(), uVar23 < uVar13; uVar23 = uVar23 + 1) {
    uVar14 = _MIDIGetDestination();
    if ((int)uVar14 != 0) {
      FUN_1002875a4(&local_108,uVar14,uVar12);
      FUN_1002875a4(&local_158,uVar14,uVar20);
      if ((char)bStack_f1 < '\0') {
        FUN_10018127c(&local_140,local_108,ppppppplStack_100);
      }
      else {
        ppppppplStack_138 = ppppppplStack_100;
        local_140 = local_108;
        local_130 = (long *******)CONCAT17(bStack_f1,local_f8);
      }
      if (cStack_141 < '\0') {
        FUN_10018127c(&local_128,local_158,ppppppplStack_150);
      }
      else {
        ppppppplStack_120 = ppppppplStack_150;
        local_128 = local_158;
        local_118 = (long ******)CONCAT17(cStack_141,local_148);
      }
      ppppppplVar3 = local_f0;
      if (ppppppplStack_e8 < local_e0) {
        ppppppplStack_e8[2] = (long ******)local_130;
        ppppppplStack_e8[1] = (long ******)ppppppplStack_138;
        *ppppppplStack_e8 = (long ******)local_140;
        ppppppplStack_138 = (long *******)0x0;
        local_130 = (long *******)0x0;
        local_140 = (long *******)0x0;
        ppppppplStack_e8[4] = (long ******)ppppppplStack_120;
        ppppppplStack_e8[3] = (long ******)local_128;
        ppppppplStack_e8[5] = local_118;
        ppppppplStack_120 = (long *******)0x0;
        local_118 = (long ******)0x0;
        local_128 = (long *******)0x0;
        ppppppplStack_e8 = ppppppplStack_e8 + 6;
      }
      else {
        sVar22 = (long)ppppppplStack_e8 - (long)local_f0;
        uVar13 = ((long)sVar22 >> 4) * -0x5555555555555555 + 1;
        if (0x555555555555555 < uVar13) {
          FUN_1001bc450(&local_f0);
LAB_1002873b8:
                    /* WARNING: Does not return */
          pcVar10 = (code *)SoftwareBreakpoint(1,0x1002873bc);
          (*pcVar10)();
        }
        lVar16 = (long)local_e0 - (long)local_f0 >> 4;
        uVar19 = lVar16 * 0x5555555555555556;
        if (uVar19 < uVar13 || uVar19 - uVar13 == 0) {
          uVar19 = uVar13;
        }
        if (0x2aaaaaaaaaaaaa9 < (ulong)(lVar16 * -0x5555555555555555)) {
          uVar19 = 0x555555555555555;
        }
        if (uVar19 == 0) {
          pvVar15 = (void *)0x0;
        }
        else {
          if (0x555555555555555 < uVar19) {
                    /* WARNING: Subroutine does not return */
            FUN_10017f504();
          }
          pvVar15 = operator_new(uVar19 * 0x30);
        }
        plVar18 = (long *)((long)pvVar15 + ((long)sVar22 >> 4) * 0x10);
        plVar18[2] = (long)local_130;
        plVar18[1] = (long)ppppppplStack_138;
        *plVar18 = (long)local_140;
        ppppppplStack_138 = (long *******)0x0;
        local_130 = (long *******)0x0;
        local_140 = (long *******)0x0;
        plVar18[4] = (long)ppppppplStack_120;
        plVar18[3] = (long)local_128;
        plVar18[5] = (long)local_118;
        local_128 = (long *******)0x0;
        ppppppplStack_120 = (long *******)0x0;
        ppppppplVar2 = (long *******)(plVar18 + 6);
        local_118 = (long ******)0x0;
        _memcpy((long *******)((long)plVar18 - sVar22),ppppppplVar3,sVar22);
        local_f0 = (long *******)((long)plVar18 - sVar22);
        local_e0 = (long *******)((long)pvVar15 + uVar19 * 0x30);
        ppppppplStack_e8 = ppppppplVar2;
        if (ppppppplVar3 == (long *******)0x0) {
        }
        else {
          operator_delete(ppppppplVar3);
          ppppppplStack_e8 = ppppppplVar2;
          if ((long)local_118 < 0) {
            operator_delete(local_128);
          }
        }
        if ((long)local_130 < 0) {
          operator_delete(local_140);
        }
      }
      uVar4 = (uint)(char)bStack_f1;
      ppppppplVar3 = ppppppplStack_100;
      if (-1 < (int)uVar4) {
        ppppppplVar3 = (long *******)(ulong)bStack_f1;
      }
      if (ppppppplVar3 == (long *******)0xe) {
        ppppppplVar3 = local_108;
        if (-1 < (int)uVar4) {
          ppppppplVar3 = (long *******)&local_108;
        }
        if ((*ppppppplVar3 == (long ******)0x206e6f74656c6241 &&
            *(long *)((long)ppppppplVar3 + 6) == 0x322068737550206e) && !bVar5) {
          local_174 = uVar23 >> 8;
          bVar5 = true;
          local_164 = uVar23;
          goto joined_r0x000100286e9c;
        }
        if (*ppppppplVar3 != (long ******)0x206e6f74656c6241 ||
            *(long *)((long)ppppppplVar3 + 6) != 0x332068737550206e) goto joined_r0x000100286e9c;
        if (!bVar7) {
          local_184 = uVar23 >> 8;
          bVar7 = true;
          local_17c = uVar23;
          goto joined_r0x000100286e9c;
        }
        bVar7 = true;
        if (-1 < cStack_141) goto LAB_100286ea0;
LAB_100286bf4:
        operator_delete(local_158);
        if (-1 < (char)bStack_f1) goto LAB_100286c04;
      }
      else {
joined_r0x000100286e9c:
        if (cStack_141 < '\0') goto LAB_100286bf4;
LAB_100286ea0:
        if ((uVar4 >> 7 & 1) == 0) goto LAB_100286c04;
      }
      operator_delete(local_108);
    }
LAB_100286c04:
  }
  if ((bool)(bVar6 | bVar8)) {
    if (bVar5 || bVar7 != false) {
      if (((bool)(bVar8 ^ bVar5)) || ((bool)(bVar6 ^ bVar7))) {
        uVar12 = std::chrono::system_clock::now();
        FUN_1003324b0(&local_140,4,uVar12);
        iVar11 = FUN_10032ece8(&local_140);
        if (iVar11 != 0) {
          FUN_10032bea8(&local_140,"In port has no corresponding out port (or vice versa)");
        }
        thunk_FUN_10032ba14(&local_140);
        goto LAB_1002871f4;
      }
      if ((byte)(bVar6 & bVar7) == 0) {
        local_17c = local_164;
        local_184 = local_174;
        local_178 = uVar9;
        local_180 = local_170;
      }
      local_140 = (long *******)
                  CONCAT44(local_178 & 0xff | local_180 << 8,(uint)(byte)(bVar6 & bVar7));
      ppppppplStack_138 =
           (long *******)CONCAT44(ppppppplStack_138._4_4_,local_17c & 0xff | local_184 << 8);
      uVar12 = std::chrono::system_clock::now();
      FUN_1003324b0(&local_108,2,uVar12);
      iVar11 = FUN_10032ece8(&local_108);
      if (iVar11 != 0) {
        uVar12 = FUN_10032bea8(&local_108,"Hardware type: ");
        FUN_100287790(uVar12,&local_140);
      }
      thunk_FUN_10032ba14(&local_108);
      uVar19 = (ulong)local_140 & 0xffffffffffffff00;
      uVar13 = (ulong)ppppppplStack_138 & 0xffffffff | 0x100000000;
      uVar21 = (ulong)local_140 & 0xff;
    }
    else {
      uVar12 = std::chrono::system_clock::now();
      FUN_1003324b0(&local_140,4,uVar12);
      iVar11 = FUN_10032ece8(&local_140);
      if (iVar11 != 0) {
        FUN_10032bea8(&local_140,"Couldn\'t find MIDI out port");
      }
      thunk_FUN_10032ba14(&local_140);
      if (local_f0 != ppppppplStack_e8) {
        uVar12 = std::chrono::system_clock::now();
        FUN_1003324b0(&local_140,2,uVar12);
        iVar11 = FUN_10032ece8(&local_140);
        if (iVar11 != 0) {
          FUN_10032bea8(&local_140,"Candidates were:");
        }
        thunk_FUN_10032ba14(&local_140);
        ppppppplVar2 = ppppppplStack_e8;
        for (ppppppplVar3 = local_f0; ppppppplVar3 != ppppppplVar2; ppppppplVar3 = ppppppplVar3 + 6)
        {
          uVar12 = std::chrono::system_clock::now();
          FUN_1003324b0(&local_140,2,uVar12);
          iVar11 = FUN_10032ece8(&local_140);
          if (iVar11 != 0) {
            uVar12 = FUN_10032cd88(&local_140,ppppppplVar3);
            uVar12 = FUN_10032bea8(uVar12,":");
            FUN_10032cd88(uVar12,ppppppplVar3 + 3);
          }
          thunk_FUN_10032ba14(&local_140);
        }
        goto LAB_1002871f4;
      }
      uVar13 = 0;
      uVar19 = 0;
      uVar21 = 0;
    }
  }
  else {
    uVar12 = std::chrono::system_clock::now();
    FUN_1003324b0(&local_140,4,uVar12);
    iVar11 = FUN_10032ece8(&local_140);
    if (iVar11 != 0) {
      FUN_10032bea8(&local_140,"Couldn\'t find MIDI in port");
    }
    thunk_FUN_10032ba14(&local_140);
    if (local_d8 != local_d0) {
      uVar12 = std::chrono::system_clock::now();
      FUN_1003324b0(&local_140,2,uVar12);
      iVar11 = FUN_10032ece8(&local_140);
      if (iVar11 != 0) {
        FUN_10032bea8(&local_140,"Candidates were:");
      }
      thunk_FUN_10032ba14(&local_140);
      plVar1 = local_d0;
      for (plVar18 = local_d8; plVar18 != plVar1; plVar18 = plVar18 + 6) {
        uVar12 = std::chrono::system_clock::now();
        FUN_1003324b0(&local_140,2,uVar12);
        iVar11 = FUN_10032ece8(&local_140);
        if (iVar11 != 0) {
          uVar12 = FUN_10032cd88(&local_140,plVar18);
          uVar12 = FUN_10032bea8(uVar12,":");
          FUN_10032cd88(uVar12,plVar18 + 3);
        }
        thunk_FUN_10032ba14(&local_140);
      }
    }
LAB_1002871f4:
    uVar13 = 0;
    uVar19 = 0;
    uVar21 = 0;
  }
  if (local_f0 != (long *******)0x0) {
    for (; ppppppplStack_e8 != local_f0; ppppppplStack_e8 = ppppppplStack_e8 + -6) {
    }
    ppppppplStack_e8 = local_f0;
    operator_delete(local_f0);
  }
  if (local_d8 != (long *)0x0) {
    for (; local_d0 != local_d8; local_d0 = local_d0 + -6) {
    }
    local_d0 = local_d8;
    operator_delete(local_d8);
  }
  if (local_78 == 1) {
    if (local_80 == (undefined ***)0x0) {
                    /* WARNING: Subroutine does not return */
      FUN_10018001c();
    }
    (*(code *)(*local_80)[6])();
    if ((local_78 & 1) != 0) {
      if (local_80 == &local_98) {
        lVar16 = 0x20;
      }
      else {
        if (local_80 == (undefined ***)0x0) goto LAB_100287348;
        lVar16 = 0x28;
      }
      (**(code **)((long)*local_80 + lVar16))();
    }
  }
LAB_100287348:
  if (*(long *)PTR____stack_chk_guard_101b8c408 == local_70) {
    auVar24._0_8_ = uVar21 | uVar19;
    auVar24._8_8_ = uVar13;
    return auVar24;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

