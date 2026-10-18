// x86 0x101198610 FUN_101198610 state=exported-with-warnings chunk=chunk-00677.jsonl code_sha256=75b4648fcc5951d9a76c6f9f3b3b097fccb248ae6388f90b18d9f7a77c413a40

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

uint FUN_101198610(void)

{
  char cVar1;
  uint extraout_EDX;
  undefined4 local_28;
  undefined4 uStack_24;
  undefined4 uStack_20;
  undefined4 uStack_1c;
  undefined8 local_18;
  undefined8 uStack_10;
  
  cVar1 = FUN_10118f7d0();
  if (cVar1 != '\0') {
    return 0;
  }
  local_18 = _DAT_105d5fe54;
  uStack_10 = _UNK_105d5fe5c;
  local_28 = _DAT_105d5fe44;
  uStack_24 = _UNK_105d5fe48;
  uStack_20 = _UNK_105d5fe4c;
  uStack_1c = _UNK_105d5fe50;
  FUN_101188890(&local_28);
  return (extraout_EDX ^ 1) & 0xffffff01;
}

