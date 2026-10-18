
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* void ableton::utility::detail::CallbackTypes<TPushClientConnection, void, TMidiDeviceStateChanges
   const&>::CallMemberFunc<&TPushClientConnection::OnMidiDevicesChanged>(void*,
   TMidiDeviceStateChanges const&) */

void ableton::utility::detail::
     CallbackTypes<TPushClientConnection,void,TMidiDeviceStateChanges_const&>::
     CallMemberFunc<&TPushClientConnection::OnMidiDevicesChanged>
               (void *param_1,TMidiDeviceStateChanges *param_2)

{
  int iVar1;
  undefined8 uVar2;
  uint extraout_w1;
  undefined8 local_40;
  undefined8 uStack_38;
  undefined8 uStack_30;
  undefined8 uStack_28;
  
  uVar2 = FUN_1038f2224(param_1,(int)param_2);
  FUN_1022a9658();
  iVar1 = FUN_1022bcb4c();
  if (iVar1 == 0) {
    uStack_38 = _UNK_105942250;
    local_40 = _DAT_105942248;
    uStack_28 = _UNK_105942260;
    uStack_30 = _DAT_105942258;
    FUN_1011aeb80(&local_40);
    *(byte *)((long)param_1 + 0x182) = (byte)extraout_w1 & 1;
    if ((extraout_w1 & 1) == 0) {
      FUN_1038f0838(uVar2);
      *(undefined1 *)((long)param_1 + 0x181) = 0;
      return;
    }
  }
  else {
    *(undefined1 *)((long)param_1 + 0x182) = 1;
  }
  if (*(char *)((long)param_1 + 0x180) == '\x01') {
    FUN_1038f08c4(uVar2);
  }
  return;
}

