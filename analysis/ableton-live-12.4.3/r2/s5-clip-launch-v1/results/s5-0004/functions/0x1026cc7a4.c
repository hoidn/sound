
/* void ableton::utility::detail::CallbackTypes<LSongUnit, void, ARemoteable*,
   TRemoteableUpdate>::CallMemberFunc<&LSongUnit::OnGlobalQuantizationChanged>(void*, ARemoteable*,
   TRemoteableUpdate) */

void ableton::utility::detail::CallbackTypes<LSongUnit,void,ARemoteable*,TRemoteableUpdate>::
     CallMemberFunc<&LSongUnit::OnGlobalQuantizationChanged>
               (long param_1,undefined8 param_2,uint param_3)

{
  undefined8 uVar1;
  long local_40;
  undefined8 local_38;
  
  if ((param_3 < 2) && (*(long *)(param_1 + 0x18) != 0)) {
    FUN_101ab7348(&local_40,&DAT_10700ca58,0x100500,0x10100,0);
    FUN_101a9c618(local_38,*(undefined8 *)(param_1 + 0x20));
    uVar1 = FUN_1015661b8(*(undefined8 *)(*(long *)(param_1 + 0x78) + 0x388));
    FUN_101a9c534(local_38,uVar1);
    (**(code **)(local_40 + 0x10))(&local_40);
    FUN_101ab786c(&local_40);
  }
  return;
}

