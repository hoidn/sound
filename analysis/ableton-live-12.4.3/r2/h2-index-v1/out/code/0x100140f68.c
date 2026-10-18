// 0x100140f68 FUN_100140f68 state=exported-with-warnings body_bytes=672 warnings=2 chunk=chunk-00052.jsonl

void FUN_100140f68(long param_1,undefined8 param_2,undefined8 param_3,undefined8 *param_4,
                  undefined8 param_5)

{
  undefined8 *puVar1;
  int iVar2;
  ulong uVar3;
  code *pcVar4;
  undefined8 *puVar5;
  void *pvVar6;
  undefined8 *puVar7;
  undefined8 uVar8;
  int *piVar9;
  undefined8 *local_118;
  undefined8 *local_110;
  long local_108;
  undefined8 *local_100;
  undefined8 *puStack_f8;
  int *local_f0;
  int *local_e8;
  undefined8 **local_e0;
  undefined1 local_d8;
  undefined8 local_d0;
  undefined8 uStack_c8;
  undefined8 local_c0;
  undefined8 *puStack_b8;
  undefined8 *puStack_b0;
  undefined8 uStack_a8;
  undefined8 local_a0;
  undefined8 uStack_98;
  undefined8 uStack_90;
  undefined8 uStack_88;
  undefined8 local_80;
  undefined4 local_78;
  undefined8 local_70;
  long local_68;
  
  local_68 = *(long *)PTR____stack_chk_guard_100d60390;
  uStack_98 = 0;
  local_a0 = 0;
  uStack_88 = 0;
  uStack_90 = 0;
  puStack_b8 = (undefined8 *)0x0;
  local_c0 = 0;
  uStack_a8 = 0;
  puStack_b0 = (undefined8 *)0x0;
  uStack_c8 = 0;
  local_d0 = 0;
  local_80 = 0x400;
  local_78 = 0;
  local_70 = 0;
  puVar5 = operator_new(0x18);
  *puVar5 = 0x10000;
  pvVar6 = operator_new(1);
  puVar7 = _malloc(0x38);
  puVar5[1] = pvVar6;
  puVar5[2] = puVar7;
  puVar7[4] = 0;
  *puVar7 = puVar7 + 4;
  puVar7[1] = pvVar6;
  puVar7[5] = 0;
  puVar7[6] = 0;
  *(undefined1 *)(puVar7 + 3) = 1;
  puVar7[2] = 1;
  puVar7 = *(undefined8 **)(param_1 + 0x20);
  puStack_b8 = puVar5;
  puStack_b0 = puVar5;
  FUN_10044ca6c(&local_e8,L"FinishedActivity");
  local_100 = &local_d0;
  if (local_c0._6_2_ != 3) {
    uStack_c8 = 0;
    local_d0 = 0;
    local_c0 = 0x3000000000000;
  }
  puStack_f8 = local_100;
  uVar8 = FUN_10015748c(&local_100,"EventId",param_2);
  uVar8 = FUN_100157698(uVar8,"NeedsRefresh",param_3);
  local_118 = (undefined8 *)0x0;
  local_110 = (undefined8 *)0x0;
  local_108 = 0;
  puVar5 = (undefined8 *)*param_4;
  puVar1 = (undefined8 *)param_4[1];
  local_e0 = &local_118;
  local_d8 = 0;
  uVar3 = (long)puVar1 - (long)puVar5;
  if (uVar3 != 0) {
    if ((long)uVar3 < 0) {
      FUN_1001515fc(&local_118);
                    /* WARNING: Does not return */
      pcVar4 = (code *)SoftwareBreakpoint(1,0x100141208);
      (*pcVar4)();
    }
    local_118 = operator_new(uVar3);
    local_108 = (long)local_118 + uVar3;
    local_110 = local_118;
    do {
      piVar9 = (int *)*puVar5;
      *local_110 = piVar9;
      if (piVar9 != (int *)0x0) {
        *piVar9 = *piVar9 + 1;
      }
      puVar5 = puVar5 + 1;
      local_110 = local_110 + 1;
    } while (puVar5 != puVar1);
  }
  uVar8 = FUN_10015789c(uVar8,"UpdatedLocations",&local_118);
  puVar5 = (undefined8 *)FUN_100157698(uVar8,"RefreshCategories",param_5);
  FUN_1002b1378(&local_f0,*puVar5,0);
  (**(code **)*puVar7)(puVar7,&local_e8,&local_f0);
  if ((local_f0 != (int *)0x0) && (iVar2 = *local_f0, *local_f0 = iVar2 + -1, iVar2 + -1 == 0)) {
    FUN_100469e84();
  }
  puVar7 = local_118;
  puVar5 = local_110;
  if (local_118 != (undefined8 *)0x0) {
    while (puVar5 != puVar7) {
      puVar5 = puVar5 + -1;
      piVar9 = (int *)*puVar5;
      if ((piVar9 != (int *)0x0) && (iVar2 = *piVar9, *piVar9 = iVar2 + -1, iVar2 + -1 == 0)) {
        FUN_100469e84();
      }
    }
    local_110 = puVar7;
    operator_delete(local_118);
  }
  if ((local_e8 != (int *)0x0) && (iVar2 = *local_e8, *local_e8 = iVar2 + -1, iVar2 + -1 == 0)) {
    FUN_100469e84();
  }
  FUN_10014d918(&local_d0);
  if (*(long *)PTR____stack_chk_guard_100d60390 != local_68) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}

