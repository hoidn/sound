
/* WARNING: Removing unreachable block (ram,0x00002d51) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined1
_CalcA(long param_1,ulong param_2,ulong param_3,ulong param_4,undefined8 param_5,undefined8 param_6,
      undefined8 param_7,uint *param_8)

{
  int *piVar1;
  float *pfVar2;
  float *pfVar3;
  int iVar4;
  float fVar5;
  float fVar6;
  float fVar7;
  uint uVar8;
  ulong uVar9;
  ulong uVar10;
  long lVar11;
  long lVar12;
  ulong unaff_RBX;
  ulong unaff_R12;
  uint unaff_R13D;
  uint *unaff_R14;
  ulong unaff_R15;
  bool bVar13;
  float fVar14;
  float fVar15;
  float fVar16;
  float fVar17;
  float fVar18;
  float fVar19;
  undefined1 uStack_49;
  ulong uStack_48;
  ulong uStack_40;
  long lStack_38;
  
  lStack_38 = *(long *)PTR____stack_chk_guard_00030070;
  if (param_1 != 0) {
    uStack_49 = 0;
    func_0x0000e910(param_5,param_6,*(undefined8 *)(param_1 + 0xe0028));
    unaff_R13D = *(uint *)(&UNK_00004010 + *(long *)(*(long *)(param_1 + 0xe0028) + 0x98));
    *(undefined8 *)(param_1 + 0xe0058) = param_7;
    uStack_48 = param_3;
    uStack_40 = param_4;
    if (param_8 == (uint *)0x0) goto LAB_00002a60;
    bVar13 = *param_8 != 0;
    goto LAB_00002a62;
  }
  param_3 = unaff_RBX;
  param_2 = unaff_R12;
  param_8 = unaff_R14;
  param_4 = unaff_R15;
  if (*(long *)PTR____stack_chk_guard_00030070 == lStack_38) {
    return 0;
  }
LAB_00002a5b:
  ___stack_chk_fail();
LAB_00002a60:
  bVar13 = false;
LAB_00002a62:
  uVar8 = func_0x00003820(param_1,&uStack_48,param_2 & 0xffffffff,bVar13,&uStack_49);
  if (unaff_R13D != 0) {
    if (*(long **)(param_1 + 8) != (long *)0x0) {
      (**(code **)(**(long **)(param_1 + 8) + 0x78))();
      unaff_R13D = uVar8;
    }
    if (0 < (long)param_2) {
      fVar14 = _DAT_0002e1b0 / (float)(long)param_2;
      if ((param_2 < 4) || ((param_3 < param_4 + param_2 * 4 && (param_4 < param_3 + param_2 * 4))))
      {
        uVar9 = 0;
        uVar10 = 0xffffffffffffffff;
        fVar15 = _DAT_0002e1b0;
      }
      else {
        uVar9 = param_2 & 0xfffffffffffffffc;
        fVar15 = fVar14 * _DAT_0002e1e0 + _DAT_0002e1f0;
        fVar16 = fVar14 * _UNK_0002e1e4 + _UNK_0002e1f4;
        fVar17 = fVar14 * _UNK_0002e1e8 + _UNK_0002e1f8;
        fVar18 = fVar14 * _UNK_0002e1ec + _UNK_0002e1fc;
        lVar11 = (uVar9 - 4 >> 2) + 1;
        uVar10 = (ulong)((uint)lVar11 & 1);
        if (uVar9 - 4 == 0) {
          lVar12 = 0;
LAB_00002c19:
          pfVar2 = (float *)(param_3 + lVar12 * 4);
          fVar19 = pfVar2[1];
          fVar5 = pfVar2[2];
          fVar6 = pfVar2[3];
          pfVar3 = (float *)(param_3 + lVar12 * 4);
          *pfVar3 = *pfVar2 * fVar15;
          pfVar3[1] = fVar19 * fVar16;
          pfVar3[2] = fVar5 * fVar17;
          pfVar3[3] = fVar6 * fVar18;
          pfVar2 = (float *)(param_4 + lVar12 * 4);
          fVar19 = pfVar2[1];
          fVar5 = pfVar2[2];
          fVar6 = pfVar2[3];
          pfVar3 = (float *)(param_4 + lVar12 * 4);
          *pfVar3 = *pfVar2 * fVar15;
          pfVar3[1] = fVar19 * fVar16;
          pfVar3[2] = fVar5 * fVar17;
          pfVar3[3] = fVar6 * fVar18;
        }
        else {
          fVar19 = _DAT_0002e1b4 * fVar14;
          lVar11 = lVar11 - uVar10;
          lVar12 = 0;
          do {
            pfVar2 = (float *)(param_3 + lVar12 * 4);
            fVar5 = pfVar2[1];
            fVar6 = pfVar2[2];
            fVar7 = pfVar2[3];
            pfVar3 = (float *)(param_3 + lVar12 * 4);
            *pfVar3 = *pfVar2 * fVar15;
            pfVar3[1] = fVar5 * fVar16;
            pfVar3[2] = fVar6 * fVar17;
            pfVar3[3] = fVar7 * fVar18;
            pfVar2 = (float *)(param_4 + lVar12 * 4);
            fVar5 = pfVar2[1];
            fVar6 = pfVar2[2];
            fVar7 = pfVar2[3];
            pfVar3 = (float *)(param_4 + lVar12 * 4);
            *pfVar3 = *pfVar2 * fVar15;
            pfVar3[1] = fVar5 * fVar16;
            pfVar3[2] = fVar6 * fVar17;
            pfVar3[3] = fVar7 * fVar18;
            fVar15 = fVar15 - fVar19;
            fVar16 = fVar16 - fVar19;
            fVar17 = fVar17 - fVar19;
            fVar18 = fVar18 - fVar19;
            pfVar2 = (float *)(param_3 + 0x10 + lVar12 * 4);
            fVar5 = pfVar2[1];
            fVar6 = pfVar2[2];
            fVar7 = pfVar2[3];
            pfVar3 = (float *)(param_3 + 0x10 + lVar12 * 4);
            *pfVar3 = *pfVar2 * fVar15;
            pfVar3[1] = fVar5 * fVar16;
            pfVar3[2] = fVar6 * fVar17;
            pfVar3[3] = fVar7 * fVar18;
            pfVar2 = (float *)(param_4 + 0x10 + lVar12 * 4);
            fVar5 = pfVar2[1];
            fVar6 = pfVar2[2];
            fVar7 = pfVar2[3];
            pfVar3 = (float *)(param_4 + 0x10 + lVar12 * 4);
            *pfVar3 = *pfVar2 * fVar15;
            pfVar3[1] = fVar5 * fVar16;
            pfVar3[2] = fVar6 * fVar17;
            pfVar3[3] = fVar7 * fVar18;
            lVar12 = lVar12 + 8;
            fVar15 = fVar15 - fVar19;
            fVar16 = fVar16 - fVar19;
            fVar17 = fVar17 - fVar19;
            fVar18 = fVar18 - fVar19;
            lVar11 = lVar11 + -2;
          } while (lVar11 != 0);
          if (uVar10 != 0) goto LAB_00002c19;
        }
        if (uVar9 == param_2) goto LAB_00002c3a;
        fVar15 = _DAT_0002e1b0 - (float)(long)uVar9 * fVar14;
        uVar10 = ~uVar9;
      }
      if ((param_2 & 1) != 0) {
        *(float *)(param_3 + uVar9 * 4) = *(float *)(param_3 + uVar9 * 4) * fVar15;
        *(float *)(param_4 + uVar9 * 4) = *(float *)(param_4 + uVar9 * 4) * fVar15;
        fVar15 = fVar15 - fVar14;
        uVar9 = uVar9 | 1;
      }
      if (uVar10 + param_2 != 0) {
        do {
          *(float *)(param_3 + uVar9 * 4) = *(float *)(param_3 + uVar9 * 4) * fVar15;
          *(float *)(param_4 + uVar9 * 4) = *(float *)(param_4 + uVar9 * 4) * fVar15;
          fVar15 = fVar15 - fVar14;
          *(float *)(param_3 + 4 + uVar9 * 4) = *(float *)(param_3 + 4 + uVar9 * 4) * fVar15;
          *(float *)(param_4 + 4 + uVar9 * 4) = *(float *)(param_4 + 4 + uVar9 * 4) * fVar15;
          fVar15 = fVar15 - fVar14;
          uVar9 = uVar9 + 2;
        } while (param_2 != uVar9);
      }
    }
  }
LAB_00002c3a:
  if ((param_8 != (uint *)0x0) && (*param_8 = uVar8 & 0xff, (uVar8 & 0xff) != 0))
  goto code_r0x00002c56;
  goto LAB_00002cd1;
code_r0x00002c56:
  lVar11 = 0;
  if (0 < (long)param_2) {
    do {
      fVar14 = *(float *)(param_3 + lVar11 * 4);
      if ((((_DAT_0002e1b8 < fVar14) || (fVar14 < _DAT_0002e1bc)) ||
          (fVar14 = *(float *)(param_4 + lVar11 * 4), _DAT_0002e1b8 < fVar14)) ||
         (fVar14 < _DAT_0002e1bc)) {
        *(undefined4 *)(param_1 + 0xe04fc) = *(undefined4 *)(param_1 + 0xe04f8);
        if (*(long *)PTR____stack_chk_guard_00030070 == lStack_38) {
          return uStack_49;
        }
        goto LAB_00002a5b;
      }
      lVar11 = lVar11 + 1;
    } while (lVar11 < (long)param_2);
  }
  piVar1 = (int *)(param_1 + 0xe04fc);
  iVar4 = *piVar1;
  *piVar1 = *piVar1 - (int)lVar11;
  if (*piVar1 == 0 || SBORROW4(iVar4,(int)lVar11) != *piVar1 < 0) {
    *param_8 = 0;
    *(undefined4 *)(param_1 + 0xe04fc) = 0;
    lVar11 = *(long *)PTR____stack_chk_guard_00030070;
  }
  else {
LAB_00002cd1:
    lVar11 = *(long *)PTR____stack_chk_guard_00030070;
  }
  if (lVar11 == lStack_38) {
    return uStack_49;
  }
  goto LAB_00002a5b;
}

