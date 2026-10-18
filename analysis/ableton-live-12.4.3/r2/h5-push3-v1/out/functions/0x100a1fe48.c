// 0x100a1fe48 FUN_100a1fe48 state=exported role=nanomsg bind (create_ep bind=1)
// source chunk chunk-00519.jsonl; code_sha256=003589a205a98b7f12d64d0810a33d8d11b55eea33cd61997f6d5919d259e695

undefined8 FUN_100a1fe48(uint param_1,undefined8 param_2)

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
    uVar2 = FUN_100a1ff34(lVar4,param_2,1);
    if (-1 < (int)uVar2) {
      FUN_100a36524(&DAT_101dee3e0);
      FUN_100a22578(lVar4);
      FUN_100a36540(&DAT_101dee3e0);
      return uVar2;
    }
    FUN_100a1fbd0(lVar4);
    piVar3 = ___error();
    *piVar3 = -(int)uVar2;
    return 0xffffffff;
  }
  FUN_1014efef0();
  return 0xffffffff;
}

