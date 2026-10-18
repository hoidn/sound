
void FUN_101463eb4(undefined8 *param_1)

{
  undefined8 *puVar1;
  
  puVar1 = (undefined8 *)FUN_1012d9850(0x78);
  FUN_10128ed98();
  *puVar1 = &PTR_FUN_10666fa70;
  FUN_101449838(puVar1 + 3);
  puVar1[4] = 0;
  *puVar1 = &PTR_thunk_FUN_101463f7c_106672718;
  puVar1[6] = 0;
  puVar1[5] = 0;
  puVar1[8] = 0;
  puVar1[7] = 0;
  puVar1[9] = 0x100000000000;
  *(undefined1 *)(puVar1 + 10) = 0;
  *(undefined1 *)(puVar1 + 0xd) = 0;
  *(undefined4 *)(puVar1 + 0xe) = 0;
  *(undefined1 *)((long)puVar1 + 0x74) = 0;
  *param_1 = puVar1;
  *(int *)(puVar1 + 1) = *(int *)(puVar1 + 1) + 1;
  return;
}

