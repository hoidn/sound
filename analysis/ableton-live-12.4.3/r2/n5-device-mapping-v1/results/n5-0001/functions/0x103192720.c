
void FUN_103192720(undefined4 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4,
                  undefined8 param_5,undefined8 param_6,undefined8 param_7)

{
  int iVar1;
  int *local_60;
  int *local_58;
  
  FUN_101427680(&local_58,param_4);
  FUN_101427680(&local_60,param_6);
  FUN_103197830(param_1,param_2,param_3,&local_58,param_5,&local_60,param_7,0);
  if (local_60 != (int *)0x0) {
    iVar1 = *local_60;
    *local_60 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_58 != (int *)0x0) {
    iVar1 = *local_58;
    *local_58 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  return;
}

