// 0x1031b8c68 FUN_1031b8c68 exported-with-warnings  sig: undefined FUN_1031b8c68()

/* WARNING: Removing unreachable block (ram,0x0001031b8d1c) */
/* WARNING: Removing unreachable block (ram,0x0001031b8dc0) */

void FUN_1031b8c68(undefined8 *param_1,undefined8 param_2)

{
  void *pvVar1;
  void *pvVar2;
  int iVar3;
  long lVar4;
  int *piVar5;
  void *local_58;
  void *local_50;
  
  *param_1 = 0;
  param_1[1] = 0;
  param_1[2] = 0;
  lVar4 = FUN_1031b7670();
  if (lVar4 != 0) {
    iVar3 = FUN_1015645a0(*(undefined8 *)(lVar4 + 0x30));
    if (iVar3 != 0) {
      FUN_1031b8e5c(&local_58);
      FUN_1031c2d1c(param_1,param_1[1],local_58,local_50,(long)local_50 - (long)local_58 >> 5);
      pvVar1 = local_58;
      if (local_58 != (void *)0x0) {
        for (; local_50 != pvVar1; local_50 = (void *)((long)local_50 + -0x20)) {
          piVar5 = *(int **)((long)local_50 + -8);
          if ((piVar5 != (int *)0x0) && (iVar3 = *piVar5, *piVar5 = iVar3 + -1, iVar3 + -1 == 0)) {
            FUN_101449efc();
          }
        }
        local_50 = pvVar1;
        operator_delete(local_58);
      }
    }
    iVar3 = FUN_1015645a0(*(undefined8 *)(lVar4 + 0x48));
    if (iVar3 != 0) {
      FUN_1031b7f94(&local_58,param_2);
      FUN_1031c2d1c(param_1,param_1[1],local_58,local_50,(long)local_50 - (long)local_58 >> 5);
      pvVar2 = local_58;
      pvVar1 = local_50;
      if (local_58 != (void *)0x0) {
        for (; pvVar1 != pvVar2; pvVar1 = (void *)((long)pvVar1 + -0x20)) {
          piVar5 = *(int **)((long)pvVar1 + -8);
          if ((piVar5 != (int *)0x0) && (iVar3 = *piVar5, *piVar5 = iVar3 + -1, iVar3 + -1 == 0)) {
            FUN_101449efc();
          }
        }
        local_50 = pvVar2;
        operator_delete(local_58);
      }
    }
  }
  return;
}


