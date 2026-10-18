// 0x100153650 FUN_100153650 state=exported-with-warnings body_bytes=924 warnings=3 chunk=chunk-00056.jsonl

uint FUN_100153650(undefined8 param_1,long param_2)

{
  ulong uVar1;
  code *pcVar2;
  int iVar3;
  uint uVar4;
  long *plVar5;
  undefined *puVar6;
  undefined *****pppppuVar7;
  undefined8 *puVar8;
  void *pvVar9;
  undefined8 *puVar10;
  undefined8 uVar11;
  long lVar12;
  ulong uVar13;
  uint uVar14;
  int *local_f0;
  undefined8 *local_e8;
  undefined8 local_e0;
  undefined8 uStack_d8;
  undefined ****local_d0;
  ulong uStack_c8;
  ulong local_c0;
  undefined ****local_b0;
  ulong uStack_a8;
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
  
  local_48 = *(long *)PTR____stack_chk_guard_100d60390;
  uStack_d8 = CONCAT17(9,(undefined7)uStack_d8);
  local_e8 = (undefined8 *)s_libconfig_100c1d5dd._0_8_;
  local_e0 = CONCAT62(local_e0._2_6_,0x67);
  plVar5 = (long *)FUN_10019e650(param_1,&local_e8);
  puVar6 = PTR_typeinfo_100d60300;
  if ((long *)*plVar5 != (long *)0x0) {
    puVar6 = (undefined *)(**(code **)(*(long *)*plVar5 + 0x10))();
  }
  if (((char *)(*(ulong *)(puVar6 + 8) & 0x7fffffffffffffff) !=
       "NSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEE") &&
     (iVar3 = _strcmp((char *)(*(ulong *)(puVar6 + 8) & 0x7fffffffffffffff),
                      "NSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEE"), iVar3 != 0)
     ) {
    local_b0 = (undefined ****)0x0;
    std::bad_cast::bad_cast((bad_cast *)&local_b0);
    local_b0 = (undefined ****)&PTR__bad_cast_100d880e8;
    FUN_1001499a0(&local_b0);
                    /* WARNING: Does not return */
    pcVar2 = (code *)SoftwareBreakpoint(1,0x1001539bc);
    (*pcVar2)();
  }
  lVar12 = *plVar5;
  uVar13 = (ulong)*(char *)(lVar12 + 0x1f);
  if ((long)uVar13 < 0) {
    uVar13 = *(ulong *)(lVar12 + 0x10);
    if (0x7ffffffffffffff7 < uVar13) {
                    /* WARNING: Subroutine does not return */
      FUN_100147bd8(&local_b0);
    }
    pvVar9 = *(void **)(lVar12 + 8);
    if (0x16 < uVar13) goto LAB_100153738;
LAB_10015370c:
    local_a0 = CONCAT17((char)uVar13,(undefined7)local_a0);
    pppppuVar7 = &local_b0;
    if (uVar13 != 0) goto LAB_100153760;
  }
  else {
    pvVar9 = (void *)(lVar12 + 8);
    if (uVar13 < 0x17) goto LAB_10015370c;
LAB_100153738:
    uVar1 = 0x19;
    if ((uVar13 | 7) != 0x17) {
      uVar1 = (uVar13 | 7) + 1;
    }
    pppppuVar7 = operator_new(uVar1);
    local_a0 = uVar1 | 0x8000000000000000;
    local_b0 = (undefined ****)pppppuVar7;
    uStack_a8 = uVar13;
LAB_100153760:
    _memmove(pppppuVar7,pvVar9,uVar13);
  }
  *(undefined1 *)((long)pppppuVar7 + uVar13) = 0;
  uStack_c8 = uStack_a8;
  local_d0 = local_b0;
  local_c0 = local_a0;
  if (uStack_d8 < 0) {
    operator_delete(local_e8);
    uVar13 = uStack_c8;
    if (-1 < (long)local_c0) {
      uVar13 = local_c0 >> 0x38;
    }
    if (uVar13 != 0) goto LAB_1001537c8;
LAB_100153a74:
    uVar14 = 0;
  }
  else {
    uVar13 = uStack_a8;
    if (-1 < (long)local_a0) {
      uVar13 = local_a0 >> 0x38;
    }
    if (uVar13 == 0) goto LAB_100153a74;
LAB_1001537c8:
    FUN_100295758(&local_f0,&local_d0);
    uStack_78 = 0;
    local_80 = 0;
    uStack_68 = 0;
    uStack_70 = 0;
    puStack_98 = (undefined8 *)0x0;
    local_a0 = 0;
    uStack_88 = 0;
    puStack_90 = (undefined8 *)0x0;
    uStack_a8 = 0;
    local_b0 = (undefined ****)0x0;
    local_60 = 0x400;
    local_58 = 0;
    local_50 = 0;
    puVar8 = operator_new(0x18);
    *puVar8 = 0x10000;
    pvVar9 = operator_new(1);
    puVar10 = _malloc(0x38);
    puVar8[1] = pvVar9;
    puVar8[2] = puVar10;
    puVar10[4] = 0;
    *puVar10 = puVar10 + 4;
    puVar10[1] = pvVar9;
    puVar10[5] = 0;
    puVar10[6] = 0;
    *(undefined1 *)(puVar10 + 3) = 1;
    puVar10[2] = 1;
    puStack_98 = puVar8;
    puStack_90 = puVar8;
    uVar4 = FUN_1002b143c(&local_f0,&local_b0);
    if (uVar4 != 0) {
      local_e0 = 0;
      uStack_d8 = 0;
      local_e8 = &local_e0;
      uVar11 = FUN_100153c20(&local_e8,"builtin-folders",param_2);
      uVar11 = FUN_100153c20(uVar11,"factory-packs",param_2 + 0x18);
      uVar11 = FUN_100153d64(uVar11,"user-library",param_2 + 0x30);
      uVar11 = FUN_100153c20(uVar11,"user-folders",param_2 + 0x60);
      uVar11 = FUN_100153d64(uVar11,"current-project",param_2 + 0x78);
      uVar11 = FUN_100153c20(uVar11,"managed-folders",param_2 + 0xa8);
      uVar11 = FUN_100153c20(uVar11,"places-only-managed-folders",param_2 + 0xc0);
      uVar11 = FUN_100153c20(uVar11,"legacy-packs",param_2 + 0xd8);
      uVar11 = FUN_100153d64(uVar11,"cloud-manager-folder",param_2 + 0xf0);
      uVar11 = FUN_100153d64(uVar11,"abl-factory-library",param_2 + 0x120);
      puVar8 = (undefined8 *)FUN_1002b1668(&local_b0,uVar11);
      FUN_100154078(&local_e8,local_e0);
    }
    uVar14 = (uint)puVar8;
    FUN_10014d918(&local_b0);
    if ((local_f0 != (int *)0x0) && (iVar3 = *local_f0, *local_f0 = iVar3 + -1, iVar3 + -1 == 0)) {
      FUN_100469e84();
    }
    if ((uVar4 & 1) == 0) goto LAB_100153a74;
  }
  if ((long)local_c0 < 0) {
    operator_delete(local_d0);
    if (*(long *)PTR____stack_chk_guard_100d60390 == local_48) {
LAB_10015396c:
      return uVar14 & 1;
    }
  }
  else if (*(long *)PTR____stack_chk_guard_100d60390 == local_48) goto LAB_10015396c;
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

