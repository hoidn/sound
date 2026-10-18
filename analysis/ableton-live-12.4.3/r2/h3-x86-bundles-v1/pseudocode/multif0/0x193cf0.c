// 0x193cf0 _mf0p_CancelProcess | undefined _mf0p_CancelProcess() | state=exported | chunk-00006.jsonl

void _mf0p_CancelProcess(long param_1)

{
  FUN_00006ff0(*(undefined8 *)(param_1 + 8));
  FUN_00029ce0(*(undefined8 *)(param_1 + 0x18));
  _fwrite("\r   Process to cancel set ...   \n",1,0x21,*(FILE **)PTR____stderrp_0046e300);
  FUN_00006fd0(*(undefined8 *)(param_1 + 8));
  return;
}

