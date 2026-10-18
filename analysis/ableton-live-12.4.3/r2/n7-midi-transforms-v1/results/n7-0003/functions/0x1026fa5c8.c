
void FUN_1026fa5c8(undefined8 *param_1,undefined4 param_2,undefined8 param_3,undefined8 param_4)

{
  undefined4 uVar1;
  long lVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  undefined1 auVar5 [16];
  
  lVar2 = FUN_1026e8ccc();
  if (lVar2 == 0) {
    param_1[4] = 0;
    param_1[1] = 0;
    *param_1 = 0;
    param_1[3] = 0;
    param_1[2] = 0;
  }
  else {
    auVar5 = FUN_1026fa684(param_3,param_4);
    uVar3 = (**(code **)(**(long **)(lVar2 + 0x88) + 0x290))();
    uVar1 = *(undefined4 *)(lVar2 + 0x78);
    uVar4 = FUN_1026e88e8(param_3);
    FUN_101b7c214(param_2,param_1,auVar5._0_8_,auVar5._8_8_ & 0xffffffffffff,uVar3,uVar1,uVar4);
  }
  *(bool *)((long)param_1 + 0x24) = lVar2 != 0;
  return;
}

