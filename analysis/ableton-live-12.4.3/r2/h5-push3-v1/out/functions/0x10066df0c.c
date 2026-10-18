// 0x10066df0c FUN_10066df0c state=exported role=kill(pid, 0) liveness check
// source chunk chunk-00230.jsonl; code_sha256=78fcbd67427d3888d20a8acce437553e4ca649abfd4b98cc6623a70e5e841da4

bool FUN_10066df0c(pid_t param_1)

{
  int iVar1;
  
  iVar1 = _kill(param_1,0);
  return iVar1 == 0;
}

