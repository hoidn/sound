
void FUN_10146c0d4(undefined8 param_1,undefined8 param_2,undefined8 param_3)

{
  int iVar1;
  void *pvVar2;
  undefined8 *puVar3;
  long *plVar4;
  undefined8 uVar5;
  undefined8 uVar6;
  int *piVar7;
  long lVar8;
  long *plVar9;
  void *pvVar10;
  int *local_88;
  long *local_80;
  long *plStack_78;
  undefined8 local_70;
  void *pvStack_68;
  undefined8 uStack_60;
  undefined8 *local_58;
  undefined8 local_50;
  undefined4 local_48;
  undefined4 local_34;
  
  local_34 = 0x80000000;
  local_50 = 0;
  pvStack_68 = (void *)0x0;
  local_70 = 0;
  local_58 = (undefined8 *)0x0;
  uStack_60 = 0;
  plStack_78 = (long *)0x0;
  local_80 = (long *)0x0;
  local_48 = 0x3f800000;
  FUN_1011c4104();
  FUN_101427680(&local_88);
  uVar5 = FUN_1011c41c4();
  uVar6 = FUN_1011c41fc();
  FUN_10146c258(param_1,param_2,&local_88,uVar5,uVar6,param_3,&local_34,&local_80);
  pvVar2 = pvStack_68;
  puVar3 = local_58;
  if ((local_88 != (int *)0x0) && (iVar1 = *local_88, *local_88 = iVar1 + -1, iVar1 + -1 == 0)) {
    FUN_101449efc();
    pvVar2 = pvStack_68;
    puVar3 = local_58;
  }
  while (puVar3 != (void *)0x0) {
    pvVar10 = (void *)*puVar3;
    piVar7 = (int *)puVar3[2];
    pvStack_68 = pvVar2;
    if ((piVar7 != (int *)0x0) && (iVar1 = *piVar7, *piVar7 = iVar1 + -1, iVar1 + -1 == 0)) {
      FUN_101449efc();
    }
    operator_delete(puVar3);
    pvVar2 = pvStack_68;
    puVar3 = pvVar10;
  }
  pvStack_68 = (void *)0x0;
  if (pvVar2 != (void *)0x0) {
    operator_delete(pvVar2);
  }
  plVar4 = local_80;
  plVar9 = plStack_78;
  if (local_80 != (long *)0x0) {
    while (plVar9 != plVar4) {
      plVar9 = plVar9 + -1;
      lVar8 = *plVar9;
      *plVar9 = 0;
      if (lVar8 != 0) {
        FUN_101478454(plVar9);
      }
    }
    plStack_78 = plVar4;
    operator_delete(local_80);
  }
  return;
}

