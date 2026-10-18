
void FUN_1015170e0(long *param_1,long *param_2)

{
  ulong uVar1;
  int iVar2;
  undefined8 uVar3;
  undefined8 *puVar4;
  int iVar5;
  long lVar6;
  long lVar7;
  ulong uVar8;
  int *local_50;
  int *local_48;
  int *local_40;
  int *local_38;
  
  if ((int)param_1[3] == 2) {
    (**(code **)(*param_1 + 0x38))(param_1,">");
  }
  uVar3 = FUN_101428734(param_2,0x5b,1,0);
  iVar2 = (int)uVar3;
  if (iVar2 < 0) {
    local_50 = (int *)*param_2;
    if (local_50 != (int *)0x0) {
      *local_50 = *local_50 + 1;
    }
  }
  else {
    FUN_1011cb734(&local_40);
    FUN_10142881c(&local_48,param_2,0,uVar3);
    uVar3 = FUN_10142da5c(&local_40,&local_48);
    FUN_101427680(&local_38,".");
    uVar3 = FUN_10142da5c(uVar3,&local_38);
    if (local_38 != (int *)0x0) {
      iVar5 = *local_38;
      *local_38 = iVar5 + -1;
      if (iVar5 + -1 == 0) {
        FUN_101449efc();
      }
    }
    if (*param_2 == 0) {
      iVar5 = -1;
    }
    else {
      iVar5 = *(int *)(*param_2 + 4) / 2 + -1;
    }
    FUN_10142881c(&local_38,param_2,iVar2 + 1,(iVar5 - iVar2) + -2);
    puVar4 = (undefined8 *)FUN_10142da5c(uVar3,&local_38);
    local_50 = (int *)*puVar4;
    if (local_50 != (int *)0x0) {
      *local_50 = *local_50 + 1;
    }
    if (local_38 != (int *)0x0) {
      iVar2 = *local_38;
      *local_38 = iVar2 + -1;
      if (iVar2 + -1 == 0) {
        FUN_101449efc();
      }
    }
    if (local_48 != (int *)0x0) {
      iVar2 = *local_48;
      *local_48 = iVar2 + -1;
      if (iVar2 + -1 == 0) {
        FUN_101449efc();
      }
    }
    if (local_40 != (int *)0x0) {
      iVar2 = *local_40;
      *local_40 = iVar2 + -1;
      if (iVar2 + -1 == 0) {
        FUN_101449efc();
      }
    }
  }
  (**(code **)(*param_1 + 0x28))(param_1);
  (**(code **)(*param_1 + 0x40))(param_1);
  (**(code **)(*param_1 + 0x38))(param_1,"<");
  (**(code **)(*param_1 + 0x30))(param_1,&local_50);
  lVar6 = param_1[5];
  *(undefined4 *)(param_1 + 3) = 2;
  uVar1 = 0;
  if (param_1[6] != lVar6) {
    uVar1 = (param_1[6] - lVar6) * 0x40 - 1;
  }
  lVar7 = param_1[9];
  uVar8 = lVar7 + param_1[8];
  if (uVar1 == uVar8) {
    FUN_10062f02c(param_1 + 4);
    lVar6 = param_1[5];
    lVar7 = param_1[9];
    uVar8 = param_1[8] + lVar7;
  }
  *(int **)(*(long *)(lVar6 + (uVar8 >> 6 & 0x3fffffffffffff8)) + (uVar8 & 0x1ff) * 8) = local_50;
  if (local_50 != (int *)0x0) {
    iVar2 = *local_50;
    param_1[9] = lVar7 + 1;
    *(int *)(param_1 + 0xb) = (int)param_1[0xb] + 1;
    if (iVar2 == 0) {
      FUN_101449efc();
    }
    return;
  }
  param_1[9] = lVar7 + 1;
  *(int *)(param_1 + 0xb) = (int)param_1[0xb] + 1;
  return;
}

