// arm 0x10276a7b0 FUN_10276a7b0 state=exported chunk=chunk-01922.jsonl code_sha256=3a4280de0861339b673aac0edd653f9db1d1725a05be1a2a5d07caa5bda95662

void FUN_10276a7b0(long param_1,int param_2,undefined8 param_3)

{
  int iVar1;
  long *plVar2;
  long lVar3;
  ulong uVar4;
  undefined8 uVar5;
  undefined8 uVar6;
  int *local_78;
  int *local_70;
  int *local_68;
  undefined1 auStack_60 [48];
  
  plVar2 = (long *)thunk_FUN_101849958();
  (**(code **)(*plVar2 + 0x998))();
  if (*(char *)(param_1 + 0x8b0) != '\x01') goto LAB_10276a8ec;
  if (((*(long *)(param_1 + 0x48) != 0) && (plVar2 = (long *)FUN_10268b7cc(), plVar2 != (long *)0x0)
      ) && (lVar3 = (**(code **)(*plVar2 + 0x198))(), lVar3 != 0)) {
    FUN_102336410();
  }
  uVar4 = FUN_101a48488();
  if ((uVar4 & 1) != 0) goto LAB_10276a8ec;
  if (param_2 == 0) {
    if (*(double *)(param_1 + 0x968) != 1.79769313486232e+308) {
      uVar5 = 0;
      if (*(long *)(param_1 + 0x48) != 0) {
        plVar2 = (long *)FUN_10268b7cc();
        uVar5 = 0;
        if (plVar2 != (long *)0x0) {
          lVar3 = (**(code **)(*plVar2 + 0x198))();
          uVar5 = 0;
          if (lVar3 != 0) {
            uVar5 = FUN_102336410();
          }
        }
      }
      uVar6 = *(undefined8 *)(param_1 + 0x968);
      goto LAB_10276a8a4;
    }
  }
  else {
    if (((*(long *)(param_1 + 0x48) == 0) ||
        (plVar2 = (long *)FUN_10268b7cc(), plVar2 == (long *)0x0)) ||
       (lVar3 = (**(code **)(*plVar2 + 0x198))(), lVar3 == 0)) {
      uVar5 = 0;
    }
    else {
      uVar5 = FUN_102336410();
    }
    FUN_102769868(auStack_60,param_1);
    uVar6 = FUN_101a4c2dc(auStack_60);
LAB_10276a8a4:
    FUN_101a4b1d0(uVar6,uVar5,0x100500);
  }
  uVar5 = 0;
  if (*(long *)(param_1 + 0x48) != 0) {
    plVar2 = (long *)FUN_10268b7cc();
    uVar5 = 0;
    if (plVar2 != (long *)0x0) {
      lVar3 = (**(code **)(*plVar2 + 0x198))();
      uVar5 = 0;
      if (lVar3 != 0) {
        uVar5 = FUN_102336410();
      }
    }
  }
  FUN_101a4abd8(uVar5,0x100500,1,0,param_3);
LAB_10276a8ec:
  iVar1 = FUN_1015645a0(*(undefined8 *)(param_1 + 0x5a8));
  if (iVar1 != 0) {
    thunk_FUN_101849958();
    uVar4 = FUN_1016f9c84();
    if ((uVar4 & 1) == 0) {
      FUN_101557e04(auStack_60,*(undefined8 *)(param_1 + 0x48),param_1);
      FUN_1011cb734(&local_68);
      FUN_1011cb734(&local_70);
      FUN_1011cb734(&local_78);
      FUN_101558118(auStack_60,&DAT_106e50678,&local_68,&local_70,&local_78);
      if ((local_78 != (int *)0x0) && (iVar1 = *local_78, *local_78 = iVar1 + -1, iVar1 + -1 == 0))
      {
        FUN_101449efc();
      }
      if ((local_70 != (int *)0x0) && (iVar1 = *local_70, *local_70 = iVar1 + -1, iVar1 + -1 == 0))
      {
        FUN_101449efc();
      }
      if ((local_68 != (int *)0x0) && (iVar1 = *local_68, *local_68 = iVar1 + -1, iVar1 + -1 == 0))
      {
        FUN_101449efc();
      }
      plVar2 = (long *)thunk_FUN_101849958();
      (**(code **)(*plVar2 + 0x738))();
      FUN_101558298(auStack_60);
      thunk_FUN_101849958();
      FUN_1017906e8();
      FUN_1015580bc(auStack_60);
    }
  }
  return;
}

