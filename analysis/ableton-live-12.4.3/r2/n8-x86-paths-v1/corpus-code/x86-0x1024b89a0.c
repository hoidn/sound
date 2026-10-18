// x86 0x1024b89a0 FUN_1024b89a0 state=exported-with-warnings chunk=chunk-01672.jsonl code_sha256=d0362966ebea261af907cb3d684db8fad45de79e387fb6cbf5e61a50cbac6725

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 FUN_1024b89a0(int param_1)

{
  int *piVar1;
  char cVar2;
  ulong extraout_RDX;
  undefined4 local_58;
  undefined4 uStack_54;
  undefined4 uStack_50;
  undefined4 uStack_4c;
  undefined8 local_48;
  undefined8 uStack_40;
  int *local_30;
  int *local_28;
  int *local_20;
  int *local_18;
  
  if (param_1 == 1) {
    cVar2 = FUN_10118f7d0();
    if (cVar2 == '\0') {
      FUN_1011a7c70(&local_58);
      FUN_1011a7c70(&local_30);
      FUN_1011a7c70(&local_28);
      FUN_1011a7c70(&local_20);
      FUN_1011a7c70(&local_18);
      FUN_101222a20(&DAT_10749b868,&local_58,&local_30,&local_28,&local_20,&local_18);
      if ((local_18 != (int *)0x0) && (*local_18 = *local_18 + -1, *local_18 == 0)) {
        FUN_101442b40();
      }
      if ((local_20 != (int *)0x0) && (*local_20 = *local_20 + -1, *local_20 == 0)) {
        FUN_101442b40();
      }
      if ((local_28 != (int *)0x0) && (*local_28 = *local_28 + -1, *local_28 == 0)) {
        FUN_101442b40();
      }
      if ((local_30 != (int *)0x0) && (*local_30 = *local_30 + -1, *local_30 == 0)) {
        FUN_101442b40();
      }
      piVar1 = (int *)CONCAT44(uStack_54,local_58);
      if ((piVar1 != (int *)0x0) && (*piVar1 = *piVar1 + -1, *piVar1 == 0)) {
        FUN_101442b40();
      }
    }
  }
  else {
    if (param_1 != 2) {
      return 1;
    }
    local_48 = _DAT_105de829c;
    uStack_40 = _UNK_105de82a4;
    local_58 = _DAT_105de828c;
    uStack_54 = _UNK_105de8290;
    uStack_50 = _UNK_105de8294;
    uStack_4c = _UNK_105de8298;
    FUN_101188890(&local_58);
    if (((extraout_RDX & 1) == 0) && (cVar2 = FUN_101198610(), cVar2 != '\0')) {
      FUN_1011a7c70(&local_58);
      FUN_1011a7c70(&local_30);
      FUN_1011a7c70(&local_28);
      FUN_1011a7c70(&local_20);
      FUN_1011a7c70(&local_18);
      FUN_101222a20(&DAT_10749b850,&local_58,&local_30,&local_28,&local_20,&local_18);
      if ((local_18 != (int *)0x0) && (*local_18 = *local_18 + -1, *local_18 == 0)) {
        FUN_101442b40();
      }
      if ((local_20 != (int *)0x0) && (*local_20 = *local_20 + -1, *local_20 == 0)) {
        FUN_101442b40();
      }
      if ((local_28 != (int *)0x0) && (*local_28 = *local_28 + -1, *local_28 == 0)) {
        FUN_101442b40();
      }
      if ((local_30 != (int *)0x0) && (*local_30 = *local_30 + -1, *local_30 == 0)) {
        FUN_101442b40();
      }
      piVar1 = (int *)CONCAT44(uStack_54,local_58);
      if ((piVar1 != (int *)0x0) && (*piVar1 = *piVar1 + -1, *piVar1 == 0)) {
        FUN_101442b40();
      }
    }
  }
  DAT_10749b880 = 1;
  return 0;
}

