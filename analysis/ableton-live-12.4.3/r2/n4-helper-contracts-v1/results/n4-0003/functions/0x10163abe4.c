
void FUN_10163abe4(undefined8 *param_1,undefined8 param_2)

{
  int iVar1;
  ulong uVar2;
  code *pcVar3;
  undefined8 *puVar4;
  void *pvVar5;
  undefined8 *puVar6;
  undefined8 uVar7;
  int *piVar8;
  undefined8 *local_160;
  undefined8 *local_158;
  long local_150;
  int *local_148;
  int *local_140;
  int *local_138;
  void *local_130;
  undefined8 uStack_128;
  long local_120;
  void *local_110;
  undefined8 uStack_108;
  long local_100;
  int *local_f8;
  void *local_f0;
  undefined8 uStack_e8;
  long local_e0;
  undefined8 *local_d0;
  undefined8 *puStack_c8;
  int *local_c0;
  undefined1 local_b8;
  undefined8 local_b0;
  undefined8 uStack_a8;
  undefined8 local_a0;
  undefined8 *puStack_98;
  undefined8 *puStack_90;
  undefined8 uStack_88;
  undefined8 local_80;
  undefined8 uStack_78;
  undefined8 uStack_70;
  undefined8 uStack_68;
  undefined8 local_60;
  undefined4 local_58;
  undefined8 local_50;
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_1064f8818;
  uStack_78 = 0;
  local_80 = 0;
  uStack_68 = 0;
  uStack_70 = 0;
  puStack_98 = (undefined8 *)0x0;
  local_a0 = 0;
  uStack_88 = 0;
  puStack_90 = (undefined8 *)0x0;
  uStack_a8 = 0;
  local_b0 = 0;
  local_60 = 0x400;
  local_58 = 0;
  local_50 = 0;
  puVar4 = operator_new(0x18);
  *puVar4 = 0x10000;
  pvVar5 = operator_new(1);
  puVar6 = _malloc(0x38);
  puVar6[4] = 0;
  puVar4[1] = pvVar5;
  puVar4[2] = puVar6;
  *puVar6 = puVar6 + 4;
  puVar6[1] = pvVar5;
  puVar6[5] = 0;
  puVar6[6] = 0;
  *(undefined1 *)(puVar6 + 3) = 1;
  puVar6[2] = 1;
  local_d0 = &local_b0;
  uStack_a8 = 0;
  local_b0 = 0;
  local_a0 = 0x3000000000000;
  puStack_c8 = local_d0;
  puStack_98 = puVar4;
  puStack_90 = puVar4;
  if (*(char *)((long)param_1 + 0x17) < '\0') {
    FUN_10023448c(&local_f0,*param_1,param_1[1]);
  }
  else {
    uStack_e8 = param_1[1];
    local_f0 = (void *)*param_1;
    local_e0 = param_1[2];
  }
  uVar7 = FUN_100275a94(&local_d0,"db-path",&local_f0);
  local_f8 = (int *)param_1[6];
  if (local_f8 != (int *)0x0) {
    *local_f8 = *local_f8 + 1;
  }
  uVar7 = FUN_10024e4b0(uVar7,"ipc-channel",&local_f8);
  if (*(char *)((long)param_1 + 0x4f) < '\0') {
    FUN_10023448c(&local_110,param_1[7],param_1[8]);
  }
  else {
    uStack_108 = param_1[8];
    local_110 = (void *)param_1[7];
    local_100 = param_1[9];
  }
  uVar7 = FUN_100275a94(uVar7,"usage-data_file",&local_110);
  if (*(char *)((long)param_1 + 0x2f) < '\0') {
    FUN_10023448c(&local_130,param_1[3],param_1[4]);
  }
  else {
    uStack_128 = param_1[4];
    local_130 = (void *)param_1[3];
    local_120 = param_1[5];
  }
  uVar7 = FUN_100275a94(uVar7,"fileref-map-path",&local_130);
  local_138 = (int *)param_1[10];
  if (local_138 != (int *)0x0) {
    *local_138 = *local_138 + 1;
  }
  uVar7 = FUN_10024e4b0(uVar7,"parent-pid",&local_138);
  local_140 = (int *)param_1[0xb];
  if (local_140 != (int *)0x0) {
    *local_140 = *local_140 + 1;
  }
  uVar7 = FUN_10024e4b0(uVar7,"log-traces",&local_140);
  uVar7 = FUN_10024d77c(uVar7,"profile-log",*(undefined1 *)(param_1 + 0xc));
  local_148 = (int *)param_1[0xd];
  if (local_148 != (int *)0x0) {
    *local_148 = *local_148 + 1;
  }
  uVar7 = FUN_10024e4b0(uVar7,"os-events-flags",&local_148);
  uVar7 = FUN_10024de4c(uVar7,"db-stats-trigger",*(undefined4 *)(param_1 + 0xe));
  uVar7 = FUN_10024de4c(uVar7,"db-stale-factor",*(undefined4 *)((long)param_1 + 0x74));
  uVar7 = FUN_10024d77c(uVar7,"sound-analyzer",*(undefined1 *)(param_1 + 0xf));
  uVar7 = FUN_10024d77c(uVar7,"auto-keywords",*(undefined1 *)((long)param_1 + 0x79));
  local_160 = (undefined8 *)0x0;
  local_158 = (undefined8 *)0x0;
  local_150 = 0;
  puVar4 = (undefined8 *)param_1[0x10];
  puVar6 = (undefined8 *)param_1[0x11];
  local_b8 = 0;
  uVar2 = (long)puVar6 - (long)puVar4;
  local_c0 = (int *)&local_160;
  if (uVar2 != 0) {
    if ((long)uVar2 < 0) {
      local_c0 = (int *)&local_160;
      FUN_100256758(&local_160);
                    /* WARNING: Does not return */
      pcVar3 = (code *)SoftwareBreakpoint(1,0x10163b050);
      (*pcVar3)();
    }
    local_c0 = (int *)&local_160;
    local_160 = operator_new(uVar2);
    local_150 = (long)local_160 + uVar2;
    local_158 = local_160;
    do {
      piVar8 = (int *)*puVar4;
      *local_158 = piVar8;
      if (piVar8 != (int *)0x0) {
        *piVar8 = *piVar8 + 1;
      }
      puVar4 = puVar4 + 1;
      local_158 = local_158 + 1;
    } while (puVar4 != puVar6);
  }
  FUN_10024fd00(uVar7,"features",&local_160);
  puVar6 = local_160;
  puVar4 = local_158;
  if (local_160 != (undefined8 *)0x0) {
    while (puVar4 != puVar6) {
      puVar4 = puVar4 + -1;
      piVar8 = (int *)*puVar4;
      if ((piVar8 != (int *)0x0) && (iVar1 = *piVar8, *piVar8 = iVar1 + -1, iVar1 + -1 == 0)) {
        FUN_101449efc();
      }
    }
    local_158 = puVar6;
    operator_delete(local_160);
  }
  if ((local_148 != (int *)0x0) && (iVar1 = *local_148, *local_148 = iVar1 + -1, iVar1 + -1 == 0)) {
    FUN_101449efc();
  }
  if ((local_140 != (int *)0x0) && (iVar1 = *local_140, *local_140 = iVar1 + -1, iVar1 + -1 == 0)) {
    FUN_101449efc();
  }
  if ((local_138 != (int *)0x0) && (iVar1 = *local_138, *local_138 = iVar1 + -1, iVar1 + -1 == 0)) {
    FUN_101449efc();
  }
  if (local_120 < 0) {
    operator_delete(local_130);
  }
  if (local_100 < 0) {
    operator_delete(local_110);
  }
  if ((local_f8 != (int *)0x0) && (iVar1 = *local_f8, *local_f8 = iVar1 + -1, iVar1 + -1 == 0)) {
    FUN_101449efc();
  }
  if (local_e0 < 0) {
    operator_delete(local_f0);
  }
  FUN_101293eb4(&local_c0,&local_b0,0);
  FUN_1012784bc(&local_c0,param_2,0);
  if ((local_c0 != (int *)0x0) && (iVar1 = *local_c0, *local_c0 = iVar1 + -1, iVar1 + -1 == 0)) {
    FUN_101449efc();
  }
  FUN_10024db90(&local_b0);
  if (*(long *)PTR____stack_chk_guard_1064f8818 == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

