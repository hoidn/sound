
void FUN_101437334(undefined8 param_1,double param_2,long param_3)

{
  char *pcVar1;
  int iVar2;
  int iVar3;
  double dVar4;
  int *local_48;
  
  if (param_2 <= *(double *)(param_3 + 0x20) + 0.3) {
    FUN_101427680(&local_48,"-inf");
  }
  else {
    iVar3 = *(int *)(param_3 + 0x18);
    dVar4 = (double)___exp10((double)iVar3);
    dVar4 = (double)(long)(ABS(param_2) * dVar4) / dVar4;
    if (10.0 <= dVar4) {
      if (100.0 <= dVar4) {
        iVar3 = 0;
        iVar2 = 0;
      }
      else {
        iVar2 = iVar3 + -1;
        if (iVar3 < 1) {
          iVar2 = 0;
        }
        if (*(char *)(param_3 + 0x28) == '\0') {
          iVar3 = iVar2;
        }
        if ((*(char *)(param_3 + 0x29) != '\x01') ||
           (iVar2 = *(int *)(param_3 + 0x1c), *(int *)(param_3 + 0x1c) < 1)) {
          iVar2 = iVar3;
        }
      }
    }
    else {
      iVar2 = iVar3;
      if ((*(char *)(param_3 + 0x29) == '\x01') &&
         (iVar2 = *(int *)(param_3 + 0x1c), *(int *)(param_3 + 0x1c) < 1)) {
        iVar2 = iVar3;
      }
    }
    FUN_101431c6c(&local_48,param_2,0,CONCAT44(iVar3,iVar2));
  }
  pcVar1 = " dB";
  if (*(char *)(param_3 + 0x2a) == '\0') {
    pcVar1 = "";
  }
  FUN_10142dd4c(param_1,&local_48,pcVar1);
  if ((local_48 != (int *)0x0) && (iVar3 = *local_48, *local_48 = iVar3 + -1, iVar3 + -1 == 0)) {
    FUN_101449efc();
  }
  return;
}

