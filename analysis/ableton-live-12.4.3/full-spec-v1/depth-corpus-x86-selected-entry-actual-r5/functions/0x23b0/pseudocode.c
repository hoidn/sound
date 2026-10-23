
long _CreateInstanceU(void)

{
  undefined8 uVar1;
  undefined8 uVar2;
  long lVar3;
  
  uVar1 = _newlocale(0x3f,"C",0);
  uVar2 = _uselocale(uVar1);
  lVar3 = __Znwm(0xe0500);
  func_0x0000dc20(lVar3);
  *(undefined8 *)(lVar3 + 0xe04f8) = 0x113a0000113a;
  _uselocale(uVar2);
  _freelocale(uVar1);
  return lVar3;
}

