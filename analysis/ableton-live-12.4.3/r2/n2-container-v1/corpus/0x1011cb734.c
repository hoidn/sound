
undefined8 * FUN_1011cb734(undefined8 *param_1)

{
  int iVar1;
  undefined8 *puVar2;
  int *piVar3;
  int *piVar4;
  
  FUN_101449838();
  puVar2 = DAT_106e0ca98;
  piVar4 = (int *)*DAT_106e0ca98;
  if (piVar4 != (int *)0x0) {
    *piVar4 = *piVar4 + 1;
  }
  piVar3 = (int *)*param_1;
  if ((piVar3 != (int *)0x0) && (iVar1 = *piVar3, *piVar3 = iVar1 + -1, iVar1 + -1 == 0)) {
    FUN_101449efc();
    *param_1 = *puVar2;
    return param_1;
  }
  *param_1 = piVar4;
  return param_1;
}

