// 0x101af9d50 FUN_101af9d50 state=exported body=[['0x101af9d50', '0x101af9ea0']]

double FUN_101af9d50(long *param_1,int param_2,int param_3,long param_4,long param_5,int param_6,
                    uint param_7,byte param_8,char param_9,char param_10)

{
  undefined8 uVar1;
  long lVar2;
  double dVar3;
  double dVar4;
  
  if (param_2 == 0) {
    return 0.0;
  }
  if (param_9 == '\0') {
    if (param_6 == 1) {
      return 0.0;
    }
  }
  else {
    uVar1 = (**(code **)(*param_1 + 0x28))();
    lVar2 = FUN_101adcf20(uVar1);
    if (*(char *)(lVar2 + 0x68) != '\x01') {
      return 0.0;
    }
    if (param_6 == 1) {
      return 0.0;
    }
    if (param_3 == -2) {
      return 0.0;
    }
    if (*(long *)(lVar2 + 0x98) == param_1[0x76]) {
      return 0.0;
    }
  }
  if (param_7 < 0xe) {
    uVar1 = (**(code **)(*param_1 + 0x28))();
    lVar2 = FUN_101adcf20(uVar1);
  }
  else {
    if (param_10 != '\0') {
      param_5 = param_4;
    }
    dVar4 = DAT_105b35858;
    if (((param_5 != 0) && (*(char *)(param_5 + 0x38) == '\x01')) && (1 < *(int *)(param_5 + 0x20)))
    {
      dVar4 = *(double *)(*(long *)(param_5 + 0x50) + 0x50);
    }
    dVar3 = 0.0;
    if (dVar4 >= 0.0) {
      dVar3 = dVar4;
    }
    if ((dVar4 < 0.0 & param_8) != 1) {
      return dVar3;
    }
    uVar1 = (**(code **)(*param_1 + 0x28))(dVar3);
    lVar2 = FUN_101adcf20(uVar1);
    uVar1 = FUN_101b3d010(*(undefined8 *)(param_1[3] + 0x20));
    param_7 = FUN_101b3e260(uVar1);
  }
  dVar4 = (double)FUN_101ad2ef0(lVar2 + 0x38,param_7);
  return dVar4;
}


