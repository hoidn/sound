
void FUN_101529970(long param_1,undefined8 param_2,undefined8 *param_3)

{
  int iVar1;
  int *piVar2;
  int *piVar3;
  
  *(undefined1 *)(param_1 + 0x28) = 1;
  piVar3 = (int *)*param_3;
  if (piVar3 != (int *)0x0) {
    *piVar3 = *piVar3 + 1;
  }
  piVar2 = *(int **)(param_1 + 0x30);
  if ((piVar2 != (int *)0x0) && (iVar1 = *piVar2, *piVar2 = iVar1 + -1, iVar1 + -1 == 0)) {
    FUN_101449efc(piVar2);
    *(undefined8 *)(param_1 + 0x30) = *param_3;
    return;
  }
  *(int **)(param_1 + 0x30) = piVar3;
  return;
}

