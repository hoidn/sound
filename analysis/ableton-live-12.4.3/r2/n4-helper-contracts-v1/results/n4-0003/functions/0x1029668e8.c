
void FUN_1029668e8(long param_1,int param_2)

{
  int iVar1;
  undefined8 uVar2;
  long *plVar3;
  int *piVar4;
  long lVar5;
  long *plVar6;
  long *local_60;
  long *local_58;
  int *local_50;
  long *local_48;
  long *local_40;
  char local_31;
  
  if (param_2 - 5U < 2) {
    uVar2 = std::chrono::system_clock::now();
    FUN_103f3ffec(&local_48,2,uVar2);
    iVar1 = FUN_103f3c8b8(&local_48);
    if (iVar1 != 0) {
      FUN_103f39a78(&local_48,"AddOns: killed");
    }
LAB_102966ba8:
    thunk_FUN_103f395e4(&local_48);
    FUN_102966800(param_1);
    return;
  }
  if (param_2 == 4) {
    if ((*(byte *)(param_1 + 0x60) & 1) != 0) {
      uVar2 = std::chrono::system_clock::now();
      FUN_103f3ffec(&local_48,2,uVar2);
      iVar1 = FUN_103f3c8b8(&local_48);
      if (iVar1 != 0) {
        FUN_103f39a78(&local_48,"AddOns: process stopped");
      }
      goto LAB_102966ba8;
    }
    if (*(int *)(param_1 + 100) < 0xb) {
      local_31 = '\x03';
      local_48 = (long *)CONCAT44(local_48._4_4_,0x766564);
      uVar2 = std::chrono::system_clock::now();
      FUN_103f3ff2c(&local_50,4,&local_48,uVar2);
      if (local_31 < '\0') {
        operator_delete(local_48);
      }
      iVar1 = FUN_103f3c8b8(&local_50);
      if (iVar1 != 0) {
        uVar2 = FUN_103f39a78(&local_50,"AddOns: process stopped prematurely [");
        uVar2 = FUN_103f3b7b0(uVar2,*(undefined4 *)(param_1 + 100));
        FUN_103f39a78(uVar2,"]. Restart");
      }
      thunk_FUN_103f395e4(&local_50);
      FUN_102966254(param_1);
      return;
    }
    local_31 = '\x03';
    local_48 = (long *)CONCAT44(local_48._4_4_,0x766564);
    uVar2 = std::chrono::system_clock::now();
    FUN_103f3ff2c(&local_50,4,&local_48,uVar2);
    if (local_31 < '\0') {
      operator_delete(local_48);
    }
    iVar1 = FUN_103f3c8b8(&local_50);
    if (iVar1 != 0) {
      uVar2 = FUN_103f39a78(&local_50,
                            "AddOns: process stopped prematurely, but restarting failed for ");
      uVar2 = FUN_103f3b7b0(uVar2,*(undefined4 *)(param_1 + 100));
      FUN_103f39a78(uVar2," times.  Giving up");
    }
    thunk_FUN_103f395e4(&local_50);
    local_48 = (long *)0x0;
    local_40 = (long *)0x0;
    FUN_1029655e4(*(undefined8 *)(param_1 + 0x40),&local_48,0);
    if (local_48 != (long *)0x0) {
      iVar1 = (int)local_48[1] + -1;
      *(int *)(local_48 + 1) = iVar1;
      if (iVar1 == 0) {
        FUN_10128eea0();
      }
    }
  }
  else if (param_2 == 3) {
    uVar2 = std::chrono::system_clock::now();
    FUN_103f3ffec(&local_48,2,uVar2);
    iVar1 = FUN_103f3c8b8(&local_48);
    if (iVar1 != 0) {
      FUN_103f39a78(&local_48,"AddOns: connected");
    }
    thunk_FUN_103f395e4(&local_48);
    plVar3 = operator_new(0x38);
    local_48 = *(long **)(param_1 + 0x48);
    if (local_48 != (long *)0x0) {
      *(int *)(local_48 + 1) = (int)local_48[1] + 1;
    }
    thunk_FUN_1025dd66c(plVar3,&local_48);
    if (local_48 != (long *)0x0) {
      iVar1 = (int)local_48[1] + -1;
      *(int *)(local_48 + 1) = iVar1;
      if (iVar1 == 0) {
        FUN_10128eea0();
      }
    }
    piVar4 = (int *)FUN_1012d9850(0x68);
    local_48 = plVar3;
    thunk_FUN_1015a3368(piVar4,&local_48,"live->addons");
    plVar3 = local_48;
    if (piVar4 != (int *)0x0) {
      piVar4[2] = piVar4[2] + 1;
    }
    local_48 = (long *)0x0;
    local_50 = piVar4;
    if (plVar3 != (long *)0x0) {
      (**(code **)(*plVar3 + 8))();
    }
    plVar6 = (long *)(param_1 + 0x50);
    lVar5 = *plVar6;
    plVar3 = (long *)0x0;
    if (piVar4 != (int *)0x0) {
      plVar3 = (long *)(piVar4 + 6);
    }
    *(long **)(param_1 + 0x58) = plVar3;
    if (lVar5 != 0) {
      iVar1 = *(int *)(lVar5 + 8) + -1;
      *(int *)(lVar5 + 8) = iVar1;
      if (iVar1 == 0) {
        FUN_10128eea0();
        plVar3 = *(long **)(param_1 + 0x58);
      }
    }
    *plVar6 = (long)piVar4;
    FUN_101427680(&local_50,"done");
    local_58 = operator_new(0x40);
    local_58[2] = 0;
    local_60 = local_58 + 3;
    *local_60 = (long)&PTR_FUN_106592870;
    *local_58 = (long)&PTR_FUN_106592790;
    local_58[1] = 0;
    local_58[4] = (long)&PTR_FUN_106833918;
    local_58[7] = (long)(local_58 + 4);
    local_58[5] = param_1;
    local_48 = (long *)0x0;
    local_40 = (long *)0x0;
    (**(code **)(*plVar3 + 8))(plVar3,&local_50,&local_60);
    if (local_58 != (long *)0x0) {
      LOAcquire();
      lVar5 = local_58[1];
      local_58[1] = lVar5 + -1;
      LORelease();
      if (lVar5 == 0) {
        (**(code **)(*local_58 + 0x10))(local_58);
        std::__shared_weak_count::__release_weak();
      }
    }
    if (local_40 != (long *)0x0) {
      LOAcquire();
      lVar5 = local_40[1];
      local_40[1] = lVar5 + -1;
      LORelease();
      if (lVar5 == 0) {
        (**(code **)(*local_40 + 0x10))(local_40);
        std::__shared_weak_count::__release_weak();
      }
    }
    if (local_50 != (int *)0x0) {
      iVar1 = *local_50;
      *local_50 = iVar1 + -1;
      if (iVar1 + -1 == 0) {
        FUN_101449efc();
      }
    }
    FUN_1029655e4(*(undefined8 *)(param_1 + 0x40),plVar6,0);
  }
  return;
}

