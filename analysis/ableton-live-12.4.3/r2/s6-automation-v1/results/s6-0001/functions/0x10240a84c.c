
void FUN_10240a84c(undefined8 param_1,double *param_2,long *param_3,undefined8 param_4)

{
  long *plVar1;
  long lVar2;
  long local_38;
  long local_30;
  long *local_28;
  
  (**(code **)(*param_3 + 1000))(&local_38,*param_2,param_3,param_4);
  lVar2 = local_30;
  if (((int)param_4 == 0) && (local_30 != *(long *)(local_38 + 0x18))) {
    plVar1 = (long *)(**(code **)(*local_28 + 0x60))();
    lVar2 = (**(code **)(*plVar1 + 0x20))(plVar1,local_28,lVar2);
    if (*(double *)(*(long *)(lVar2 + 8) + 0x50) == *param_2) {
      local_30 = *(long *)(local_30 + 0x20);
    }
  }
  lVar2 = local_30;
  plVar1 = (long *)(**(code **)(*local_28 + 0x60))();
  lVar2 = (**(code **)(*plVar1 + 0x20))(plVar1,local_28,lVar2);
  (**(code **)(**(long **)(lVar2 + 8) + 0x1f0))();
  return;
}

