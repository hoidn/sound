
void FUN_10146208c(long *param_1)

{
  long lVar1;
  
  lVar1 = FUN_1012d9850(0x38);
  FUN_1014620e8();
  *param_1 = lVar1;
  if (lVar1 != 0) {
    *(int *)(lVar1 + 8) = *(int *)(lVar1 + 8) + 1;
  }
  return;
}

