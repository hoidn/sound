
void * FUN_00001b7c(void)

{
  void *pvVar1;
  void *pvVar2;
  
  pvVar1 = operator_new(0xe0130);
  thunk_FUN_00001c84();
  pvVar2 = operator_new(0x48070);
  FUN_00015860();
  *(void **)((long)pvVar2 + 8) = pvVar1;
  FUN_00015950(0x3a83126f,pvVar2);
  FUN_000161c0(0x472c4400,pvVar2);
  return pvVar2;
}

