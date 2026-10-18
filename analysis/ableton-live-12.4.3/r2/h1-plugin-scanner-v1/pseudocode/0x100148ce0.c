
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

uint * FUN_100148ce0(uint *param_1)

{
  uint *puVar1;
  uint uVar2;
  undefined8 uVar3;
  uint *puVar4;
  int iVar5;
  void *pvVar6;
  long *plVar7;
  uint *puVar8;
  uint *puVar9;
  uint *local_b0;
  uint *puStack_a8;
  undefined8 uStack_a0;
  undefined8 *local_98;
  undefined1 auStack_90 [32];
  undefined1 auStack_70 [8];
  long *local_68;
  undefined8 *local_60;
  uint *apuStack_58 [3];
  
  uVar3 = _DAT_1009a8ff0;
  *(undefined8 *)(param_1 + 2) = _UNK_1009a8ff8;
  *(undefined8 *)param_1 = uVar3;
  *(undefined8 *)(param_1 + 4) = DAT_1009a9000;
  FUN_10014a2b4(param_1 + 6,0);
  param_1[0x1a] = 0;
  *(undefined ***)(param_1 + 0x1c) = &PTR_FUN_100b44618;
  pvVar6 = operator_new(0x28);
  FUN_10014bdf4(pvVar6,&local_b0,&local_60);
  *(void **)(param_1 + 0x1e) = pvVar6;
  puVar8 = param_1 + 0x20;
  puVar8[0] = 0;
  puVar8[1] = 0;
  FUN_10014d19c(param_1 + 0x1e,pvVar6,puVar8);
  *(undefined ***)(param_1 + 0x22) = &PTR_FUN_100b44618;
  pvVar6 = operator_new(0x28);
  FUN_10014bdf4(pvVar6,&local_b0,&local_60);
  *(void **)(param_1 + 0x24) = pvVar6;
  puVar8 = param_1 + 0x26;
  puVar8[0] = 0;
  puVar8[1] = 0;
  FUN_10014d19c(param_1 + 0x24,pvVar6,puVar8);
  *(undefined ***)(param_1 + 0x28) = &PTR_FUN_100b44618;
  pvVar6 = operator_new(0x28);
  FUN_10014bdf4(pvVar6,&local_b0,&local_60);
  *(void **)(param_1 + 0x2a) = pvVar6;
  puVar8 = param_1 + 0x2c;
  puVar8[0] = 0;
  puVar8[1] = 0;
  FUN_10014d19c(param_1 + 0x2a,pvVar6,puVar8);
  FUN_1001492d8(param_1 + 6,1);
  FUN_1001492d8(param_1 + 6,2);
  FUN_1001492d8(param_1 + 6,6);
  FUN_1001492d8(param_1 + 6,3);
  FUN_1001492d8(param_1 + 6,4);
  FUN_1001492d8(param_1 + 6,5);
  FUN_1001492d8(param_1 + 6,7);
  FUN_1001492d8(param_1 + 6,8);
  FUN_10014d7c0(param_1 + 6,0,1,0);
  FUN_10014d7c0(param_1 + 6,0,2,3);
  FUN_10014d7c0(param_1 + 6,1,3,3);
  FUN_10014d7c0(param_1 + 6,1,7,(ulong)param_1[2] | 0x100000000);
  FUN_10014d7c0(param_1 + 6,2,3,0);
  FUN_10014d7c0(param_1 + 6,2,7,(ulong)param_1[1] | 0x100000000);
  FUN_10014d7c0(param_1 + 6,3,6,2);
  FUN_10014d7c0(param_1 + 6,3,4,(ulong)param_1[3] | 0x100000000);
  FUN_10014d7c0(param_1 + 6,4,6,2);
  FUN_10014d7c0(param_1 + 6,4,5,(ulong)param_1[4] | 0x100000000);
  FUN_10014d7c0(param_1 + 6,5,6,2);
  FUN_10014d7c0(param_1 + 6,5,7,(ulong)param_1[5] | 0x100000000);
  FUN_10014d7c0(param_1 + 6,0,7,(ulong)param_1[1] | 0x100000000);
  FUN_10014d7c0(param_1 + 6,6,6,1);
  FUN_10014d7c0(param_1 + 6,6,7,(ulong)*param_1 | 0x100000000);
  FUN_10014d7c0(param_1 + 6,0,7,4);
  FUN_10014d7c0(param_1 + 6,3,7,4);
  FUN_10014d7c0(param_1 + 6,4,7,4);
  FUN_10014d7c0(param_1 + 6,5,7,4);
  FUN_10014d7c0(param_1 + 6,6,8,4);
  puStack_a8 = (uint *)0x0;
  local_b0 = (uint *)0x0;
  local_98 = (undefined8 *)0x0;
  uStack_a0 = 0;
  local_60 = &DAT_100b44fb9;
  apuStack_58[0] = param_1;
  FUN_1001502f0(&local_60,&local_98);
  if (((local_60 != (undefined8 *)0x0) && (((ulong)local_60 & 1) == 0)) &&
     ((code *)*local_60 != (code *)0x0)) {
    (*(code *)*local_60)(apuStack_58,apuStack_58,2);
  }
  FUN_10014dc1c(auStack_70,*(undefined8 *)(param_1 + 0x12),&local_b0,0);
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
  puVar8 = puStack_a8;
  if (local_b0 != (uint *)0x0) {
    while (puVar8 != puVar4) {
      puVar9 = puVar8 + -6;
      uVar2 = *puVar9 ^ (int)*puVar9 >> 0x1f;
      if (uVar2 == 2) {
        puVar1 = puVar8 + -4;
        puVar8 = puVar9;
        if (*(long **)puVar1 != (long *)0x0) {
          (**(code **)(**(long **)puVar1 + 8))();
        }
      }
      else if (uVar2 == 1) {
        plVar7 = *(long **)(puVar8 + -2);
        puVar8 = puVar9;
        if (plVar7 != (long *)0x0) {
          LOAcquire();
          iVar5 = *(int *)((long)plVar7 + 0xc);
          *(int *)((long)plVar7 + 0xc) = iVar5 + -1;
          LORelease();
          if (iVar5 == 1) {
            (**(code **)(*plVar7 + 0x18))();
          }
        }
      }
      else {
        plVar7 = *(long **)(puVar8 + -2);
        puVar8 = puVar9;
        if (plVar7 != (long *)0x0) {
          LOAcquire();
          iVar5 = *(int *)((long)plVar7 + 0xc);
          *(int *)((long)plVar7 + 0xc) = iVar5 + -1;
          LORelease();
          if (iVar5 == 1) {
            (**(code **)(*plVar7 + 0x18))();
          }
        }
      }
    }
    puStack_a8 = puVar4;
    operator_delete(local_b0);
  }
  return param_1;
}

