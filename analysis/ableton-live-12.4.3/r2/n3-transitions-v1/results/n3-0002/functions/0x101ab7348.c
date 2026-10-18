
undefined8 *
FUN_101ab7348(undefined8 *param_1,int *param_2,undefined4 param_3,undefined4 param_4,
             undefined4 param_5)

{
  int iVar1;
  undefined8 uVar2;
  long lVar3;
  
  *(undefined4 *)(param_1 + 2) = param_3;
  *(undefined4 *)((long)param_1 + 0x14) = param_4;
  *param_1 = &PTR_FUN_106756188;
  param_1[1] = 0;
  *(undefined4 *)(param_1 + 3) = 0xffffffff;
  *(undefined4 *)((long)param_1 + 0x1c) = param_5;
  uVar2 = FUN_101aae14c();
  lVar3 = FUN_101aac7cc(uVar2,param_2,*(undefined4 *)(param_1 + 2),
                        *(undefined4 *)((long)param_1 + 0x14),*(undefined4 *)(param_1 + 3));
  param_1[1] = lVar3;
  if (lVar3 != 0) {
    return param_1;
  }
  iVar1 = *param_2;
  if (iVar1 == -1) {
    iVar1 = FUN_101a9c2d0(*(undefined8 *)(param_2 + 2));
    *param_2 = iVar1;
  }
  DAT_106f56460 = (undefined2)iVar1;
  DAT_106f56462 = 0;
  param_1[1] = &DAT_106f56460;
  return param_1;
}

