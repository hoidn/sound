// 0x10023b614 FUN_10023b614 state=exported-with-warnings body_bytes=992 warnings=3 chunk=chunk-00097.jsonl

void FUN_10023b614(long param_1,undefined8 param_2,undefined8 param_3)

{
  ulong uVar1;
  int iVar2;
  undefined8 uVar3;
  long lVar4;
  int local_a8;
  undefined4 uStack_a4;
  undefined8 local_a0;
  char local_91;
  void *local_90 [2];
  char local_79;
  long local_78;
  long *local_70;
  undefined1 auStack_68 [8];
  void *local_60 [2];
  char local_49;
  void **local_48;
  byte local_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_100d60390;
  uVar1 = *(ulong *)(param_1 + 8);
  if (-1 < (char)*(byte *)(param_1 + 0x17)) {
    uVar1 = (ulong)*(byte *)(param_1 + 0x17);
  }
  if (uVar1 == 0) goto LAB_10023b9bc;
  uVar3 = std::chrono::system_clock::now();
  FUN_10073cdf4(local_60,2,uVar3);
  iVar2 = FUN_1007396c0(local_60);
  if (iVar2 != 0) {
    uVar3 = FUN_100736880(local_60,"Database: About to copy database from old database file ");
    FUN_10013a004(uVar3,param_1);
  }
  thunk_FUN_1007363ec(local_60);
  FUN_10022be94(&local_78);
  (**(code **)(*local_70 + 0x30))(local_70,param_1);
  (**(code **)(*local_70 + 8))(local_70,2);
  (**(code **)(*local_70 + 0x10))(local_70,1);
  (**(code **)(*local_70 + 0x80))(local_70,10000);
  FUN_10025e9ac(local_60,0);
  (**(code **)(*local_70 + 0x50))();
  if (local_40 == 1) {
    if (local_48 == (void **)0x0) {
                    /* WARNING: Subroutine does not return */
      FUN_100158190();
    }
    (**(code **)((long)*local_48 + 0x30))();
    if ((local_40 & 1) != 0) {
      if (local_48 == local_60) {
        lVar4 = 0x20;
      }
      else {
        if (local_48 == (void **)0x0) goto LAB_10023b764;
        lVar4 = 0x28;
      }
      (**(code **)((long)*local_48 + lVar4))();
    }
  }
LAB_10023b764:
  FUN_100716728(local_60,param_2);
  local_a8 = 0x706d6574;
  uStack_a4 = 0x62642e;
  local_91 = '\a';
  FUN_10014bdb8(local_90,local_60,&local_a8);
  if (local_91 < '\0') {
    operator_delete((void *)CONCAT44(uStack_a4,local_a8));
  }
  if (local_49 < '\0') {
    operator_delete(local_60[0]);
  }
  FUN_10025e9ac(local_60,0);
  (**(code **)(*local_70 + 0x70))(local_70,local_90,0xffffffff);
  if (local_40 == 1) {
    if (local_48 == (void **)0x0) {
                    /* WARNING: Subroutine does not return */
      FUN_100158190();
    }
    (**(code **)((long)*local_48 + 0x30))();
    if ((local_40 & 1) != 0) {
      if (local_48 == local_60) {
        lVar4 = 0x20;
      }
      else {
        if (local_48 == (void **)0x0) goto LAB_10023b848;
        lVar4 = 0x28;
      }
      (**(code **)((long)*local_48 + lVar4))();
    }
  }
LAB_10023b848:
  local_a8 = 0;
  local_a0 = std::system_category();
  FUN_10070c2e4(param_2,&local_a8);
  iVar2 = FUN_100716cfc(local_90);
  if ((iVar2 != 0) && (FUN_10070c5c4(local_90,param_2,&local_a8), local_a8 != 0)) {
    uVar3 = std::chrono::system_clock::now();
    FUN_10073cdf4(auStack_68,4,uVar3);
    iVar2 = FUN_1007396c0(auStack_68);
    if (iVar2 != 0) {
      uVar3 = FUN_100736880(auStack_68,"Database: Could not replace file ");
      uVar3 = FUN_10013a004(uVar3,param_2);
      uVar3 = FUN_100736880(uVar3," with ");
      uVar3 = FUN_10013a004(uVar3,local_90);
      uVar3 = FUN_100736880(uVar3,": ");
      std::error_code::message();
      FUN_100737760(uVar3,local_60);
      if (local_49 < '\0') {
        operator_delete(local_60[0]);
      }
    }
    thunk_FUN_1007363ec(auStack_68);
  }
  iVar2 = FUN_100716cfc(param_2);
  if (iVar2 == 0) {
    uVar3 = std::chrono::system_clock::now();
    FUN_10073cdf4(local_60,3,uVar3);
    iVar2 = FUN_1007396c0(local_60);
    if (iVar2 != 0) {
      FUN_100736880(local_60,"Database: Copying old database: Could not rename temporary copy.");
    }
  }
  else {
    uVar3 = std::chrono::system_clock::now();
    FUN_10073cdf4(local_60,2,uVar3);
    iVar2 = FUN_1007396c0(local_60);
    if (iVar2 != 0) {
      uVar3 = FUN_100736880(local_60,
                            "Database: Copying old database: Successfully copied database from version "
                           );
      FUN_1004525f4(uVar3,param_3);
    }
  }
  thunk_FUN_1007363ec(local_60);
  if (local_79 < '\0') {
    operator_delete(local_90[0]);
  }
  if ((local_78 != 0) &&
     (iVar2 = *(int *)(local_78 + 8) + -1, *(int *)(local_78 + 8) = iVar2, iVar2 == 0)) {
    FUN_1002abea8();
  }
LAB_10023b9bc:
  if (*(long *)PTR____stack_chk_guard_100d60390 == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

