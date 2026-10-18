// arm 0x1027684bc FUN_1027684bc state=exported chunk=chunk-01921.jsonl code_sha256=659887e8d8f9bddd5d26443d1cdbcf181733afeaaf27fcfffebc32f7f82eecb9

void FUN_1027684bc(long param_1)

{
  int iVar1;
  ulong uVar2;
  long *plVar3;
  long lVar4;
  undefined8 uVar5;
  undefined8 uVar6;
  undefined8 uVar7;
  
  if (((*(long *)(param_1 + 0x8c8) == 0) || (uVar2 = FUN_101a4abac(), (uVar2 & 1) == 0)) &&
     (iVar1 = FUN_1015645a0(*(undefined8 *)(param_1 + 0xf0)), iVar1 == 0)) {
    plVar3 = (long *)thunk_FUN_101849958();
    (**(code **)(*plVar3 + 0x998))();
    FUN_10268bd44(*(undefined8 *)(param_1 + 0x48));
    iVar1 = FUN_1026de548();
    if (iVar1 != 0) {
      iVar1 = FUN_1015645a0(*(undefined8 *)(param_1 + 0x788));
      if (iVar1 != 0) {
        FUN_102767b70(param_1);
      }
      if (((*(long *)(param_1 + 0x48) == 0) ||
          (plVar3 = (long *)FUN_10268b7cc(), plVar3 == (long *)0x0)) ||
         (lVar4 = (**(code **)(*plVar3 + 0x198))(), lVar4 == 0)) {
        uVar5 = 0;
      }
      else {
        uVar5 = FUN_102336410();
      }
      FUN_10268bd44(*(undefined8 *)(param_1 + 0x48));
      uVar6 = FUN_1026de350();
      FUN_10268bd44(*(undefined8 *)(param_1 + 0x48));
      uVar7 = FUN_1026de558();
      FUN_101a4b40c(uVar6,uVar7,uVar5,1);
      return;
    }
    FUN_10268bd44(*(undefined8 *)(param_1 + 0x48));
    iVar1 = FUN_1026df618();
    uVar5 = 0;
    if (iVar1 != 0) {
      FUN_10268bd44(*(undefined8 *)(param_1 + 0x48));
      uVar5 = FUN_1026de350();
    }
    uVar6 = 0;
    if (((*(long *)(param_1 + 0x48) != 0) &&
        (plVar3 = (long *)FUN_10268b7cc(), uVar6 = 0, plVar3 != (long *)0x0)) &&
       (lVar4 = (**(code **)(*plVar3 + 0x198))(), uVar6 = 0, lVar4 != 0)) {
      uVar6 = FUN_102336410();
    }
    FUN_101a4b1d0(uVar5,uVar6,0x100500);
    uVar5 = 0;
    if (((*(long *)(param_1 + 0x48) != 0) &&
        (plVar3 = (long *)FUN_10268b7cc(), uVar5 = 0, plVar3 != (long *)0x0)) &&
       (lVar4 = (**(code **)(*plVar3 + 0x198))(), uVar5 = 0, lVar4 != 0)) {
      uVar5 = FUN_102336410();
    }
    FUN_101a4abd8(uVar5,0x100500,1,0,1);
    return;
  }
  FUN_102767b70(param_1);
  return;
}

