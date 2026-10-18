
void FUN_100134348(undefined8 *param_1,undefined8 param_2)

{
  undefined **ppuVar1;
  char *pcVar2;
  uint uVar3;
  undefined **ppuVar4;
  undefined **ppuVar5;
  int iVar6;
  undefined **ppuVar7;
  long *plVar8;
  ulong uVar9;
  undefined8 *puVar10;
  undefined8 uVar11;
  undefined *puVar12;
  undefined **ppuVar13;
  long lVar14;
  code *pcVar15;
  undefined **ppuVar16;
  undefined **ppuVar17;
  undefined **ppuVar18;
  undefined **ppuVar19;
  undefined *puVar20;
  long *local_130;
  long *local_128;
  undefined1 auStack_120 [8];
  long *local_118;
  undefined1 auStack_110 [8];
  long *local_108;
  undefined1 auStack_100 [8];
  long *local_f8;
  undefined8 *local_f0;
  undefined **local_e8 [3];
  long alStack_d0 [3];
  long *local_b8;
  undefined **local_b0;
  undefined **ppuStack_a8;
  undefined8 local_a0;
  undefined ***local_98;
  undefined1 auStack_90 [24];
  long local_78;
  
  local_78 = *(long *)PTR____stack_chk_guard_100b1c378;
  ppuVar7 = operator_new(0x38);
  *ppuVar7 = (undefined *)&PTR_FUN_100b442c8;
  *(undefined1 *)(ppuVar7 + 1) = 0;
  ppuVar13 = ppuVar7 + 2;
  *ppuVar13 = (undefined *)0x0;
  ppuVar16 = ppuVar7 + 3;
  *ppuVar16 = (undefined *)0x0;
  ppuVar17 = ppuVar7 + 4;
  *ppuVar17 = (undefined *)0x0;
  FUN_1001908f8(ppuVar7 + 5);
  plVar8 = operator_new(0x58);
  FUN_10013da2c(&local_b0,param_2,0);
  *plVar8 = (long)&PTR_thunk_FUN_10013ed4c_100b44348;
  plVar8[1] = (long)(plVar8 + 2);
  *(undefined8 *)((long)plVar8 + 0x14) = DAT_1009a8748;
  *(undefined4 *)((long)plVar8 + 0x1c) = 0xffffffff;
  if (local_a0 < 0) {
    FUN_100135b64(plVar8 + 4,local_b0,ppuStack_a8);
    *(undefined4 *)(plVar8 + 7) = 0;
    plVar8[9] = 0;
    plVar8[10] = 0;
    plVar8[8] = 0;
    if (local_a0 < 0) {
      operator_delete(local_b0);
    }
  }
  else {
    plVar8[5] = (long)ppuStack_a8;
    plVar8[4] = (long)local_b0;
    plVar8[6] = local_a0;
    *(undefined4 *)(plVar8 + 7) = 0;
    plVar8[9] = 0;
    plVar8[10] = 0;
    plVar8[8] = 0;
  }
  (**(code **)(*plVar8 + 0x38))(plVar8);
  uVar9 = (**(code **)(*plVar8 + 0x10))(plVar8);
  if ((uVar9 & 1) == 0) {
    local_a0._7_1_ = '\x04';
    local_b0 = (undefined **)CONCAT35(local_b0._5_3_,0x72726563);
    uVar11 = std::chrono::system_clock::now();
    FUN_1006a284c(&local_f0,4,&local_b0,uVar11);
    if (local_a0._7_1_ < '\0') {
      operator_delete(local_b0);
    }
    iVar6 = FUN_10069f1d8(&local_f0);
    if (iVar6 != 0) {
      uVar11 = FUN_10069c398(&local_f0,"Scanner: Failed to set up IPC channel. ");
      (**(code **)(*plVar8 + 0x48))(&local_b0,plVar8);
      uVar11 = FUN_10069d278(uVar11,&ppuStack_a8);
      uVar11 = FUN_10069c398(uVar11," ");
      iVar6 = FUN_1001806e4();
      pcVar2 = " Process orphaned.";
      if (iVar6 == 0) {
        pcVar2 = "";
      }
      FUN_10069c398(uVar11,pcVar2);
      if ((long)local_98 < 0) {
        operator_delete(ppuStack_a8);
      }
    }
    thunk_FUN_10069bf04(&local_f0);
    pcVar15 = *(code **)(*plVar8 + 8);
  }
  else {
    puVar10 = (undefined8 *)FUN_1002e29c4(0xe8);
    local_b0 = &PTR_FUN_100b443e8;
    local_98 = &local_b0;
    ppuStack_a8 = ppuVar7;
    FUN_100648de8(puVar10,&local_b0);
    if (puVar10 != (undefined8 *)0x0) {
      *(int *)(puVar10 + 1) = *(int *)(puVar10 + 1) + 1;
    }
    local_f0 = puVar10;
    if (local_98 == &local_b0) {
      lVar14 = 0x20;
LAB_1001345b4:
      (**(code **)((long)*local_98 + lVar14))();
    }
    else if (local_98 != (undefined ***)0x0) {
      lVar14 = 0x28;
      goto LAB_1001345b4;
    }
    puVar12 = *ppuVar13;
    if ((puVar12 != (undefined *)0x0) &&
       (iVar6 = *(int *)(puVar12 + 8), *(int *)(puVar12 + 8) = iVar6 + -1, iVar6 + -1 == 0)) {
      FUN_100292f88();
    }
    *ppuVar13 = (undefined *)puVar10;
    local_b8 = (long *)0x0;
    local_130 = plVar8;
    FUN_100649d30(&local_128,puVar10,&local_130,alStack_d0);
    if (local_b8 == alStack_d0) {
      lVar14 = 0x20;
LAB_10013461c:
      (**(code **)(*local_b8 + lVar14))();
    }
    else if (local_b8 != (long *)0x0) {
      lVar14 = 0x28;
      goto LAB_10013461c;
    }
    plVar8 = local_130;
    local_130 = (long *)0x0;
    if (plVar8 != (long *)0x0) {
      (**(code **)(*plVar8 + 8))();
    }
    plVar8 = local_128;
    local_128 = (long *)0x0;
    ppuVar13 = operator_new(0x10);
    *ppuVar13 = (undefined *)&PTR_FUN_100b44478;
    ppuVar13[1] = (undefined *)plVar8;
    puVar12 = (undefined *)FUN_1002e29c4(0xe0);
    local_b0 = ppuVar13;
    thunk_FUN_100617c6c(puVar12,&local_b0,"plugin-scanner->live");
    ppuVar13 = local_b0;
    if (puVar12 != (undefined *)0x0) {
      *(int *)(puVar12 + 8) = *(int *)(puVar12 + 8) + 1;
    }
    local_b0 = (undefined **)0x0;
    if (ppuVar13 != (undefined **)0x0) {
      (**(code **)(*ppuVar13 + 8))();
    }
    ppuVar13 = operator_new(0xd8);
    ppuVar19 = ppuVar13 + 1;
    *ppuVar13 = puVar12;
    thunk_FUN_100148ce0(ppuVar19);
    FUN_1001908f8(ppuVar13 + 0x18);
    *(undefined1 *)(ppuVar13 + 0x1a) = 1;
    local_b0 = &PTR_FUN_100b444d8;
    local_98 = &local_b0;
    ppuStack_a8 = ppuVar13;
    FUN_1006187e8(auStack_100,*ppuVar13,1,&local_b0);
    if (local_f8 != (long *)0x0) {
      LOAcquire();
      iVar6 = *(int *)((long)local_f8 + 0xc);
      *(int *)((long)local_f8 + 0xc) = iVar6 + -1;
      LORelease();
      if (iVar6 == 1) {
        (**(code **)(*local_f8 + 0x18))();
      }
    }
    if (local_98 == &local_b0) {
      lVar14 = 0x20;
LAB_10013474c:
      (**(code **)((long)*local_98 + lVar14))();
    }
    else if (local_98 != (undefined ***)0x0) {
      lVar14 = 0x28;
      goto LAB_10013474c;
    }
    local_b0 = &PTR_FUN_100b44558;
    local_98 = &local_b0;
    ppuStack_a8 = ppuVar13;
    FUN_1006187e8(auStack_110,*ppuVar13,2,&local_b0);
    if (local_108 != (long *)0x0) {
      LOAcquire();
      iVar6 = *(int *)((long)local_108 + 0xc);
      *(int *)((long)local_108 + 0xc) = iVar6 + -1;
      LORelease();
      if (iVar6 == 1) {
        (**(code **)(*local_108 + 0x18))();
      }
    }
    if (local_98 == &local_b0) {
      lVar14 = 0x20;
LAB_1001347c8:
      (**(code **)((long)*local_98 + lVar14))();
    }
    else if (local_98 != (undefined ***)0x0) {
      lVar14 = 0x28;
      goto LAB_1001347c8;
    }
    ppuStack_a8 = (undefined **)0x0;
    local_b0 = (undefined **)0x0;
    local_98 = (undefined ***)0x0;
    local_a0 = 0;
    local_f0 = &DAT_100b445c9;
    local_e8[0] = ppuVar13;
    FUN_10013f600(&local_f0,&local_98);
    if (((local_f0 != (undefined8 *)0x0) && (((ulong)local_f0 & 1) == 0)) &&
       ((code *)*local_f0 != (code *)0x0)) {
      (*(code *)*local_f0)(local_e8,local_e8,2);
    }
    FUN_100149a9c(auStack_120,ppuVar19,&local_b0);
    if (local_118 != (long *)0x0) {
      LOAcquire();
      iVar6 = *(int *)((long)local_118 + 0xc);
      *(int *)((long)local_118 + 0xc) = iVar6 + -1;
      LORelease();
      if (iVar6 == 1) {
        (**(code **)(*local_118 + 0x18))();
      }
    }
    if (local_98 != (undefined ***)0x0) {
      if ((((ulong)local_98 & 1) == 0) && (*local_98 != (undefined **)0x0)) {
        (*(code *)*local_98)(auStack_90,auStack_90,2);
      }
      local_98 = (undefined ***)0x0;
    }
    ppuVar5 = local_b0;
    ppuVar4 = ppuStack_a8;
    if (local_b0 != (undefined **)0x0) {
      while (ppuVar4 != ppuVar5) {
        ppuVar18 = ppuVar4 + -3;
        uVar3 = *(uint *)ppuVar18 ^ (int)*(uint *)ppuVar18 >> 0x1f;
        if (uVar3 == 2) {
          ppuVar1 = ppuVar4 + -2;
          ppuVar4 = ppuVar18;
          if ((long *)*ppuVar1 != (long *)0x0) {
            (**(code **)(*(long *)*ppuVar1 + 8))();
          }
        }
        else if (uVar3 == 1) {
          plVar8 = (long *)ppuVar4[-1];
          ppuVar4 = ppuVar18;
          if (plVar8 != (long *)0x0) {
            LOAcquire();
            iVar6 = *(int *)((long)plVar8 + 0xc);
            *(int *)((long)plVar8 + 0xc) = iVar6 + -1;
            LORelease();
            if (iVar6 == 1) {
              (**(code **)(*plVar8 + 0x18))();
            }
          }
        }
        else {
          plVar8 = (long *)ppuVar4[-1];
          ppuVar4 = ppuVar18;
          if (plVar8 != (long *)0x0) {
            LOAcquire();
            iVar6 = *(int *)((long)plVar8 + 0xc);
            *(int *)((long)plVar8 + 0xc) = iVar6 + -1;
            LORelease();
            if (iVar6 == 1) {
              (**(code **)(*plVar8 + 0x18))();
            }
          }
        }
      }
      ppuStack_a8 = ppuVar5;
      operator_delete(local_b0);
    }
    ppuStack_a8 = (undefined **)0x0;
    local_b0 = (undefined **)0x0;
    local_98 = (undefined ***)0x0;
    local_a0._0_7_ = 0;
    local_a0._7_1_ = '\0';
    local_f0 = &DAT_100b445e9;
    local_e8[0] = ppuVar13;
    FUN_10013f600(&local_f0,&local_98);
    if (((local_f0 != (undefined8 *)0x0) && (((ulong)local_f0 & 1) == 0)) &&
       ((code *)*local_f0 != (code *)0x0)) {
      (*(code *)*local_f0)(local_e8,local_e8,2);
    }
    FUN_100149aa8(&local_f0,ppuVar19,&local_b0);
    if (local_e8[0] != (undefined **)0x0) {
      LOAcquire();
      iVar6 = *(int *)((long)local_e8[0] + 0xc);
      *(int *)((long)local_e8[0] + 0xc) = iVar6 + -1;
      LORelease();
      if (iVar6 == 1) {
        (**(code **)(*local_e8[0] + 0x18))();
      }
    }
    if (local_98 != (undefined ***)0x0) {
      if ((((ulong)local_98 & 1) == 0) && (*local_98 != (undefined **)0x0)) {
        (*(code *)*local_98)(auStack_90,auStack_90,2);
      }
      local_98 = (undefined ***)0x0;
    }
    ppuVar5 = local_b0;
    ppuVar4 = ppuStack_a8;
    if (local_b0 != (undefined **)0x0) {
      while (ppuVar4 != ppuVar5) {
        ppuVar18 = ppuVar4 + -3;
        uVar3 = *(uint *)ppuVar18 ^ (int)*(uint *)ppuVar18 >> 0x1f;
        if (uVar3 == 2) {
          ppuVar1 = ppuVar4 + -2;
          ppuVar4 = ppuVar18;
          if ((long *)*ppuVar1 != (long *)0x0) {
            (**(code **)(*(long *)*ppuVar1 + 8))();
          }
        }
        else if (uVar3 == 1) {
          plVar8 = (long *)ppuVar4[-1];
          ppuVar4 = ppuVar18;
          if (plVar8 != (long *)0x0) {
            LOAcquire();
            iVar6 = *(int *)((long)plVar8 + 0xc);
            *(int *)((long)plVar8 + 0xc) = iVar6 + -1;
            LORelease();
            if (iVar6 == 1) {
              (**(code **)(*plVar8 + 0x18))();
            }
          }
        }
        else {
          plVar8 = (long *)ppuVar4[-1];
          ppuVar4 = ppuVar18;
          if (plVar8 != (long *)0x0) {
            LOAcquire();
            iVar6 = *(int *)((long)plVar8 + 0xc);
            *(int *)((long)plVar8 + 0xc) = iVar6 + -1;
            LORelease();
            if (iVar6 == 1) {
              (**(code **)(*plVar8 + 0x18))();
            }
          }
        }
      }
      ppuStack_a8 = ppuVar5;
      operator_delete(local_b0);
    }
    FUN_10014954c(ppuVar19,0);
    FUN_10014954c(ppuVar19,3);
    puVar20 = *ppuVar17;
    *ppuVar17 = (undefined *)ppuVar13;
    if (puVar20 != (undefined *)0x0) {
      FUN_10013f9f0(puVar20 + 8);
      operator_delete(puVar20);
    }
    if (puVar12 != (undefined *)0x0) {
      *(int *)(puVar12 + 8) = *(int *)(puVar12 + 8) + 1;
    }
    puVar20 = *ppuVar16;
    if ((puVar20 != (undefined *)0x0) &&
       (iVar6 = *(int *)(puVar20 + 8), *(int *)(puVar20 + 8) = iVar6 + -1, iVar6 + -1 == 0)) {
      FUN_100292f88();
    }
    *ppuVar16 = puVar12;
    if ((puVar12 != (undefined *)0x0) &&
       (iVar6 = *(int *)(puVar12 + 8), *(int *)(puVar12 + 8) = iVar6 + -1, iVar6 + -1 == 0)) {
      FUN_100292f88(puVar12);
    }
    plVar8 = local_128;
    local_128 = (long *)0x0;
    if (plVar8 == (long *)0x0) goto LAB_100134b74;
    pcVar15 = *(code **)(*plVar8 + 8);
  }
  (*pcVar15)(plVar8);
LAB_100134b74:
  *param_1 = ppuVar7;
  if (*(long *)PTR____stack_chk_guard_100b1c378 != local_78) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}

