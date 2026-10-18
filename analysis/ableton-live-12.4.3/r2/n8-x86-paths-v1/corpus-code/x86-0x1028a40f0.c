// x86 0x1028a40f0 FUN_1028a40f0 state=exported-with-warnings chunk=chunk-01917.jsonl code_sha256=6a8fdee3653bec8fdd63e7ba8685ed632a690d4d15b10b941be5c8499ce82588

void FUN_1028a40f0(long param_1)

{
  char cVar1;
  
  cVar1 = FUN_1015544c0(*(undefined8 *)(param_1 + 0x788));
  if (cVar1 == '\0') {
    if (*(long *)(param_1 + 0x8c8) != 0) {
      cVar1 = FUN_101a6f1b0();
      if (cVar1 != '\0') goto LAB_1028a412e;
    }
    cVar1 = FUN_1015544c0(*(undefined8 *)(param_1 + 0xf0));
    if (cVar1 == '\0') {
                    /* WARNING: Could not recover jumptable at 0x0001028a4158. Too many branches */
                    /* WARNING: Treating indirect jump as call */
      (**(code **)(**(long **)(param_1 + 0x5a8) + 0x248))(*(long **)(param_1 + 0x5a8),1);
      return;
    }
  }
LAB_1028a412e:
  FUN_1028a0460(param_1);
  return;
}

