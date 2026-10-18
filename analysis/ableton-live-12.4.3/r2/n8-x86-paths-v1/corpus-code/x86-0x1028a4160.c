// x86 0x1028a4160 FUN_1028a4160 state=exported chunk=chunk-01917.jsonl code_sha256=2b1d9237fdc4ee68cc8b951f315723cdbb06d824d4966de9d22a4af57903b643

void FUN_1028a4160(long param_1)

{
  char cVar1;
  
  cVar1 = FUN_1015544c0(*(undefined8 *)(param_1 + 0x788));
  if (cVar1 == '\0') {
    if (*(long *)(param_1 + 0x8c8) != 0) {
      cVar1 = FUN_101a6f1b0();
      if (cVar1 != '\0') goto LAB_1028a419e;
    }
    cVar1 = FUN_1015544c0(*(undefined8 *)(param_1 + 0xf0));
    if (cVar1 == '\0') {
      FUN_1028a3500(param_1,0,0);
      return;
    }
  }
LAB_1028a419e:
  FUN_1028a0460(param_1);
  return;
}

