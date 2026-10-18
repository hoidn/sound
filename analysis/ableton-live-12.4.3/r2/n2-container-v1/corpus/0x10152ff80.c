
void FUN_10152ff80(long *param_1,long *param_2,undefined8 param_3,undefined8 *param_4)

{
  int iVar1;
  long lVar2;
  void *pvVar3;
  int *piVar4;
  int *piVar5;
  long lVar6;
  
  lVar2 = param_2[7];
  param_2[7] = 0;
  if (lVar2 != 0) {
    pvVar3 = (void *)FUN_10148dbd4();
    operator_delete(pvVar3);
  }
  lVar2 = param_2[10];
  lVar6 = param_2[0xb];
  while (lVar6 != lVar2) {
    lVar6 = lVar6 + -0x38;
    FUN_10148a13c(lVar6);
  }
  param_2[0xb] = lVar2;
  lVar2 = param_2[0xd];
  for (lVar6 = param_2[0xe]; lVar6 != lVar2; lVar6 = FUN_1014784fc(lVar6 + -0x38)) {
  }
  param_2[0xe] = lVar2;
  *(undefined1 *)(param_2 + 5) = 0;
  (**(code **)(*param_2 + 0x40))(param_2);
  if ((char)param_2[5] == '\x01') {
                    /* WARNING: Subroutine does not return */
    FUN_10148229c(param_2[3],param_2 + 6);
  }
  if (param_2[7] != 0) {
    FUN_1015146f0(param_2[7],param_2 + 10);
    lVar2 = param_2[7];
    param_2[7] = 0;
    *param_1 = lVar2;
    return;
  }
  lVar2 = FUN_101488e64(param_2[3],"No schema found");
  *(undefined1 *)(lVar2 + 0x28) = 1;
  piVar5 = (int *)*param_4;
  if (piVar5 != (int *)0x0) {
    *piVar5 = *piVar5 + 1;
  }
  piVar4 = *(int **)(lVar2 + 0x30);
  if ((piVar4 != (int *)0x0) && (iVar1 = *piVar4, *piVar4 = iVar1 + -1, iVar1 + -1 == 0)) {
    FUN_101449efc(piVar4);
    *(undefined8 *)(lVar2 + 0x30) = *param_4;
    return;
  }
  *(int **)(lVar2 + 0x30) = piVar5;
  return;
}

