
void FUN_1015743b0(undefined4 param_1,undefined4 param_2,undefined4 param_3,long param_4,
                  long param_5,undefined8 param_6)

{
  int iVar1;
  long lVar2;
  
  *(undefined4 *)(param_4 + 0x80) = param_1;
  *(undefined4 *)(param_4 + 0x84) = param_2;
  *(undefined4 *)(param_4 + 0x88) = param_3;
  if (param_5 != 0) {
    *(int *)(param_5 + 8) = *(int *)(param_5 + 8) + 1;
  }
  lVar2 = *(long *)(param_4 + 0x78);
  if ((lVar2 != 0) && (iVar1 = *(int *)(lVar2 + 8) + -1, *(int *)(lVar2 + 8) = iVar1, iVar1 == 0)) {
    FUN_10128eea0(lVar2);
  }
  *(long *)(param_4 + 0x78) = param_5;
  FUN_101568960(param_3,param_4,param_6);
  return;
}

