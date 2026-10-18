// 0x1002b5da4 FUN_1002b5da4 exported  sig: undefined FUN_1002b5da4()

void FUN_1002b5da4(undefined8 *param_1,undefined8 *param_2)

{
  undefined8 *puVar1;
  int iVar2;
  undefined8 uVar3;
  int *local_28;
  
  *param_1 = 0;
  param_1[1] = 0;
  param_1[2] = 0;
  FUN_10025ca80(param_1,1);
  local_28 = (int *)*param_2;
  *param_2 = 0;
  puVar1 = (undefined8 *)param_1[1];
  if (puVar1 < (undefined8 *)param_1[2]) {
    *puVar1 = local_28;
    param_1[1] = puVar1 + 1;
    return;
  }
  uVar3 = FUN_1002b614c(param_1,&local_28);
  param_1[1] = uVar3;
  if (local_28 != (int *)0x0) {
    iVar2 = *local_28;
    *local_28 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  return;
}


