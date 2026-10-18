
void FUN_1018ed778(undefined8 param_1,long *param_2)

{
  int iVar1;
  long lVar2;
  long lVar3;
  long local_38;
  
  lVar2 = FUN_1014ed3e4();
  lVar3 = FUN_1012d9850(0x50);
  if (lVar2 != 0) {
    *(int *)(lVar2 + 8) = *(int *)(lVar2 + 8) + 1;
  }
  local_38 = lVar2;
  FUN_1014ea3fc(lVar3,&local_38);
  if (lVar3 != 0) {
    *(int *)(lVar3 + 8) = *(int *)(lVar3 + 8) + 1;
  }
  if (local_38 != 0) {
    iVar1 = *(int *)(local_38 + 8) + -1;
    *(int *)(local_38 + 8) = iVar1;
    if (iVar1 == 0) {
      FUN_10128eea0();
    }
  }
  FUN_1014ea68c(lVar3,1);
  FUN_1014ecba8(&local_38,lVar3);
  (**(code **)(*param_2 + 0xa0))(param_2,10,1);
  (**(code **)(*param_2 + 0x68))(param_2,1);
  FUN_101485c50(param_1,param_2,0,0xffffffff,0,0);
  (**(code **)(*param_2 + 0x70))(param_2);
  FUN_1014ecc88(&local_38);
  if (lVar3 != 0) {
    iVar1 = *(int *)(lVar3 + 8) + -1;
    *(int *)(lVar3 + 8) = iVar1;
    if (iVar1 == 0) {
      FUN_10128eea0(lVar3);
    }
  }
  return;
}

