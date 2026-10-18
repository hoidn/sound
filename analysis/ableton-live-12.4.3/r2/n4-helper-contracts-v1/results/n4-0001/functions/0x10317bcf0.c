
/* WARNING: Removing unreachable block (ram,0x00010317c2c4) */
/* WARNING: Removing unreachable block (ram,0x00010317c134) */
/* WARNING: Removing unreachable block (ram,0x00010317c100) */
/* WARNING: Removing unreachable block (ram,0x00010317c144) */
/* WARNING: Removing unreachable block (ram,0x00010317c2f0) */

void FUN_10317bcf0(long param_1,int param_2)

{
  int iVar1;
  long *plVar2;
  int *piVar3;
  long lVar4;
  undefined8 *puVar5;
  undefined8 uVar6;
  void *local_120;
  void *pvStack_118;
  undefined8 local_110;
  undefined8 *local_100;
  long *local_f8;
  void *local_f0;
  void *pvStack_e8;
  undefined8 local_e0;
  undefined8 *local_d0;
  long *local_c8;
  long *local_c0;
  long *local_b8;
  int *local_b0;
  undefined **local_a8;
  long lStack_a0;
  undefined ***local_90;
  undefined **local_88;
  long lStack_80;
  undefined ***local_70;
  long *local_68;
  long *local_60;
  undefined1 local_51;
  undefined4 local_50;
  undefined3 uStack_4c;
  undefined1 uStack_49;
  undefined1 local_39;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_1064f8818;
  if (param_2 - 5U < 2) {
    if (*(long *)PTR____stack_chk_guard_1064f8818 == local_38) {
      FUN_10317c634(param_1);
      return;
    }
    goto LAB_10317c3cc;
  }
  if (param_2 == 4) {
    if (*(int *)(param_1 + 200) == 2) {
      uVar6 = std::chrono::system_clock::now();
      FUN_103f3ffec(&local_68,2,uVar6);
      iVar1 = FUN_103f3c8b8(&local_68);
      if (iVar1 != 0) {
        FUN_103f39a78(&local_68,"Plugins: scanner process finished a chunk of work.  Continue");
      }
      thunk_FUN_103f395e4(&local_68);
      *(undefined1 *)(param_1 + 0xcc) = 0;
      FUN_103179e68(param_1);
    }
    else if (*(int *)(param_1 + 200) == 0) {
      uVar6 = std::chrono::system_clock::now();
      FUN_103f3ffec(&local_68,2,uVar6);
      iVar1 = FUN_103f3c8b8(&local_68);
      if (iVar1 != 0) {
        FUN_103f39a78(&local_68,"Plugins: scanner process stopped prematurely.  Restart");
      }
      thunk_FUN_103f395e4(&local_68);
      *(undefined1 *)(param_1 + 0xcc) = 0;
      FUN_103179e68(param_1);
    }
    else {
      uVar6 = std::chrono::system_clock::now();
      FUN_103f3ffec(&local_68,2,uVar6);
      iVar1 = FUN_103f3c8b8(&local_68);
      if (iVar1 != 0) {
        FUN_103f39a78(&local_68,"Plugins: scanner process stopped");
      }
      thunk_FUN_103f395e4(&local_68);
      FUN_10317c634(param_1);
    }
  }
  else if (param_2 == 3) {
    plVar2 = operator_new(0x38);
    local_68 = *(long **)(param_1 + 0x80);
    if (local_68 != (long *)0x0) {
      *(int *)(local_68 + 1) = (int)local_68[1] + 1;
    }
    thunk_FUN_1025dd66c(plVar2,&local_68);
    if ((local_68 != (long *)0x0) &&
       (iVar1 = (int)local_68[1] + -1, *(int *)(local_68 + 1) = iVar1, iVar1 == 0)) {
      FUN_10128eea0();
    }
    piVar3 = (int *)FUN_1012d9850(0x68);
    local_68 = plVar2;
    thunk_FUN_1015a3368(piVar3,&local_68,"live->plugin-scanner");
    plVar2 = local_68;
    if (piVar3 != (int *)0x0) {
      piVar3[2] = piVar3[2] + 1;
    }
    local_68 = (long *)0x0;
    local_b0 = piVar3;
    if (plVar2 != (long *)0x0) {
      (**(code **)(*plVar2 + 8))();
    }
    plVar2 = (long *)0x0;
    if (piVar3 != (int *)0x0) {
      plVar2 = (long *)(piVar3 + 6);
    }
    *(long **)(param_1 + 0x90) = plVar2;
    lVar4 = *(long *)(param_1 + 0x88);
    if ((lVar4 != 0) && (iVar1 = *(int *)(lVar4 + 8) + -1, *(int *)(lVar4 + 8) = iVar1, iVar1 == 0))
    {
      FUN_10128eea0();
      plVar2 = *(long **)(param_1 + 0x90);
    }
    *(int **)(param_1 + 0x88) = piVar3;
    FUN_101427680(&local_b0,"scan");
    local_b8 = operator_new(0x40);
    local_b8[2] = 0;
    local_c0 = local_b8 + 3;
    *local_c0 = (long)&PTR_FUN_106592870;
    *local_b8 = (long)&PTR_FUN_106592790;
    local_b8[1] = 0;
    local_b8[4] = (long)&PTR_FUN_1068d8780;
    local_b8[7] = (long)(local_b8 + 4);
    local_b8[5] = param_1;
    local_68 = (long *)0x0;
    local_60 = (long *)0x0;
    (**(code **)(*plVar2 + 8))(plVar2,&local_b0,&local_c0);
    if (local_b8 != (long *)0x0) {
      LOAcquire();
      lVar4 = local_b8[1];
      local_b8[1] = lVar4 + -1;
      LORelease();
      if (lVar4 == 0) {
        (**(code **)(*local_b8 + 0x10))(local_b8);
        std::__shared_weak_count::__release_weak();
      }
    }
    if (local_60 != (long *)0x0) {
      LOAcquire();
      lVar4 = local_60[1];
      local_60[1] = lVar4 + -1;
      LORelease();
      if (lVar4 == 0) {
        (**(code **)(*local_60 + 0x10))(local_60);
        std::__shared_weak_count::__release_weak();
      }
    }
    if ((local_b0 != (int *)0x0) && (iVar1 = *local_b0, *local_b0 = iVar1 + -1, iVar1 + -1 == 0)) {
      FUN_101449efc();
    }
    plVar2 = *(long **)(param_1 + 0x90);
    FUN_101427680(&local_b0,"update");
    puVar5 = operator_new(0x40);
    local_51 = 5;
    local_68 = (long *)CONCAT26(local_68._6_2_,0x6c61746f74);
    local_39 = 7;
    local_50 = 0x72727563;
    uStack_4c = 0x746e65;
    uStack_49 = 0;
    FUN_100261120(&local_f0,&local_68,2);
    local_88 = &PTR_FUN_1068d8800;
    local_70 = &local_88;
    *puVar5 = &PTR_FUN_1065e2958;
    puVar5[2] = pvStack_e8;
    puVar5[1] = local_f0;
    puVar5[3] = local_e0;
    local_f0 = (void *)0x0;
    pvStack_e8 = (void *)0x0;
    local_e0 = 0;
    puVar5[4] = &PTR_FUN_1068d8800;
    puVar5[7] = puVar5 + 4;
    puVar5[5] = param_1;
    local_d0 = puVar5;
    lStack_80 = param_1;
    local_c8 = operator_new(0x20);
    *local_c8 = (long)&PTR____shared_weak_count_1065e2998;
    local_c8[1] = 0;
    local_c8[2] = 0;
    local_c8[3] = (long)puVar5;
    (**(code **)(*plVar2 + 8))(plVar2,&local_b0,&local_d0);
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
    if (local_70 == &local_88) {
      lVar4 = 0x20;
LAB_10317c0c4:
      (**(code **)((long)*local_70 + lVar4))();
    }
    else if (local_70 != (undefined ***)0x0) {
      lVar4 = 0x28;
      goto LAB_10317c0c4;
    }
    if (local_f0 != (void *)0x0) {
      for (; pvStack_e8 != local_f0; pvStack_e8 = (void *)((long)pvStack_e8 + -0x18)) {
      }
      pvStack_e8 = local_f0;
      operator_delete(local_f0);
    }
    if ((local_b0 != (int *)0x0) && (iVar1 = *local_b0, *local_b0 = iVar1 + -1, iVar1 + -1 == 0)) {
      FUN_101449efc();
    }
    plVar2 = *(long **)(param_1 + 0x90);
    FUN_101427680(&local_b0,"current-plugin");
    puVar5 = operator_new(0x40);
    local_51 = 4;
    local_68 = (long *)CONCAT35(local_68._5_3_,0x656d616e);
    FUN_100261120(&local_120,&local_68,1);
    local_a8 = &PTR_FUN_1068d8880;
    local_90 = &local_a8;
    *puVar5 = &PTR_FUN_10658f818;
    puVar5[2] = pvStack_118;
    puVar5[1] = local_120;
    puVar5[3] = local_110;
    local_120 = (void *)0x0;
    pvStack_118 = (void *)0x0;
    local_110 = 0;
    puVar5[4] = &PTR_FUN_1068d8880;
    puVar5[7] = puVar5 + 4;
    puVar5[5] = param_1;
    local_100 = puVar5;
    lStack_a0 = param_1;
    local_f8 = operator_new(0x20);
    *local_f8 = (long)&PTR____shared_weak_count_10658f858;
    local_f8[1] = 0;
    local_f8[2] = 0;
    local_f8[3] = (long)puVar5;
    (**(code **)(*plVar2 + 8))(plVar2,&local_b0,&local_100);
    if (local_f8 != (long *)0x0) {
      LOAcquire();
      lVar4 = local_f8[1];
      local_f8[1] = lVar4 + -1;
      LORelease();
      if (lVar4 == 0) {
        (**(code **)(*local_f8 + 0x10))(local_f8);
        std::__shared_weak_count::__release_weak();
      }
    }
    if (local_90 == &local_a8) {
      lVar4 = 0x20;
LAB_10317c288:
      (**(code **)((long)*local_90 + lVar4))();
    }
    else if (local_90 != (undefined ***)0x0) {
      lVar4 = 0x28;
      goto LAB_10317c288;
    }
    if (local_120 != (void *)0x0) {
      for (; pvStack_118 != local_120; pvStack_118 = (void *)((long)pvStack_118 + -0x18)) {
      }
      pvStack_118 = local_120;
      operator_delete(local_120);
    }
    if ((local_b0 != (int *)0x0) && (iVar1 = *local_b0, *local_b0 = iVar1 + -1, iVar1 + -1 == 0)) {
      FUN_101449efc();
    }
  }
  if (*(long *)PTR____stack_chk_guard_1064f8818 == local_38) {
    return;
  }
LAB_10317c3cc:
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

