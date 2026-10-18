
undefined8 FUN_10246a2e8(undefined8 param_1,undefined8 param_2,int param_3)

{
  long lVar1;
  undefined8 uVar2;
  
  uVar2 = param_1;
  if ((DAT_10700a2d0 & 1) == 0) {
    uVar2 = FUN_105421040();
  }
  if ((DAT_10700a2d8 & 1) == 0) {
    FUN_105421080(uVar2,param_2);
  }
  lVar1 = 0xd0;
  if (param_3 == 0) {
    lVar1 = 0xc0;
  }
  FUN_1023298f8(param_1,param_2,&DAT_10700a268 + lVar1);
  return param_1;
}

