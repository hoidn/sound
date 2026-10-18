// 0x1002313d8 FUN_1002313d8 state=exported-with-warnings role=ScriptHost embedded module names
// source chunk chunk-00097.jsonl; code_sha256=9b4da753a063fbe24badb8ec45b734148fe699e0d8783915579c2d9f41085d02

void FUN_1002313d8(undefined8 *param_1)

{
  long **pplVar1;
  long *plVar2;
  long *plVar3;
  undefined8 uVar4;
  long lVar5;
  long *plVar6;
  long *local_b0;
  undefined8 local_a8;
  undefined8 uStack_a0;
  undefined8 local_98;
  undefined8 uStack_90;
  undefined1 local_81;
  undefined8 local_80;
  undefined8 local_78;
  long *local_70;
  long *local_68;
  long *local_60;
  undefined1 auStack_58 [8];
  long *local_50;
  char *pcStack_48;
  long *local_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_101b8c408;
  plVar2 = (long *)FUN_100f56340("BrowserBackend");
  if (plVar2 == (long *)0x0) {
    uVar4 = ___cxa_allocate_exception(0x18);
    FUN_100193580();
LAB_100231734:
                    /* WARNING: Subroutine does not return */
    ___cxa_throw(uVar4,&PTR_vtable_101bd0c88,FUN_100193654);
  }
  lVar5 = *plVar2;
  *plVar2 = lVar5 + -1;
  if (lVar5 + -1 == 0) {
    FUN_100e7fb2c();
  }
  plVar2 = (long *)FUN_100f56340("UsbInterface");
  if (plVar2 == (long *)0x0) {
    uVar4 = ___cxa_allocate_exception(0x18);
    FUN_100193580();
    goto LAB_100231734;
  }
  lVar5 = *plVar2;
  *plVar2 = lVar5 + -1;
  if (lVar5 + -1 == 0) {
    FUN_100e7fb2c();
  }
  plVar2 = (long *)FUN_100f56340("WifiConnector");
  if (plVar2 == (long *)0x0) {
    uVar4 = ___cxa_allocate_exception(0x18);
    FUN_100193580();
    goto LAB_100231734;
  }
  lVar5 = *plVar2;
  *plVar2 = lVar5 + -1;
  if (lVar5 + -1 == 0) {
    FUN_100e7fb2c();
  }
  plVar2 = (long *)FUN_100f56340("Screen");
  if (plVar2 == (long *)0x0) {
    uVar4 = ___cxa_allocate_exception(0x18);
    FUN_100193580();
    goto LAB_100231734;
  }
  lVar5 = *plVar2;
  *plVar2 = lVar5 + -1;
  if (lVar5 + -1 == 0) {
    FUN_100e7fb2c();
  }
  plVar2 = (long *)FUN_100f56340("WebService");
  if (plVar2 == (long *)0x0) {
    uVar4 = ___cxa_allocate_exception(0x18);
    FUN_100193580();
    goto LAB_100231734;
  }
  lVar5 = *plVar2;
  *plVar2 = lVar5 + -1;
  if (lVar5 + -1 == 0) {
    FUN_100e7fb2c();
  }
  plVar2 = (long *)FUN_100f56340("SoftwareUpdater");
  if (plVar2 == (long *)0x0) {
    uVar4 = ___cxa_allocate_exception(0x18);
    FUN_100193580();
    goto LAB_100231734;
  }
  lVar5 = *plVar2;
  *plVar2 = lVar5 + -1;
  if (lVar5 + -1 == 0) {
    FUN_100e7fb2c();
  }
  plVar2 = (long *)FUN_100f56340("MidiRemoteScript");
  if (plVar2 == (long *)0x0) {
    uVar4 = ___cxa_allocate_exception(0x18);
    FUN_100193580();
                    /* WARNING: Subroutine does not return */
    ___cxa_throw(uVar4,&PTR_vtable_101bd0c88,FUN_100193654);
  }
  local_60 = plVar2;
  plVar3 = (long *)FUN_100f56340(param_1[0x1d]);
  if (plVar3 == (long *)0x0) {
    uVar4 = ___cxa_allocate_exception(0x18);
    FUN_100193580();
                    /* WARNING: Subroutine does not return */
    ___cxa_throw(uVar4,&PTR_vtable_101bd0c88,FUN_100193654);
  }
  pcStack_48 = "create_instance";
  local_78 = param_1[0xf];
  local_80 = *param_1;
  local_81 = 1;
  uStack_90 = param_1[6];
  local_98 = param_1[8];
  uStack_a0 = param_1[9];
  local_a8 = param_1[10];
  local_40 = (long *)0x0;
  local_68 = plVar3;
  local_50 = plVar3;
  FUN_100231e34(&local_70,auStack_58,&local_78,&local_80,param_1 + 0xd,(long)param_1 + 0x6c,
                (long)param_1 + 0x6d,&local_81,param_1 + 5,&uStack_90,&local_98,param_1 + 0x15,
                param_1 + 0x19,&uStack_a0,&local_a8,param_1 + 0x22);
  pplVar1 = (long **)(param_1 + 0x24);
  if (pplVar1 != &local_70) {
    plVar6 = *pplVar1;
    *pplVar1 = local_70;
    local_70 = (long *)0x0;
    if ((plVar6 == (long *)0x0) || (lVar5 = *plVar6, *plVar6 = lVar5 + -1, lVar5 + -1 != 0))
    goto LAB_1002315ec;
    FUN_100e7fb2c(plVar6);
  }
  if (local_70 != (long *)0x0) {
    lVar5 = *local_70;
    *local_70 = lVar5 + -1;
    if (lVar5 + -1 == 0) {
      FUN_100e7fb2c();
    }
  }
LAB_1002315ec:
  if (local_40 != (long *)0x0) {
    lVar5 = *local_40;
    *local_40 = lVar5 + -1;
    if (lVar5 + -1 == 0) {
      FUN_100e7fb2c();
    }
  }
  local_50 = *pplVar1;
  pcStack_48 = "port_settings_changed";
  local_40 = (long *)0x0;
  FUN_100231a68(&local_b0,auStack_58);
  if (local_b0 != (long *)0x0) {
    lVar5 = *local_b0;
    *local_b0 = lVar5 + -1;
    if (lVar5 + -1 == 0) {
      FUN_100e7fb2c();
    }
  }
  if (local_40 != (long *)0x0) {
    lVar5 = *local_40;
    *local_40 = lVar5 + -1;
    if (lVar5 + -1 == 0) {
      FUN_100e7fb2c();
    }
  }
  lVar5 = *plVar3;
  *plVar3 = lVar5 + -1;
  if (lVar5 + -1 == 0) {
    FUN_100e7fb2c(plVar3);
  }
  lVar5 = *plVar2;
  *plVar2 = lVar5 + -1;
  if (lVar5 + -1 == 0) {
    FUN_100e7fb2c(plVar2);
  }
  if (*(long *)PTR____stack_chk_guard_101b8c408 == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

