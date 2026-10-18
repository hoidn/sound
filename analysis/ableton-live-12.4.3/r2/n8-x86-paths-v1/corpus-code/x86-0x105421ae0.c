// x86 0x105421ae0 FUN_105421ae0 state=exported-with-warnings chunk=chunk-03675.jsonl code_sha256=0c15babda82c9b383ac06d9d31f9b76df7c7974c0cdb389d5f5631c808b3d6c4

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 FUN_105421ae0(void)

{
  char cVar1;
  uint uVar2;
  undefined8 uVar3;
  undefined8 local_18;
  
  if (DAT_1074e2af8 != 0) {
    _DAT_1074e2af0 = _DAT_1074e2af0 + 1;
    return 1;
  }
  local_18 = 0;
  cVar1 = FUN_105421c60(&local_18,"ReWire Debugging.bundle");
  if (cVar1 == '\0') {
    cVar1 = FUN_105421c60(&local_18,"ReWire Testing.bundle");
    if (cVar1 == '\0') {
      cVar1 = FUN_105421c60(&local_18,"ReWire.bundle");
      if (cVar1 == '\0') {
        return 100;
      }
    }
  }
  uVar3 = local_18;
  DAT_1074e2af8 = _CFBundleCreate(*(undefined8 *)PTR__kCFAllocatorDefault_106a33388,local_18);
  _CFRelease(uVar3);
  if (DAT_1074e2af8 != 0) {
    uVar2 = _CFBundleGetVersionNumber();
    uVar3 = 0x65;
    if ((uVar2 & 0xff800000) == 0x1800000) {
      _DAT_1074e2af0 = 1;
      uVar3 = 1;
    }
    return uVar3;
  }
  return 9;
}

