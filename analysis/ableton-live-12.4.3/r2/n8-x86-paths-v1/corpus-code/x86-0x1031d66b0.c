// x86 0x1031d66b0 FUN_1031d66b0 state=exported chunk=chunk-02323.jsonl code_sha256=80a29fc17a43b9e7e4b8c3f4e83cb6d20134a825f1f6754cd5f25278a7ed22e0

undefined8 FUN_1031d66b0(undefined8 param_1)

{
  long *plVar1;
  long lVar2;
  long *plVar3;
  long *local_38;
  long *local_30;
  long *local_28;
  
  FUN_104e80b40(&local_28);
  local_38 = local_28;
  if (local_28 == (long *)0x0) {
    plVar3 = (long *)0x0;
  }
  else {
    plVar3 = operator_new(0x20);
    plVar3[1] = 0;
    plVar3[2] = 0;
    *plVar3 = (long)&PTR_FUN_106e02668;
    plVar3[3] = (long)local_28;
  }
  local_28 = (long *)0x0;
  local_30 = plVar3;
  FUN_1031d67b0(param_1,&local_38);
  if (plVar3 != (long *)0x0) {
    LOCK();
    plVar1 = plVar3 + 1;
    lVar2 = *plVar1;
    *plVar1 = *plVar1 + -1;
    UNLOCK();
    if (lVar2 == 0) {
      (**(code **)(*plVar3 + 0x10))(plVar3);
      std::__shared_weak_count::__release_weak();
    }
  }
  plVar3 = local_28;
  local_28 = (long *)0x0;
  if (plVar3 != (long *)0x0) {
    (**(code **)(*plVar3 + 8))();
  }
  return param_1;
}

