// 0x100232af8 FUN_100232af8 state=exported-with-warnings body_bytes=488 warnings=1 chunk=chunk-00096.jsonl

void FUN_100232af8(long *param_1,undefined8 param_2)

{
  int iVar1;
  ulong uVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  undefined1 auStack_60 [8];
  undefined1 auStack_58 [8];
  undefined1 auStack_50 [8];
  undefined1 auStack_48 [8];
  undefined1 auStack_40 [8];
  long *local_38;
  
  if ((param_1[4] != 0) && (uVar2 = FUN_100233910(), (uVar2 & 1) == 0)) {
    (**(code **)(*(long *)param_1[4] + 0xc0))
              ((long *)param_1[4],"CREATE TABLE version (  version  INT,         platform INT )");
    (**(code **)(*(long *)param_1[4] + 0xd0))
              (&local_38,(long *)param_1[4],
               "INSERT INTO version (version, platform) VALUES (:version, :platform)");
    if (local_38 == (long *)0x0) {
      uVar3 = std::chrono::system_clock::now();
      FUN_10073cdf4(auStack_40,4,uVar3);
      iVar1 = FUN_1007396c0(auStack_40);
      if (iVar1 != 0) {
        uVar3 = FUN_100736880(auStack_40,"Database: Failed: ");
        uVar4 = (**(code **)(*(long *)param_1[4] + 0x90))();
        FUN_100736880(uVar3,uVar4);
      }
      thunk_FUN_1007363ec(auStack_40);
      (**(code **)(*param_1 + 0x80))(param_1);
      (**(code **)(*(long *)param_1[4] + 0x58))();
      uVar3 = ___cxa_allocate_exception(0x30);
      FUN_1001d4d4c(auStack_40);
      FUN_1001d4d4c(auStack_48);
      FUN_1001d4d4c(auStack_50);
      FUN_1001d4d4c(auStack_58);
      FUN_1001d4d4c(auStack_60);
      FUN_10025df70(uVar3,&DAT_100e2bdb8,auStack_40,auStack_48,auStack_50,auStack_58,auStack_60);
                    /* WARNING: Subroutine does not return */
      ___cxa_throw(uVar3,&PTR_vtable_100d923c8,FUN_10025e5e4);
    }
    (**(code **)(*local_38 + 0x50))(local_38,":version",param_2);
    if (local_38 != (long *)0x0) {
      (**(code **)(*local_38 + 0x50))(local_38,":platform",2);
      if (local_38 != (long *)0x0) {
        (**(code **)(*local_38 + 0xb0))();
        if (local_38 != (long *)0x0) {
          (**(code **)(*local_38 + 0x28))();
          if (local_38 != (long *)0x0) {
            iVar1 = (int)local_38[1] + -1;
            *(int *)(local_38 + 1) = iVar1;
            if (iVar1 == 0) {
              FUN_1002abea8();
            }
          }
        }
      }
    }
  }
  return;
}

