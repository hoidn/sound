
void FUN_1027785a0(undefined8 *param_1)

{
  undefined8 *puVar1;
  undefined8 *puVar2;
  undefined1 auVar3 [16];
  
  puVar1 = (undefined8 *)FUN_1012d9734(0x80);
  puVar2 = (undefined8 *)FUN_1024deba8();
  *puVar2 = &PTR_FUN_1068061a0;
  FUN_101486414();
  *puVar1 = &PTR_thunk_FUN_10155dda8_106806830;
  *(undefined4 *)(puVar1 + 0xb) = 0x7f7fffff;
  auVar3 = NEON_fmov(0x3fe0000000000000,8);
  puVar1[0xd] = auVar3._8_8_;
  puVar1[0xc] = auVar3._0_8_;
  puVar1[0xf] = auVar3._8_8_;
  puVar1[0xe] = auVar3._0_8_;
  FUN_101486414(puVar1);
  *param_1 = puVar1;
  *(int *)(puVar1 + 1) = *(int *)(puVar1 + 1) + 1;
  FUN_101482718(puVar1);
  return;
}

