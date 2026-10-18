// 0x100230ab8 FUN_100230ab8 state=exported-with-warnings role=LiveFlip application root
// source chunk chunk-00097.jsonl; code_sha256=02ab3075438f7d0fa44bfbf15a6144cb8acd97a77a553ab3ec81eb770f23bfcc

void FUN_100230ab8(long *param_1)

{
  long **pplVar1;
  long *plVar2;
  long *plVar3;
  undefined8 uVar4;
  long lVar5;
  undefined8 local_c0;
  long *local_b8 [2];
  long *local_a8;
  long *local_98;
  long *local_90;
  char *local_88;
  undefined1 local_80;
  long *local_78;
  long *local_70;
  char *pcStack_68;
  long *local_60;
  undefined1 auStack_58 [8];
  long *local_50;
  char *pcStack_48;
  long *local_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_101b8c408;
  plVar2 = (long *)FUN_100f56340("Live");
  if (plVar2 == (long *)0x0) {
    uVar4 = ___cxa_allocate_exception(0x18);
    FUN_100193580();
                    /* WARNING: Subroutine does not return */
    ___cxa_throw(uVar4,&PTR_vtable_101bd0c88,FUN_100193654);
  }
  pcStack_68 = "Application";
  local_60 = (long *)0x0;
  local_90 = plVar2;
  local_70 = plVar2;
  local_50 = (long *)FUN_10019f8bc(&local_78);
  local_50 = (long *)*local_50;
  if (local_50 == (long *)0x0) {
    pcStack_48 = "create_application_instance";
    local_40 = (long *)0x0;
  }
  else {
    pcStack_48 = "create_application_instance";
    local_40 = (long *)0x0;
    if (*local_50 == 0) {
      FUN_100e7fb2c();
    }
  }
  local_c0 = *(undefined8 *)(*param_1 + 0x210);
  local_88 = "flip_root";
  local_80 = 2;
  FUN_100271f0c(local_b8,&local_88,&local_c0,0);
  FUN_100231980(&local_98,auStack_58,local_b8);
  if (local_98 != (long *)0x0) {
    lVar5 = *local_98;
    *local_98 = lVar5 + -1;
    if (lVar5 + -1 == 0) {
      FUN_100e7fb2c();
    }
  }
  if (local_a8 != (long *)0x0) {
    lVar5 = *local_a8;
    *local_a8 = lVar5 + -1;
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
  if (local_60 != (long *)0x0) {
    lVar5 = *local_60;
    *local_60 = lVar5 + -1;
    if (lVar5 + -1 == 0) {
      FUN_100e7fb2c();
    }
  }
  plVar3 = (long *)FUN_100f56340("LiveFlip");
  if (plVar3 == (long *)0x0) {
    uVar4 = ___cxa_allocate_exception(0x18);
    FUN_100193580();
                    /* WARNING: Subroutine does not return */
    ___cxa_throw(uVar4,&PTR_vtable_101bd0c88,FUN_100193654);
  }
  lVar5 = *plVar3;
  *plVar3 = lVar5 + -1;
  if (lVar5 + -1 == 0) {
    FUN_100e7fb2c();
  }
  pcStack_68 = "Application";
  local_60 = (long *)0x0;
  local_70 = plVar2;
  local_50 = (long *)FUN_10019f8bc(&local_78);
  local_50 = (long *)*local_50;
  if (local_50 == (long *)0x0) {
    pcStack_48 = "get_application";
    local_40 = (long *)0x0;
  }
  else {
    pcStack_48 = "get_application";
    local_40 = (long *)0x0;
    if (*local_50 == 0) {
      FUN_100e7fb2c();
    }
  }
  FUN_100231a68(local_b8,auStack_58);
  if (local_40 != (long *)0x0) {
    lVar5 = *local_40;
    *local_40 = lVar5 + -1;
    if (lVar5 + -1 == 0) {
      FUN_100e7fb2c();
    }
  }
  if (local_60 != (long *)0x0) {
    lVar5 = *local_60;
    *local_60 = lVar5 + -1;
    if (lVar5 + -1 == 0) {
      FUN_100e7fb2c();
    }
  }
  local_50 = local_b8[0];
  pcStack_48 = "get_flip_model_root";
  local_40 = (long *)0x0;
  FUN_100231a68(&local_78,auStack_58);
  pplVar1 = (long **)(param_1 + 0x23);
  if (pplVar1 != &local_78) {
    plVar3 = *pplVar1;
    *pplVar1 = local_78;
    local_78 = (long *)0x0;
    if ((plVar3 == (long *)0x0) || (lVar5 = *plVar3, *plVar3 = lVar5 + -1, lVar5 + -1 != 0))
    goto LAB_100230d14;
    FUN_100e7fb2c(plVar3);
  }
  if (local_78 != (long *)0x0) {
    lVar5 = *local_78;
    *local_78 = lVar5 + -1;
    if (lVar5 + -1 == 0) {
      FUN_100e7fb2c();
    }
  }
LAB_100230d14:
  if (local_40 != (long *)0x0) {
    lVar5 = *local_40;
    *local_40 = lVar5 + -1;
    if (lVar5 + -1 == 0) {
      FUN_100e7fb2c();
    }
  }
  if (local_b8[0] != (long *)0x0) {
    lVar5 = *local_b8[0];
    *local_b8[0] = lVar5 + -1;
    if (lVar5 + -1 == 0) {
      FUN_100e7fb2c();
    }
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

