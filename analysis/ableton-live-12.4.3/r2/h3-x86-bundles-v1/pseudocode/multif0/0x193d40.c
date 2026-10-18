// 0x193d40 _mf0p_FreeMultiF0Result | undefined _mf0p_FreeMultiF0Result() | state=exported | chunk-00006.jsonl

void _mf0p_FreeMultiF0Result(long *param_1)

{
  long lVar1;
  int iVar2;
  
  if (param_1 != (long *)0x0) {
    if (0 < (int)param_1[1]) {
      iVar2 = 0;
      lVar1 = 0;
      do {
        _free(*(void **)(*param_1 + 0x10 + lVar1));
        iVar2 = iVar2 + 1;
        lVar1 = lVar1 + 0x20;
      } while (iVar2 < (int)param_1[1]);
    }
    _free((void *)*param_1);
    _free(param_1);
    return;
  }
  return;
}

