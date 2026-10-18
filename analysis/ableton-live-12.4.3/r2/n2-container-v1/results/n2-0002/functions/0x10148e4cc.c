
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_10148e4cc(void)

{
  long lVar1;
  undefined1 auStack_228 [480];
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_1064f8818;
  FUN_101426298(&DAT_106f4f648);
  ___cxa_atexit(FUN_101426318,&DAT_106f4f648,0x100000000);
  uRam0000000106f4f788 = 0;
  _DAT_106f4f780 = 0;
  uRam0000000106f4f798 = 0;
  _DAT_106f4f790 = 0;
  DAT_106f4f7a0 = 0x3f800000;
  ___cxa_atexit(FUN_10147e3cc,&DAT_106f4f780,0x100000000);
  _memcpy(auStack_228,&DAT_105815550,0x1e0);
  lVar1 = 0;
  DAT_106f4f7b0 = 0;
  DAT_106f4f7a8 = 0;
  DAT_106f4f7c0 = 0;
  _DAT_106f4f7b8 = 0;
  DAT_106f4f7c8 = 0x3f800000;
  do {
    FUN_10148dd1c(&DAT_106f4f7a8,auStack_228 + lVar1,auStack_228 + lVar1);
    lVar1 = lVar1 + 8;
  } while (lVar1 != 0x1e0);
  ___cxa_atexit(FUN_101480020,&DAT_106f4f7a8,0x100000000);
  FUN_10147e458(&DAT_106e0cdf8,L"ACompound",9,&DAT_106e0cdf8,PTR_SNewCompound<ACompound>_1064fdbb8,
                FUN_10148265c,0,1,0);
  ___cxa_atexit(thunk_FUN_10147e7d0,&DAT_106e0cdf8,0x100000000);
  thunk_FUN_101446d04(&DAT_106f4f708,"ACompound","sErrorDocumentCorruptWhileReading");
  ___cxa_atexit(FUN_100236a4c,&DAT_106f4f708,0x100000000);
  thunk_FUN_101446d04(&DAT_106f4f720,"ACompound","sErrorDocumentIsFromNewerVersion");
  ___cxa_atexit(FUN_100236a4c,&DAT_106f4f720,0x100000000);
  thunk_FUN_101446d04(&DAT_106f4f738,"ACompound","sErrorClassesMissingFromSchema");
  ___cxa_atexit(FUN_100236a4c,&DAT_106f4f738,0x100000000);
  DAT_106f4f758 = 0;
  DAT_106f4f750 = &DAT_106f4f758;
  DAT_106f4f760 = 0;
  ___cxa_atexit(FUN_1004629c4,&DAT_106f4f750,0x100000000);
  if (*(long *)PTR____stack_chk_guard_1064f8818 == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

