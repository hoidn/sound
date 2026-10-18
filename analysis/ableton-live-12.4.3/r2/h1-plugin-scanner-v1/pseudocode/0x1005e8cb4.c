
/* WARNING: Removing unreachable block (ram,0x0001005e8e70) */
/* WARNING: Removing unreachable block (ram,0x0001005e8e8c) */
/* WARNING: Removing unreachable block (ram,0x0001005e9030) */
/* WARNING: Removing unreachable block (ram,0x0001005e8f1c) */
/* WARNING: Removing unreachable block (ram,0x0001005e8f30) */
/* WARNING: Removing unreachable block (ram,0x0001005e8f6c) */

void FUN_1005e8cb4(undefined8 *param_1,long *param_2)

{
  long lVar1;
  void *pvVar2;
  undefined8 *puVar3;
  long lVar4;
  int iVar5;
  int iVar6;
  undefined8 uVar7;
  ulong uVar8;
  undefined8 uVar9;
  undefined8 uVar10;
  long *plVar11;
  ulong extraout_x1;
  long lVar12;
  void *pvVar13;
  void *local_110;
  long *plStack_108;
  long local_100;
  int local_f8 [2];
  undefined8 local_f0;
  void *local_e8 [2];
  char local_d1;
  long local_d0;
  long *local_c8;
  void *local_c0;
  undefined8 uStack_b8;
  undefined8 *local_b0;
  undefined8 uStack_a8;
  undefined4 local_a0;
  int local_90 [2];
  undefined8 local_88;
  void *local_80;
  long *plStack_78;
  undefined7 local_70;
  undefined1 uStack_69;
  
  param_1[1] = 0;
  *param_1 = 0;
  param_1[3] = 0;
  param_1[2] = 0;
  *(undefined4 *)(param_1 + 4) = 0x3f800000;
  lVar12 = *param_2;
  lVar1 = param_2[1];
  if (lVar12 != lVar1) {
    uVar7 = std::system_category();
    do {
      local_90[0] = 0;
      uStack_b8 = 0;
      local_c0 = (void *)0x0;
      uStack_a8 = 0;
      local_b0 = (undefined8 *)0x0;
      local_a0 = 0x3f800000;
      local_88 = uVar7;
      FUN_100661bb0(&local_d0,lVar12,5,local_90);
      while( true ) {
        local_80 = (void *)0x0;
        plStack_78 = (long *)0x0;
        uVar8 = FUN_100661edc(&local_d0,&local_80);
        if (plStack_78 != (long *)0x0) {
          LOAcquire();
          lVar4 = plStack_78[1];
          plStack_78[1] = lVar4 + -1;
          LORelease();
          if (lVar4 == 0) {
            (**(code **)(*plStack_78 + 0x10))(plStack_78);
            std::__shared_weak_count::__release_weak();
          }
        }
        if ((uVar8 & 1) == 0) break;
        FUN_100661674(local_d0);
        uVar9 = FUN_1006604c0();
        FUN_100674264(&local_80,uVar9,local_90);
        FUN_10067ac78(local_e8,&local_80);
        if (local_90[0] == 0) {
          local_f8[0] = 0;
          local_f0 = uVar7;
          plVar11 = (long *)FUN_100661674(local_d0);
          plVar11 = (long *)*plVar11;
          if (plVar11 == (long *)0x0) {
            uVar9 = 0xffff00000000;
          }
          else {
            uVar9 = (**(code **)(*plVar11 + 0x28))(plVar11,local_f8);
          }
          iVar5 = FUN_10066f1e4(uVar9);
          if ((iVar5 != 0) && (FUN_1005e64f0(&local_c0,local_e8,local_e8), (extraout_x1 & 1) == 0))
          {
            *(undefined1 *)(local_d0 + 0x28) = 0;
          }
          FUN_1006c4724(&local_80,local_e8);
          plStack_108 = plStack_78;
          local_110 = local_80;
          local_100 = CONCAT17(uStack_69,local_70);
          local_80 = (void *)CONCAT26(local_80._6_2_,0x337473762e);
          uStack_69 = 5;
          iVar6 = FUN_100679138(&local_110,&local_80);
          if (local_100 < 0) {
            operator_delete(local_110);
          }
          if (iVar6 == 0) {
            if (iVar5 != 0) {
              *(undefined1 *)(local_d0 + 0x28) = 0;
            }
            if (local_f8[0] == 0) {
              FUN_1005e64f0(param_1,local_e8,local_e8);
            }
          }
        }
        else {
          uVar9 = std::chrono::system_clock::now();
          FUN_1006a290c(&local_110,3,uVar9);
          iVar5 = FUN_10069f1d8(&local_110);
          if (iVar5 != 0) {
            uVar9 = FUN_10069c398(&local_110,"Can\'t resolve path: ");
            FUN_100661674(local_d0);
            uVar10 = FUN_1006604c0();
            uVar9 = FUN_10013300c(uVar9,uVar10);
            uVar9 = FUN_10069c398(uVar9," (");
            std::error_code::message();
            uVar9 = FUN_10069d278(uVar9,&local_80);
            FUN_10069c398(uVar9,")");
          }
          thunk_FUN_10069bf04(&local_110);
          local_90[0] = 0;
          local_88 = uVar7;
        }
        if (local_d1 < '\0') {
          operator_delete(local_e8[0]);
        }
        FUN_100661d2c(&local_d0,local_90);
      }
      if (local_c8 != (long *)0x0) {
        LOAcquire();
        lVar4 = local_c8[1];
        local_c8[1] = lVar4 + -1;
        LORelease();
        if (lVar4 == 0) {
          (**(code **)(*local_c8 + 0x10))(local_c8);
          std::__shared_weak_count::__release_weak();
        }
      }
      pvVar2 = local_c0;
      puVar3 = local_b0;
      if (local_90[0] != 0) {
        uVar9 = std::chrono::system_clock::now();
        FUN_1006a290c(local_e8,4,uVar9);
        iVar5 = FUN_10069f1d8(local_e8);
        if (iVar5 != 0) {
          uVar9 = FUN_10069c398(local_e8,"Reading directory failed: ");
          std::error_code::message();
          FUN_10069d278(uVar9,&local_80);
        }
        thunk_FUN_10069bf04(local_e8);
        pvVar2 = local_c0;
        puVar3 = local_b0;
      }
      while (puVar3 != (void *)0x0) {
        pvVar13 = (void *)*puVar3;
        local_c0 = pvVar2;
        if (*(char *)((long)puVar3 + 0x27) < '\0') {
          operator_delete((void *)puVar3[2]);
        }
        operator_delete(puVar3);
        pvVar2 = local_c0;
        puVar3 = pvVar13;
      }
      local_c0 = (void *)0x0;
      if (pvVar2 != (void *)0x0) {
        operator_delete(pvVar2);
      }
      lVar12 = lVar12 + 0x18;
    } while (lVar12 != lVar1);
  }
  return;
}

