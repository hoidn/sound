// 0x1956d0 _mf0p_RunMultiF0OnAudio | undefined _mf0p_RunMultiF0OnAudio() | state=exported | chunk-00006.jsonl

long * _mf0p_RunMultiF0OnAudio(undefined8 param_1,undefined8 param_2,undefined **param_3)

{
  undefined *puVar1;
  char cVar2;
  int iVar3;
  void *pvVar4;
  long *plVar5;
  allocator *paVar6;
  undefined *local_98;
  undefined *local_90;
  undefined1 local_88;
  undefined *local_80;
  undefined *local_78;
  undefined *local_70;
  undefined *local_68;
  undefined *local_60;
  
  puVar1 = PTR__S_empty_rep_storage_0046e240;
  local_98 = PTR__S_empty_rep_storage_0046e240 + 0x18;
  if (param_3 == (undefined **)0x0) {
    param_3 = &local_98;
  }
  local_88 = 1;
  local_90 = local_98;
  local_80 = local_98;
  local_78 = local_98;
  local_70 = local_98;
  local_68 = local_98;
  local_60 = local_98;
  pvVar4 = operator_new(0x198);
  FUN_0012b4c0(pvVar4,param_1,param_2);
  plVar5 = operator_new(0x20);
  *plVar5 = 0;
  plVar5[1] = 0;
  plVar5[2] = (long)pvVar4;
  plVar5[3] = 0;
  pvVar4 = operator_new(0x50);
  FUN_00006d30(pvVar4);
  *plVar5 = (long)pvVar4;
  pvVar4 = operator_new(0x40);
  FUN_00006e10(pvVar4);
  plVar5[1] = (long)pvVar4;
  pvVar4 = operator_new(0xd0);
  FUN_0002bd10(pvVar4,plVar5[2],param_3,plVar5[1]);
  plVar5[3] = (long)pvVar4;
  cVar2 = FUN_00007010(plVar5[1]);
  if ((cVar2 == '\0') ||
     (FUN_00007030(*plVar5,FUN_00193dd0,plVar5[3]), *(char *)(*plVar5 + 0x48) == '\0')) {
    FUN_00029cf0(plVar5[3],0xfffffffd);
  }
  else {
    do {
    } while (*(char *)(plVar5[3] + 0xcd) == '\0');
  }
  paVar6 = (allocator *)(local_60 + -0x18);
  if (((allocator *)puVar1 != paVar6) &&
     (iVar3 = __gnu_cxx::__exchange_and_add((int *)(local_60 + -8),-1), iVar3 < 1)) {
    std::string::_Rep::_M_destroy(paVar6);
  }
  paVar6 = (allocator *)(local_68 + -0x18);
  if (((allocator *)puVar1 != paVar6) &&
     (iVar3 = __gnu_cxx::__exchange_and_add((int *)(local_68 + -8),-1), iVar3 < 1)) {
    std::string::_Rep::_M_destroy(paVar6);
  }
  paVar6 = (allocator *)(local_70 + -0x18);
  if (((allocator *)puVar1 != paVar6) &&
     (iVar3 = __gnu_cxx::__exchange_and_add((int *)(local_70 + -8),-1), iVar3 < 1)) {
    std::string::_Rep::_M_destroy(paVar6);
  }
  paVar6 = (allocator *)(local_78 + -0x18);
  if (((allocator *)puVar1 != paVar6) &&
     (iVar3 = __gnu_cxx::__exchange_and_add((int *)(local_78 + -8),-1), iVar3 < 1)) {
    std::string::_Rep::_M_destroy(paVar6);
  }
  paVar6 = (allocator *)(local_80 + -0x18);
  if (((allocator *)puVar1 != paVar6) &&
     (iVar3 = __gnu_cxx::__exchange_and_add((int *)(local_80 + -8),-1), iVar3 < 1)) {
    std::string::_Rep::_M_destroy(paVar6);
  }
  paVar6 = (allocator *)(local_90 + -0x18);
  if (((allocator *)puVar1 != paVar6) &&
     (iVar3 = __gnu_cxx::__exchange_and_add((int *)(local_90 + -8),-1), iVar3 < 1)) {
    std::string::_Rep::_M_destroy(paVar6);
  }
  paVar6 = (allocator *)(local_98 + -0x18);
  if (((allocator *)puVar1 != paVar6) &&
     (iVar3 = __gnu_cxx::__exchange_and_add((int *)(local_98 + -8),-1), iVar3 < 1)) {
    std::string::_Rep::_M_destroy(paVar6);
  }
  return plVar5;
}

