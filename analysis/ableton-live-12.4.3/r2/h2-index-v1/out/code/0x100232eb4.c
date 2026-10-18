// 0x100232eb4 FUN_100232eb4 state=exported body_bytes=616 warnings=0 chunk=chunk-00096.jsonl

void FUN_100232eb4(long *param_1,int param_2,undefined8 param_3,undefined8 param_4,
                  undefined8 param_5)

{
  undefined8 *puVar1;
  undefined8 *puVar2;
  int iVar3;
  undefined8 uVar4;
  undefined8 uVar5;
  undefined1 auStack_48 [8];
  
  if (param_2 < 2) {
    if (param_2 == 0) {
      (**(code **)(*param_1 + 0x50))(param_1);
      (**(code **)(*param_1 + 0x58))(param_1);
      puVar2 = (undefined8 *)param_1[0xb];
      for (puVar1 = (undefined8 *)param_1[10]; puVar1 != puVar2; puVar1 = puVar1 + 1) {
        (**(code **)(*(long *)*puVar1 + 0x10))();
      }
      if (*(char *)((long)param_1 + 0x29) == '\x01') {
        (**(code **)(*param_1 + 0x68))(param_1);
        puVar2 = (undefined8 *)param_1[0xb];
        for (puVar1 = (undefined8 *)param_1[10]; puVar1 != puVar2; puVar1 = puVar1 + 1) {
          (**(code **)(*(long *)*puVar1 + 8))();
        }
      }
      else {
        (**(code **)(*param_1 + 0x60))(param_1);
        puVar2 = (undefined8 *)param_1[0xb];
        for (puVar1 = (undefined8 *)param_1[10]; puVar1 != puVar2; puVar1 = puVar1 + 1) {
          (*(code *)**(undefined8 **)*puVar1)();
        }
      }
    }
    else if (param_2 == 1) {
      std::chrono::system_clock::now();
      FUN_10073cf98(auStack_48);
      iVar3 = FUN_1007396c0(auStack_48);
      if (iVar3 != 0) {
        uVar5 = FUN_100736880(auStack_48,"Database: Database is at version ");
        uVar5 = FUN_1007385b8(uVar5,param_3);
        uVar5 = FUN_100736880(uVar5,", upgrade to ");
        uVar4 = (**(code **)(*param_1 + 0x30))(param_1);
        FUN_1007385b8(uVar5,uVar4);
      }
      thunk_FUN_1007363ec(auStack_48);
      FUN_1002336e0(param_1,param_3,param_4);
    }
    return;
  }
  if (param_2 == 2) {
    std::chrono::system_clock::now();
    FUN_10073cf98(auStack_48);
    iVar3 = FUN_1007396c0(auStack_48);
    if (iVar3 != 0) {
      uVar5 = FUN_100736880(auStack_48,"Database: Database is at version ");
      uVar5 = FUN_1007385b8(uVar5,param_3);
      FUN_100736880(uVar5,".  Need to recreate");
    }
  }
  else if (param_2 == 3) {
    std::chrono::system_clock::now();
    FUN_10073cf98(auStack_48);
    iVar3 = FUN_1007396c0(auStack_48);
    if (iVar3 != 0) {
      FUN_100736880(auStack_48,"Database: Database is from a different platform.  Need to recreate")
      ;
    }
  }
  else {
    if (param_2 != 4) {
      return;
    }
    std::chrono::system_clock::now();
    FUN_10073cf98(auStack_48);
    iVar3 = FUN_1007396c0(auStack_48);
    if (iVar3 != 0) {
      FUN_100736880(auStack_48,"Database: Database is at a unknown version.  Need to recreate");
    }
  }
  thunk_FUN_1007363ec(auStack_48);
  FUN_1002322e0(param_1,param_5);
  return;
}

