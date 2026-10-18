
void FUN_10151752c(long *param_1)

{
  char *pcVar1;
  undefined4 uVar2;
  long lVar3;
  ulong uVar4;
  
  *(int *)(param_1 + 0xb) = (int)param_1[0xb] + -1;
  lVar3 = *param_1;
  if ((int)param_1[3] == 2) {
    pcVar1 = " />";
  }
  else {
    (**(code **)(lVar3 + 0x28))(param_1);
    (**(code **)(*param_1 + 0x40))(param_1);
    (**(code **)(*param_1 + 0x38))(param_1,"</");
    uVar4 = (param_1[9] + param_1[8]) - 1;
    (**(code **)(*param_1 + 0x30))
              (param_1,*(long *)(param_1[5] + (uVar4 >> 6 & 0x3fffffffffffff8)) +
                       (uVar4 & 0x1ff) * 8);
    lVar3 = *param_1;
    pcVar1 = ">";
  }
  (**(code **)(lVar3 + 0x38))(param_1,pcVar1);
  FUN_101462cec(param_1 + 4);
  uVar2 = 5;
  if (param_1[9] != 0) {
    uVar2 = 3;
  }
  *(undefined4 *)(param_1 + 3) = uVar2;
  return;
}

