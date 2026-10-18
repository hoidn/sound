
void FUN_10276c6f4(long param_1)

{
  int iVar1;
  undefined8 uVar2;
  double dVar3;
  double dVar4;
  
  FUN_101486fa8();
  iVar1 = FUN_1015645a0(*(undefined8 *)(param_1 + 0x60));
  if (iVar1 != 0) {
    FUN_1027686f4(param_1);
  }
  uVar2 = *(undefined8 *)(param_1 + 0x1f8);
  dVar3 = (double)FUN_1015651fc(*(undefined8 *)(param_1 + 0x1c8));
  dVar4 = (double)FUN_1015651fc(*(undefined8 *)(param_1 + 0x1e0));
  FUN_1015652f0(dVar3 + dVar4,uVar2);
  uVar2 = FUN_102676cf0();
  FUN_1025fb288(uVar2,"OnLoad");
  return;
}

