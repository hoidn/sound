
void FUN_102777f3c(undefined8 *param_1)

{
  undefined8 *puVar1;
  undefined8 *puVar2;
  
  puVar1 = (undefined8 *)FUN_1012d9734(0x60);
  puVar2 = (undefined8 *)FUN_1024deba8();
  *puVar2 = &PTR_FUN_1068061a0;
  FUN_101486414();
  *puVar1 = &PTR_thunk_FUN_10155dda8_106806600;
  FUN_101486414(puVar1);
  *(undefined4 *)(puVar1 + 0xb) = 0x80000000;
  *param_1 = puVar1;
  *(int *)(puVar1 + 1) = *(int *)(puVar1 + 1) + 1;
  FUN_101482718(puVar1);
  return;
}

