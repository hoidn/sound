
/* WARNING: Removing unreachable block (ram,0x0001025dce80) */

void FUN_1025dcc88(long param_1,undefined4 param_2,int param_3,long param_4)

{
  int iVar1;
  undefined8 uVar2;
  long lVar3;
  long *plVar4;
  int local_80;
  undefined4 uStack_7c;
  void *local_68 [2];
  char local_51;
  undefined1 local_50 [24];
  int local_38;
  undefined4 uStack_34;
  
  local_38 = param_3;
  uStack_34 = param_2;
  FUN_1025d8b1c(local_50,&uStack_34);
  FUN_1025d8b1c(local_68,&local_38);
  if (((DAT_10700ba30 & 1) == 0) && (iVar1 = ___cxa_guard_acquire(&DAT_10700ba30), iVar1 != 0)) {
    uVar2 = FUN_1011b89d0();
    DAT_10700b9c0 = FUN_1011b8ac4(uVar2,"Trace::ProcessObserver",1);
    ___cxa_guard_release(&DAT_10700ba30);
  }
  uVar2 = FUN_1011b89d0();
  iVar1 = FUN_1011b8ab0(uVar2,DAT_10700b9c0);
  if (iVar1 != 0) {
    if (*(long **)(param_1 + 0x10) != (long *)0x0) {
      (**(code **)(**(long **)(param_1 + 0x10) + 0x48))();
    }
    FUN_1011b66f8("ProcessObserver","OnStateChanged (%x) %s -> %s, PID: %i");
  }
  if (param_4 == 3) {
    FUN_100e170d0(&local_80,2);
    FUN_1025dcfe8(param_1,&local_80);
  }
  else if (local_38 < 8) {
    if (local_38 != 3) {
      if (local_38 != 6) goto LAB_1025dcddc;
LAB_1025dcda8:
      if (*(long **)(param_1 + 0x10) != (long *)0x0) {
        (**(code **)(**(long **)(param_1 + 0x10) + 0x38))();
        lVar3 = *(long *)(param_1 + 0x10);
        if ((lVar3 != 0) &&
           (iVar1 = *(int *)(lVar3 + 8) + -1, *(int *)(lVar3 + 8) = iVar1, iVar1 == 0)) {
          FUN_10128eea0();
        }
        *(undefined8 *)(param_1 + 0x10) = 0;
      }
      goto LAB_1025dcddc;
    }
    FUN_100e170d0(&local_80,1);
    FUN_1025dcfe8(param_1,&local_80);
  }
  else {
    if (local_38 != 8) {
      if (local_38 != 10) goto LAB_1025dcddc;
      goto LAB_1025dcda8;
    }
    FUN_100e170d0(&local_80,2);
    FUN_1025dcfe8(param_1,&local_80);
  }
  if ((void *)CONCAT44(uStack_7c,local_80) != (void *)0x0) {
    operator_delete((void *)CONCAT44(uStack_7c,local_80));
  }
LAB_1025dcddc:
  if ((((*(long **)(param_1 + 8) != (long *)0x0) &&
       (iVar1 = (**(code **)(**(long **)(param_1 + 8) + 0x20))(), iVar1 != 0)) &&
      (**(uint **)(param_1 + 0x18) < 0xb)) &&
     ((1 << (ulong)(**(uint **)(param_1 + 0x18) & 0x1f) & 0x670U) != 0)) {
    (**(code **)(**(long **)(param_1 + 8) + 0x18))();
  }
  plVar4 = *(long **)(param_1 + 0x38);
  if (plVar4 != (long *)0x0) {
    local_80 = local_38;
    (**(code **)(*plVar4 + 0x30))(plVar4,param_1,&local_80);
  }
  if (local_51 < '\0') {
    operator_delete(local_68[0]);
  }
  return;
}

