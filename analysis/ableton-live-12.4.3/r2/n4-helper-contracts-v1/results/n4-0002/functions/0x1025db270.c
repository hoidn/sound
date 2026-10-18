
undefined8 *
FUN_1025db270(undefined8 *param_1,undefined8 *param_2,long *param_3,long *param_4,undefined8 param_5
             )

{
  uint *puVar1;
  uint uVar2;
  uint *puVar3;
  uint *puVar4;
  int iVar5;
  void *pvVar6;
  long *plVar7;
  undefined8 uVar8;
  long lVar9;
  uint *puVar10;
  undefined1 auStack_f0 [8];
  long *local_e8;
  uint *local_e0;
  uint *puStack_d8;
  undefined8 uStack_d0;
  undefined8 *local_c8;
  undefined1 auStack_c0 [24];
  undefined1 auStack_a8 [8];
  long *local_a0;
  undefined8 *local_98;
  undefined8 *apuStack_90 [3];
  undefined **local_78;
  undefined8 *puStack_70;
  undefined ***local_60;
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_1064f8818;
  *param_1 = &PTR_thunk_FUN_1025dc834_1067e2c58;
  uVar8 = *param_2;
  *param_2 = 0;
  param_1[1] = uVar8;
  param_1[2] = 0;
  pvVar6 = operator_new(0x50);
  FUN_1025e4c64(pvVar6,0);
  param_1[3] = pvVar6;
  plVar7 = (long *)param_3[3];
  uVar8 = 0;
  if (plVar7 == (long *)0x0) {
LAB_1025db304:
    param_1[7] = uVar8;
  }
  else {
    if (plVar7 != param_3) {
      uVar8 = (**(code **)(*plVar7 + 0x10))();
      goto LAB_1025db304;
    }
    param_1[7] = param_1 + 4;
    (**(code **)(*(long *)param_3[3] + 0x18))((long *)param_3[3],param_1 + 4);
  }
  plVar7 = (long *)param_4[3];
  uVar8 = 0;
  if (plVar7 == (long *)0x0) {
LAB_1025db344:
    param_1[0xb] = uVar8;
  }
  else {
    if (plVar7 != param_4) {
      uVar8 = (**(code **)(*plVar7 + 0x10))();
      goto LAB_1025db344;
    }
    param_1[0xb] = param_1 + 8;
    (**(code **)(*(long *)param_4[3] + 0x18))((long *)param_4[3],param_1 + 8);
  }
  param_1[0xc] = param_5;
  FUN_1025db9fc(param_1[3],1);
  FUN_1025db9fc(param_1[3],2);
  FUN_1025db9fc(param_1[3],3);
  FUN_1025db9fc(param_1[3],4);
  FUN_1025db9fc(param_1[3],7);
  FUN_1025db9fc(param_1[3],5);
  FUN_1025db9fc(param_1[3],6);
  FUN_1025db9fc(param_1[3],8);
  FUN_1025db9fc(param_1[3],9);
  FUN_1025db9fc(param_1[3],10);
  FUN_1025e6af0(param_1[3],0,1,0);
  FUN_1025e6af0(param_1[3],1,2,1);
  FUN_1025e6af0(param_1[3],1,4,0x100004e20);
  FUN_1025e6af0(param_1[3],1,3,4);
  FUN_1025e6af0(param_1[3],1,7,3);
  FUN_1025e6af0(param_1[3],2,7,3);
  FUN_1025e6af0(param_1[3],2,4,2);
  FUN_1025e6af0(param_1[3],2,3,4);
  FUN_1025e6af0(param_1[3],2,6,0x10000ea60);
  FUN_1025e6af0(param_1[3],3,7,3);
  FUN_1025e6af0(param_1[3],3,4,2);
  FUN_1025e6af0(param_1[3],7,5,2);
  FUN_1025e6af0(param_1[3],7,6,"coa");
  FUN_1025e6af0(param_1[3],3,8,5);
  FUN_1025e6af0(param_1[3],8,9,2);
  FUN_1025e6af0(param_1[3],8,10,"coa");
  lVar9 = param_1[3];
  puStack_d8 = (uint *)0x0;
  local_e0 = (uint *)0x0;
  local_c8 = (undefined8 *)0x0;
  uStack_d0 = 0;
  local_98 = &DAT_1067e3a91;
  apuStack_90[0] = param_1;
  FUN_1025e8a0c(&local_98,&local_c8);
  if (((local_98 != (undefined8 *)0x0) && (((ulong)local_98 & 1) == 0)) &&
     ((code *)*local_98 != (code *)0x0)) {
    (*(code *)*local_98)(apuStack_90,apuStack_90,2);
  }
  FUN_1025e6f4c(auStack_a8,*(undefined8 *)(lVar9 + 0x30),&local_e0,0);
  if (local_a0 != (long *)0x0) {
    LOAcquire();
    iVar5 = *(int *)((long)local_a0 + 0xc);
    *(int *)((long)local_a0 + 0xc) = iVar5 + -1;
    LORelease();
    if (iVar5 == 1) {
      (**(code **)(*local_a0 + 0x18))();
    }
  }
  if (local_c8 != (undefined8 *)0x0) {
    if ((((ulong)local_c8 & 1) == 0) && ((code *)*local_c8 != (code *)0x0)) {
      (*(code *)*local_c8)(auStack_c0,auStack_c0,2);
    }
    local_c8 = (undefined8 *)0x0;
  }
  puVar4 = local_e0;
  puVar3 = puStack_d8;
  if (local_e0 != (uint *)0x0) {
    while (puVar3 != puVar4) {
      puVar10 = puVar3 + -6;
      uVar2 = *puVar10 ^ (int)*puVar10 >> 0x1f;
      if (uVar2 == 2) {
        puVar1 = puVar3 + -4;
        puVar3 = puVar10;
        if (*(long **)puVar1 != (long *)0x0) {
          (**(code **)(**(long **)puVar1 + 8))();
        }
      }
      else if (uVar2 == 1) {
        plVar7 = *(long **)(puVar3 + -2);
        puVar3 = puVar10;
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
        plVar7 = *(long **)(puVar3 + -2);
        puVar3 = puVar10;
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
    puStack_d8 = puVar4;
    operator_delete(local_e0);
  }
  local_78 = &PTR_FUN_1067e3ac0;
  puStack_70 = param_1;
  local_60 = &local_78;
  (**(code **)(*(long *)param_1[1] + 0x10))((long *)param_1[1],&local_78);
  if (local_60 == &local_78) {
    lVar9 = 0x20;
  }
  else {
    if (local_60 == (undefined ***)0x0) goto LAB_1025db6f8;
    lVar9 = 0x28;
  }
  (**(code **)((long)*local_60 + lVar9))();
LAB_1025db6f8:
  if (param_1[0xc] != 0) {
    lVar9 = param_1[3];
    puStack_d8 = (uint *)0x0;
    local_e0 = (uint *)0x0;
    local_c8 = (undefined8 *)0x0;
    uStack_d0 = 0;
    local_98 = &DAT_1067e3b91;
    apuStack_90[0] = param_1;
    FUN_1025e8a0c(&local_98,&local_c8);
    if (((local_98 != (undefined8 *)0x0) && (((ulong)local_98 & 1) == 0)) &&
       ((code *)*local_98 != (code *)0x0)) {
      (*(code *)*local_98)(apuStack_90,apuStack_90,2);
    }
    FUN_1025e6f4c(auStack_f0,*(undefined8 *)(lVar9 + 0x30),&local_e0,0);
    if (local_e8 != (long *)0x0) {
      LOAcquire();
      iVar5 = *(int *)((long)local_e8 + 0xc);
      *(int *)((long)local_e8 + 0xc) = iVar5 + -1;
      LORelease();
      if (iVar5 == 1) {
        (**(code **)(*local_e8 + 0x18))();
      }
    }
    if (local_c8 != (undefined8 *)0x0) {
      if ((((ulong)local_c8 & 1) == 0) && ((code *)*local_c8 != (code *)0x0)) {
        (*(code *)*local_c8)(auStack_c0,auStack_c0,2);
      }
      local_c8 = (undefined8 *)0x0;
    }
    puVar4 = local_e0;
    puVar3 = puStack_d8;
    if (local_e0 != (uint *)0x0) {
      while (puVar3 != puVar4) {
        puVar10 = puVar3 + -6;
        uVar2 = *puVar10 ^ (int)*puVar10 >> 0x1f;
        if (uVar2 == 2) {
          puVar1 = puVar3 + -4;
          puVar3 = puVar10;
          if (*(long **)puVar1 != (long *)0x0) {
            (**(code **)(**(long **)puVar1 + 8))();
          }
        }
        else if (uVar2 == 1) {
          plVar7 = *(long **)(puVar3 + -2);
          puVar3 = puVar10;
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
          plVar7 = *(long **)(puVar3 + -2);
          puVar3 = puVar10;
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
      puStack_d8 = puVar4;
      operator_delete(local_e0);
    }
  }
  if (*(long *)PTR____stack_chk_guard_1064f8818 != local_58) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return param_1;
}

