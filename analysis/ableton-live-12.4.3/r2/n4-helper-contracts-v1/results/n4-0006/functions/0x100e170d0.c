
void FUN_100e170d0(undefined8 *param_1,undefined1 param_2)

{
  undefined1 *puVar1;
  
  *param_1 = 0;
  param_1[1] = 0;
  param_1[2] = 0;
  puVar1 = operator_new(1);
  *param_1 = puVar1;
  *puVar1 = param_2;
  param_1[1] = puVar1 + 1;
  param_1[2] = puVar1 + 1;
  return;
}

