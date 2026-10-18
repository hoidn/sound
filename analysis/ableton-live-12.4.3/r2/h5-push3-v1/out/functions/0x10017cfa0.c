// 0x10017cfa0 FUN_10017cfa0 state=exported-with-warnings role=application main: hardware search, sockets, ScriptHost, main loop
// source chunk chunk-00065.jsonl; code_sha256=459248b58956f117db2fdf51aea6763c23729383a455ab4bf1e6db832707e2da

/* WARNING: Removing unreachable block (ram,0x00010017d454) */
/* WARNING: Removing unreachable block (ram,0x00010017d220) */
/* WARNING: Removing unreachable block (ram,0x00010017d2ec) */
/* WARNING: Removing unreachable block (ram,0x00010017d438) */
/* WARNING: Removing unreachable block (ram,0x00010017d758) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 FUN_10017cfa0(undefined8 param_1,undefined8 param_2,long param_3)

{
  byte *pbVar1;
  undefined *puVar2;
  undefined4 uVar3;
  undefined1 uVar4;
  char cVar5;
  byte bVar6;
  long lVar7;
  undefined6 uVar8;
  undefined2 uVar9;
  undefined6 uVar10;
  code *pcVar11;
  uint uVar12;
  int iVar13;
  int iVar14;
  undefined **ppuVar15;
  undefined8 uVar16;
  undefined8 uVar17;
  undefined8 uVar18;
  long lVar19;
  long *plVar20;
  long lVar21;
  long lVar22;
  undefined ***pppuVar23;
  long lVar24;
  runtime_error *prVar25;
  ulong extraout_x1;
  long lVar26;
  undefined **ppuVar27;
  long *plVar28;
  undefined ***pppuVar29;
  undefined ****ppppuVar30;
  undefined1 auVar31 [16];
  undefined1 uStack_a59;
  undefined **local_a58;
  uint local_a50;
  undefined1 local_a4c;
  undefined **local_a48;
  undefined8 uStack_a40;
  undefined7 local_a38;
  char cStack_a31;
  undefined **local_a30;
  undefined8 uStack_a28;
  long local_a20;
  void *local_a10;
  undefined8 uStack_a08;
  long local_a00;
  undefined1 auStack_9f8 [11];
  byte local_9ed;
  uint local_9ec;
  long *local_9e8 [2];
  char local_9d1;
  undefined **local_6b8;
  void *local_6b0;
  undefined1 auStack_6a8 [7];
  char local_6a1;
  undefined ***local_6a0;
  undefined1 auStack_680 [448];
  void *local_4c0;
  void *local_4b8;
  long local_4a8;
  undefined **local_4a0 [11];
  void *local_448;
  void *local_440;
  void *local_430;
  void *local_428;
  void *local_418;
  void *local_410;
  undefined **local_3f0;
  void *local_3e8;
  void *local_3e0;
  long alStack_3d0 [3];
  long *local_3b8;
  long alStack_3b0 [3];
  long *local_398;
  void *local_388;
  void *local_380;
  long *local_370;
  void *local_340;
  char local_329;
  char local_328;
  long alStack_320 [3];
  long *local_308;
  byte local_300;
  undefined **local_2f8;
  byte *local_2f0;
  undefined ***local_2e0;
  undefined **local_2d8 [3];
  undefined ***local_2c0;
  undefined **local_2b8 [3];
  undefined ***local_2a0;
  long *local_298;
  long *local_290;
  char local_281;
  undefined **local_100;
  undefined6 uStack_f8;
  undefined2 uStack_f2;
  char acStack_f0 [6];
  undefined1 uStack_ea;
  undefined1 uStack_e9;
  undefined ***local_e8;
  undefined1 auStack_d8 [8];
  undefined8 local_d0;
  long *local_b8;
  undefined **local_a0;
  byte *pbStack_98;
  undefined8 local_90;
  undefined ***local_88 [2];
  long local_78;
  
  local_78 = *(long *)PTR____stack_chk_guard_101b8c408;
  FUN_100286584(alStack_320);
  local_a50 = local_a50 & 0xffffff00;
  local_a4c = 0;
  if ((*(byte *)(param_3 + 0x46) & 1) == 0) {
    local_6b8 = (undefined **)&DAT_3b9aca00;
    std::this_thread::sleep_for((duration *)&local_6b8);
    uVar12 = FUN_1002867e0();
    if ((extraout_x1 >> 0x20 & 1) == 0) {
      prVar25 = (runtime_error *)___cxa_allocate_exception(0x10);
      std::runtime_error::runtime_error(prVar25,"No Push hardware found");
                    /* WARNING: Subroutine does not return */
      ___cxa_throw(prVar25,PTR_typeinfo_101b8c318,PTR__runtime_error_101b8c1f0);
    }
    local_a4c = 1;
    local_a50 = uVar12;
    FUN_1001ce5b0(&local_6b8);
    plVar28 = operator_new(0x278);
    thunk_FUN_100275ed0(plVar28,&local_6b8,uVar12 == 1);
    if (local_6a1 < '\0') {
      operator_delete(local_6b8);
    }
    FUN_10017eabc(&local_6b8,&local_a50);
    FUN_10017ec18(&local_6b8);
    if ((long)local_6a0 < 0) {
      operator_delete(local_6b0);
    }
    ppuVar15 = local_6b8;
    local_6b8 = (undefined **)0x0;
    if (ppuVar15 != (undefined **)0x0) {
      (**(code **)(*ppuVar15 + 0x40))();
    }
    FUN_1002786c0(plVar28);
  }
  else {
    plVar28 = (long *)0x0;
  }
  if (*(char *)(param_3 + 0x40) == '\x01') {
    uVar3 = *(undefined4 *)(param_3 + 0x3c);
    FUN_10017f084(&local_298);
    ppuVar15 = operator_new(0xf8);
    local_9e8[0] = local_298;
    local_6b8 = &PTR_FUN_101bcedd0;
    local_6a0 = &local_6b8;
    FUN_10017f52c(ppuVar15,local_9e8,uVar3,&local_6b8);
    if (local_6a0 == &local_6b8) {
      lVar26 = 0x20;
LAB_10017d124:
      (**(code **)((long)*local_6a0 + lVar26))();
    }
    else if (local_6a0 != (undefined ***)0x0) {
      lVar26 = 0x28;
      goto LAB_10017d124;
    }
    plVar20 = local_9e8[0];
    local_9e8[0] = (long *)0x0;
    if (plVar20 != (long *)0x0) {
      (**(code **)(*plVar20 + 8))();
    }
    local_a58 = ppuVar15;
  }
  else {
    FUN_10017f084(&local_6b8);
    ppuVar15 = (undefined **)0x0;
    local_a58 = local_6b8;
  }
  local_9d1 = '\x04';
  local_9e8[0] = (long *)CONCAT35(local_9e8[0]._5_3_,0x68737550);
  FUN_100182354(&local_6b8,&local_a58,local_9e8);
  if (local_9d1 < '\0') {
    operator_delete(local_9e8[0]);
  }
  ppuVar27 = local_a58;
  local_a58 = (undefined **)0x0;
  if (ppuVar27 != (undefined **)0x0) {
    (**(code **)(*ppuVar27 + 8))();
  }
  FUN_1001ce29c(&local_298);
  FUN_1001ce5b0(&local_100);
  thunk_FUN_1011959c8(local_9e8,&local_298,&local_100,local_4a8,param_3 + 0xc0);
  if (local_281 < '\0') {
    operator_delete(local_298);
  }
  FUN_1001cd358(&local_298);
  thunk_FUN_1013ff4a8(&uStack_a59,&local_298);
  if (local_298 != (long *)0x0) {
    for (; local_290 != local_298; local_290 = local_290 + -3) {
    }
    local_290 = local_298;
    operator_delete(local_298);
  }
  local_9ec = local_a50;
  local_9ed = 1;
  FUN_100225898(*(undefined4 *)(param_3 + 0x34),param_3 + 0x68);
  thunk_FUN_1001a56a8(auStack_9f8,param_3,local_4a8);
  local_a10 = (void *)0x0;
  uStack_a08 = 0;
  local_a00 = 0;
  local_2b8[0] = &PTR_FUN_101bcf530;
  local_2a0 = local_2b8;
  uVar16 = FUN_1001a6614(auStack_9f8);
  uVar17 = FUN_1001a65fc(auStack_9f8);
  uVar18 = FUN_1001a6608(auStack_9f8);
  uVar12 = local_9ec;
  local_2d8[0] = &PTR_FUN_101bcf5c0;
  local_2c0 = local_2d8;
  FUN_1002811a4(&local_a48);
  if (cStack_a31 < '\0') {
    FUN_10018127c(&local_a30,local_a48,uStack_a40);
  }
  else {
    uStack_a28 = uStack_a40;
    local_a30 = local_a48;
    local_a20 = CONCAT17(cStack_a31,local_a38);
  }
  uStack_f8 = (undefined6)uStack_a28;
  uStack_f2 = (undefined2)((ulong)uStack_a28 >> 0x30);
  local_100 = local_a30;
  acStack_f0 = SUB86(local_a20,0);
  uStack_ea = (undefined1)((ulong)local_a20 >> 0x30);
  uStack_e9 = (undefined1)((ulong)local_a20 >> 0x38);
  uStack_a28 = 0;
  local_a20 = 0;
  local_a30 = (undefined **)0x0;
  local_e8 = (undefined ***)CONCAT71(local_e8._1_7_,1);
  if (*(char *)(param_3 + 0x9f) < '\0') {
    FUN_10018127c(&local_a0,*(undefined8 *)(param_3 + 0x88),*(undefined8 *)(param_3 + 0x90));
  }
  else {
    pbStack_98 = *(byte **)(param_3 + 0x90);
    local_a0 = *(undefined ***)(param_3 + 0x88);
    local_90 = *(undefined8 *)(param_3 + 0x98);
  }
  local_88[0] = (undefined ***)CONCAT71(local_88[0]._1_7_,1);
  local_2f8 = &PTR_FUN_101bcf650;
  local_2f0 = &local_9ed;
  local_2e0 = &local_2f8;
  FUN_100230f2c(&local_298,&local_6b8,local_2b8,plVar28 + 1,uVar16,uVar17,uVar18,local_2d8,
                &local_a10,uVar12,&local_100,&local_a0,"Push2",&local_2f8,0);
  if (local_2e0 == &local_2f8) {
    lVar26 = 0x20;
LAB_10017d418:
    (**(code **)((long)*local_2e0 + lVar26))();
  }
  else if (local_2e0 != (undefined ***)0x0) {
    lVar26 = 0x28;
    goto LAB_10017d418;
  }
  if (local_a20 < 0) {
    operator_delete(local_a30);
    if (cStack_a31 < '\0') goto LAB_10017d498;
LAB_10017d46c:
    if (local_2c0 != local_2d8) goto LAB_10017d47c;
LAB_10017d4b0:
    lVar26 = 0x20;
LAB_10017d4b4:
    (**(code **)((long)*local_2c0 + lVar26))();
  }
  else {
    if (-1 < cStack_a31) goto LAB_10017d46c;
LAB_10017d498:
    operator_delete(local_a48);
    if (local_2c0 == local_2d8) goto LAB_10017d4b0;
LAB_10017d47c:
    if (local_2c0 != (undefined ***)0x0) {
      lVar26 = 0x28;
      goto LAB_10017d4b4;
    }
  }
  if (local_2a0 == local_2b8) {
    lVar26 = 0x20;
LAB_10017d4e0:
    (**(code **)((long)*local_2a0 + lVar26))();
  }
  else if (local_2a0 != (undefined ***)0x0) {
    lVar26 = 0x28;
    goto LAB_10017d4e0;
  }
  local_a30 = (undefined **)0x0;
  lVar19 = FUN_1001a6614(auStack_9f8);
  uVar4 = *(undefined1 *)(param_3 + 0x3a);
  plVar20 = operator_new(0x2a118);
  *plVar20 = (long)&local_298;
  plVar20[1] = 0;
  plVar20[2] = 0;
  plVar20[3] = 0;
  pbVar1 = (byte *)(plVar20 + 6);
  plVar20[4] = (long)&local_6b8;
  plVar20[5] = (long)local_9e8;
  thunk_FUN_100228794();
  thunk_FUN_100227d58(plVar20 + 0x37);
  FUN_10022d21c(plVar20 + 0x4b);
  thunk_FUN_10022af2c(plVar20 + 0x14b);
  thunk_FUN_10022af2c(plVar20 + 0xa5a);
  thunk_FUN_10022af2c(plVar20 + 0x1369);
  thunk_FUN_10022af2c(plVar20 + 0x1c78);
  thunk_FUN_10022af2c(plVar20 + 0x2587);
  thunk_FUN_10022af2c(plVar20 + 0x2e96);
  thunk_FUN_10022af2c(plVar20 + 0x37a5);
  thunk_FUN_10022af2c(plVar20 + 0x40b4);
  thunk_FUN_10022af2c(plVar20 + 0x49c3);
  plVar20[0x53d2] = 0;
  lVar24 = _UNK_1015703a8;
  lVar26 = _DAT_1015703a0;
  plVar20[0x53db] = _UNK_1015703a8;
  plVar20[0x53da] = lVar26;
  iVar13 = _posix_memalign(&local_100,0x40,0x8020);
  if ((iVar13 != 0) || (local_100 == (undefined **)0x0)) {
    std::bad_alloc::bad_alloc((bad_alloc *)&local_100);
    FUN_100184f8c();
    goto LAB_10017dfe8;
  }
  plVar20[0x53dc] = (long)local_100;
  plVar20[0x53dd] = DAT_1015703f0;
  *(undefined4 *)(plVar20 + 0x53de) = 2;
  lVar21 = std::chrono::steady_clock::now();
  plVar20[0x53df] = lVar21;
  lVar7 = _UNK_1015703b8;
  lVar21 = _DAT_1015703b0;
  plVar20[0x53e1] = _UNK_1015703b8;
  plVar20[0x53e0] = lVar21;
  lVar22 = std::chrono::steady_clock::now();
  plVar20[0x53e2] = lVar22;
  plVar20[0x53e4] = lVar7;
  plVar20[0x53e3] = lVar21;
  lVar22 = std::chrono::steady_clock::now();
  plVar20[0x53e5] = lVar22;
  plVar20[0x53e7] = lVar7;
  plVar20[0x53e6] = lVar21;
  thunk_FUN_100220998(plVar20 + 0x53e8);
  lVar22 = std::chrono::steady_clock::now();
  plVar20[0x53f4] = lVar22;
  plVar20[0x53f6] = lVar7;
  plVar20[0x53f5] = lVar21;
  *(undefined1 *)(plVar20 + 0x53f7) = 0;
  *(undefined4 *)((long)plVar20 + 0x29fbc) = 0;
  *(undefined1 *)(plVar20 + 0x53f8) = 0;
  auVar31 = FUN_1002867e0();
  if ((auVar31._8_8_ >> 0x20 & 1) == 0) {
    prVar25 = (runtime_error *)___cxa_allocate_exception(0x10);
    std::runtime_error::runtime_error(prVar25,"No Push hardware found");
                    /* WARNING: Subroutine does not return */
    ___cxa_throw(prVar25,PTR_typeinfo_101b8c318,PTR__runtime_error_101b8c1f0);
  }
  if (local_9ec != auVar31._0_4_) {
    uVar16 = std::chrono::system_clock::now();
    FUN_1003324b0(&local_100,3,uVar16);
    iVar13 = FUN_10032ece8(&local_100);
    if (iVar13 != 0) {
      FUN_10032bea8(&local_100,"Unexpected Push hardware type found");
    }
    thunk_FUN_10032ba14(&local_100);
  }
  uVar10 = s_Ableton_Internal_Input_101837720._16_6_;
  uVar9 = s_Ableton_Internal_Input_101837720._14_2_;
  uVar8 = s_Ableton_Internal_Input_101837720._8_6_;
  uVar16 = s_Ableton_Internal_Input_101837720._0_8_;
  acStack_f0[0] = s_Ableton_Internal_Input_101837720[0x10];
  acStack_f0[1] = s_Ableton_Internal_Input_101837720[0x11];
  acStack_f0[2] = s_Ableton_Internal_Input_101837720[0x12];
  acStack_f0[3] = s_Ableton_Internal_Input_101837720[0x13];
  acStack_f0[4] = s_Ableton_Internal_Input_101837720[0x14];
  acStack_f0[5] = s_Ableton_Internal_Input_101837720[0x15];
  uStack_f8._0_1_ = s_Ableton_Internal_Input_101837720[8];
  uStack_f8._1_1_ = s_Ableton_Internal_Input_101837720[9];
  uStack_f8._2_1_ = s_Ableton_Internal_Input_101837720[10];
  uStack_f8._3_1_ = s_Ableton_Internal_Input_101837720[0xb];
  uStack_f8._4_1_ = s_Ableton_Internal_Input_101837720[0xc];
  uStack_f8._5_1_ = s_Ableton_Internal_Input_101837720[0xd];
  uStack_f2._0_1_ = s_Ableton_Internal_Input_101837720[0xe];
  uStack_f2._1_1_ = s_Ableton_Internal_Input_101837720[0xf];
  local_100 = (undefined **)s_Ableton_Internal_Input_101837720._0_8_;
  uStack_ea = 0;
  uStack_e9 = 0x16;
  plVar20[0x53f9] = 0;
  plVar20[0x53fa] = (long)&PTR_FUN_101bcf6d0;
  plVar20[0x53fb] = (long)pbVar1;
  plVar20[0x53fd] = (long)(plVar20 + 0x53fa);
  *(undefined4 *)(plVar20 + 0x53fe) = 1;
  *(undefined1 *)((long)plVar20 + 0x29ff4) = 1;
  plVar20[0x5400] = CONCAT26(uVar9,uVar8);
  plVar20[0x53ff] = uVar16;
  plVar20[0x5401] = CONCAT17(0x16,(uint7)(uint6)uVar10);
  FUN_1001cb69c(plVar20 + 0x53f9,auVar31._0_8_ >> 0x20,&local_100,1);
  FUN_10017eabc(plVar20 + 0x5402,&local_9ec);
  local_a0 = &PTR_FUN_101bcfdc0;
  local_88[0] = &local_a0;
  local_100 = &PTR_FUN_101bcfdc0;
  uStack_f8 = SUB86(pbVar1,0);
  uStack_f2 = (undefined2)((ulong)pbVar1 >> 0x30);
  local_e8 = &local_100;
  pbStack_98 = pbVar1;
  FUN_1002284a4(plVar20 + 0x5406,&local_100);
  if (local_e8 == &local_100) {
    lVar21 = 0x20;
LAB_10017d7c8:
    (**(code **)((long)*local_e8 + lVar21))();
  }
  else if (local_e8 != (undefined ***)0x0) {
    lVar21 = 0x28;
    goto LAB_10017d7c8;
  }
  if (local_88[0] == &local_a0) {
    lVar21 = 0x20;
LAB_10017d7f4:
    (**(code **)((long)*local_88[0] + lVar21))();
  }
  else if (local_88[0] != (undefined ***)0x0) {
    lVar21 = 0x28;
    goto LAB_10017d7f4;
  }
  *(undefined2 *)(plVar20 + 0x540c) = 0;
  plVar20[0x540d] = 0;
  plVar20[0x5416] = lVar24;
  plVar20[0x5415] = lVar26;
  iVar13 = _posix_memalign(&local_100,0x40,0x8020);
  if ((iVar13 != 0) || (local_100 == (undefined **)0x0)) {
    std::bad_alloc::bad_alloc((bad_alloc *)&local_100);
    FUN_100184f8c();
LAB_10017dfe8:
                    /* WARNING: Does not return */
    pcVar11 = (code *)SoftwareBreakpoint(1,0x10017dfec);
    (*pcVar11)();
  }
  plVar20[0x5417] = (long)local_100;
  plVar20[0x5418] = (long)&local_9ec;
  *(undefined1 *)(plVar20 + 0x5419) = 0;
  *(undefined1 *)(plVar20 + 0x541a) = 0;
  _bzero(plVar20 + 0x52d2,0x800);
  FUN_100228524(plVar20 + 0x5406);
  lVar26 = FUN_10078a33c(&local_6b8);
  plVar20[0x541b] = (long)&PTR_thunk_FUN_10018d57c_101bd0170;
  plVar20[0x541c] = lVar26;
  plVar20[0x541d] = (long)&PTR_FUN_101bd01c0;
  plVar20[0x541e] = (long)plVar20;
  plVar20[0x5420] = (long)(plVar20 + 0x541d);
  iVar13 = FUN_100a06bdc();
  if (iVar13 != 0) {
    FUN_10030513c("false","modules/flip/include/flip/DocumentObserverDynamic.hpp",0x2e);
LAB_10017dfa8:
                    /* WARNING: Subroutine does not return */
    _abort();
  }
  iVar13 = FUN_100a1965c(*(undefined8 *)(plVar20[0x541c] + 0xb0));
  if (iVar13 != 0) {
    FUN_10030513c("false","modules/flip/include/flip/DocumentObserverDynamic.hpp",0x31);
    goto LAB_10017dfa8;
  }
  FUN_100a0805c(&local_100,plVar20[0x541c],2);
  FUN_1009ed87c(plVar20[0x541c],plVar20 + 0x541b);
  FUN_100a08080(&local_100);
  plVar20[0x5421] = lVar19;
  *(undefined1 *)(plVar20 + 0x5422) = uVar4;
  *(undefined2 *)((long)plVar20 + 0x2a111) = 0;
  FUN_1002313d8(&local_298);
  FUN_1007259b8(local_4a8 + 0x4c30,0);
  FUN_10078a3b4(&local_100,plVar20[4]);
  local_100 = &PTR_FUN_101bd0430;
  if (local_b8 != (long *)0x0) {
    LOAcquire();
    lVar26 = local_b8[1];
    local_b8[1] = lVar26 + -1;
    LORelease();
    if (lVar26 == 0) {
      (**(code **)(*local_b8 + 0x10))(local_b8);
      std::__shared_weak_count::__release_weak();
    }
  }
  FUN_10018d504(auStack_d8,local_d0);
  FUN_10078a7f8(plVar20[4]);
  FUN_100a1aab0(plVar20[4] + 0x218);
  local_a48 = (undefined **)0x0;
  FUN_10018d6dc(&local_a30,plVar20);
  FUN_10018d6dc(&local_a48,0);
  local_100 = &PTR_FUN_101bd0460;
  uStack_f8 = SUB86(&local_a30,0);
  uStack_f2 = (undefined2)((ulong)&local_a30 >> 0x30);
  local_e8 = &local_100;
  FUN_1002787b0(plVar28,&local_100);
  if (local_e8 == &local_100) {
    lVar26 = 0x20;
LAB_10017d9d0:
    (**(code **)((long)*local_e8 + lVar26))();
  }
  else if (local_e8 != (undefined ***)0x0) {
    lVar26 = 0x28;
    goto LAB_10017d9d0;
  }
  if (ppuVar15 != (undefined **)0x0) {
    local_88[0] = &local_a0;
    ppuVar27 = &PTR_FUN_101bd04e0;
    pbStack_98 = &local_9ed;
    local_a0 = &PTR_FUN_101bd04e0;
    ppppuVar30 = (undefined ****)(ppuVar15 + 0x1b);
    pppuVar23 = *ppppuVar30;
    pppuVar29 = (undefined ***)(ppuVar15 + 0x18);
    *ppppuVar30 = (undefined ***)0x0;
    if (pppuVar23 == pppuVar29) {
      (*(code *)(*pppuVar23)[4])();
joined_r0x00010017da44:
      if (local_88[0] != (undefined ***)0x0) {
        if (local_88[0] == &local_a0) {
          ppuVar27 = *local_88[0];
          goto LAB_10017da70;
        }
        *ppppuVar30 = local_88[0];
        ppppuVar30 = local_88;
      }
      *ppppuVar30 = (undefined ***)0x0;
    }
    else {
      if (pppuVar23 != (undefined ***)0x0) {
        (*(code *)(*pppuVar23)[5])();
        goto joined_r0x00010017da44;
      }
LAB_10017da70:
      *ppppuVar30 = pppuVar29;
      (*(code *)ppuVar27[3])(local_88[0],pppuVar29);
    }
    if (local_88[0] == &local_a0) {
      lVar26 = 0x20;
    }
    else {
      if (local_88[0] == (undefined ***)0x0) goto LAB_10017daac;
      lVar26 = 0x28;
    }
    (**(code **)((long)*local_88[0] + lVar26))();
  }
