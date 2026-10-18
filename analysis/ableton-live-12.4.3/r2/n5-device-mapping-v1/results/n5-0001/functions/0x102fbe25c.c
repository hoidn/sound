
undefined8 * FUN_102fbe25c(long param_1)

{
  long lVar1;
  undefined4 uVar2;
  undefined8 uVar3;
  undefined8 *puVar4;
  long *plVar5;
  undefined8 *puVar6;
  
  if ((((((*(long *)(param_1 + 0x48) != 0) ||
         (FUN_102f998c4(param_1,param_1 + 0x58), *(long *)(param_1 + 0x48) != 0)) &&
        (*(code **)(param_1 + 0x18) != (code *)0x0)) &&
       ((*(long *)(param_1 + 0x20) != 0 && (*(long *)(param_1 + 0x28) != 0)))) &&
      ((*(long *)(param_1 + 0x30) != 0 &&
       ((*(long *)(param_1 + 0x38) != 0 && (*(long *)(param_1 + 0x40) != 0)))))) &&
     (*(int *)(param_1 + 0x80) != 0)) {
    uVar3 = (**(code **)(param_1 + 0x18))();
    puVar4 = (undefined8 *)thunk_FUN_101aa0448(0x38);
    plVar5 = puVar4 + 1;
    *plVar5 = 0;
    *puVar4 = &PTR_FUN_1068b8290;
    puVar6 = puVar4 + 2;
    puVar4[3] = 0;
    *puVar6 = 0;
    puVar4[5] = 0;
    puVar4[4] = 0;
    *(undefined4 *)(puVar4 + 6) = 0xac44;
    LOAcquire();
    lVar1 = *plVar5;
    *plVar5 = lVar1 + 1;
    LORelease();
    *puVar6 = uVar3;
    uVar3 = *(undefined8 *)(param_1 + 0x30);
    puVar4[4] = *(undefined8 *)(param_1 + 0x38);
    puVar4[3] = uVar3;
    puVar4[5] = param_1;
    FUN_101a45218(lVar1);
    uVar2 = FUN_101a46974();
    *(undefined4 *)(puVar4 + 6) = uVar2;
    if (puVar4[5] != 0) {
      FUN_102fbe580(puVar4[5],*puVar6);
    }
    *(int *)(param_1 + 0x50) = *(int *)(param_1 + 0x50) + 1;
    return puVar4;
  }
  return (undefined8 *)0x0;
}

