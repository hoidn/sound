
void FUN_101529908(long param_1,undefined8 *param_2)

{
  int iVar1;
  int *piVar2;
  int *piVar3;
  
  piVar3 = (int *)*param_2;
  if (piVar3 != (int *)0x0) {
    *piVar3 = *piVar3 + 1;
  }
  piVar2 = *(int **)(param_1 + 0x50);
  if ((piVar2 != (int *)0x0) && (iVar1 = *piVar2, *piVar2 = iVar1 + -1, iVar1 + -1 == 0)) {
    FUN_101449efc(piVar2);
    *(undefined8 *)(param_1 + 0x50) = *param_2;
    return;
  }
  *(int **)(param_1 + 0x50) = piVar3;
  return;
}

