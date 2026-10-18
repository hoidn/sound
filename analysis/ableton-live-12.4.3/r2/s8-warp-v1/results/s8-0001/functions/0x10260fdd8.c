
void FUN_10260fdd8(void)

{
  int iVar1;
  undefined1 auStack_30 [8];
  int *local_28;
  
  FUN_10120d9f0(auStack_30,0);
  FUN_10147e954(&DAT_106e4e4f0,0xffffffff,0xffffffff,0x50,L"mSecTime",8,&DAT_1062a3ca0,0,auStack_30,
                0x4fffffffc);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  FUN_10120d9f0(auStack_30,0);
  FUN_10147e954(&DAT_106e4e4f0,0xffffffff,0xffffffff,0x58,L"mBeatTime",9,&DAT_1062a3ca0,0,auStack_30
                ,0x4fffffffc);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  return;
}

