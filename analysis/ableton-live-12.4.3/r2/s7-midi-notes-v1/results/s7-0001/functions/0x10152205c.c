
void FUN_10152205c(long *param_1,undefined8 param_2,uint *param_3,undefined8 param_4)

{
  char *pcVar1;
  int iVar2;
  undefined8 uVar3;
  uint uVar4;
  int *local_48;
  undefined4 local_40;
  undefined1 auStack_35 [5];
  
  iVar2 = FUN_10120e264(param_4);
  if (0x13 < iVar2) {
    if (iVar2 < 0x18) {
      if (iVar2 == 0x14) {
        FUN_101449838(&local_48);
        local_40 = 0;
        FUN_101522b50(&local_48,param_3);
        (**(code **)(*param_1 + 0x38))(param_1," ");
        (**(code **)(*param_1 + 0x30))(param_1,param_2);
        FUN_1011bfe14(auStack_35,5,"=%c");
        (**(code **)(*param_1 + 0x38))(param_1,auStack_35);
        *(undefined4 *)(param_1 + 3) = 4;
        FUN_101522dfc(param_1[10],&local_48);
        FUN_1011bfe14(auStack_35,5,"%c");
        (**(code **)(*param_1 + 0x38))(param_1,auStack_35);
        *(undefined4 *)(param_1 + 3) = 2;
        if ((local_48 != (int *)0x0) && (iVar2 = *local_48, *local_48 = iVar2 + -1, iVar2 + -1 == 0)
           ) {
          FUN_101449efc();
        }
      }
      else if (iVar2 == 0x17) {
        (**(code **)(*param_1 + 0x38))(param_1," ");
        (**(code **)(*param_1 + 0x30))(param_1,param_2);
        FUN_1011bfe14(&local_48,5,"=%c");
        (**(code **)(*param_1 + 0x38))(param_1,&local_48);
        *(undefined4 *)(param_1 + 3) = 4;
        FUN_101520dbc(*(undefined8 *)param_3,param_1);
        goto LAB_101522510;
      }
    }
    else {
      if (iVar2 == 0x18) {
        (**(code **)(*param_1 + 0x38))(param_1," ");
        (**(code **)(*param_1 + 0x30))(param_1,param_2);
        FUN_1011bfe14(&local_48,5,"=%c");
        (**(code **)(*param_1 + 0x38))(param_1,&local_48);
        *(undefined4 *)(param_1 + 3) = 4;
        FUN_101430fc4(&local_48,*(undefined8 *)param_3);
        (**(code **)(*param_1 + 0x30))(param_1,&local_48);
        if ((local_48 != (int *)0x0) && (iVar2 = *local_48, *local_48 = iVar2 + -1, iVar2 + -1 == 0)
           ) {
          FUN_101449efc();
        }
        goto LAB_101522510;
      }
      if (iVar2 == 0x19) {
        FUN_101449838(&local_48);
        local_40 = 0;
        uVar3 = FUN_101290c14(param_3);
        FUN_101522b50(&local_48,uVar3);
        (**(code **)(*param_1 + 0x38))(param_1," ");
        (**(code **)(*param_1 + 0x30))(param_1,param_2);
        FUN_1011bfe14(auStack_35,5,"=%c");
        (**(code **)(*param_1 + 0x38))(param_1,auStack_35);
        *(undefined4 *)(param_1 + 3) = 4;
        FUN_101522dfc(param_1[10],&local_48);
        FUN_1011bfe14(auStack_35,5,"%c");
        (**(code **)(*param_1 + 0x38))(param_1,auStack_35);
        *(undefined4 *)(param_1 + 3) = 2;
        if ((local_48 != (int *)0x0) && (iVar2 = *local_48, *local_48 = iVar2 + -1, iVar2 + -1 == 0)
           ) {
          FUN_101449efc();
        }
      }
    }
    return;
  }
  if (iVar2 < 0x12) {
    if (iVar2 == 0x10) {
      (**(code **)(*param_1 + 0x38))(param_1," ");
      (**(code **)(*param_1 + 0x30))(param_1,param_2);
      FUN_1011bfe14(&local_48,5,"=%c");
      (**(code **)(*param_1 + 0x38))(param_1,&local_48);
      *(undefined4 *)(param_1 + 3) = 4;
      pcVar1 = "true";
      if ((char)*param_3 == '\0') {
        pcVar1 = "false";
      }
      (**(code **)(*param_1 + 0x38))(param_1,pcVar1);
      goto LAB_101522510;
    }
    if (iVar2 != 0x11) {
      return;
    }
    (**(code **)(*param_1 + 0x38))(param_1," ");
    (**(code **)(*param_1 + 0x30))(param_1,param_2);
    FUN_1011bfe14(&local_48,5,"=%c");
    (**(code **)(*param_1 + 0x38))(param_1,&local_48);
    *(undefined4 *)(param_1 + 3) = 4;
    uVar4 = *param_3;
  }
  else {
    if (iVar2 == 0x12) {
      (**(code **)(*param_1 + 0x38))(param_1," ");
      (**(code **)(*param_1 + 0x30))(param_1,param_2);
      FUN_1011bfe14(&local_48,5,"=%c");
      (**(code **)(*param_1 + 0x38))(param_1,&local_48);
      *(undefined4 *)(param_1 + 3) = 4;
      FUN_101520c70(*param_3,param_1);
      goto LAB_101522510;
    }
    if (iVar2 != 0x13) {
      return;
    }
    (**(code **)(*param_1 + 0x38))(param_1," ");
    (**(code **)(*param_1 + 0x30))(param_1,param_2);
    FUN_1011bfe14(&local_48,5,"=%c");
    (**(code **)(*param_1 + 0x38))(param_1,&local_48);
    *(undefined4 *)(param_1 + 3) = 4;
    uVar4 = (uint)(ushort)*param_3;
  }
  FUN_101520b2c(param_1,uVar4);
LAB_101522510:
  FUN_1011bfe14(&local_48,5,"%c");
  (**(code **)(*param_1 + 0x38))(param_1,&local_48);
  *(undefined4 *)(param_1 + 3) = 2;
  return;
}