LAB_10017daac:
  uVar16 = std::chrono::system_clock::now();
  FUN_1003324b0(&local_a48,2,uVar16);
  iVar13 = FUN_10032ece8(&local_a48);
  if (iVar13 != 0) {
    FUN_10032bea8(&local_a48,"Starting the main loop");
  }
  thunk_FUN_10032ba14(&local_a48);
  cVar5 = *(char *)(param_3 + 0x44);
  bVar6 = *(byte *)(param_3 + 0x45);
  FUN_100278798(plVar28);
  lVar26 = std::chrono::steady_clock::now();
  if (local_9ed == 1) {
    do {
      iVar13 = FUN_100278158(plVar28,500000);
      if ((((*(byte *)((long)plVar28 + 0x17c) & 1) != 0) && (cVar5 != '\0')) && ((bVar6 & 1) != 0))
      {
        local_9ed = 0;
        break;
      }
      lVar24 = std::chrono::steady_clock::now();
      lVar26 = (lVar24 - lVar26) / 1000;
      if ((ppuVar15 != (undefined **)0x0) &&
         (iVar14 = (**(code **)(*(long *)ppuVar15[0x1c] + 0x10))(), iVar14 != 0)) {
        puVar2 = ppuVar15[0x1d] + lVar26;
        ppuVar15[0x1d] = puVar2;
        if (499999 < (long)puVar2) {
          ppuVar15[0x1d] = (undefined *)((ulong)puVar2 % 500000);
          FUN_100668408(ppuVar15 + 1);
          FUN_100668374(ppuVar15 + 1,500);
        }
      }
      FUN_1001828a4(local_a30,lVar26,0);
      FUN_1013f7ee8(&local_a10);
      if (iVar13 != 0) {
        uVar16 = FUN_101198ddc(local_9e8);
        FUN_100278184(plVar28,uVar16);
      }
      lVar26 = lVar24;
    } while ((local_9ed & 1) != 0);
  }
  uVar16 = std::chrono::system_clock::now();
  FUN_1003324b0(&local_a48,2,uVar16);
  iVar13 = FUN_10032ece8(&local_a48);
  if (iVar13 != 0) {
    FUN_10032bea8(&local_a48,"Preparing to quit");
  }
  thunk_FUN_10032ba14(&local_a48);
  FUN_100276d1c(plVar28);
  FUN_100232028(&local_298);
  FUN_1001828a4(local_a30,0,1);
  FUN_10018d6dc(&local_a30,0);
  thunk_FUN_100230f70(&local_298);
  if (local_a00 < 0) {
    operator_delete(local_a10);
  }
  FUN_1001a65c0(auStack_9f8);
  FUN_1013ffc18(&uStack_a59);
  thunk_FUN_101195e58(local_9e8);
  local_4a0[0] = &PTR_FUN_101c3c3d8;
  if ((local_328 == '\x01') && (local_329 < '\0')) {
    operator_delete(local_340);
  }
  plVar20 = local_370;
  local_370 = (long *)0x0;
  if (plVar20 != (long *)0x0) {
    (**(code **)(*plVar20 + 8))();
  }
  if (local_388 != (void *)0x0) {
    local_380 = local_388;
    operator_delete(local_388);
  }
  local_3f0 = &PTR_FUN_101bcf460;
  if (local_398 == alStack_3b0) {
    lVar26 = 0x20;
LAB_10017ddbc:
    (**(code **)(*local_398 + lVar26))();
  }
  else if (local_398 != (long *)0x0) {
    lVar26 = 0x28;
    goto LAB_10017ddbc;
  }
  if (local_3b8 == alStack_3d0) {
    lVar26 = 0x20;
LAB_10017ddec:
    (**(code **)(*local_3b8 + lVar26))();
  }
  else if (local_3b8 != (long *)0x0) {
    lVar26 = 0x28;
    goto LAB_10017ddec;
  }
  if (local_3e8 != (void *)0x0) {
    local_3e0 = local_3e8;
    operator_delete(local_3e8);
  }
  if (local_418 != (void *)0x0) {
    local_410 = local_418;
    operator_delete(local_418);
  }
  if (local_430 != (void *)0x0) {
    local_428 = local_430;
    operator_delete(local_430);
  }
  if (local_448 != (void *)0x0) {
    local_440 = local_448;
    operator_delete(local_448);
  }
  FUN_1009ffd24(local_4a0);
  local_6b8 = &PTR_FUN_101bcf430;
  if (local_4c0 != (void *)0x0) {
    local_4b8 = local_4c0;
    operator_delete(local_4c0);
  }
  thunk_FUN_1009ed588(auStack_680);
  FUN_10018253c(auStack_6a8,local_6a0);
  if (plVar28 != (long *)0x0) {
    (**(code **)(*plVar28 + 0x10))(plVar28);
  }
  if (local_300 == 1) {
    if (local_308 == (long *)0x0) {
                    /* WARNING: Subroutine does not return */
      FUN_10018001c();
    }
    (**(code **)(*local_308 + 0x30))();
    if ((local_300 & 1) != 0) {
      if (local_308 == alStack_320) {
        lVar26 = 0x20;
      }
      else {
        if (local_308 == (long *)0x0) goto LAB_10017dee4;
        lVar26 = 0x28;
      }
      (**(code **)(*local_308 + lVar26))();
    }
  }
LAB_10017dee4:
  if (*(long *)PTR____stack_chk_guard_101b8c408 == local_78) {
    return 0;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

