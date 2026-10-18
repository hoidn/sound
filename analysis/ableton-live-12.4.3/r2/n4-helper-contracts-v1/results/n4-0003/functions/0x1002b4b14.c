
/* WARNING: Removing unreachable block (ram,0x0001002b4db4) */
/* WARNING: Removing unreachable block (ram,0x0001002b4d88) */
/* WARNING: Removing unreachable block (ram,0x0001002b4da4) */
/* WARNING: Removing unreachable block (ram,0x0001002b50f8) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1002b4b14(long param_1)

{
  undefined8 *******pppppppuVar1;
  int *******pppppppiVar2;
  undefined5 uVar3;
  undefined3 uVar4;
  pid_t pVar5;
  int iVar6;
  long *plVar7;
  undefined8 uVar8;
  int *piVar9;
  undefined8 *puVar10;
  ulong extraout_x1;
  ulong uVar11;
  undefined8 *puVar12;
  undefined8 uVar13;
  undefined1 auVar14 [16];
  long *local_1c0;
  undefined8 ******local_1b8;
  ulong uStack_1b0;
  byte bStack_1a1;
  int ******local_1a0;
  ulong uStack_198;
  undefined7 local_190;
  byte bStack_189;
  undefined8 ******local_188;
  ulong uStack_180;
  undefined7 local_178;
  byte bStack_171;
  void *local_170 [2];
  char local_159;
  int *local_158;
  undefined5 local_150;
  undefined4 uStack_14b;
  undefined4 uStack_147;
  char cStack_143;
  undefined2 uStack_142;
  undefined8 local_140;
  undefined8 uStack_138;
  undefined8 local_130;
  ulong uStack_128;
  undefined8 local_120;
  undefined8 ******local_118;
  ulong uStack_110;
  undefined8 local_108;
  char cStack_101;
  int *local_100;
  undefined8 ******local_f8;
  ulong uStack_f0;
  undefined8 local_e8;
  int *local_e0;
  int *local_d8;
  undefined1 local_d0;
  int *local_c8;
  undefined4 local_c0;
  undefined4 local_bc;
  undefined1 local_b8;
  undefined1 local_b7;
  int **local_90;
  undefined8 uStack_88;
  undefined8 local_80;
  long local_70;
  long *local_68;
  undefined1 local_60 [16];
  undefined8 ******local_48;
  ulong uStack_40;
  byte bStack_31;
  
  if ((DAT_106ec1cc0 & 1) == 0) {
    FUN_1053e9f88();
  }
  FUN_1014412dc(&local_158,7);
  plVar7 = operator_new(0x58);
  FUN_1014320f0(&local_150,&local_158);
  FUN_1002725dc(&local_130,&local_150,0);
  *plVar7 = (long)&PTR_thunk_FUN_10027a25c_1065928b0;
  plVar7[1] = (long)(plVar7 + 2);
  *(undefined8 *)((long)plVar7 + 0x14) = DAT_1055d3960;
  *(undefined4 *)((long)plVar7 + 0x1c) = 0xffffffff;
  if (local_120 < 0) {
    FUN_10023448c(plVar7 + 4,local_130,uStack_128);
    *(undefined4 *)(plVar7 + 7) = 0;
    plVar7[9] = 0;
    plVar7[10] = 0;
    plVar7[8] = 0;
    if (local_120 < 0) {
      operator_delete(local_130);
    }
  }
  else {
    plVar7[5] = uStack_128;
    plVar7[4] = (long)local_130;
    plVar7[6] = local_120;
    *(undefined4 *)(plVar7 + 7) = 0;
    plVar7[9] = 0;
    plVar7[10] = 0;
    plVar7[8] = 0;
  }
  local_130._6_2_ = (undefined2)((ulong)local_130 >> 0x30);
  if (local_140 < 0) {
    operator_delete((void *)CONCAT35((undefined3)uStack_14b,local_150));
  }
  local_130 = (int *******)CONCAT26(local_130._6_2_,0x7865646e49);
  local_120._7_1_ = '\x05';
  local_150._0_1_ = s_Ableton_Index_105aabd80[0];
  local_150._1_1_ = s_Ableton_Index_105aabd80[1];
  local_150._2_1_ = s_Ableton_Index_105aabd80[2];
  local_150._3_1_ = s_Ableton_Index_105aabd80[3];
  local_150._4_1_ = s_Ableton_Index_105aabd80[4];
  uStack_14b = (undefined4)CONCAT53(s_Ableton_Index_105aabd80._8_5_,s_Ableton_Index_105aabd80._5_3_)
  ;
  uStack_147 = SUB54(s_Ableton_Index_105aabd80._8_5_,1);
  cStack_143 = 0;
  local_140 = CONCAT17(0xd,(undefined7)local_140);
  FUN_1011e8540(local_170,&local_130,&local_150);
  if (local_140 < 0) {
    operator_delete((void *)CONCAT35((undefined3)uStack_14b,local_150));
  }
  if (local_120._7_1_ < '\0') {
    operator_delete(local_130);
  }
  (**(code **)(**(long **)(param_1 + 0x28) + 0xa58))(&local_1a0);
  FUN_1002e957c(&local_1b8,*(undefined8 *)(param_1 + 0x28));
  FUN_1011db938(&local_70);
  (**(code **)(*local_68 + 0x78))(local_60);
  uStack_14b._3_1_ = (char)s_com_ableton_index__105aabdc8._8_8_;
  uStack_147 = SUB84(s_com_ableton_index__105aabdc8._8_8_,1);
  cStack_143 = SUB81(s_com_ableton_index__105aabdc8._8_8_,5);
  uStack_142 = SUB82(s_com_ableton_index__105aabdc8._8_8_,6);
  local_150 = (undefined5)s_com_ableton_index__105aabdc8._0_8_;
  uStack_14b._0_3_ = SUB83(s_com_ableton_index__105aabdc8._0_8_,5);
  local_140 = CONCAT53(local_140._3_5_,0x2e78);
  local_140 = CONCAT17(0x12,(undefined7)local_140);
  FUN_1014320f0(&local_48,&local_158);
  uVar11 = uStack_40;
  pppppppuVar1 = (undefined8 *******)local_48;
  if (-1 < (char)bStack_31) {
    uVar11 = (ulong)bStack_31;
    pppppppuVar1 = &local_48;
  }
  FUN_10025dc7c(&local_150,pppppppuVar1,(long)pppppppuVar1 + uVar11);
  uStack_128 = CONCAT26(uStack_142,CONCAT15(cStack_143,CONCAT41(uStack_147,uStack_14b._3_1_)));
  local_130 = (int *******)CONCAT35((undefined3)uStack_14b,local_150);
  local_120 = local_140;
  uStack_147 = 0;
  cStack_143 = 0;
  uStack_142 = 0;
  local_140 = 0;
  local_150 = 0;
  uStack_14b = 0;
  FUN_10025dc7c(&local_130,".txt","");
  uStack_88 = uStack_128;
  local_90 = (int **)local_130;
  local_80 = local_120;
  uStack_128 = 0;
  local_120 = 0;
  local_130 = (int *******)0x0;
  if (local_140 < 0) {
    operator_delete((void *)CONCAT35((undefined3)uStack_14b,local_150));
  }
  FUN_100241e54(&local_188,local_60,&local_90);
  if ((local_70 != 0) &&
     (iVar6 = *(int *)(local_70 + 8) + -1, *(int *)(local_70 + 8) = iVar6, iVar6 == 0)) {
    FUN_10128eea0();
  }
  FUN_1002b5f04(&local_130);
  if (local_158 != (int *)0x0) {
    *local_158 = *local_158 + 1;
  }
  if ((local_100 != (int *)0x0) && (iVar6 = *local_100, *local_100 = iVar6 + -1, iVar6 + -1 == 0)) {
    FUN_101449efc();
  }
  FUN_101455cc8();
  FUN_1014565d0(&local_48);
  local_150 = 0x65646e692e;
  uStack_14b = 0x726578;
  local_140._7_1_ = '\b';
  FUN_103f62520(&local_48,&local_150);
  if (local_140._7_1_ < '\0') {
    operator_delete((void *)CONCAT35((undefined3)uStack_14b,local_150));
    uVar11 = (ulong)bStack_31;
    if (-1 < local_e8._7_1_) goto LAB_1002b4e68;
  }
  else {
    uVar11 = (ulong)bStack_31;
    if (-1 < local_e8) {
LAB_1002b4e68:
      if ((uint)uVar11 >> 7 == 0) {
        uStack_f0 = uStack_40;
        local_f8 = local_48;
      }
      else {
        FUN_100251b18(&local_f8,local_48,uStack_40);
      }
      goto LAB_1002b4ec8;
    }
  }
  if (-1 < (char)uVar11) {
    uStack_40 = uVar11;
    local_48 = &local_48;
  }
  FUN_100251bd8(&local_f8,local_48,uStack_40);
LAB_1002b4ec8:
  pVar5 = _getpid();
  FUN_101430a10(&local_150,pVar5);
  piVar9 = (int *)CONCAT35((undefined3)uStack_14b,local_150);
  local_150 = SUB85(local_e0,0);
  uStack_14b._0_3_ = (undefined3)((ulong)local_e0 >> 0x28);
  if ((local_e0 != (int *)0x0) && (iVar6 = *local_e0, *local_e0 = iVar6 + -1, iVar6 + -1 == 0)) {
    local_e0 = piVar9;
    FUN_101449efc();
    piVar9 = local_e0;
  }
  local_e0 = piVar9;
  if (local_120 < 0) {
    pppppppiVar2 = (int *******)local_1a0;
    if (-1 < (char)bStack_189) {
      uStack_198 = (ulong)bStack_189;
      pppppppiVar2 = &local_1a0;
    }
    FUN_100251bd8(&local_130,pppppppiVar2,uStack_198);
  }
  else if ((char)bStack_189 < '\0') {
    FUN_100251b18(&local_130,local_1a0,uStack_198);
  }
  else {
    uStack_128 = uStack_198;
    local_130 = (int *******)local_1a0;
    local_120 = CONCAT17(bStack_189,local_190);
  }
  if (cStack_101 < '\0') {
    pppppppuVar1 = (undefined8 *******)local_1b8;
    if (-1 < (char)bStack_1a1) {
      uStack_1b0 = (ulong)bStack_1a1;
      pppppppuVar1 = &local_1b8;
    }
    FUN_100251bd8(&local_118,pppppppuVar1,uStack_1b0);
  }
  else if ((char)bStack_1a1 < '\0') {
    FUN_100251b18(&local_118,local_1b8,uStack_1b0);
  }
  else {
    uStack_110 = uStack_1b0;
    local_118 = local_1b8;
  }
  uStack_14b._3_1_ = (char)_UNK_1055d76fc;
  uStack_147 = (undefined4)((ulong)_UNK_1055d76fc >> 8);
  cStack_143 = (char)((ulong)_UNK_1055d76fc >> 0x28);
  uStack_142 = (undefined2)((ulong)_UNK_1055d76fc >> 0x30);
  local_150 = (undefined5)_DAT_1055d76f4;
  uStack_14b._0_3_ = (undefined3)((ulong)_DAT_1055d76f4 >> 0x28);
  uStack_138 = _UNK_1055d770c;
  local_140 = _DAT_1055d7704;
  local_60 = FUN_1011aeb80(&local_150);
  piVar9 = local_d8;
  if ((local_60._8_8_ & 1) != 0) {
    FUN_1011abfa4(local_60);
    FUN_101427680(&local_150);
    piVar9 = (int *)CONCAT35((undefined3)uStack_14b,local_150);
    local_150 = SUB85(local_d8,0);
    uStack_14b._0_3_ = (undefined3)((ulong)local_d8 >> 0x28);
    if ((local_d8 != (int *)0x0) && (iVar6 = *local_d8, *local_d8 = iVar6 + -1, iVar6 + -1 == 0)) {
      local_d8 = piVar9;
      FUN_101449efc();
      piVar9 = local_d8;
    }
  }
  local_d8 = piVar9;
  uStack_14b._3_1_ = (char)_UNK_1055d771c;
  uStack_147 = (undefined4)((ulong)_UNK_1055d771c >> 8);
  cStack_143 = (char)((ulong)_UNK_1055d771c >> 0x28);
  uStack_142 = (undefined2)((ulong)_UNK_1055d771c >> 0x30);
  local_150 = (undefined5)_DAT_1055d7714;
  uStack_14b._0_3_ = (undefined3)((ulong)_DAT_1055d7714 >> 0x28);
  uStack_138 = _UNK_1055d772c;
  local_140 = _DAT_1055d7724;
  FUN_1011aeb80(&local_150);
  if ((extraout_x1 & 1) != 0) {
    local_d0 = 1;
  }
  uStack_14b._3_1_ = (char)_UNK_1055d773c;
  uStack_147 = (undefined4)((ulong)_UNK_1055d773c >> 8);
  cStack_143 = (char)((ulong)_UNK_1055d773c >> 0x28);
  uStack_142 = (undefined2)((ulong)_UNK_1055d773c >> 0x30);
  local_150 = (undefined5)_DAT_1055d7734;
  uStack_14b._0_3_ = (undefined3)((ulong)_DAT_1055d7734 >> 0x28);
  uStack_138 = _UNK_1055d774c;
  local_140 = _DAT_1055d7744;
  auVar14 = FUN_1011aeb80(&local_150);
  piVar9 = local_c8;
  local_60 = auVar14;
  if ((auVar14._8_8_ & 1) != 0) {
    FUN_1011abfa4(local_60);
    FUN_101427680(&local_150);
    piVar9 = (int *)CONCAT35((undefined3)uStack_14b,local_150);
    local_150 = SUB85(local_c8,0);
    uStack_14b._0_3_ = (undefined3)((ulong)local_c8 >> 0x28);
    if ((local_c8 != (int *)0x0) && (iVar6 = *local_c8, *local_c8 = iVar6 + -1, iVar6 + -1 == 0)) {
      local_c8 = piVar9;
      FUN_101449efc();
      piVar9 = local_c8;
    }
  }
  local_c8 = piVar9;
  local_c0 = FUN_10122ed30();
  local_bc = FUN_10122ed88();
  local_b8 = FUN_100237fe8();
  local_b7 = FUN_10326fa58();
  FUN_10163abe4(&local_130,&local_188);
  FUN_1002b5ff8(&local_130);
  if ((char)bStack_1a1 < '\0') {
    operator_delete(local_1b8);
  }
  if ((char)bStack_189 < '\0') {
    operator_delete(local_1a0);
  }
  if (DAT_106ec20f8 < 0) {
    pppppppuVar1 = (undefined8 *******)local_188;
    if (-1 < (char)bStack_171) {
      uStack_180 = (ulong)bStack_171;
      pppppppuVar1 = &local_188;
    }
    FUN_100251bd8(&DAT_106ec20e8,pppppppuVar1,uStack_180);
  }
  else if ((char)bStack_171 < '\0') {
    FUN_100251b18(&DAT_106ec20e8,local_188,uStack_180);
  }
  else {
    DAT_106ec20f8 = CONCAT17(bStack_171,local_178);
    _DAT_106ec20e8 = (undefined8 *******)local_188;
    uRam0000000106ec20f0 = uStack_180;
  }
  thunk_FUN_101432b6c(&local_130,&local_188);
  FUN_1002b5da4(&local_150,&local_130);
  if ((local_130 != (int *******)0x0) &&
     (iVar6 = *(int *)local_130, *(int *)local_130 = iVar6 + -1, iVar6 + -1 == 0)) {
    FUN_101449efc();
  }
  uVar8 = std::chrono::system_clock::now();
  FUN_103f3ffec(&local_130,2,uVar8);
  iVar6 = FUN_103f3c8b8(&local_130);
  if (iVar6 != 0) {
    FUN_103f39a78(&local_130,"Indexer: start process");
  }
  thunk_FUN_103f395e4(&local_130);
  uVar13 = *(undefined8 *)(param_1 + 0x30);
  uStack_128 = _UNK_1055d775c;
  local_130 = (int *******)_DAT_1055d7754;
  local_118 = _UNK_1055d776c;
  local_120 = _DAT_1055d7764;
  local_1c0 = plVar7;
  uVar8 = FUN_1014416b0(&local_130,2);
  FUN_1025da348(uVar13,local_170,&local_150,&local_1c0,1,uVar8);
  plVar7 = local_1c0;
  local_1c0 = (long *)0x0;
  if (plVar7 != (long *)0x0) {
    (**(code **)(*plVar7 + 8))();
  }
  uVar4 = (undefined3)uStack_14b;
  uVar3 = local_150;
  *(int *)(param_1 + 0x4c) = *(int *)(param_1 + 0x4c) + 1;
  puVar10 = (undefined8 *)CONCAT35((undefined3)uStack_14b,local_150);
  if (puVar10 != (undefined8 *)0x0) {
    puVar12 = (undefined8 *)
              CONCAT26(uStack_142,CONCAT15(cStack_143,CONCAT41(uStack_147,uStack_14b._3_1_)));
    if (puVar12 != puVar10) {
      do {
        puVar12 = puVar12 + -1;
        piVar9 = (int *)*puVar12;
        if ((piVar9 != (int *)0x0) && (iVar6 = *piVar9, *piVar9 = iVar6 + -1, iVar6 + -1 == 0)) {
          FUN_101449efc();
        }
      } while (puVar12 != puVar10);
      puVar10 = (undefined8 *)CONCAT35((undefined3)uStack_14b,local_150);
    }
    uStack_14b._3_1_ = (char)uVar3;
    uStack_147 = (undefined4)((uint5)uVar3 >> 8);
    cStack_143 = (char)uVar4;
    uStack_142 = (undefined2)((uint3)uVar4 >> 8);
    operator_delete(puVar10);
  }
  if ((char)bStack_171 < '\0') {
    operator_delete(local_188);
  }
  if (local_159 < '\0') {
    operator_delete(local_170[0]);
  }
  if ((local_158 != (int *)0x0) && (iVar6 = *local_158, *local_158 = iVar6 + -1, iVar6 + -1 == 0)) {
    FUN_101449efc();
  }
  return;
}

