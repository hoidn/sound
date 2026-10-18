// 0x100668408 FUN_100668408 state=exported role=Watchdog tick: kLiveStillRunning unless parent pid is gone
// source chunk chunk-00229.jsonl; code_sha256=8419297918745e04560f3e7f10e4eb96ac56d04a0faf93769f35d8a2f719487c

void FUN_100668408(long param_1)

{
  int iVar1;
  
  if ((*(int *)(param_1 + 0x68) != 0) && (iVar1 = FUN_10066df0c(), iVar1 == 0)) {
    return;
  }
  FUN_100668114(param_1 + 0x18,1);
  return;
}

