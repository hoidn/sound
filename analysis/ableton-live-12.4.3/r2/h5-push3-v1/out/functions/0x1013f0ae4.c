// 0x1013f0ae4 FUN_1013f0ae4 state=exported-with-warnings role=async bulk IN transfer setup
// source chunk chunk-00893.jsonl; code_sha256=a8b69925597d5897b00c345948f151494717c219efc4038f6b968087f6319f1c

long FUN_1013f0ae4(long param_1,long param_2,long *param_3,long *param_4)

{
  long *plVar1;
  undefined8 uVar2;
  bad_alloc *this;
  
  plVar1 = (long *)param_3[3];
  if (plVar1 == (long *)0x0) {
    *(undefined8 *)(param_1 + 0x18) = 0;
    plVar1 = (long *)param_4[3];
    if (plVar1 != (long *)0x0) goto LAB_1013f0b68;
    uVar2 = 0;
  }
  else if (plVar1 == param_3) {
    *(long *)(param_1 + 0x18) = param_1;
    (**(code **)(*(long *)param_3[3] + 0x18))((long *)param_3[3],param_1);
    plVar1 = (long *)param_4[3];
    uVar2 = 0;
    if (plVar1 != (long *)0x0) goto LAB_1013f0b68;
  }
  else {
    uVar2 = (**(code **)(*plVar1 + 0x10))();
    *(undefined8 *)(param_1 + 0x18) = uVar2;
    plVar1 = (long *)param_4[3];
    if (plVar1 == (long *)0x0) {
      uVar2 = 0;
    }
    else {
LAB_1013f0b68:
      if (plVar1 == param_4) {
        *(long *)(param_1 + 0x38) = param_1 + 0x20;
        (**(code **)(*(long *)param_4[3] + 0x18))((long *)param_4[3],param_1 + 0x20);
        goto LAB_1013f0b9c;
      }
      uVar2 = (**(code **)(*plVar1 + 0x10))();
    }
  }
  *(undefined8 *)(param_1 + 0x38) = uVar2;
LAB_1013f0b9c:
  plVar1 = (long *)_libusb_alloc_transfer(0);
  *(long **)(param_1 + 0x240) = plVar1;
  if (param_2 == 0) {
    FUN_10030513c("pDeviceHandle","shared/push-usb-interface/src/LibUsbBulkTransfer.cpp",0xc9);
                    /* WARNING: Subroutine does not return */
    _abort();
  }
  if (plVar1 != (long *)0x0) {
    *plVar1 = param_2;
    *(undefined2 *)((long)plVar1 + 9) = 0x281;
    *(undefined4 *)((long)plVar1 + 0xc) = 0;
    plVar1[5] = param_1;
    plVar1[6] = param_1 + 0x40;
    *(undefined4 *)((long)plVar1 + 0x14) = 0x200;
    plVar1[4] = (long)FUN_1013f0c94;
    return param_1;
  }
  this = (bad_alloc *)___cxa_allocate_exception(8);
  uVar2 = std::bad_alloc::bad_alloc(this);
                    /* WARNING: Subroutine does not return */
  ___cxa_throw(uVar2,PTR_typeinfo_101b8c340,PTR__bad_alloc_101b8c2c8);
}

