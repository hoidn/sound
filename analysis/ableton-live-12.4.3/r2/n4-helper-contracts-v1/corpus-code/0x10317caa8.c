// 0x10317caa8 FUN_10317caa8 exported  sig: undefined FUN_10317caa8()

void FUN_10317caa8(undefined8 *param_1,undefined8 *param_2,undefined8 param_3,undefined8 param_4,
                  undefined8 param_5)

{
  int iVar1;
  int *local_48;
  
  *param_1 = 0;
  param_1[1] = 0;
  param_1[2] = 0;
  FUN_10025ca80(param_1,4);
  local_48 = (int *)*param_2;
  *param_2 = 0;
  FUN_10317cb74(param_1,&local_48,param_3,param_4,param_5);
  if (local_48 != (int *)0x0) {
    iVar1 = *local_48;
    *local_48 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  return;
}


