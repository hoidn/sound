// x86 0x1024b4840 FUN_1024b4840 state=exported-with-warnings chunk=chunk-01670.jsonl code_sha256=2a03ca7b3a9ab7cd2f4ef3d63dc5f62d7416d289d4b4102991b095dd3cb74bda

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 FUN_1024b4840(void)

{
  char cVar1;
  undefined8 uVar2;
  byte extraout_DL;
  undefined4 local_28;
  undefined4 uStack_24;
  undefined4 uStack_20;
  undefined4 uStack_1c;
  undefined8 local_18;
  undefined8 uStack_10;
  
  cVar1 = FUN_101ab6780();
  if (cVar1 != '\0') {
    local_18 = _DAT_105de827c;
    uStack_10 = _UNK_105de8284;
    local_28 = _DAT_105de826c;
    uStack_24 = _UNK_105de8270;
    uStack_20 = _UNK_105de8274;
    uStack_1c = _UNK_105de8278;
    FUN_101188890(&local_28);
    if ((extraout_DL & 1) == 0) {
      uVar2 = FUN_101198610();
      return uVar2;
    }
  }
  return 0;
}

