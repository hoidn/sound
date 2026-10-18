
void FUN_1028ab9f4(long *param_1)

{
  long lVar1;
  undefined8 *puVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  
  lVar1 = FUN_1012d9734(0x48);
  puVar2 = (undefined8 *)FUN_1014826c4();
  *puVar2 = &PTR_FUN_106820bd0;
  FUN_1028b1bfc(puVar2 + 5);
  *(undefined4 *)(lVar1 + 0x40) = 0xffffffff;
  FUN_101486414(lVar1);
  uVar4 = *(undefined8 *)(lVar1 + 0x30);
  uVar3 = FUN_1028e2540();
  FUN_10155ed5c(uVar4,uVar3,0x30);
  *param_1 = lVar1;
  *(int *)(lVar1 + 8) = *(int *)(lVar1 + 8) + 1;
  FUN_101482718(lVar1);
  return;
}

