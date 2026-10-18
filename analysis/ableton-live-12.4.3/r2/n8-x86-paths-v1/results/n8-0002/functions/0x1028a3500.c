
void FUN_1028a3500(long param_1,char param_2,undefined1 param_3)

{
  char cVar1;
  long *plVar2;
  long lVar3;
  undefined8 uVar4;
  undefined8 uVar5;
  undefined1 local_70 [48];
  int *local_40;
  int *local_38;
  int *local_30;
  
  plVar2 = (long *)FUN_10279e9c0();
  (**(code **)(*plVar2 + 0x998))(plVar2);
  if (*(char *)(param_1 + 0x8b0) == '\x01') {
    if (((*(long *)(param_1 + 0x48) == 0) ||
        (plVar2 = (long *)FUN_1027b59a0(), plVar2 == (long *)0x0)) ||
       (lVar3 = (**(code **)(*plVar2 + 0x198))(plVar2), lVar3 == 0)) {
      cVar1 = FUN_101a6c470(0);
    }
    else {
      uVar4 = FUN_10244a5b0(lVar3);
      cVar1 = FUN_101a6c470(uVar4);
    }
    if (cVar1 == '\0') {
      if (param_2 == '\0') {
        if ((*(double *)(param_1 + 0x968) != DAT_105b3ce00) ||
           (NAN(*(double *)(param_1 + 0x968)) || NAN(DAT_105b3ce00))) {
          if ((*(long *)(param_1 + 0x48) == 0) ||
             ((plVar2 = (long *)FUN_1027b59a0(), plVar2 == (long *)0x0 ||
              (lVar3 = (**(code **)(*plVar2 + 0x198))(plVar2), lVar3 == 0)))) {
            uVar4 = 0;
          }
          else {
            uVar4 = FUN_10244a5b0(lVar3);
          }
          uVar5 = *(undefined8 *)(param_1 + 0x968);
          goto LAB_1028a370b;
        }
      }
      else {
        if (((*(long *)(param_1 + 0x48) == 0) ||
            (plVar2 = (long *)FUN_1027b59a0(), plVar2 == (long *)0x0)) ||
           (lVar3 = (**(code **)(*plVar2 + 0x198))(plVar2), lVar3 == 0)) {
          uVar4 = 0;
        }
        else {
          uVar4 = FUN_10244a5b0(lVar3);
        }
        FUN_1028a2540(local_70,param_1);
        uVar5 = FUN_101a70860(local_70);
LAB_1028a370b:
        FUN_101a6f760(uVar5,uVar4,0x100500);
      }
      if (((*(long *)(param_1 + 0x48) == 0) ||
          (plVar2 = (long *)FUN_1027b59a0(), plVar2 == (long *)0x0)) ||
         (lVar3 = (**(code **)(*plVar2 + 0x198))(plVar2), lVar3 == 0)) {
        uVar4 = 0;
      }
      else {
        uVar4 = FUN_10244a5b0(lVar3);
      }
      FUN_101a6f1f0(uVar4,0x100500,1,0,param_3);
      cVar1 = FUN_1015544c0(*(undefined8 *)(param_1 + 0x5a8));
      goto joined_r0x0001028a35d0;
    }
  }
  cVar1 = FUN_1015544c0(*(undefined8 *)(param_1 + 0x5a8));
joined_r0x0001028a35d0:
  if (cVar1 != '\0') {
    uVar4 = FUN_10279e9c0();
    cVar1 = FUN_101706690(uVar4);
    if (cVar1 == '\0') {
      FUN_101547c30(local_70,*(undefined8 *)(param_1 + 0x48),param_1);
      FUN_1011a7c70(&local_40);
      FUN_1011a7c70(&local_38);
      FUN_1011a7c70(&local_30);
      FUN_101547ee0(local_70,&DAT_10752f568,&local_40,&local_38,&local_30);
      if ((local_30 != (int *)0x0) && (*local_30 = *local_30 + -1, *local_30 == 0)) {
        FUN_101442b40();
      }
      if ((local_38 != (int *)0x0) && (*local_38 = *local_38 + -1, *local_38 == 0)) {
        FUN_101442b40();
      }
      if ((local_40 != (int *)0x0) && (*local_40 = *local_40 + -1, *local_40 == 0)) {
        FUN_101442b40();
      }
      plVar2 = (long *)FUN_10279e9c0();
      (**(code **)(*plVar2 + 0x738))(plVar2);
      FUN_101548040(local_70);
      uVar4 = FUN_10279e9c0();
      FUN_1017a54d0(uVar4);
      FUN_101547e90(local_70);
    }
  }
  return;
}

