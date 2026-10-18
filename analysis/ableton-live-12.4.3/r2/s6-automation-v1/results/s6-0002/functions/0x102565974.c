
void FUN_102565974(long *param_1,double param_2,long param_3,int param_4)

{
  long lVar1;
  long *plVar2;
  long lVar3;
  long *plVar4;
  undefined8 uVar5;
  long lVar6;
  
  FUN_102565a48(*(undefined8 *)(param_3 + 0x58),*(undefined8 *)(param_3 + 0x100));
  lVar1 = *param_1;
  if (param_1[1] == lVar1) {
    lVar6 = *(long *)(lVar1 + 0x18);
  }
  else {
    lVar6 = *(long *)(param_1[1] + 0x18);
    param_1[1] = lVar6;
    if (param_4 != 1) {
      return;
    }
    if (lVar6 == lVar1) {
      return;
    }
    if (lVar6 != *(long *)(lVar1 + 0x20)) {
      plVar4 = (long *)param_1[2];
      do {
        uVar5 = *(undefined8 *)(lVar6 + 0x18);
        plVar2 = (long *)(**(code **)(*plVar4 + 0x60))(plVar4);
        lVar3 = (**(code **)(*plVar2 + 0x20))(plVar2,plVar4,uVar5);
        if (*(double *)(*(long *)(lVar3 + 8) + 0x50) != param_2) break;
        lVar6 = *(long *)(lVar6 + 0x18);
      } while (lVar6 != *(long *)(lVar1 + 0x20));
    }
  }
  param_1[1] = lVar6;
  return;
}

