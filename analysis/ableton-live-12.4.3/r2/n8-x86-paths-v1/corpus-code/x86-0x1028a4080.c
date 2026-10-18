// x86 0x1028a4080 FUN_1028a4080 state=exported chunk=chunk-01917.jsonl code_sha256=554eb20f9d2b423649109a0a5a650da33360badc48a72cee37dfb42772bb3c6c

void FUN_1028a4080(long param_1)

{
  char cVar1;
  
  if (*(long *)(param_1 + 0x8c8) != 0) {
    cVar1 = FUN_101a6f1b0();
    if (cVar1 != '\0') goto LAB_1028a40ae;
  }
  cVar1 = FUN_1015544c0(*(undefined8 *)(param_1 + 0xf0));
  if (cVar1 == '\0') {
    cVar1 = FUN_1015544c0(*(undefined8 *)(param_1 + 0x788));
    if (cVar1 != '\0') {
      return;
    }
    FUN_1028a3500(param_1,0,0);
    return;
  }
LAB_1028a40ae:
  FUN_1028a0460(param_1);
  return;
}

