
/* WARNING: Removing unreachable block (ram,0x0001005ab390) */
/* WARNING: Removing unreachable block (ram,0x0001005ab024) */
/* WARNING: Removing unreachable block (ram,0x0001005aade8) */
/* WARNING: Removing unreachable block (ram,0x0001005aadec) */
/* WARNING: Removing unreachable block (ram,0x0001005aadfc) */
/* WARNING: Removing unreachable block (ram,0x0001005ab480) */
/* WARNING: Removing unreachable block (ram,0x0001005ab49c) */
/* WARNING: Removing unreachable block (ram,0x0001005ab17c) */
/* WARNING: Removing unreachable block (ram,0x0001005ab2a4) */
/* WARNING: Removing unreachable block (ram,0x0001005ab008) */
/* WARNING: Removing unreachable block (ram,0x0001005ab2b4) */
/* WARNING: Removing unreachable block (ram,0x0001005ab2c4) */
/* WARNING: Removing unreachable block (ram,0x0001005ab2d4) */
/* WARNING: Removing unreachable block (ram,0x0001005ab2e4) */
/* WARNING: Removing unreachable block (ram,0x0001005ab08c) */
/* WARNING: Removing unreachable block (ram,0x0001005ab0bc) */
/* WARNING: Removing unreachable block (ram,0x0001005ab0a0) */

void FUN_1005aad10(undefined8 *param_1,undefined8 *param_2)

