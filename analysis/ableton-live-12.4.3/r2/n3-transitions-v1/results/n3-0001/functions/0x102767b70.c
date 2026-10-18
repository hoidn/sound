
void FUN_102767b70(long param_1)

{
  int iVar1;
  long *plVar2;
  long lVar3;
  ulong uVar4;
  undefined8 uVar5;
  
  if (((*(long *)(param_1 + 0x48) != 0) && (plVar2 = (long *)FUN_10268b7cc(), plVar2 != (long *)0x0)
      ) && (lVar3 = (**(code **)(*plVar2 + 0x198))(), lVar3 != 0)) {
    FUN_102336410();
  }
  uVar4 = FUN_101a48488();
  if ((uVar4 & 1) == 0) {
    uVar5 = 0;
    if (((*(long *)(param_1 + 0x48) != 0) &&
        (plVar2 = (long *)FUN_10268b7cc(), uVar5 = 0, plVar2 != (long *)0x0)) &&
       (lVar3 = (**(code **)(*plVar2 + 0x198))(), uVar5 = 0, lVar3 != 0)) {
      uVar5 = FUN_102336410();
    }
    FUN_101a4abd8(uVar5,0x100500,0,1,0);
  }
  iVar1 = FUN_1015645a0(*(undefined8 *)(param_1 + 0x788));
  if (iVar1 == 0) {
    if ((*(long *)(param_1 + 0x8c8) == 0) || (uVar4 = FUN_101a4abac(), (uVar4 & 1) == 0)) {
                    /* WARNING: Could not recover jumptable at 0x000102767c98. Too many branches */
                    /* WARNING: Treating indirect jump as call */
      (**(code **)(**(long **)(param_1 + 0x240) + 0x248))(0);
      return;
    }
  }
  else {
    if (((*(long *)(param_1 + 0x48) != 0) &&
        (plVar2 = (long *)FUN_10268b7cc(), plVar2 != (long *)0x0)) &&
       (lVar3 = (**(code **)(*plVar2 + 0x198))(), lVar3 != 0)) {
      FUN_102336410();
    }
    uVar4 = FUN_101a48488();
    if ((uVar4 & 1) == 0) {
      plVar2 = (long *)thunk_FUN_101849958();
      (**(code **)(*plVar2 + 0x998))();
    }
    iVar1 = FUN_1015645a0(*(undefined8 *)(param_1 + 0xb0));
    if ((iVar1 != 0) && (iVar1 = FUN_1015645a0(*(undefined8 *)(param_1 + 0x5c0)), iVar1 != 0)) {
                    /* WARNING: Could not recover jumptable at 0x000102767c60. Too many branches */
                    /* WARNING: Treating indirect jump as call */
      (**(code **)(**(long **)(param_1 + 0xb0) + 0x248))(*(long **)(param_1 + 0xb0),0);
      return;
    }
  }
  return;
}

