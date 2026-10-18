
undefined1  [16]
FUN_101acffa4(long *param_1,int param_2,int param_3,long param_4,long param_5,int param_6,
             undefined8 param_7,int param_8,undefined8 param_9)

{
  long lVar1;
  undefined8 uVar2;
  double dVar3;
  undefined1 auVar4 [16];
  
  dVar3 = 0.0;
  if (param_2 == 0) goto LAB_101ad00e4;
  if ((char)param_9 == '\0') {
    if (param_6 == 1) goto LAB_101ad00e4;
  }
  else {
    (**(code **)(*param_1 + 0x28))(0);
    lVar1 = FUN_101ab4558();
    if (*(char *)(lVar1 + 0x68) != '\x01') {
      dVar3 = 0.0;
      goto LAB_101ad00e4;
    }
    dVar3 = 0.0;
    if (((param_6 == 1) || (param_3 == -2)) || (*(long *)(lVar1 + 0x98) == param_1[0x76]))
    goto LAB_101ad00e4;
  }
  if ((uint)param_7 < 0xe) {
    (**(code **)(*param_1 + 0x28))(0);
    lVar1 = FUN_101ab4558();
    auVar4 = FUN_101aaae44(lVar1 + 0x38,param_7);
    return auVar4;
  }
  if (param_9._1_1_ == '\0') {
    param_4 = param_5;
  }
  dVar3 = -1.0;
  if (((param_4 != 0) && (*(char *)(param_4 + 0x38) == '\x01')) && (1 < *(int *)(param_4 + 0x20))) {
    dVar3 = *(double *)(*(long *)(param_4 + 0x50) + 0x50);
  }
  if ((dVar3 < 0.0) && (dVar3 = 0.0, param_8 != 0)) {
    (**(code **)(*param_1 + 0x28))(0);
    lVar1 = FUN_101ab4558();
    FUN_101b0cf8c(*(undefined8 *)(param_1[3] + 0x20));
    uVar2 = FUN_101b0e1c0();
    auVar4 = FUN_101aaae44(lVar1 + 0x38,uVar2);
    return auVar4;
  }
LAB_101ad00e4:
  auVar4._8_8_ = 0;
  auVar4._0_8_ = dVar3;
  return auVar4;
}

