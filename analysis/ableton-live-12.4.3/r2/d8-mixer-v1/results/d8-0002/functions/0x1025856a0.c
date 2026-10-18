
void FUN_1025856a0(undefined8 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
                  long param_5,long *param_6)

{
  undefined *puVar1;
  undefined8 uVar2;
  undefined4 uVar3;
  undefined4 uVar4;
  undefined *local_50;
  long lStack_48;
  
  if ((*(byte *)(param_5 + 0x5c) & 1) == 0) {
    *(undefined1 *)(param_5 + 0x5c) = 1;
  }
  *(int *)(param_5 + 0x58) = (int)param_1;
  if ((*(byte *)(param_5 + 100) & 1) == 0) {
    *(undefined1 *)(param_5 + 100) = 1;
  }
  *(undefined4 *)(param_5 + 0x60) = param_2;
  uVar2 = *(undefined8 *)(param_5 + 0x30);
  uVar3 = (**(code **)(*param_6 + 0x30))(param_1,param_3,param_4,param_6);
  puVar1 = PTR_CallMemberFunc<&AMidiControllerRange::OnMinOrMaxChanged>_10652fd48;
  local_50 = PTR_CallMemberFunc<&AMidiControllerRange::OnMinOrMaxChanged>_10652fd48;
  lStack_48 = param_5;
  FUN_10157432c(param_3,param_4,uVar3,uVar2,param_6,&local_50);
  uVar2 = *(undefined8 *)(param_5 + 0x48);
  uVar3 = (**(code **)(*param_6 + 0x30))(*(undefined4 *)(param_5 + 0x60),param_3,param_4,param_6);
  local_50 = puVar1;
  lStack_48 = param_5;
  FUN_10157432c(param_3,param_4,uVar3,uVar2,param_6,&local_50);
  uVar4 = 0;
  uVar3 = 0;
  if (*(char *)(param_5 + 0x5c) == '\x01') {
    uVar3 = *(undefined4 *)(param_5 + 0x58);
  }
  local_50._0_4_ = uVar3;
  FUN_101574564(*(undefined8 *)(param_5 + 0x30),&local_50);
  if (*(char *)(param_5 + 100) == '\x01') {
    uVar4 = *(undefined4 *)(param_5 + 0x60);
  }
  local_50 = (undefined *)CONCAT44(local_50._4_4_,uVar4);
  FUN_101574564(*(undefined8 *)(param_5 + 0x48),&local_50);
  return;
}

