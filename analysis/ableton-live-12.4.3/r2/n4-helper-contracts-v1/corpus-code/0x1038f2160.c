// 0x1038f2160 thunk_FUN_1038f1fcc exported  sig: undefined thunk_FUN_1038f1fcc()

long thunk_FUN_1038f1fcc(long param_1,long *param_2,undefined8 param_3)

{
  long *plVar1;
  undefined8 *puVar2;
  long lVar3;
  long *plStack_48;
  
  puVar2 = (undefined8 *)FUN_10128ed98();
  *puVar2 = &PTR_thunk_FUN_1038f2164_106a3e1c8;
  puVar2[3] = 0;
  plStack_48 = operator_new(0x58);
  *plStack_48 = (long)&PTR_thunk_FUN_10027a25c_1065928b0;
  plStack_48[1] = (long)(plStack_48 + 2);
  *(undefined8 *)((long)plStack_48 + 0x14) = DAT_1055d3960;
  *(undefined4 *)((long)plStack_48 + 0x1c) = 0xffffffff;
  if (*(char *)((long)param_2 + 0x17) < '\0') {
    FUN_10023448c(plStack_48 + 4,*param_2,param_2[1]);
  }
  else {
    lVar3 = *param_2;
    plStack_48[5] = param_2[1];
    plStack_48[4] = lVar3;
    plStack_48[6] = param_2[2];
  }
  *(undefined4 *)(plStack_48 + 7) = 0;
  plStack_48[9] = 0;
  plStack_48[10] = 0;
  plStack_48[8] = 0;
  FUN_1053ddf54(param_1 + 0x20,&plStack_48);
  plVar1 = plStack_48;
  plStack_48 = (long *)0x0;
  if (plVar1 != (long *)0x0) {
    (**(code **)(*plVar1 + 8))();
  }
  *(undefined4 *)(param_1 + 0x170) = 0;
  *(undefined8 *)(param_1 + 0x178) = param_3;
  FUN_103906790(param_3,param_1);
  return param_1;
}


