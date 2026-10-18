// 0x1013ebf50 FUN_1013ebf50 state=exported-with-warnings role=libusb hotplug registration
// source chunk chunk-00891.jsonl; code_sha256=d82878cc36177c71bf314ac4e5d79abfb2104eec1d86148150e5d612fea8ee0e

undefined8 * FUN_1013ebf50(undefined8 *param_1,long *param_2)

{
  int iVar1;
  undefined8 *puVar2;
  long *plVar3;
  undefined8 uVar4;
  long lVar5;
  long alStack_58 [3];
  long *local_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_101b8c408;
  puVar2 = operator_new(0x28);
  puVar2[1] = 0;
  *puVar2 = 0;
  puVar2[3] = 0;
  puVar2[2] = 0;
  puVar2[4] = 0;
  *param_1 = puVar2;
  plVar3 = (long *)param_2[3];
  local_40 = (long *)0x0;
  if (plVar3 != (long *)0x0) {
    if (plVar3 == param_2) {
      local_40 = alStack_58;
      (**(code **)(*plVar3 + 0x18))(plVar3,alStack_58);
    }
    else {
      local_40 = (long *)(**(code **)(*plVar3 + 0x10))();
    }
  }
  FUN_10029739c(alStack_58,puVar2 + 1);
  if (local_40 == alStack_58) {
    lVar5 = 0x20;
  }
  else {
    if (local_40 == (long *)0x0) goto LAB_1013ec00c;
    lVar5 = 0x28;
  }
  (**(code **)(*local_40 + lVar5))();
LAB_1013ec00c:
  _libusb_init(0);
  iVar1 = _libusb_hotplug_register_callback
                    (0,1,0,0x2982,0x1969,0xffffffff,FUN_1013ec10c,param_1,*param_1);
  if (iVar1 != 0) {
    uVar4 = std::chrono::system_clock::now();
    FUN_1003324b0(alStack_58,3,uVar4);
    iVar1 = FUN_10032ece8(alStack_58);
    if (iVar1 != 0) {
      FUN_10032bea8(alStack_58,"Could not create libusb hotplug callback");
    }
    thunk_FUN_10032ba14(alStack_58);
  }
  if (*(long *)PTR____stack_chk_guard_101b8c408 != local_38) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return param_1;
}

