
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_102610bc4(double param_1,long *param_2)

{
  double dVar1;
  double dVar2;
  double dVar3;
  undefined8 *puVar4;
  long lVar5;
  long *plVar6;
  long lVar7;
  long lVar8;
  undefined8 uVar9;
  undefined8 uVar10;
  long lVar11;
  long lVar12;
  undefined2 uVar13;
  undefined2 uVar14;
  undefined2 uVar15;
  undefined2 uVar16;
  ushort uVar17;
  double dVar18;
  double dVar19;
  double dVar20;
  double dVar21;
  double local_b0;
  
  puVar4 = (undefined8 *)(**(code **)(*param_2 + 0x60))();
  lVar5 = (**(code **)*puVar4)(puVar4,param_2);
  uVar9 = *(undefined8 *)(lVar5 + 0x18);
  puVar4 = (undefined8 *)(**(code **)(*param_2 + 0x60))(param_2);
  lVar5 = (**(code **)*puVar4)(puVar4,param_2);
  lVar8 = *(long *)(lVar5 + 0x20);
  plVar6 = (long *)(**(code **)(*param_2 + 0x60))(param_2);
  lVar5 = (**(code **)(*plVar6 + 0x20))(plVar6,param_2,lVar8);
  dVar19 = *(double *)(*(long *)(lVar5 + 8) + 0x58);
  plVar6 = (long *)(**(code **)(*param_2 + 0x60))(param_2);
  lVar5 = (**(code **)(*plVar6 + 0x20))(plVar6,param_2,uVar9);
  dVar21 = *(double *)(*(long *)(lVar5 + 8) + 0x58);
  puVar4 = (undefined8 *)(**(code **)(*param_2 + 0x60))(param_2);
  lVar5 = (**(code **)*puVar4)(puVar4,param_2);
  lVar11 = *(long *)(lVar5 + 0x18);
  puVar4 = (undefined8 *)(**(code **)(*param_2 + 0x60))(param_2);
  (**(code **)*puVar4)(puVar4,param_2);
  dVar3 = _UNK_1055d9698;
  dVar2 = _DAT_1055d9690;
  dVar20 = _UNK_1055d9688;
  dVar18 = _DAT_1055d9680;
  if (lVar11 != lVar5) {
    do {
      plVar6 = (long *)(**(code **)(*param_2 + 0x60))(param_2);
      lVar7 = (**(code **)(*plVar6 + 0x20))(plVar6,param_2,lVar11);
      lVar12 = *(long *)(lVar7 + 8);
      plVar6 = (long *)(**(code **)(*param_2 + 0x60))(param_2);
      lVar7 = (**(code **)(*plVar6 + 0x20))(plVar6,param_2,uVar9);
      dVar1 = *(double *)(*(long *)(lVar7 + 8) + 0x58);
      dVar1 = dVar1 + dVar1 * -param_1 + *(double *)(lVar12 + 0x58) * param_1;
      uVar13 = SUB82(dVar1,0);
      uVar14 = (undefined2)((ulong)dVar1 >> 0x10);
      uVar15 = (undefined2)((ulong)dVar1 >> 0x20);
      uVar16 = (undefined2)((ulong)dVar1 >> 0x30);
      uVar17 = NEON_umaxv(CONCAT26(-(ushort)(dVar1 == dVar3),
                                   CONCAT24(-(ushort)(dVar1 == dVar2),
                                            CONCAT22(-(ushort)(dVar1 == dVar20),
                                                     -(ushort)(dVar1 == dVar18)))),2);
      if ((uVar17 & 1) == 0) {
        uVar17 = 0x3ff0;
        if (dVar1 < 0.0) {
          uVar17 = 0xbff0;
        }
        dVar1 = (double)((ulong)uVar17 << 0x30) *
                ((double)(long)(ABS(dVar1 + (double)((ulong)uVar17 << 0x30) * 2.6015651015651016e-07
                                            * 0.5) * 3843840.0) / 3843840.0);
        uVar13 = SUB82(dVar1,0);
        uVar14 = (undefined2)((ulong)dVar1 >> 0x10);
        uVar15 = (undefined2)((ulong)dVar1 >> 0x20);
        uVar16 = (undefined2)((ulong)dVar1 >> 0x30);
      }
      *(ulong *)(lVar12 + 0x58) = CONCAT26(uVar16,CONCAT24(uVar15,CONCAT22(uVar14,uVar13)));
      lVar11 = *(long *)(lVar11 + 0x18);
    } while (lVar11 != lVar5);
  }
  uVar10 = *(undefined8 *)(lVar8 + 0x20);
  plVar6 = (long *)(**(code **)(*param_2 + 0x60))(param_2);
  lVar5 = (**(code **)(*plVar6 + 0x20))(plVar6,param_2,uVar10);
  local_b0 = *(double *)(*(long *)(lVar5 + 8) + 0x58) + 0.03125;
  uVar17 = NEON_umaxv(CONCAT26(-(ushort)(local_b0 == _UNK_1055d9698),
                               CONCAT24(-(ushort)(local_b0 == _DAT_1055d9690),
                                        CONCAT22(-(ushort)(local_b0 == _UNK_1055d9688),
                                                 -(ushort)(local_b0 == _DAT_1055d9680)))),2);
  if ((uVar17 & 1) == 0) {
    uVar17 = 0x3ff0;
    if (local_b0 < 0.0) {
      uVar17 = 0xbff0;
    }
    local_b0 = (double)((ulong)uVar17 << 0x30) *
               ((double)(long)(ABS(local_b0 +
                                   (double)((ulong)uVar17 << 0x30) * 2.6015651015651016e-07 * 0.5) *
                              3843840.0) / 3843840.0);
  }
  plVar6 = (long *)(**(code **)(*param_2 + 0x60))(param_2);
  lVar5 = (**(code **)(*plVar6 + 0x20))(plVar6,param_2,uVar9);
  dVar18 = (local_b0 - *(double *)(*(long *)(lVar5 + 8) + 0x58)) / ((dVar19 - dVar21) * param_1);
  plVar6 = (long *)(**(code **)(*param_2 + 0x60))(param_2);
  lVar5 = (**(code **)(*plVar6 + 0x20))(plVar6,param_2,lVar8);
  lVar11 = *(long *)(lVar5 + 8);
  plVar6 = (long *)(**(code **)(*param_2 + 0x60))(param_2);
  lVar5 = (**(code **)(*plVar6 + 0x20))(plVar6,param_2,uVar9);
  dVar20 = *(double *)(*(long *)(lVar5 + 8) + 0x50);
  plVar6 = (long *)(**(code **)(*param_2 + 0x60))(param_2);
  lVar5 = (**(code **)(*plVar6 + 0x20))(plVar6,param_2,lVar8);
  *(double *)(lVar11 + 0x50) =
       (dVar20 - dVar20 * dVar18) + *(double *)(*(long *)(lVar5 + 8) + 0x50) * dVar18;
  *(double *)(lVar11 + 0x58) = local_b0;
  return;
}

