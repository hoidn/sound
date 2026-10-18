
void FUN_1008eb548(undefined8 param_1,undefined8 param_2,undefined8 param_3)

{
  int iVar1;
  undefined8 uVar2;
  undefined8 *puVar3;
  void *pvVar4;
  undefined8 *puVar5;
  long lVar6;
  int *local_e0;
  int *local_d8;
  int *local_d0;
  int *local_c8;
  code **local_c0;
  code **ppcStack_b8;
  code *local_b0;
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
  uVar2 = FUN_1017ec4b8();
  FUN_1017eca30(uVar2,param_1);
  uVar2 = std::chrono::system_clock::now();
  FUN_103f3ffec(&local_b0,2,uVar2);
  iVar1 = FUN_103f3c8b8(&local_b0);
  if (iVar1 != 0) {
    uVar2 = FUN_103f39a78(&local_b0,"WebConnectStarter: ");
    FUN_103f39a78(uVar2,"Starting up");
  }
  thunk_FUN_103f395e4(&local_b0);
  FUN_101427680(&local_b0,"start");
  FUN_1014528e4(&local_b0);
  if (local_b0 != (code *)0x0) {
    iVar1 = *(int *)local_b0;
    *(int *)local_b0 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  FUN_101849958();
  thunk_FUN_101854584();
  FUN_10031c488();
  uStack_78 = 0;
  local_80 = 0;
  uStack_68 = 0;
  uStack_70 = 0;
  puStack_98 = (undefined8 *)0x0;
  local_a0 = 0;
  uStack_88 = 0;
  puStack_90 = (undefined8 *)0x0;
  uStack_a8 = 0;
  local_b0 = (code *)0x0;
  local_60 = 0x400;
  local_58 = 0;
  local_50 = 0;
  puVar3 = operator_new(0x18);
  *puVar3 = 0x10000;
  pvVar4 = operator_new(1);
  puVar5 = _malloc(0x38);
  puVar3[1] = pvVar4;
  puVar3[2] = puVar5;
  puVar5[4] = 0;
  *puVar5 = puVar5 + 4;
  puVar5[1] = pvVar4;
  puVar5[5] = 0;
  puVar5[6] = 0;
  *(undefined1 *)(puVar5 + 3) = 1;
  puVar5[2] = 1;
  local_c0 = &local_b0;
  uStack_a8 = 0;
  local_b0 = (code *)0x0;
  local_a0 = 0x3000000000000;
  ppcStack_b8 = local_c0;
  puStack_98 = puVar3;
  puStack_90 = puVar3;
  FUN_1014550ec(&local_c8,DAT_106eca240);
  uVar2 = FUN_10024e4b0(&local_c0,"collect_crashlog_was_called",&local_c8);
  local_d0 = DAT_106eca228;
  if (DAT_106eca228 != (int *)0x0) {
    *DAT_106eca228 = *DAT_106eca228 + 1;
  }
  uVar2 = FUN_10024e4b0(uVar2,"found_previous_usage_log",&local_d0);
  local_d8 = DAT_106eca230;
  if (DAT_106eca230 != (int *)0x0) {
    *DAT_106eca230 = *DAT_106eca230 + 1;
  }
  uVar2 = FUN_10024e4b0(uVar2,"found_crash_file",&local_d8);
  local_e0 = DAT_106eca238;
  if (DAT_106eca238 != (int *)0x0) {
    *DAT_106eca238 = *DAT_106eca238 + 1;
  }
  puVar3 = (undefined8 *)FUN_10024e4b0(uVar2,"copied_crash_file",&local_e0);
  FUN_101454230("crash_file_upload_data",*puVar3,0);
  if (local_e0 != (int *)0x0) {
    iVar1 = *local_e0;
    *local_e0 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_d8 != (int *)0x0) {
    iVar1 = *local_d8;
    *local_d8 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_d0 != (int *)0x0) {
    iVar1 = *local_d0;
    *local_d0 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_c8 != (int *)0x0) {
    iVar1 = *local_c8;
    *local_c8 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  FUN_10024db90(&local_b0);
  FUN_101849958();
  FUN_10184a7f4();
  lVar6 = FUN_102694660();
  if (lVar6 != 0) {
    FUN_1027752f0();
  }
  FUN_1008eab44(&local_b0);
  FUN_1014528e4(&local_b0);
  if (local_b0 != (code *)0x0) {
    iVar1 = *(int *)local_b0;
    *(int *)local_b0 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  local_b0 = FUN_1008eff68;
  uStack_a8 = 0;
  FUN_101447d84(60000,&local_b0,"NWebConnector");
  FUN_1008eb988(param_2,param_3);
  DAT_106ec9ff5 = 1;
  if (*(long *)PTR____stack_chk_guard_1064f8818 == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

