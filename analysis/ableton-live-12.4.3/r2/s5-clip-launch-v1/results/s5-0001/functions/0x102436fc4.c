
/* WARNING: Removing unreachable block (ram,0x000102438258) */
/* WARNING: Removing unreachable block (ram,0x000102438268) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

long * FUN_102436fc4(long *param_1)

{
  undefined *puVar1;
  undefined *puVar2;
  int iVar3;
  undefined8 *puVar4;
  long lVar5;
  undefined **ppuVar6;
  undefined8 uVar7;
  undefined8 *puVar8;
  undefined8 *puVar9;
  long lVar10;
  long lVar11;
  long *plVar12;
  bool bVar13;
  int *local_160;
  int *local_158;
  undefined *local_150;
  long *plStack_148;
  undefined *local_140;
  long *plStack_138;
  undefined *local_130;
  long *plStack_128;
  undefined *local_120;
  long *plStack_118;
  undefined *local_110;
  long *plStack_108;
  undefined *local_100;
  long *plStack_f8;
  undefined *local_f0;
  long *plStack_e8;
  undefined *local_e0;
  long *plStack_d8;
  undefined *local_d0;
  long *plStack_c8;
  undefined *local_c0;
  long *plStack_b8;
  int *local_b0;
  long *plStack_a8;
  undefined **local_a0;
  long *plStack_98;
  undefined ***local_88;
  undefined *local_80;
  long *plStack_78;
  long local_70;
  
  local_70 = *(long *)PTR____stack_chk_guard_1064f8818;
  puVar4 = (undefined8 *)FUN_1024deba8();
  puVar4[0xb] = &PTR_FUN_1067b7178;
  *puVar4 = &PTR_FUN_1067b6cc0;
  FUN_1015643d8(&local_a0);
  FUN_10150b1cc(param_1 + 0xc,local_a0);
  if ((local_a0 != (undefined **)0x0) &&
     (iVar3 = *(int *)(local_a0 + 1), *(int *)(local_a0 + 1) = iVar3 + -1, iVar3 + -1 == 0)) {
    FUN_10128eea0();
  }
  param_1[0xc] = (long)&PTR_thunk_FUN_10150b2b4_10658fdd8;
  FUN_1015643d8(&local_a0);
  FUN_10150b1cc(param_1 + 0xf,local_a0);
  if ((local_a0 != (undefined **)0x0) &&
     (iVar3 = *(int *)(local_a0 + 1), *(int *)(local_a0 + 1) = iVar3 + -1, iVar3 + -1 == 0)) {
    FUN_10128eea0();
  }
  param_1[0xf] = (long)&PTR_thunk_FUN_10150b2b4_10658fdd8;
  FUN_10242650c(&local_a0);
  FUN_10150b1cc(param_1 + 0x12,local_a0);
  if ((local_a0 != (undefined **)0x0) &&
     (iVar3 = *(int *)(local_a0 + 1), *(int *)(local_a0 + 1) = iVar3 + -1, iVar3 + -1 == 0)) {
    FUN_10128eea0();
  }
  param_1[0x12] = (long)&PTR_thunk_FUN_10150b2b4_1067b7ad0;
  FUN_1015643d8(&local_a0);
  FUN_10150b1cc(param_1 + 0x15,local_a0);
  if ((local_a0 != (undefined **)0x0) &&
     (iVar3 = *(int *)(local_a0 + 1), *(int *)(local_a0 + 1) = iVar3 + -1, iVar3 + -1 == 0)) {
    FUN_10128eea0();
  }
  param_1[0x15] = (long)&PTR_thunk_FUN_10150b2b4_10658fdd8;
  FUN_101565098(&local_a0);
  FUN_10150b1cc(param_1 + 0x18,local_a0);
  if ((local_a0 != (undefined **)0x0) &&
     (iVar3 = *(int *)(local_a0 + 1), *(int *)(local_a0 + 1) = iVar3 + -1, iVar3 + -1 == 0)) {
    FUN_10128eea0();
  }
  param_1[0x18] = (long)&PTR_thunk_FUN_10150b2b4_10673f310;
  FUN_101565098(&local_a0);
  FUN_10150b1cc(param_1 + 0x1b,local_a0);
  if ((local_a0 != (undefined **)0x0) &&
     (iVar3 = *(int *)(local_a0 + 1), *(int *)(local_a0 + 1) = iVar3 + -1, iVar3 + -1 == 0)) {
    FUN_10128eea0();
  }
  param_1[0x1b] = (long)&PTR_thunk_FUN_10150b2b4_10673f310;
  FUN_10156f89c(&local_a0);
  FUN_10150b1cc(param_1 + 0x1e,local_a0);
  if ((local_a0 != (undefined **)0x0) &&
     (iVar3 = *(int *)(local_a0 + 1), *(int *)(local_a0 + 1) = iVar3 + -1, iVar3 + -1 == 0)) {
    FUN_10128eea0();
  }
  param_1[0x1e] = (long)&PTR_thunk_FUN_10150b2b4_10658fe68;
  FUN_10156f89c(&local_a0);
  FUN_10150b1cc(param_1 + 0x21,local_a0);
  if ((local_a0 != (undefined **)0x0) &&
     (iVar3 = *(int *)(local_a0 + 1), *(int *)(local_a0 + 1) = iVar3 + -1, iVar3 + -1 == 0)) {
    FUN_10128eea0();
  }
  param_1[0x21] = (long)&PTR_thunk_FUN_10150b2b4_10658fe68;
  param_1[0x24] = 0;
  FUN_101563fa0(&local_a0);
  lVar5 = param_1[0x24];
  if ((lVar5 != 0) && (iVar3 = *(int *)(lVar5 + 8) + -1, *(int *)(lVar5 + 8) = iVar3, iVar3 == 0)) {
    FUN_10128eea0();
  }
  param_1[0x24] = (long)local_a0;
  FUN_1015643d8(&local_a0);
  FUN_10150b1cc(param_1 + 0x25,local_a0);
  if ((local_a0 != (undefined **)0x0) &&
     (iVar3 = *(int *)(local_a0 + 1), *(int *)(local_a0 + 1) = iVar3 + -1, iVar3 + -1 == 0)) {
    FUN_10128eea0();
  }
  param_1[0x25] = (long)&PTR_thunk_FUN_10150b2b4_10658fdd8;
  FUN_1015643d8(&local_a0);
  FUN_10150b1cc(param_1 + 0x28,local_a0);
  if ((local_a0 != (undefined **)0x0) &&
     (iVar3 = *(int *)(local_a0 + 1), *(int *)(local_a0 + 1) = iVar3 + -1, iVar3 + -1 == 0)) {
    FUN_10128eea0();
  }
  param_1[0x28] = (long)&PTR_thunk_FUN_10150b2b4_10658fdd8;
  param_1[0x2b] = (long)&PTR_FUN_1067b77c8;
  param_1[0x2d] = 0;
  param_1[0x2c] = 0;
  param_1[0x2f] = 0;
  param_1[0x2e] = 0;
  param_1[0x31] = 0;
  param_1[0x30] = 0;
  puVar4 = (undefined8 *)FUN_1012d9850(0x28);
  FUN_10128ed98();
  puVar4[3] = param_1;
  puVar4[4] = param_1 + 0x31;
  *puVar4 = &PTR_thunk_FUN_10128edf8_1067b7a30;
  param_1[0x32] = (long)puVar4;
  *(int *)(puVar4 + 1) = *(int *)(puVar4 + 1) + 1;
  puVar4 = (undefined8 *)FUN_1012d9850(0x28);
  FUN_10128ed98();
  puVar4[3] = param_1;
  puVar4[4] = (long)param_1 + 0x18c;
  *puVar4 = &PTR_thunk_FUN_10128edf8_1067b7a80;
  param_1[0x33] = (long)puVar4;
  *(int *)(puVar4 + 1) = *(int *)(puVar4 + 1) + 1;
  FUN_10245ab94(&local_a0);
  FUN_10150b1cc(param_1 + 0x34,local_a0);
  if ((local_a0 != (undefined **)0x0) &&
     (iVar3 = *(int *)(local_a0 + 1), *(int *)(local_a0 + 1) = iVar3 + -1, iVar3 + -1 == 0)) {
    FUN_10128eea0();
  }
  param_1[0x34] = (long)&PTR_thunk_FUN_10150b2b4_1067b7b60;
  FUN_102503dbc(&local_a0);
  FUN_10150b1cc(param_1 + 0x37,local_a0);
  if ((local_a0 != (undefined **)0x0) &&
     (iVar3 = *(int *)(local_a0 + 1), *(int *)(local_a0 + 1) = iVar3 + -1, iVar3 + -1 == 0)) {
    FUN_10128eea0();
  }
  param_1[0x37] = (long)&PTR_thunk_FUN_10150b2b4_1067b7bf0;
  FUN_1026e27ec(&local_a0);
  FUN_10150b1cc(param_1 + 0x3a,local_a0);
  if ((local_a0 != (undefined **)0x0) &&
     (iVar3 = *(int *)(local_a0 + 1), *(int *)(local_a0 + 1) = iVar3 + -1, iVar3 + -1 == 0)) {
    FUN_10128eea0();
  }
  param_1[0x3a] = (long)&PTR_thunk_FUN_10150b2b4_1067b7c80;
  FUN_1017744a0(&local_a0);
  FUN_10150b1cc(param_1 + 0x3e,local_a0);
  if ((local_a0 != (undefined **)0x0) &&
     (iVar3 = *(int *)(local_a0 + 1), *(int *)(local_a0 + 1) = iVar3 + -1, iVar3 + -1 == 0)) {
    FUN_10128eea0();
  }
  param_1[0x3e] = (long)&PTR_thunk_FUN_10150b2b4_1067b7d10;
  FUN_102650888(&local_a0);
  FUN_10150b1cc(param_1 + 0x41,local_a0);
  if ((local_a0 != (undefined **)0x0) &&
     (iVar3 = *(int *)(local_a0 + 1), *(int *)(local_a0 + 1) = iVar3 + -1, iVar3 + -1 == 0)) {
    FUN_10128eea0();
  }
  param_1[0x41] = (long)&PTR_thunk_FUN_10150b2b4_1067b7da0;
  FUN_102448ed0(param_1 + 0x44);
  FUN_1015643d8(&local_a0);
  FUN_10150b1cc(param_1 + 0x47,local_a0);
  if ((local_a0 != (undefined **)0x0) &&
     (iVar3 = *(int *)(local_a0 + 1), *(int *)(local_a0 + 1) = iVar3 + -1, iVar3 + -1 == 0)) {
    FUN_10128eea0();
  }
  param_1[0x47] = (long)&PTR_thunk_FUN_10150b2b4_10658fdd8;
  FUN_101565f54(&local_a0);
  FUN_10150b1cc(param_1 + 0x4a,local_a0);
  if ((local_a0 != (undefined **)0x0) &&
     (iVar3 = *(int *)(local_a0 + 1), *(int *)(local_a0 + 1) = iVar3 + -1, iVar3 + -1 == 0)) {
    FUN_10128eea0();
  }
  param_1[0x4a] = (long)&PTR_thunk_FUN_10150b2b4_1065925e0;
  FUN_101565f54(&local_a0);
  FUN_10150b1cc(param_1 + 0x4d,local_a0);
  if ((local_a0 != (undefined **)0x0) &&
     (iVar3 = *(int *)(local_a0 + 1), *(int *)(local_a0 + 1) = iVar3 + -1, iVar3 + -1 == 0)) {
    FUN_10128eea0();
  }
  param_1[0x4d] = (long)&PTR_thunk_FUN_10150b2b4_1065925e0;
  FUN_10256bcd0(&local_a0);
  FUN_10150b1cc(param_1 + 0x50,local_a0);
  if ((local_a0 != (undefined **)0x0) &&
     (iVar3 = *(int *)(local_a0 + 1), *(int *)(local_a0 + 1) = iVar3 + -1, iVar3 + -1 == 0)) {
    FUN_10128eea0();
  }
  param_1[0x50] = (long)&PTR_thunk_FUN_10150b2b4_1067b7ec0;
  FUN_1026df1c4(&local_a0);
  FUN_10150b1cc(param_1 + 0x53,local_a0);
  if ((local_a0 != (undefined **)0x0) &&
     (iVar3 = *(int *)(local_a0 + 1), *(int *)(local_a0 + 1) = iVar3 + -1, iVar3 + -1 == 0)) {
    FUN_10128eea0();
  }
  param_1[0x53] = (long)&PTR_thunk_FUN_10150b2b4_1067b7f50;
  FUN_102453ed0(&local_a0);
  FUN_10150b1cc(param_1 + 0x56,local_a0);
  if ((local_a0 != (undefined **)0x0) &&
     (iVar3 = *(int *)(local_a0 + 1), *(int *)(local_a0 + 1) = iVar3 + -1, iVar3 + -1 == 0)) {
    FUN_10128eea0();
  }
  param_1[0x56] = (long)&PTR_thunk_FUN_10150b2b4_1067b7fe0;
  param_1[0x59] = 0;
  FUN_101563fa0(&local_a0);
  lVar5 = param_1[0x59];
  if ((lVar5 != 0) && (iVar3 = *(int *)(lVar5 + 8) + -1, *(int *)(lVar5 + 8) = iVar3, iVar3 == 0)) {
    FUN_10128eea0();
  }
  param_1[0x59] = (long)local_a0;
  param_1[0x5a] = 0;
  FUN_101565f54(&local_a0);
  lVar5 = param_1[0x5a];
  if ((lVar5 != 0) && (iVar3 = *(int *)(lVar5 + 8) + -1, *(int *)(lVar5 + 8) = iVar3, iVar3 == 0)) {
    FUN_10128eea0();
  }
  param_1[0x5a] = (long)local_a0;
  FUN_10150b744(param_1 + 0x5b,param_1);
  param_1[0x5d] = 0;
  param_1[0x5c] = 0;
  FUN_1015643d8(&local_a0);
  FUN_10150b1cc(param_1 + 0x5e,local_a0);
  if ((local_a0 != (undefined **)0x0) &&
     (iVar3 = *(int *)(local_a0 + 1), *(int *)(local_a0 + 1) = iVar3 + -1, iVar3 + -1 == 0)) {
    FUN_10128eea0();
  }
  param_1[0x5e] = (long)&PTR_thunk_FUN_10150b2b4_10658fdd8;
  param_1[0x62] = 0;
  ppuVar6 = (undefined **)FUN_1012d9850(0x58);
  ppuVar6[10] = (undefined *)0x0;
  ppuVar6[7] = (undefined *)0x0;
  ppuVar6[6] = (undefined *)0x0;
  ppuVar6[9] = (undefined *)0x0;
  ppuVar6[8] = (undefined *)0x0;
  ppuVar6[3] = (undefined *)0x0;
  ppuVar6[2] = (undefined *)0x0;
  ppuVar6[5] = (undefined *)0x0;
  ppuVar6[4] = (undefined *)0x0;
  ppuVar6[1] = (undefined *)0x0;
  *ppuVar6 = (undefined *)0x0;
  FUN_10128ed98();
  *ppuVar6 = (undefined *)&PTR_FUN_1067b8070;
  ppuVar6[5] = (undefined *)0x0;
  ppuVar6[6] = (undefined *)0x0;
  ppuVar6[3] = &DAT_10658efe0;
  ppuVar6[4] = (undefined *)0x0;
  ppuVar6[9] = (undefined *)0x0;
  ppuVar6[10] = (undefined *)0x0;
  ppuVar6[7] = &DAT_1067a0288;
  ppuVar6[8] = (undefined *)0x0;
  *(int *)(ppuVar6 + 1) = *(int *)(ppuVar6 + 1) + 1;
  lVar5 = param_1[0x62];
  local_a0 = ppuVar6;
  if ((lVar5 != 0) && (iVar3 = *(int *)(lVar5 + 8) + -1, *(int *)(lVar5 + 8) = iVar3, iVar3 == 0)) {
    FUN_10128eea0();
  }
  param_1[0x62] = (long)ppuVar6;
  param_1[0x66] = 0;
  param_1[0x65] = 0;
  param_1[100] = 0;
  param_1[99] = (long)&DAT_1065ab9b8;
  FUN_101565098(&local_a0);
  FUN_10150b1cc(param_1 + 0x67,local_a0);
  if ((local_a0 != (undefined **)0x0) &&
     (iVar3 = *(int *)(local_a0 + 1), *(int *)(local_a0 + 1) = iVar3 + -1, iVar3 + -1 == 0)) {
    FUN_10128eea0();
  }
  param_1[0x67] = (long)&PTR_thunk_FUN_10150b2b4_10673f310;
  FUN_101565098(&local_a0);
  FUN_10150b1cc(param_1 + 0x6a,local_a0);
  if ((local_a0 != (undefined **)0x0) &&
     (iVar3 = *(int *)(local_a0 + 1), *(int *)(local_a0 + 1) = iVar3 + -1, iVar3 + -1 == 0)) {
    FUN_10128eea0();
  }
  param_1[0x6a] = (long)&PTR_thunk_FUN_10150b2b4_10673f310;
  FUN_101565098(&local_a0);
  FUN_10150b1cc(param_1 + 0x6d,local_a0);
  if ((local_a0 != (undefined **)0x0) &&
     (iVar3 = *(int *)(local_a0 + 1), *(int *)(local_a0 + 1) = iVar3 + -1, iVar3 + -1 == 0)) {
    FUN_10128eea0();
  }
  param_1[0x6d] = (long)&PTR_thunk_FUN_10150b2b4_10673f310;
  FUN_1015643d8(&local_a0);
  FUN_10150b1cc(param_1 + 0x70,local_a0);
  if ((local_a0 != (undefined **)0x0) &&
     (iVar3 = *(int *)(local_a0 + 1), *(int *)(local_a0 + 1) = iVar3 + -1, iVar3 + -1 == 0)) {
    FUN_10128eea0();
  }
  param_1[0x70] = (long)&PTR_thunk_FUN_10150b2b4_10658fdd8;
  FUN_10156915c(&local_a0);
  FUN_10150b1cc(param_1 + 0x73,local_a0);
  if ((local_a0 != (undefined **)0x0) &&
     (iVar3 = *(int *)(local_a0 + 1), *(int *)(local_a0 + 1) = iVar3 + -1, iVar3 + -1 == 0)) {
    FUN_10128eea0();
  }
  param_1[0x73] = (long)&PTR_thunk_FUN_10150b2b4_10658fd48;
  FUN_1015740f0(&local_a0);
  FUN_10150b1cc(param_1 + 0x76,local_a0);
  if ((local_a0 != (undefined **)0x0) &&
     (iVar3 = *(int *)(local_a0 + 1), *(int *)(local_a0 + 1) = iVar3 + -1, iVar3 + -1 == 0)) {
    FUN_10128eea0();
  }
  param_1[0x76] = (long)&PTR_thunk_FUN_10150b2b4_106590220;
  FUN_102640760(&local_a0);
  FUN_10150b1cc(param_1 + 0x79,local_a0);
  if ((local_a0 != (undefined **)0x0) &&
     (iVar3 = *(int *)(local_a0 + 1), *(int *)(local_a0 + 1) = iVar3 + -1, iVar3 + -1 == 0)) {
    FUN_10128eea0();
  }
  param_1[0x79] = (long)&PTR_thunk_FUN_10150b2b4_1067b80c0;
  FUN_1015643d8(&local_a0);
  FUN_10150b1cc(param_1 + 0x7c,local_a0);
  if ((local_a0 != (undefined **)0x0) &&
     (iVar3 = *(int *)(local_a0 + 1), *(int *)(local_a0 + 1) = iVar3 + -1, iVar3 + -1 == 0)) {
    FUN_10128eea0();
  }
  param_1[0x7c] = (long)&PTR_thunk_FUN_10150b2b4_10658fdd8;
  param_1[0x7f] = (long)&PTR_FUN_1066026a8;
  param_1[0x80] = 0;
  param_1[0x82] = 0;
  param_1[0x81] = 0;
  param_1[0x83] = (long)&PTR_FUN_1066026a8;
  param_1[0x85] = 0;
  param_1[0x84] = 0;
  param_1[0x87] = 0;
  param_1[0x86] = 0;
  param_1[0x88] = 0;
  FUN_1025eb980(&local_a0);
  FUN_10150b1cc(param_1 + 0x89,local_a0);
  if ((local_a0 != (undefined **)0x0) &&
     (iVar3 = *(int *)(local_a0 + 1), *(int *)(local_a0 + 1) = iVar3 + -1, iVar3 + -1 == 0)) {
    FUN_10128eea0();
  }
  param_1[0x89] = (long)&PTR_thunk_FUN_10150b2b4_1067acd70;
  FUN_101486414(param_1);
  *(undefined4 *)(param_1 + 0x3d) = 0;
  local_a0 = (undefined **)PTR_CallMemberFunc<&AClip::OnUpdateTimeSelection>_106534a18;
  plStack_98 = param_1;
  FUN_10155e028(param_1[0x54],&local_a0);
  lVar5 = _DAT_10561dfd0;
  param_1[0x5d] = _UNK_10561dfd8;
  param_1[0x5c] = lVar5;
  local_a0 = (undefined **)PTR_CallMemberFunc<&AClip::OnCurrentStartChanged>_106534a10;
  plStack_98 = param_1;
  FUN_1015655f4(0,param_1[0x19],&local_a0);
  local_a0 = (undefined **)PTR_CallMemberFunc<&AClip::CurrentStartController>_106534aa8;
  plStack_98 = param_1;
  FUN_1015656bc(param_1[0x19],&local_a0);
  local_a0 = (undefined **)PTR_CallMemberFunc<&AClip::OnCurrentEndChanged>_106534a00;
  plStack_98 = param_1;
  FUN_1015655f4(0x3ff0000000000000,param_1[0x1c],&local_a0);
  local_a0 = (undefined **)PTR_CallMemberFunc<&AClip::CurrentEndController>_106534aa0;
  plStack_98 = param_1;
  FUN_1015656bc(param_1[0x1c],&local_a0);
  FUN_101565624(param_1[0x19],1,1);
  FUN_101565624(param_1[0x1c],1,1);
  puVar2 = PTR__lambda___1__ARemoteable__TRemoteableUpdate__106551c78;
  local_a0 = (undefined **)PTR__lambda___1__ARemoteable__TRemoteableUpdate__106551c78;
  plStack_98 = (long *)0x0;
  FUN_101564728(param_1[0x16],1,&local_a0);
  (**(code **)(*param_1 + 0x1e8))(0,param_1);
  local_a0 = (undefined **)PTR_CallMemberFunc<&AClip::LoopStartController>_106534a98;
  local_b0 = (int *)PTR_CallMemberFunc<&AClip::OnLoopStartOrEndChanged>_106534a30;
  local_c0 = PTR_CallMemberFunc<&AClip::LoopEndController>_106534a90;
  local_d0 = PTR_CallMemberFunc<&AClip::OnLoopStartOrEndChanged>_106534a30;
  local_e0 = PTR_CallMemberFunc<&AClip::StartRelativeController>_106534ab8;
  local_f0 = PTR_CallMemberFunc<&AClip::OnOffsetChanged>_1065349e8;
  local_100 = PTR_CallMemberFunc<&AClip::StartAbsoluteController>_106534ab0;
  local_110 = PTR_CallMemberFunc<&AClip::OnLoopStartAbsolute>_106534a08;
  local_120 = PTR_CallMemberFunc<&AClip::LoopOnController>_106534a80;
  local_130 = PTR_CallMemberFunc<&AClip::OnLoopOn>_106534a68;
  local_140 = PTR_CallMemberFunc<&(AClip::MinMaxLoopValues()const)>_106536320;
  local_150 = PTR_CallMemberFunc<&(AClip::MinLoopLength()const)>_106536328;
  plStack_148 = param_1;
  plStack_138 = param_1;
  plStack_128 = param_1;
  plStack_118 = param_1;
  plStack_108 = param_1;
  plStack_f8 = param_1;
  plStack_e8 = param_1;
  plStack_d8 = param_1;
  plStack_c8 = param_1;
  plStack_b8 = param_1;
  plStack_a8 = param_1;
  plStack_98 = param_1;
  FUN_10256c4ec(param_1[0x51],&local_a0,&local_b0,&local_c0,&local_d0,&local_e0,&local_f0,&local_100
                ,&local_110,&local_120,&local_130,&local_140,&local_150);
  lVar5 = FUN_10244ea54(param_1[0x57]);
  FUN_101458fc8(&local_a0,param_1);
  puVar1 = PTR_CallMemberFunc<&AClip::OnEnvelopeChanged>_106534a70;
  local_a0 = (undefined **)&DAT_106592510;
  local_80 = PTR_CallMemberFunc<&AClip::OnEnvelopeChanged>_106534a70;
  puVar4 = *(undefined8 **)(lVar5 + 0x10);
  plStack_78 = param_1;
  if (puVar4 < *(undefined8 **)(lVar5 + 0x18)) {
    puVar8 = puVar4 + 2;
    *puVar8 = 0;
    puVar4[1] = 0;
    puVar4[3] = local_88;
    if (local_88 != (undefined ***)0x0) {
      lVar10 = *(long *)((long)local_88 + 0x10);
      puVar9 = puVar4;
      if (lVar10 != 0) {
        puVar8 = (undefined8 *)(lVar10 + 8);
        puVar9 = (undefined8 *)*puVar8;
        puVar4[2] = lVar10;
        puVar9[2] = puVar4;
      }
      puVar4[1] = puVar9;
      *puVar8 = puVar4;
      *(undefined8 **)((long)local_88 + 0x10) = puVar4;
    }
    *puVar4 = &DAT_106592510;
    puVar4[5] = param_1;
    puVar4[4] = puVar1;
    puVar4 = puVar4 + 6;
  }
  else {
    puVar4 = (undefined8 *)FUN_1024491fc(lVar5 + 8,&local_a0);
  }
  *(undefined8 **)(lVar5 + 0x10) = puVar4;
  FUN_101459068(&local_a0);
  puVar1 = PTR_CallMemberFunc<&AClip::UpdateEngineWithoutArrangerProtocol>_106534a60;
  local_a0 = (undefined **)PTR_CallMemberFunc<&AClip::UpdateEngineWithoutArrangerProtocol>_106534a60
  ;
  plStack_98 = param_1;
  FUN_101564728(param_1[0xd],0,&local_a0);
  local_a0 = (undefined **)puVar1;
  plStack_98 = param_1;
  FUN_101564728(param_1[0x10],0,&local_a0);
  uVar7 = FUN_10245add0(param_1[0x35]);
  local_a0 = (undefined **)PTR_CallMemberFunc<&AClip::OnGrooveSettingsChanged>_106534a28;
  plStack_98 = param_1;
  FUN_10155c8c0(uVar7,param_1,&local_a0);
  local_a0 = (undefined **)PTR_CallMemberFunc<&AClip::OnClipDisabled>_1065349d8;
  plStack_98 = param_1;
  FUN_101564728(param_1[0x29],0,&local_a0);
  local_a0 = (undefined **)
             PTR___ZN7ableton7utility6detail13CallbackTypesI5AClipvJP15ARemoteableBoolbEE14CallMemberFuncIXadL_ZNS3_17IsMutedControllerES5_bEEEEvPvS5_b_106534a88
  ;
  plStack_98 = param_1;
  FUN_101564768(param_1[0x29],&local_a0);
  plVar12 = (long *)param_1[0x77];
  FUN_101427680(&local_a0,"Velocity Amount");
  (**(code **)(*plVar12 + 0x1c8))(plVar12,&local_a0);
  if ((local_a0 != (undefined **)0x0) &&
     (iVar3 = *(int *)local_a0, *(int *)local_a0 = iVar3 + -1, iVar3 + -1 == 0)) {
    FUN_101449efc();
  }
  lVar5 = param_1[0x77];
  uVar7 = FUN_1012d9850(0x38);
  FUN_101575868(0,0x3f800000,0x3c23d70a,0x3a83126f);
  local_a0 = (undefined **)PTR_CallMemberFunc<&AClip::OnVelocityAmountChanged>_106534a40;
  plStack_98 = param_1;
  FUN_1015743b0(0,0x3f800000,0,lVar5,uVar7,&local_a0);
  lVar5 = FUN_101849958();
  if (lVar5 == 0) {
    lVar5 = 0;
  }
  else {
    lVar5 = FUN_102676cf0();
  }
  FUN_101774608(param_1[0x3f],0);
  local_a0 = (undefined **)PTR_CallMemberFunc<&AClip::OnColorChanged>_1065349e0;
  plStack_98 = param_1;
  FUN_10155c8c0(param_1[0x3f],param_1,&local_a0);
  local_a0 = (undefined **)PTR_CallMemberFunc<&AClip::ColorController>_106534ad0;
  plStack_98 = param_1;
  FUN_101774970(param_1[0x3f],&local_a0);
  local_a0 = (undefined **)PTR_CallMemberFunc<&AClip::NameController>_106534ac0;
  plStack_98 = param_1;
  FUN_10156fde8(param_1[0x1f],&local_a0);
  lVar10 = FUN_102503e14(param_1[0x38]);
  FUN_101458fc8(&local_a0,param_1);
  puVar1 = PTR_CallMemberFunc<&AClip::OnFollowActionChanged>_1065349c8;
  local_a0 = (undefined **)&DAT_106592510;
  local_80 = PTR_CallMemberFunc<&AClip::OnFollowActionChanged>_1065349c8;
  puVar4 = *(undefined8 **)(lVar10 + 0x10);
  if (puVar4 < *(undefined8 **)(lVar10 + 0x18)) {
    puVar8 = puVar4 + 2;
    *puVar8 = 0;
    puVar4[1] = 0;
    puVar4[3] = local_88;
    if (local_88 != (undefined ***)0x0) {
      lVar11 = *(long *)((long)local_88 + 0x10);
      puVar9 = puVar4;
      if (lVar11 != 0) {
        puVar8 = (undefined8 *)(lVar11 + 8);
        puVar9 = (undefined8 *)*puVar8;
        puVar4[2] = lVar11;
        puVar9[2] = puVar4;
      }
      puVar4[1] = puVar9;
      *puVar8 = puVar4;
      *(undefined8 **)((long)local_88 + 0x10) = puVar4;
    }
    *puVar4 = &DAT_106592510;
    puVar4[5] = param_1;
    puVar4[4] = puVar1;
    *(undefined8 **)(lVar10 + 0x10) = puVar4 + 6;
    plStack_78 = param_1;
    FUN_101459068(&local_a0);
    lVar10 = param_1[0x4e];
    if (lVar5 == 0) goto LAB_102437e60;
LAB_102437e14:
    FUN_1026ab2ec(lVar5);
    uVar7 = FUN_1015661b8();
  }
  else {
    plStack_78 = param_1;
    uVar7 = FUN_100278ee0(lVar10 + 8,&local_a0);
    *(undefined8 *)(lVar10 + 0x10) = uVar7;
    FUN_101459068(&local_a0);
    lVar10 = param_1[0x4e];
    if (lVar5 != 0) goto LAB_102437e14;
LAB_102437e60:
    uVar7 = 0;
  }
  FUN_102438b44();
  puVar1 = PTR_CallMemberFunc<&AClip::UpdateEngineForLaunchParameters>_106534a58;
  local_a0 = (undefined **)PTR_CallMemberFunc<&AClip::UpdateEngineForLaunchParameters>_106534a58;
  plStack_98 = param_1;
  FUN_101567bfc(lVar10,uVar7,&DAT_10700a120,0,&local_a0);
  plVar12 = (long *)param_1[0x4e];
  FUN_101427680(&local_a0,"Launch Mode");
  (**(code **)(*plVar12 + 0x1c8))(plVar12,&local_a0);
  if ((local_a0 != (undefined **)0x0) &&
     (iVar3 = *(int *)local_a0, *(int *)local_a0 = iVar3 + -1, iVar3 + -1 == 0)) {
    FUN_101449efc();
  }
  lVar10 = param_1[0x4b];
  uVar7 = 0;
  if (lVar5 != 0) {
    FUN_1026ab2f4(lVar5);
    uVar7 = FUN_1015661b8();
  }
  FUN_102438d00();
  local_a0 = (undefined **)puVar1;
  plStack_98 = param_1;
  FUN_101567bfc(lVar10,uVar7,&DAT_10700a138,0,&local_a0);
  plVar12 = (long *)param_1[0x4b];
  FUN_101427680(&local_a0,"Launch Quantisation");
  (**(code **)(*plVar12 + 0x1c8))(plVar12,&local_a0);
  if ((local_a0 != (undefined **)0x0) &&
     (iVar3 = *(int *)local_a0, *(int *)local_a0 = iVar3 + -1, iVar3 + -1 == 0)) {
    FUN_101449efc();
  }
  plVar12 = (long *)param_1[0x3b];
  FUN_101427680(&local_158,"Original Signature");
  (**(code **)(*plVar12 + 0x1e8))(plVar12,&local_158);
  if ((local_158 != (int *)0x0) && (iVar3 = *local_158, *local_158 = iVar3 + -1, iVar3 + -1 == 0)) {
    FUN_101449efc();
  }
  FUN_102426b28(param_1[0x13],param_1[0x3b]);
  lVar5 = param_1[0x5a];
  FUN_1024390a0();
  local_a0 = (undefined **)puVar2;
  plStack_98 = (long *)0x0;
  FUN_101567bfc(lVar5,0,&DAT_10700a168,0,&local_a0);
  local_a0 = (undefined **)puVar2;
  plStack_98 = (long *)0x0;
  FUN_101564728(param_1[0x26],1,&local_a0);
  FUN_10155baa4(param_1[0x26],1);
  local_a0 = (undefined **)PTR_CallMemberFunc<&AClip::OnKeepPlayPositionBang>_106534a20;
  plStack_98 = param_1;
  FUN_101564728(param_1[0x5f],0,&local_a0);
  local_a0 = (undefined **)puVar2;
  plStack_98 = (long *)0x0;
  FUN_1015655f4(0,param_1[0x68],&local_a0);
  local_a0 = (undefined **)puVar2;
  plStack_98 = (long *)0x0;
  FUN_1015655f4(0,param_1[0x6b],&local_a0);
  *(undefined1 *)(param_1 + 0x61) = 1;
  plVar12 = (long *)param_1[0x22];
  FUN_101447580(&local_a0,&DAT_10700a0c0);
  (**(code **)(*plVar12 + 0x1c8))(plVar12,&local_a0);
  if ((local_a0 != (undefined **)0x0) &&
     (iVar3 = *(int *)local_a0, *(int *)local_a0 = iVar3 + -1, iVar3 + -1 == 0)) {
    FUN_101449efc();
  }
  local_a0 = (undefined **)puVar2;
  plStack_98 = (long *)0x0;
  FUN_1015655f4(0,param_1[0x6e],&local_a0);
  FUN_10155baa4(param_1[0x6e],1);
  lVar5 = param_1[0x48];
  iVar3 = FUN_1015661b8(*(undefined8 *)(param_1[0x45] + 0x30));
  local_a0 = (undefined **)puVar2;
  plStack_98 = (long *)0x0;
  FUN_101564728(lVar5,iVar3 == 2,&local_a0);
  FUN_10155baa4(param_1[0x48],1);
  local_a0 = (undefined **)PTR_CallMemberFunc<&AClip::OnRecordingStateChanged>_106534a38;
  plStack_98 = param_1;
  FUN_10155c8c0(*(undefined8 *)(param_1[0x45] + 0x30),param_1,&local_a0);
  local_a0 = (undefined **)puVar2;
  plStack_98 = (long *)0x0;
  FUN_101564728(param_1[0x71],0,&local_a0);
  FUN_10155baa4(param_1[0x71],1);
  local_a0 = (undefined **)PTR_CallMemberFunc<&AClip::OnTakeIdChanged>_1065349f0;
  plStack_98 = param_1;
  FUN_10156934c(param_1[0x74],0xffffffff,&local_a0);
  lVar5 = FUN_101849958();
  if (((lVar5 == 0) || (iVar3 = FUN_10184d7e0(lVar5), iVar3 == 0)) ||
     (lVar10 = FUN_10184a7f4(lVar5), lVar10 == 0)) {
    lVar5 = 0;
    lVar10 = param_1[0x7d];
LAB_102438188:
    uVar7 = 0;
    bVar13 = true;
  }
  else {
    lVar5 = FUN_10184a7f4(lVar5);
    lVar10 = param_1[0x7d];
    if (lVar5 == 0) goto LAB_102438188;
    FUN_10269222c(lVar5);
    uVar7 = FUN_1015645a0();
    bVar13 = false;
  }
  local_a0 = (undefined **)PTR_CallMemberFunc<&AClip::OnIsInKeyChanged>_1065349f8;
  plStack_98 = param_1;
  FUN_101564728(lVar10,uVar7,&local_a0);
  local_a0 = (undefined **)PTR_CallMemberFunc<&AClip::InKeyController>_106534a78;
  plStack_98 = param_1;
  FUN_101564768(param_1[0x7d],&local_a0);
  if (bVar13) {
    puVar4 = (undefined8 *)FUN_1026400c4();
    local_b0 = (int *)*puVar4;
    uVar7 = 0;
    if (local_b0 == (int *)0x0) {
      lVar5 = param_1[0x7a];
    }
    else {
      *local_b0 = *local_b0 + 1;
      lVar5 = param_1[0x7a];
LAB_102438214:
      *local_b0 = *local_b0 + 1;
    }
  }
  else {
    FUN_10269220c(lVar5);
    FUN_102640f6c(&local_b0);
    FUN_10269220c(lVar5);
    uVar7 = FUN_102640d7c();
    lVar5 = param_1[0x7a];
    if (local_b0 != (int *)0x0) goto LAB_102438214;
  }
  local_160 = local_b0;
  FUN_102640b40(lVar5,uVar7,&local_160);
  if ((local_160 != (int *)0x0) && (iVar3 = *local_160, *local_160 = iVar3 + -1, iVar3 + -1 == 0)) {
    FUN_101449efc();
  }
  local_a0 = (undefined **)PTR_CallMemberFunc<&AClip::OnScaleInformationChanged>_106534a48;
  plStack_98 = param_1;
  FUN_10155e028(param_1[0x7a],&local_a0);
  local_a0 = (undefined **)PTR_CallMemberFunc<&AClip::ScaleController>_106534ac8;
  plStack_98 = param_1;
  FUN_102641db8(param_1[0x7a],&local_a0);
  local_a0 = &PTR_FUN_1067b8150;
  plStack_98 = param_1;
  local_88 = &local_a0;
  FUN_1025ebb00(param_1[0x8a],&local_a0);
  if (local_88 == &local_a0) {
    lVar5 = 0x20;
  }
  else {
    if (local_88 == (undefined ***)0x0) goto LAB_1024382e8;
    lVar5 = 0x28;
  }
  (**(code **)((long)*local_88 + lVar5))();
LAB_1024382e8:
  if ((local_b0 != (int *)0x0) && (iVar3 = *local_b0, *local_b0 = iVar3 + -1, iVar3 + -1 == 0)) {
    FUN_101449efc();
  }
  if (*(long *)PTR____stack_chk_guard_1064f8818 == local_70) {
    return param_1;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

