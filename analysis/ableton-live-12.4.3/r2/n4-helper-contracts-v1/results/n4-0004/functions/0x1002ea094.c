
/* WARNING: Removing unreachable block (ram,0x0001002eac54) */
/* WARNING: Removing unreachable block (ram,0x0001002ea47c) */
/* WARNING: Removing unreachable block (ram,0x0001002ea3f8) */
/* WARNING: Removing unreachable block (ram,0x0001002eac88) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1002ea094(void)

{
  char cVar1;
  uint uVar2;
  uint uVar3;
  code *pcVar4;
  int iVar5;
  undefined8 uVar6;
  undefined8 uVar7;
  long *plVar8;
  undefined *puVar9;
  long lVar10;
  undefined ***pppuVar11;
  undefined4 *puVar12;
  ulong extraout_x1;
  ulong extraout_x1_00;
  ulong extraout_x1_01;
  ulong extraout_x1_02;
  ulong extraout_x1_03;
  ulong extraout_x1_04;
  undefined4 uVar13;
  ulong uVar14;
  char *pcVar15;
  undefined4 local_728 [2];
  int *local_720;
  undefined1 auStack_718 [104];
  undefined **local_6b0 [2];
  undefined1 auStack_6a0 [8];
  undefined8 local_698;
  undefined1 auStack_688 [8];
  undefined8 local_680;
  undefined1 auStack_670 [8];
  undefined8 local_668;
  void *local_658;
  void *local_650;
  undefined1 auStack_640 [360];
  int *local_4d8 [13];
  long *local_470 [13];
  long *local_408 [13];
  long *local_3a0;
  undefined8 uStack_398;
  undefined8 uStack_390;
  undefined8 uStack_388;
  long *local_330;
  undefined8 uStack_328;
  undefined8 uStack_320;
  undefined8 uStack_318;
  char *local_2c0;
  ulong uStack_2b8;
  long lStack_2b0;
  undefined8 uStack_2a8;
  long *local_250;
  long *plStack_248;
  undefined8 uStack_240;
  undefined8 uStack_238;
  undefined **local_1e0;
  long *plStack_1d8;
  long lStack_1d0;
  undefined8 uStack_1c8;
  undefined ***local_170;
  undefined ***pppuStack_168;
  undefined8 local_160;
  undefined ****local_158;
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_1064f8818;
  thunk_FUN_1011c2bb0(auStack_640,"Ableton","Live","12.4.3","12.0",4,0x612d6c76);
  FUN_1011c368c(auStack_640,1);
  FUN_1011c39e0(auStack_640);
  FUN_1011db860();
  uVar3 = DAT_105674bd0;
  uVar2 = DAT_105674bd0 >> 1;
  FUN_100e47578(auStack_718,DAT_105674bd0,uVar2);
  FUN_1011b54ec(&local_170,1);
  uVar6 = FUN_100e47670(auStack_718,&local_170);
  thunk_FUN_103f3cdf4(&local_1e0);
  uVar7 = FUN_100e47670(uVar6,&local_1e0);
  local_2c0 = operator_new(0x20);
  uVar6 = s_Python_scripting_engine_options_105ab032e._0_8_;
  lStack_2b0 = _UNK_1055cdf68;
  uStack_2b8 = _DAT_1055cdf60;
  *(ulong *)(local_2c0 + 8) =
       CONCAT17(s_Python_scripting_engine_options_105ab032e[0xf],
                s_Python_scripting_engine_options_105ab032e._8_7_);
  *(undefined8 *)local_2c0 = uVar6;
  uVar6 = CONCAT71(s_Python_scripting_engine_options_105ab032e._16_7_,
                   s_Python_scripting_engine_options_105ab032e[0xf]);
  *(undefined8 *)(local_2c0 + 0x17) = s_Python_scripting_engine_options_105ab032e._23_8_;
  *(undefined8 *)(local_2c0 + 0xf) = uVar6;
  local_2c0[0x1f] = '\0';
  FUN_100e47604(&local_250,&local_2c0,uVar3,uVar2);
  if (lStack_2b0 < 0) {
    operator_delete(local_2c0);
  }
  local_2c0 = (char *)FUN_100e47938(&local_250);
  uVar6 = FUN_100e4ce20();
  FUN_100e47398(&local_2c0,"python-output-to-terminal",uVar6,
                "Redirect python output to the terminal");
  uVar6 = FUN_100e47670(uVar7,&local_250);
  FUN_1008e6768(&local_2c0);
  uVar6 = FUN_100e47670(uVar6,&local_2c0);
  FUN_1008e541c(&local_330);
  uVar6 = FUN_100e47670(uVar6,&local_330);
  FUN_100331cb4(&local_3a0);
  uVar6 = FUN_100e47670(uVar6,&local_3a0);
  FUN_1011ad78c(local_408);
  uVar6 = FUN_100e47670(uVar6,local_408);
  FUN_1011cbc34(local_470);
  uVar6 = FUN_100e47670(uVar6,local_470);
  FUN_102370d94(local_4d8);
  FUN_100e47670(uVar6,local_4d8);
  FUN_1002fe554(local_4d8);
  FUN_1002fe554(local_470);
  FUN_1002fe554(local_408);
  FUN_1002fe554(&local_3a0);
  FUN_1002fe554(&local_330);
  FUN_1002fe554(&local_2c0);
  FUN_1002fe554(&local_250);
  FUN_1002fe554(&local_1e0);
  FUN_1002fe554(&local_170);
  local_170 = (undefined ***)FUN_100e47938(auStack_718);
  uVar6 = FUN_100e4ce20();
  FUN_100e47398(&local_170,"help,h",uVar6,"Show this help");
  FUN_1016b6c70(&local_250);
  pppuStack_168 = (undefined ***)0x0;
  local_170 = (undefined ***)0x0;
  local_160 = 0;
  FUN_1011b7b70(local_6b0,&local_250,auStack_718,1,&local_170);
  if (local_160 < 0) {
    operator_delete(local_170);
  }
  local_160 = CONCAT17(4,(undefined7)local_160);
  local_170 = (undefined ***)CONCAT35(local_170._5_3_,0x706c6568);
  plVar8 = (long *)FUN_100e53e88(local_6b0,&local_170);
  puVar9 = PTR_typeinfo_1064f8750;
  if ((long *)*plVar8 != (long *)0x0) {
    puVar9 = (undefined *)(**(code **)(*(long *)*plVar8 + 0x10))();
  }
  pcVar15 = (char *)(*(ulong *)(PTR_typeinfo_1064f86f0 + 8) & 0x7fffffffffffffff);
  if (((char *)(*(ulong *)(puVar9 + 8) & 0x7fffffffffffffff) != pcVar15) &&
     (iVar5 = _strcmp((char *)(*(ulong *)(puVar9 + 8) & 0x7fffffffffffffff),pcVar15), iVar5 != 0)) {
    local_1e0 = (undefined **)0x0;
    std::bad_cast::bad_cast((bad_cast *)&local_1e0);
    local_1e0 = &PTR__bad_cast_10659c938;
    FUN_1002fdf48(&local_1e0);
    goto LAB_1002eb1e8;
  }
  cVar1 = *(char *)(*plVar8 + 8);
  if (local_160 < 0) {
    operator_delete(local_170);
  }
  if (cVar1 != '\0') {
                    /* WARNING: Subroutine does not return */
    FUN_1011b5244();
  }
  if (local_250 != (long *)0x0) {
    for (; plStack_248 != local_250; plStack_248 = plStack_248 + -3) {
    }
    plStack_248 = local_250;
    operator_delete(local_250);
  }
  FUN_1002fe554(auStack_718);
  FUN_1011aea94(&local_658);
  uVar6 = FUN_1002e9f08();
  FUN_1012109e8();
  pppuStack_168 = (undefined ***)0x0;
  local_170 = (undefined ***)0x0;
  local_160 = 0;
  FUN_1011b5630(local_6b0,0,&local_170);
  if (local_170 != (undefined ***)0x0) {
    for (; pppuStack_168 != local_170; pppuStack_168 = pppuStack_168 + -3) {
    }
    pppuStack_168 = local_170;
    operator_delete(local_170);
  }
  iVar5 = FUN_1011b59ec();
  if (iVar5 == 1) {
LAB_1002ea54c:
    FUN_1011b5360();
  }
  else {
    pppuStack_168 = _UNK_1055d8118;
    local_170 = _DAT_1055d8110;
    local_158 = (undefined ****)_UNK_1055d8128;
    local_160 = _DAT_1055d8120;
    FUN_1011aeb80(&local_170);
    if ((extraout_x1 & 1) != 0) goto LAB_1002ea54c;
    plStack_1d8 = _UNK_1055d8138;
    local_1e0 = _DAT_1055d8130;
    uStack_1c8 = _UNK_1055d8148;
    lStack_1d0 = _DAT_1055d8140;
    FUN_1011aeb80(&local_1e0);
    if ((extraout_x1_00 & 1) != 0) goto LAB_1002ea54c;
    plStack_248 = _UNK_1055d8158;
    local_250 = _DAT_1055d8150;
    uStack_238 = _UNK_1055d8168;
    uStack_240 = _DAT_1055d8160;
    FUN_1011aeb80(&local_250);
    if ((extraout_x1_01 & 1) != 0) goto LAB_1002ea54c;
    uStack_2b8 = _UNK_1055d8178;
    local_2c0 = _DAT_1055d8170;
    uStack_2a8 = _UNK_1055d8188;
    lStack_2b0 = _DAT_1055d8180;
    FUN_1011aeb80(&local_2c0);
    if ((extraout_x1_02 & 1) != 0) goto LAB_1002ea54c;
    uStack_328 = _UNK_1055d8198;
    local_330 = _DAT_1055d8190;
    uStack_318 = _UNK_1055d81a8;
    uStack_320 = _DAT_1055d81a0;
    FUN_1011aeb80(&local_330);
    if ((extraout_x1_03 & 1) != 0) goto LAB_1002ea54c;
    uStack_398 = _UNK_1055d81b8;
    local_3a0 = _DAT_1055d81b0;
    uStack_388 = _UNK_1055d81c8;
    uStack_390 = _DAT_1055d81c0;
    FUN_1011aeb80(&local_3a0);
    if ((extraout_x1_04 & 1) != 0) goto LAB_1002ea54c;
  }
  FUN_1011e899c(&local_170);
  FUN_1011e88b8(&local_2c0,&local_170);
  if ((local_170 != (undefined ***)0x0) &&
     (iVar5 = *(int *)local_170, *(int *)local_170 = iVar5 + -1, iVar5 + -1 == 0)) {
    FUN_101449efc();
  }
  if ((int)uStack_2b8 == -1) {
                    /* WARNING: Subroutine does not return */
    FUN_10024d044();
  }
  local_170 = &local_1e0;
  (*(code *)(&PTR_FUN_10659c970)[uStack_2b8 & 0xffffffff])(&local_170,&local_2c0);
  FUN_1011af958();
  FUN_1011db880(&local_1e0);
  uStack_240 = CONCAT17(7,(undefined7)uStack_240);
  local_250 = (long *)0x7478742e676f4c;
  FUN_1011bc93c(&local_170,&local_1e0,&local_250);
  FUN_1011bbb00(local_6b0,&local_170);
  if (local_160 < 0) {
    operator_delete(local_170);
  }
  if (uStack_240 < 0) {
    operator_delete(local_250);
  }
  if (lStack_1d0 < 0) {
    operator_delete(local_1e0);
  }
  DAT_106ec26d8 = FUN_1011e89b4();
  local_170 = operator_new(0x20);
  uVar7 = s_python_output_to_terminal_105ab034e._0_8_;
  local_160 = _UNK_1055cdf98;
  pppuStack_168 = (undefined ***)_DAT_1055cdf90;
  local_170[1] = (undefined **)
                 CONCAT71(s_python_output_to_terminal_105ab034e._9_7_,
                          s_python_output_to_terminal_105ab034e[8]);
  *local_170 = (undefined **)uVar7;
  uVar7 = CONCAT17(s_python_output_to_terminal_105ab034e[0x10],
                   s_python_output_to_terminal_105ab034e._9_7_);
  *(undefined8 *)((long)local_170 + 0x11) = s_python_output_to_terminal_105ab034e._17_8_;
  *(undefined8 *)((long)local_170 + 9) = uVar7;
  *(char *)((long)local_170 + 0x19) = '\0';
  plVar8 = (long *)FUN_100e53e88(local_6b0,&local_170);
  if ((long *)*plVar8 == (long *)0x0) {
    uVar14 = *(ulong *)(PTR_typeinfo_1064f8750 + 8);
  }
  else {
    lVar10 = (**(code **)(*(long *)*plVar8 + 0x10))();
    uVar14 = *(ulong *)(lVar10 + 8);
  }
  if (((char *)(uVar14 & 0x7fffffffffffffff) != pcVar15) &&
     (iVar5 = _strcmp((char *)(uVar14 & 0x7fffffffffffffff),pcVar15), iVar5 != 0)) {
    local_1e0 = (undefined **)0x0;
    std::bad_cast::bad_cast((bad_cast *)&local_1e0);
    local_1e0 = &PTR__bad_cast_10659c938;
    FUN_1002fdf48(&local_1e0);
LAB_1002eb1e8:
                    /* WARNING: Does not return */
    pcVar4 = (code *)SoftwareBreakpoint(1,0x1002eb1ec);
    (*pcVar4)();
  }
  thunk_FUN_1017d47d4(*(undefined1 *)(*plVar8 + 8));
  if (local_160 < 0) {
    operator_delete(local_170);
  }
  FUN_1011db938(&local_1e0);
  (**(code **)(*plStack_1d8 + 0x100))(&local_170);
  FUN_1017d5690(&local_170);
  if (local_160 < 0) {
    operator_delete(local_170);
  }
  if ((local_1e0 != (undefined **)0x0) &&
     (iVar5 = *(int *)(local_1e0 + 1), *(int *)(local_1e0 + 1) = iVar5 + -1, iVar5 + -1 == 0)) {
    FUN_10128eea0();
  }
  local_170 = (undefined ***)&PTR_FUN_10659c990;
  pppuStack_168 = (undefined ***)FUN_10036c388;
  local_158 = &local_170;
  FUN_1017d668c(&local_170);
  if (local_158 == &local_170) {
    lVar10 = 0x20;
LAB_1002ea790:
    (**(code **)((long)*local_158 + lVar10))();
  }
  else if (local_158 != (undefined ****)0x0) {
    lVar10 = 0x28;
    goto LAB_1002ea790;
  }
  FUN_100e6d03c(local_408,"abl.live");
  FUN_100e59c34(&local_3a0,local_408);
  lVar10 = *local_408[0];
  *local_408[0] = lVar10 + -1;
  if (lVar10 + -1 == 0) {
    FUN_101032fbc();
  }
  *local_3a0 = *local_3a0 + 1;
  local_250 = local_3a0;
  plStack_248 = (long *)0x105ab0390;
  FUN_1014552a0(local_4d8);
  FUN_1014320f0(&local_1e0,local_4d8);
  FUN_100e6cbc4(&local_330,&local_250,plStack_248);
  FUN_1002feb04(local_470,local_330,"12.4.3","e3d8be4d07c71dbd4de9e4183bf90652f680375b",&local_1e0,0
               );
  lVar10 = *local_330;
  *local_330 = lVar10 + -1;
  if (lVar10 + -1 == 0) {
    FUN_101032fbc();
  }
  lVar10 = *local_470[0];
  *local_470[0] = lVar10 + -1;
  if (lVar10 + -1 == 0) {
    FUN_101032fbc();
  }
  if (lStack_1d0 < 0) {
    operator_delete(local_1e0);
  }
  if ((local_4d8[0] != (int *)0x0) &&
     (iVar5 = *local_4d8[0], *local_4d8[0] = iVar5 + -1, iVar5 + -1 == 0)) {
    FUN_101449efc();
  }
  lVar10 = *local_250;
  *local_250 = lVar10 + -1;
  if (lVar10 + -1 == 0) {
    FUN_101032fbc();
  }
  lVar10 = *local_3a0;
  *local_3a0 = lVar10 + -1;
  if (lVar10 + -1 == 0) {
    FUN_101032fbc();
  }
  FUN_101210ec8(local_6b0,1);
  FUN_10148935c(1);
  FUN_10153e578(1);
  FUN_101655498();
  FUN_10157fddc(1);
  thunk_FUN_1016353c8();
  iVar5 = FUN_1011b59ec();
  pppuVar11 = (undefined ***)FUN_1012d9850(0x20);
  if (iVar5 == 2) {
    FUN_10128ed98(pppuVar11);
    puVar9 = &UNK_1065d15f0;
  }
  else {
    FUN_10128ed98(pppuVar11);
    puVar9 = &UNK_1067a1df0;
  }
  pppuStack_168 = pppuVar11 + 3;
  *pppuStack_168 = (undefined **)(puVar9 + 0x90);
  *pppuVar11 = (undefined **)(puVar9 + 0x10);
  *(int *)(pppuVar11 + 1) = *(int *)(pppuVar11 + 1) + 1;
  local_170 = pppuVar11;
  iVar5 = FUN_1011b59ec();
  uVar13 = 100;
  if (iVar5 != 2) {
    uVar13 = 60000;
  }
  FUN_10235e080(uVar6,&local_170,uVar13,local_6b0);
  if ((local_170 != (undefined ***)0x0) &&
     (iVar5 = *(int *)(local_170 + 1), *(int *)(local_170 + 1) = iVar5 + -1, iVar5 + -1 == 0)) {
    FUN_10128eea0();
  }
  uVar14 = FUN_101ac3ddc(1);
  if ((uVar14 & 1) == 0) {
    uVar6 = ___cxa_allocate_exception(0x30);
    FUN_1011cb734(&local_170);
    FUN_1011cb734(&local_1e0);
    FUN_1011cb734(&local_250);
    FUN_1011cb734(&local_330);
    FUN_1011cb734(&local_3a0);
    FUN_101242ce8(uVar6,&DAT_106ec32e0,&local_170,&local_1e0,&local_250,&local_330,&local_3a0);
                    /* WARNING: Subroutine does not return */
    ___cxa_throw(uVar6,&PTR_vtable_106661270,FUN_10124335c);
  }
  FUN_101b3b444();
  FUN_101b59a90();
  FUN_101b84770();
  FUN_10212ce2c();
  FUN_102fd8550();
  FUN_10225c4b0();
  FUN_10178ac20();
  FUN_1019f55c4();
  FUN_103e68308();
  FUN_10217c68c();
  FUN_102295fd0();
  FUN_1022b4a48();
  FUN_102312394();
  FUN_10239ef3c();
  puVar12 = (undefined4 *)FUN_1027d854c();
  local_728[0] = *puVar12;
  local_720 = *(int **)(puVar12 + 2);
  if (local_720 != (int *)0x0) {
    *local_720 = *local_720 + 1;
  }
  FUN_102551844(local_728);
  if ((local_720 != (int *)0x0) && (iVar5 = *local_720, *local_720 = iVar5 + -1, iVar5 + -1 == 0)) {
    FUN_101449efc();
  }
  FUN_10278d554();
  FUN_10295b8e8();
  FUN_102811fb4();
  FUN_1028ab630();
  FUN_1029af4e4(1);
  FUN_102be25a4();
  FUN_10305bb34();
  FUN_102a297b8();
  FUN_1030e7ad4();
  FUN_10330a02c();
  FUN_1033cf4ac();
  FUN_103420ec8();
  FUN_1039f8940();
  FUN_1033d852c();
  FUN_1038f3dd4();
  FUN_1035201c8();
  FUN_103814418();
  FUN_10367f4f8();
  FUN_10374214c();
  FUN_103ce04cc();
  FUN_103dbe4c0();
  FUN_103e57a94();
  uVar6 = FUN_101505400();
  uVar7 = FUN_101a4517c();
  FUN_1015093e0(uVar6,uVar7);
  plVar8 = (long *)FUN_10157c3d0();
  (**(code **)(*plVar8 + 0x80))(plVar8,1,100);
  pppuVar11 = (undefined ***)FUN_1012d9850(0x20);
  FUN_10128ed98();
  pppuStack_168 = pppuVar11 + 3;
  *pppuStack_168 = &PTR_FUN_10668eb38;
  *pppuVar11 = &PTR_thunk_FUN_10128edf8_10668eaf0;
  *(int *)(pppuVar11 + 1) = *(int *)(pppuVar11 + 1) + 1;
  local_170 = pppuVar11;
  FUN_101446418(&local_170);
  if ((local_170 != (undefined ***)0x0) &&
     (iVar5 = *(int *)(local_170 + 1), *(int *)(local_170 + 1) = iVar5 + -1, iVar5 + -1 == 0)) {
    FUN_10128eea0();
  }
  FUN_1008e5594(local_6b0);
  FUN_100331dbc(local_6b0);
  FUN_1008e6898(local_6b0);
  FUN_1023123b8();
  local_170 = (undefined ***)&DAT_10659ca40;
  local_158 = &local_170;
  FUN_102fe12bc(&local_170);
  if (local_158 == &local_170) {
    lVar10 = 0x20;
  }
  else {
    if (local_158 == (undefined ****)0x0) goto LAB_1002eab80;
    lVar10 = 0x28;
  }
  (**(code **)((long)*local_158 + lVar10))();
