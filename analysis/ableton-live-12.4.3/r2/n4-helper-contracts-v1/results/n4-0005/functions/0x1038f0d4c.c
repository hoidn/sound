
/* WARNING: Removing unreachable block (ram,0x0001038f14fc) */
/* WARNING: Removing unreachable block (ram,0x0001038f150c) */
/* WARNING: Removing unreachable block (ram,0x0001038f1708) */
/* WARNING: Removing unreachable block (ram,0x0001038f1438) */
/* WARNING: Removing unreachable block (ram,0x0001038f16bc) */
/* WARNING: Removing unreachable block (ram,0x0001038f16e8) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1038f0d4c(undefined8 param_1,undefined8 param_2,int param_3,undefined8 param_4)

{
  int iVar1;
  long lVar2;
  undefined8 *puVar3;
  pid_t pVar4;
  int iVar5;
  char *pcVar6;
  undefined8 uVar7;
  int *piVar8;
  ulong extraout_x1;
  ulong extraout_x1_00;
  undefined8 *puVar9;
  undefined1 auVar10 [16];
  void *local_120 [2];
  char local_109;
  undefined1 local_108 [16];
  undefined8 *local_f8;
  undefined8 *local_f0;
  undefined8 *local_e8;
  undefined8 **local_e0;
  ulong uStack_d8;
  long lStack_d0;
  undefined8 uStack_c8;
  int *local_c0;
  undefined4 local_b8;
  undefined4 uStack_b4;
  undefined1 uStack_b0;
  undefined1 local_af;
  char local_a1;
  undefined4 local_a0;
  undefined4 uStack_9c;
  char local_89;
  undefined4 local_88;
  undefined4 uStack_84;
  undefined1 uStack_80;
  undefined1 uStack_7f;
  undefined6 uStack_7e;
  undefined1 local_71;
  undefined1 local_70 [8];
  long *plStack_68;
  undefined8 uStack_60;
  undefined8 uStack_58;
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_1064f8818;
  uStack_d8 = _UNK_105928998;
  local_e0 = _DAT_105928990;
  uStack_c8 = _UNK_1059289a8;
  lStack_d0 = _DAT_1059289a0;
  _local_70 = FUN_1011aeb80(&local_e0);
  if ((local_70._8_8_ & 1) == 0) {
    pcVar6 = "info";
  }
  else {
    pcVar6 = (char *)FUN_1011abfc0(local_70,1,"info");
  }
  FUN_101427680(&local_c0,pcVar6);
  FUN_1011cb734(local_70);
  FUN_101427680(&local_e0,"--parent-process-id=");
  uVar7 = FUN_10142da5c(local_70,&local_e0);
  if ((local_e0 != (undefined8 **)0x0) &&
     (iVar5 = *(int *)local_e0, *(int *)local_e0 = iVar5 + -1, iVar5 + -1 == 0)) {
    FUN_101449efc();
  }
  pVar4 = _getpid();
  FUN_101430a10(&local_e0,pVar4);
  FUN_10142da5c(uVar7,&local_e0);
  if ((local_e0 != (undefined8 **)0x0) &&
     (iVar5 = *(int *)local_e0, *(int *)local_e0 = iVar5 + -1, iVar5 + -1 == 0)) {
    FUN_101449efc();
  }
  FUN_101427680(&local_88,"--log-level=");
  FUN_10142dc34(&plStack_68,&local_88,&local_c0);
  local_f8 = (undefined8 *)0x0;
  local_f0 = (undefined8 *)0x0;
  local_e0 = &local_f8;
  local_e8 = (undefined8 *)0x0;
  uStack_d8 = uStack_d8 & 0xffffffffffffff00;
  local_f8 = operator_new(0x10);
  local_f0 = local_f8 + 2;
  *local_f8 = local_70;
  if (local_70 != (undefined1  [8])0x0) {
    *(int *)local_70 = *(int *)local_70 + 1;
  }
  local_f8[1] = plStack_68;
  local_e8 = local_f0;
  if (plStack_68 != (long *)0x0) {
    *(int *)plStack_68 = (int)*plStack_68 + 1;
    iVar5 = (int)*plStack_68 + -1;
    *(int *)plStack_68 = iVar5;
    if (iVar5 == 0) {
      FUN_101449efc(plStack_68);
    }
  }
  if (local_70 != (undefined1  [8])0x0) {
    iVar5 = *(int *)local_70;
    *(int *)local_70 = iVar5 + -1;
    if (iVar5 + -1 == 0) {
      FUN_101449efc();
    }
  }
  piVar8 = (int *)CONCAT44(uStack_84,local_88);
  if ((piVar8 != (int *)0x0) && (iVar5 = *piVar8, *piVar8 = iVar5 + -1, iVar5 + -1 == 0)) {
    FUN_101449efc();
  }
  uStack_d8 = _UNK_1059289b8;
  local_e0 = _DAT_1059289b0;
  uStack_c8 = _UNK_1059289c8;
  lStack_d0 = _DAT_1059289c0;
  auVar10 = FUN_1011aeb80(&local_e0);
  _local_70 = auVar10;
  if ((auVar10._8_8_ & 1) != 0) {
    FUN_101427680(&local_88,"--python-log-filters=");
    FUN_1011abfa4(local_70);
    FUN_101427680(&local_a0);
    FUN_10142dc34(&local_e0,&local_88,&local_a0);
    if (local_f0 < local_e8) {
      *local_f0 = 0;
      *local_f0 = local_e0;
      local_e0 = (undefined8 **)0x0;
      local_f0 = local_f0 + 1;
    }
    else {
      local_f0 = (undefined8 *)FUN_1002b614c(&local_f8,&local_e0);
      if ((local_e0 != (undefined8 **)0x0) &&
         (iVar5 = *(int *)local_e0, *(int *)local_e0 = iVar5 + -1, iVar5 + -1 == 0)) {
        FUN_101449efc();
      }
    }
    piVar8 = (int *)CONCAT44(uStack_9c,local_a0);
    if ((piVar8 != (int *)0x0) && (iVar5 = *piVar8, *piVar8 = iVar5 + -1, iVar5 + -1 == 0)) {
      FUN_101449efc();
    }
    piVar8 = (int *)CONCAT44(uStack_84,local_88);
    if ((piVar8 != (int *)0x0) && (iVar5 = *piVar8, *piVar8 = iVar5 + -1, iVar5 + -1 == 0)) {
      FUN_101449efc();
    }
  }
  FUN_1011db938(&local_88);
  iVar5 = (**(code **)(*(long *)CONCAT62(uStack_7e,CONCAT11(uStack_7f,uStack_80)) + 0x80))();
  if (iVar5 == 0) {
LAB_1038f103c:
    plStack_68 = _UNK_1059289f8;
    local_70 = (undefined1  [8])_DAT_1059289f0;
    uStack_58 = _UNK_105928a08;
    uStack_60 = _DAT_105928a00;
    FUN_1011aeb80(local_70);
    lVar2 = CONCAT44(uStack_84,local_88);
    if ((lVar2 != 0) && (iVar5 = *(int *)(lVar2 + 8) + -1, *(int *)(lVar2 + 8) = iVar5, iVar5 == 0))
    {
      FUN_10128eea0();
    }
    if ((extraout_x1_00 & 1) != 0) goto LAB_1038f10e4;
    FUN_101427680(&local_e0,"--dont-log-to-console");
    if (local_e8 <= local_f0) {
      local_f0 = (undefined8 *)FUN_1002b614c(&local_f8,&local_e0);
      auVar10._8_8_ = plStack_68;
      auVar10._0_8_ = local_70;
      if ((local_e0 != (undefined8 **)0x0) &&
         (iVar5 = *(int *)local_e0, *(int *)local_e0 = iVar5 + -1, _local_70 = auVar10,
         iVar5 + -1 == 0)) {
        FUN_101449efc();
      }
      goto LAB_1038f1110;
    }
  }
  else {
    uStack_d8 = _UNK_1059289d8;
    local_e0 = _DAT_1059289d0;
    uStack_c8 = _UNK_1059289e8;
    lStack_d0 = _DAT_1059289e0;
    FUN_1011aeb80(&local_e0);
    if ((extraout_x1 & 1) != 0) goto LAB_1038f103c;
    lVar2 = CONCAT44(uStack_84,local_88);
    if ((lVar2 != 0) && (iVar5 = *(int *)(lVar2 + 8) + -1, *(int *)(lVar2 + 8) = iVar5, iVar5 == 0))
    {
      FUN_10128eea0();
    }
LAB_1038f10e4:
    FUN_101427680(&local_e0,"--show-developer-window");
    if (local_e8 <= local_f0) {
      local_f0 = (undefined8 *)FUN_1002b614c(&local_f8,&local_e0);
      if ((local_e0 != (undefined8 **)0x0) &&
         (iVar5 = *(int *)local_e0, *(int *)local_e0 = iVar5 + -1, iVar5 + -1 == 0)) {
        FUN_101449efc();
      }
      goto LAB_1038f1110;
    }
  }
  *local_f0 = 0;
  *local_f0 = local_e0;
  local_f0 = local_f0 + 1;
LAB_1038f1110:
  if (param_3 != 0) {
    FUN_101427680(&local_e0,"--faceless");
    if (local_f0 < local_e8) {
      *local_f0 = 0;
      *local_f0 = local_e0;
      local_f0 = local_f0 + 1;
    }
    else {
      local_f0 = (undefined8 *)FUN_1002b614c(&local_f8,&local_e0);
      if ((local_e0 != (undefined8 **)0x0) &&
         (iVar5 = *(int *)local_e0, *(int *)local_e0 = iVar5 + -1, iVar5 + -1 == 0)) {
        FUN_101449efc();
      }
    }
  }
  uStack_d8 = _UNK_105928a18;
  local_e0 = _DAT_105928a10;
  uStack_c8 = _UNK_105928a28;
  lStack_d0 = _DAT_105928a20;
  local_108 = FUN_1011aeb80(&local_e0);
  if ((local_108._8_8_ & 1) != 0) {
    FUN_101427680(&local_e0,"--emulator");
    if (local_f0 < local_e8) {
      *local_f0 = 0;
      *local_f0 = local_e0;
      local_f0 = local_f0 + 1;
    }
    else {
      local_f0 = (undefined8 *)FUN_1002b614c(&local_f8,&local_e0);
      if ((local_e0 != (undefined8 **)0x0) &&
         (iVar5 = *(int *)local_e0, *(int *)local_e0 = iVar5 + -1, iVar5 + -1 == 0)) {
        FUN_101449efc();
      }
    }
    if ((local_108._8_8_ & 1) != 0) {
      pcVar6 = (char *)FUN_1011abfa4(local_108);
      iVar5 = _strcmp(pcVar6,"ah05");
      if (iVar5 == 0) {
        FUN_101427680(&local_e0,"--emulator-device=ah05");
        if (local_f0 < local_e8) {
          *local_f0 = 0;
          *local_f0 = local_e0;
          local_f0 = local_f0 + 1;
        }
        else {
          local_f0 = (undefined8 *)FUN_1002b614c(&local_f8,&local_e0);
          if ((local_e0 != (undefined8 **)0x0) &&
             (iVar5 = *(int *)local_e0, *(int *)local_e0 = iVar5 + -1, iVar5 + -1 == 0)) {
            FUN_101449efc();
          }
        }
      }
    }
  }
  if ((int)param_4 != -1) {
    FUN_10142d468(local_70,L"--crashpad-fd=");
    FUN_101430a10(&local_88,param_4);
    FUN_10142dc34(&local_e0,local_70,&local_88);
    if (local_f0 < local_e8) {
      *local_f0 = 0;
      *local_f0 = local_e0;
      local_e0 = (undefined8 **)0x0;
      local_f0 = local_f0 + 1;
    }
    else {
      local_f0 = (undefined8 *)FUN_1002b614c(&local_f8,&local_e0);
      if ((local_e0 != (undefined8 **)0x0) &&
         (iVar5 = *(int *)local_e0, *(int *)local_e0 = iVar5 + -1, iVar5 + -1 == 0)) {
        FUN_101449efc();
      }
    }
    piVar8 = (int *)CONCAT44(uStack_84,local_88);
    if ((piVar8 != (int *)0x0) && (iVar5 = *piVar8, *piVar8 = iVar5 + -1, iVar5 + -1 == 0)) {
      FUN_101449efc();
    }
    if ((local_70 != (undefined1  [8])0x0) &&
       (iVar5 = *(int *)local_70, *(int *)local_70 = iVar5 + -1, iVar5 + -1 == 0)) {
      FUN_101449efc();
    }
  }
  FUN_10142d468(local_70,L"--language=");
  FUN_1015041e0(&local_88);
  FUN_10142dc34(&local_e0,local_70,&local_88);
  if (local_f0 < local_e8) {
    *local_f0 = 0;
    *local_f0 = local_e0;
    local_e0 = (undefined8 **)0x0;
    local_f0 = local_f0 + 1;
  }
  else {
    local_f0 = (undefined8 *)FUN_1002b614c(&local_f8,&local_e0);
    if ((local_e0 != (undefined8 **)0x0) &&
       (iVar5 = *(int *)local_e0, *(int *)local_e0 = iVar5 + -1, iVar5 + -1 == 0)) {
      FUN_101449efc();
    }
  }
  piVar8 = (int *)CONCAT44(uStack_84,local_88);
  if ((piVar8 != (int *)0x0) && (iVar5 = *piVar8, *piVar8 = iVar5 + -1, iVar5 + -1 == 0)) {
    FUN_101449efc();
  }
  if ((local_70 != (undefined1  [8])0x0) &&
     (iVar5 = *(int *)local_70, *(int *)local_70 = iVar5 + -1, iVar5 + -1 == 0)) {
    FUN_101449efc();
  }
  FUN_1008fcae4(local_70);
  FUN_103e96bc4(&local_e0,local_70);
  FUN_1011db938(local_70);
  iVar5 = (**(code **)(*plStack_68 + 0x80))();
  if ((local_70 != (undefined1  [8])0x0) &&
     (iVar1 = *(int *)((long)local_70 + 8) + -1, *(int *)((long)local_70 + 8) = iVar1, iVar1 == 0))
  {
    FUN_10128eea0();
  }
  if (iVar5 == 0) {
    FUN_1002aab04(local_70,&local_e0);
    local_a0 = 0x706c6548;
    uStack_9c = 0x737265;
    local_89 = '\a';
    FUN_100241e54(&local_88,local_70,&local_a0);
    local_b8 = 0x68737550;
    uStack_b4 = 0x70612e33;
    uStack_b0 = 0x70;
    local_af = 0;
    local_a1 = '\t';
    FUN_100241e54(local_120,&local_88,&local_b8);
    if (local_a1 < '\0') {
      operator_delete((void *)CONCAT44(uStack_b4,local_b8));
    }
    if (local_89 < '\0') {
      operator_delete((void *)CONCAT44(uStack_9c,local_a0));
    }
  }
  else {
    FUN_1002aab04(&local_a0,&local_e0);
    FUN_1002aab04(&local_88,&local_a0);
    FUN_1002aab04(local_70,&local_88);
    if (local_89 < '\0') {
      operator_delete((void *)CONCAT44(uStack_9c,local_a0));
    }
    local_88 = 0x68737550;
    uStack_84 = 0x70612e33;
    uStack_80 = 0x70;
    uStack_7f = 0;
    local_71 = 9;
    FUN_100241e54(local_120,local_70,&local_88);
  }
  if (lStack_d0 < 0) {
    operator_delete(local_e0);
  }
  local_e0 = (undefined8 **)((ulong)local_e0 & 0xffffffff00000000);
  local_70 = (undefined1  [8])((ulong)local_70 & 0xffffffff00000000);
  FUN_1038f1a8c(param_1,local_120,&local_f8,PTR_KPushIpcChannelName_106509670,"push-app-launching",
                param_2,&local_e0,local_70);
  puVar3 = local_f8;
  puVar9 = local_f0;
  if (local_109 < '\0') {
    operator_delete(local_120[0]);
    puVar3 = local_f8;
    puVar9 = local_f0;
  }
  local_f8 = puVar3;
  local_f0 = puVar9;
  if (puVar3 != (undefined8 *)0x0) {
    if (puVar9 == puVar3) {
      local_f0 = puVar3;
      operator_delete(puVar3);
    }
    else {
      do {
        puVar9 = puVar9 + -1;
        piVar8 = (int *)*puVar9;
        if ((piVar8 != (int *)0x0) && (iVar5 = *piVar8, *piVar8 = iVar5 + -1, iVar5 + -1 == 0)) {
          FUN_101449efc();
        }
      } while (puVar9 != puVar3);
      local_f0 = puVar3;
      operator_delete(local_f8);
    }
  }
  if ((local_c0 != (int *)0x0) && (iVar5 = *local_c0, *local_c0 = iVar5 + -1, iVar5 + -1 == 0)) {
    FUN_101449efc();
  }
  if (*(long *)PTR____stack_chk_guard_1064f8818 == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

