
undefined8 FUN_1049b2ed8(uint param_1,undefined8 param_2)

{
  int iVar1;
  undefined8 uVar2;
  int *piVar3;
  long lVar4;
  
  FUN_1049c95b4(&DAT_107048e78);
  if ((((param_1 < 0x200) && (DAT_1070489a8 != 0)) &&
      (lVar4 = *(long *)(DAT_1070489a8 + (ulong)param_1 * 8), lVar4 != 0)) &&
     (iVar1 = FUN_1049b55d8(lVar4), iVar1 == 0)) {
    FUN_1049c95d0(&DAT_107048e78);
    uVar2 = FUN_1049b2fc4(lVar4,param_2,1);
    if (-1 < (int)uVar2) {
      FUN_1049c95b4(&DAT_107048e78);
      FUN_1049b5608(lVar4);
      FUN_1049c95d0(&DAT_107048e78);
      return uVar2;
    }
    FUN_1049b2c60(lVar4);
    piVar3 = ___error();
    *piVar3 = -(int)uVar2;
    return 0xffffffff;
  }
  FUN_105443e24();
  return 0xffffffff;
}

