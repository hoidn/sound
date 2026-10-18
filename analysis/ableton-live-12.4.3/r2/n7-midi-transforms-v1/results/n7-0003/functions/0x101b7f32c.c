
void FUN_101b7f32c(undefined4 param_1,long param_2,undefined8 param_3,undefined8 *param_4,
                  undefined1 param_5)

{
  undefined8 uVar1;
  undefined8 uVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  
  *(undefined8 *)(param_2 + 0x18) = param_3;
  uVar2 = param_4[1];
  uVar1 = *param_4;
  uVar4 = param_4[3];
  uVar3 = param_4[2];
  *(undefined1 *)(param_2 + 0x40) = *(undefined1 *)(param_4 + 4);
  *(undefined8 *)(param_2 + 0x28) = uVar2;
  *(undefined8 *)(param_2 + 0x20) = uVar1;
  *(undefined8 *)(param_2 + 0x38) = uVar4;
  *(undefined8 *)(param_2 + 0x30) = uVar3;
  *(undefined1 *)(param_2 + 0x44) = param_5;
  *(undefined4 *)(param_2 + 0x48) = param_1;
  return;
}

