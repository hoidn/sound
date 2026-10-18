
bool FUN_101acfe68(long *param_1)

{
  long lVar1;
  
  (**(code **)(*param_1 + 0x28))();
  lVar1 = FUN_101ab4558();
  if (*(char *)(lVar1 + 0x68) == '\x01') {
    return *(long *)(lVar1 + 0x98) != param_1[0x76];
  }
  return false;
}

