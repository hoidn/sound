// 0x101a4517c FUN_101a4517c exported  sig: undefined FUN_101a4517c()

uint FUN_101a4517c(void)

{
  uint uVar1;
  ulong uVar2;
  
  uVar2 = FUN_101ab902c();
  if ((uVar2 & 1) != 0) {
    return 1;
  }
  uVar1 = FUN_101ab95ac();
  return uVar1 ^ 1;
}


