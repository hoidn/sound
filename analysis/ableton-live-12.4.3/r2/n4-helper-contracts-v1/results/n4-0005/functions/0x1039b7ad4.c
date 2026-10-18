
/* void ableton::utility::detail::CallbackTypes<TPushClientConnection, void,
   TProcessObserver::State>::CallMemberFunc<&TPushClientConnection::OnPushProcessStateChanged>(void*,
   TProcessObserver::State) */

void ableton::utility::detail::CallbackTypes<TPushClientConnection,void,TProcessObserver::State>::
     CallMemberFunc<&TPushClientConnection::OnPushProcessStateChanged>(long param_1,uint param_2)

{
  undefined8 uVar1;
  
  if (((param_2 < 0xb) && ((1 << (ulong)(param_2 & 0x1f) & 0x610U) != 0)) &&
     ((*(byte *)(param_1 + 0x181) & 1) == 0)) {
    uVar1 = FUN_1038f2224();
    FUN_1038f0d24(uVar1,0x5dc);
    return;
  }
  return;
}

