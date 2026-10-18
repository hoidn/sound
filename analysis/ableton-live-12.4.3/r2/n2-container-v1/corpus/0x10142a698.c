
void FUN_10142a698(long *param_1,long param_2,long *param_3)

{
  char acVar1 [1];
  int iVar2;
  long lVar3;
  long local_30;
  long local_28;
  
  lVar3 = *param_3;
  acVar1[0] = s__105baf587[0];
  if (lVar3 != 0) {
    iVar2 = *(int *)(lVar3 + 4) / 2 + -1;
    if (3 < *(int *)(lVar3 + 4)) {
      if (*(short *)(lVar3 + 0x10) != 0x2f || iVar2 != 1) goto LAB_10142a6f0;
      iVar2 = 1;
    }
    acVar1[0] = "/"[iVar2];
  }
  if (acVar1[0] == '\0') {
    *param_1 = param_2;
    if (param_2 == 0) {
      return;
    }
    *(int *)(param_2 + 8) = *(int *)(param_2 + 8) + 1;
    return;
  }
LAB_10142a6f0:
  local_30 = param_2;
  FUN_10142a750(&local_28,&local_30);
  *param_1 = local_28;
  return;
}

