// 0x100277ddc FUN_100277ddc state=exported role=UsbDisplay::transmitFrameBuffer
// source chunk chunk-00108.jsonl; code_sha256=34ff388b4497b92d500cf8f06e30a8d1a78dbee0e0dedea5f0de818498a025e9

void FUN_100277ddc(long param_1,undefined8 *param_2)

{
  void *pvVar1;
  int iVar2;
  long lVar3;
  undefined8 uVar4;
  undefined1 auStack_70 [8];
  uint local_68;
  undefined8 *local_60;
  long *plStack_58;
  long local_50;
  undefined8 local_48;
  void *local_40 [2];
  
  FUN_10066461c("UsbDisplay","transmitFrameBuffer");
  if ((*PTR_sLog_101b8cac8 & 1) == 0) {
    FUN_1014a8888();
  }
  uVar4 = *(undefined8 *)PTR_sLog_101ba0f90;
  local_48 = uVar4;
  lVar3 = _os_signpost_id_generate(uVar4);
  local_50 = lVar3;
  if ((lVar3 - 1U < 0xfffffffffffffffe) && (iVar2 = _os_signpost_enabled(uVar4), iVar2 != 0)) {
    local_60 = (undefined8 *)((ulong)local_60 & 0xffffffffffff0000);
    __os_signpost_emit_with_name_impl
              (0x100000000,uVar4,1,lVar3,"transmitFrameBuffer","",&local_60,2);
  }
  local_60 = &local_48;
  plStack_58 = &local_50;
  local_40[0] = (void *)*param_2;
  *param_2 = 0;
  (**(code **)(**(long **)(param_1 + 0x20) + 0x20))(auStack_70,*(long **)(param_1 + 0x20),local_40);
  pvVar1 = local_40[0];
  local_40[0] = (void *)0x0;
  if (pvVar1 != (void *)0x0) {
    operator_delete(pvVar1);
  }
  if (local_68 != 0xffffffff) {
    (*(code *)(&PTR_FUN_101bd61c8)[local_68])(local_40,auStack_70);
  }
  uVar4 = local_48;
  lVar3 = local_50;
  local_68 = 0xffffffff;
  if (local_50 - 1U < 0xfffffffffffffffe) {
    iVar2 = _os_signpost_enabled(local_48);
    if (iVar2 != 0) {
      local_40[0] = (void *)((ulong)local_40[0] & 0xffffffffffff0000);
      __os_signpost_emit_with_name_impl
                (0x100000000,uVar4,2,lVar3,"transmitFrameBuffer","",local_40,2);
    }
  }
  FUN_100664a3c("UsbDisplay","transmitFrameBuffer");
  return;
}

