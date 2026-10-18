
void FUN_102565e10(long *param_1,double param_2,long param_3,int param_4)

{
  long lVar1;
  long *plVar2;
  long lVar3;
  long lVar4;
  long *plVar5;
  undefined8 uVar6;
  
  FUN_102565a48(*(undefined8 *)(param_3 + 0x58),*(undefined8 *)(param_3 + 0x100));
  lVar1 = *param_1;
  if (param_1[1] != *(long *)(lVar1 + 0x20)) {
    lVar4 = *(long *)(param_1[1] + 0x18);
    param_1[1] = lVar4;
    plVar5 = (long *)param_1[2];
    plVar2 = (long *)(**(code **)(*plVar5 + 0x60))(plVar5);
    lVar3 = (**(code **)(*plVar2 + 0x20))(plVar2,plVar5,lVar4);
    if (*(double *)(*(long *)(lVar3 + 8) + 0x50) <= param_2) {
      if (param_4 != 1) {
        return;
      }
      if (lVar4 != *(long *)(lVar1 + 0x20)) {
        do {
          uVar6 = *(undefined8 *)(lVar4 + 0x18);
          plVar2 = (long *)(**(code **)(*plVar5 + 0x60))(plVar5);
          lVar3 = (**(code **)(*plVar2 + 0x20))(plVar2,plVar5,uVar6);
          if (*(double *)(*(long *)(lVar3 + 8) + 0x50) != param_2) break;
          lVar4 = *(long *)(lVar4 + 0x18);
        } while (lVar4 != *(long *)(lVar1 + 0x20));
      }
    }
    else {
      lVar4 = *(long *)(lVar4 + 0x20);
    }
    param_1[1] = lVar4;
  }
  return;
}

