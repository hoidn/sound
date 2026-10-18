
void FUN_101573d24(long *param_1,undefined8 param_2)

{
  int iVar1;
  ulong uVar2;
  undefined8 *puVar3;
  void *pvVar4;
  undefined8 *puVar5;
  int *piVar6;
  int *local_c8;
  undefined8 *local_c0;
  undefined8 *puStack_b8;
  undefined8 local_b0;
  undefined8 uStack_a8;
  undefined8 uStack_a0;
  undefined8 *local_98;
  undefined8 *local_90;
  undefined8 uStack_88;
  undefined8 uStack_80;
  undefined8 uStack_78;
  undefined8 local_70;
  undefined8 uStack_68;
  undefined8 local_60;
  undefined8 uStack_58;
  undefined8 local_50;
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_1064f8818;
  if (((*param_1 == 0) || ((*(uint *)(*param_1 + 4) & 0xfffffffe) != 2)) &&
     (uVar2 = FUN_10142e540(param_1,"Ableton "), (uVar2 & 1) == 0)) {
    uStack_68 = 0;
    local_70 = 0;
    uStack_58 = 0;
    uStack_88 = 0;
    local_90 = (undefined8 *)0x0;
    uStack_78 = 0;
    uStack_80 = 0;
    uStack_a8 = 0;
    local_b0 = 0;
    local_98 = (undefined8 *)0x0;
    uStack_a0 = 0;
    local_60 = 0x400;
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
    piVar6 = (int *)*param_1;
    if (piVar6 == (int *)0x0) {
      uStack_a8 = 0;
      local_b0 = 0;
      uStack_a0 = 0x3000000000000;
    }
    else {
      *piVar6 = *piVar6 + 1;
      if (uStack_a0._6_2_ != 3) {
        uStack_a8 = 0;
        local_b0 = 0;
        uStack_a0 = 0x3000000000000;
      }
      *piVar6 = *piVar6 + 1;
    }
    puStack_b8 = &local_b0;
    local_c0 = &local_b0;
    local_c8 = piVar6;
    local_98 = puVar3;
    local_90 = puVar3;
    FUN_10024e4b0(&local_c0,"creatorname",&local_c8);
    if (local_c8 != (int *)0x0) {
      iVar1 = *local_c8;
      *local_c8 = iVar1 + -1;
      if (iVar1 + -1 == 0) {
        FUN_101449efc();
      }
    }
    local_c0 = &local_b0;
    if (uStack_a0._6_2_ != 3) {
      uStack_a8 = 0;
      local_b0 = 0;
      uStack_a0 = 0x3000000000000;
    }
    puStack_b8 = local_c0;
    FUN_10024d77c(&local_c0,"drag-and-drop",param_2);
    FUN_101454230("third-party-document",&local_b0,0);
    if (piVar6 != (int *)0x0) {
      iVar1 = *piVar6;
      *piVar6 = iVar1 + -1;
      if (iVar1 + -1 == 0) {
        FUN_101449efc(piVar6);
      }
    }
    FUN_10024db90(&local_b0);
  }
  if (*(long *)PTR____stack_chk_guard_1064f8818 == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

