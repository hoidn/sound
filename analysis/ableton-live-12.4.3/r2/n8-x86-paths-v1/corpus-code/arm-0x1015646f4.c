// arm 0x1015646f4 FUN_1015646f4 state=exported chunk=chunk-00832.jsonl code_sha256=7d290f2dc6ea44e96caa3841f95b99a4083f7e7ea54990c9e9380ab93be2ff14

void FUN_1015646f4(long param_1,uint param_2)

{
  if (*(byte *)(param_1 + 0x60) != param_2) {
    *(char *)(param_1 + 0x60) = (char)param_2;
  }
  return;
}

