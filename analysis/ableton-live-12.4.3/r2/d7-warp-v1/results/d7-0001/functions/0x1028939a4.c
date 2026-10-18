
long FUN_1028939a4(long param_1,long *param_2)

{
  undefined8 uVar1;
  undefined8 uVar2;
  long lVar3;
  long lVar4;
  
  lVar4 = *(long *)(param_1 + 0x28);
  if (lVar4 == 0) {
    FUN_1027b4b08(param_2);
    uVar1 = FUN_102876f14();
    uVar2 = (**(code **)(*param_2 + 0x4b0))(param_2);
    uVar1 = FUN_10284cb18(uVar1);
    lVar4 = thunk_FUN_101a9b404(0x30);
    FUN_1022484b8(lVar4,uVar1);
    uVar1 = FUN_1022487c8(lVar4);
    FUN_10277b71c(uVar1,uVar2);
    lVar3 = *(long *)(param_1 + 0x28);
    *(long *)(param_1 + 0x28) = lVar4;
    if (lVar3 != 0) {
      FUN_101aa002c(lVar3,0x100500,1);
      return *(long *)(param_1 + 0x28);
    }
  }
  return lVar4;
}

