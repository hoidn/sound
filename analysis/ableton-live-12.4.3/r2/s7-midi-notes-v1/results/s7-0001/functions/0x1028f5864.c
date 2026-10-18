
/* WARNING: Type propagation algorithm not settling */

void FUN_1028f5864(long param_1,undefined8 param_2)

{
  undefined *puVar1;
  char *pcVar2;
  code *pcVar3;
  int iVar4;
  undefined8 *puVar5;
  long *plVar6;
  undefined8 uVar7;
  undefined8 ******ppppppuVar8;
  undefined8 ******ppppppuVar9;
  ulong uVar10;
  long *plVar11;
  long *plVar12;
  long lVar13;
  undefined8 ******ppppppuVar14;
  ulong uVar15;
  long *plVar16;
  undefined8 ******ppppppuVar17;
  size_t sVar18;
  char *pcVar19;
  long lVar20;
  long lVar21;
  undefined8 uVar22;
  undefined8 *****pppppuVar23;
  undefined8 ******local_118;
  undefined8 ******ppppppuStack_110;
  char *local_108;
  undefined8 uStack_100;
  undefined1 auStack_f8 [8];
  undefined8 *******local_f0;
  long lStack_e8;
  char local_d9;
  void *local_d8 [2];
  char local_c1;
  undefined1 auStack_c0 [8];
  long *local_b8;
  long *local_b0;
  undefined8 *******local_a0;
  undefined8 ******local_98;
  undefined8 ******local_90;
  char *local_88;
  char *local_80;
  long *local_78;
  undefined8 ******local_70;
  
  FUN_101486fa8();
  FUN_101849958();
  iVar4 = FUN_10185138c();
  puVar1 = PTR_KAllMidiKeys_106508188;
  if (iVar4 != 0) {
    lVar13 = 0;
    lVar21 = param_1 + 0x28;
    do {
      lVar20 = (long)*(int *)(puVar1 + lVar13);
      if ((*(long *)(lVar21 + lVar20 * 8) != 0) && (iVar4 = FUN_1028ac07c(), iVar4 == 0)) {
        FUN_10156d800(*(undefined8 *)(param_1 + 0x430),*(undefined8 *)(lVar21 + lVar20 * 8));
        *(undefined8 *)(lVar21 + lVar20 * 8) = 0;
      }
      lVar13 = lVar13 + 4;
    } while (lVar13 != 0x200);
  }
  FUN_1028f5f74(param_1);
  plVar16 = *(long **)(param_1 + 0x430);
  puVar5 = (undefined8 *)(**(code **)(*plVar16 + 0x60))(plVar16);
  lVar13 = (**(code **)*puVar5)(puVar5,plVar16);
  lVar21 = *(long *)(lVar13 + 0x18);
  puVar5 = (undefined8 *)(**(code **)(*plVar16 + 0x60))(plVar16);
  (**(code **)*puVar5)(puVar5,plVar16);
  puVar1 = PTR_CallMemberFunc<&AMidiNotes::OnKeyTrackUpdate>_10652a008;
  for (; lVar21 != lVar13; lVar21 = *(long *)(lVar21 + 0x18)) {
    plVar6 = (long *)(**(code **)(*plVar16 + 0x60))(plVar16);
    lVar20 = (**(code **)(*plVar6 + 0x20))(plVar6,plVar16,lVar21);
    uVar7 = FUN_1028abe68(*(undefined8 *)(lVar20 + 8));
    local_a0 = (undefined8 *******)puVar1;
    local_98 = (undefined8 ******)param_1;
    FUN_10155ee3c(uVar7,param_1,&local_a0,1);
  }
  FUN_1028f6154(&local_b8,param_1);
  plVar16 = local_b0;
  plVar6 = local_b8;
  if ((local_b0 != local_b8) && (plVar6 = local_b0, local_b8 + 1 != local_b0)) {
    plVar12 = local_b8 + 1;
    do {
      plVar6 = plVar12;
      if (*local_b8 != *plVar6) break;
      plVar12 = plVar6 + 1;
      plVar6 = local_b0;
    } while (plVar12 != local_b0);
  }
  local_a0 = (undefined8 *******)0x0;
  local_98 = (undefined8 ******)0x0;
  local_90 = (undefined8 ******)0x0;
  if ((local_b8 == local_b0) && (plVar6 == local_b0)) {
    ppppppuVar17 = (undefined8 ******)0x0;
    if (local_b8 != local_b0) goto LAB_1028f5a08;
LAB_1028f5b44:
    lVar21 = 1;
  }
  else {
    ppppppuVar9 = (undefined8 ******)0x0;
    ppppppuVar14 = (undefined8 ******)0x0;
    ppppppuVar17 = (undefined8 ******)0x0;
    plVar12 = local_b8;
    do {
      plVar11 = plVar6;
      ppppppuVar8 = ppppppuVar17;
      if (8 < (ulong)((long)plVar11 - (long)plVar12)) {
        pppppuVar23 = (undefined8 *****)*plVar12;
        if (ppppppuVar14 < ppppppuVar9) {
          *ppppppuVar14 = pppppuVar23;
          ppppppuVar14 = ppppppuVar14 + 1;
        }
        else {
          sVar18 = (long)ppppppuVar14 - (long)ppppppuVar17;
          lVar21 = (long)sVar18 >> 3;
          uVar10 = lVar21 + 1;
          if (uVar10 >> 0x3d != 0) {
            local_a0 = (undefined8 *******)ppppppuVar17;
            local_98 = ppppppuVar14;
            local_90 = ppppppuVar9;
                    /* WARNING: Subroutine does not return */
            FUN_100d338b0(&local_a0);
          }
          uVar15 = (long)ppppppuVar9 - (long)ppppppuVar17 >> 2;
          if (uVar15 <= uVar10) {
            uVar15 = uVar10;
          }
          if (0x7ffffffffffffff7 < (ulong)((long)ppppppuVar9 - (long)ppppppuVar17)) {
            uVar15 = 0x1fffffffffffffff;
          }
          if (uVar15 == 0) {
            ppppppuVar8 = (undefined8 ******)0x0;
          }
          else {
            if (uVar15 >> 0x3d != 0) {
              local_a0 = (undefined8 *******)ppppppuVar17;
              local_90 = ppppppuVar9;
                    /* WARNING: Subroutine does not return */
              FUN_10024a858();
            }
            ppppppuVar8 = operator_new(uVar15 << 3);
          }
          ppppppuVar9 = ppppppuVar8 + uVar15;
          ppppppuVar14 = ppppppuVar8 + lVar21 + 1;
          ppppppuVar8[lVar21] = pppppuVar23;
          _memcpy(ppppppuVar8,ppppppuVar17,sVar18);
          if (ppppppuVar17 != (undefined8 ******)0x0) {
            operator_delete(ppppppuVar17);
          }
        }
      }
      ppppppuVar17 = ppppppuVar8;
      plVar6 = plVar11;
      if ((plVar16 != plVar11) && (plVar12 = plVar11 + 1, plVar6 = plVar16, plVar12 != plVar16)) {
        do {
          plVar6 = plVar12;
          if (*plVar11 != *plVar12) break;
          plVar12 = plVar12 + 1;
          plVar6 = plVar16;
        } while (plVar12 != plVar16);
      }
      plVar12 = plVar11;
    } while ((plVar11 != plVar16) || (plVar6 != plVar16));
    if (ppppppuVar17 != ppppppuVar14) {
      uVar15 = (long)ppppppuVar14 - (long)ppppppuVar17 >> 3;
      uVar10 = uVar15;
      if (9 < uVar15) {
        uVar10 = 10;
      }
      uVar7 = std::chrono::system_clock::now();
      FUN_103f3ffec(auStack_c0,4,uVar7);
      iVar4 = FUN_103f3c8b8(auStack_c0);
      if (iVar4 != 0) {
        FUN_1014861d8(auStack_f8,param_1);
        FUN_1014320f0(&local_f0,auStack_f8);
        ppppppuStack_110 = ppppppuVar17 + uVar10;
        local_108 = ", ";
        uStack_100 = 2;
        local_80 = "...";
        if (uVar15 < 0xb) {
          local_80 = "";
        }
        local_a0 = local_f0;
        if (-1 < (long)local_d9) {
          local_a0 = &local_f0;
        }
        local_98 = (undefined8 ******)lStack_e8;
        if (-1 < local_d9) {
          local_98 = (undefined8 ******)(long)local_d9;
        }
        local_90 = &local_118;
        local_88 = 
        PTR_format_custom<fmt::v12::join_view<std::__wrap_iter<unsigned_long_long_const*>,std::__wrap_iter<unsigned_long_long_const*>,char>>_106509e90
        ;
        local_118 = ppppppuVar17;
        FUN_103f94148(local_d8,"Note IDs are not unique in {}: {}{}",0x23,0xcfd,&local_a0);
        FUN_103f3a958(auStack_c0,local_d8);
        if (local_c1 < '\0') {
          operator_delete(local_d8[0]);
        }
        if (local_d9 < '\0') {
          operator_delete(local_f0);
        }
        FUN_100234444(auStack_f8);
      }
      thunk_FUN_103f395e4(auStack_c0);
      FUN_101488e64(param_2,"Note IDs are not unique");
      goto LAB_1028f5e30;
    }
    if (local_b8 == local_b0) goto LAB_1028f5b44;
LAB_1028f5a08:
    lVar21 = local_b0[-1] + 1;
  }
  FUN_102920db4(*(undefined8 *)(param_1 + 0x598),lVar21);
  FUN_1028f64d0(param_1,&local_b8);
  plVar16 = *(long **)(param_1 + 0x430);
  puVar5 = (undefined8 *)(**(code **)(*plVar16 + 0x60))(plVar16);
  local_88 = (char *)(**(code **)*puVar5)(puVar5,plVar16);
  local_70 = (undefined8 ******)0x0;
  local_80 = local_88;
  local_78 = plVar16;
  FUN_1028eb274(&local_a0);
  FUN_1028eb274(&local_a0);
  ppppppuVar9 = local_70;
  plVar16 = local_78;
  pcVar19 = local_80;
  pcVar2 = local_88;
  ppppppuVar14 = local_90;
  plVar6 = *(long **)(param_1 + 0x430);
  puVar5 = (undefined8 *)(**(code **)(*plVar6 + 0x60))(plVar6);
  local_88 = (char *)(**(code **)*puVar5)(puVar5,plVar6);
  local_70 = (undefined8 ******)0x0;
  local_80 = local_88;
  local_78 = plVar6;
  FUN_1028eb274(&local_a0);
  while (ppppppuVar9 != (undefined8 ******)0x0) {
    uVar22 = *(undefined8 *)(param_1 + 0x490);
    uVar7 = FUN_1028da61c(ppppppuVar9);
    FUN_1028dea48(ppppppuVar9);
    FUN_10292c960(uVar22,uVar7);
    ppppppuVar9 = ppppppuVar9 + 6;
    if (ppppppuVar14 <= ppppppuVar9) {
      do {
        pcVar19 = *(char **)((long)pcVar19 + 0x18);
        if (pcVar19 == pcVar2) goto LAB_1028f5c8c;
        if (pcVar19 == (char *)0x0) {
          uVar7 = 0;
        }
        else {
          plVar6 = (long *)(**(code **)(*plVar16 + 0x60))(plVar16);
          lVar21 = (**(code **)(*plVar6 + 0x20))(plVar6,plVar16,pcVar19);
          uVar7 = *(undefined8 *)(lVar21 + 8);
        }
        iVar4 = FUN_1028ac07c(uVar7);
      } while (iVar4 == 0);
      uVar7 = FUN_1028a89d0(uVar7);
      ppppppuVar9 = (undefined8 ******)FUN_10155ee2c(uVar7,0);
      ppppppuVar14 = ppppppuVar9 + (long)iVar4 * 6;
    }
  }
LAB_1028f5c8c:
  FUN_1028f6664(param_1);
  uVar10 = FUN_1028f5640(param_1);
  if ((uVar10 & 1) != 0) {
    if (ppppppuVar17 != (undefined8 ******)0x0) {
      operator_delete(ppppppuVar17);
    }
    if (local_b8 != (long *)0x0) {
      local_b0 = local_b8;
      operator_delete(local_b8);
    }
    return;
  }
  FUN_101488e64(param_2,"Note-group ids are corrupt.");
LAB_1028f5e30:
                    /* WARNING: Does not return */
  pcVar3 = (code *)SoftwareBreakpoint(1,0x1028f5e34);
  (*pcVar3)();
}

