// 0x1013f1ca4 FUN_1013f1ca4 state=exported-with-warnings role=real-time channel shared memory open
// source chunk chunk-00893.jsonl; code_sha256=83a361c32fbf32112e622b9af4c6bf169b796f83f754ddaf4c3d9256ca8055a8

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 FUN_1013f1ca4(long param_1,undefined **param_2)

{
  int iVar1;
  long *plVar2;
  void *pvVar3;
  long lVar4;
  undefined8 uVar5;
  undefined8 in_x7;
  void *pvVar6;
  undefined2 local_58;
  undefined6 uStack_56;
  undefined **local_50;
  undefined8 local_48;
  undefined8 uStack_40;
  char *local_38;
  
  plVar2 = operator_new(0x28);
  local_50 = (undefined **)*param_2;
  if (-1 < *(char *)((long)param_2 + 0x17)) {
    local_50 = param_2;
  }
  plVar2[1] = 0;
  *plVar2 = 0;
  plVar2[3] = 0;
  plVar2[2] = 0;
  *(undefined8 *)((long)plVar2 + 0x1d) = 0;
  local_58 = 0x1a4;
  FUN_1013f46e0(plVar2 + 1,1,&local_50,0,2,0,&local_58,in_x7,plVar2,1);
  pvVar6 = *(void **)(param_1 + 200);
  *(long **)(param_1 + 200) = plVar2;
  if (pvVar6 != (void *)0x0) {
    pvVar3 = *(void **)((long)pvVar6 + 8);
    if (pvVar3 != (void *)0x0) {
      if (*(char *)((long)pvVar6 + 0x24) == '\x01') {
        _shmdt(pvVar3);
      }
      else {
        _munmap((long)pvVar3 - *(long *)((long)pvVar6 + 0x18),
                *(long *)((long)pvVar6 + 0x10) + *(long *)((long)pvVar6 + 0x18));
      }
    }
    operator_delete(pvVar6);
    plVar2 = *(long **)(param_1 + 200);
  }
  lVar4 = *plVar2;
  if ((int)plVar2[4] == 0) {
    uStack_40 = _UNK_10180b468;
    local_48 = _DAT_10180b460;
    local_38 = "N7ableton15realtimechannel14shareddatatype6RTSyncE";
    local_50 = &PTR_FUN_101ca2ea0;
    uVar5 = FUN_101193010(lVar4,"N7ableton15realtimechannel14shareddatatype6RTSyncE",lVar4 + 0xd8,
                          &local_50,&local_58,0);
  }
  else {
    uStack_40 = _UNK_10180b468;
    local_48 = _DAT_10180b460;
    local_38 = "N7ableton15realtimechannel14shareddatatype6RTSyncE";
    local_50 = &PTR_FUN_101ca2ea0;
    uVar5 = FUN_101193010(lVar4,"N7ableton15realtimechannel14shareddatatype6RTSyncE",lVar4 + 0xd8,
                          &local_50,&local_58,1);
  }
  if (CONCAT62(uStack_56,local_58) != 1) {
    uVar5 = std::chrono::system_clock::now();
    FUN_1003324b0(&local_50,4,uVar5);
    iVar1 = FUN_10032ece8(&local_50);
    if (iVar1 != 0) {
      FUN_10032bea8(&local_50,"Could not open shared memory for real-time data");
    }
    thunk_FUN_10032ba14(&local_50);
    return 0;
  }
  FUN_1013f79c0(param_1 + 0x80,uVar5);
  if (*(long *)(param_1 + 200) != 0) {
    for (lVar4 = *(long *)(param_1 + 0xb8); lVar4 != param_1 + 0xb0; lVar4 = *(long *)(lVar4 + 8)) {
      (**(code **)(**(long **)(lVar4 + 0x10) + 0x30))
                (*(long **)(lVar4 + 0x10),*(undefined8 *)(param_1 + 200));
    }
  }
  return 1;
}

