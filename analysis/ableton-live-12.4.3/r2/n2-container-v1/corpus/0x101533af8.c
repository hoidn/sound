
void FUN_101533af8(undefined8 *param_1)

{
  int iVar1;
  long lVar2;
  int *piVar3;
  undefined8 *puVar4;
  undefined8 *puVar5;
  undefined8 *puVar6;
  
  *param_1 = &PTR_thunk_FUN_101533af8_106676ee0;
  if ((long *)param_1[0x1a] != (long *)0x0) {
    (**(code **)(*(long *)param_1[0x1a] + 0x18))();
    lVar2 = param_1[0x1a];
    if (lVar2 != 0) {
      iVar1 = *(int *)(lVar2 + 8) + -1;
      *(int *)(lVar2 + 8) = iVar1;
      if (iVar1 == 0) {
        FUN_10128eea0();
      }
    }
  }
  piVar3 = (int *)param_1[0x18];
  if (piVar3 != (int *)0x0) {
    iVar1 = *piVar3;
    *piVar3 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  lVar2 = param_1[0x14];
  if (lVar2 != 0) {
    iVar1 = *(int *)(lVar2 + 8) + -1;
    *(int *)(lVar2 + 8) = iVar1;
    if (iVar1 == 0) {
      FUN_10128eea0();
    }
  }
  FUN_101532c6c(param_1 + 0xd);
  puVar5 = (undefined8 *)param_1[0xe];
  puVar6 = (undefined8 *)param_1[0xf];
  if (puVar5 != puVar6) {
    do {
      puVar4 = puVar5 + 1;
      operator_delete((void *)*puVar5);
      puVar5 = puVar4;
    } while (puVar4 != puVar6);
    puVar5 = (undefined8 *)param_1[0xe];
    puVar6 = (undefined8 *)param_1[0xf];
  }
  if (puVar6 != puVar5) {
    param_1[0xf] = (long)puVar6 + ((long)puVar5 + (7 - (long)puVar6) & 0xfffffffffffffff8U);
  }
  if ((void *)param_1[0xd] != (void *)0x0) {
    operator_delete((void *)param_1[0xd]);
  }
  piVar3 = (int *)param_1[10];
  if (piVar3 != (int *)0x0) {
    iVar1 = *piVar3;
    *piVar3 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  piVar3 = (int *)param_1[9];
  if (piVar3 != (int *)0x0) {
    iVar1 = *piVar3;
    *piVar3 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  piVar3 = (int *)param_1[7];
  if (piVar3 != (int *)0x0) {
    iVar1 = *piVar3;
    *piVar3 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  piVar3 = (int *)param_1[6];
  if (piVar3 != (int *)0x0) {
    iVar1 = *piVar3;
    *piVar3 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  *param_1 = &PTR_FUN_106672398;
  lVar2 = param_1[4];
  if (lVar2 != 0) {
    iVar1 = *(int *)(lVar2 + 8) + -1;
    *(int *)(lVar2 + 8) = iVar1;
    if (iVar1 == 0) {
      FUN_10128eea0();
    }
  }
  lVar2 = param_1[3];
  if (lVar2 != 0) {
    iVar1 = *(int *)(lVar2 + 8) + -1;
    *(int *)(lVar2 + 8) = iVar1;
    if (iVar1 == 0) {
      FUN_10128eea0();
    }
  }
  FUN_10128edf8(param_1);
  return;
}

