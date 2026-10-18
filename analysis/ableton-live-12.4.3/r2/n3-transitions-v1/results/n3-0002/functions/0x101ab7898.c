
void FUN_101ab7898(long param_1)

{
  undefined8 uVar1;
  
  if (*(undefined2 **)(param_1 + 8) != &DAT_106f56460) {
    FUN_101a9ccd0(param_1);
    uVar1 = FUN_101aae14c();
    FUN_101aaca84(uVar1,*(undefined8 *)(param_1 + 8),*(undefined4 *)(param_1 + 0x10),
                  *(undefined4 *)(param_1 + 0x14),*(undefined4 *)(param_1 + 0x18));
  }
  *(undefined8 *)(param_1 + 8) = 0;
  return;
}

