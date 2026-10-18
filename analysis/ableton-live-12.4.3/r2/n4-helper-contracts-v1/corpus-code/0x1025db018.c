// 0x1025db018 FUN_1025db018 exported-with-warnings  sig: undefined FUN_1025db018()

void FUN_1025db018(undefined8 param_1,undefined8 param_2)

{
  ulong uVar1;
  void *pvVar2;
  int iVar3;
  undefined8 uVar4;
  void *pvVar5;
  ulong extraout_x1;
  ulong uVar6;
  void *local_70;
  undefined8 uStack_68;
  long local_60;
  void *local_58;
  void *local_50;
  char local_40;
  int *local_38;
  
  if (((DAT_10700b9f8 & 1) == 0) && (iVar3 = ___cxa_guard_acquire(&DAT_10700b9f8), iVar3 != 0)) {
    uVar4 = FUN_1011b89d0();
    DAT_10700b9a8 = FUN_1011b8ac4(uVar4,"Trace::ProcessObserver",1);
    ___cxa_guard_release(&DAT_10700b9f8);
  }
  uVar4 = FUN_1011b89d0();
  iVar3 = FUN_1011b8ab0(uVar4,DAT_10700b9a8);
  if (iVar3 != 0) {
    FUN_1011b6484("ProcessObserver","KillLingeringProcesses");
  }
  FUN_101288264(&local_38,param_2);
  if ((DAT_10700ba00 & 1) == 0) {
    FUN_105422ed8();
  }
  FUN_101512154(&DAT_10700bbe0,&local_38,&local_38);
  if ((extraout_x1 & 1) != 0) {
    FUN_1011c74dc(&local_70,&local_38);
    FUN_1011a62a8(&local_58,&local_70);
    pvVar2 = local_58;
    if (local_60 < 0) {
      operator_delete(local_70);
      pvVar2 = local_58;
    }
    local_58 = pvVar2;
    if (local_40 == '\x01') {
      local_70 = (void *)0x0;
      uStack_68 = 0;
      local_60 = 0;
      uVar1 = (long)local_50 - (long)pvVar2;
      if (uVar1 != 0) {
        if ((long)uVar1 < 0) {
                    /* WARNING: Subroutine does not return */
          FUN_100256744(&local_70);
        }
        pvVar5 = operator_new(uVar1);
        _memcpy(pvVar5,pvVar2,uVar1);
        uVar6 = 0;
        do {
          FUN_1011a66d4(*(undefined4 *)((long)pvVar5 + uVar6));
          uVar6 = uVar6 + 4;
        } while (uVar1 != uVar6);
        operator_delete(pvVar5);
      }
    }
    if ((local_40 == '\x01') && (local_58 != (void *)0x0)) {
      local_50 = local_58;
      operator_delete(local_58);
    }
  }
  if ((local_38 != (int *)0x0) && (iVar3 = *local_38, *local_38 = iVar3 + -1, iVar3 + -1 == 0)) {
    FUN_101449efc();
  }
  return;
}


