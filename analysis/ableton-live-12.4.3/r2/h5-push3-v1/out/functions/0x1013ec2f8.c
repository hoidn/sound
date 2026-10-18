// 0x1013ec2f8 FUN_1013ec2f8 state=exported-with-warnings role=DisplayUsbCommunication ctor (16-byte header)
// source chunk chunk-00891.jsonl; code_sha256=ab0720b19b289b14f750b89b721d2c511d46398e2d96e0bdd489b0a2e127cc1c

undefined8 * FUN_1013ec2f8(undefined8 *param_1,long param_2,undefined8 param_3)

{
  long lVar1;
  undefined *local_c8;
  undefined8 uStack_c0;
  undefined **local_b8;
  undefined8 *puStack_b0;
  undefined ***local_a0;
  undefined **local_98;
  undefined8 *puStack_90;
  undefined ***local_80;
  undefined **local_78;
  undefined8 *puStack_70;
  undefined ***local_60;
  undefined **local_58 [3];
  undefined ***local_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_101b8c408;
  *param_1 = param_3;
  param_1[1] = 0;
  *(undefined4 *)(param_1 + 2) = 0;
  FUN_1013f1168(param_1 + 3);
  local_40 = local_58;
  local_58[0] = &PTR_FUN_101ca2108;
  local_78 = &PTR_FUN_101ca2198;
  puStack_70 = param_1;
  local_60 = &local_78;
  thunk_FUN_1013f00c8(param_1 + 7,param_2,local_58,&local_78);
  if (local_60 == &local_78) {
    lVar1 = 0x20;
LAB_1013ec38c:
    (**(code **)((long)*local_60 + lVar1))();
  }
  else if (local_60 != (undefined ***)0x0) {
    lVar1 = 0x28;
    goto LAB_1013ec38c;
  }
  if (local_40 == local_58) {
    lVar1 = 0x20;
LAB_1013ec3b8:
    (**(code **)((long)*local_40 + lVar1))();
  }
  else if (local_40 != (undefined ***)0x0) {
    lVar1 = 0x28;
    goto LAB_1013ec3b8;
  }
  local_98 = &PTR_FUN_101ca2228;
  local_80 = &local_98;
  local_b8 = &PTR_FUN_101ca22a8;
  puStack_b0 = param_1;
  local_a0 = &local_b8;
  puStack_90 = param_1;
  thunk_FUN_1013f00c8(param_1 + 0x10,param_2,&local_98,&local_b8);
  if (local_a0 == &local_b8) {
    lVar1 = 0x20;
LAB_1013ec41c:
    (**(code **)((long)*local_a0 + lVar1))();
  }
  else if (local_a0 != (undefined ***)0x0) {
    lVar1 = 0x28;
    goto LAB_1013ec41c;
  }
  if (local_80 == &local_98) {
    lVar1 = 0x20;
  }
  else {
    if (local_80 == (undefined ***)0x0) goto LAB_1013ec454;
    lVar1 = 0x28;
  }
  (**(code **)((long)*local_80 + lVar1))();
LAB_1013ec454:
  if (param_2 == 0) {
    FUN_10030513c("pDeviceHandle","shared/push-usb-interface/src/DisplayUsbCommunication.cpp",0x50);
                    /* WARNING: Subroutine does not return */
    _abort();
  }
  local_c8 = &DAT_101809960;
  uStack_c0 = 0x10;
  FUN_1013f053c(param_1 + 7,&local_c8);
  if (*(long *)PTR____stack_chk_guard_101b8c408 == local_38) {
    return param_1;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

