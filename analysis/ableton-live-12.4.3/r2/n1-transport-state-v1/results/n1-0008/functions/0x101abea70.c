
int FUN_101abea70(int *param_1)

{
  int iVar1;
  undefined2 uVar2;
  uint uVar3;
  
  if (0 < *param_1) {
    iVar1 = param_1[1];
    uVar3 = CONCAT13(POPCOUNT((char)((uint)iVar1 >> 0x18)),
                     CONCAT12(POPCOUNT((char)((uint)iVar1 >> 0x10)),
                              CONCAT11(POPCOUNT((char)((uint)iVar1 >> 8)),POPCOUNT((char)iVar1))));
    uVar2 = NEON_uaddlv((ulong)uVar3,1);
    if (iVar1 - 1U < 0x10 && CONCAT22((short)(uVar3 >> 0x10),uVar2) == 1) {
      return *param_1 + (0x1f - (int)LZCOUNT(iVar1)) * 99 + -1;
    }
  }
  return -0x80000000;
}

