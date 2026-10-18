// 0x1038f08c4 FUN_1038f08c4 exported  sig: undefined FUN_1038f08c4()

void FUN_1038f08c4(long param_1)

{
  if ((*(byte *)(param_1 + 0x78) & 1) != 0) {
    return;
  }
  *(undefined1 *)(param_1 + 0x78) = 1;
  if (*(int *)(param_1 + 0x74) != 0) {
    FUN_1038f0914();
    return;
  }
  FUN_1025db018(*(undefined8 *)(param_1 + 0x60),param_1 + 0x18);
  FUN_1038f0914(param_1);
  return;
}


