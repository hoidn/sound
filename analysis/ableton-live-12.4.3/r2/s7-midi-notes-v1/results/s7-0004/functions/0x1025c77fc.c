
void FUN_1025c77fc(long *param_1)

{
  long lVar1;
  undefined8 *puVar2;
  undefined1 auVar3 [16];
  
  lVar1 = FUN_1012d9734(0x60);
  puVar2 = (undefined8 *)FUN_1014826c4();
  *puVar2 = &PTR_thunk_FUN_10128edf8_1067df620;
  puVar2[5] = &PTR_FUN_1067df7d8;
  puVar2[6] = &DAT_7fefffffffffffff;
  *(undefined4 *)(puVar2 + 7) = 0;
  auVar3 = NEON_fmov(0x3fe0000000000000,8);
  puVar2[9] = auVar3._8_8_;
  puVar2[8] = auVar3._0_8_;
  puVar2[0xb] = auVar3._8_8_;
  puVar2[10] = auVar3._0_8_;
  FUN_101486414();
  *param_1 = lVar1;
  *(int *)(lVar1 + 8) = *(int *)(lVar1 + 8) + 1;
  FUN_101482718(lVar1);
  return;
}

