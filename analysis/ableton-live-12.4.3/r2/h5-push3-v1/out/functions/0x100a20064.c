// 0x100a20064 FUN_100a20064 state=exported role=nanomsg connect (create_ep bind=0)
// source chunk chunk-00519.jsonl; code_sha256=4a6bdc525ffecc049a2224c7a918b9c6a1c1bb947a4b5c969e84787d68372d03

undefined8 FUN_100a20064(uint param_1,undefined8 param_2)

{
  int iVar1;
  undefined8 uVar2;
  int *piVar3;
  long lVar4;
  
  FUN_100a36524(&DAT_101dee3e0);
  if ((((param_1 < 0x200) && (DAT_101dedf10 != 0)) &&
      (lVar4 = *(long *)(DAT_101dedf10 + (ulong)param_1 * 8), lVar4 != 0)) &&
     (iVar1 = FUN_100a22548(lVar4), iVar1 == 0)) {
    FUN_100a36540(&DAT_101dee3e0);
    uVar2 = FUN_100a1ff34(lVar4,param_2,0);
    FUN_100a36524(&DAT_101dee3e0);
    FUN_100a22578(lVar4);
    FUN_100a36540(&DAT_101dee3e0);
    if (-1 < (int)uVar2) {
      return uVar2;
    }
    iVar1 = -(int)uVar2;
  }
  else {
    FUN_100a36540(&DAT_101dee3e0);
    iVar1 = 9;
  }
  piVar3 = ___error();
  *piVar3 = iVar1;
  return 0xffffffff;
}

