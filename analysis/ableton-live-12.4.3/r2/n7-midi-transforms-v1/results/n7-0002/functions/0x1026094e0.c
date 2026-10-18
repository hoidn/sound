
void FUN_1026094e0(long *param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4,
                  long param_5)

{
  undefined8 uVar1;
  undefined8 uVar2;
  undefined8 *puVar3;
  undefined1 auStack_8c [12];
  undefined1 auStack_80 [8];
  long local_78;
  int local_70;
  char local_6c;
  undefined1 auStack_5c [12];
  
  uVar1 = thunk_FUN_101a9b404(0x48);
  FUN_101b7fc28();
  uVar2 = FUN_101b7c22c(param_2);
  uVar2 = (**(code **)(*param_1 + 0x48))(param_1,uVar2);
  FUN_101b7fc74(uVar1,uVar2,param_2,0);
  uVar2 = thunk_FUN_101a9b404(0x38);
  FUN_101b7b55c();
  puVar3 = (undefined8 *)(**(code **)(*param_1 + 0x60))(param_1,5);
  FUN_101b7b59c(uVar2,uVar1,*puVar3,1,1);
  FUN_101b7b878(auStack_5c,param_3,param_4,5);
  if (*(char *)(param_5 + 0x20) == '\x01') {
    (**(code **)(*param_1 + 0x80))(param_1,auStack_5c,uVar2,param_2,param_5);
  }
  else {
    FUN_101b7ca84(auStack_80,1);
    (**(code **)(*param_1 + 0x80))(param_1,auStack_5c,uVar2,param_2,auStack_80);
    if ((local_78 != 0) && (local_6c == '\x01')) {
      thunk_FUN_101aa0360(local_78,(long)local_70);
    }
  }
  uVar2 = thunk_FUN_101a9b404(0x38);
  FUN_101b7b55c();
  thunk_FUN_101a9b64c(uVar1);
  puVar3 = (undefined8 *)(**(code **)(*param_1 + 0x60))(param_1,6);
  FUN_101b7b59c(uVar2,uVar1,*puVar3,1,1);
  FUN_101b7b878(auStack_8c,param_3,(int)param_4 + 0x20,5);
  FUN_101b7ca84(auStack_80,1);
  (**(code **)(*param_1 + 0x80))(param_1,auStack_8c,uVar2,param_2,auStack_80);
  if ((local_78 != 0) && (local_6c == '\x01')) {
    thunk_FUN_101aa0360(local_78,(long)local_70);
  }
  return;
}

