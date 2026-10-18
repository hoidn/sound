// 0x1013eff5c FUN_1013eff5c state=exported role=sync bulk OUT endpoint 0x01
// source chunk chunk-00893.jsonl; code_sha256=b7450f175cf4c06359800024809c7dd0e4ca2c41b57ae0072881b5ec5b34853c

bool FUN_1013eff5c(undefined8 param_1,undefined8 param_2,undefined8 param_3)

{
  int iVar1;
  undefined8 uVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  undefined1 auStack_28 [8];
  
  uVar2 = _libusb_bulk_transfer(param_1,1,param_2,param_3,0,1000);
  if ((int)uVar2 != 0) {
    uVar3 = std::chrono::system_clock::now();
    FUN_1003324b0(auStack_28,4,uVar3);
    iVar1 = FUN_10032ece8(auStack_28);
    if (iVar1 != 0) {
      uVar3 = FUN_10032bea8(auStack_28,"USB bulk transfer failed: ");
      uVar4 = _libusb_strerror(uVar2);
      FUN_10032bea8(uVar3,uVar4);
    }
    thunk_FUN_10032ba14(auStack_28);
  }
  return (int)uVar2 == 0;
}

