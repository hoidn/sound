// 0xb6fb50 _ReWireFindReWireSharedLibraryFunction | undefined _ReWireFindReWireSharedLibraryFunction() | state=exported | chunk-00521.jsonl

undefined8 _ReWireFindReWireSharedLibraryFunction(undefined8 param_1)

{
  long lVar1;
  undefined8 uVar2;
  
  if (DAT_018aa5f8 != 0) {
    lVar1 = _CFStringCreateWithCString
                      (*(undefined8 *)PTR__kCFAllocatorDefault_01727060,param_1,0x8000100);
    if (lVar1 != 0) {
      uVar2 = _CFBundleGetFunctionPointerForName(DAT_018aa5f8,lVar1);
      _CFRelease(lVar1);
      return uVar2;
    }
  }
  return 0;
}

