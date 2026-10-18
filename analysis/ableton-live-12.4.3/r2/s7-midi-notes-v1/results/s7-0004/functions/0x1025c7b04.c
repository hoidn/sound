
void FUN_1025c7b04(long param_1)

{
  undefined1 auVar1 [16];
  
  auVar1 = NEON_fmov(0x3fe0000000000000,8);
  *(long *)(param_1 + 0x48) = auVar1._8_8_;
  *(long *)(param_1 + 0x40) = auVar1._0_8_;
  *(long *)(param_1 + 0x58) = auVar1._8_8_;
  *(long *)(param_1 + 0x50) = auVar1._0_8_;
  return;
}

