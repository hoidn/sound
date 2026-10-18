// x86 0x1024b6190 FUN_1024b6190 state=exported chunk=chunk-01671.jsonl code_sha256=9704f7aa0949d4a99a1ceec0790eb0ed27ab9aa9a1a0fc3ca1d59cdd6e82e55c

long * FUN_1024b6190(long *param_1)

{
  long lVar1;
  
  lVar1 = FUN_1012bd9b0(0x50);
  FUN_1024b4cf0(lVar1);
  *param_1 = lVar1;
  if (lVar1 != 0) {
    *(int *)(lVar1 + 8) = *(int *)(lVar1 + 8) + 1;
  }
  FUN_101479bf0(lVar1);
  return param_1;
}

