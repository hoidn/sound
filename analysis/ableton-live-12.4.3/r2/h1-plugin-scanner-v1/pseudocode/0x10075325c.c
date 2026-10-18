
void FUN_10075325c(undefined8 param_1)

{
  int iVar1;
  long local_18;
  
  local_18 = 0;
  iVar1 = _SecStaticCodeCreateWithPath(param_1,0,&local_18);
  if (iVar1 != 0) {
    return;
  }
  if (local_18 != 0) {
    _CFAutorelease();
  }
  _SecStaticCodeCheckValidity(local_18,9,0);
  return;
}

