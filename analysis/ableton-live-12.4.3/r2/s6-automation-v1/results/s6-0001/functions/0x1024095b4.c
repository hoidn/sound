
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1024095b4(undefined1 param_1 [16],undefined1 param_2 [16],undefined8 param_3,
                  undefined8 param_4,float *param_5,double *param_6,long *param_7,undefined8 param_8
                  ,undefined8 param_9)

{
  undefined8 uVar1;
  undefined8 uVar2;
  bool bVar3;
  int iVar4;
  long *plVar5;
  long lVar6;
  long lVar7;
  long *plVar8;
  undefined4 uVar9;
  float fVar10;
  float fVar11;
  double dVar12;
  undefined8 uVar13;
  double dVar14;
  undefined2 uVar15;
  ushort uVar16;
  undefined2 uVar17;
  undefined2 uVar18;
  undefined2 uVar19;
  double dVar20;
  double dVar21;
  double dVar22;
  long local_c0;
  long lStack_b8;
  long *local_b0;
  float local_a8 [2];
  undefined8 local_a0;
  long *plStack_98;
  undefined8 uStack_90;
  undefined8 uStack_88;
  
  (**(code **)(*param_7 + 0x3c8))(&local_c0,*param_6,param_7,param_8);
  lVar7 = lStack_b8;
  if (lStack_b8 == local_c0) {
    (**(code **)(*param_7 + 0x428))(local_a8,param_7);
    plVar5 = (long *)(**(code **)(*plStack_98 + 0x60))();
    lVar7 = (**(code **)(*plVar5 + 0x20))(plVar5,plStack_98,local_a0);
    dVar12 = *param_6;
    local_a8[0] = (float)(**(code **)(**(long **)(lVar7 + 8) + 0x1f0))();
    uVar9 = FUN_102778f50(dVar12,param_9,local_a8);
    FUN_102778d24(param_9);
    fVar10 = (float)FUN_101574bb0(uVar9);
  }
  else {
    plVar5 = (long *)(**(code **)(*local_b0 + 0x60))();
    lVar6 = (**(code **)(*plVar5 + 0x20))(plVar5,local_b0,lVar7);
    lVar7 = lStack_b8;
    dVar12 = *param_6;
    uVar15 = SUB82(dVar12,0);
    uVar17 = (undefined2)((ulong)dVar12 >> 0x10);
    uVar18 = (undefined2)((ulong)dVar12 >> 0x20);
    uVar19 = (undefined2)((ulong)dVar12 >> 0x30);
    if (*(double *)(*(long *)(lVar6 + 8) + 0x50) == dVar12) {
      plVar5 = (long *)0x0;
      if ((lStack_b8 != 0) && (lStack_b8 != local_c0)) {
        plVar5 = (long *)(**(code **)(*local_b0 + 0x60))();
        lVar7 = (**(code **)(*plVar5 + 0x20))(plVar5,local_b0,lVar7);
        plVar5 = *(long **)(lVar7 + 8);
      }
      if (lStack_b8 == *(long *)(local_c0 + 0x20)) {
        lVar7 = 0;
      }
      else {
        lVar6 = *(long *)(lStack_b8 + 0x18);
        lVar7 = 0;
        if (lVar6 != 0) {
          plVar8 = (long *)(**(code **)(*local_b0 + 0x60))();
          lVar7 = (**(code **)(*plVar8 + 0x20))(plVar8,local_b0,lVar6);
          lVar7 = *(long *)(lVar7 + 8);
        }
      }
      lVar6 = plVar5[10];
      local_a8[0] = (float)(**(code **)(*plVar5 + 0x1f0))(plVar5);
      uVar9 = FUN_102778f50(lVar6,param_9,local_a8);
      FUN_102778d24(param_9);
      fVar10 = (float)FUN_101574bb0(uVar9);
      iVar4 = FUN_1027778a4(plVar5);
      if ((iVar4 == 0) || (lVar7 == 0)) {
        plVar5 = (long *)(**(code **)(*local_b0 + 0x60))();
        lVar7 = (**(code **)(*plVar5 + 0x20))(plVar5,local_b0,lStack_b8);
        uVar13 = (**(code **)(**(long **)(lVar7 + 8) + 0x218))();
        *param_5 = fVar10;
        *(undefined8 *)(param_5 + 2) = uVar13;
        *(ulong *)(param_5 + 4) = CONCAT26(uVar19,CONCAT24(uVar18,CONCAT22(uVar17,uVar15)));
        *(undefined8 *)(param_5 + 6) = param_3;
        *(undefined8 *)(param_5 + 8) = param_4;
        return;
      }
      dVar12 = (double)plVar5[10];
      uVar16 = NEON_umaxv(CONCAT26(-(ushort)(dVar12 == _UNK_1055d9698),
                                   CONCAT24(-(ushort)(dVar12 == _DAT_1055d9690),
                                            CONCAT22(-(ushort)(dVar12 == _UNK_1055d9688),
                                                     -(ushort)(dVar12 == _DAT_1055d9680)))),2);
      if ((uVar16 & 1) == 0) {
        uVar16 = 0x3ff0;
        if (dVar12 < 0.0) {
          uVar16 = 0xbff0;
        }
        dVar12 = (double)((ulong)uVar16 << 0x30) *
                 ((double)(long)(ABS(dVar12 + (double)((ulong)uVar16 << 0x30) *
                                              2.6015651015651016e-07 * 0.5) * 3843840.0) / 3843840.0
                 );
      }
      FUN_102404218(local_a8,dVar12,SUB82(param_6[1],0),plVar5,lVar7,param_9);
      *param_5 = fVar10;
LAB_102409894:
      *(long **)(param_5 + 4) = plStack_98;
      *(undefined8 *)(param_5 + 2) = local_a0;
      *(undefined8 *)(param_5 + 8) = uStack_88;
      *(undefined8 *)(param_5 + 6) = uStack_90;
      return;
    }
    uVar13 = FUN_102778d24(param_9);
    if (lStack_b8 == *(long *)(local_c0 + 0x18)) {
      plVar5 = (long *)0x0;
    }
    else {
      lVar7 = *(long *)(lStack_b8 + 0x20);
      plVar5 = (long *)0x0;
      if (lVar7 != 0) {
        plVar5 = (long *)(**(code **)(*local_b0 + 0x60))();
        lVar7 = (**(code **)(*plVar5 + 0x20))(plVar5,local_b0,lVar7);
        plVar5 = *(long **)(lVar7 + 8);
      }
    }
    plVar8 = (long *)0x0;
    if ((lStack_b8 != 0) && (plVar8 = (long *)0x0, lStack_b8 != local_c0)) {
      plVar8 = (long *)(**(code **)(*local_b0 + 0x60))();
      lVar7 = (**(code **)(*plVar8 + 0x20))(plVar8,local_b0,lStack_b8);
      plVar8 = *(long **)(lVar7 + 8);
    }
    fVar10 = (float)(**(code **)(*plVar5 + 0x1f0))(plVar5);
    fVar11 = (float)(**(code **)(*plVar8 + 0x1f0))(plVar8);
    if (fVar10 == fVar11) {
      dVar12 = *param_6;
      local_a8[0] = (float)(**(code **)(*plVar5 + 0x1f0))(plVar5);
      FUN_102778f50(dVar12,param_9,local_a8);
      fVar10 = (float)FUN_101574bb0(uVar13);
    }
    else {
      iVar4 = FUN_1027778a4(plVar5);
      if (iVar4 != 0) {
        FUN_102404218(local_a8,*param_6,SUB82(param_6[1],0),plVar5,plVar8,param_9);
        *param_5 = local_a8[0];
        goto LAB_102409894;
      }
      (**(code **)(*plVar5 + 0x1f0))(plVar5);
      fVar10 = (float)FUN_101574bb0(uVar13);
      (**(code **)(*plVar8 + 0x1f0))(plVar8);
      fVar11 = (float)FUN_101574bb0(uVar13);
      dVar14 = *param_6;
      dVar20 = (double)plVar5[10];
      dVar22 = (double)plVar8[10];
      dVar21 = (double)fVar10;
      dVar12 = (double)fVar11;
      bVar3 = false;
      if ((dVar20 == dVar21) && (bVar3 = false, !NAN(dVar22) && !NAN(dVar12))) {
        bVar3 = dVar22 == dVar12;
      }
      if (!bVar3) {
        dVar14 = (dVar14 - dVar20) / (dVar22 - dVar20);
        dVar14 = (dVar21 - dVar21 * dVar14) + dVar12 * dVar14;
      }
      local_a8[0] = (float)dVar14;
      fVar10 = (float)FUN_102779088(param_9,local_a8);
    }
  }
  *param_5 = fVar10;
  uVar2 = _UNK_10587de28;
  uVar1 = _DAT_10587de20;
  uVar13 = _DAT_10587de10;
  *(undefined8 *)(param_5 + 4) = _UNK_10587de18;
  *(undefined8 *)(param_5 + 2) = uVar13;
  *(undefined8 *)(param_5 + 8) = uVar2;
  *(undefined8 *)(param_5 + 6) = uVar1;
  return;
}

