
void FUN_1002b56c4(long param_1,int param_2)

{
  int iVar1;
  undefined8 uVar2;
  long *plVar3;
  int *piVar4;
  long lVar5;
  long *plVar6;
  long *local_58;
  long *local_50;
  int *local_48;
  long *local_40;
  long *local_38;
  
  if (param_2 - 5U < 2) {
    uVar2 = std::chrono::system_clock::now();
    FUN_103f3ffec(&local_40,1,uVar2);
    iVar1 = FUN_103f3c8b8(&local_40);
    if (iVar1 != 0) {
      FUN_103f39a78(&local_40,"Indexer: killed");
    }
    thunk_FUN_103f395e4(&local_40);
    local_40 = (long *)0x0;
    local_38 = (long *)0x0;
    *(undefined8 *)(param_1 + 0x40) = 0;
    lVar5 = *(long *)(param_1 + 0x38);
    if (lVar5 != 0) {
      iVar1 = *(int *)(lVar5 + 8) + -1;
      *(int *)(lVar5 + 8) = iVar1;
      if (iVar1 == 0) {
        FUN_10128eea0();
      }
    }
  }
  else {
    if (param_2 != 4) {
      if (param_2 == 3) {
        uVar2 = std::chrono::system_clock::now();
        FUN_103f3ffec(&local_40,1,uVar2);
        iVar1 = FUN_103f3c8b8(&local_40);
        if (iVar1 != 0) {
          FUN_103f39a78(&local_40,"Indexer: connected");
        }
        thunk_FUN_103f395e4(&local_40);
        plVar3 = operator_new(0x38);
        local_40 = *(long **)(param_1 + 0x30);
        if (local_40 != (long *)0x0) {
          *(int *)(local_40 + 1) = (int)local_40[1] + 1;
        }
        thunk_FUN_1025dd66c(plVar3,&local_40);
        if (local_40 != (long *)0x0) {
          iVar1 = (int)local_40[1] + -1;
          *(int *)(local_40 + 1) = iVar1;
          if (iVar1 == 0) {
            FUN_10128eea0();
          }
        }
        piVar4 = (int *)FUN_1012d9850(0x68);
        local_40 = plVar3;
        thunk_FUN_1015a3368(piVar4,&local_40,"live->indexer");
        plVar3 = local_40;
        if (piVar4 != (int *)0x0) {
          piVar4[2] = piVar4[2] + 1;
        }
        local_40 = (long *)0x0;
        local_48 = piVar4;
        if (plVar3 != (long *)0x0) {
          (**(code **)(*plVar3 + 8))();
        }
        plVar6 = (long *)(param_1 + 0x38);
        lVar5 = *plVar6;
        plVar3 = (long *)0x0;
        if (piVar4 != (int *)0x0) {
          plVar3 = (long *)(piVar4 + 6);
        }
        *(long **)(param_1 + 0x40) = plVar3;
        if (lVar5 != 0) {
          iVar1 = *(int *)(lVar5 + 8) + -1;
          *(int *)(lVar5 + 8) = iVar1;
          if (iVar1 == 0) {
            FUN_10128eea0();
            plVar3 = *(long **)(param_1 + 0x40);
          }
        }
        *plVar6 = (long)piVar4;
        FUN_101427680(&local_48,"done");
        local_50 = operator_new(0x40);
        local_50[2] = 0;
        local_58 = local_50 + 3;
        *local_58 = (long)&PTR_FUN_106592870;
        *local_50 = (long)&PTR_FUN_106592790;
        local_50[1] = 0;
        local_50[4] = (long)&PTR_FUN_106598870;
        local_50[7] = (long)(local_50 + 4);
        local_50[5] = param_1;
        local_40 = (long *)0x0;
        local_38 = (long *)0x0;
        (**(code **)(*plVar3 + 8))(plVar3,&local_48,&local_58);
        if (local_50 != (long *)0x0) {
          LOAcquire();
          lVar5 = local_50[1];
          local_50[1] = lVar5 + -1;
          LORelease();
          if (lVar5 == 0) {
            (**(code **)(*local_50 + 0x10))(local_50);
            std::__shared_weak_count::__release_weak();
          }
        }
        if (local_38 != (long *)0x0) {
          LOAcquire();
          lVar5 = local_38[1];
          local_38[1] = lVar5 + -1;
          LORelease();
          if (lVar5 == 0) {
            (**(code **)(*local_38 + 0x10))(local_38);
            std::__shared_weak_count::__release_weak();
          }
        }
        if (local_48 != (int *)0x0) {
          iVar1 = *local_48;
          *local_48 = iVar1 + -1;
          if (iVar1 + -1 == 0) {
            FUN_101449efc();
          }
        }
        uVar2 = FUN_1002e96e8(*(undefined8 *)(param_1 + 0x28));
        FUN_10023894c(uVar2,plVar6,1 < *(int *)(param_1 + 0x4c));
      }
      return;
    }
    if ((*(byte *)(param_1 + 0x48) & 1) == 0) {
      if (*(int *)(param_1 + 0x4c) < 0x65) {
        uVar2 = std::chrono::system_clock::now();
        FUN_103f3ffec(&local_40,4,uVar2);
        iVar1 = FUN_103f3c8b8(&local_40);
        if (iVar1 != 0) {
          uVar2 = FUN_103f39a78(&local_40,"Indexer: process stopped prematurely [");
          uVar2 = FUN_103f3b7b0(uVar2,*(undefined4 *)(param_1 + 0x4c));
          FUN_103f39a78(uVar2,"]. Restart");
        }
        thunk_FUN_103f395e4(&local_40);
        FUN_1002b4b14(param_1);
        return;
      }
      uVar2 = std::chrono::system_clock::now();
      FUN_103f3ffec(&local_40,4,uVar2);
      iVar1 = FUN_103f3c8b8(&local_40);
      if (iVar1 != 0) {
        uVar2 = FUN_103f39a78(&local_40,
                              "Indexer: process stopped prematurely, but restarting failed for ");
        uVar2 = FUN_103f3b7b0(uVar2,*(undefined4 *)(param_1 + 0x4c));
        FUN_103f39a78(uVar2," times.  Giving up");
      }
      thunk_FUN_103f395e4(&local_40);
      return;
    }
    uVar2 = std::chrono::system_clock::now();
    FUN_103f3ffec(&local_40,1,uVar2);
    iVar1 = FUN_103f3c8b8(&local_40);
    if (iVar1 != 0) {
      FUN_103f39a78(&local_40,"Indexer: process stopped");
    }
    thunk_FUN_103f395e4(&local_40);
    local_40 = (long *)0x0;
    local_38 = (long *)0x0;
    *(undefined8 *)(param_1 + 0x40) = 0;
    lVar5 = *(long *)(param_1 + 0x38);
    if (lVar5 != 0) {
      iVar1 = *(int *)(lVar5 + 8) + -1;
      *(int *)(lVar5 + 8) = iVar1;
      if (iVar1 == 0) {
        FUN_10128eea0();
      }
    }
  }
  *(undefined8 *)(param_1 + 0x38) = 0;
  lVar5 = *(long *)(param_1 + 0x30);
  if (lVar5 != 0) {
    iVar1 = *(int *)(lVar5 + 8) + -1;
    *(int *)(lVar5 + 8) = iVar1;
    if (iVar1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined8 *)(param_1 + 0x30) = 0;
  *(undefined1 *)(param_1 + 0x48) = 0;
  *(undefined4 *)(param_1 + 0x4c) = 0;
  *(undefined1 *)(param_1 + 0x20) = 0;
  return;
}

