
void FUN_102875ec0(void)

{
  int iVar1;
  undefined4 uVar2;
  undefined4 *puVar3;
  undefined4 local_30 [2];
  int *local_28;
  
  FUN_10120d8a0(local_30,0);
  FUN_10147e954(&DAT_106e57440,0xffffffff,0xffffffff,0xe8,L"mDefaultDuration",0x10,&DAT_1062a3ca0,0,
                local_30,0xfffffffc);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  FUN_10120d8a0(local_30,0);
  FUN_10147e954(&DAT_106e57440,0xffffffff,0xffffffff,0xec,L"mDefaultSampleRate",0x12,&DAT_1062a3ca0,
                0,local_30,0xfffffffc);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  puVar3 = (undefined4 *)FUN_101565d6c();
  local_30[0] = *puVar3;
  local_28 = *(int **)(puVar3 + 2);
  if (local_28 != (int *)0x0) {
    *local_28 = *local_28 + 1;
  }
  uVar2 = FUN_101565d9c();
  FUN_10147e954(&DAT_106e57440,0xffffffff,0xffffffff,0x100,L"mpSamplesToAutoWarp",0x13,
                &DAT_1062a3ca0,0,local_30,uVar2);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  return;
}

