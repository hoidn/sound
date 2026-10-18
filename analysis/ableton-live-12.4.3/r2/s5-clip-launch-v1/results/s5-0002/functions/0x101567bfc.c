
void FUN_101567bfc(long param_1,undefined4 param_2,long param_3,long param_4,undefined8 param_5)

{
  long lVar1;
  
  lVar1 = param_3;
  if (param_4 != 0) {
    lVar1 = param_4;
  }
  *(undefined4 *)(param_1 + 0xd8) = param_2;
  FUN_101482dac();
  *(undefined4 *)(param_1 + 0xdc) = param_2;
  *(long *)(param_1 + 0x90) = param_3;
  *(long *)(param_1 + 0x98) = lVar1;
  FUN_10155e028(param_1,param_5);
  return;
}

