// 0x1006677a8 FUN_1006677a8 state=exported role=one-byte message
// source chunk chunk-00229.jsonl; code_sha256=a27312396f929f74121e1817d3d4c713569e45a820b916e2df0196f386a69f01

void FUN_1006677a8(undefined8 *param_1,undefined1 param_2)

{
  undefined1 *puVar1;
  
  *param_1 = 0;
  param_1[1] = 0;
  param_1[2] = 0;
  puVar1 = operator_new(1);
  *param_1 = puVar1;
  *puVar1 = param_2;
  param_1[1] = puVar1 + 1;
  param_1[2] = puVar1 + 1;
  return;
}

