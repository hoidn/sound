// 0x10307a96c FUN_10307a96c exported  sig: undefined FUN_10307a96c()

void FUN_10307a96c(undefined8 param_1)

{
  long lVar1;
  long *plVar2;
  long *local_48;
  long *local_40;
  long *local_38;
  
  FUN_104a7f378(&local_48);
  local_40 = local_48;
  if (local_48 == (long *)0x0) {
    plVar2 = (long *)0x0;
  }
  else {
    plVar2 = operator_new(0x20);
    *plVar2 = (long)&PTR____shared_weak_count_1068bcc10;
    plVar2[1] = 0;
    plVar2[2] = 0;
    plVar2[3] = (long)local_48;
  }
  local_48 = (long *)0x0;
  local_38 = plVar2;
  FUN_10307aa68(param_1,&local_40);
  if (plVar2 != (long *)0x0) {
    LOAcquire();
    lVar1 = plVar2[1];
    plVar2[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*plVar2 + 0x10))(plVar2);
      std::__shared_weak_count::__release_weak();
    }
  }
  plVar2 = local_48;
  local_48 = (long *)0x0;
  if (plVar2 != (long *)0x0) {
    (**(code **)(*plVar2 + 8))();
  }
  return;
}


