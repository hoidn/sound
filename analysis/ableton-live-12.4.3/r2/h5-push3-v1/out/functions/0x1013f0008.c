// 0x1013f0008 FUN_1013f0008 state=exported role=sync bulk IN endpoint 0x81
// source chunk chunk-00893.jsonl; code_sha256=0b16588e8a28699f6ab80870de32b76bf6ec96abd8aecf39b72ae8bd2475dbfd

long FUN_1013f0008(undefined8 param_1,undefined8 param_2,undefined8 param_3)

{
  int iVar1;
  undefined8 uVar2;
  undefined8 uVar3;
  undefined1 auStack_30 [12];
  int local_24;
  
  local_24 = 0;
  uVar2 = _libusb_bulk_transfer(param_1,0x81,param_2,param_3,&local_24,1000);
  if ((int)uVar2 != 0) {
    uVar3 = std::chrono::system_clock::now();
    FUN_1003324b0(auStack_30,4,uVar3);
    iVar1 = FUN_10032ece8(auStack_30);
    if (iVar1 != 0) {
      uVar3 = FUN_10032bea8(auStack_30,"USB bulk transfer failed: ");
      uVar2 = _libusb_strerror(uVar2);
      FUN_10032bea8(uVar3,uVar2);
    }
    thunk_FUN_10032ba14(auStack_30);
    return 0;
  }
  return (long)local_24;
}

