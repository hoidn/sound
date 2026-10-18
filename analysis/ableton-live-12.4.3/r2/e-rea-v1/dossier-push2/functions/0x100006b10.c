
/* WARNING: Removing unreachable block (ram,0x0001000080cc) */
/* WARNING: Removing unreachable block (ram,0x000100008048) */
/* WARNING: Removing unreachable block (ram,0x000100007c30) */
/* WARNING: Removing unreachable block (ram,0x000100007acc) */
/* WARNING: Removing unreachable block (ram,0x000100007960) */
/* WARNING: Removing unreachable block (ram,0x000100007700) */
/* WARNING: Removing unreachable block (ram,0x000100007304) */
/* WARNING: Removing unreachable block (ram,0x00010000731c) */
/* WARNING: Removing unreachable block (ram,0x000100007208) */
/* WARNING: Removing unreachable block (ram,0x0001000071e8) */
/* WARNING: Removing unreachable block (ram,0x0001000071f8) */
/* WARNING: Removing unreachable block (ram,0x000100007124) */
/* WARNING: Removing unreachable block (ram,0x0001000074dc) */
/* WARNING: Removing unreachable block (ram,0x0001000078b8) */
/* WARNING: Removing unreachable block (ram,0x00010000799c) */
/* WARNING: Removing unreachable block (ram,0x000100007b90) */
/* WARNING: Removing unreachable block (ram,0x000100007c6c) */
/* WARNING: Removing unreachable block (ram,0x000100008064) */
/* WARNING: Removing unreachable block (ram,0x0001000083c8) */
/* WARNING: Removing unreachable block (ram,0x0001000081ec) */
/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 entry(int param_1,char **param_2)

