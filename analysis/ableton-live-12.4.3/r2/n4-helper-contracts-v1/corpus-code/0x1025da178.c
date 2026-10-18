// 0x1025da178 FUN_1025da178 exported  sig: undefined FUN_1025da178()

undefined8 FUN_1025da178(long param_1,undefined8 param_2,undefined8 param_3)

{
  void *pvVar1;
  int iVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  long *plVar5;
  int local_50;
  undefined4 uStack_4c;
  void *local_48;
  char local_31;
  
  if (((*(long **)(param_1 + 8) == (long *)0x0) ||
      (iVar2 = (**(code **)(**(long **)(param_1 + 8) + 0x20))(), iVar2 == 0)) ||
     (iVar2 = (**(code **)(**(long **)(param_1 + 8) + 0x38))(), iVar2 == 0)) {
    return 1;
  }
  plVar5 = *(long **)(param_1 + 8);
  FUN_100e17004(&local_50,param_2);
  uVar3 = (**(code **)(*plVar5 + 0x28))(plVar5,&local_50,param_3);
  pvVar1 = (void *)CONCAT44(uStack_4c,local_50);
  if (pvVar1 != (void *)0x0) {
    local_48 = pvVar1;
    operator_delete(pvVar1);
  }
  (**(code **)(**(long **)(param_1 + 8) + 0x30))(&local_50);
  if (local_50 != 0) {
    if (((DAT_10700ba08 & 1) == 0) && (iVar2 = ___cxa_guard_acquire(&DAT_10700ba08), iVar2 != 0)) {
      uVar4 = FUN_1011b89d0();
      DAT_10700b9ac = FUN_1011b8ac4(uVar4,"Trace::ProcessObserver",1);
      ___cxa_guard_release(&DAT_10700ba08);
    }
    uVar4 = FUN_1011b89d0();
    iVar2 = FUN_1011b8ab0(uVar4,DAT_10700b9ac);
    if (iVar2 != 0) {
      FUN_1011b66f8("ProcessObserver","IPC Socket error: %s");
    }
  }
  if (-1 < local_31) {
    return uVar3;
  }
  operator_delete(local_48);
  return uVar3;
}


