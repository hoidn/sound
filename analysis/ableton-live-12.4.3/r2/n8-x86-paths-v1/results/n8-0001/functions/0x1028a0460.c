
void FUN_1028a0460(long param_1)

{
  char cVar1;
  long *plVar2;
  long lVar3;
  undefined8 uVar4;
  
  if (((*(long *)(param_1 + 0x48) == 0) || (plVar2 = (long *)FUN_1027b59a0(), plVar2 == (long *)0x0)
      ) || (lVar3 = (**(code **)(*plVar2 + 0x198))(plVar2), lVar3 == 0)) {
    cVar1 = FUN_101a6c470(0);
  }
  else {
    uVar4 = FUN_10244a5b0(lVar3);
    cVar1 = FUN_101a6c470(uVar4);
  }
  if (cVar1 == '\0') {
    if (((*(long *)(param_1 + 0x48) == 0) ||
        (plVar2 = (long *)FUN_1027b59a0(), plVar2 == (long *)0x0)) ||
       (lVar3 = (**(code **)(*plVar2 + 0x198))(plVar2), lVar3 == 0)) {
      uVar4 = 0;
    }
    else {
      uVar4 = FUN_10244a5b0(lVar3);
    }
    FUN_101a6f1f0(uVar4,0x100500,0,1,0);
    cVar1 = FUN_1015544c0(*(undefined8 *)(param_1 + 0x788));
  }
  else {
    cVar1 = FUN_1015544c0(*(undefined8 *)(param_1 + 0x788));
  }
  if (cVar1 == '\0') {
    if ((*(long *)(param_1 + 0x8c8) == 0) || (cVar1 = FUN_101a6f1b0(), cVar1 == '\0')) {
                    /* WARNING: Could not recover jumptable at 0x0001028a0584. Too many branches */
                    /* WARNING: Treating indirect jump as call */
      (**(code **)(**(long **)(param_1 + 0x240) + 0x248))(0);
      return;
    }
  }
  else {
    if (((*(long *)(param_1 + 0x48) == 0) ||
        (plVar2 = (long *)FUN_1027b59a0(), plVar2 == (long *)0x0)) ||
       (lVar3 = (**(code **)(*plVar2 + 0x198))(plVar2), lVar3 == 0)) {
      cVar1 = FUN_101a6c470(0);
    }
    else {
      uVar4 = FUN_10244a5b0(lVar3);
      cVar1 = FUN_101a6c470(uVar4);
    }
    if (cVar1 == '\0') {
      plVar2 = (long *)FUN_10279e9c0();
      (**(code **)(*plVar2 + 0x998))(plVar2);
    }
    cVar1 = FUN_1015544c0(*(undefined8 *)(param_1 + 0xb0));
    if ((cVar1 != '\0') && (cVar1 = FUN_1015544c0(*(undefined8 *)(param_1 + 0x5c0)), cVar1 != '\0'))
    {
                    /* WARNING: Could not recover jumptable at 0x0001028a05db. Too many branches */
                    /* WARNING: Treating indirect jump as call */
      (**(code **)(**(long **)(param_1 + 0xb0) + 0x248))(*(long **)(param_1 + 0xb0),0);
      return;
    }
  }
  return;
}

