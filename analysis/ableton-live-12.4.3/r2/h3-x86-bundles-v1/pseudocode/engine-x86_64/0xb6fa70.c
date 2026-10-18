// 0xb6fa70 _ReWireLoadReWireSharedLibrary | undefined _ReWireLoadReWireSharedLibrary() | state=exported-with-warnings | chunk-00521.jsonl

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 _ReWireLoadReWireSharedLibrary(void)

{
  char cVar1;
  uint uVar2;
  undefined8 uVar3;
  undefined8 local_18;
  
  if (DAT_018aa5f8 != 0) {
    _DAT_018aa5f0 = _DAT_018aa5f0 + 1;
    return 1;
  }
  local_18 = 0;
  cVar1 = FUN_00b6fbf0(&local_18,"ReWire Debugging.bundle");
  if (cVar1 == '\0') {
    cVar1 = FUN_00b6fbf0(&local_18,"ReWire Testing.bundle");
    if (cVar1 == '\0') {
      cVar1 = FUN_00b6fbf0(&local_18,"ReWire.bundle");
      if (cVar1 == '\0') {
        return 100;
      }
    }
  }
  uVar3 = local_18;
  DAT_018aa5f8 = _CFBundleCreate(*(undefined8 *)PTR__kCFAllocatorDefault_01727060,local_18);
  _CFRelease(uVar3);
  if (DAT_018aa5f8 != 0) {
    uVar2 = _CFBundleGetVersionNumber();
    uVar3 = 0x65;
    if ((uVar2 & 0xff800000) == 0x1800000) {
      _DAT_018aa5f0 = 1;
      uVar3 = 1;
    }
    return uVar3;
  }
  return 9;
}

