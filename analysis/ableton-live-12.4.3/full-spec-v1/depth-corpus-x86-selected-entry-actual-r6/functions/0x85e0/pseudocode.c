
/* WARNING: Removing unreachable block (ram,0x00008c96) */
/* WARNING: Removing unreachable block (ram,0x00008ca6) */
/* WARNING: Removing unreachable block (ram,0x00008cb6) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 FUN_000085e0(long *param_1,undefined8 param_2,ulong *param_3,uint param_4,long param_5)

{
  float *pfVar1;
  undefined8 *puVar2;
  float *pfVar3;
  ulong uVar4;
  ulong uVar5;
  undefined8 *puVar6;
  undefined4 *puVar7;
  undefined4 *puVar8;
  long *plVar9;
  float fVar10;
  float fVar11;
  float fVar12;
  float fVar13;
  float fVar14;
  float fVar15;
  float fVar16;
  float fVar17;
  float fVar18;
  float fVar19;
  float fVar20;
  float fVar21;
  float fVar22;
  float fVar23;
  float fVar24;
  undefined4 uVar25;
  undefined4 uVar26;
  undefined4 uVar27;
  undefined8 uVar28;
  undefined8 uVar29;
  undefined8 uVar30;
  float fVar31;
  float fVar32;
  float fVar33;
  float fVar34;
  float fVar35;
  char cVar36;
  ulong uVar37;
  ulong uVar38;
  ulong uVar39;
  ulong uVar40;
  uint uVar41;
  long lVar42;
  long lVar43;
  uint uVar44;
  ulong uVar45;
  uint uVar46;
  ulong uVar47;
  ulong uVar48;
  int aiStack_78 [14];
  undefined8 uStack_40;
  uint uStack_38;
  undefined1 uStack_34;
  undefined1 uStack_33;
  undefined1 uStack_32;
  undefined1 uStack_31;
  
  uStack_40 = param_2;
  uStack_38 = param_4;
  cVar36 = (**(code **)(*(long *)param_1[7] + 0x10))((long *)param_1[7],aiStack_78);
  if (cVar36 != '\0') {
    do {
      if (aiStack_78[0] != 0) {
        func_0x00017050(param_1[8],aiStack_78);
      }
      cVar36 = (**(code **)(*(long *)param_1[7] + 0x10))((long *)param_1[7],aiStack_78);
    } while (cVar36 != '\0');
  }
  for (plVar9 = (long *)param_1[10]; plVar9 != (long *)0x0; plVar9 = (long *)plVar9[1]) {
    (**(code **)(*plVar9 + 0x50))(*plVar9,3,param_3);
  }
  if (param_5 != 0) {
    for (plVar9 = (long *)param_1[0xb]; plVar9 != (long *)0x0; plVar9 = (long *)plVar9[1]) {
      (**(code **)(*plVar9 + 0x50))(*plVar9,2,param_5);
    }
  }
  uVar28 = uStack_40;
  for (plVar9 = (long *)param_1[9]; plVar9 != (long *)0x0; plVar9 = (long *)plVar9[1]) {
    (**(code **)(*plVar9 + 0x50))(*plVar9,0,uVar28);
  }
  if (0 < (int)uStack_38) {
    uVar47 = *param_3;
    uVar48 = param_3[1];
    do {
      uVar46 = *(uint *)(param_1 + 3);
      if ((int)uStack_38 <= (int)*(uint *)(param_1 + 3)) {
        uVar46 = uStack_38;
      }
      (**(code **)(param_1[0x1e] + 8))(param_1[0x1e],uVar46);
      (**(code **)(param_1[0x1f] + 8))(param_1[0x1f],uVar46);
      (**(code **)(param_1[0x20] + 8))(param_1[0x20],uVar46);
      (**(code **)(param_1[0x21] + 8))(param_1[0x21],uVar46);
      (**(code **)(param_1[0x27] + 8))(param_1[0x27],uVar46);
      (**(code **)(param_1[0x23] + 8))(param_1[0x23],uVar46);
      (**(code **)(param_1[0x25] + 8))(param_1[0x25],uVar46);
      (**(code **)(param_1[0x22] + 8))(param_1[0x22],uVar46);
      (**(code **)(param_1[0x28] + 8))(param_1[0x28],uVar46);
      (**(code **)(param_1[0x24] + 8))(param_1[0x24],uVar46);
      (**(code **)(param_1[0x26] + 8))(param_1[0x26],uVar46);
      (**(code **)(param_1[0x29] + 8))(param_1[0x29],uVar46);
      (**(code **)(param_1[0x2a] + 8))(param_1[0x2a],uVar46);
      (**(code **)(param_1[0x2b] + 8))(param_1[0x2b],uVar46);
      uVar37 = func_0x0001cc30(param_1[0x2c],1);
      uVar38 = func_0x0001cc30(param_1[0x2c],2);
      fVar35 = _DAT_0002e270;
      fVar34 = _UNK_0002e26c;
      fVar33 = _UNK_0002e268;
      fVar32 = _UNK_0002e264;
      fVar31 = _DAT_0002e260;
      if (uVar37 == uVar38) {
        if ((int)uVar46 < 1) goto LAB_00008a20;
        if (uVar46 < 8) {
          uVar38 = 0;
        }
        else {
          uVar38 = (ulong)(uVar46 & 0xfffffff8);
          lVar42 = (uVar38 - 8 >> 3) + 1;
          uVar39 = (ulong)((uint)lVar42 & 1);
          if (uVar38 - 8 == 0) {
            lVar43 = 0;
LAB_000088f1:
            pfVar1 = (float *)(uVar37 + lVar43 * 4);
            fVar10 = pfVar1[1];
            fVar11 = pfVar1[2];
            fVar12 = pfVar1[3];
            pfVar3 = (float *)(uVar37 + 0x10 + lVar43 * 4);
            fVar13 = *pfVar3;
            fVar14 = pfVar3[1];
            fVar15 = pfVar3[2];
            fVar16 = pfVar3[3];
            pfVar3 = (float *)(uVar37 + lVar43 * 4);
            *pfVar3 = *pfVar1 * fVar31;
            pfVar3[1] = fVar10 * fVar32;
            pfVar3[2] = fVar11 * fVar33;
            pfVar3[3] = fVar12 * fVar34;
            pfVar1 = (float *)(uVar37 + 0x10 + lVar43 * 4);
            *pfVar1 = fVar13 * fVar31;
            pfVar1[1] = fVar14 * fVar32;
            pfVar1[2] = fVar15 * fVar33;
            pfVar1[3] = fVar16 * fVar34;
          }
          else {
            lVar42 = lVar42 - uVar39;
            lVar43 = 0;
            do {
              pfVar1 = (float *)(uVar37 + lVar43 * 4);
              fVar10 = pfVar1[1];
              fVar11 = pfVar1[2];
              fVar12 = pfVar1[3];
              pfVar3 = (float *)(uVar37 + 0x10 + lVar43 * 4);
              fVar13 = *pfVar3;
              fVar14 = pfVar3[1];
              fVar15 = pfVar3[2];
              fVar16 = pfVar3[3];
              pfVar3 = (float *)(uVar37 + 0x20 + lVar43 * 4);
              fVar17 = *pfVar3;
              fVar18 = pfVar3[1];
              fVar19 = pfVar3[2];
              fVar20 = pfVar3[3];
              pfVar3 = (float *)(uVar37 + 0x30 + lVar43 * 4);
              fVar21 = *pfVar3;
              fVar22 = pfVar3[1];
              fVar23 = pfVar3[2];
              fVar24 = pfVar3[3];
              pfVar3 = (float *)(uVar37 + lVar43 * 4);
              *pfVar3 = *pfVar1 * fVar31;
              pfVar3[1] = fVar10 * fVar32;
              pfVar3[2] = fVar11 * fVar33;
              pfVar3[3] = fVar12 * fVar34;
              pfVar1 = (float *)(uVar37 + 0x10 + lVar43 * 4);
              *pfVar1 = fVar13 * fVar31;
              pfVar1[1] = fVar14 * fVar32;
              pfVar1[2] = fVar15 * fVar33;
              pfVar1[3] = fVar16 * fVar34;
              pfVar1 = (float *)(uVar37 + 0x20 + lVar43 * 4);
              *pfVar1 = fVar17 * fVar31;
              pfVar1[1] = fVar18 * fVar32;
              pfVar1[2] = fVar19 * fVar33;
              pfVar1[3] = fVar20 * fVar34;
              pfVar1 = (float *)(uVar37 + 0x30 + lVar43 * 4);
              *pfVar1 = fVar21 * fVar31;
              pfVar1[1] = fVar22 * fVar32;
              pfVar1[2] = fVar23 * fVar33;
              pfVar1[3] = fVar24 * fVar34;
              lVar43 = lVar43 + 0x10;
              lVar42 = lVar42 + -2;
            } while (lVar42 != 0);
            if (uVar39 != 0) goto LAB_000088f1;
          }
          if (uVar38 == uVar46) goto LAB_00008a20;
        }
        do {
          *(float *)(uVar37 + uVar38 * 4) = *(float *)(uVar37 + uVar38 * 4) * fVar35;
          uVar38 = uVar38 + 1;
        } while (uVar38 < uVar46);
      }
      else if (0 < (int)uVar46) {
        uVar39 = (ulong)uVar46;
        if ((uVar46 < 8) || ((uVar37 < uVar38 + uVar39 * 4 && (uVar38 < uVar37 + uVar39 * 4)))) {
          uVar40 = 0;
        }
        else {
          uVar40 = (ulong)(uVar46 & 0xfffffff8);
          lVar42 = (uVar40 - 8 >> 3) + 1;
          uVar45 = (ulong)((uint)lVar42 & 1);
          if (uVar40 - 8 == 0) {
            lVar43 = 0;
LAB_000089e3:
            pfVar1 = (float *)(uVar37 + lVar43 * 4);
            fVar10 = pfVar1[1];
            fVar11 = pfVar1[2];
            fVar12 = pfVar1[3];
            pfVar3 = (float *)(uVar37 + 0x10 + lVar43 * 4);
            fVar13 = *pfVar3;
            fVar14 = pfVar3[1];
            fVar15 = pfVar3[2];
            fVar16 = pfVar3[3];
            pfVar3 = (float *)(uVar37 + lVar43 * 4);
            *pfVar3 = *pfVar1 * fVar31;
            pfVar3[1] = fVar10 * fVar32;
            pfVar3[2] = fVar11 * fVar33;
            pfVar3[3] = fVar12 * fVar34;
            pfVar1 = (float *)(uVar37 + 0x10 + lVar43 * 4);
            *pfVar1 = fVar13 * fVar31;
            pfVar1[1] = fVar14 * fVar32;
            pfVar1[2] = fVar15 * fVar33;
            pfVar1[3] = fVar16 * fVar34;
            pfVar1 = (float *)(uVar38 + lVar43 * 4);
            fVar10 = pfVar1[1];
            fVar11 = pfVar1[2];
            fVar12 = pfVar1[3];
            pfVar3 = (float *)(uVar38 + 0x10 + lVar43 * 4);
            fVar13 = *pfVar3;
            fVar14 = pfVar3[1];
            fVar15 = pfVar3[2];
            fVar16 = pfVar3[3];
            pfVar3 = (float *)(uVar38 + lVar43 * 4);
            *pfVar3 = *pfVar1 * fVar31;
            pfVar3[1] = fVar10 * fVar32;
            pfVar3[2] = fVar11 * fVar33;
            pfVar3[3] = fVar12 * fVar34;
            pfVar1 = (float *)(uVar38 + 0x10 + lVar43 * 4);
            *pfVar1 = fVar13 * fVar31;
            pfVar1[1] = fVar14 * fVar32;
            pfVar1[2] = fVar15 * fVar33;
            pfVar1[3] = fVar16 * fVar34;
          }
          else {
            lVar42 = lVar42 - uVar45;
            lVar43 = 0;
            do {
              pfVar1 = (float *)(uVar37 + lVar43 * 4);
              fVar10 = pfVar1[1];
              fVar11 = pfVar1[2];
              fVar12 = pfVar1[3];
              pfVar3 = (float *)(uVar37 + 0x10 + lVar43 * 4);
              fVar13 = *pfVar3;
              fVar14 = pfVar3[1];
              fVar15 = pfVar3[2];
              fVar16 = pfVar3[3];
              pfVar3 = (float *)(uVar37 + lVar43 * 4);
              *pfVar3 = *pfVar1 * fVar31;
              pfVar3[1] = fVar10 * fVar32;
              pfVar3[2] = fVar11 * fVar33;
              pfVar3[3] = fVar12 * fVar34;
              pfVar1 = (float *)(uVar37 + 0x10 + lVar43 * 4);
              *pfVar1 = fVar13 * fVar31;
              pfVar1[1] = fVar14 * fVar32;
              pfVar1[2] = fVar15 * fVar33;
              pfVar1[3] = fVar16 * fVar34;
              pfVar1 = (float *)(uVar38 + lVar43 * 4);
              fVar10 = pfVar1[1];
              fVar11 = pfVar1[2];
              fVar12 = pfVar1[3];
              pfVar3 = (float *)(uVar38 + 0x10 + lVar43 * 4);
              fVar13 = *pfVar3;
              fVar14 = pfVar3[1];
              fVar15 = pfVar3[2];
              fVar16 = pfVar3[3];
              pfVar3 = (float *)(uVar38 + lVar43 * 4);
              *pfVar3 = *pfVar1 * fVar31;
              pfVar3[1] = fVar10 * fVar32;
              pfVar3[2] = fVar11 * fVar33;
              pfVar3[3] = fVar12 * fVar34;
              pfVar1 = (float *)(uVar38 + 0x10 + lVar43 * 4);
              *pfVar1 = fVar13 * fVar31;
              pfVar1[1] = fVar14 * fVar32;
              pfVar1[2] = fVar15 * fVar33;
              pfVar1[3] = fVar16 * fVar34;
              pfVar1 = (float *)(uVar37 + 0x20 + lVar43 * 4);
              fVar10 = pfVar1[1];
              fVar11 = pfVar1[2];
              fVar12 = pfVar1[3];
              pfVar3 = (float *)(uVar37 + 0x30 + lVar43 * 4);
              fVar13 = *pfVar3;
              fVar14 = pfVar3[1];
              fVar15 = pfVar3[2];
              fVar16 = pfVar3[3];
              pfVar3 = (float *)(uVar37 + 0x20 + lVar43 * 4);
              *pfVar3 = *pfVar1 * fVar31;
              pfVar3[1] = fVar10 * fVar32;
              pfVar3[2] = fVar11 * fVar33;
              pfVar3[3] = fVar12 * fVar34;
              pfVar1 = (float *)(uVar37 + 0x30 + lVar43 * 4);
              *pfVar1 = fVar13 * fVar31;
              pfVar1[1] = fVar14 * fVar32;
              pfVar1[2] = fVar15 * fVar33;
              pfVar1[3] = fVar16 * fVar34;
              pfVar1 = (float *)(uVar38 + 0x20 + lVar43 * 4);
              fVar10 = pfVar1[1];
              fVar11 = pfVar1[2];
              fVar12 = pfVar1[3];
              pfVar3 = (float *)(uVar38 + 0x30 + lVar43 * 4);
              fVar13 = *pfVar3;
              fVar14 = pfVar3[1];
              fVar15 = pfVar3[2];
              fVar16 = pfVar3[3];
              pfVar3 = (float *)(uVar38 + 0x20 + lVar43 * 4);
              *pfVar3 = *pfVar1 * fVar31;
              pfVar3[1] = fVar10 * fVar32;
              pfVar3[2] = fVar11 * fVar33;
              pfVar3[3] = fVar12 * fVar34;
              pfVar1 = (float *)(uVar38 + 0x30 + lVar43 * 4);
              *pfVar1 = fVar13 * fVar31;
              pfVar1[1] = fVar14 * fVar32;
              pfVar1[2] = fVar15 * fVar33;
              pfVar1[3] = fVar16 * fVar34;
              lVar43 = lVar43 + 0x10;
              lVar42 = lVar42 + -2;
            } while (lVar42 != 0);
            if (uVar45 != 0) goto LAB_000089e3;
          }
          if (uVar40 == uVar39) goto LAB_00008a20;
        }
        do {
          *(float *)(uVar37 + uVar40 * 4) = *(float *)(uVar37 + uVar40 * 4) * fVar35;
          *(float *)(uVar38 + uVar40 * 4) = *(float *)(uVar38 + uVar40 * 4) * fVar35;
          uVar40 = uVar40 + 1;
        } while (uVar40 < uVar39);
      }
LAB_00008a20:
      uStack_38 = uStack_38 - uVar46;
      uVar38 = func_0x0001cc30(param_1[0x2c],1);
      uVar37 = func_0x0001cc30();
      if (uVar46 != 0) {
        uVar39 = (ulong)(uVar46 - 1);
        if (6 < uVar46 - 1) {
          uVar40 = uVar47 + 4 + uVar39 * 4;
          uVar45 = uVar48 + 4 + uVar39 * 4;
          uVar4 = uVar38 + 4 + uVar39 * 4;
          uVar5 = uVar37 + 4 + uVar39 * 4;
          uStack_34 = uVar47 < uVar45;
          uStack_33 = uVar48 < uVar40;
          uStack_32 = uVar38 < uVar40;
          uStack_31 = uVar37 < uVar40;
          if ((((!(bool)uStack_34 || !(bool)uStack_33) && (uVar4 <= uVar47 || !(bool)uStack_32)) &&
              (uVar5 <= uVar47 || !(bool)uStack_31)) &&
             ((uVar4 <= uVar48 || uVar45 <= uVar38 && (uVar5 <= uVar48 || uVar45 <= uVar37)))) {
            uVar40 = uVar39 + 1 & 0xfffffffffffffff8;
            lVar42 = (uVar40 - 8 >> 3) + 1;
            uVar45 = (ulong)((uint)lVar42 & 1);
            if (uVar40 - 8 == 0) {
              lVar43 = 0;
LAB_00008b83:
              puVar2 = (undefined8 *)(uVar38 + lVar43 * 4);
              uVar28 = puVar2[1];
              puVar6 = (undefined8 *)(uVar38 + 0x10 + lVar43 * 4);
              uVar29 = *puVar6;
              uVar30 = puVar6[1];
              puVar6 = (undefined8 *)(uVar47 + lVar43 * 4);
              *puVar6 = *puVar2;
              puVar6[1] = uVar28;
              puVar2 = (undefined8 *)(uVar47 + 0x10 + lVar43 * 4);
              *puVar2 = uVar29;
              puVar2[1] = uVar30;
              puVar7 = (undefined4 *)(uVar37 + lVar43 * 4);
              uVar25 = puVar7[1];
              uVar26 = puVar7[2];
              uVar27 = puVar7[3];
              puVar2 = (undefined8 *)(uVar37 + 0x10 + lVar43 * 4);
              uVar28 = *puVar2;
              uVar29 = puVar2[1];
              puVar8 = (undefined4 *)(uVar48 + lVar43 * 4);
              *puVar8 = *puVar7;
              puVar8[1] = uVar25;
              puVar8[2] = uVar26;
              puVar8[3] = uVar27;
              puVar2 = (undefined8 *)(uVar48 + 0x10 + lVar43 * 4);
              *puVar2 = uVar28;
              puVar2[1] = uVar29;
            }
            else {
              lVar42 = uVar45 - lVar42;
              lVar43 = 0;
              do {
                puVar2 = (undefined8 *)(uVar38 + lVar43 * 4);
                uVar28 = puVar2[1];
                puVar6 = (undefined8 *)(uVar38 + 0x10 + lVar43 * 4);
                uVar29 = *puVar6;
                uVar30 = puVar6[1];
                puVar6 = (undefined8 *)(uVar47 + lVar43 * 4);
                *puVar6 = *puVar2;
                puVar6[1] = uVar28;
                puVar2 = (undefined8 *)(uVar47 + 0x10 + lVar43 * 4);
                *puVar2 = uVar29;
                puVar2[1] = uVar30;
                puVar2 = (undefined8 *)(uVar37 + lVar43 * 4);
                uVar28 = puVar2[1];
                puVar6 = (undefined8 *)(uVar37 + 0x10 + lVar43 * 4);
                uVar29 = *puVar6;
                uVar30 = puVar6[1];
                puVar6 = (undefined8 *)(uVar48 + lVar43 * 4);
                *puVar6 = *puVar2;
                puVar6[1] = uVar28;
                puVar2 = (undefined8 *)(uVar48 + 0x10 + lVar43 * 4);
                *puVar2 = uVar29;
                puVar2[1] = uVar30;
                puVar2 = (undefined8 *)(uVar38 + 0x20 + lVar43 * 4);
                uVar28 = puVar2[1];
                puVar6 = (undefined8 *)(uVar38 + 0x30 + lVar43 * 4);
                uVar29 = *puVar6;
                uVar30 = puVar6[1];
                puVar6 = (undefined8 *)(uVar47 + 0x20 + lVar43 * 4);
                *puVar6 = *puVar2;
                puVar6[1] = uVar28;
                puVar2 = (undefined8 *)(uVar47 + 0x30 + lVar43 * 4);
                *puVar2 = uVar29;
                puVar2[1] = uVar30;
                puVar7 = (undefined4 *)(uVar37 + 0x20 + lVar43 * 4);
                uVar25 = puVar7[1];
                uVar26 = puVar7[2];
                uVar27 = puVar7[3];
                puVar2 = (undefined8 *)(uVar37 + 0x30 + lVar43 * 4);
                uVar28 = *puVar2;
                uVar29 = puVar2[1];
                puVar8 = (undefined4 *)(uVar48 + 0x20 + lVar43 * 4);
                *puVar8 = *puVar7;
                puVar8[1] = uVar25;
                puVar8[2] = uVar26;
                puVar8[3] = uVar27;
                puVar2 = (undefined8 *)(uVar48 + 0x30 + lVar43 * 4);
                *puVar2 = uVar28;
                puVar2[1] = uVar29;
                lVar43 = lVar43 + 0x10;
                lVar42 = lVar42 + 2;
              } while (lVar42 != 0);
              if (uVar45 != 0) goto LAB_00008b83;
            }
            uVar48 = uVar48 + uVar40 * 4;
            uVar47 = uVar47 + uVar40 * 4;
            if (uVar39 + 1 == uVar40) goto LAB_000086f0;
            uVar46 = uVar46 - (int)uVar40;
            uVar37 = uVar37 + uVar40 * 4;
            uVar38 = uVar38 + uVar40 * 4;
          }
        }
        uVar44 = uVar46 - 1;
        if ((uVar46 & 3) != 0) {
          lVar42 = 0;
          uVar41 = 0;
          do {
            *(undefined4 *)(uVar47 + lVar42) = *(undefined4 *)(uVar38 + lVar42);
            *(undefined4 *)(uVar48 + lVar42) = *(undefined4 *)(uVar37 + lVar42);
            uVar41 = uVar41 + 1;
            lVar42 = lVar42 + 4;
          } while ((uVar46 & 3) != uVar41);
          uVar46 = uVar46 - uVar41;
          uVar37 = uVar37 + lVar42;
          uVar38 = uVar38 + lVar42;
          uVar48 = uVar48 + lVar42;
          uVar47 = uVar47 + lVar42;
        }
        if (2 < uVar44) {
          lVar42 = 0;
          lVar43 = 0;
          do {
            *(undefined4 *)(uVar47 + lVar43 * 4) = *(undefined4 *)(uVar38 + lVar43 * 4);
            *(undefined4 *)(uVar48 + lVar43 * 4) = *(undefined4 *)(uVar37 + lVar43 * 4);
            *(undefined4 *)(uVar47 + 4 + lVar43 * 4) = *(undefined4 *)(uVar38 + 4 + lVar43 * 4);
            *(undefined4 *)(uVar48 + 4 + lVar43 * 4) = *(undefined4 *)(uVar37 + 4 + lVar43 * 4);
            *(undefined4 *)(uVar47 + 8 + lVar43 * 4) = *(undefined4 *)(uVar38 + 8 + lVar43 * 4);
            *(undefined4 *)(uVar48 + 8 + lVar43 * 4) = *(undefined4 *)(uVar37 + 8 + lVar43 * 4);
            *(undefined4 *)(uVar47 + 0xc + lVar43 * 4) = *(undefined4 *)(uVar38 + 0xc + lVar43 * 4);
            *(undefined4 *)(uVar48 + 0xc + lVar43 * 4) = *(undefined4 *)(uVar37 + 0xc + lVar43 * 4);
            lVar43 = lVar43 + 4;
            lVar42 = lVar42 + -0x10;
          } while (uVar46 != (uint)lVar43);
          uVar48 = uVar48 - lVar42;
          uVar47 = uVar47 - lVar42;
        }
      }
LAB_000086f0:
    } while (0 < (int)uStack_38);
  }
  (**(code **)(*param_1 + 0x88))(param_1,uStack_40);
  return 1;
}

