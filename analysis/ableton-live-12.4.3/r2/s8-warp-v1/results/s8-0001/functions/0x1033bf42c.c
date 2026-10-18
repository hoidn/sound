
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1033bf42c(long *param_1,double *param_2)

{
  bool bVar1;
  bool bVar2;
  int iVar3;
  uint uVar4;
  undefined8 uVar5;
  undefined8 uVar6;
  ulong uVar7;
  long *plVar8;
  undefined8 *puVar9;
  long lVar10;
  long *plVar11;
  long lVar12;
  logic_error *plVar13;
  long lVar14;
  double dVar15;
  double dVar16;
  ushort uVar17;
  undefined2 uVar18;
  undefined2 uVar19;
  undefined2 uVar20;
  undefined2 uVar21;
  double dVar22;
  long local_68;
  long local_60;
  long local_58;
  
  uVar5 = (**(code **)(*param_1 + 0x170))();
  uVar6 = FUN_1027afddc();
  uVar7 = FUN_10147fd68(uVar5,uVar6);
  if ((uVar7 & 1) == 0) {
    plVar13 = (logic_error *)___cxa_allocate_exception(0x10);
    std::logic_error::logic_error(plVar13,"Warping is only available for audio clips");
LAB_1033bf938:
                    /* WARNING: Subroutine does not return */
    ___cxa_throw(plVar13,PTR_typeinfo_1064f86a8,PTR__logic_error_1064f8540);
  }
  uVar7 = (**(code **)(*param_1 + 0x300))(param_1);
  if ((uVar7 & 1) == 0) {
    plVar13 = (logic_error *)___cxa_allocate_exception(0x10);
    std::logic_error::logic_error(plVar13,"Cannot add warp marker to an unwarped clip.");
    goto LAB_1033bf938;
  }
  dVar22 = *param_2;
  dVar15 = (double)FUN_1027b6954(param_1);
  bVar1 = false;
  bVar2 = true;
  if (0.0 <= dVar22) {
    bVar1 = false;
    bVar2 = true;
    if (!NAN(dVar22) && !NAN(dVar15)) {
      bVar1 = dVar22 == dVar15;
      bVar2 = dVar15 <= dVar22;
    }
  }
  if (bVar2 && !bVar1) {
    plVar13 = (logic_error *)___cxa_allocate_exception(0x10);
    std::logic_error::logic_error(plVar13,"Warp marker sample time is out of range.");
    goto LAB_1033bf938;
  }
  plVar8 = (long *)(**(code **)(*param_1 + 0x4b0))(param_1);
  puVar9 = (undefined8 *)(**(code **)(*plVar8 + 0x60))();
  lVar10 = (**(code **)*puVar9)(puVar9,plVar8);
  local_60 = 0;
  local_58 = 0;
  lVar14 = *(long *)(lVar10 + 0x18);
  if (lVar14 != lVar10) {
    dVar15 = 0.0;
    do {
      if (lVar14 == 0) {
        uVar5 = 0;
      }
      else {
        plVar11 = (long *)(**(code **)(*plVar8 + 0x60))(plVar8);
        lVar12 = (**(code **)(*plVar11 + 0x20))(plVar11,plVar8,lVar14);
        uVar5 = *(undefined8 *)(lVar12 + 8);
      }
      dVar22 = (double)FUN_102610264(uVar5);
      if (*param_2 < dVar22) {
LAB_1033bf5bc:
        bVar1 = false;
        if ((lVar14 != *(long *)(lVar10 + 0x18)) &&
           (bVar1 = false, !NAN(param_2[1]) && !NAN(dVar15))) {
          bVar1 = param_2[1] < dVar15;
        }
        if (bVar1) {
          plVar13 = (logic_error *)___cxa_allocate_exception(0x10);
          std::logic_error::logic_error
                    (plVar13,"Warp marker beat time is ahead of left adjacent marker\'s beat time.")
          ;
LAB_1033bf984:
                    /* WARNING: Subroutine does not return */
          ___cxa_throw(plVar13,PTR_typeinfo_1064f86a8,PTR__logic_error_1064f8540);
        }
        if (lVar14 == 0) {
          uVar5 = 0;
        }
        else {
          plVar11 = (long *)(**(code **)(*plVar8 + 0x60))(plVar8);
          lVar12 = (**(code **)(*plVar11 + 0x20))(plVar11,plVar8,lVar14);
          uVar5 = *(undefined8 *)(lVar12 + 8);
        }
        uVar7 = FUN_1026102c0(uVar5);
        if ((uVar7 & 1) == 0) {
          dVar15 = param_2[1];
          if (lVar14 == 0) {
            uVar5 = 0;
          }
          else {
            plVar11 = (long *)(**(code **)(*plVar8 + 0x60))(plVar8);
            lVar12 = (**(code **)(*plVar11 + 0x20))(plVar11,plVar8,lVar14);
            uVar5 = *(undefined8 *)(lVar12 + 8);
          }
          dVar22 = (double)FUN_10261026c(uVar5);
          if (dVar22 < dVar15) {
            plVar13 = (logic_error *)___cxa_allocate_exception(0x10);
            std::logic_error::logic_error
                      (plVar13,"Warp marker beat time is behind right adjacent marker\'s beat time."
                      );
            goto LAB_1033bf984;
          }
        }
        if (lVar14 == *(long *)(lVar10 + 0x18)) {
          lVar10 = 0;
          uVar5 = 0;
          local_58 = 0;
          lVar12 = local_58;
          if (lVar14 != 0) goto LAB_1033bf6b4;
        }
        else {
          lVar10 = *(long *)(lVar14 + 0x20);
          lVar12 = 0;
          if (lVar10 != 0) {
            plVar11 = (long *)(**(code **)(*plVar8 + 0x60))(plVar8);
            lVar10 = (**(code **)(*plVar11 + 0x20))(plVar11,plVar8,lVar10);
            lVar12 = *(long *)(lVar10 + 8);
            if (lVar12 != 0) {
              *(int *)(lVar12 + 8) = *(int *)(lVar12 + 8) + 1;
            }
          }
LAB_1033bf6b4:
          local_58 = lVar12;
          lVar10 = local_58;
          plVar11 = (long *)(**(code **)(*plVar8 + 0x60))(plVar8);
          lVar12 = (**(code **)(*plVar11 + 0x20))(plVar11,plVar8,lVar14);
          uVar5 = *(undefined8 *)(lVar12 + 8);
        }
        uVar4 = FUN_1026102c0(uVar5);
        if (lVar14 == 0) {
          uVar4 = 1;
        }
        if ((uVar4 & 1) == 0) {
          plVar11 = (long *)(**(code **)(*plVar8 + 0x60))(plVar8);
          lVar14 = (**(code **)(*plVar11 + 0x20))(plVar11,plVar8,lVar14);
          lVar14 = *(long *)(lVar14 + 8);
          local_60 = lVar14;
          if (lVar14 != 0) {
            *(int *)(lVar14 + 8) = *(int *)(lVar14 + 8) + 1;
          }
        }
        else {
          lVar14 = 0;
          local_60 = 0;
        }
        goto LAB_1033bf734;
      }
      if (lVar14 == 0) {
        uVar5 = 0;
      }
      else {
        plVar11 = (long *)(**(code **)(*plVar8 + 0x60))(plVar8);
        lVar12 = (**(code **)(*plVar11 + 0x20))(plVar11,plVar8,lVar14);
        uVar5 = *(undefined8 *)(lVar12 + 8);
      }
      iVar3 = FUN_1026102c0(uVar5);
      if (iVar3 != 0) goto LAB_1033bf5bc;
      if (lVar14 == 0) {
        uVar5 = 0;
      }
      else {
        plVar11 = (long *)(**(code **)(*plVar8 + 0x60))(plVar8);
        lVar12 = (**(code **)(*plVar11 + 0x20))(plVar11,plVar8,lVar14);
        uVar5 = *(undefined8 *)(lVar12 + 8);
      }
      dVar15 = (double)FUN_10261026c(uVar5);
      lVar14 = *(long *)(lVar14 + 0x18);
    } while (lVar14 != lVar10);
  }
  lVar14 = 0;
  lVar10 = 0;
LAB_1033bf734:
  FUN_102610594(&local_68);
  dVar15 = param_2[1];
  uVar17 = NEON_umaxv(CONCAT26(-(ushort)(dVar15 == _UNK_1055d9698),
                               CONCAT24(-(ushort)(dVar15 == _DAT_1055d9690),
                                        CONCAT22(-(ushort)(dVar15 == _UNK_1055d9688),
                                                 -(ushort)(dVar15 == _DAT_1055d9680)))),2);
  if ((uVar17 & 1) == 0) {
    uVar17 = 0x3ff0;
    if (dVar15 < 0.0) {
      uVar17 = 0xbff0;
    }
    dVar15 = (double)((ulong)uVar17 << 0x30) *
             ((double)(long)(ABS(dVar15 + (double)((ulong)uVar17 << 0x30) * 2.6015651015651016e-07 *
                                          0.5) * 3843840.0) / 3843840.0);
  }
  dVar22 = *param_2;
  uVar18 = SUB82(dVar22,0);
  uVar19 = (undefined2)((ulong)dVar22 >> 0x10);
  uVar20 = (undefined2)((ulong)dVar22 >> 0x20);
  uVar21 = (undefined2)((ulong)dVar22 >> 0x30);
  FUN_10261025c(dVar15,local_68);
  lVar12 = local_68;
  if (lVar10 != 0) {
    dVar22 = (double)FUN_1027afd40(local_68,lVar10);
    dVar15 = (double)CONCAT26(uVar21,CONCAT24(uVar20,CONCAT22(uVar19,uVar18)));
    dVar16 = (double)FUN_10261026c(lVar12);
    if ((dVar16 < dVar22) || (lVar14 = local_60, dVar15 < dVar16)) goto LAB_1033bf8b4;
  }
  lVar10 = local_68;
  if (lVar14 != 0) {
    dVar15 = (double)FUN_1027afd40(local_68,lVar14);
    dVar22 = (double)FUN_10261026c(lVar10);
    if ((dVar22 < dVar15) ||
       ((double)CONCAT26(uVar21,CONCAT24(uVar20,CONCAT22(uVar19,uVar18))) < dVar22)) {
LAB_1033bf8b4:
      plVar13 = (logic_error *)___cxa_allocate_exception(0x10);
      std::logic_error::logic_error(plVar13,"Segment length out of range.");
                    /* WARNING: Subroutine does not return */
      ___cxa_throw(plVar13,PTR_typeinfo_1064f86a8,PTR__logic_error_1064f8540);
    }
  }
  FUN_1027baad8(param_1,local_68);
  if ((local_68 != 0) &&
     (iVar3 = *(int *)(local_68 + 8) + -1, *(int *)(local_68 + 8) = iVar3, iVar3 == 0)) {
    FUN_10128eea0();
  }
  if ((local_60 != 0) &&
     (iVar3 = *(int *)(local_60 + 8) + -1, *(int *)(local_60 + 8) = iVar3, iVar3 == 0)) {
    FUN_10128eea0();
  }
  if ((local_58 != 0) &&
     (iVar3 = *(int *)(local_58 + 8) + -1, *(int *)(local_58 + 8) = iVar3, iVar3 == 0)) {
    FUN_10128eea0();
  }
  return;
}

