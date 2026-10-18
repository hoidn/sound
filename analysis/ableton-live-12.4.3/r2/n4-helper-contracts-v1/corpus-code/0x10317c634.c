// 0x10317c634 FUN_10317c634 exported  sig: undefined FUN_10317c634()

void FUN_10317c634(long param_1)

{
  int iVar1;
  long lVar2;
  void *pvVar3;
  long lVar4;
  int *local_50;
  void *local_48;
  undefined8 local_40;
  undefined8 local_38;
  undefined8 uStack_30;
  undefined4 local_28;
  
  local_50 = (int *)0x0;
  local_48 = (void *)0x0;
  *(undefined8 *)(param_1 + 0x90) = 0;
  lVar2 = *(long *)(param_1 + 0x88);
  if (lVar2 != 0) {
    iVar1 = *(int *)(lVar2 + 8) + -1;
    *(int *)(lVar2 + 8) = iVar1;
    if (iVar1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined8 *)(param_1 + 0x88) = 0;
  lVar2 = *(long *)(param_1 + 0x80);
  if (lVar2 != 0) {
    iVar1 = *(int *)(lVar2 + 8) + -1;
    *(int *)(lVar2 + 8) = iVar1;
    if (iVar1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined8 *)(param_1 + 0x80) = 0;
  local_50 = (int *)((ulong)local_50 & 0xffffffffffffff00);
  local_38 = 0;
  uStack_30 = 0;
  local_28 = 0x3f800000;
  *(undefined1 *)(param_1 + 0x98) = 0;
  if (*(long *)(param_1 + 0xb8) != 0) {
    FUN_1031768f0(param_1 + 0xa0,*(undefined8 *)(param_1 + 0xb0));
    *(undefined8 *)(param_1 + 0xb0) = 0;
    lVar2 = *(long *)(param_1 + 0xa8);
    if (lVar2 != 0) {
      lVar4 = 0;
      do {
        *(undefined8 *)(*(long *)(param_1 + 0xa0) + lVar4 * 8) = 0;
        lVar4 = lVar4 + 1;
      } while (lVar2 != lVar4);
    }
    *(undefined8 *)(param_1 + 0xb8) = 0;
  }
  local_48 = (void *)0x0;
  pvVar3 = *(void **)(param_1 + 0xa0);
  *(undefined8 *)(param_1 + 0xa0) = 0;
  if (pvVar3 != (void *)0x0) {
    operator_delete(pvVar3);
  }
  *(undefined8 *)(param_1 + 0xa8) = 0;
  *(undefined8 *)(param_1 + 0xb0) = 0;
  local_40 = 0;
  *(undefined8 *)(param_1 + 0xb8) = 0;
  *(undefined4 *)(param_1 + 0xc0) = 0x3f800000;
  FUN_1031768f0(&local_48,0);
  pvVar3 = local_48;
  local_48 = (void *)0x0;
  if (pvVar3 != (void *)0x0) {
    operator_delete(pvVar3);
  }
  *(undefined4 *)(param_1 + 200) = 0;
  FUN_1011cb734(&local_50);
  FUN_10317ad9c(param_1,&local_50,0,0);
  if (local_50 != (int *)0x0) {
    iVar1 = *local_50;
    *local_50 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (*(char *)(param_1 + 0x60) != '\0') {
    *(undefined1 *)(param_1 + 0x60) = 0;
    FUN_1017cde1c(param_1 + 0x20,0);
  }
  return;
}


