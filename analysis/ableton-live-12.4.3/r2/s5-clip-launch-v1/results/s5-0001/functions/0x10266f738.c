
long FUN_10266f738(long param_1)

{
  void *pvVar1;
  void *pvVar2;
  ulong uVar3;
  undefined *puVar4;
  code *pcVar5;
  int iVar6;
  undefined8 *puVar7;
  undefined8 uVar8;
  long lVar9;
  undefined8 uVar10;
  long *plVar11;
  undefined4 local_14c;
  undefined4 local_148;
  undefined4 uStack_144;
  int *local_140;
  int *local_138;
  void *local_130;
  void *local_128;
  void *local_120;
  void *local_118;
  void *local_110;
  void *local_108;
  undefined **local_100 [3];
  undefined ***local_e8;
  undefined **local_e0;
  long lStack_d8;
  undefined1 auStack_d0 [8];
  undefined ***local_c8;
  undefined1 auStack_c0 [8];
  undefined1 auStack_b8 [8];
  undefined1 auStack_b0 [8];
  undefined1 auStack_a8 [8];
  undefined1 auStack_a0 [8];
  undefined1 auStack_98 [8];
  undefined1 auStack_90 [8];
  undefined1 auStack_88 [8];
  undefined1 auStack_80 [8];
  undefined1 auStack_78 [8];
  long local_70;
  
  local_70 = *(long *)PTR____stack_chk_guard_1064f8818;
  puVar7 = (undefined8 *)FUN_10153fbbc();
  *puVar7 = &PTR_FUN_1067f24f0;
  puVar7[10] = &PTR_FUN_1067f2960;
  puVar7[0xb] = &PTR_FUN_1067f2978;
  puVar7[0x33] = &PTR_FUN_1067f29e8;
  puVar7[0x34] = &PTR_FUN_1067f2a48;
  puVar7[0x35] = 0;
  puVar7[0x36] = 0;
  FUN_10242650c(&local_e0);
  FUN_10150b1cc(param_1 + 0x1b8,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x1b8) = &PTR_thunk_FUN_10150b2b4_1067b7ad0;
  FUN_1015643d8(&local_e0);
  FUN_10150b1cc(param_1 + 0x1d0,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x1d0) = &PTR_thunk_FUN_10150b2b4_10658fdd8;
  FUN_10156915c(&local_e0);
  FUN_10150b1cc(param_1 + 0x1e8,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x1e8) = &PTR_thunk_FUN_10150b2b4_10658fd48;
  FUN_1025ce7c0(&local_e0);
  FUN_10150b1cc(param_1 + 0x200,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x200) = &PTR_thunk_FUN_10150b2b4_1067f4a68;
  FUN_10156b17c(&local_e0);
  FUN_10150b1cc(param_1 + 0x218,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x218) = &PTR_thunk_FUN_10150b2b4_106595dc8;
  FUN_102662cfc(&local_e0);
  FUN_10150b1cc(param_1 + 0x230,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x230) = &PTR_thunk_FUN_10150b2b4_1067f4af8;
  FUN_1026df1c4(&local_e0);
  FUN_10150b1cc(param_1 + 0x248,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x248) = &PTR_thunk_FUN_10150b2b4_1067b7f50;
  FUN_1025766cc(&local_e0);
  FUN_10150b1cc(param_1 + 0x260,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x260) = &PTR_thunk_FUN_10150b2b4_1067f4b88;
  FUN_10156b17c(&local_e0);
  FUN_10150b1cc(param_1 + 0x278,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x278) = &PTR_thunk_FUN_10150b2b4_106595dc8;
  FUN_102760d30(&local_e0);
  FUN_10150b1cc(param_1 + 0x290,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x290) = &PTR_thunk_FUN_10150b2b4_1067f4c18;
  FUN_102640760(&local_e0);
  FUN_10150b1cc(param_1 + 0x2a8,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x2a8) = &PTR_thunk_FUN_10150b2b4_1067b80c0;
  FUN_1015643d8(&local_e0);
  FUN_10150b1cc(param_1 + 0x2c0,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x2c0) = &PTR_thunk_FUN_10150b2b4_10658fdd8;
  FUN_1015643d8(&local_e0);
  FUN_10150b1cc(param_1 + 0x2d8,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x2d8) = &PTR_thunk_FUN_10150b2b4_10658fdd8;
  FUN_1015686ac(&local_e0);
  FUN_10150b1cc(param_1 + 0x2f0,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x2f0) = &PTR_thunk_FUN_10150b2b4_1065a39c8;
  FUN_10156ea7c(&local_e0);
  FUN_10150b1cc(param_1 + 0x308,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x308) = &PTR_thunk_FUN_10150b2b4_106747050;
  FUN_101565f54(&local_e0);
  FUN_10150b1cc(param_1 + 800,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 800) = &PTR_thunk_FUN_10150b2b4_1065925e0;
  FUN_1015643d8(&local_e0);
  FUN_10150b1cc(param_1 + 0x338,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x338) = &PTR_thunk_FUN_10150b2b4_10658fdd8;
  FUN_101563fa0(&local_e0);
  FUN_10150b1cc(param_1 + 0x350,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x350) = &PTR_thunk_FUN_10150b2b4_106592670;
  FUN_1015686ac(&local_e0);
  FUN_10150b1cc(param_1 + 0x368,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x368) = &PTR_thunk_FUN_10150b2b4_1065a39c8;
  FUN_101565f54(&local_e0);
  FUN_10150b1cc(param_1 + 0x380,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x380) = &PTR_thunk_FUN_10150b2b4_1065925e0;
  FUN_10260a70c(&local_e0);
  FUN_10150b1cc(param_1 + 0x398,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x398) = &PTR_thunk_FUN_10150b2b4_1067bd7a8;
  *(undefined8 *)(param_1 + 0x3b0) = 0;
  FUN_101565f54(&local_e0);
  FUN_10150b1cc(param_1 + 0x3b8,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x3b8) = &PTR_thunk_FUN_10150b2b4_1065925e0;
  FUN_102472bac(&local_e0);
  FUN_10150b1cc(param_1 + 0x3d0,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x3d0) = &PTR_thunk_FUN_10150b2b4_1067f4ca8;
  FUN_102478ce8(&local_e0);
  FUN_10150b1cc(param_1 + 1000,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 1000) = &PTR_thunk_FUN_10150b2b4_1067f4d38;
  FUN_1015643d8(&local_e0);
  FUN_10150b1cc(param_1 + 0x400,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x400) = &PTR_thunk_FUN_10150b2b4_10658fdd8;
  FUN_10156915c(&local_e0);
  FUN_10150b1cc(param_1 + 0x418,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x418) = &PTR_thunk_FUN_10150b2b4_10658fd48;
  FUN_1015643d8(&local_e0);
  FUN_10150b1cc(param_1 + 0x430,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x430) = &PTR_thunk_FUN_10150b2b4_10658fdd8;
  FUN_10156915c(&local_e0);
  FUN_10150b1cc(param_1 + 0x448,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x448) = &PTR_thunk_FUN_10150b2b4_10658fd48;
  FUN_10156b17c(&local_e0);
  FUN_10150b1cc(param_1 + 0x460,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x460) = &PTR_thunk_FUN_10150b2b4_106595dc8;
  FUN_10156b17c(&local_e0);
  FUN_10150b1cc(param_1 + 0x478,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x478) = &PTR_thunk_FUN_10150b2b4_106595dc8;
  FUN_10156915c(&local_e0);
  FUN_10150b1cc(param_1 + 0x490,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x490) = &PTR_thunk_FUN_10150b2b4_10658fd48;
  FUN_10156915c(&local_e0);
  FUN_10150b1cc(param_1 + 0x4a8,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x4a8) = &PTR_thunk_FUN_10150b2b4_10658fd48;
  FUN_10156915c(&local_e0);
  FUN_10150b1cc(param_1 + 0x4c0,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x4c0) = &PTR_thunk_FUN_10150b2b4_10658fd48;
  FUN_1015643d8(&local_e0);
  FUN_10150b1cc(param_1 + 0x4d8,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x4d8) = &PTR_thunk_FUN_10150b2b4_10658fdd8;
  FUN_1015740f0(&local_e0);
  FUN_10150b1cc(param_1 + 0x4f0,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x4f0) = &PTR_thunk_FUN_10150b2b4_106590220;
  FUN_10260a70c(&local_e0);
  FUN_10150b1cc(param_1 + 0x508,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x508) = &PTR_thunk_FUN_10150b2b4_1067bd7a8;
  *(undefined8 *)(param_1 + 0x520) = 0;
  FUN_1015643d8(&local_e0);
  FUN_10150b1cc(param_1 + 0x528,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x528) = &PTR_thunk_FUN_10150b2b4_10658fdd8;
  FUN_10260a70c(&local_e0);
  FUN_10150b1cc(param_1 + 0x540,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x540) = &PTR_thunk_FUN_10150b2b4_1067bd7a8;
  *(undefined8 *)(param_1 + 0x558) = 0;
  FUN_10260a70c(&local_e0);
  FUN_10150b1cc(param_1 + 0x560,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x560) = &PTR_thunk_FUN_10150b2b4_1067bd7a8;
  *(undefined8 *)(param_1 + 0x578) = 0;
  FUN_1025eb980(&local_e0);
  FUN_10150b1cc(param_1 + 0x580,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x580) = &PTR_thunk_FUN_10150b2b4_1067acd70;
  FUN_1025eb980(&local_e0);
  FUN_10150b1cc(param_1 + 0x598,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x598) = &PTR_thunk_FUN_10150b2b4_1067acd70;
  FUN_1025eb980(&local_e0);
  FUN_10150b1cc(param_1 + 0x5b0,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x5b0) = &PTR_thunk_FUN_10150b2b4_1067acd70;
  FUN_1025eb980(&local_e0);
  FUN_10150b1cc(param_1 + 0x5c8,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x5c8) = &PTR_thunk_FUN_10150b2b4_1067acd70;
  FUN_1025eb980(&local_e0);
  FUN_10150b1cc(param_1 + 0x5e0,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x5e0) = &PTR_thunk_FUN_10150b2b4_1067acd70;
  *(undefined8 *)(param_1 + 0x5f8) = 0;
  puVar7 = (undefined8 *)FUN_1012d9850(0x28);
  FUN_10128ed98();
  puVar7[3] = param_1;
  puVar7[4] = param_1 + 0x5f8;
  *puVar7 = &PTR_thunk_FUN_10128edf8_1067f49c8;
  *(undefined8 **)(param_1 + 0x600) = puVar7;
  *(int *)(puVar7 + 1) = *(int *)(puVar7 + 1) + 1;
  puVar7 = (undefined8 *)FUN_1012d9850(0x28);
  FUN_10128ed98();
  puVar7[3] = param_1;
  puVar7[4] = param_1 + 0x5fc;
  *puVar7 = &PTR_thunk_FUN_10128edf8_1067f4a18;
  *(undefined8 **)(param_1 + 0x608) = puVar7;
  *(int *)(puVar7 + 1) = *(int *)(puVar7 + 1) + 1;
  FUN_10156b17c(&local_e0);
  FUN_10150b1cc(param_1 + 0x610,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x610) = &PTR_thunk_FUN_10150b2b4_106595dc8;
  FUN_10156b17c(&local_e0);
  FUN_10150b1cc(param_1 + 0x628,local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)(local_e0 + 1);
    *(int *)(local_e0 + 1) = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x628) = &PTR_thunk_FUN_10150b2b4_106595dc8;
  *(undefined ***)(param_1 + 0x640) = &PTR_FUN_1066026a8;
  *(undefined8 *)(param_1 + 0x668) = 0;
  *(undefined8 *)(param_1 + 0x650) = 0;
  *(undefined8 *)(param_1 + 0x648) = 0;
  *(undefined8 *)(param_1 + 0x660) = 0;
  *(undefined8 *)(param_1 + 0x658) = 0;
  uVar8 = FUN_1012d9850(0xb30);
  FUN_102672448(uVar8,param_1);
  *(undefined **)(param_1 + 0x1a8) = PTR_Delete_106537100;
  *(undefined8 *)(param_1 + 0x1b0) = uVar8;
  FUN_101486414(param_1);
  FUN_102767780(*(undefined8 *)(param_1 + 0x298),param_1);
  puVar4 = PTR__lambda___1__ARemoteable__TRemoteableUpdate__106551c78;
  local_e0 = (undefined **)PTR__lambda___1__ARemoteable__TRemoteableUpdate__106551c78;
  lStack_d8 = 0;
  FUN_101564728(*(undefined8 *)(param_1 + 0x438),1,&local_e0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x438),1);
  local_e0 = (undefined **)puVar4;
  lStack_d8 = 0;
  FUN_10156934c(*(undefined8 *)(param_1 + 0x450),0,&local_e0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x450),1);
  local_e0 = (undefined **)puVar4;
  lStack_d8 = 0;
  FUN_101564728(*(undefined8 *)(param_1 + 0x408),1,&local_e0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x408),1);
  local_e0 = (undefined **)puVar4;
  lStack_d8 = 0;
  FUN_10156934c(*(undefined8 *)(param_1 + 0x420),0,&local_e0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x420),1);
  (**(code **)(**(long **)(param_1 + 0x3d8) + 400))(*(long **)(param_1 + 0x3d8),param_1);
  local_e0 = (undefined **)puVar4;
  lStack_d8 = 0;
  FUN_10156934c(*(undefined8 *)(param_1 + 0x498),4,&local_e0);
  local_e0 = (undefined **)puVar4;
  lStack_d8 = 0;
  FUN_10156934c(*(undefined8 *)(param_1 + 0x4b0),0x78,&local_e0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x4b0),1);
  local_e0 = (undefined **)puVar4;
  lStack_d8 = 0;
  FUN_10156934c(*(undefined8 *)(param_1 + 0x4c8),0x78,&local_e0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x4c8),1);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x358),1);
  local_e0 = (undefined **)puVar4;
  lStack_d8 = 0;
  FUN_10156934c(*(undefined8 *)(param_1 + 0x1f0),0xac44,&local_e0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x1f0),1);
  uVar10 = *(undefined8 *)(param_1 + 0x618);
  uVar8 = FUN_102704388();
  local_e0 = (undefined **)PTR_CallMemberFunc<&ASong::OnUpdateTracks>_106534b10;
  lStack_d8 = param_1;
  FUN_10156da84(uVar10,uVar8,&local_e0);
  lStack_d8 = *(long *)(param_1 + 0x1b0);
  local_e0 = (undefined **)PTR_CallMemberFunc<&LSong::TrackAddController>_106534d30;
  FUN_10156db2c(*(undefined8 *)(param_1 + 0x618),&local_e0);
  lStack_d8 = *(long *)(param_1 + 0x1b0);
  local_e0 = (undefined **)PTR_CallMemberFunc<&LSong::TrackRemoveController>_106534d40;
  FUN_10156db3c(*(undefined8 *)(param_1 + 0x618),&local_e0);
  uVar10 = *(undefined8 *)(param_1 + 0x630);
  uVar8 = FUN_1026660a0();
  local_e0 = (undefined **)PTR__lambda___1__ACompound__int_TListNotifierType__106551db8;
  lStack_d8 = 0;
  FUN_10156da84(uVar10,uVar8,&local_e0);
  lStack_d8 = *(long *)(param_1 + 0x1b0);
  local_e0 = (undefined **)PTR_CallMemberFunc<&LSong::SceneAddController>_106534d28;
  FUN_10156db2c(*(undefined8 *)(param_1 + 0x280),&local_e0);
  lStack_d8 = *(long *)(param_1 + 0x1b0);
  local_e0 = (undefined **)PTR_CallMemberFunc<&LSong::SceneRemoveController>_106534d38;
  FUN_10156db3c(*(undefined8 *)(param_1 + 0x280),&local_e0);
  uVar10 = *(undefined8 *)(param_1 + 0x220);
  uVar8 = FUN_10147e8b4(&DAT_106e504e8);
  local_e0 = (undefined **)PTR_CallMemberFunc<&ASong::OnUpdateSendsPre>_106534b18;
  lStack_d8 = param_1;
  FUN_10156da84(uVar10,uVar8,&local_e0);
  uVar10 = *(undefined8 *)(param_1 + 0x280);
  uVar8 = FUN_102642524();
  local_e0 = (undefined **)PTR_CallMemberFunc<&ASong::OnUpdateScene>_106534b08;
  lStack_d8 = param_1;
  FUN_10156da84(uVar10,uVar8,&local_e0);
  uVar8 = *(undefined8 *)(param_1 + 0x468);
  puVar7 = (undefined8 *)FUN_102587e34();
  local_118 = (void *)0x0;
  local_110 = (void *)0x0;
  local_108 = (void *)0x0;
  pvVar2 = (void *)*puVar7;
  uVar3 = puVar7[1] - (long)pvVar2;
  if (uVar3 != 0) {
    if ((long)uVar3 < 0) {
      FUN_10259163c(&local_118);
      goto LAB_1026711a8;
    }
    local_118 = operator_new(uVar3);
    pvVar1 = (void *)((long)local_118 + uVar3);
    local_110 = local_118;
    local_108 = pvVar1;
    _memcpy(local_118,pvVar2,uVar3);
    local_110 = pvVar1;
  }
  FUN_102671d44(uVar8,2,&local_118);
  if (local_118 != (void *)0x0) {
    local_110 = local_118;
    operator_delete(local_118);
  }
  uVar8 = *(undefined8 *)(param_1 + 0x480);
  puVar7 = (undefined8 *)FUN_102587cbc();
  local_130 = (void *)0x0;
  local_128 = (void *)0x0;
  local_120 = (void *)0x0;
  pvVar2 = (void *)*puVar7;
  uVar3 = puVar7[1] - (long)pvVar2;
  if (uVar3 != 0) {
    if ((long)uVar3 < 0) {
      FUN_10259163c(&local_130);
LAB_1026711a8:
                    /* WARNING: Does not return */
      pcVar5 = (code *)SoftwareBreakpoint(1,0x1026711ac);
      (*pcVar5)();
    }
    local_130 = operator_new(uVar3);
    pvVar1 = (void *)((long)local_130 + uVar3);
    local_128 = local_130;
    local_120 = pvVar1;
    _memcpy(local_130,pvVar2,uVar3);
    local_128 = pvVar1;
  }
  FUN_102671d44(uVar8,0,&local_130);
  if (local_130 != (void *)0x0) {
    local_128 = local_130;
    operator_delete(local_130);
  }
  if (((DAT_10700c498 & 1) == 0) && (iVar6 = ___cxa_guard_acquire(&DAT_10700c498), iVar6 != 0)) {
    FUN_101427680(&local_e0,"SMPTE Off");
    FUN_101427680("SMPTE 24 fps");
    FUN_101427680("SMPTE 25 fps");
    FUN_101427680(&local_c8,"SMPTE 30 fps (No Drop)");
    FUN_101427680(auStack_c0,"SMPTE 30 fps (Drop Frame)");
    FUN_101427680(auStack_b8,"SMPTE 29.77 fps (No Drop)");
    FUN_1002c29cc(&DAT_10700c728,&local_e0,6);
    FUN_100234444(auStack_b8);
    FUN_100234444(auStack_c0);
    FUN_100234444(&local_c8);
    FUN_100234444(auStack_d0);
    FUN_100234444(&lStack_d8);
    FUN_100234444(&local_e0);
    ___cxa_atexit(FUN_1002343c8,&DAT_10700c728,0x100000000);
    ___cxa_guard_release(&DAT_10700c498);
  }
  local_e0 = (undefined **)puVar4;
  lStack_d8 = 0;
  FUN_101567bfc(*(undefined8 *)(param_1 + 0x328),0,&DAT_10700c728,0,&local_e0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x328),1);
  if (((DAT_10700c4a0 & 1) == 0) && (iVar6 = ___cxa_guard_acquire(&DAT_10700c4a0), iVar6 != 0)) {
    FUN_101427680(&local_e0,"None");
    FUN_101427680("8 Bars");
    FUN_101427680("4 Bars");
    FUN_101427680("2 Bars");
    FUN_101427680("1 Bar");
    FUN_101427680("1/2");
    FUN_101427680("1/2T");
    FUN_101427680("1/4");
    FUN_101427680("1/4T");
    FUN_101427680("1/8");
    FUN_101427680("1/8T");
    FUN_101427680(auStack_88,"1/16");
    FUN_101427680(auStack_80,"1/16T");
    FUN_101427680(auStack_78,"1/32");
    FUN_1002c29cc(&DAT_10700c740,&local_e0,0xe);
    FUN_100234444(auStack_78);
    FUN_100234444(auStack_80);
    FUN_100234444(auStack_88);
    FUN_100234444(auStack_90);
    FUN_100234444(auStack_98);
    FUN_100234444(auStack_a0);
    FUN_100234444(auStack_a8);
    FUN_100234444(auStack_b0);
    FUN_100234444(auStack_b8);
    FUN_100234444(auStack_c0);
    FUN_100234444(&local_c8);
    FUN_100234444(auStack_d0);
    FUN_100234444(&lStack_d8);
    FUN_100234444(&local_e0);
    ___cxa_atexit(FUN_1002343c8,&DAT_10700c740,0x100000000);
    ___cxa_guard_release(&DAT_10700c4a0);
  }
  plVar11 = *(long **)(param_1 + 0x370);
  FUN_101427680(&local_e0,"SwingAmount");
  (**(code **)(*plVar11 + 0x1c8))(plVar11,&local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)local_e0;
    *(int *)local_e0 = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_101449efc();
    }
  }
  local_e0 = (undefined **)puVar4;
  lStack_d8 = 0;
  FUN_101568960(0,*(undefined8 *)(param_1 + 0x370),&local_e0);
  plVar11 = *(long **)(param_1 + 0x388);
  FUN_101427680(&local_e0,"Global Quantization");
  (**(code **)(*plVar11 + 0x1c8))(plVar11,&local_e0);
  if (local_e0 != (undefined **)0x0) {
    iVar6 = *(int *)local_e0;
    *(int *)local_e0 = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_101449efc();
    }
  }
  local_e0 = (undefined **)puVar4;
  lStack_d8 = 0;
  FUN_101567bfc(*(undefined8 *)(param_1 + 0x388),4,&DAT_10700c740,0,&local_e0);
  FUN_101427680(&local_138,"Transport");
  FUN_101427680(&local_140,"Quantization");
  local_148 = 0;
  uStack_144 = 0x2711;
  local_14c = 1000;
  FUN_10248c0b4(&local_e0,&local_138,&local_140,&uStack_144,&local_148,&local_14c);
  lVar9 = *(long *)(param_1 + 0x3b0);
  if (lVar9 != 0) {
    iVar6 = *(int *)(lVar9 + 8) + -1;
    *(int *)(lVar9 + 8) = iVar6;
    if (iVar6 == 0) {
      FUN_10128eea0();
    }
  }
  *(long *)(param_1 + 0x3b0) = (long)local_e0;
  local_e0 = (undefined **)0x0;
  if (local_140 != (int *)0x0) {
    iVar6 = *local_140;
    *local_140 = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_138 != (int *)0x0) {
    iVar6 = *local_138;
    *local_138 = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_101449efc();
    }
  }
  lVar9 = 0;
  if (*(long *)(param_1 + 0x3b0) != 0) {
    lVar9 = *(long *)(param_1 + 0x3b0) + 0x18;
  }
  FUN_10260aa38(*(undefined8 *)(param_1 + 0x3a0),lVar9,0);
  FUN_101427680(&local_138,"Arrangement");
  FUN_101427680(&local_140,"Lock Envelopes");
  local_148 = 0;
  uStack_144 = 0x2715;
  local_14c = 0x272b;
  FUN_102671e38(&local_e0,&local_138,&local_140,&uStack_144,&local_148,&local_14c);
  lVar9 = *(long *)(param_1 + 0x578);
  if (lVar9 != 0) {
    iVar6 = *(int *)(lVar9 + 8) + -1;
    *(int *)(lVar9 + 8) = iVar6;
    if (iVar6 == 0) {
      FUN_10128eea0();
    }
  }
  *(long *)(param_1 + 0x578) = (long)local_e0;
  local_e0 = (undefined **)0x0;
  if (local_140 != (int *)0x0) {
    iVar6 = *local_140;
    *local_140 = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_138 != (int *)0x0) {
    iVar6 = *local_138;
    *local_138 = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_101449efc();
    }
  }
  lVar9 = 0;
  if (*(long *)(param_1 + 0x578) != 0) {
    lVar9 = *(long *)(param_1 + 0x578) + 0x18;
  }
  FUN_10260aa38(*(undefined8 *)(param_1 + 0x568),lVar9,0);
  FUN_101427680(&local_138,"Waveform Zoom");
  FUN_101427680(&local_140,"Gain");
  local_148 = 0;
  uStack_144 = 0x2715;
  local_14c = 0x272e;
  FUN_102671e38(&local_e0,&local_138,&local_140,&uStack_144,&local_148,&local_14c);
  lVar9 = *(long *)(param_1 + 0x520);
  if (lVar9 != 0) {
    iVar6 = *(int *)(lVar9 + 8) + -1;
    *(int *)(lVar9 + 8) = iVar6;
    if (iVar6 == 0) {
      FUN_10128eea0();
    }
  }
  *(long *)(param_1 + 0x520) = (long)local_e0;
  local_e0 = (undefined **)0x0;
  if (local_140 != (int *)0x0) {
    iVar6 = *local_140;
    *local_140 = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_138 != (int *)0x0) {
    iVar6 = *local_138;
    *local_138 = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_101449efc();
    }
  }
  lVar9 = 0;
  if (*(long *)(param_1 + 0x520) != 0) {
    lVar9 = *(long *)(param_1 + 0x520) + 0x18;
  }
  FUN_10260aa38(*(undefined8 *)(param_1 + 0x510),lVar9,0);
  FUN_101427680(&local_138,"Waveform Zoom");
  FUN_101427680(&local_140,"On/Off");
  local_148 = 0;
  uStack_144 = 0x2715;
  local_14c = 0x272f;
  FUN_102671e38(&local_e0,&local_138,&local_140,&uStack_144,&local_148,&local_14c);
  lVar9 = *(long *)(param_1 + 0x558);
  if (lVar9 != 0) {
    iVar6 = *(int *)(lVar9 + 8) + -1;
    *(int *)(lVar9 + 8) = iVar6;
    if (iVar6 == 0) {
      FUN_10128eea0();
    }
  }
  *(long *)(param_1 + 0x558) = (long)local_e0;
  local_e0 = (undefined **)0x0;
  if (local_140 != (int *)0x0) {
    iVar6 = *local_140;
    *local_140 = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_138 != (int *)0x0) {
    iVar6 = *local_138;
    *local_138 = iVar6 + -1;
    if (iVar6 + -1 == 0) {
      FUN_101449efc();
    }
  }
  lVar9 = 0;
  if (*(long *)(param_1 + 0x558) != 0) {
    lVar9 = *(long *)(param_1 + 0x558) + 0x18;
  }
  FUN_10260aa38(*(undefined8 *)(param_1 + 0x548),lVar9,0);
  if (((DAT_10700c4a8 & 1) == 0) && (iVar6 = ___cxa_guard_acquire(&DAT_10700c4a8), iVar6 != 0)) {
    FUN_101427680(&local_e0,"None");
    FUN_101427680("1/4");
    FUN_101427680("1/8");
    FUN_101427680("1/8T");
    FUN_101427680("1/8 + 1/8T");
    FUN_101427680(auStack_b8,"1/16");
    FUN_101427680(auStack_b0,"1/16T");
    FUN_101427680(auStack_a8,"1/16 + 1/16T");
    FUN_101427680(auStack_a0,"1/32");
    FUN_1002c29cc(&DAT_10700c758,&local_e0,9);
    FUN_100234444(auStack_a0);
    FUN_100234444(auStack_a8);
    FUN_100234444(auStack_b0);
    FUN_100234444(auStack_b8);
    FUN_100234444(auStack_c0);
    FUN_100234444(&local_c8);
    FUN_100234444(auStack_d0);
    FUN_100234444(&lStack_d8);
    FUN_100234444(&local_e0);
    ___cxa_atexit(FUN_1002343c8,&DAT_10700c758,0x100000000);
    ___cxa_guard_release(&DAT_10700c4a8);
  }
  local_e0 = (undefined **)puVar4;
  lStack_d8 = 0;
  FUN_101567bfc(*(undefined8 *)(param_1 + 0x3c0),0,&DAT_10700c758,0,&local_e0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x3c0),1);
  local_e0 = &PTR_FUN_1067f4dc8;
  lStack_d8 = param_1;
  local_c8 = &local_e0;
  FUN_1025ebb00(*(undefined8 *)(param_1 + 0x588),&local_e0);
  if (local_c8 == &local_e0) {
    lVar9 = 0x20;
LAB_102670abc:
    (**(code **)((long)*local_c8 + lVar9))();
  }
  else if (local_c8 != (undefined ***)0x0) {
    lVar9 = 0x28;
    goto LAB_102670abc;
  }
  local_e0 = &PTR_FUN_1067f4e48;
  lStack_d8 = param_1;
  local_c8 = &local_e0;
  FUN_1025ebb00(*(undefined8 *)(param_1 + 0x5a0),&local_e0);
  if (local_c8 == &local_e0) {
    lVar9 = 0x20;
LAB_102670b04:
    (**(code **)((long)*local_c8 + lVar9))();
  }
  else if (local_c8 != (undefined ***)0x0) {
    lVar9 = 0x28;
    goto LAB_102670b04;
  }
  local_e0 = &PTR_FUN_1067f4ec8;
  lStack_d8 = param_1;
  local_c8 = &local_e0;
  FUN_1025ebb00(*(undefined8 *)(param_1 + 0x5b8),&local_e0);
  if (local_c8 == &local_e0) {
    lVar9 = 0x20;
LAB_102670b4c:
    (**(code **)((long)*local_c8 + lVar9))();
  }
  else if (local_c8 != (undefined ***)0x0) {
    lVar9 = 0x28;
    goto LAB_102670b4c;
  }
  local_e0 = &PTR_FUN_1067f4f48;
  lStack_d8 = param_1;
  local_c8 = &local_e0;
  FUN_1025ebb00(*(undefined8 *)(param_1 + 0x5d0),&local_e0);
  if (local_c8 == &local_e0) {
    lVar9 = 0x20;
LAB_102670b94:
    (**(code **)((long)*local_c8 + lVar9))();
  }
  else if (local_c8 != (undefined ***)0x0) {
    lVar9 = 0x28;
    goto LAB_102670b94;
  }
  local_e0 = &PTR_FUN_1067f5008;
  lStack_d8 = param_1;
  local_c8 = &local_e0;
  FUN_1025ebb00(*(undefined8 *)(param_1 + 0x5e8),&local_e0);
  if (local_c8 == &local_e0) {
    lVar9 = 0x20;
LAB_102670bdc:
    (**(code **)((long)*local_c8 + lVar9))();
  }
  else if (local_c8 != (undefined ***)0x0) {
    lVar9 = 0x28;
    goto LAB_102670bdc;
  }
  FUN_102640c7c(*(undefined8 *)(param_1 + 0x2b0));
  FUN_10155e55c(*(undefined8 *)(param_1 + 0x2b0),1);
  local_e0 = (undefined **)puVar4;
  lStack_d8 = 0;
  FUN_101564728(*(undefined8 *)(param_1 + 0x2c8),1,&local_e0);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x2c8),1);
  local_e0 = (undefined **)PTR_CallMemberFunc<&ASong::InKeyController>_106534af8;
  lStack_d8 = param_1;
  FUN_101564768(*(undefined8 *)(param_1 + 0x2c8),&local_e0);
  local_e0 = (undefined **)PTR_CallMemberFunc<&ASong::ScaleController>_106534b00;
  lStack_d8 = param_1;
  FUN_102641db8(*(undefined8 *)(param_1 + 0x2b0),&local_e0);
  uVar8 = FUN_101544830(param_1);
  local_100[0] = &PTR_FUN_1067f50c8;
  local_e8 = local_100;
  FUN_10155bbac(uVar8,local_100);
  if (local_e8 == local_100) {
    lVar9 = 0x20;
  }
  else {
    if (local_e8 == (undefined ***)0x0) goto LAB_102670c98;
    lVar9 = 0x28;
  }
  (**(code **)((long)*local_e8 + lVar9))();
LAB_102670c98:
  local_e0 = (undefined **)puVar4;
  lStack_d8 = 0;
  FUN_101568960(0,*(undefined8 *)(param_1 + 0x2f8),&local_e0);
  if (*(long *)PTR____stack_chk_guard_1064f8818 == local_70) {
    return param_1;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

