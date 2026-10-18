// x86 0x1031d7d70 FUN_1031d7d70 state=exported chunk=chunk-02323.jsonl code_sha256=2e3d70f510759965fa58a12c628264e678aa824f7caa86ec11873f43dddcd766

undefined8 FUN_1031d7d70(undefined8 param_1,long param_2)

{
  undefined8 *puVar1;
  
  if (*(int *)(param_2 + 0x48) == 0) {
    puVar1 = &DAT_1075566e8;
  }
  else {
    if (*(int *)(param_2 + 0x48) != 1) {
      FUN_1011a7c70(param_1);
      return param_1;
    }
    puVar1 = &DAT_1075566b8;
  }
  FUN_101440510(param_1,puVar1);
  return param_1;
}

