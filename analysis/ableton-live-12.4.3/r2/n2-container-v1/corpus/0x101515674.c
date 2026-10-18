
void FUN_101515674(long param_1)

{
  int *piVar1;
  int *piVar2;
  int iVar3;
  undefined8 *puVar4;
  long *plVar5;
  undefined8 uVar6;
  int *local_40;
  int *local_38;
  
  piVar2 = *(int **)(param_1 + 0x10);
  for (piVar1 = *(int **)(param_1 + 8); piVar1 != piVar2; piVar1 = piVar1 + 0xe) {
    FUN_1014812d8(piVar1);
    puVar4 = (undefined8 *)FUN_10120e26c();
    local_40 = (int *)*puVar4;
    if (local_40 != (int *)0x0) {
      *local_40 = *local_40 + 1;
    }
    local_38 = piVar1;
    FUN_10152417c(param_1 + 0x20,&local_40,&local_40);
    if ((local_40 != (int *)0x0) && (iVar3 = *local_40, *local_40 = iVar3 + -1, iVar3 + -1 == 0)) {
      FUN_101449efc();
    }
    plVar5 = (long *)FUN_1014812dc(piVar1);
    if ((*plVar5 == 0) || ((*(uint *)(*plVar5 + 4) & 0xfffffffe) != 2)) {
      uVar6 = FUN_1014812dc(piVar1);
    }
    else {
      FUN_1014812d8(piVar1);
      uVar6 = FUN_10120e26c();
    }
    local_40 = piVar1;
    FUN_101524878(param_1 + 0x48,uVar6,uVar6,&local_40);
  }
  return;
}

