
void FUN_10246a1a4(long *param_1)

{
  long lVar1;
  undefined8 *puVar2;
  
  lVar1 = FUN_1012d9734(0x128);
  puVar2 = (undefined8 *)FUN_102329650();
  *puVar2 = &PTR_thunk_FUN_102329838_1067b9830;
  puVar2[0xc] = &PTR_FUN_1067b9b08;
  *(undefined4 *)(puVar2 + 0x24) = 1;
  FUN_101486414();
  *param_1 = lVar1;
  *(int *)(lVar1 + 8) = *(int *)(lVar1 + 8) + 1;
  FUN_101482718(lVar1);
  return;
}

