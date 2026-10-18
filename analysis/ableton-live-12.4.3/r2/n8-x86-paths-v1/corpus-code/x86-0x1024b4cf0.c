// x86 0x1024b4cf0 FUN_1024b4cf0 state=exported-with-warnings chunk=chunk-01670.jsonl code_sha256=4733a254b58bbd7b7e7bb484f53211cfe77eebc07354ad34d017578a16b62c11

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1024b4cf0(undefined8 *param_1)

{
  int *piVar1;
  undefined8 local_30;
  
  FUN_101479b80();
  *param_1 = &PTR_FUN_106cea210;
  param_1[5] = 0;
  FUN_1014425e0(param_1 + 7);
  FUN_10147d5c0(param_1);
  FUN_101553e70(&local_30);
  if (param_1[5] != 0) {
    piVar1 = (int *)(param_1[5] + 8);
    *piVar1 = *piVar1 + -1;
    if (*piVar1 == 0) {
      FUN_1012716c0();
    }
  }
  param_1[5] = local_30;
  *(undefined1 *)(param_1 + 6) = 0;
  *(undefined4 *)(param_1 + 8) = 0;
  param_1[9] = 0;
  _DAT_10749b898 = param_1;
  return;
}

