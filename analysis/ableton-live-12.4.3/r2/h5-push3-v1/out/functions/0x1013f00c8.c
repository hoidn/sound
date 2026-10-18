// 0x1013f00c8 FUN_1013f00c8 state=exported-with-warnings role=async bulk OUT transfer setup
// source chunk chunk-00893.jsonl; code_sha256=900940cc91568937667052dafb7c4aeabd627d7eb8dd56b3bf6006708075a9ca

long FUN_1013f00c8(long param_1,long param_2,long *param_3,long *param_4)

{
  long *plVar1;
  undefined8 uVar2;
  bad_alloc *this;
  
  plVar1 = (long *)param_3[3];
  if (plVar1 == (long *)0x0) {
    *(undefined8 *)(param_1 + 0x18) = 0;
    plVar1 = (long *)param_4[3];
    if (plVar1 != (long *)0x0) goto LAB_1013f014c;
    uVar2 = 0;
  }
  else if (plVar1 == param_3) {
    *(long *)(param_1 + 0x18) = param_1;
    (**(code **)(*(long *)param_3[3] + 0x18))((long *)param_3[3],param_1);
    plVar1 = (long *)param_4[3];
    uVar2 = 0;
    if (plVar1 != (long *)0x0) goto LAB_1013f014c;
  }
  else {
    uVar2 = (**(code **)(*plVar1 + 0x10))();
    *(undefined8 *)(param_1 + 0x18) = uVar2;
    plVar1 = (long *)param_4[3];
    if (plVar1 == (long *)0x0) {
      uVar2 = 0;
    }
    else {
LAB_1013f014c:
      if (plVar1 == param_4) {
        *(long *)(param_1 + 0x38) = param_1 + 0x20;
        (**(code **)(*(long *)param_4[3] + 0x18))((long *)param_4[3],param_1 + 0x20);
        goto LAB_1013f0180;
      }
      uVar2 = (**(code **)(*plVar1 + 0x10))();
    }
  }
  *(undefined8 *)(param_1 + 0x38) = uVar2;
LAB_1013f0180:
  plVar1 = (long *)_libusb_alloc_transfer(0);
  *(long **)(param_1 + 0x40) = plVar1;
  if (param_2 == 0) {
    FUN_10030513c("pDeviceHandle","shared/push-usb-interface/src/LibUsbBulkTransfer.cpp",0x4d);
                    /* WARNING: Subroutine does not return */
    _abort();
  }
  if (plVar1 != (long *)0x0) {
    *plVar1 = param_2;
    *(undefined2 *)((long)plVar1 + 9) = 0x201;
    *(undefined4 *)((long)plVar1 + 0xc) = 1000;
    plVar1[5] = param_1;
    plVar1[6] = 0;
    *(undefined4 *)((long)plVar1 + 0x14) = 0;
    plVar1[4] = (long)FUN_1013f0274;
    return param_1;
  }
  this = (bad_alloc *)___cxa_allocate_exception(8);
  uVar2 = std::bad_alloc::bad_alloc(this);
                    /* WARNING: Subroutine does not return */
  ___cxa_throw(uVar2,PTR_typeinfo_101b8c340,PTR__bad_alloc_101b8c2c8);
}

