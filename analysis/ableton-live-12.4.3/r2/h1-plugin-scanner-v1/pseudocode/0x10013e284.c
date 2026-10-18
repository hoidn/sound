
void FUN_10013e284(long param_1,undefined8 *param_2)

{
  int iVar1;
  undefined8 *puVar2;
  void *pvVar3;
  undefined8 *puVar4;
  long *plVar5;
  int *local_d8;
  undefined8 *local_d0;
  undefined8 *puStack_c8;
  int *local_c0;
  int *local_b8;
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
  
  local_48 = *(long *)PTR____stack_chk_guard_100b1c378;
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
  puVar2 = operator_new(0x18);
  *puVar2 = 0x10000;
  pvVar3 = operator_new(1);
  puVar4 = _malloc(0x38);
  puVar2[1] = pvVar3;
  puVar2[2] = puVar4;
  puVar4[4] = 0;
  *puVar4 = puVar4 + 4;
  puVar4[1] = pvVar3;
  puVar4[5] = 0;
  puVar4[6] = 0;
  *(undefined1 *)(puVar4 + 3) = 1;
  puVar4[2] = 1;
  plVar5 = *(long **)(param_1 + 0x18);
  puStack_98 = puVar2;
  puStack_90 = puVar2;
  FUN_100431940(&local_b8,"current-plugin");
  local_d0 = &local_b0;
  if (local_a0._6_2_ != 3) {
    uStack_a8 = 0;
    local_b0 = 0;
    local_a0 = 0x3000000000000;
  }
  local_d8 = (int *)*param_2;
  if (local_d8 != (int *)0x0) {
    *local_d8 = *local_d8 + 1;
  }
  puStack_c8 = local_d0;
  puVar2 = (undefined8 *)FUN_100140360(&local_d0,"name",&local_d8);
  FUN_10029863c(&local_c0,*puVar2,0);
  (**(code **)(*plVar5 + 0x28))(plVar5,&local_b8,&local_c0);
  if (local_c0 != (int *)0x0) {
    iVar1 = *local_c0;
    *local_c0 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_100454b40();
    }
  }
  if (local_d8 != (int *)0x0) {
    iVar1 = *local_d8;
    *local_d8 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_100454b40();
    }
  }
  if (local_b8 != (int *)0x0) {
    iVar1 = *local_b8;
    *local_b8 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_100454b40();
    }
  }
  FUN_1001402a8(&local_b0);
  if (*(long *)PTR____stack_chk_guard_100b1c378 == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

