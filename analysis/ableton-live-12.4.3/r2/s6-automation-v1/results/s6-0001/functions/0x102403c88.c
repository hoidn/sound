
void FUN_102403c88(undefined8 param_1,undefined1 param_2 [16],double param_3,double param_4,
                  double param_5,long *param_6,long *param_7,undefined8 param_8)

{
  float fVar1;
  double dVar2;
  double dVar3;
  double dVar4;
  double dVar5;
  double dVar6;
  undefined4 local_78;
  undefined4 local_74;
  double local_70;
  double dStack_68;
  double local_60;
  double dStack_58;
  double dStack_50;
  double dStack_48;
  double local_40;
  double dStack_38;
  
  dVar2 = (double)param_6[10];
  local_74 = (**(code **)(*param_6 + 0x1f0))();
  fVar1 = (float)FUN_102778d28(dVar2,param_8,&local_74);
  dVar3 = (double)fVar1;
  dVar4 = (double)param_7[10];
  local_78 = (**(code **)(*param_7 + 0x1f0))(param_7);
  fVar1 = (float)FUN_102778d28(dVar4,param_8,&local_78);
  dVar5 = (double)(**(code **)(*param_6 + 0x218))(param_6);
  dVar6 = (double)fVar1 - dVar3;
  local_60 = dVar2 + (dVar4 - dVar2) * dVar5;
  dStack_58 = dVar3 + dVar6 * param_3;
  dStack_50 = dVar2 + (dVar4 - dVar2) * param_4;
  dStack_48 = dVar3 + dVar6 * param_5;
  local_70 = dVar2;
  dStack_68 = dVar3;
  local_40 = dVar4;
  dStack_38 = (double)fVar1;
  FUN_10121255c(param_1,&local_70);
  return;
}

