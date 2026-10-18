// 0x1031c0144 FUN_1031c0144 exported  sig: undefined FUN_1031c0144()

void FUN_1031c0144(undefined8 *param_1,long *param_2)

{
  ulong uVar1;
  undefined8 *puVar2;
  int iVar3;
  undefined8 uVar4;
  uint uVar5;
  int *local_40;
  void *local_38;
  ulong uStack_30;
  undefined7 local_28;
  byte bStack_21;
  
  *param_1 = 0;
  param_1[1] = 0;
  param_1[2] = 0;
  (**(code **)(*param_2 + 0x98))(&local_38);
  uVar5 = (uint)(char)bStack_21;
  uVar1 = uStack_30;
  if (-1 < (int)uVar5) {
    uVar1 = (ulong)bStack_21;
  }
  if (uVar1 != 0) {
    FUN_101427680(&local_40,"custom");
    puVar2 = (undefined8 *)param_1[1];
    if (puVar2 < (undefined8 *)param_1[2]) {
      if ((char)bStack_21 < '\0') {
        FUN_10023448c(puVar2,local_38,uStack_30);
      }
      else {
        puVar2[2] = CONCAT17(bStack_21,local_28);
        puVar2[1] = uStack_30;
        *puVar2 = local_38;
      }
      puVar2[3] = local_40;
      param_1[1] = puVar2 + 4;
    }
    else {
      uVar4 = FUN_1031c36ac(param_1,&local_38,&local_40);
      param_1[1] = uVar4;
      if (local_40 != (int *)0x0) {
        iVar3 = *local_40;
        *local_40 = iVar3 + -1;
        if (iVar3 + -1 == 0) {
          FUN_101449efc();
        }
      }
    }
    uVar5 = (uint)bStack_21;
  }
  if ((uVar5 >> 7 & 1) == 0) {
    return;
  }
  operator_delete(local_38);
  return;
}


