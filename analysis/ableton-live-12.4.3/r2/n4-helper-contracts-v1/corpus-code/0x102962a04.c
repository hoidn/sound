// 0x102962a04 FUN_102962a04 exported  sig: undefined FUN_102962a04()

void FUN_102962a04(long param_1)

{
  long lVar1;
  
  lVar1 = *(long *)(param_1 + 0x28);
  if (*(char *)(lVar1 + 0x38) == '\x01') {
    *(undefined1 *)(lVar1 + 0x38) = 0;
    FUN_1017cde1c(lVar1 + 0x18,0);
    if (*(long *)(lVar1 + 0x48) != 0) {
      FUN_1025d9fac();
      return;
    }
  }
  return;
}


