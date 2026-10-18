// 0x1025d9fac FUN_1025d9fac exported  sig: undefined FUN_1025d9fac()

void FUN_1025d9fac(long param_1)

{
  uint uVar1;
  uint *puVar2;
  
  if ((*(long *)(param_1 + 0x48) != 0) &&
     (puVar2 = *(uint **)(*(long *)(param_1 + 0x38) + 0x28), uVar1 = *puVar2,
     uVar1 < 9 && (1 << (ulong)(uVar1 & 0x1f) & 0x18eU) != 0)) {
    FUN_1025dca28(puVar2,3);
    return;
  }
  return;
}


