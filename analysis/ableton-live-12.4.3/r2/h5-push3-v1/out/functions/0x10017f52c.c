// 0x10017f52c FUN_10017f52c state=exported role=ControlledProcessSocket<Watchdog> ctor
// source chunk chunk-00065.jsonl; code_sha256=358955504a391141dd70f72ea78c1a75e270928f030e2adc7515a6369b6673e4

undefined8 * FUN_10017f52c(undefined8 *param_1,undefined8 *param_2,undefined8 param_3,long param_4)

{
  uint *puVar1;
  uint uVar2;
  uint *puVar3;
  uint *puVar4;
  int iVar5;
  long *plVar6;
  undefined8 uVar7;
  long lVar8;
  uint *puVar9;
  undefined1 auStack_c0 [8];
  long *local_b8;
  uint *local_b0;
  uint *puStack_a8;
  undefined8 uStack_a0;
  undefined8 *local_98;
  undefined1 auStack_90 [32];
  undefined1 auStack_70 [8];
  long *local_68;
  undefined8 *local_60;
  undefined8 *apuStack_58 [3];
  
  *param_1 = &PTR_FUN_101bcee60;
  thunk_FUN_1006678a0(param_1 + 1);
  plVar6 = (long *)(param_4 + 0x18);
  lVar8 = *plVar6;
  if (lVar8 == 0) {
    plVar6 = param_1 + 0x1b;
  }
  else {
    if (lVar8 == param_4) {
      param_1[0x1b] = param_1 + 0x18;
      (**(code **)(*(long *)*plVar6 + 0x18))((long *)*plVar6,param_1 + 0x18);
      goto LAB_10017f5b0;
    }
    param_1[0x1b] = lVar8;
  }
  *plVar6 = 0;
LAB_10017f5b0:
  uVar7 = *param_2;
  *param_2 = 0;
  param_1[0x1c] = uVar7;
  param_1[0x1d] = 0;
  *(undefined1 *)(param_1 + 0x1e) = 0;
  FUN_100668400(param_1 + 1,param_3);
  puStack_a8 = (uint *)0x0;
  local_b0 = (uint *)0x0;
  local_98 = (undefined8 *)0x0;
  uStack_a0 = 0;
  local_60 = (undefined8 *)((ulong)PTR_stored_vtable_101ba0f20 | 1);
  apuStack_58[0] = param_1;
  FUN_10017fddc(&local_60,&local_98);
  if (((local_60 != (undefined8 *)0x0) && (((ulong)local_60 & 1) == 0)) &&
     ((code *)*local_60 != (code *)0x0)) {
    (*(code *)*local_60)(apuStack_58,apuStack_58,2);
  }
  FUN_100668668(auStack_70,param_1 + 1,&local_b0);
  if (local_68 != (long *)0x0) {
    LOAcquire();
    iVar5 = *(int *)((long)local_68 + 0xc);
    *(int *)((long)local_68 + 0xc) = iVar5 + -1;
    LORelease();
    if (iVar5 == 1) {
      (**(code **)(*local_68 + 0x18))();
    }
  }
  if (local_98 != (undefined8 *)0x0) {
    if ((((ulong)local_98 & 1) == 0) && ((code *)*local_98 != (code *)0x0)) {
      (*(code *)*local_98)(auStack_90,auStack_90,2);
    }
    local_98 = (undefined8 *)0x0;
  }
  puVar4 = local_b0;
  puVar3 = puStack_a8;
  if (local_b0 != (uint *)0x0) {
    while (puVar3 != puVar4) {
      puVar9 = puVar3 + -6;
      uVar2 = *puVar9 ^ (int)*puVar9 >> 0x1f;
      if (uVar2 == 2) {
        puVar1 = puVar3 + -4;
        puVar3 = puVar9;
        if (*(long **)puVar1 != (long *)0x0) {
          (**(code **)(**(long **)puVar1 + 8))();
        }
      }
      else if (uVar2 == 1) {
        plVar6 = *(long **)(puVar3 + -2);
        puVar3 = puVar9;
        if (plVar6 != (long *)0x0) {
          LOAcquire();
          iVar5 = *(int *)((long)plVar6 + 0xc);
          *(int *)((long)plVar6 + 0xc) = iVar5 + -1;
          LORelease();
          if (iVar5 == 1) {
            (**(code **)(*plVar6 + 0x18))();
          }
        }
      }
      else {
        plVar6 = *(long **)(puVar3 + -2);
        puVar3 = puVar9;
        if (plVar6 != (long *)0x0) {
          LOAcquire();
          iVar5 = *(int *)((long)plVar6 + 0xc);
          *(int *)((long)plVar6 + 0xc) = iVar5 + -1;
          LORelease();
          if (iVar5 == 1) {
            (**(code **)(*plVar6 + 0x18))();
          }
        }
      }
    }
    puStack_a8 = puVar4;
    operator_delete(local_b0);
  }
  puStack_a8 = (uint *)0x0;
  local_b0 = (uint *)0x0;
  local_98 = (undefined8 *)0x0;
  uStack_a0 = 0;
  local_60 = (undefined8 *)((ulong)PTR_stored_vtable_101ba0f18 | 1);
  apuStack_58[0] = param_1;
  FUN_10017fddc(&local_60,&local_98);
  if (((local_60 != (undefined8 *)0x0) && (((ulong)local_60 & 1) == 0)) &&
     ((code *)*local_60 != (code *)0x0)) {
    (*(code *)*local_60)(apuStack_58,apuStack_58,2);
  }
  FUN_10066865c(auStack_c0,param_1 + 1,&local_b0);
  if (local_b8 != (long *)0x0) {
    LOAcquire();
    iVar5 = *(int *)((long)local_b8 + 0xc);
    *(int *)((long)local_b8 + 0xc) = iVar5 + -1;
    LORelease();
    if (iVar5 == 1) {
      (**(code **)(*local_b8 + 0x18))();
    }
  }
  if (local_98 != (undefined8 *)0x0) {
    if ((((ulong)local_98 & 1) == 0) && ((code *)*local_98 != (code *)0x0)) {
      (*(code *)*local_98)(auStack_90,auStack_90,2);
    }
    local_98 = (undefined8 *)0x0;
  }
  puVar4 = local_b0;
  puVar3 = puStack_a8;
  if (local_b0 != (uint *)0x0) {
    while (puVar3 != puVar4) {
      puVar9 = puVar3 + -6;
      uVar2 = *puVar9 ^ (int)*puVar9 >> 0x1f;
      if (uVar2 == 2) {
        puVar1 = puVar3 + -4;
        puVar3 = puVar9;
        if (*(long **)puVar1 != (long *)0x0) {
          (**(code **)(**(long **)puVar1 + 8))();
        }
      }
      else if (uVar2 == 1) {
        plVar6 = *(long **)(puVar3 + -2);
        puVar3 = puVar9;
        if (plVar6 != (long *)0x0) {
          LOAcquire();
          iVar5 = *(int *)((long)plVar6 + 0xc);
          *(int *)((long)plVar6 + 0xc) = iVar5 + -1;
          LORelease();
          if (iVar5 == 1) {
            (**(code **)(*plVar6 + 0x18))();
          }
        }
      }
      else {
        plVar6 = *(long **)(puVar3 + -2);
        puVar3 = puVar9;
        if (plVar6 != (long *)0x0) {
          LOAcquire();
          iVar5 = *(int *)((long)plVar6 + 0xc);
          *(int *)((long)plVar6 + 0xc) = iVar5 + -1;
          LORelease();
          if (iVar5 == 1) {
            (**(code **)(*plVar6 + 0x18))();
          }
        }
      }
    }
    puStack_a8 = puVar4;
    operator_delete(local_b0);
  }
  return param_1;
}

