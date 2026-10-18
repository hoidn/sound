
/* WARNING: Removing unreachable block (ram,0x000103169b2c) */
/* WARNING: Removing unreachable block (ram,0x000103169b40) */

uint FUN_103169978(long param_1,undefined8 param_2)

{
  int iVar1;
  uint uVar2;
  undefined8 uVar3;
  void *pvVar4;
  long *plVar5;
  long lVar6;
  int *piVar7;
  long *plVar8;
  undefined8 *puVar9;
  void *pvVar10;
  uint uVar11;
  undefined8 *puVar12;
  undefined8 *puVar13;
  void *pvVar14;
  undefined4 local_c4;
  undefined8 local_c0;
  undefined8 uStack_b8;
  undefined8 local_b0;
  undefined1 local_a0 [8];
  void *local_98;
  undefined8 uStack_90;
  undefined8 local_88;
  undefined8 uStack_80;
  undefined4 local_78;
  undefined1 uStack_69;
  undefined4 *local_68;
  
  iVar1 = FUN_1011b59ec();
  if (iVar1 == 2) {
    uVar11 = 0;
    goto LAB_103169bf4;
  }
  uVar3 = std::chrono::system_clock::now();
  FUN_103f3ffec(local_a0,2,uVar3);
  iVar1 = FUN_103f3c8b8(local_a0);
  if (iVar1 != 0) {
    FUN_103f39a78(local_a0,"PluginManager: Scan start ------------------");
  }
  thunk_FUN_103f395e4(local_a0);
  uStack_80 = 0;
  local_88 = 0;
  uStack_90 = 0;
  local_98 = (void *)0x0;
  local_78 = 0x3f800000;
  local_a0[0] = (undefined1)param_2;
  puVar12 = *(undefined8 **)(param_1 + 0xc0);
  puVar13 = *(undefined8 **)(param_1 + 200);
  if (puVar12 == puVar13) {
    FUN_1031693a4(param_1);
    puVar12 = *(undefined8 **)(param_1 + 0xc0);
    puVar13 = *(undefined8 **)(param_1 + 200);
    if (puVar12 == puVar13) goto LAB_103169b8c;
LAB_103169a1c:
    uVar11 = 0;
    do {
      plVar8 = (long *)*puVar12;
      plVar5 = (long *)(**(code **)(*plVar8 + 0x58))(plVar8);
      if (plVar5 == (long *)0x0) {
        uVar2 = (**(code **)(*plVar8 + 0x30))(plVar8,param_2);
        uVar11 = uVar11 | uVar2;
        if ((*(byte *)(param_1 + 0xd9) & 1) == 0) {
          (**(code **)(*plVar8 + 0x38))(plVar8);
        }
      }
      else {
        (**(code **)(*plVar5 + 0x18))(plVar5);
        (**(code **)(*plVar5 + 0x10))(&local_c0,plVar5);
        local_c4 = (**(code **)(*plVar8 + 0x10))(plVar8);
        local_68 = &local_c4;
        lVar6 = FUN_103177ccc(&local_98,&local_c4,PTR_piecewise_construct_106537430,&local_68,
                              &uStack_69);
        puVar9 = (undefined8 *)(lVar6 + 0x18);
        pvVar10 = (void *)*puVar9;
        if (pvVar10 != (void *)0x0) {
          pvVar14 = *(void **)(lVar6 + 0x20);
          pvVar4 = pvVar10;
          if (pvVar14 != pvVar10) {
            do {
              piVar7 = *(int **)((long)pvVar14 + -8);
              if ((piVar7 != (int *)0x0) && (iVar1 = *piVar7, *piVar7 = iVar1 + -1, iVar1 + -1 == 0)
                 ) {
                FUN_101449efc();
              }
              pvVar14 = (void *)((long)pvVar14 + -0x20);
            } while (pvVar14 != pvVar10);
            pvVar4 = (void *)*puVar9;
          }
          *(void **)(lVar6 + 0x20) = pvVar10;
          operator_delete(pvVar4);
          *puVar9 = 0;
          *(undefined8 *)(lVar6 + 0x20) = 0;
          *(undefined8 *)(lVar6 + 0x28) = 0;
        }
        *(undefined8 *)(lVar6 + 0x20) = uStack_b8;
        *(undefined8 *)(lVar6 + 0x18) = local_c0;
        *(undefined8 *)(lVar6 + 0x28) = local_b0;
      }
      puVar12 = puVar12 + 1;
    } while (puVar12 != puVar13);
  }
  else {
    if (puVar12 != puVar13) goto LAB_103169a1c;
LAB_103169b8c:
    uVar11 = 0;
  }
  FUN_103169770(param_1,local_a0);
  uVar3 = std::chrono::system_clock::now();
  FUN_103f3ffec(&local_c0,2,uVar3);
  iVar1 = FUN_103f3c8b8(&local_c0);
  if (iVar1 != 0) {
    FUN_103f39a78(&local_c0,"PluginManager: Scan end --------------------");
  }
  thunk_FUN_103f395e4(&local_c0);
  uVar11 = (uint)param_2 | uVar11;
  FUN_1031768f0(&local_98,local_88);
  pvVar10 = local_98;
  local_98 = (void *)0x0;
  if (pvVar10 != (void *)0x0) {
    operator_delete(pvVar10);
  }
LAB_103169bf4:
  return uVar11 & 1;
}

