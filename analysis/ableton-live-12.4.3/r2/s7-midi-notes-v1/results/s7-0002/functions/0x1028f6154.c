
void FUN_1028f6154(undefined8 *param_1,long param_2)

{
  ulong uVar1;
  long lVar2;
  int iVar3;
  ulong uVar4;
  ulonglong *puVar5;
  undefined8 *puVar6;
  ulonglong uVar7;
  ulonglong *puVar8;
  long lVar9;
  ulong uVar10;
  ulong uVar11;
  long *plVar12;
  long lVar13;
  long *plVar14;
  undefined8 uVar15;
  size_t sVar16;
  ulonglong *puVar17;
  ulonglong *puVar18;
  long local_a0;
  __less a_Stack_98 [16];
  ulong local_88;
  long local_80;
  long local_78;
  long *local_70;
  ulong local_68;
  
  param_1[1] = 0;
  param_1[2] = 0;
  *param_1 = 0;
  local_a0 = param_2;
  uVar4 = FUN_102911034(&local_a0);
  if (uVar4 == 0) {
    puVar18 = (ulonglong *)0x0;
    puVar5 = (ulonglong *)0x0;
  }
  else {
    if (uVar4 >> 0x3d != 0) {
                    /* WARNING: Subroutine does not return */
      FUN_100d338b0(param_1);
    }
    puVar5 = operator_new(uVar4 << 3);
    puVar18 = puVar5 + uVar4;
    *param_1 = puVar5;
    param_1[1] = puVar5;
    param_1[2] = puVar18;
  }
  plVar12 = *(long **)(local_a0 + 0x430);
  puVar6 = (undefined8 *)(**(code **)(*plVar12 + 0x60))(plVar12);
  local_80 = (**(code **)*puVar6)(puVar6,plVar12);
  local_68 = 0;
  local_78 = local_80;
  local_70 = plVar12;
  FUN_1028eb274(a_Stack_98);
  FUN_1028eb274(a_Stack_98);
  uVar4 = local_68;
  plVar12 = local_70;
  lVar13 = local_78;
  lVar2 = local_80;
  plVar14 = *(long **)(local_a0 + 0x430);
  puVar6 = (undefined8 *)(**(code **)(*plVar14 + 0x60))(plVar14);
  local_80 = (**(code **)*puVar6)(puVar6,plVar14);
  local_68 = 0;
  local_78 = local_80;
  local_70 = plVar14;
  FUN_1028eb274(a_Stack_98);
  uVar11 = local_88;
  puVar17 = puVar5;
  if (uVar4 == 0) {
    puVar8 = (ulonglong *)*param_1;
    puVar5 = (ulonglong *)param_1[1];
  }
  else {
    do {
      uVar7 = FUN_1028da61c(uVar4);
      puVar8 = puVar17;
      if (uVar7 != 0) {
        if (puVar5 < puVar18) {
          *puVar5 = uVar7;
          puVar5 = puVar5 + 1;
        }
        else {
          sVar16 = (long)puVar5 - (long)puVar17;
          lVar9 = (long)sVar16 >> 3;
          uVar1 = lVar9 + 1;
          if (uVar1 >> 0x3d != 0) {
            param_1[1] = puVar5;
            param_1[2] = puVar18;
            *param_1 = puVar17;
                    /* WARNING: Subroutine does not return */
            FUN_100d338b0(param_1);
          }
          uVar10 = (long)puVar18 - (long)puVar17 >> 2;
          if (uVar10 <= uVar1) {
            uVar10 = uVar1;
          }
          if (0x7ffffffffffffff7 < (ulong)((long)puVar18 - (long)puVar17)) {
            uVar10 = 0x1fffffffffffffff;
          }
          if (uVar10 == 0) {
            puVar8 = (ulonglong *)0x0;
          }
          else {
            if (uVar10 >> 0x3d != 0) {
              param_1[1] = puVar5;
              param_1[2] = puVar18;
              *param_1 = puVar17;
                    /* WARNING: Subroutine does not return */
              FUN_10024a858();
            }
            puVar8 = operator_new(uVar10 << 3);
          }
          puVar18 = puVar8 + uVar10;
          puVar5 = puVar8 + lVar9 + 1;
          puVar8[lVar9] = uVar7;
          _memcpy(puVar8,puVar17,sVar16);
          if (puVar17 != (ulonglong *)0x0) {
            operator_delete(puVar17);
          }
        }
      }
      uVar4 = uVar4 + 0x30;
      if (uVar11 <= uVar4) {
        do {
          lVar13 = *(long *)(lVar13 + 0x18);
          if (lVar13 == lVar2) goto LAB_1028f6398;
          if (lVar13 == 0) {
            uVar15 = 0;
          }
          else {
            plVar14 = (long *)(**(code **)(*plVar12 + 0x60))(plVar12);
            lVar9 = (**(code **)(*plVar14 + 0x20))(plVar14,plVar12,lVar13);
            uVar15 = *(undefined8 *)(lVar9 + 8);
          }
          iVar3 = FUN_1028ac07c(uVar15);
        } while (iVar3 == 0);
        uVar15 = FUN_1028a89d0(uVar15);
        uVar4 = FUN_10155ee2c(uVar15,0);
        uVar11 = uVar4 + (long)iVar3 * 0x30;
      }
      puVar17 = puVar8;
    } while (uVar4 != 0);
LAB_1028f6398:
    param_1[1] = puVar5;
    param_1[2] = puVar18;
    *param_1 = puVar8;
  }
  std::__sort<std::__less<unsigned_long_long,unsigned_long_long>&,unsigned_long_long*>
            (puVar8,puVar5,a_Stack_98);
  return;
}