{
  int *****pppppiVar1;
  long *plVar2;
  long *plVar3;
  char cVar4;
  undefined8 *****pppppuVar5;
  undefined8 *puVar6;
  long ****pppplVar7;
  long ***ppplVar8;
  bool bVar9;
  byte bVar10;
  int iVar11;
  long *****ppppplVar12;
  undefined8 uVar13;
  ulong uVar14;
  undefined8 uVar15;
  undefined8 uVar16;
  ulong extraout_x1;
  long ****pppplVar17;
  long ****pppplVar18;
  void *pvVar19;
  long *****ppppplVar20;
  long ***local_1a0;
  long ***ppplStack_198;
  long ***local_190;
  long ***local_188;
  long ***ppplStack_180;
  long ***local_178;
  void *local_170;
  undefined8 uStack_168;
  void *local_160;
  undefined8 uStack_158;
  undefined4 local_150;
  long ****local_148;
  long ****local_140;
  long local_138;
  undefined8 ****ppppuStack_130;
  long ***local_128;
  long ***local_120;
  int local_110 [2];
  undefined8 local_108;
  undefined8 ****local_100;
  long ***ppplStack_f8;
  undefined7 local_f0;
  char cStack_e9;
  long *local_e8;
  int local_e0 [2];
  undefined8 local_d8;
  undefined8 ****local_d0;
  long ***ppplStack_c8;
  long ***local_c0;
  int ****local_b8;
  ulong local_b0;
  byte local_a1;
  undefined8 ****local_a0;
  long ***ppplStack_98;
  long ***local_90;
  long ***local_88;
  long ***ppplStack_80;
  long ***local_78;
  
  local_138 = 0;
  plVar3 = (long *)param_2[1];
  local_148 = (long ****)&local_148;
  local_140 = (long ****)&local_148;
  for (plVar2 = (long *)*param_2; plVar2 != plVar3; plVar2 = plVar2 + 3) {
    if (*(char *)((long)plVar2 + 0x17) < '\0') {
      FUN_100135b64(&local_a0,*plVar2,plVar2[1]);
    }
    else {
      ppplStack_98 = (long ***)plVar2[1];
      local_a0 = (undefined8 ****)*plVar2;
      local_90 = (long ***)plVar2[2];
    }
    local_88 = (long ***)0x0;
    ppplStack_80 = (long ***)0x0;
    local_78 = (long ***)0x0;
    ppppplVar12 = operator_new(0x40);
    ppplVar8 = local_90;
    ppppplVar12[3] = (long ****)ppplStack_98;
    ppppplVar12[2] = local_a0;
    ppplStack_98 = (long ***)0x0;
    local_90 = (long ***)0x0;
    local_a0 = (undefined8 *****)0x0;
    ppppplVar12[4] = (long ****)ppplVar8;
    ppppplVar12[5] = (long ****)0x0;
    ppppplVar12[6] = (long ****)0x0;
    ppppplVar12[7] = (long ****)0x0;
    ppplStack_80 = (long ***)0x0;
    local_78 = (long ***)0x0;
    local_88 = (long ***)0x0;
    *ppppplVar12 = local_148;
    ppppplVar12[1] = (long ****)&local_148;
    local_148[1] = (long ***)ppppplVar12;
    local_138 = local_138 + 1;
    local_148 = (long ****)ppppplVar12;
  }
  uStack_168 = 0;
  local_170 = (void *)0x0;
  uStack_158 = 0;
  local_160 = (void *)0x0;
  local_150 = 0x3f800000;
  param_1[1] = 0;
  *param_1 = 0;
  param_1[3] = 0;
  param_1[2] = 0;
  *(undefined4 *)(param_1 + 4) = 0x3f800000;
  if (local_138 != 0) {
    do {
      pppplVar17 = local_140;
      if (*(char *)((long)local_140 + 0x27) < '\0') {
        FUN_100135b64(&local_1a0,local_140[2],local_140[3]);
      }
      else {
        ppplStack_198 = local_140[3];
        local_1a0 = local_140[2];
        local_190 = local_140[4];
      }
      if (*(char *)((long)pppplVar17 + 0x3f) < '\0') {
        FUN_100135b64(&local_188,pppplVar17[5],pppplVar17[6]);
      }
      else {
        ppplStack_180 = pppplVar17[6];
        local_188 = pppplVar17[5];
        local_178 = pppplVar17[7];
      }
      pppplVar7 = local_140;
      pppplVar17 = (long ****)*local_140;
      pppplVar18 = (long ****)local_140[1];
      pppplVar17[1] = (long ***)pppplVar18;
      *pppplVar18 = (long ***)pppplVar17;
      local_138 = local_138 + -1;
      if (*(char *)((long)local_140 + 0x3f) < '\0') {
        operator_delete(local_140[5]);
        cVar4 = *(char *)((long)pppplVar7 + 0x27);
      }
      else {
        cVar4 = *(char *)((long)local_140 + 0x27);
      }
      if (cVar4 < '\0') {
        operator_delete(pppplVar7[2]);
      }
      operator_delete(pppplVar7);
      FUN_1005e64f0(&local_170,&local_1a0,&local_1a0);
      if ((extraout_x1 & 1) != 0) {
        local_e0[0] = 0;
        uVar13 = std::system_category();
        local_d8 = uVar13;
        thunk_FUN_1006606b0(&local_e8,&local_1a0,local_e0);
        while (local_e8 != (long *)0x0) {
          uVar14 = (**(code **)(*local_e8 + 0x30))();
          plVar2 = local_e8;
          if ((uVar14 & 1) != 0) {
            local_e8 = (long *)0x0;
            if (plVar2 != (long *)0x0) {
              (**(code **)(*plVar2 + 8))();
            }
            break;
          }
          if (local_e0[0] != 0) {
            uVar13 = std::chrono::system_clock::now();
            FUN_1006a290c(&local_b8,3,uVar13);
            iVar11 = FUN_10069f1d8(&local_b8);
            if (iVar11 != 0) {
              uVar13 = FUN_10069c398(&local_b8,"Failed to scan folder: ");
              if (local_e8 == (long *)0x0) {
                FUN_100720494("mBaseIt",
                              "shared/filesystem/include/ableton/filesystem/DirectoryIterator.ipp",
                              0x8d);
                goto LAB_1005ab5e8;
              }
              (**(code **)(*local_e8 + 0x20))();
              uVar15 = FUN_1006604c0();
              uVar13 = FUN_10013300c(uVar13,uVar15);
              uVar13 = FUN_10069c398(uVar13," (");
              std::error_code::message();
              uVar13 = FUN_10069d278(uVar13,&local_a0);
              FUN_10069c398(uVar13,")");
            }
            thunk_FUN_10069bf04(&local_b8);
            plVar2 = local_e8;
            local_e8 = (long *)0x0;
            if (plVar2 != (long *)0x0) {
              (**(code **)(*plVar2 + 8))();
            }
            goto LAB_1005ab450;
          }
          if (local_e8 == (long *)0x0) {
            FUN_100720494("mBaseIt",
                          "shared/filesystem/include/ableton/filesystem/DirectoryIterator.ipp",0x8d)
            ;
LAB_1005ab5e8:
                    /* WARNING: Subroutine does not return */
            _abort();
          }
          (**(code **)(*local_e8 + 0x20))();
          uVar15 = FUN_1006604c0();
          FUN_100674264(&local_a0,uVar15,local_e0);
          FUN_10067ac78(&local_100,&local_a0);
          if (local_e0[0] == 0) {
            local_110[0] = 0;
            local_108 = uVar13;
            bVar10 = FUN_10066f240(&local_100,local_110);
            if ((local_110[0] == 0 & bVar10) != 0) {
              FUN_1006c4724(&local_a0,&local_100);
              if ((long)local_90 < 0) {
                local_120 = local_90;
                local_128 = ppplStack_98;
                ppppuStack_130 = local_a0;
                FUN_100135b64(&local_d0,local_a0,ppplStack_98);
              }
              else {
                local_120 = local_90;
                local_128 = ppplStack_98;
                ppppuStack_130 = local_a0;
                ppplStack_c8 = ppplStack_98;
                local_d0 = local_a0;
                local_c0 = local_90;
              }
              pppplVar17 = (long ****)ppplStack_c8;
              pppppuVar5 = (undefined8 *****)local_d0;
              if (-1 < (long)local_c0) {
                pppplVar17 = (long ****)((ulong)local_c0 >> 0x38);
                pppppuVar5 = &local_d0;
              }
              FUN_1006ad5c8(&local_b8,pppppuVar5,pppplVar17);
              uVar14 = local_b0;
              if (-1 < (char)local_a1) {
                uVar14 = (ulong)local_a1;
              }
              if (uVar14 == 4) {
                pppppiVar1 = (int *****)local_b8;
                if (-1 < (char)local_a1) {
                  pppppiVar1 = &local_b8;
                }
                bVar9 = *(int *)pppppiVar1 == 0x7473762e;
              }
              else {
                bVar9 = false;
              }
              if ((char)local_a1 < '\0') {
                operator_delete(local_b8);
              }
              if ((long)local_120 < 0) {
                operator_delete(ppppuStack_130);
              }
              if (bVar9) {
                FUN_1005d48ac(param_1,&local_100,&local_100,&local_188);
              }
              else {
                if (local_e8 == (long *)0x0) {
                  FUN_100720494("mBaseIt",
                                "shared/filesystem/include/ableton/filesystem/DirectoryIterator.ipp"
                                ,0x8d);
                  goto LAB_1005ab5e8;
                }
                (**(code **)(*local_e8 + 0x20))();
                uVar15 = FUN_1006604c0();
                if (cStack_e9 < '\0') {
                  FUN_100135b64(&local_a0,local_100,ppplStack_f8);
                }
                else {
                  ppplStack_98 = ppplStack_f8;
                  local_a0 = local_100;
                  local_90 = (long ***)CONCAT17(cStack_e9,local_f0);
                }
                FUN_10067c300(&local_d0,uVar15);
                thunk_FUN_10067ac78(&local_b8,&local_d0);
                FUN_10018ef44(&local_88,&local_188,&local_b8);
                ppppplVar12 = operator_new(0x40);
                ppppplVar12[3] = (long ****)ppplStack_98;
                ppppplVar12[2] = local_a0;
                ppppplVar12[4] = (long ****)local_90;
                ppplStack_98 = (long ***)0x0;
                local_90 = (long ***)0x0;
                local_a0 = (undefined8 *****)0x0;
                ppppplVar12[6] = (long ****)ppplStack_80;
                ppppplVar12[5] = (long ****)local_88;
                ppppplVar12[7] = (long ****)local_78;
                local_88 = (long ***)0x0;
                ppplStack_80 = (long ***)0x0;
                local_78 = (long ***)0x0;
                *ppppplVar12 = local_148;
                ppppplVar12[1] = (long ****)&local_148;
                local_148[1] = (long ***)ppppplVar12;
                local_138 = local_138 + 1;
                local_148 = (long ****)ppppplVar12;
              }
            }
          }
          else {
            uVar15 = std::chrono::system_clock::now();
            FUN_1006a290c(&local_b8,3,uVar15);
            iVar11 = FUN_10069f1d8(&local_b8);
            if (iVar11 != 0) {
              uVar15 = FUN_10069c398(&local_b8,"Can\'t resolve path: ");
              if (local_e8 == (long *)0x0) {
                FUN_100720494("mBaseIt",
                              "shared/filesystem/include/ableton/filesystem/DirectoryIterator.ipp",
                              0x8d);
                goto LAB_1005ab5e8;
              }
              (**(code **)(*local_e8 + 0x20))();
              uVar16 = FUN_1006604c0();
              uVar15 = FUN_10013300c(uVar15,uVar16);
              uVar15 = FUN_10069c398(uVar15," (");
              std::error_code::message();
              uVar15 = FUN_10069d278(uVar15,&local_a0);
              FUN_10069c398(uVar15,")");
            }
            thunk_FUN_10069bf04(&local_b8);
          }
          if (cStack_e9 < '\0') {
            operator_delete(local_100);
          }
          if (local_e8 == (long *)0x0) {
            FUN_100720494("mBaseIt",
                          "shared/filesystem/include/ableton/filesystem/DirectoryIterator.ipp",0x7e)
            ;
            goto LAB_1005ab5e8;
          }
          (**(code **)(*local_e8 + 0x18))(local_e8,local_e0);
        }
        if (local_e0[0] != 0) {
          uVar13 = std::chrono::system_clock::now();
          FUN_1006a290c(&local_b8,3,uVar13);
          iVar11 = FUN_10069f1d8(&local_b8);
          if (iVar11 != 0) {
            uVar13 = FUN_10069c398(&local_b8,"VST2: Failed to scan folder: ");
            uVar13 = FUN_10013300c(uVar13,&local_1a0);
            uVar13 = FUN_10069c398(uVar13," (");
            std::error_code::message();
            uVar13 = FUN_10069d278(uVar13,&local_a0);
            FUN_10069c398(uVar13,")");
          }
          thunk_FUN_10069bf04(&local_b8);
        }
      }
LAB_1005ab450:
      if ((long)local_178 < 0) {
        operator_delete(local_188);
      }
      if ((long)local_190 < 0) {
        operator_delete(local_1a0);
      }
    } while (local_138 != 0);
    local_138 = 0;
    puVar6 = local_160;
    while (puVar6 != (void *)0x0) {
      pvVar19 = (void *)*puVar6;
      if (*(char *)((long)puVar6 + 0x27) < '\0') {
        operator_delete((void *)puVar6[2]);
      }
      operator_delete(puVar6);
      puVar6 = pvVar19;
    }
  }
  pvVar19 = local_170;
  local_170 = (void *)0x0;
  if (pvVar19 != (void *)0x0) {
    operator_delete(pvVar19);
  }
  if (local_138 != 0) {
    pppplVar18 = (long ****)*local_140;
    pppplVar17 = (long ****)local_148[1];
    pppplVar18[1] = (long ***)pppplVar17;
    *pppplVar17 = (long ***)pppplVar18;
    local_138 = 0;
    ppppplVar12 = (long *****)local_140;
    while (ppppplVar12 != &local_148) {
      ppppplVar20 = (long *****)ppppplVar12[1];
      if (*(char *)((long)ppppplVar12 + 0x3f) < '\0') {
        operator_delete(ppppplVar12[5]);
        cVar4 = *(char *)((long)ppppplVar12 + 0x27);
      }
      else {
        cVar4 = *(char *)((long)ppppplVar12 + 0x27);
      }
      if (cVar4 < '\0') {
        operator_delete(ppppplVar12[2]);
      }
      operator_delete(ppppplVar12);
      ppppplVar12 = ppppplVar20;
    }
  }
  return;
}

