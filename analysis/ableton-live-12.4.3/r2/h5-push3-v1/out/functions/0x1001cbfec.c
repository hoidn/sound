// 0x1001cbfec FUN_1001cbfec state=exported role=RtMidi output open
// source chunk chunk-00082.jsonl; code_sha256=fa37fdbca3eb537e2e08dd6aa23dd6f0bdbb545b38cd0664f0c6ec762def169e

long * FUN_1001cbfec(long *param_1,undefined8 param_2,long *param_3)

{
  char cVar1;
  undefined8 *puVar2;
  long *plVar3;
  long lVar4;
  long lVar5;
  void *local_80;
  long lStack_78;
  long local_70;
  void *local_60;
  char acStack_58 [8];
  undefined4 local_50;
  undefined1 local_4c;
  char local_49;
  
  *param_1 = 0;
  if (*(char *)((long)param_3 + 0x17) < '\0') {
    FUN_10018127c(param_1 + 1,*param_3,param_3[1]);
  }
  else {
    lVar5 = param_3[1];
    lVar4 = *param_3;
    param_1[3] = param_3[2];
    param_1[2] = lVar5;
    param_1[1] = lVar4;
  }
  puVar2 = operator_new(0x10);
  local_49 = '\x14';
  local_50 = 0x746e6569;
  acStack_58[0] = s_RtMidi_Output_Client_101839099[8];
  acStack_58[1] = s_RtMidi_Output_Client_101839099[9];
  acStack_58[2] = s_RtMidi_Output_Client_101839099[10];
  acStack_58[3] = s_RtMidi_Output_Client_101839099[0xb];
  acStack_58[4] = s_RtMidi_Output_Client_101839099[0xc];
  acStack_58[5] = s_RtMidi_Output_Client_101839099[0xd];
  acStack_58[6] = s_RtMidi_Output_Client_101839099[0xe];
  acStack_58[7] = s_RtMidi_Output_Client_101839099[0xf];
  local_60 = (void *)s_RtMidi_Output_Client_101839099._0_8_;
  local_4c = 0;
  thunk_FUN_1005a6edc(puVar2,0,&local_60);
  if (local_49 < '\0') {
    operator_delete(local_60);
    cVar1 = *(char *)((long)param_3 + 0x17);
  }
  else {
    cVar1 = *(char *)((long)param_3 + 0x17);
  }
  if (cVar1 < '\0') {
    FUN_10018127c(&local_80,*param_3,param_3[1]);
  }
  else {
    lStack_78 = param_3[1];
    local_80 = (void *)*param_3;
    local_70 = param_3[2];
  }
  (**(code **)*puVar2)(puVar2,param_2,&local_80);
  if (local_70 < 0) {
    operator_delete(local_80);
  }
  plVar3 = (long *)*param_1;
  *param_1 = (long)puVar2;
  if (plVar3 != (long *)0x0) {
    (**(code **)(*plVar3 + 0x40))();
  }
  return param_1;
}