{
  char *pcVar1;
  ulong uVar2;
  undefined8 uVar3;
  undefined *puVar4;
  undefined4 uVar5;
  int iVar6;
  undefined8 *puVar7;
  undefined8 uVar8;
  undefined8 uVar9;
  size_t sVar10;
  QDir *this;
  QArrayData *pQVar11;
  undefined4 *puVar12;
  QString *pQVar13;
  undefined4 uVar14;
  char *pcVar15;
  uint uVar16;
  QArrayData *pQVar17;
  undefined8 *******pppppppuVar18;
  QArrayData *pQVar19;
  long lVar20;
  uint local_2f8;
  undefined4 uStack_2f4;
  char *local_2f0;
  ulong local_2e8;
  long lStack_2e0;
  undefined8 *******local_2d8;
  QArrayData *pQStack_2d0;
  undefined8 local_2c8;
  undefined8 local_2c0;
  undefined1 auStack_2b0 [8];
  undefined8 local_2a8;
  undefined1 auStack_298 [8];
  undefined8 local_290;
  void **local_268;
  char *local_260;
  char *local_258;
  ulong uStack_250;
  void *local_238 [2];
  char local_221;
  undefined1 local_1d0;
  undefined7 uStack_1cf;
  char local_1b9;
  char local_1b8;
  undefined7 uStack_1b7;
  char local_1a1;
  char local_1a0;
  undefined7 uStack_19f;
  ulong local_198;
  byte local_189;
  char local_188;
  undefined7 uStack_187;
  ulong local_180;
  byte local_171;
  undefined4 local_16c;
  undefined1 local_165;
  undefined4 local_164;
  undefined8 *******local_160;
  QArrayData *pQStack_158;
  undefined8 local_150;
  void *local_140;
  ulong local_138;
  ulong local_130;
  void *local_128;
  undefined1 local_120;
  char local_111;
  Connection aCStack_110 [8];
  long *local_108;
  QArrayData *local_100 [2];
  QUrl aQStack_f0 [8];
  undefined8 local_e8;
  QArrayData *local_d8 [2];
  undefined1 local_c1;
  QArrayData *local_c0 [2];
  QArrayData *local_b0;
  int local_a4;
  QArrayData *local_a0;
  QArrayData *pQStack_98;
  undefined8 local_90;
  QArrayData *local_88;
  QArrayData *pQStack_80;
  undefined8 local_78;
  
  FUN_1000143b0();
  local_111 = '\b';
  local_130 = 0;
  local_128 = (void *)0x6370693268737570;
  local_120 = 0;
  local_140 = (void *)0x0;
  local_138 = 0;
  FUN_100008ca0(local_238);
  local_260 = operator_new(0x19);
  uVar8 = s_Push2DisplayProcess_log_100280fd2._0_8_;
  *(ulong *)(local_260 + 8) =
       CONCAT17(s_Push2DisplayProcess_log_100280fd2[0xf],s_Push2DisplayProcess_log_100280fd2._8_7_);
  *(undefined8 *)local_260 = uVar8;
  *(ulong *)(local_260 + 0xf) =
       CONCAT71(s_Push2DisplayProcess_log_100280fd2._16_7_,s_Push2DisplayProcess_log_100280fd2[0xf])
  ;
  local_260[0x17] = '\0';
  uStack_250 = _UNK_1002374c8;
  local_258 = _DAT_1002374c0;
  FUN_100008b90(&local_2d8,local_238,&local_260);
  pppppppuVar18 = local_2d8;
  pQVar17 = pQStack_2d0;
  lVar20 = local_2c8;
  if ((local_2c8 < 0) &&
     (FUN_100005a5c(&local_160,local_2d8,pQStack_2d0), pppppppuVar18 = local_160,
     pQVar17 = pQStack_158, lVar20 = local_150, local_2c8 < 0)) {
    operator_delete(local_2d8);
    pppppppuVar18 = local_160;
    pQVar17 = pQStack_158;
    lVar20 = local_150;
  }
  local_150 = lVar20;
  pQStack_158 = pQVar17;
  local_160 = pppppppuVar18;
  if ((long)uStack_250 < 0) {
    operator_delete(local_260);
  }
  if (local_221 < '\0') {
    operator_delete(local_238[0]);
  }
  local_164 = 2;
  local_165 = 0;
  local_16c = 0;
  local_171 = 0;
  local_188 = '\0';
  local_189 = 0;
  local_1a0 = '\0';
  local_1a1 = '\0';
  local_1b8 = '\0';
  local_1b9 = '\0';
  local_1d0 = 0;
  local_2d8 = operator_new(0x20);
  uVar8 = s_Push_2_Display_Process_options_100280feb._0_8_;
  local_2c8 = _UNK_1002374d8;
  pQStack_2d0 = (QArrayData *)_DAT_1002374d0;
  local_2d8[1] = (undefined8 ******)
                 CONCAT26(s_Push_2_Display_Process_options_100280feb._14_2_,
                          s_Push_2_Display_Process_options_100280feb._8_6_);
  *local_2d8 = (undefined8 ******)uVar8;
  uVar8 = CONCAT62(s_Push_2_Display_Process_options_100280feb._16_6_,
                   s_Push_2_Display_Process_options_100280feb._14_2_);
  *(undefined8 *)((long)local_2d8 + 0x16) = s_Push_2_Display_Process_options_100280feb._22_8_;
  *(undefined8 *)((long)local_2d8 + 0xe) = uVar8;
  *(char *)((long)local_2d8 + 0x1e) = '\0';
  FUN_10010d898(local_238,&local_2d8,DAT_10024c14c,DAT_10024c14c >> 1);
  if (local_2c8 < 0) {
    operator_delete(local_2d8);
  }
  local_c0[0] = (QArrayData *)FUN_10010dbcc(local_238);
  puVar7 = operator_new(0x98);
  *puVar7 = &PTR_FUN_10029df08;
  puVar7[1] = &PTR_FUN_10029df78;
  puVar7[2] = &local_128;
  puVar7[0xf] = 0;
  puVar7[4] = 0;
  puVar7[3] = 0;
  puVar7[6] = 0;
  puVar7[5] = 0;
  puVar7[8] = 0;
  puVar7[7] = 0;
  puVar7[10] = 0;
  puVar7[9] = 0;
  puVar7[0xc] = 0;
  puVar7[0xb] = 0;
  *(undefined8 *)((long)puVar7 + 0x6d) = 0;
  *(undefined8 *)((long)puVar7 + 0x65) = 0;
  local_2c8 = CONCAT17(8,(undefined7)local_2c8);
  local_2d8 = (undefined8 *******)0x6370693268737570;
  pQStack_2d0 = (QArrayData *)((ulong)pQStack_2d0 & 0xffffffffffffff00);
  uVar8 = FUN_100008f5c(puVar7,&local_2d8);
  uVar8 = FUN_10010d62c(local_c0,"push2-ipc-channel",uVar8,
                        "Set the ipc channel to connect to. Default is \'push2ipc\'");
  puVar7 = operator_new(0x98);
  *puVar7 = &PTR_FUN_10029df08;
  puVar7[1] = &PTR_FUN_10029df78;
  puVar7[2] = &local_160;
  puVar7[0xf] = 0;
  puVar7[4] = 0;
  puVar7[3] = 0;
  puVar7[6] = 0;
  puVar7[5] = 0;
  puVar7[8] = 0;
  puVar7[7] = 0;
  puVar7[10] = 0;
  puVar7[9] = 0;
  puVar7[0xc] = 0;
  puVar7[0xb] = 0;
  *(undefined8 *)((long)puVar7 + 0x6d) = 0;
  *(undefined8 *)((long)puVar7 + 0x65) = 0;
  uVar8 = FUN_10010d62c(uVar8,"push2-log-file",puVar7,
                        "Set the log file path. Default is \'Push2DisplayProcess.log\' within the preferences folder"
                       );
  puVar7 = operator_new(0x98);
  *puVar7 = &PTR_FUN_10029e1c0;
  puVar7[1] = &PTR_FUN_10029e230;
  puVar7[2] = &local_164;
  puVar7[0xf] = 0;
  puVar7[4] = 0;
  puVar7[3] = 0;
  puVar7[6] = 0;
  puVar7[5] = 0;
  puVar7[8] = 0;
  puVar7[7] = 0;
  puVar7[10] = 0;
  puVar7[9] = 0;
  puVar7[0xc] = 0;
  puVar7[0xb] = 0;
  *(undefined8 *)((long)puVar7 + 0x6d) = 0;
  *(undefined8 *)((long)puVar7 + 0x65) = 0;
  uVar8 = FUN_10010d62c(uVar8,"push2-log-level",puVar7,"Set the log-level. Default is \'info\'");
  puVar7 = operator_new(0x98);
  *puVar7 = &PTR_FUN_10029e5d8;
  puVar7[1] = &PTR_FUN_10029e648;
  puVar7[2] = &local_16c;
  puVar7[0xf] = 0;
  puVar7[4] = 0;
  puVar7[3] = 0;
  puVar7[6] = 0;
  puVar7[5] = 0;
  puVar7[8] = 0;
  puVar7[7] = 0;
  puVar7[10] = 0;
  puVar7[9] = 0;
  puVar7[0xc] = 0;
  puVar7[0xb] = 0;
  *(undefined8 *)((long)puVar7 + 0x6d) = 0;
  *(undefined8 *)((long)puVar7 + 0x65) = 0;
  local_e8 = (undefined **)((ulong)local_e8._4_4_ << 0x20);
  uVar9 = FUN_10000906c(puVar7,&local_e8);
  uVar8 = FUN_10010d62c(uVar8,"push2-parent-process-id",uVar9,
                        "Set parent process id to watch out for. Default is 0 and disables checking"
                       );
  uVar9 = FUN_10011345c(&local_165);
  uVar8 = FUN_10010d62c(uVar8,"push2-log-to-console",uVar9,"Log additionally to the console");
  puVar7 = operator_new(0x98);
  *puVar7 = &PTR_FUN_10029df08;
  puVar7[1] = &PTR_FUN_10029df78;
  puVar7[2] = &local_188;
  puVar7[0xf] = 0;
  puVar7[4] = 0;
  puVar7[3] = 0;
  puVar7[6] = 0;
  puVar7[5] = 0;
  puVar7[8] = 0;
  puVar7[7] = 0;
  puVar7[10] = 0;
  puVar7[9] = 0;
  puVar7[0xc] = 0;
  puVar7[0xb] = 0;
  *(undefined8 *)((long)puVar7 + 0x6d) = 0;
  *(undefined8 *)((long)puVar7 + 0x65) = 0;
  uStack_250 = uStack_250 & 0xffffffffffffff;
  local_260 = (char *)((ulong)local_260 & 0xffffffffffffff00);
  uVar9 = FUN_100008f5c(puVar7,&local_260);
  uVar8 = FUN_10010d62c(uVar8,"push2-model-playback-root",uVar9,
                        "Root filename of screengrabs stored if push2-model-recording-filename is set"
                       );
  puVar7 = operator_new(0x98);
  *puVar7 = &PTR_FUN_10029df08;
  puVar7[1] = &PTR_FUN_10029df78;
  puVar7[2] = &local_1a0;
  puVar7[0xf] = 0;
  puVar7[4] = 0;
  puVar7[3] = 0;
  puVar7[6] = 0;
  puVar7[5] = 0;
  puVar7[8] = 0;
  puVar7[7] = 0;
  puVar7[10] = 0;
  puVar7[9] = 0;
  puVar7[0xc] = 0;
  puVar7[0xb] = 0;
  *(undefined8 *)((long)puVar7 + 0x6d) = 0;
  *(undefined8 *)((long)puVar7 + 0x65) = 0;
  local_2e8 = local_2e8 & 0xffffffffffffff;
  local_2f8 = local_2f8 & 0xffffff00;
  uVar9 = FUN_100008f5c(puVar7,&local_2f8);
  uVar8 = FUN_10010d62c(uVar8,"push2-model-recording-filename",uVar9,
                        "File to record model changes to if push2-model-playback-root is not set, or file to read model changes from if push2-model-playback-root is set"
                       );
  puVar7 = operator_new(0x98);
  *puVar7 = &PTR_FUN_10029df08;
  puVar7[1] = &PTR_FUN_10029df78;
  puVar7[2] = &local_1b8;
  puVar7[0xf] = 0;
  puVar7[4] = 0;
  puVar7[3] = 0;
  puVar7[6] = 0;
  puVar7[5] = 0;
  puVar7[8] = 0;
  puVar7[7] = 0;
  puVar7[10] = 0;
  puVar7[9] = 0;
  puVar7[0xc] = 0;
  puVar7[0xb] = 0;
  *(undefined8 *)((long)puVar7 + 0x6d) = 0;
  *(undefined8 *)((long)puVar7 + 0x65) = 0;
  local_78 = local_78 & 0xffffffffffffff;
  local_88 = (QArrayData *)((ulong)local_88 & 0xffffffffffffff00);
  uVar9 = FUN_100008f5c(puVar7,&local_88);
  uVar8 = FUN_10010d62c(uVar8,"push2-screenshot-filename",uVar9,
                        "Filename to write a PNG of the screen every 300ms");
  puVar7 = operator_new(0x98);
  *puVar7 = &PTR_FUN_10029df08;
  puVar7[1] = &PTR_FUN_10029df78;
  puVar7[2] = &local_140;
  puVar7[0xf] = 0;
  puVar7[4] = 0;
  puVar7[3] = 0;
  puVar7[6] = 0;
  puVar7[5] = 0;
  puVar7[8] = 0;
  puVar7[7] = 0;
  puVar7[10] = 0;
  puVar7[9] = 0;
  puVar7[0xc] = 0;
  puVar7[0xb] = 0;
  *(undefined8 *)((long)puVar7 + 0x6d) = 0;
  *(undefined8 *)((long)puVar7 + 0x65) = 0;
  local_90 = local_90 & 0xffffffffffffff;
  local_a0 = (QArrayData *)((ulong)local_a0 & 0xffffffffffffff00);
  uVar9 = FUN_100008f5c(puVar7,&local_a0);
  uVar8 = FUN_10010d62c(uVar8,"push2-graphwiz-uri",uVar9,
                        "If given, connect to this URI to monitor the Watchdog state automata");
  puVar7 = operator_new(0x98);
  *puVar7 = &PTR_FUN_10029df08;
  puVar7[1] = &PTR_FUN_10029df78;
  puVar7[2] = &local_1d0;
  puVar7[0xf] = 0;
  puVar7[4] = 0;
  puVar7[3] = 0;
  puVar7[6] = 0;
  puVar7[5] = 0;
  puVar7[8] = 0;
  puVar7[7] = 0;
  puVar7[10] = 0;
  puVar7[9] = 0;
  puVar7[0xc] = 0;
  puVar7[0xb] = 0;
  *(undefined8 *)((long)puVar7 + 0x6d) = 0;
  *(undefined8 *)((long)puVar7 + 0x65) = 0;
  local_c1 = 2;
  local_d8[0] = (QArrayData *)CONCAT53(local_d8[0]._3_5_,0x4e45);
  uVar9 = FUN_100008f5c(puVar7,local_d8);
  FUN_10010d62c(uVar8,"push2-language",uVar9,
                "The language Push 2 should display in (used for specifying the CJK font.");
  if ((long)local_2e8 < 0) {
    operator_delete((void *)CONCAT44(uStack_2f4,local_2f8));
  }
  if ((long)uStack_250 < 0) {
    operator_delete(local_260);
  }
  if (local_2c8 < 0) {
    operator_delete(local_2d8);
  }
  puVar4 = PTR_sArgs_10029d1e8;
  FUN_100013a90(&local_2f8,PTR_sArgs_10029d1e8);
  FUN_10010351c(&local_2d8,&local_2f8);
  lVar20 = CONCAT44(uStack_2f4,local_2f8);
  if (lVar20 != 0) {
    for (; local_2f0 != (char *)lVar20; local_2f0 = (char *)((long)local_2f0 + -0x18)) {
    }
    local_2f0 = (char *)lVar20;
    operator_delete((void *)CONCAT44(uStack_2f4,local_2f8));
  }
  FUN_100103a80(&local_2d8,local_238);
  local_268 = local_238;
  FUN_1000091a8(&local_260,&local_2d8);
  FUN_1000093cc(&local_2d8);
  FUN_10011a34c(&local_2d8);
  FUN_100119388(&local_260,&local_2d8,0);
  thunk_FUN_10011a134(&local_2d8);
  local_2f8 = QCoreApplication::applicationPid();
  uStack_2f4 = local_16c;
  local_2f0 = operator_new(0x30);
  uVar3 = s_e3d8be4d07c71dbd4de9e4183bf90652_10028136b._24_8_;
  uVar9 = s_e3d8be4d07c71dbd4de9e4183bf90652_10028136b._16_8_;
  uVar8 = s_e3d8be4d07c71dbd4de9e4183bf90652_10028136b._0_8_;
  lStack_2e0 = _UNK_1002374e8;
  local_2e8 = _DAT_1002374e0;
  *(undefined8 *)(local_2f0 + 8) = s_e3d8be4d07c71dbd4de9e4183bf90652_10028136b._8_8_;
  *(undefined8 *)local_2f0 = uVar8;
  *(undefined8 *)(local_2f0 + 0x18) = uVar3;
  *(undefined8 *)(local_2f0 + 0x10) = uVar9;
  *(undefined8 *)(local_2f0 + 0x20) = s_e3d8be4d07c71dbd4de9e4183bf90652_10028136b._32_8_;
  local_2f0[0x28] = '\0';
  pQVar17 = (QArrayData *)(long)local_150._7_1_;
  if ((long)pQVar17 < 0) {
    if ((QArrayData *)0x7ffffffffffffff7 < pQStack_158) {
                    /* WARNING: Subroutine does not return */
      FUN_1000059ac(&local_88);
    }
    pQVar17 = pQStack_158;
    pppppppuVar18 = local_160;
    if ((QArrayData *)0x16 < pQStack_158) goto LAB_100007260;
LAB_1000071d8:
    local_78 = CONCAT17((char)pQStack_158,(undefined7)local_78);
    pQVar19 = (QArrayData *)&local_88;
    pQVar17 = pQStack_158;
    if (pQStack_158 != (QArrayData *)0x0) goto LAB_100007288;
  }
  else {
    pQStack_158 = pQVar17;
    pppppppuVar18 = &local_160;
    if (pQVar17 < (QArrayData *)0x17) goto LAB_1000071d8;
LAB_100007260:
    uVar2 = 0x19;
    if (((ulong)pQVar17 | 7) != 0x17) {
      uVar2 = ((ulong)pQVar17 | 7) + 1;
    }
    pQVar19 = operator_new(uVar2);
    local_78 = uVar2 | 0x8000000000000000;
    local_88 = pQVar19;
    pQStack_80 = pQVar17;
LAB_100007288:
    _memmove(pQVar19,pppppppuVar18,(size_t)pQVar17);
    pQStack_158 = pQVar17;
  }
  pQVar19[(long)pQStack_158] = (QArrayData)0x0;
  pQStack_98 = pQStack_80;
  local_a0 = local_88;
  local_90 = local_78;
  FUN_100005058(&local_a0,local_165,local_164,&local_2f8);
  if (-1 < (char)local_189) {
    local_198 = (ulong)local_189;
  }
  if (local_198 == 0) {
    uVar14 = 0;
  }
  else {
    uVar2 = local_180;
    if (-1 < (char)local_171) {
      uVar2 = (ulong)local_171;
    }
    uVar14 = 1;
    if (uVar2 == 0) {
      uVar14 = 2;
    }
  }
  uVar8 = std::chrono::system_clock::now();
  FUN_100046504(&local_88,2,uVar8);
  iVar6 = FUN_100042ca8(&local_88);
  if (iVar6 != 0) {
    uVar8 = FUN_10003fe68(&local_88,"Push2DisplayProcess ");
    uVar8 = FUN_10003fe68(uVar8,"12.4.3");
    FUN_10003fe68(uVar8," - started");
  }
  thunk_FUN_10003f9d4(&local_88);
  uVar5 = local_16c;
  pcVar15 = *(char **)puVar4;
  pcVar1 = *(char **)pcVar15;
  uVar16 = *(uint *)(pcVar15 + 8);
  if (-1 < pcVar15[0x17]) {
    pcVar1 = pcVar15;
    uVar16 = (uint)(byte)pcVar15[0x17];
  }
  local_a4 = param_1;
  if ((pcVar1 != (char *)0x0) && (uVar16 == 0xffffffff)) {
    sVar10 = _strlen(pcVar1);
    uVar16 = (uint)sVar10;
  }
  QString::fromUtf8_helper(pcVar1,uVar16);
  QDir::QDir((QDir *)local_100,(QString *)&local_b0);
  uVar8 = std::chrono::system_clock::now();
  FUN_100046504(local_d8,2,uVar8);
  iVar6 = FUN_100042ca8(local_d8);
  if (iVar6 != 0) {
    uVar8 = FUN_10003fe68(local_d8,"applicationDirPath: ");
    QDir::absolutePath();
    QString::toUtf8_helper((QString *)local_c0);
    pQVar17 = local_a0;
    uVar16 = *(uint *)(local_a0 + 4);
    pQVar19 = (QArrayData *)(long)(int)uVar16;
    if ((int)uVar16 < 0) {
                    /* WARNING: Subroutine does not return */
      FUN_1000059ac(&local_88);
    }
    lVar20 = *(long *)(local_a0 + 0x10);
    if (uVar16 < 0x17) {
      local_78 = CONCAT17((char)uVar16,(undefined7)local_78);
      pQVar11 = (QArrayData *)&local_88;
      if (uVar16 != 0) goto LAB_100007480;
                    /* WARNING: Ignoring partial resolution of indirect */
      local_88._0_1_ = (QArrayData)0x0;
      iVar6 = *(int *)local_a0;
    }
    else {
      uVar2 = 0x19;
      if (((ulong)pQVar19 | 7) != 0x17) {
        uVar2 = ((ulong)pQVar19 | 7) + 1;
      }
      pQVar11 = operator_new(uVar2);
      local_78 = uVar2 | 0x8000000000000000;
      local_88 = pQVar11;
      pQStack_80 = pQVar19;
LAB_100007480:
      _memmove(pQVar11,pQVar17 + lVar20,(size_t)pQVar19);
      pQVar11[(long)pQVar19] = (QArrayData)0x0;
      iVar6 = *(int *)local_a0;
    }
    if (iVar6 != -1) {
      if (iVar6 != 0) {
        LOAcquire();
        iVar6 = *(int *)local_a0;
        *(int *)local_a0 = iVar6 + -1;
        LORelease();
        if (iVar6 != 1) goto LAB_1000074c8;
      }
      QArrayData::deallocate(local_a0,1,8);
    }
LAB_1000074c8:
    FUN_100040d48(uVar8,&local_88);
    if (*(int *)local_c0[0] != -1) {
      if (*(int *)local_c0[0] != 0) {
        LOAcquire();
        iVar6 = *(int *)local_c0[0];
        *(int *)local_c0[0] = iVar6 + -1;
        LORelease();
        if (iVar6 != 1) goto LAB_100007518;
      }
      QArrayData::deallocate(local_c0[0],2,8);
    }
  }
LAB_100007518:
  this = (QDir *)thunk_FUN_10003f9d4(local_d8);
  uVar8 = QDir::QDir(this,(QDir *)local_100);
  FUN_100006a00(&local_88,uVar8,5);
  pQVar17 = local_d8[0];
  local_d8[0] = local_88;
  local_88 = pQVar17;
  QDir::~QDir((QDir *)&local_88);
  local_88 = (QArrayData *)QString::fromAscii_helper("Qt",2);
  QDir::cd((QString *)local_d8);
  if (*(int *)local_88 != -1) {
    if (*(int *)local_88 != 0) {
      LOAcquire();
      iVar6 = *(int *)local_88;
      *(int *)local_88 = iVar6 + -1;
      LORelease();
      if (iVar6 != 1) goto LAB_1000075a0;
    }
    QArrayData::deallocate(local_88,2,8);
  }
LAB_1000075a0:
  local_88 = (QArrayData *)QString::fromAscii_helper("plugins",7);
  QDir::cd((QString *)local_d8);
  if (*(int *)local_88 != -1) {
    if (*(int *)local_88 != 0) {
      LOAcquire();
      iVar6 = *(int *)local_88;
      *(int *)local_88 = iVar6 + -1;
      LORelease();
      if (iVar6 != 1) goto LAB_1000075f4;
    }
    QArrayData::deallocate(local_88,2,8);
  }
LAB_1000075f4:
  uVar8 = std::chrono::system_clock::now();
  FUN_100046504(local_c0,2,uVar8);
  iVar6 = FUN_100042ca8(local_c0);
  if (iVar6 != 0) {
    uVar8 = FUN_10003fe68(local_c0,"Adding Qt plugins path: ");
    QDir::absolutePath();
    QString::toUtf8_helper((QString *)&local_e8);
    pQVar17 = local_a0;
    uVar16 = *(uint *)(local_a0 + 4);
    pQVar19 = (QArrayData *)(long)(int)uVar16;
    if ((int)uVar16 < 0) {
                    /* WARNING: Subroutine does not return */
      FUN_1000059ac(&local_88);
    }
    lVar20 = *(long *)(local_a0 + 0x10);
    if (uVar16 < 0x17) {
      local_78 = CONCAT17((char)uVar16,(undefined7)local_78);
      pQVar11 = (QArrayData *)&local_88;
      if (uVar16 != 0) goto LAB_1000076a4;
                    /* WARNING: Ignoring partial resolution of indirect */
      local_88._0_1_ = (QArrayData)0x0;
      iVar6 = *(int *)local_a0;
    }
    else {
      uVar2 = 0x19;
      if (((ulong)pQVar19 | 7) != 0x17) {
        uVar2 = ((ulong)pQVar19 | 7) + 1;
      }
      pQVar11 = operator_new(uVar2);
      local_78 = uVar2 | 0x8000000000000000;
      local_88 = pQVar11;
      pQStack_80 = pQVar19;
LAB_1000076a4:
      _memmove(pQVar11,pQVar17 + lVar20,(size_t)pQVar19);
      pQVar11[(long)pQVar19] = (QArrayData)0x0;
      iVar6 = *(int *)local_a0;
    }
    if (iVar6 != -1) {
      if (iVar6 != 0) {
        LOAcquire();
        iVar6 = *(int *)local_a0;
        *(int *)local_a0 = iVar6 + -1;
        LORelease();
        if (iVar6 != 1) goto LAB_1000076ec;
      }
      QArrayData::deallocate(local_a0,1,8);
    }
LAB_1000076ec:
    FUN_100040d48(uVar8,&local_88);
    if (*(int *)local_e8 != -1) {
      if (*(int *)local_e8 != 0) {
        LOAcquire();
        iVar6 = *(int *)local_e8;
        *(int *)local_e8 = iVar6 + -1;
        LORelease();
        if (iVar6 != 1) goto LAB_10000773c;
      }
      QArrayData::deallocate((QArrayData *)local_e8,2,8);
    }
  }
LAB_10000773c:
  thunk_FUN_10003f9d4(local_c0);
  QDir::absolutePath();
  QCoreApplication::addLibraryPath((QString *)&local_88);
  if (*(int *)local_88 != -1) {
    if (*(int *)local_88 != 0) {
      LOAcquire();
      iVar6 = *(int *)local_88;
      *(int *)local_88 = iVar6 + -1;
      LORelease();
      if (iVar6 != 1) goto LAB_10000778c;
    }
    QArrayData::deallocate(local_88,2,8);
  }
LAB_10000778c:
  QDir::~QDir((QDir *)local_d8);
  QDir::~QDir((QDir *)local_100);
  if (*(int *)local_b0 != -1) {
    if (*(int *)local_b0 != 0) {
      LOAcquire();
      iVar6 = *(int *)local_b0;
      *(int *)local_b0 = iVar6 + -1;
      LORelease();
      if (iVar6 != 1) goto LAB_1000077d0;
    }
    QArrayData::deallocate(local_b0,2,8);
  }
LAB_1000077d0:
  QApplication::QApplication((QApplication *)local_c0,&local_a4,param_2,0x50f02);
  QQmlEngine::QQmlEngine((QQmlEngine *)local_d8,(QObject *)0x0);
  FUN_10000a060(&local_88);
  pQVar17 = pQStack_80;
  if (local_88 != pQStack_80) {
    pQVar19 = local_88;
    do {
      uVar8 = std::chrono::system_clock::now();
      FUN_100046504(&local_e8,1,uVar8);
      iVar6 = FUN_100042ca8(&local_e8);
      if (iVar6 != 0) {
        uVar8 = FUN_10003fe68(&local_e8,"importPath:");
        if ((char)pQVar19[0x17] < '\0') {
          FUN_100005a5c(&local_a0,*(undefined8 *)pQVar19,*(undefined8 *)(pQVar19 + 8));
        }
        else {
          pQStack_98 = *(QArrayData **)(pQVar19 + 8);
          local_a0 = *(QArrayData **)pQVar19;
          local_90 = *(ulong *)(pQVar19 + 0x10);
        }
        FUN_100040d48(uVar8,&local_a0);
      }
      thunk_FUN_10003f9d4(&local_e8);
      if ((char)pQVar19[0x17] < '\0') {
        FUN_100005a5c(&local_a0,*(undefined8 *)pQVar19,*(undefined8 *)(pQVar19 + 8));
      }
      else {
        pQStack_98 = *(QArrayData **)(pQVar19 + 8);
        local_a0 = *(QArrayData **)pQVar19;
        local_90 = *(ulong *)(pQVar19 + 0x10);
      }
      uVar16 = (uint)local_90._7_1_;
      if ((&local_a0 != (QArrayData **)0x0) && (uVar16 == 0xffffffff)) {
        sVar10 = _strlen((char *)&local_a0);
        uVar16 = (uint)sVar10;
      }
      QString::fromUtf8_helper((char *)&local_a0,uVar16);
      QQmlEngine::addImportPath((QString *)local_d8);
      if (*(int *)local_e8 != -1) {
        if (*(int *)local_e8 != 0) {
          LOAcquire();
          iVar6 = *(int *)local_e8;
          *(int *)local_e8 = iVar6 + -1;
          LORelease();
          if (iVar6 != 1) goto LAB_100007958;
        }
        QArrayData::deallocate((QArrayData *)local_e8,2,8);
      }
LAB_100007958:
      pQVar19 = pQVar19 + 0x18;
    } while (pQVar19 != pQVar17);
  }
  if (local_88 != (QArrayData *)0x0) {
    for (; pQStack_80 != local_88; pQStack_80 = pQStack_80 + -0x18) {
    }
    pQStack_80 = local_88;
    operator_delete(local_88);
  }
  local_88 = (QArrayData *)QString::fromAscii_helper(":",1);
  QQmlEngine::addImportPath((QString *)local_d8);
  if (*(int *)local_88 != -1) {
    if (*(int *)local_88 != 0) {
      LOAcquire();
      iVar6 = *(int *)local_88;
      *(int *)local_88 = iVar6 + -1;
      LORelease();
      if (iVar6 != 1) goto LAB_100007a08;
    }
    QArrayData::deallocate(local_88,2,8);
  }
LAB_100007a08:
  FUN_10000a518(&local_88);
  pQVar17 = pQStack_80;
  if (local_88 != pQStack_80) {
    pQVar19 = local_88;
    do {
      uVar8 = std::chrono::system_clock::now();
      FUN_100046504(&local_e8,1,uVar8);
      iVar6 = FUN_100042ca8(&local_e8);
      if (iVar6 != 0) {
        uVar8 = FUN_10003fe68(&local_e8,"import/plugin Path:");
        if ((char)pQVar19[0x17] < '\0') {
          FUN_100005a5c(&local_a0,*(undefined8 *)pQVar19,*(undefined8 *)(pQVar19 + 8));
        }
        else {
          pQStack_98 = *(QArrayData **)(pQVar19 + 8);
          local_a0 = *(QArrayData **)pQVar19;
          local_90 = *(ulong *)(pQVar19 + 0x10);
        }
        FUN_100040d48(uVar8,&local_a0);
      }
      thunk_FUN_10003f9d4(&local_e8);
      if ((char)pQVar19[0x17] < '\0') {
        FUN_100005a5c(&local_a0,*(undefined8 *)pQVar19,*(undefined8 *)(pQVar19 + 8));
      }
      else {
        pQStack_98 = *(QArrayData **)(pQVar19 + 8);
        local_a0 = *(QArrayData **)pQVar19;
        local_90 = *(ulong *)(pQVar19 + 0x10);
      }
      uVar16 = (uint)local_90._7_1_;
      if ((&local_a0 != (QArrayData **)0x0) && (uVar16 == 0xffffffff)) {
        sVar10 = _strlen((char *)&local_a0);
        uVar16 = (uint)sVar10;
      }
      QString::fromUtf8_helper((char *)&local_a0,uVar16);
      QQmlEngine::addImportPath((QString *)local_d8);
      if (*(int *)local_e8 != -1) {
        if (*(int *)local_e8 != 0) {
          LOAcquire();
          iVar6 = *(int *)local_e8;
          *(int *)local_e8 = iVar6 + -1;
          LORelease();
          if (iVar6 != 1) goto LAB_100007b6c;
        }
        QArrayData::deallocate((QArrayData *)local_e8,2,8);
      }
LAB_100007b6c:
      if ((char)pQVar19[0x17] < '\0') {
        FUN_100005a5c(&local_a0,*(undefined8 *)pQVar19,*(undefined8 *)(pQVar19 + 8));
      }
      else {
        pQStack_98 = *(QArrayData **)(pQVar19 + 8);
        local_a0 = *(QArrayData **)pQVar19;
        local_90 = *(ulong *)(pQVar19 + 0x10);
      }
      uVar16 = (uint)local_90._7_1_;
      if ((&local_a0 != (QArrayData **)0x0) && (uVar16 == 0xffffffff)) {
        sVar10 = _strlen((char *)&local_a0);
        uVar16 = (uint)sVar10;
      }
      QString::fromUtf8_helper((char *)&local_a0,uVar16);
      QQmlEngine::addPluginPath((QString *)local_d8);
      if (*(int *)local_e8 != -1) {
        if (*(int *)local_e8 != 0) {
          LOAcquire();
          iVar6 = *(int *)local_e8;
          *(int *)local_e8 = iVar6 + -1;
          LORelease();
          if (iVar6 != 1) goto LAB_100007c28;
        }
        QArrayData::deallocate((QArrayData *)local_e8,2,8);
      }
LAB_100007c28:
      pQVar19 = pQVar19 + 0x18;
    } while (pQVar19 != pQVar17);
  }
  if (local_88 != (QArrayData *)0x0) {
    for (; pQStack_80 != local_88; pQStack_80 = pQStack_80 + -0x18) {
    }
    pQStack_80 = local_88;
    operator_delete(local_88);
  }
  QQmlEngine::setOutputWarningsToStandardError((bool)((char)&stack0xfffffffffffffff0 + '8'));
  local_88 = (QArrayData *)PTR_warnings_10029c0d8;
  pQStack_80 = (QArrayData *)0x0;
  puVar12 = operator_new(0x18);
  *puVar12 = 1;
  *(code **)(puVar12 + 2) = FUN_10000b2d0;
  QObject::connectImpl
            (&local_a0,local_d8,&local_88,local_d8,0,puVar12,1,0,PTR_staticMetaObject_10029c0d0);
  QMetaObject::Connection::~Connection((Connection *)&local_a0);
  QObject::connect(&local_88,local_d8,"2quit()",local_c0,"1quit()",0);
  QMetaObject::Connection::~Connection((Connection *)&local_88);
  if (-1 < (char)local_171) {
    local_180 = (ulong)local_171;
  }
  pQVar17 = operator_new(0x110);
  FUN_1000c3b98(pQVar17,local_180 == 0,uVar5,0);
  local_b0 = pQVar17;
  if (local_180 == 0) {
    uVar2 = local_138;
    if (-1 < (long)local_130) {
      uVar2 = local_130 >> 0x38;
    }
    if (uVar2 != 0) {
      FUN_1000c41dc(pQVar17,&local_140);
    }
  }
  QObject::connect(&local_88,pQVar17,"2shutdown()",local_c0,"1quit()",0);
  QMetaObject::Connection::~Connection((Connection *)&local_88);
  QObject::QObject((QObject *)&local_e8,(QObject *)0x0);
  local_e8 = &PTR_FUN_10029daf8;
  pQVar13 = (QString *)QQmlEngine::rootContext();
  local_88 = (QArrayData *)QString::fromAscii_helper("CRASHER",7);
  QQmlContext::setContextProperty(pQVar13,(QObject *)&local_88);
  if (*(int *)local_88 != -1) {
    if (*(int *)local_88 != 0) {
      LOAcquire();
      iVar6 = *(int *)local_88;
      *(int *)local_88 = iVar6 + -1;
      LORelease();
      if (iVar6 != 1) goto LAB_100007e24;
    }
    QArrayData::deallocate(local_88,2,8);
  }
LAB_100007e24:
  pQVar13 = (QString *)QQmlEngine::rootContext();
  local_88 = (QArrayData *)QString::fromAscii_helper("IPC_CHANNEL",0xb);
  QQmlContext::setContextProperty(pQVar13,(QObject *)&local_88);
  if (*(int *)local_88 != -1) {
    if (*(int *)local_88 != 0) {
      LOAcquire();
      iVar6 = *(int *)local_88;
      *(int *)local_88 = iVar6 + -1;
      LORelease();
      if (iVar6 != 1) goto LAB_100007e88;
    }
    QArrayData::deallocate(local_88,2,8);
  }
LAB_100007e88:
  pQVar13 = (QString *)QQmlEngine::rootContext();
  local_a0 = (QArrayData *)QString::fromAscii_helper("MODEL_RECORDING_FILENAME",0x18);
  pcVar1 = (char *)CONCAT71(uStack_19f,local_1a0);
  if (-1 < (char)local_189) {
    pcVar1 = &local_1a0;
  }
  QVariant::QVariant((QVariant *)&local_88,pcVar1);
  QQmlContext::setContextProperty(pQVar13,(QVariant *)&local_a0);
  QVariant::~QVariant((QVariant *)&local_88);
  if (*(int *)local_a0 != -1) {
    if (*(int *)local_a0 != 0) {
      LOAcquire();
      iVar6 = *(int *)local_a0;
      *(int *)local_a0 = iVar6 + -1;
      LORelease();
      if (iVar6 != 1) goto LAB_100007f10;
    }
    QArrayData::deallocate(local_a0,2,8);
  }
LAB_100007f10:
  pQVar13 = (QString *)QQmlEngine::rootContext();
  local_a0 = (QArrayData *)QString::fromAscii_helper("MODEL_PLAYBACK_ROOT",0x13);
  pcVar1 = (char *)CONCAT71(uStack_187,local_188);
  if (-1 < (char)local_171) {
    pcVar1 = &local_188;
  }
  QVariant::QVariant((QVariant *)&local_88,pcVar1);
  QQmlContext::setContextProperty(pQVar13,(QVariant *)&local_a0);
  QVariant::~QVariant((QVariant *)&local_88);
  if (*(int *)local_a0 != -1) {
    if (*(int *)local_a0 != 0) {
      LOAcquire();
      iVar6 = *(int *)local_a0;
      *(int *)local_a0 = iVar6 + -1;
      LORelease();
      if (iVar6 != 1) goto LAB_100007f98;
    }
    QArrayData::deallocate(local_a0,2,8);
  }
LAB_100007f98:
  pQVar13 = (QString *)QQmlEngine::rootContext();
  local_a0 = (QArrayData *)QString::fromAscii_helper("SCREENSHOT_FILENAME",0x13);
  pcVar1 = (char *)CONCAT71(uStack_1b7,local_1b8);
  if (-1 < local_1a1) {
    pcVar1 = &local_1b8;
  }
  QVariant::QVariant((QVariant *)&local_88,pcVar1);
  QQmlContext::setContextProperty(pQVar13,(QVariant *)&local_a0);
  QVariant::~QVariant((QVariant *)&local_88);
  if (*(int *)local_a0 != -1) {
    if (*(int *)local_a0 != 0) {
      LOAcquire();
      iVar6 = *(int *)local_a0;
      *(int *)local_a0 = iVar6 + -1;
      LORelease();
      if (iVar6 != 1) goto LAB_100008020;
    }
    QArrayData::deallocate(local_a0,2,8);
  }
LAB_100008020:
  FUN_1000094f8(&local_88,uVar14);
  pQStack_98 = pQStack_80;
  local_a0 = local_88;
  local_90 = local_78;
  sVar10 = _strlen((char *)&local_a0);
  local_100[0] = (QArrayData *)QString::fromAscii_helper((char *)&local_a0,(int)sVar10);
  QUrl::fromLocalFile((QString *)local_100);
  if (*(int *)local_100[0] != -1) {
    if (*(int *)local_100[0] != 0) {
      LOAcquire();
      iVar6 = *(int *)local_100[0];
      *(int *)local_100[0] = iVar6 + -1;
      LORelease();
      if (iVar6 != 1) goto LAB_1000080c4;
    }
    QArrayData::deallocate(local_100[0],2,8);
  }
LAB_1000080c4:
  uVar8 = std::chrono::system_clock::now();
  FUN_100046504(&local_a0,1,uVar8);
  iVar6 = FUN_100042ca8(&local_a0);
  if (iVar6 != 0) {
    uVar8 = FUN_10003fe68(&local_a0,"Use qml file ");
    FUN_100009bf4(uVar8,&local_88);
  }
  thunk_FUN_10003f9d4(&local_a0);
  QQmlComponent::QQmlComponent((QQmlComponent *)local_100,(QQmlEngine *)local_d8,(QObject *)0x0);
  local_108 = (long *)0x0;
  local_a0 = (QArrayData *)PTR_statusChanged_10029c0e0;
  pQStack_98 = (QArrayData *)0x0;
  puVar12 = operator_new(0x48);
  *(QUrl **)(puVar12 + 6) = aQStack_f0;
  *(void ***)(puVar12 + 8) = &local_128;
  *(QArrayData ***)(puVar12 + 10) = &local_b0;
  *(long ***)(puVar12 + 0xc) = &local_108;
  *(undefined1 **)(puVar12 + 0xe) = &local_1d0;
  *(QArrayData ***)(puVar12 + 0x10) = local_d8;
  *puVar12 = 1;
  *(code **)(puVar12 + 2) = FUN_10000ca78;
  *(QArrayData ***)(puVar12 + 4) = local_100;
  QObject::connectImpl
            (aCStack_110,local_100,&local_a0,local_100,0,puVar12,1,0,PTR_staticMetaObject_10029c0e8)
  ;
  QMetaObject::Connection::~Connection(aCStack_110);
  QQmlComponent::loadUrl((QUrl *)local_100);
  uVar8 = QApplication::exec();
  if (local_108 != (long *)0x0) {
    (**(code **)(*local_108 + 0x20))();
  }
  QQmlComponent::~QQmlComponent((QQmlComponent *)local_100);
  QUrl::~QUrl(aQStack_f0);
  QObject::~QObject((QObject *)&local_e8);
  pQVar17 = local_b0;
  local_b0 = (QArrayData *)0x0;
  if (pQVar17 != (QArrayData *)0x0) {
    (**(code **)(*(long *)pQVar17 + 0x20))();
  }
  QQmlEngine::~QQmlEngine((QQmlEngine *)local_d8);
  QApplication::~QApplication((QApplication *)local_c0);
  uVar9 = std::chrono::system_clock::now();
  FUN_100046504(&local_88,2,uVar9);
  iVar6 = FUN_100042ca8(&local_88);
  if (iVar6 != 0) {
    uVar9 = FUN_10003fe68(&local_88,"Push2DisplayProcess - terminated with ");
    FUN_100041ba0(uVar9,uVar8);
  }
  thunk_FUN_10003f9d4(&local_88);
  if (lStack_2e0 < 0) {
    operator_delete(local_2f0);
  }
  local_2d8 = (undefined8 *******)&PTR_FUN_1002aa6a8;
  FUN_10000d914(auStack_298,local_290);
  FUN_10000d98c(auStack_2b0,local_2a8);
  FUN_10000d9ec(&local_2c8,local_2c0);
  pcVar15 = local_260;
  pcVar1 = local_258;
  if (local_260 != (char *)0x0) {
    while (pcVar1 != pcVar15) {
      FUN_10000dabc(pcVar1 + -0x58);
      pcVar1 = pcVar1 + -0x58;
    }
    local_258 = pcVar15;
    operator_delete(local_260);
  }
  FUN_10000db8c(local_238);
  if (local_1b9 < '\0') {
    operator_delete((void *)CONCAT71(uStack_1cf,local_1d0));
  }
  if (local_1a1 < '\0') {
    operator_delete((void *)CONCAT71(uStack_1b7,local_1b8));
  }
  if ((char)local_189 < '\0') {
    operator_delete((void *)CONCAT71(uStack_19f,local_1a0));
  }
  if ((char)local_171 < '\0') {
    operator_delete((void *)CONCAT71(uStack_187,local_188));
  }
  if (local_150 < 0) {
    operator_delete(local_160);
  }
  if ((long)local_130 < 0) {
    operator_delete(local_140);
  }
  if (local_111 < '\0') {
    operator_delete(local_128);
  }
  return uVar8;
}