LAB_1002eab80:
  uVar14 = FUN_101455b80();
  if ((((uVar14 & 1) == 0) &&
      (((FUN_1011d6094(&local_170), local_170 != (undefined ***)0x0 &&
        (((ulong)*local_170 & 0xfffffffe00000000) == 0x200000000)) ||
       (FUN_101455430(&local_170), local_170 != (undefined ***)0x0)))) &&
     (iVar5 = *(int *)local_170, *(int *)local_170 = iVar5 + -1, iVar5 + -1 == 0)) {
    FUN_101449efc();
  }
  FUN_10147e8b4(&DAT_106e067e0);
  FUN_10147e8b4(&DAT_106e068a8);
  FUN_10147e8b4(&DAT_106e06970);
  FUN_10147e8b4(&DAT_106e06a38);
  FUN_10147e8b4(&DAT_106e06b00);
  FUN_10147e8b4(&DAT_106e06bc8);
  if ((int)uStack_2b8 != -1) {
    (*(code *)(&PTR_FUN_10659cac0)[uStack_2b8 & 0xffffffff])(&local_170,&local_2c0);
  }
  if (local_658 != (void *)0x0) {
    for (; local_650 != local_658; local_650 = (void *)((long)local_650 + -0x30)) {
    }
    local_650 = local_658;
    operator_delete(local_658);
  }
  local_6b0[0] = &PTR_FUN_106622408;
  FUN_1002fee40(auStack_670,local_668);
  FUN_1002feeb8(auStack_688,local_680);
  FUN_1002fef18(auStack_6a0,local_698);
  FUN_1002fcaa8(auStack_640);
  if (*(long *)PTR____stack_chk_guard_1064f8818 == local_58) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail(1);
}

