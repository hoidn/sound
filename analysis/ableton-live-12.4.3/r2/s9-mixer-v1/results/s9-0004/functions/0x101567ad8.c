
void FUN_101567ad8(long param_1,undefined4 param_2,long *param_3,undefined8 param_4)

{
  long *plVar1;
  long *plVar2;
  
  *(undefined4 *)(param_1 + 0xd8) = param_2;
  FUN_101482dac();
  *(undefined4 *)(param_1 + 0xdc) = param_2;
  plVar1 = (long *)(param_1 + 0x60);
  if (plVar1 != param_3) {
    FUN_1006f7258(plVar1,*param_3,param_3[1],param_3[1] - *param_3 >> 3);
  }
  plVar2 = (long *)(param_1 + 0x78);
  if (plVar2 != param_3) {
    FUN_1006f7258(plVar2,*param_3,param_3[1],param_3[1] - *param_3 >> 3);
  }
  *(long **)(param_1 + 0x90) = plVar1;
  *(long **)(param_1 + 0x98) = plVar2;
  FUN_10155e028(param_1,param_4);
  return;
}

