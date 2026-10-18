
void FUN_10143a290(undefined8 param_1,double param_2)

{
  int iVar1;
  int *local_28;
  
  if (-0.01 <= param_2) {
    if (param_2 <= 0.01) {
      FUN_101427680("C");
      return;
    }
    FUN_101431c60(&local_28,param_2 * 50.0,0,0);
    FUN_10142dd4c(param_1,&local_28,"R");
    if ((local_28 != (int *)0x0) && (iVar1 = *local_28, *local_28 = iVar1 + -1, iVar1 + -1 == 0)) {
      FUN_101449efc();
    }
  }
  else {
    FUN_101431c60(&local_28,param_2 * -50.0,0,0);
    FUN_10142dd4c(param_1,&local_28,"L");
    if ((local_28 != (int *)0x0) && (iVar1 = *local_28, *local_28 = iVar1 + -1, iVar1 + -1 == 0)) {
      FUN_101449efc();
    }
  }
  return;
}

