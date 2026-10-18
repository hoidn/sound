
/* WARNING: Removing unreachable block (ram,0x00010317a308) */
/* WARNING: Removing unreachable block (ram,0x00010317a074) */
/* WARNING: Removing unreachable block (ram,0x00010317aa50) */
/* WARNING: Removing unreachable block (ram,0x000103179f30) */
/* WARNING: Removing unreachable block (ram,0x00010317a520) */
/* WARNING: Removing unreachable block (ram,0x00010317a65c) */
/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_103179e68(long param_1)

{
  ulong uVar1;
  ulong uVar2;
  uint5 *puVar3;
  ulong uVar4;
  uint uVar5;
  byte bVar6;
  undefined8 *puVar7;
  code *pcVar8;
  int iVar9;
  long *plVar10;
  int *******pppppppiVar11;
  void *pvVar12;
  undefined8 uVar13;
  int *piVar14;
  undefined8 *puVar15;
  undefined1 *puVar16;
  undefined8 *puVar17;
  long lVar18;
  long *plVar19;
  undefined8 *puVar20;
  ulong uVar21;
  undefined8 *puVar22;
  uint uVar23;
  ulong uVar24;
  undefined8 *puVar25;
  int *******pppppppiVar26;
  size_t sVar27;
  ulong uVar28;
  undefined1 auVar29 [16];
  long *local_158;
  uint5 local_150;
  undefined3 uStack_14b;
  undefined5 uStack_148;
  char cStack_143;
  char cStack_142;
  char cStack_141;
  undefined7 uStack_140;
  byte bStack_139;
  undefined8 uStack_138;
  int *local_130;
  undefined8 *local_128;
  undefined8 *local_120;
  undefined8 *puStack_118;
  void *local_110 [2];
  char local_f9;
  int *local_f8;
  undefined8 *local_f0;
  undefined8 *local_e8;
  undefined8 *local_e0;
  int *local_d8 [2];
  char local_c1;
  int *******local_c0;
  ulong uStack_b8;
  undefined8 local_b0;
  int *******local_a0;
  undefined6 uStack_98;
  undefined2 uStack_92;
  char acStack_90 [8];
  undefined7 local_88;
  char cStack_81;
  undefined7 uStack_80;
  long local_78;
  
  local_78 = *(long *)PTR____stack_chk_guard_1064f8818;
  FUN_1014412dc(&local_f8,7);
  plVar10 = operator_new(0x58);
  FUN_1014320f0(&local_a0,&local_f8);
  FUN_1002725dc(&local_150,&local_a0,0);
  *plVar10 = (long)&PTR_thunk_FUN_10027a25c_1065928b0;
  plVar10[1] = (long)(plVar10 + 2);
  *(undefined8 *)((long)plVar10 + 0x14) = DAT_1055d3960;
  *(undefined4 *)((long)plVar10 + 0x1c) = 0xffffffff;
  if ((char)bStack_139 < '\0') {
    FUN_10023448c(plVar10 + 4,CONCAT35(uStack_14b,local_150),
                  CONCAT17(cStack_141,CONCAT16(cStack_142,CONCAT15(cStack_143,uStack_148))));
    *(undefined4 *)(plVar10 + 7) = 0;
    plVar10[9] = 0;
    plVar10[10] = 0;
    plVar10[8] = 0;
    if ((char)bStack_139 < '\0') {
      operator_delete((void *)CONCAT35(uStack_14b,local_150));
    }
  }
  else {
    plVar10[5] = CONCAT17(cStack_141,CONCAT16(cStack_142,CONCAT15(cStack_143,uStack_148)));
    plVar10[4] = CONCAT35(uStack_14b,local_150);
    plVar10[6] = CONCAT17(bStack_139,uStack_140);
    *(undefined4 *)(plVar10 + 7) = 0;
    plVar10[9] = 0;
    plVar10[10] = 0;
    plVar10[8] = 0;
  }
  local_150._0_1_ = s_PluginScanner_105be57b8[0];
  local_150._1_1_ = s_PluginScanner_105be57b8[1];
  local_150._2_1_ = s_PluginScanner_105be57b8[2];
  local_150._3_1_ = s_PluginScanner_105be57b8[3];
  local_150._4_1_ = s_PluginScanner_105be57b8[4];
  uStack_14b._0_1_ = s_PluginScanner_105be57b8[5];
  uStack_14b._1_1_ = s_PluginScanner_105be57b8[6];
  uStack_14b._2_1_ = s_PluginScanner_105be57b8[7];
  uStack_148._0_1_ = s_PluginScanner_105be57b8[8];
  uStack_148._1_1_ = s_PluginScanner_105be57b8[9];
  uStack_148._2_1_ = s_PluginScanner_105be57b8[10];
  uStack_148._3_1_ = s_PluginScanner_105be57b8[0xb];
  uStack_148._4_1_ = s_PluginScanner_105be57b8[0xc];
  cStack_143 = 0;
  bStack_139 = '\r';
  uStack_98._0_1_ = s_Ableton_Plugin_Scanner_105be57c8[8];
  uStack_98._1_1_ = s_Ableton_Plugin_Scanner_105be57c8[9];
  uStack_98._2_1_ = s_Ableton_Plugin_Scanner_105be57c8[10];
  uStack_98._3_1_ = s_Ableton_Plugin_Scanner_105be57c8[0xb];
  uStack_98._4_1_ = s_Ableton_Plugin_Scanner_105be57c8[0xc];
  uStack_98._5_1_ = s_Ableton_Plugin_Scanner_105be57c8[0xd];
  local_a0 = (int *******)s_Ableton_Plugin_Scanner_105be57c8._0_8_;
  uStack_92._0_1_ = s_Ableton_Plugin_Scanner_105be57c8[0xe];
  uStack_92._1_1_ = s_Ableton_Plugin_Scanner_105be57c8[0xf];
  acStack_90[0] = s_Ableton_Plugin_Scanner_105be57c8[0x10];
  acStack_90[1] = s_Ableton_Plugin_Scanner_105be57c8[0x11];
  acStack_90[2] = s_Ableton_Plugin_Scanner_105be57c8[0x12];
  acStack_90[3] = s_Ableton_Plugin_Scanner_105be57c8[0x13];
  acStack_90[4] = s_Ableton_Plugin_Scanner_105be57c8[0x14];
  acStack_90[5] = s_Ableton_Plugin_Scanner_105be57c8[0x15];
  acStack_90[6] = 0;
  acStack_90[7] = '\x16';
  FUN_1011e8540(local_110,&local_150,&local_a0);
  if ((char)bStack_139 < '\0') {
    operator_delete((void *)CONCAT35(uStack_14b,local_150));
  }
  FUN_101427680(&local_a0,"--db");
  (**(code **)(**(long **)(param_1 + 0x78) + 0xa60))(&local_150);
  thunk_FUN_101432b6c(&local_c0,&local_150);
  FUN_101427680(local_d8,"--cid");
  FUN_10317caa8(&local_128,&local_a0,&local_c0,local_d8,&local_f8);
  if ((local_d8[0] != (int *)0x0) &&
     (iVar9 = *local_d8[0], *local_d8[0] = iVar9 + -1, iVar9 + -1 == 0)) {
    FUN_101449efc();
  }
  if ((local_c0 != (int *******)0x0) &&
     (iVar9 = *(int *)local_c0, *(int *)local_c0 = iVar9 + -1, iVar9 + -1 == 0)) {
    FUN_101449efc();
  }
  if ((char)bStack_139 < '\0') {
    operator_delete((void *)CONCAT35(uStack_14b,local_150));
  }
  if ((local_a0 != (int *******)0x0) &&
     (iVar9 = *(int *)local_a0, *(int *)local_a0 = iVar9 + -1, iVar9 + -1 == 0)) {
    FUN_101449efc();
  }
  plVar19 = *(long **)(param_1 + 0xb0);
  do {
    if (plVar19 == (long *)0x0) {
      if ((*(byte *)(param_1 + 0xcc) & 1) != 0) {
        FUN_101427680(&local_150,"--reset");
        if (local_120 < puStack_118) {
          *local_120 = 0;
          *local_120 = CONCAT35(uStack_14b,local_150);
          local_120 = local_120 + 1;
        }
        else {
          local_120 = (undefined8 *)FUN_1002b614c(&local_128,&local_150);
          piVar14 = (int *)CONCAT35(uStack_14b,local_150);
          if ((piVar14 != (int *)0x0) && (iVar9 = *piVar14, *piVar14 = iVar9 + -1, iVar9 + -1 == 0))
          {
            FUN_101449efc();
          }
        }
        FUN_101427680(&local_150,"all");
        if (local_120 < puStack_118) {
          *local_120 = 0;
          *local_120 = CONCAT35(uStack_14b,local_150);
          local_120 = local_120 + 1;
        }
        else {
          local_120 = (undefined8 *)FUN_1002b614c(&local_128,&local_150);
          piVar14 = (int *)CONCAT35(uStack_14b,local_150);
          if ((piVar14 != (int *)0x0) && (iVar9 = *piVar14, *piVar14 = iVar9 + -1, iVar9 + -1 == 0))
          {
            FUN_101449efc();
          }
        }
      }
      uStack_148 = (undefined5)_UNK_1058ca434;
      cStack_143 = (char)((ulong)_UNK_1058ca434 >> 0x28);
      cStack_142 = (char)((ulong)_UNK_1058ca434 >> 0x30);
      cStack_141 = (char)((ulong)_UNK_1058ca434 >> 0x38);
      local_150 = (uint5)_DAT_1058ca42c;
      uStack_14b = (undefined3)((ulong)_DAT_1058ca42c >> 0x28);
      uStack_138 = _UNK_1058ca444;
      uStack_140 = (undefined7)_DAT_1058ca43c;
      bStack_139 = (byte)((ulong)_DAT_1058ca43c >> 0x38);
      auVar29 = FUN_1011aeb80(&local_150);
      local_a0 = auVar29._0_8_;
      uStack_98 = auVar29._8_6_;
      uStack_92 = auVar29._14_2_;
      if (((auVar29._8_8_ & 1) != 0) && (uVar23 = FUN_1011ac014(&local_a0,1,0x32), 0 < (int)uVar23))
      {
        local_150 = (uint5)uVar23;
        uStack_14b = 0;
        uStack_148 = 0;
        cStack_143 = 0;
        cStack_142 = 0;
        cStack_141 = 0;
        FUN_10143e88c(&local_c0,L"--limit={}",10,1,&local_150);
        if (local_120 < puStack_118) {
          *local_120 = 0;
          *local_120 = local_c0;
          local_120 = local_120 + 1;
        }
        else {
          local_120 = (undefined8 *)FUN_1002b614c(&local_128,&local_c0);
          if ((local_c0 != (int *******)0x0) &&
             (iVar9 = *(int *)local_c0, *(int *)local_c0 = iVar9 + -1, iVar9 + -1 == 0)) {
            FUN_101449efc();
          }
        }
      }
      FUN_10142d468(&local_150,L"--lang");
      if (local_120 < puStack_118) {
        *local_120 = 0;
        *local_120 = CONCAT35(uStack_14b,local_150);
        local_120 = local_120 + 1;
      }
      else {
        local_120 = (undefined8 *)FUN_1002b614c(&local_128,&local_150);
        piVar14 = (int *)CONCAT35(uStack_14b,local_150);
        if ((piVar14 != (int *)0x0) && (iVar9 = *piVar14, *piVar14 = iVar9 + -1, iVar9 + -1 == 0)) {
          FUN_101449efc();
        }
      }
      FUN_1015041e0(&local_150);
      if (local_120 < puStack_118) {
        *local_120 = 0;
        *local_120 = CONCAT35(uStack_14b,local_150);
        local_120 = local_120 + 1;
      }
      else {
        local_120 = (undefined8 *)FUN_1002b614c(&local_128,&local_150);
        piVar14 = (int *)CONCAT35(uStack_14b,local_150);
        if ((piVar14 != (int *)0x0) && (iVar9 = *piVar14, *piVar14 = iVar9 + -1, iVar9 + -1 == 0)) {
          FUN_101449efc();
        }
      }
      uVar13 = std::chrono::system_clock::now();
      FUN_103f3ffec(&local_150,2,uVar13);
      iVar9 = FUN_103f3c8b8(&local_150);
      if (iVar9 != 0) {
        FUN_103f39a78(&local_150,"Plugins: start scanner process");
      }
      thunk_FUN_103f395e4(&local_150);
      local_158 = plVar10;
      FUN_1025da348(*(undefined8 *)(param_1 + 0x80),local_110,&local_128,&local_158,1,0);
      plVar10 = local_158;
      local_158 = (long *)0x0;
      if (plVar10 != (long *)0x0) {
        (**(code **)(*plVar10 + 8))();
      }
      puVar15 = local_128;
      puVar20 = local_120;
      if (local_128 != (undefined8 *)0x0) {
        while (puVar20 != puVar15) {
          puVar20 = puVar20 + -1;
          piVar14 = (int *)*puVar20;
          if ((piVar14 != (int *)0x0) && (iVar9 = *piVar14, *piVar14 = iVar9 + -1, iVar9 + -1 == 0))
          {
            FUN_101449efc();
          }
        }
        local_120 = puVar15;
        operator_delete(local_128);
      }
      if (local_f9 < '\0') {
        operator_delete(local_110[0]);
      }
      if ((local_f8 != (int *)0x0) && (iVar9 = *local_f8, *local_f8 = iVar9 + -1, iVar9 + -1 == 0))
      {
        FUN_101449efc();
      }
      if (*(long *)PTR____stack_chk_guard_1064f8818 != local_78) {
                    /* WARNING: Subroutine does not return */
        ___stack_chk_fail();
      }
      return;
    }
    if (plVar19[3] != plVar19[4]) {
      uVar23 = *(int *)(plVar19 + 2) - 4U >> 2;
      uVar5 = uVar23 | *(int *)(plVar19 + 2) << 0x1e;
      if ((uVar5 < 8) && ((0x8bU >> (ulong)(uVar23 & 0x1f) & 1) != 0)) {
        FUN_101427680(&local_150,(&PTR_s___au_1068d88f0)[uVar5]);
      }
      else {
        FUN_1011cb734(&local_150);
      }
      if (local_120 < puStack_118) {
        *local_120 = 0;
        *local_120 = CONCAT35(uStack_14b,local_150);
        local_120 = local_120 + 1;
      }
      else {
        local_120 = (undefined8 *)FUN_1002b614c(&local_128,&local_150);
        piVar14 = (int *)CONCAT35(uStack_14b,local_150);
        if ((piVar14 != (int *)0x0) && (iVar9 = *piVar14, *piVar14 = iVar9 + -1, iVar9 + -1 == 0)) {
          FUN_101449efc();
        }
      }
      puVar20 = (undefined8 *)plVar19[3];
      puVar15 = (undefined8 *)plVar19[4];
      local_f0 = (undefined8 *)0x0;
      local_e8 = (undefined8 *)0x0;
      local_e0 = (undefined8 *)0x0;
      lVar18 = (long)puVar15 - (long)puVar20;
      if (lVar18 != 0) {
        uVar21 = lVar18 >> 5;
        if (0xaaaaaaaaaaaaaaa < uVar21) {
          FUN_1002612d0(&local_f0);
LAB_10317aa88:
                    /* WARNING: Does not return */
          pcVar8 = (code *)SoftwareBreakpoint(1,0x10317aa8c);
          (*pcVar8)();
        }
        local_f0 = operator_new(uVar21 * 0x18);
        local_e0 = local_f0 + uVar21 * 3;
        local_e8 = local_f0;
        do {
          FUN_1014320f0(&local_a0,puVar20 + 3);
          uVar21 = (ulong)acStack_90[7];
          if ((long)uVar21 < 0) {
            uVar21 = CONCAT26(uStack_92,uStack_98);
            uVar24 = CONCAT17(acStack_90[7],CONCAT16(acStack_90[6],acStack_90._0_6_)) &
                     0x7fffffffffffffff;
            sVar27 = uVar24 - 1;
            pppppppiVar26 = local_a0;
            if (sVar27 == uVar21) {
              if (uVar24 == 0x7ffffffffffffff7) {
                    /* WARNING: Subroutine does not return */
                FUN_100234518(&local_a0);
              }
              uVar21 = 0x7ffffffffffffff7;
              if (sVar27 < 0x3ffffffffffffff3) goto LAB_10317a270;
              goto LAB_10317a298;
            }
LAB_10317a2e8:
            *(undefined1 *)((long)pppppppiVar26 + uVar21) = 0x3d;
            acStack_90[7] = (byte)(uVar21 + 1) & 0x7f;
            puVar16 = (undefined1 *)((long)pppppppiVar26 + uVar21 + 1);
          }
          else {
            pppppppiVar26 = (int *******)&local_a0;
            if (acStack_90[7] != '\x16') goto LAB_10317a2e8;
            uVar24 = 0x17;
            sVar27 = 0x16;
LAB_10317a270:
            uVar1 = uVar24;
            if (uVar24 <= sVar27 * 2) {
              uVar1 = sVar27 * 2;
            }
            uVar28 = 0x19;
            if ((uVar1 | 7) != 0x17) {
              uVar28 = (uVar1 | 7) + 1;
            }
            uVar21 = 0x17;
            if (0x16 < uVar1) {
              uVar21 = uVar28;
            }
LAB_10317a298:
            pppppppiVar11 = operator_new(uVar21);
            if (sVar27 != 0) {
              _memmove(pppppppiVar11,pppppppiVar26,sVar27);
            }
            *(undefined1 *)((long)pppppppiVar11 + sVar27) = 0x3d;
            if (sVar27 != 0x16) {
              operator_delete(pppppppiVar26);
            }
            acStack_90[7] = (byte)(uVar21 >> 0x38) | 0x80;
            uStack_98 = (undefined6)uVar24;
            uStack_92 = (undefined2)(uVar24 >> 0x30);
            acStack_90._0_6_ = (undefined6)uVar21;
            acStack_90[6] = (char)(uVar21 >> 0x30);
            puVar16 = (undefined1 *)((long)pppppppiVar11 + uVar24);
            local_a0 = pppppppiVar11;
          }
          *puVar16 = 0;
          uStack_148 = (undefined5)uStack_98;
          cStack_143 = SUB61(uStack_98,5);
          cStack_142 = (char)uStack_92;
          cStack_141 = SUB21(uStack_92,1);
          local_150 = (uint5)local_a0;
          uStack_14b = (undefined3)((ulong)local_a0 >> 0x28);
          uStack_140 = CONCAT16(acStack_90[6],acStack_90._0_6_);
          bStack_139 = acStack_90[7];
          uStack_98._0_1_ = '\0';
          uStack_98._1_1_ = '\0';
          uStack_98._2_1_ = '\0';
          uStack_98._3_1_ = '\0';
          uStack_98._4_1_ = '\0';
          uStack_98._5_1_ = '\0';
          uStack_92._0_1_ = '\0';
          uStack_92._1_1_ = '\0';
          acStack_90[0] = '\0';
          acStack_90[1] = '\0';
          acStack_90[2] = '\0';
          acStack_90[3] = '\0';
          acStack_90[4] = '\0';
          acStack_90[5] = '\0';
          acStack_90[6] = 0;
          acStack_90[7] = '\0';
          local_a0 = (int *******)0x0;
          if (*(char *)((long)puVar20 + 0x17) < '\0') {
            FUN_10023448c(&local_c0,*puVar20,puVar20[1]);
          }
          else {
            uStack_b8 = puVar20[1];
            local_c0 = (int *******)*puVar20;
            local_b0 = puVar20[2];
          }
          uVar23 = (uint)(char)local_b0._7_1_;
          uVar21 = uStack_b8;
          pppppppiVar26 = local_c0;
          if (-1 < (int)uVar23) {
            uVar21 = (ulong)local_b0._7_1_;
            pppppppiVar26 = (int *******)&local_c0;
          }
          uVar24 = (CONCAT17(bStack_139,uStack_140) & 0x7fffffffffffffff) - 1;
          sVar27 = CONCAT17(cStack_141,CONCAT16(cStack_142,CONCAT15(cStack_143,uStack_148)));
          if (-1 < (char)bStack_139) {
            uVar24 = 0x16;
            sVar27 = (ulong)bStack_139;
          }
          if (uVar24 - sVar27 < uVar21) {
            uVar1 = sVar27 + uVar21;
            if (~uVar24 + 0x7ffffffffffffff7 < uVar1 - uVar24) {
                    /* WARNING: Subroutine does not return */
              FUN_100234518(&local_150);
            }
            puVar3 = (uint5 *)CONCAT35(uStack_14b,local_150);
            if (-1 < (char)bStack_139) {
              puVar3 = &local_150;
            }
            uVar28 = 0x7ffffffffffffff7;
            if (uVar24 < 0x3ffffffffffffff3) {
              uVar2 = uVar1;
              if (uVar1 <= uVar24 * 2) {
                uVar2 = uVar24 * 2;
              }
              uVar4 = 0x19;
              if ((uVar2 | 7) != 0x17) {
                uVar4 = (uVar2 | 7) + 1;
              }
              uVar28 = 0x17;
              if (0x16 < uVar2) {
                uVar28 = uVar4;
              }
            }
            pvVar12 = operator_new(uVar28);
            if (sVar27 != 0) {
              _memmove(pvVar12,puVar3,sVar27);
            }
            _memcpy((void *)((long)pvVar12 + sVar27),pppppppiVar26,uVar21);
            if (uVar24 != 0x16) {
              operator_delete(puVar3);
            }
            bStack_139 = (byte)(uVar28 >> 0x38) | 0x80;
            uStack_148 = (undefined5)uVar1;
            cStack_143 = (char)(uVar1 >> 0x28);
            cStack_142 = (char)(uVar1 >> 0x30);
            cStack_141 = (char)(uVar1 >> 0x38);
            uStack_140 = (undefined7)uVar28;
            local_150 = (uint5)pvVar12;
            uStack_14b = (undefined3)((ulong)pvVar12 >> 0x28);
            puVar16 = (undefined1 *)((long)pvVar12 + uVar1);
LAB_10317a4b4:
            *puVar16 = 0;
            uVar23 = (uint)local_b0._7_1_;
            bVar6 = bStack_139;
          }
          else {
            bVar6 = bStack_139;
            if (uVar21 != 0) {
              puVar3 = (uint5 *)CONCAT35(uStack_14b,local_150);
              if (-1 < (char)bStack_139) {
                puVar3 = &local_150;
              }
              _memmove((void *)((long)puVar3 + sVar27),pppppppiVar26,uVar21);
              lVar18 = sVar27 + uVar21;
              if ((char)bStack_139 < '\0') {
                uStack_148 = (undefined5)lVar18;
                cStack_143 = (char)((ulong)lVar18 >> 0x28);
                cStack_142 = (char)((ulong)lVar18 >> 0x30);
                cStack_141 = (char)((ulong)lVar18 >> 0x38);
              }
              else {
                bStack_139 = (byte)lVar18 & 0x7f;
              }
              puVar16 = (undefined1 *)((long)puVar3 + lVar18);
              goto LAB_10317a4b4;
            }
          }
          uVar13 = CONCAT35(uStack_14b,local_150);
          local_88 = CONCAT16(cStack_142,CONCAT15(cStack_143,uStack_148));
          cStack_81 = cStack_141;
          uStack_80 = uStack_140;
          uStack_148._0_1_ = '\0';
          uStack_148._1_1_ = '\0';
          uStack_148._2_1_ = '\0';
          uStack_148._3_1_ = '\0';
          uStack_148._4_1_ = '\0';
          cStack_143 = 0;
          cStack_142 = 0;
          cStack_141 = 0;
          uStack_140 = 0;
          bStack_139 = '\0';
          local_150 = 0;
          uStack_14b._0_1_ = '\0';
          uStack_14b._1_1_ = '\0';
          uStack_14b._2_1_ = '\0';
          if (((uVar23 >> 7 & 1) != 0) && (operator_delete(local_c0), (char)bStack_139 < '\0')) {
            operator_delete((void *)CONCAT35(uStack_14b,local_150));
          }
          puVar7 = local_f0;
          if (local_e8 < local_e0) {
            *local_e8 = uVar13;
            local_e8[1] = CONCAT17(cStack_81,local_88);
            *(ulong *)((long)local_e8 + 0xf) = CONCAT71(uStack_80,cStack_81);
            *(byte *)((long)local_e8 + 0x17) = bVar6;
            puVar22 = local_e8 + 3;
          }
          else {
            sVar27 = (long)local_e8 - (long)local_f0;
            uVar21 = ((long)sVar27 >> 3) * -0x5555555555555555 + 1;
            if (0xaaaaaaaaaaaaaaa < uVar21) {
              FUN_1002612d0(&local_f0);
              goto LAB_10317aa88;
            }
            lVar18 = (long)local_e0 - (long)local_f0 >> 3;
            uVar24 = lVar18 * 0x5555555555555556;
            if (uVar24 < uVar21 || uVar24 - uVar21 == 0) {
              uVar24 = uVar21;
            }
            if (0x555555555555554 < (ulong)(lVar18 * -0x5555555555555555)) {
              uVar24 = 0xaaaaaaaaaaaaaaa;
            }
            if (uVar24 == 0) {
              pvVar12 = (void *)0x0;
            }
            else {
              if (0xaaaaaaaaaaaaaaa < uVar24) {
                    /* WARNING: Subroutine does not return */
                FUN_10024a858();
              }
              pvVar12 = operator_new(uVar24 * 0x18);
            }
            puVar17 = (undefined8 *)((long)pvVar12 + ((long)sVar27 >> 3) * 8);
            *puVar17 = uVar13;
            puVar17[1] = CONCAT17(cStack_81,local_88);
            puVar25 = (undefined8 *)((long)pvVar12 + uVar24 * 0x18);
            *(ulong *)((long)puVar17 + 0xf) = CONCAT71(uStack_80,cStack_81);
            *(byte *)((long)puVar17 + 0x17) = bVar6;
            puVar22 = puVar17 + 3;
            puVar17 = (undefined8 *)((long)puVar17 - sVar27);
            _memcpy(puVar17,puVar7,sVar27);
            local_f0 = puVar17;
            local_e0 = puVar25;
            if (puVar7 != (undefined8 *)0x0) {
              local_e8 = puVar22;
              operator_delete(puVar7);
            }
          }
          puVar20 = puVar20 + 4;
          local_e8 = puVar22;
        } while (puVar20 != puVar15);
      }
      FUN_10317ccdc(local_d8,&local_f0,",");
      FUN_101432b6c(&local_130,local_d8);
      if (local_c1 < '\0') {
        operator_delete(local_d8[0]);
        if (local_f0 != (undefined8 *)0x0) goto LAB_10317a620;
LAB_10317a694:
        if (local_120 < puStack_118) {
LAB_10317a0d0:
          *local_120 = 0;
          *local_120 = local_130;
          local_120 = local_120 + 1;
          goto LAB_10317a0e4;
        }
      }
      else {
        if (local_f0 == (undefined8 *)0x0) goto LAB_10317a694;
LAB_10317a620:
        if (local_e8 == local_f0) {
          local_e8 = local_f0;
          operator_delete(local_f0);
          if (puStack_118 <= local_120) goto LAB_10317a6a0;
          goto LAB_10317a0d0;
        }
        do {
          local_e8 = local_e8 + -3;
        } while (local_e8 != local_f0);
        local_e8 = local_f0;
        operator_delete(local_f0);
        if (local_120 < puStack_118) goto LAB_10317a0d0;
      }
LAB_10317a6a0:
      local_120 = (undefined8 *)FUN_1002b614c(&local_128,&local_130);
      if ((local_130 != (int *)0x0) &&
         (iVar9 = *local_130, *local_130 = iVar9 + -1, iVar9 + -1 == 0)) {
        FUN_101449efc();
      }
    }
LAB_10317a0e4:
    plVar19 = (long *)*plVar19;
  } while( true );
}

